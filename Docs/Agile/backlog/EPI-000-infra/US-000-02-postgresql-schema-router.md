# US-000-02 — PostgreSQL Multi-Tenant + Schema Router

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** US-000-02
**Epic:** [EPI-000 — Core Infra](epic.md)
**Prioridad:** 2
**SP:** 5 | **Sprint:** Sprint-0 | **Estado:** Planned
**Design Anchor:** `Docs/2-Design-Concept/0-Factory-Saas/9-configuracion-postgresql-fs.md`, `13-router-dinamico-esquemas-fs.md`

---

## Historia

**Como** sistema multi-tenant
**Quiero** un router de base de datos que dirija cada tenant a su propio schema PostgreSQL `tenant_{slug}`
**Para** garantizar aislamiento de datos total entre tenants sin múltiples bases de datos

---

## Criterios de Aceptación

- [ ] El schema `public` contiene solo la tabla de tenants y la de auth de Django
- [ ] Cada tenant vive en `tenant_{slug}` con sus propias tablas
- [ ] `python manage.py migrate --schema=demo` crea el schema y tablas correctamente
- [ ] El middleware de resolución de tenant activa el schema correcto por request (header o subdominio)
- [ ] Tests de aislamiento: datos de tenant A no son visibles desde tenant B
- [ ] Sin schema activo, la query eleva `TenantNotFound` controlado

---

## Tasks

- [ ] **TASK-01** (2h) `@backend` — Crear `factory_saas/db_router.py` con clase `TenantSchemaRouter` que implementa `db_for_read`, `db_for_write` leyendo `connection.schema_name` del thread-local
- [ ] **TASK-02** (1h) `@backend` — Crear `factory_saas/middleware/tenant.py`: `TenantMiddleware` que resuelve `tenant_slug` del subdominio/header y activa el schema con `connection.set_schema(slug)`
- [ ] **TASK-03** (2h) `@backend` — Crear `apps/tenants/models.py` con modelo `Tenant(slug, name, is_active)` en schema `public`; agregar migración `0001_initial`
- [ ] **TASK-04** (1h) `@backend` — Crear management command `create_tenant` en `apps/tenants/management/commands/create_tenant.py` que crea schema y corre migraciones
- [ ] **TASK-05** (1h) `@backend` — Crear `tests/test_schema_router.py` con tests: crear 2 tenants, escribir en A, verificar que B no tiene registros
- [ ] **TASK-06** (0.5h) `@backend` — Registrar `TenantMiddleware` en `MIDDLEWARE` de `settings/base.py` y `DATABASE_ROUTERS` con `TenantSchemaRouter`

---

## DoD Checklist

- [ ] `pytest tests/test_schema_router.py` pasa con 0 fallos
- [ ] `create_tenant` command crea schema en postgres verificado con `\dn` en psql
- [ ] PR revisado y aprobado
- [ ] CI pasa
