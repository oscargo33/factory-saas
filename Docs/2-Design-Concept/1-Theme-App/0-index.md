# Índice de Diseño App 1 — Theme

**Versión del documento:** 1.0
**Última actualización:** 2026-03-16

**Estado documental:** Inicio de diseño individual

**ID:** TH-0-INDEX
**Ubicación:** `./Docs/2-Design-Concept/1-Theme-App/0-index.md`
**Anchor Docs:** `Docs/1-Core_Concept/1-theme-app-cc.md`, `Docs/1-Core_Concept/0-factory_saas-cc.md`
**Dependencia Global:** `Docs/2-Design-Concept/0-Factory-Saas/*`

---

## Objetivo

Este paquete define el diseño funcional de la App Theme como base visual e i18n del ecosistema. Debe respetar la política de independencia entre apps y proporcionar contratos estables para consumo transversal.

Alcance obligatorio del paquete:
- Controlar el look and feel de todas las apps (2-9) y del Product Core integrado.
- Proveer componentes y tokens visuales basados en Tailwind CSS + Django Cotton.
- Proveer engine de traducción por base de datos usando capacidades nativas de traducción de Django y fallback a LibreTranslate.
- Exigir fallback visual y de i18n en cada app consumidora cuando Theme no esté instalado o no esté saludable.

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
| 6 | `6-matriz-trazabilidad-theme-th.md` | TH-6-TRA | Trazabilidad Core -> Design -> Evidencia |
| 7 | `7-nfr-seguridad-operacion-theme-th.md` | TH-7-NFR | Requerimientos no funcionales, seguridad y operación |
| 8 | `8-plan-validacion-diseno-theme-th.md` | TH-8-VAL | Plan de validación del diseño y evidencia de cierre |
| 9 | `9-product-visible-admin-th.md` | TH-9-PV | Producto visible + CRUD admin por modelo |
| 10 | `10-roles-permisos-capas-th.md` | TH-10-RBAC | Roles, permisos y capas de interfaz |

---

## Reglas de alineación obligatoria

- No importar modelos de otras apps.
- Exponer integración inter-app solo por contratos públicos de selector/service.
- Tener fallback neutral para consumidores cuando Theme no esté instalado.
- Mantener compatibilidad con el diseño global DC-12, DC-14 y DC-16.

Patron de paquete completo obligatorio por app:
- Modelo de datos.
- Service/Selector/Contratos.
- Endpoints/Middleware/UI segun corresponda.
- Matriz de trazabilidad.
- NFR + seguridad + operación.
- Plan de validación del diseño.

---

## Estado de Fase 1 por App

**App 1 Theme:** 🔄 En diseño

Cierre de esta app requiere checklist TH-1 en estado completo.
