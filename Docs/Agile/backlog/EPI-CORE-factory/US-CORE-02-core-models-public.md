# US-CORE-02 — Modelos Core en Schema Public

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-17

**ID:** US-CORE-02
**Epic:** [EPI-CORE — Factory SaaS](EPI-CORE-factory-saas.md)
**Prioridad:** 2
**SP:** 3 | **Sprint:** Sprint-0 | **Estado:** Planned
**Design Anchor:** `Docs/2-Design-Concept/0-Factory-Saas/9-configuracion-postgresql-fs.md`, `Docs/2-Design-Concept/0-Factory-Saas/17-diccionario-datos-logico-fs.md`

---

## Historia

**Como** plataforma multi-tenant
**Quiero** modelos base `Tenant` y `Membership` en `public`
**Para** resolver identidad de tenant y membresía sin mezclar datos de negocio por schema

---

## Criterios de Aceptación

- [ ] Existe `apps/core/models.py` con `Tenant` y `Membership`
- [ ] La migración inicial crea estas tablas en el schema `public`
- [ ] `Tenant` modela al menos `slug`, `name` e `is_active`
- [ ] `Membership` representa relación usuario-tenant con `role`
- [ ] El diseño respeta ownership definido en DC-17-FS

---

## Tasks

- [ ] **TASK-01** (1h) `@backend` — Crear `apps/core/models.py` con `Tenant` y `Membership`
- [ ] **TASK-02** (0.5h) `@backend` — Definir constraints mínimas para `slug` y relación tenant-usuario-rol
- [ ] **TASK-03** (0.5h) `@backend` — Generar migración inicial del app core
- [ ] **TASK-04** (0.5h) `@backend` — Verificar que la migración corre sobre `public`
- [ ] **TASK-05** (0.5h) `@docs` — Reflejar evidencia en sprint backlog y checklist de cierre

---

## DoD Checklist

- [ ] `Tenant` y `Membership` existen con campos mínimos acordados
- [ ] La migración inicial es reproducible
- [ ] PR revisado y aprobado
