# US-CORE-03 — Jerarquía Base de Excepciones de Dominio

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-17

**ID:** US-CORE-03
**Epic:** [EPI-CORE — Factory SaaS](EPI-CORE-factory-saas.md)
**Prioridad:** 3
**SP:** 1 | **Sprint:** Sprint-0 | **Estado:** Planned
**Design Anchor:** `Docs/2-Design-Concept/0-Factory-Saas/12-patron-service-layer-fs.md`

---

## Historia

**Como** equipo que implementará múltiples apps
**Quiero** una jerarquía base de excepciones en `apps/core/exceptions.py`
**Para** que todos los services hablen el mismo lenguaje de error y no retornen `None` como señal de fallo

---

## Criterios de Aceptación

- [ ] Existe `FactoryBaseException` como raíz del dominio
- [ ] Existen al menos `ServiceError`, `NotFoundError` y `TenantNotFoundError`
- [ ] La jerarquía es consistente con la regla descrita en EPI-CORE
- [ ] Los nombres son reutilizables por cualquier app hija

---

## Tasks

- [ ] **TASK-01** (0.5h) `@backend` — Crear `apps/core/exceptions.py` con jerarquía base
- [ ] **TASK-02** (0.25h) `@backend` — Alinear nombres con la guía de services y errores de DC-12-FS
- [ ] **TASK-03** (0.25h) `@docs` — Dejar trazabilidad en backlog y sprint backlog

---

## DoD Checklist

- [ ] La jerarquía es importable desde otras apps
- [ ] No hay duplicidad conceptual con futuras excepciones de app
- [ ] PR revisado y aprobado
