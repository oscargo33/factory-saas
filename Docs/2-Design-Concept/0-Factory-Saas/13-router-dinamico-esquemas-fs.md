# Documento: 13-router-dinamico-esquemas-fs.md

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** DC-13-FS
**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/13-router-dinamico-esquemas-fs.md`
**Referencia Core:** `0-factory_saas-cc.md`
**Capa:** 5 — Multi-Tenancy (Middleware y Schema Routing)
**Apellido:** **-fs**

---

## 1. Propósito

La Capa 5 es el núcleo del aislamiento multi-tenant de la Factory. Define cómo cada request HTTP es asociado a un tenant específico y cómo el ORM de Django es dirigido al esquema PostgreSQL correcto para ese tenant.

---

## 2. Modelo de Aislamiento: Schema-per-Tenant

Cada tenant tiene su propio **esquema PostgreSQL** (`search_path`). Las tablas del sistema (Users, Tenants, Memberships) viven en el esquema `public`. Los datos de negocio de cada tenant viven en `tenant_{slug}`.

```
PostgreSQL (única instancia, único DB)
│
├── schema: public
│   ├── users
│   ├── tenants
│   └── memberships
│
├── schema: tenant_acme
│   ├── orders
│   ├── products
│   └── ...
│
└── schema: tenant_globex
    ├── orders
    ├── products
    └── ...
```

Este modelo garantiza que **una consulta en el contexto del tenant ACME jamás puede ver datos del tenant GLOBEX**, por construcción a nivel de base de datos.

---

## 3. Flujo Completo de un Request

```
GET https://acme.factory.com/dashboard/
        │
        ▼
[Nginx] Host: acme.factory.com → proxy_pass a Gunicorn con Host intacto
        │
        ▼
[TenantMiddleware]
  1. Extrae subdomain: "acme" del header Host
  2. Busca en cache Redis (DB 0) → clave: tenant:slug:acme
  3. Si no está en cache → SELECT FROM public.tenants WHERE slug='acme'
  4. Si no existe tenant → responde 404 JSON {"error": "tenant_not_found"}
  5. Si existe → establece request.tenant = <instancia Tenant>
  6. Inserta Tenant en cache por 5 minutos
        │
        ▼
[TenantSchemaRouter]
  Llama: SET search_path TO tenant_acme, public
  (esto es inyectado en el callback cursor_created de django-tenants o via DatabaseWrapper)
        │
        ▼
[View] → consultas ORM operan en tenant_acme automáticamente
```

---

## 4. Diseño del `TenantMiddleware`

### 4.1. Extracción del Subdominio

El middleware extrae el slug del tenant desde el header `Host`:
- `acme.factory.com` → slug = `acme`
- `factory.com` (sin subdominio) → ruta al tenant raíz o landing page
- `localhost` / `127.0.0.1` → usar `DEFAULT_TENANT_SLUG` de settings para desarrollo

| Caso | Acción |
|---|---|
| Tenant encontrado, activo | `request.tenant = tenant`; continúa pipeline |
| Tenant encontrado, inactivo | Responde `403` con `{"error": "tenant_suspended"}` |
| Tenant no encontrado | Responde `404` con `{"error": "tenant_not_found"}` |
| Request al dominio raíz | `request.tenant = None`; continúa (landing page pública) |

### 4.2. Caché de Tenants

Para evitar una consulta a la DB en cada request, el middleware cachea el objeto Tenant serializado en Redis (DB 0):

| Parámetro caché | Valor |
|---|---|
| Clave | `tenant:slug:{slug}` |
| TTL | 300 segundos (5 min) |
| Invalidación | Al actualizar el registro del Tenant vía signal `post_save` |

---

## 5. Diseño del `TenantSchemaRouter`

El router de base de datos extiende el comportamiento estándar de Django para inyectar el `search_path` correcto.

### 5.1. Métodos del Router

| Método | Lógica |
|---|---|
| `db_for_read(model, **hints)` | Retorna `"default"` (única DB); el schema se maneja via `search_path` |
| `db_for_write(model, **hints)` | Ídem |
| `allow_migrate(db, app_label, **hints)` | Retorna `True` solo para el esquema activo actual |

### 5.2. Inyección del `search_path`

La inyección usa el mecanismo de `connection.set_tenant()` (si se usa `django-tenants`) o una señal `connection_created` que ejecuta:

```sql
SET search_path TO tenant_{slug}, public;
```

En contexto de tarea Celery, el `search_path` debe establecerse explícitamente al inicio de cada tarea usando un context manager `with tenant_context(tenant):`.

---

## 6. Comando de Bootstrap de Tenant

Al crear un nuevo tenant, se ejecuta el comando de gestión `bootstrap_tenant`:

| Paso | Acción |
|---|---|
| 1 | `CREATE SCHEMA IF NOT EXISTS tenant_{slug}` |
| 2 | `SET search_path TO tenant_{slug}, public` |
| 3 | `python manage.py migrate --schema=tenant_{slug}` |
| 4 | `seed_tenant_defaults(tenant)` — datos de catálogo iniciales |

Este comando es invocado por el service `create_tenant()` (Capa 4) al final de la transacción de creación.

---

## 7. Consideraciones de Desarrollo Local

En entorno de desarrollo, para facilitar las pruebas:

| Variable de entorno | Uso |
|---|---|
| `DEFAULT_TENANT_SLUG` | Slug del tenant a usar cuando el dominio es `localhost` |
| `BYPASS_TENANT_MIDDLEWARE` | `True` para deshabilitar la extracción de subdominio (solo en tests) |

---

## 8. Relación con Otros Documentos

| Documento | Relación |
|---|---|
| DC-9 `9-configuracion-postgresql-fs.md` | Define el esquema PostgreSQL que este router manipula |
| DC-10 `10-gateway-nginx-fs.md` | Nginx pasa el header `Host` que este middleware lee |
| DC-11 `11-configuracion-redis-celery-fs.md` | El middleware usa Redis DB 0 para el caché de tenants |
| DC-12 `12-patron-service-layer-fs.md` | `create_tenant()` service invoca `bootstrap_tenant` |

---

## 9. Criterios de Aceptación del Diseño

- [ ] Un request a un slug inexistente retorna `404` JSON antes de llegar a la vista.
- [ ] El objeto Tenant es cacheado en Redis por 5 minutos.
- [ ] El `search_path` es establecido correctamente antes de cualquier consulta ORM.
- [ ] Las tareas Celery aceptan un `tenant_id` en el payload y establecen el contexto de tenant antes de ejecutar.
- [ ] `BYPASS_TENANT_MIDDLEWARE` solo está disponible en entorno de tests; no en producción.
- [ ] El comando `bootstrap_tenant` crea el esquema y ejecuta migraciones en una sola operación atómica.
