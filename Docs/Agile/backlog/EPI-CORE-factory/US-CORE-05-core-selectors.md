# US-CORE-05 — Selectors Base de Tenant y Membresías

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-17

**ID:** US-CORE-05
**Epic:** [EPI-CORE — Factory SaaS](EPI-CORE-factory-saas.md)
**Prioridad:** 5
**SP:** 2 | **Sprint:** Sprint-0 | **Estado:** Planned
**Design Anchor:** `Docs/2-Design-Concept/0-Factory-Saas/12-patron-service-layer-fs.md`, `Docs/2-Design-Concept/0-Factory-Saas/16-contratos-inter-app-fs.md`

---

## Historia

**Como** apps consumidoras de contexto core
**Quiero** selectors públicos para tenants y memberships
**Para** consultar información base sin importar modelos entre apps ni romper el patrón service/selector

---

## Criterios de Aceptación

- [ ] Existe `get_tenant_by_slug(slug)`
- [ ] Existe `get_active_memberships(tenant_id)`
- [ ] Los selectors son de solo lectura y sin side effects
- [ ] Las firmas coinciden con los contratos definidos en DC-16-FS y EPI-CORE

---

## Tasks

- [ ] **TASK-01** (0.75h) `@backend` — Crear `apps/core/selectors.py` con `get_tenant_by_slug`
- [ ] **TASK-02** (0.5h) `@backend` — Crear `get_active_memberships`
- [ ] **TASK-03** (0.25h) `@backend` — Asegurar nombres y retornos coherentes con contratos públicos
- [ ] **TASK-04** (0.5h) `@docs` — Conectar estas firmas en backlog y documentación de epic

---

## DoD Checklist

- [ ] Los selectors son reutilizables por apps hijas
- [ ] No contienen escritura ni lógica transaccional
- [ ] PR revisado y aprobado
