# EPI-000 — Infraestructura Base: El Suelo Sobre el Que Todo se Construye

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** EPI-000
**Tipo:** Infrastructure Epic — Bloqueante absoluto
**Prioridad:** 0 — BLOQUEANTE de todos los demás Epics
**Sprint objetivo:** Sprint-0
**Total User Stories:** 4
**Total SP estimados:** 13 SP
**Blueprints fuente:**
- `Docs/2-Design-Concept/0-Factory-Saas/6-dockerfile-maestro-fs.md`
- `Docs/2-Design-Concept/0-Factory-Saas/7-docker-compose-specs-fs.md`
- `Docs/2-Design-Concept/0-Factory-Saas/8-entrypoint-specs-fs.md`
- `Docs/2-Design-Concept/0-Factory-Saas/9-configuracion-postgresql-fs.md`
- `Docs/2-Design-Concept/0-Factory-Saas/11-configuracion-redis-celery-fs.md`
- `Docs/2-Design-Concept/0-Factory-Saas/13-router-dinamico-esquemas-fs.md`

---

## § 1 — EL ALMA: Visión y Razón de Existir

### ¿Qué Problema Resuelve?

Sin EPI-000, no hay proyecto. No hay base de datos. No hay forma de que dos desarrolladores trabajen en el mismo entorno con los mismos resultados. No hay forma de garantizar que lo que funciona en el laptop de un desarrollador funcione en producción.

EPI-000 construye el **contrato de entorno**: un conjunto de herramientas portátiles y reproducibles que garantizan que la frase _"en mi máquina funciona"_ jamás sea pronunciada en este proyecto.

### La Promesa

Un desarrollador nuevo clona el repositorio, ejecuta `docker compose up --build`, y en minutos tiene:
- PostgreSQL 16 con aislamiento multi-tenant por schema
- Redis 7.2 como caché y broker de Celery
- Un worker Celery conectado y listo para tareas asíncronas
- Django 5.1 corriendo con hot-reload
- CI verde en cada push a `main`

Sin instalar Python, PostgreSQL, ni Redis manualmente. Sin conflictos de versiones. Sin sorpresas.

### Por Qué Bloquea a Todo lo Demás

Cada Epic posterior necesita:
- Una base de datos donde crear schemas y migraciones → EPI-000 provee PostgreSQL
- Un router de schemas para aislar datos por tenant → EPI-000 provee `TenantSchemaRouter`
- Un runner de tareas asíncronas → EPI-000 provee Celery + Redis
- Un entorno de CI para validar código → EPI-000 provee el pipeline de GitHub Actions

**Regla explícita:** Sprint-1 NO comienza hasta que todos los criterios de Done de EPI-000 estén verificados y el CI esté verde.

---

## § 2 — LA FILOSOFÍA: Principios Fundacionales Aplicados

| Principio | Cómo se aplica en EPI-000 |
|---|---|
| **Reproducibilidad** | `docker compose up` = mismo resultado en cualquier máquina |
| **Aislamiento Total** | `SET search_path TO tenant_{slug}` garantiza que queries de un tenant jamás mezclan con otro |
| **Degradación Graciosa** | `entrypoint.sh` usa `wait-for-db` — no arranca Django hasta que PostgreSQL esté listo |
| **Secretos Seguros** | Todas las credenciales en `.env` (nunca en el código). `.env.dev.example` sin valores reales |
| **CI como Guardián** | Ningún código llega a `main` sin pasar pytest + black + flake8 |

---

## § 3 — LA ARQUITECTURA: Lo Que EPI-000 Crea

### Archivos que existen después de EPI-000

```
factory_saas/
├── settings/
│   ├── base.py           ← DATABASES, CACHES Redis, CELERY config, INSTALLED_APPS
│   ├── dev.py            ← DEBUG=True, ALLOWED_HOSTS=['*']
│   ├── test.py           ← CELERY_TASK_ALWAYS_EAGER=True, DB sqlite para unit tests rápidos
│   └── prod.py           ← SECURE_*, sentry, ALLOWED_HOSTS explícito

apps/
└── core/
    ├── middleware.py     ← TenantMiddleware: host → slug → schema activation
    ├── db_router.py      ← TenantSchemaRouter: SET search_path TO tenant_{slug}, public
    ├── models.py         ← Tenant(id, slug, name, is_active), Membership
    └── tests/
        └── test_schema_router.py  ← test: 2 tenants no comparten datos

Dockerfile.dev            ← Python 3.12, poetry install, non-root user
docker-compose.dev.yml    ← services: db(postgres:16), redis(redis:7.2), web, worker
entrypoint.sh             ← wait-for-db → migrate → exec "$@"
.env.dev.example          ← DATABASE_URL, REDIS_URL, SECRET_KEY (sin valores reales)
.github/
└── workflows/
    └── ci.yml            ← pytest + black --check + flake8 en cada push/PR

pyproject.toml            ← [tool.pytest] testpaths, [tool.black] line-length=88
pytest.ini                ← DJANGO_SETTINGS_MODULE=factory_saas.settings.test
tests/
└── test_smoke.py         ← django.test.utils.setup_test_environment() + ping DB
```

