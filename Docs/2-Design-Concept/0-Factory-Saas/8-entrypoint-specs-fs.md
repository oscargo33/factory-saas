# Documento: 8-entrypoint-specs-fs.md

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** DC-8-FS
**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/8-entrypoint-specs-fs.md`
**Referencia Core:** `0-factory_saas-cc.md`
**Capa:** 1 — Entorno de Ejecución (Cierre de Capa 1)
**Apellido:** **-fs**

---

## 1. Propósito del Entrypoint

El `entrypoint.sh` es el **director de orquesta del arranque**. Es el único punto donde se garantiza que el sistema está en un estado consistente antes de aceptar tráfico. Su secuencia resuelve el problema del orden de dependencias entre servicios y la necesidad de preparar los esquemas de base de datos antes de ejecutar la aplicación.

**Responsabilidades únicas de este script:**
- Esperar que PostgreSQL esté listo (`pg_isready`) antes de continuar.
- Ejecutar migraciones sobre el esquema `public` (identidad global).
- Ejecutar `collectstatic` para publicar archivos estáticos compilados.
- Levantar Gunicorn como proceso principal del contenedor.

**Lo que este script NO hace:**
- No crea esquemas de tenant (eso lo hace el comando de management `bootstrap_tenant`).
- No ejecuta seeds de datos (eso se hace via fixtures en CI).
- No gestiona secretos (eso es responsabilidad de Docker Secrets / `.env`).

---

## 2. Secuencia de Arranque (Estado de Máquina)

```
[INICIO]
    │
    ▼
[GATE 1] db-ready?
    │  ─── esperar hasta 60 intentos (30s total) ───►  [ERROR FATAL: DB no disponible]
    │ OK
    ▼
[GATE 2] migrate --database=public
    │  ─── aplica migraciones de User, Tenant, Membership ───►  [ERROR FATAL si falla]
    │ OK
    ▼
[GATE 3] collectstatic --noinput
    │  ─── solo en entorno != development ───►  [WARN: no bloquea el arranque]
    │ OK / SKIP
    ▼
[INICIO APP] exec gunicorn config.wsgi:application
    │  ─── con configuración de workers y timeouts según ENV ───►  [SIRVIENDO]
```

---

## 3. Diseño del Script `entrypoint.sh`

### 3.1. Variables de Entorno Requeridas

| Variable | Descripción | Ejemplo |
|---|---|---|
| `DB_HOST` | Host del servicio PostgreSQL | `db` |
| `DB_PORT` | Puerto de PostgreSQL | `5432` |
| `DJANGO_SETTINGS_MODULE` | Módulo de configuración | `config.settings.production` |
| `APP_ENV` | Entorno de ejecución | `production` / `development` |
| `GUNICORN_WORKERS` | Número de workers concurrentes | `4` |
| `GUNICORN_TIMEOUT` | Timeout por request (segundos) | `120` |

### 3.2. Lógica del Gate 1: Esperar PostgreSQL

El script implementa un **bucle de polling** con back-off exponencial simplificado:
- Intentos máximos: 30
- Intervalo entre intentos: 2 segundos
- Total máximo de espera: 60 segundos
- Comando de verificación: `pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER`
- Si se agotan los intentos: exit con código 1 (Docker reiniciará el contenedor según `restart: unless-stopped`)

### 3.3. Lógica del Gate 2: Migraciones de Esquema Público

Las migraciones se ejecutan **exclusivamente sobre el esquema `public`** en el primer arranque:

```
manage.py migrate --database=default
```

El router de Django (ver Documento 13) debe estar configurado para que el comando `migrate` sin `--database` apunte al esquema `public` por defecto. Las migraciones de esquemas de tenant se ejecutan mediante el management command `migrate_schemas` (de `django-tenants`) solo cuando se provisiona un nuevo tenant.

**Orden esperado de migraciones en `public`:**
1. `django.contrib.contenttypes`
2. `django.contrib.auth`
3. `profiles.User`, `profiles.Tenant`, `profiles.Membership`
4. `telemetry.AuditLog`, `telemetry.PendingMetrics`

### 3.4. Lógica del Gate 3: Archivos Estáticos

Solo se ejecuta si `APP_ENV != development`:
```
manage.py collectstatic --noinput --clear
```

En desarrollo, los archivos estáticos son servidos directamente por Django (`DEBUG=True`), por lo que este paso es innecesario y podría sobreescribir el output de Tailwind en watch mode.

### 3.5. Comando Final: Gunicorn

El proceso principal del contenedor se levanta con `exec` (no `&`) para que Gunicorn sea el proceso PID 1 del contenedor y reciba correctamente las señales `SIGTERM`/`SIGINT` de Docker:

```
exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers $GUNICORN_WORKERS \
  --worker-class sync \
  --timeout $GUNICORN_TIMEOUT \
  --access-logfile - \
  --error-logfile - \
  --log-level info
```

---

## 4. Variante de Desarrollo

En `APP_ENV=development` el entrypoint levanta el servidor de desarrollo de Django en lugar de Gunicorn:

```
exec python manage.py runserver 0.0.0.0:8000
```

Esto permite el hot-reload del código sin necesidad de reconstruir la imagen.

---

## 5. Gestión de Errores del Entrypoint

| Escenario | Comportamiento | Recuperación |
|---|---|---|
| DB no disponible en 60s | `exit 1` | Docker reinicia el contenedor (política `restart: unless-stopped`) |
| Migración falla | `exit 1` con mensaje de error en stderr | Requiere intervención manual; revisar logs con `docker logs app` |
| `collectstatic` falla | Warning en stderr, **continúa** el arranque | Los estáticos quedan en estado anterior |
| Gunicorn falla post-arranque | El contenedor muere y Docker lo reinicia | Revisar logs de aplicación |

---

## 6. Relación con Otros Documentos

| Documento | Relación |
|---|---|
| DC-6 `6-dockerfile-maestro-fs.md` | Define que `entrypoint.sh` se copia al contenedor con permisos de ejecución |
| DC-7 `7-docker-compose-specs-fs.md` | Define la condición `service_healthy` del servicio `db` que protege el Gate 1 |
| DC-9 `9-configuracion-postgresql-fs.md` | Define los esquemas y extensiones que deben existir antes de las migraciones |
| DC-13 `13-router-dinamico-esquemas-fs.md` | Define el router que garantiza que `migrate` apunta al esquema correcto |

---

## 7. Criterios de Aceptación del Diseño

- [ ] El script valida la disponibilidad de DB antes de cualquier operación Django.
- [ ] Las migraciones del esquema `public` se ejecutan idempotentemente (sin error si ya están aplicadas).
- [ ] `collectstatic` no bloquea el arranque en caso de fallo.
- [ ] Gunicorn es el proceso PID 1 del contenedor (usando `exec`).
- [ ] El script es compatible con el entorno `development` sin modificaciones.
- [ ] Todos los errores críticos salen con código de salida != 0.
