# US-CORE-04 — TenantMiddleware y TenantSchemaRouter

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-17

**ID:** US-CORE-04
**Epic:** [EPI-CORE — Factory SaaS](EPI-CORE-factory-saas.md)
**Prioridad:** 4
**SP:** 3 | **Sprint:** Sprint-0 | **Estado:** Planned
**Design Anchor:** `Docs/2-Design-Concept/0-Factory-Saas/13-router-dinamico-esquemas-fs.md`, `Docs/2-Design-Concept/0-Factory-Saas/9-configuracion-postgresql-fs.md`

---

## Historia

**Como** runtime multi-tenant
**Quiero** middleware de resolución de tenant y router de schema
**Para** activar el `search_path` correcto por request y garantizar aislamiento por construcción

---

## Criterios de Aceptación

- [ ] Existe `TenantMiddleware` que resuelve slug desde host o contexto configurado
- [ ] Existe `TenantSchemaRouter` que activa `tenant_{slug}, public`
- [ ] Si el tenant no existe, el flujo responde con error controlado
- [ ] La lógica se alinea con DC-13-FS y EPI-CORE
- [ ] Queda claro el contrato entre middleware, selector de tenant y DB router

---

## Tasks

- [ ] **TASK-01** (1h) `@backend` — Crear `apps/core/middleware.py` con `TenantMiddleware`
- [ ] **TASK-02** (1h) `@backend` — Crear `apps/core/db_router.py` con `TenantSchemaRouter`
- [ ] **TASK-03** (0.5h) `@backend` — Definir manejo de `TenantNotFoundError` controlado
- [ ] **TASK-04** (0.5h) `@backend` — Registrar integración prevista en settings base

---

## DoD Checklist

- [ ] La resolución de tenant y el router quedan especificados e implementables
- [ ] El flujo de error está controlado
- [ ] PR revisado y aprobado
