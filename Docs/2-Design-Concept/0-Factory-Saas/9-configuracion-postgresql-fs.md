# Documento: 9-configuracion-postgresql-fs.md

**ID:** DC-9-FS
**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/9-configuracion-postgresql-fs.md`
**Referencia Core:** `0-factory_saas-cc.md`
**Capa:** 2 — Persistencia y Almacenamiento
**Apellido:** **-fs**

---

## 1. Propósito

PostgreSQL 16 es la columna vertebral de la Factory. Este documento define:
- La estrategia de **aislamiento por esquema** (multi-tenancy).
- Las **extensiones requeridas** para las capacidades del ecosistema.
- El **tuning de configuración** para ambientes de producción.
- La **estructura de esquemas** que toda la plataforma respeta.

---

## 2. Estrategia de Multi-Tenancy por Esquemas

La Factory utiliza el patrón **Schema-per-Tenant** de PostgreSQL:

```
factory_db (base de datos única)
├── public/                     ← Esquema global compartido
│   ├── profiles_user           ← User (identidad global)
│   ├── profiles_tenant         ← Tenant (registro de inquilinos)
│   ├── profiles_membership     ← Membership (roles por tenant)
│   ├── telemetry_auditlog      ← Auditoría global
│   └── telemetry_pendingmetrics← Buffer de métricas
│
├── tenant_acme/                ← Esquema del tenant "Acme Corp"
│   ├── orchestrator_product
│   ├── orchestrator_entitlement
│   ├── orders_cart
│   ├── orders_order
│   ├── payments_invoice
│   └── support_ticket
│
└── tenant_globex/              ← Esquema del tenant "Globex Inc"
    └── ... (misma estructura)
```

### Regla de Aislamiento
- **NUNCA** mezclar datos de dos tenants en una query.
- El `search_path` de PostgreSQL determina qué esquema está activo por conexión.
- El middleware de Django (DC-13) se encarga de inyectar el `search_path` correcto en cada request.

---

## 3. Extensiones Requeridas

Las siguientes extensiones deben activarse en el esquema `public` durante la inicialización:

| Extensión | Versión | Uso en el Proyecto |
|---|---|---|
| `uuid-ossp` | Incluida en PostgreSQL 16 | Generación de UUIDs como primary keys en todas las tablas |
| `pgvector` | 0.7+ | Búsqueda semántica vectorial para el RAG del Agente IA (App 8 Support) |

### Script de Inicialización (`init-db.sql`)
Se ejecuta una sola vez al crear la base de datos (montado en `/docker-entrypoint-initdb.d/`):

```sql
-- Activar extensiones en el esquema public
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Crear rol de lectura para reportes
CREATE ROLE factory_readonly;
GRANT CONNECT ON DATABASE factory_db TO factory_readonly;
```

---

## 4. Configuración de PostgreSQL (`postgresql.conf`)

Parámetros clave para el contexto de la Factory (ajustar según RAM disponible):

### 4.1. Memoria

| Parámetro | Valor Recomendado (4GB RAM) | Descripción |
|---|---|---|
| `shared_buffers` | `1GB` | Caché interna de PostgreSQL (25% de RAM) |
| `work_mem` | `16MB` | Memoria por operación de sort/hash |
| `maintenance_work_mem` | `256MB` | Memoria para VACUUM y creación de índices |
| `effective_cache_size` | `3GB` | Estimación total de caché disponible (para el planner) |

### 4.2. Conexiones

| Parámetro | Valor | Descripción |
|---|---|---|
| `max_connections` | `100` | Máximo de conexiones simultáneas |
| `connection_idle_in_transaction_session_timeout` | `60s` | Mata transacciones idle para evitar bloqueos |

> **Nota:** Para producción con múltiples tenants activos, se recomienda añadir **PgBouncer** como pooler de conexiones entre Django y PostgreSQL.

### 4.3. Logging (Auditoría)

| Parámetro | Valor | Descripción |
|---|---|---|
| `log_min_duration_statement` | `1000` | Loguear queries que tarden más de 1 segundo |
| `log_connections` | `on` | Registrar conexiones (trazabilidad de acceso) |
| `log_disconnections` | `on` | Registrar desconexiones |

### 4.4. Write-Ahead Log (Durabilidad)

| Parámetro | Valor | Descripción |
|---|---|---|
| `wal_level` | `replica` | Habilitar replicación futura |
| `checkpoint_completion_target` | `0.9` | Reducir I/O spikes en checkpoints |

---

## 5. Gestión de Volúmenes de Datos

| Volumen Docker | Ruta en Contenedor | Contenido |
|---|---|---|
| `db_data_fs` | `/var/lib/postgresql/data` | Todos los datos de todos los esquemas (tenants + public) |
| `db_init_fs` | `/docker-entrypoint-initdb.d/` | Scripts SQL de inicialización (solo se ejecutan una vez) |

---

## 6. Estrategia de Backups

El diseño contempla dos niveles de backup:

### 6.1. Backup Lógico (por tenant)
Usando `pg_dump` con `--schema=tenant_X` permite hacer backup o migrar un tenant individual sin afectar a los demás. Útil para:
- Exportar datos de un cliente que cancela.
- Restaurar un tenant a un punto en el tiempo.

### 6.2. Backup Físico (toda la base)
`pg_basebackup` para backup completo de todos los tenants. Ejecutar desde un contenedor sidecar en CI/CD. Fuera del scope de Fase 1.

---

## 7. Restricciones de Seguridad

- El usuario de Django (`factory_user`) **nunca** tiene permisos de `SUPERUSER`.
- El usuario de Django tiene: `CONNECT`, `CREATE SCHEMA`, `USAGE`, `SELECT`, `INSERT`, `UPDATE`, `DELETE` en los esquemas que le pertenecen.
- La extensión `pgvector` requiere un usuario con permisos de `SUPERUSER` solo durante la instalación inicial (via `init-db.sql` ejecutado por el usuario `postgres`).
- El puerto `5432` **nunca** se expone en `docker-compose.yml` a la red `frontnet_fs`; solo accesible desde `backnet_fs`.

---

## 8. Relación con Otros Documentos

| Documento | Relación |
|---|---|
| DC-7 `7-docker-compose-specs-fs.md` | Define el servicio `db` y el volumen `db_data_fs` |
| DC-8 `8-entrypoint-specs-fs.md` | Ejecuta `migrate` sobre el esquema `public` tras la inicialización |
| DC-13 `13-router-dinamico-esquemas-fs.md` | Usa `search_path` para cambiar de esquema por request |
| DC-17 `17-diccionario-datos-logico-fs.md` | Define qué tablas van en `public` y cuáles en esquemas de tenant |

---

## 9. Criterios de Aceptación del Diseño

- [ ] El esquema `public` contiene solo las tablas de identidad global (User, Tenant, Membership, Audit).
- [ ] Cada tenant tiene un esquema PostgreSQL propio y aislado.
- [ ] Las extensiones `uuid-ossp` y `pgvector` están activas tras la inicialización.
- [ ] El puerto 5432 no está expuesto al exterior (solo `backnet_fs`).
- [ ] El usuario de Django opera sin privilegios de `SUPERUSER`.
- [ ] Existe un `init-db.sql` documentado y versionado.
