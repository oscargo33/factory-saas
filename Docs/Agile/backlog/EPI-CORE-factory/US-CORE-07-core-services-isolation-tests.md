# US-CORE-07 — Services Core y Tests de Aislamiento

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-17

**ID:** US-CORE-07
**Epic:** [EPI-CORE — Factory SaaS](EPI-CORE-factory-saas.md)
**Prioridad:** 7
**SP:** 3 | **Sprint:** Sprint-0 | **Estado:** Planned
**Design Anchor:** `Docs/2-Design-Concept/0-Factory-Saas/12-patron-service-layer-fs.md`, `Docs/2-Design-Concept/0-Factory-Saas/13-router-dinamico-esquemas-fs.md`, `Docs/2-Design-Concept/0-Factory-Saas/26-estrategia-testing-fs.md`

---

## Historia

**Como** núcleo operativo de la Factory
**Quiero** services básicos de tenant y tests de aislamiento
**Para** materializar las reglas del core y demostrar desde Sprint-0 que la separación entre tenants no depende de convenciones manuales

---

## Criterios de Aceptación

- [ ] Existe `create_tenant(name, slug, owner_id)`
- [ ] Existe `deactivate_tenant(tenant_id)` o equivalente de suspensión controlada
- [ ] Los services siguen el patrón de DC-12-FS y elevan excepciones de dominio
- [ ] Existen tests base de aislamiento multi-tenant
- [ ] La evidencia de aislamiento queda trazada en Sprint-0

---

## Tasks

- [ ] **TASK-01** (1h) `@backend` — Crear `apps/core/services.py` con `create_tenant`
- [ ] **TASK-02** (0.5h) `@backend` — Crear `deactivate_tenant` o suspensión equivalente
- [ ] **TASK-03** (1h) `@backend` — Crear tests base de aislamiento de tenants en `apps/core/tests/`
- [ ] **TASK-04** (0.5h) `@docs` — Referenciar la evidencia en backlog y sprint backlog

---

## DoD Checklist

- [ ] Los services no retornan `None` para errores de dominio
- [ ] Hay evidencia verificable de aislamiento multi-tenant
- [ ] PR revisado y aprobado
