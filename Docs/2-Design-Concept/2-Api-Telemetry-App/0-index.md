# Indice de Diseno App 2 - Api Telemetry

**Versión del documento:** 1.0
**Última actualización:** 2026-03-16

**Estado documental:** Inicio de diseno individual

**ID:** AT-0-INDEX
**Ubicacion:** `./Docs/2-Design-Concept/2-Api-Telemetry-App/0-index.md`
**Anchor Docs:** `Docs/1-Core_Concept/2-api-app-cc.md`, `Docs/1-Core_Concept/0-factory_saas-cc.md`
**Dependencia Global:** `Docs/2-Design-Concept/0-Factory-Saas/*`

---

## Objetivo

Este paquete define el diseno funcional de la App Api/Telemetry como sensor del ecosistema y enlace resiliente con La Central.

Alcance obligatorio del paquete:
- Emitir telemetria de negocio y tecnica desde todas las apps consumidoras.
- Soportar modelo Push/Pull con autenticacion segura y trazabilidad por `X-Trace-ID`.
- Mantener fail-soft: si La Central no responde, la operacion del SaaS no se bloquea.

---

## Documentos del paquete Api Telemetry

| # | Documento | ID | Rol |
|---|---|---|---|
| 0 | `0-index.md` | AT-0-INDEX | Indice y trazabilidad |
| 1 | `1-checklist-api-telemetry-app.md` | AT-1-CK | Control de avance del diseno |
| 2 | `2-modelos-telemetry-at.md` | AT-2-MDL | Modelo de datos (TelemetryEvent, PendingMetrics, AuditLog) |
| 3 | `3-service-selector-contratos-telemetry-at.md` | AT-3-SVC | Service/Selector y contratos inter-app |
| 4 | `4-endpoints-middleware-telemetry-at.md` | AT-4-API | Endpoints DRF, middleware de trazabilidad y seguridad |
| 5 | `5-push-pull-resiliencia-telemetry-at.md` | AT-5-OPS | Flujos Push/Pull, retries, buffering y observabilidad |
| 6 | `6-matriz-trazabilidad-telemetry-at.md` | AT-6-TRA | Trazabilidad Core -> Design -> Evidencia |
| 7 | `7-nfr-seguridad-operacion-telemetry-at.md` | AT-7-NFR | NFR, seguridad y operación de telemetría |
| 8 | `8-plan-validacion-diseno-telemetry-at.md` | AT-8-VAL | Plan de validación de diseño y evidencia |
| 10 | `10-product-visible-admin-at.md` | AT-10-PV | Producto visible operador + CRUD admin |
| 11 | `11-roles-permisos-capas-at.md` | AT-11-RBAC | Roles, permisos y capas de interfaz |

---

## Reglas de alineacion obligatoria

- No importar modelos de otras apps.
- Exponer integracion inter-app solo por contratos publicos de selector/service.
- Mantener `TELEMETRY_ENABLED` como feature-flag transversal de desactivacion segura.
- Alinear seguridad y compliance con DC-15 y DC-18.

Patron de paquete completo obligatorio por app:
- Modelo de datos.
- Service/Selector/Contratos.
- Endpoints/Middleware/UI segun corresponda.
- Matriz de trazabilidad.
- NFR + seguridad + operación.
- Plan de validación del diseño.

---

## Estado de Fase 1 por App

**App 2 Api/Telemetry:** en diseno

Cierre de esta app requiere checklist AT-1 en estado completo.