### Arquitectura de la Base de Datos Multi-Tenant

```
PostgreSQL 16
├── schema: public
│   ├── core_tenant           ← (id, slug, name, is_active, created_at)
│   ├── core_membership       ← (user_id, tenant_id, role, joined_at)
│   └── auth_user             ← usuarios globales (Django auth)
├── schema: tenant_acme       ← creado por: python manage.py create_tenant --slug=acme
│   └── [tablas de negocio de acme]
└── schema: tenant_demo       ← creado por: python manage.py create_tenant --slug=demo
    └── [tablas de negocio de demo]
```

### Flujo de Request Multi-Tenant

```
Request HTTP
  → Nginx (en prod) / Django dev server
  → TenantMiddleware
      - extrae slug del Host header: "acme.factory.com" → "acme"
      - busca en Redis cache (TTL 5min): "tenant:slug:acme"
      - si no: SELECT core_tenant WHERE slug='acme'
      - si no existe: raise Http404 / return 404 {"error": "tenant_not_found"}
      - request.tenant = Tenant(slug='acme', ...)
  → TenantSchemaRouter
      - cursor.execute("SET search_path TO tenant_acme, public")
  → View / Service
      - queries del ORM apuntan automáticamente al schema del tenant
      - CERO filtros manuales por tenant en código de negocio
```

### Celery + Redis Baseline

```python
# factory_saas/celery.py
app = Celery('factory_saas')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# settings/base.py
CELERY_BROKER_URL = env('REDIS_URL', default='redis://redis:6379/0')
CELERY_RESULT_BACKEND = env('REDIS_URL', default='redis://redis:6379/0')
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

# settings/test.py
CELERY_TASK_ALWAYS_EAGER = True   # tasks síncronas en tests
CELERY_TASK_EAGER_PROPAGATES = True
```

---

## § 4 — EL ÁRBOL: User Stories de Cimientos a Acabados

| US ID | Historia | SP | Sprint | Archivo |
|---|---|---|---|---|
| US-000-01 | Docker dev environment reproducible | 3 | Sprint-0 | [US-000-01](US-000-01-docker-dev-environment.md) |
| US-000-02 | PostgreSQL multi-tenant + schema router | 5 | Sprint-0 | [US-000-02](US-000-02-postgresql-schema-router.md) |
| US-000-03 | CI pipeline (pytest + linting) | 3 | Sprint-0 | [US-000-03](US-000-03-ci-pipeline.md) |
| US-000-04 | Redis + Celery worker baseline | 2 | Sprint-0 | [US-000-04](US-000-04-redis-celery-baseline.md) |

### Dependencias dentro del Epic

```
US-000-01 (Docker) ──→ US-000-02 (PostgreSQL)
                   ──→ US-000-04 (Redis + Celery)
US-000-02 + US-000-04 ──→ US-000-03 (CI: requiere ambos para pytest completo)
```

---

## § 5 — BLUEPRINTS DE REFERENCIA

| ID | Documento | Qué gobierna |
|---|---|---|
| DC-6 | `6-dockerfile-maestro-fs.md` | Dockerfile multi-stage, usuario no-root |
| DC-7 | `7-docker-compose-specs-fs.md` | Servicios, volúmenes, health checks |
| DC-8 | `8-entrypoint-specs-fs.md` | wait-for-db, orden de arranque |
| DC-9 | `9-configuracion-postgresql-fs.md` | Schemas, roles DB, conexión desde Django |
| DC-11 | `11-configuracion-redis-celery-fs.md` | Broker, result backend, serialización |
| DC-13 | `13-router-dinamico-esquemas-fs.md` | TenantMiddleware completo + TenantSchemaRouter |
| DC-12 | `12-patron-service-layer-fs.md` | Estructura de carpetas de cada app |

---

## § 6 — DEFINITION OF DONE

EPI-000 está Done cuando:

- [ ] `docker compose up --build` en máquina limpia: 0 errores en menos de 5 minutos
- [ ] `http://localhost:8000` responde con la página de Django (o 404 de tenant para prueba)
- [ ] `docker exec web python manage.py create_tenant --slug=demo --name=Demo` crea schema `tenant_demo` en PostgreSQL
- [ ] `docker exec web pytest apps/core/tests/test_schema_router.py` pasa: 2 tenants no comparten datos
- [ ] Request a host sin tenant registrado → respuesta 404 con body `{"error": "tenant_not_found"}`
- [ ] Request a host de tenant válido → schema activado (verificable en log de DB: `SET search_path TO tenant_demo, public`)
- [ ] `docker exec worker celery -A factory_saas inspect ping` responde `pong`
- [ ] CI verde en GitHub Actions: pytest + black + flake8 en rama `main`
- [ ] `.env.dev.example` en el repo. `.env.dev` en `.gitignore`
- [ ] `product-backlog.md` actualizado: US-000-01..04 en estado `Done`
