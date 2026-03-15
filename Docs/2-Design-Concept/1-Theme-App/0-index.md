# Índice de Diseño App 1 — Theme

**ID:** TH-0-INDEX
**Ubicación:** `./Docs/2-Design-Concept/1-Theme-App/0-index.md`
**Anchor Docs:** `Docs/1-Core_Concept/1-theme-app-cc.md`, `Docs/1-Core_Concept/0-factory_saas-cc.md`
**Dependencia Global:** `Docs/2-Design-Concept/0-Factory-Saas/*`
**Estado:** v1.0 — Inicio de diseño individual

---

## Objetivo

Este paquete define el diseño funcional de la App Theme como base visual e i18n del ecosistema. Debe respetar la política de independencia entre apps y proporcionar contratos estables para consumo transversal.

---

## Documentos del paquete Theme

| # | Documento | ID | Rol |
|---|---|---|---|
| 0 | `0-index.md` | TH-0-INDEX | Índice y trazabilidad |
| 1 | `1-checklist-theme-app.md` | TH-1-CK | Control de avance del diseño |
| 2 | `2-modelos-theme-th.md` | TH-2-MDL | Diseño de entidades (Glossary, ThemeConfig) |
| 3 | `3-service-selector-contratos-theme-th.md` | TH-3-SVC | Service/Selector y contratos inter-app |
| 4 | `4-views-endpoints-middleware-theme-th.md` | TH-4-API | Middleware, context processor y endpoints internos |
| 5 | `5-componentes-cotton-pipeline-theme-th.md` | TH-5-UI | Sistema visual: Cotton, Tailwind y Alpine |

---

## Reglas de alineación obligatoria

- No importar modelos de otras apps.
- Exponer integración inter-app solo por contratos públicos de selector/service.
- Tener fallback neutral para consumidores cuando Theme no esté instalado.
- Mantener compatibilidad con el diseño global DC-12, DC-14 y DC-16.

---

## Estado de Fase 1 por App

**App 1 Theme:** 🔄 En diseño

Cierre de esta app requiere checklist TH-1 en estado completo.
