# Indice de Diseno App 3 - Profile

**ID:** PR-0-INDEX
**Ubicacion:** `./Docs/2-Design-Concept/3-Profile-App/0-index.md`
**Anchor Docs:** `Docs/1-Core_Concept/3-profile-app-cc.md`, `Docs/1-Core_Concept/0-factory_saas-cc.md`
**Dependencia Global:** `Docs/2-Design-Concept/0-Factory-Saas/*`
**Estado:** v1.0 - Inicio de diseno individual

---

## Objetivo

Este paquete define el diseno funcional de App Profile como capa de identidad y tenancy del ecosistema, incluyendo RBAC y composicion de dashboard con dependencias suaves.

Alcance obligatorio del paquete:
- Gestionar identidad global (`User`) y contexto de organizacion (`Tenant`, `Membership`).
- Gestionar preferencias por tenant (`Profile`) en esquema tenant.
- Exponer contratos de contexto para apps consumidoras y Product Core.
- Mantener fallback UI cuando Theme no este instalado/no saludable.

---

## Documentos del paquete Profile

| # | Documento | ID | Rol |
|---|---|---|---|
| 0 | `0-index.md` | PR-0-INDEX | Indice y trazabilidad |
| 1 | `1-checklist-profile-app.md` | PR-1-CK | Control de avance del diseno |
| 2 | `2-modelos-profile-pr.md` | PR-2-MDL | Modelo de datos (User, Tenant, Membership, Profile) |
| 3 | `3-service-selector-contratos-profile-pr.md` | PR-3-SVC | Service/Selector y contratos inter-app |
| 4 | `4-views-endpoints-middleware-profile-pr.md` | PR-4-API | Endpoints, middleware y router de esquema |
| 5 | `5-dashboard-fallback-composition-profile-pr.md` | PR-5-UI | Dashboard agregador y fallback visual |
| 6 | `6-matriz-trazabilidad-profile-pr.md` | PR-6-TRA | Trazabilidad Core -> Design -> Evidencia |
| 7 | `7-nfr-seguridad-operacion-profile-pr.md` | PR-7-NFR | NFR, seguridad y operacion |
| 8 | `8-plan-validacion-diseno-profile-pr.md` | PR-8-VAL | Plan de validacion del diseno |

---

## Reglas de alineacion obligatoria

- No importar modelos de otras apps.
- Toda lectura/escritura inter-app pasa por contratos de service/selector.
- Tenancy: schema-per-tenant y `search_path` obligatorio.
- Perfil y dashboard deben sobrevivir sin Theme y sin Telemetry.

Patron de paquete completo obligatorio por app:
- Modelo de datos.
- Service/Selector/Contratos.
- Endpoints/Middleware/UI segun corresponda.
- Matriz de trazabilidad.
- NFR + seguridad + operacion.
- Plan de validacion del diseno.

---

## Estado de Fase 1 por App

**App 3 Profile:** en diseno

Cierre de esta app requiere checklist PR-1 en estado completo.
