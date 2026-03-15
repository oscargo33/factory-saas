# Product Backlog - Factory-SaaS

## Reglas
- Unico backlog ordenado por valor/riesgo/dependencias.
- Cada item referencia Anchor Doc.
- Cada item declara Scope y Non-scope por app.

## Items (Inicial)
| ID | Title | Type | Anchor Doc(s) | Scope / Non-scope | Acceptance Criteria | Risks / Dependencies | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| PB-001 | Cerrar Fase 0 de concepcion | Documentation | `Docs/1-Core_Concept/*` | Scope: politicas, glosario, riesgos, aprobaciones. Non-scope: implementacion tecnica. | Gate de Fase 0 completo y aprobado. | Requiere validacion de arquitectura/negocio. | TBD | In Progress |
| PB-002 | Completar diseno transversal 0-Factory-SaaS (capas 2-7) | Documentation | `Docs/2-Design-Concept/0-Factory-Saas/*` | Scope: especificaciones `-fs`. Non-scope: codigo ejecutable. | Documentos 8-13 creados y revisados. | Dependencia de cierre Fase 0. | TBD | Todo |
| PB-003 | Matriz contratos inter-app | Documentation | `Docs/2-Design-Concept/0-Factory-Saas/` | Scope: contratos y fallback. Non-scope: payload runtime definitivo. | Matriz aprobada por arquitectura. | Alineacion con independencia de apps. | TBD | Todo |
| PB-004 | Diccionario de datos logico de diseno | Documentation | `Docs/2-Design-Concept/0-Factory-Saas/` | Scope: entidades/ownership/relaciones. Non-scope: migraciones. | Diccionario aprobado y trazable a Core Concept. | Requiere glosario fase 0. | TBD | Todo |
