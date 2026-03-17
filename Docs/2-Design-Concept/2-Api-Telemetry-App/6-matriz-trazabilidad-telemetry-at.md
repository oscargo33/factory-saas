# Documento: Matriz de Trazabilidad - App Api Telemetry

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** AT-6-TRA
**Ubicación:** `./Docs/2-Design-Concept/2-Api-Telemetry-App/6-matriz-trazabilidad-telemetry-at.md`
**Anchor Docs:** `Docs/1-Core_Concept/2-api-app-cc.md`, `Docs/2-Design-Concept/0-Factory-Saas/15-protocolo-comunicacion-central-fs.md`

---

## 1. Propósito

Asegurar trazabilidad entre requerimientos del sensor Api/Telemetry, decisiones de diseño y criterios de validación.

---

## 2. Matriz Requerimiento -> Diseño -> Evidencia

| Req ID | Requerimiento | Documento de Diseño | Criterio de Evidencia |
|---|---|---|---|
| AT-R01 | Push a La Central cada 5 min | `5-push-pull-resiliencia-telemetry-at.md` | Task Celery y scheduler definidos |
| AT-R02 | Pull de inspección bajo token | `4-endpoints-middleware-telemetry-at.md` | Endpoint `/inspect/` con auth |
| AT-R03 | Trazabilidad con `X-Trace-ID` | `4-endpoints-middleware-telemetry-at.md` | Middleware inyecta trace en request/response |
| AT-R04 | Fail-soft sin bloquear SaaS | `5-push-pull-resiliencia-telemetry-at.md` | Buffer `PendingMetrics` y retry |
| AT-R05 | Payload sin PII | `2-modelos-telemetry-at.md` | Validación de schema por `event_type` |
| AT-R06 | Contratos inter-app versionados | `3-service-selector-contratos-telemetry-at.md` | `telemetry.contract.v1` publicado |
| AT-R07 | Feature-flag de apagado seguro | `5-push-pull-resiliencia-telemetry-at.md` | `TELEMETRY_ENABLED` documentado |

---

## 3. Cobertura por Capa

| Capa | Cobertura Telemetry |
|---|---|
| Capa 3 | Redis/Celery para colas y buffering |
| Capa 4 | Service/Selector y contratos inter-app |
| Capa 7 | Protocolo Push/Pull con La Central |
| Capa Transversal | Seguridad de payload y auditoría inmutable |

---

## 4. Criterios de aceptación

- [ ] Todos los requerimientos AT-R01..AT-R07 trazados a artefactos de diseño.
- [ ] Cada requerimiento tiene evidencia verificable para Sprint Review.
- [ ] No quedan huecos de trazabilidad entre Core y Design.

## 5. Cobertura obligatoria DC-12/DC-13/DC-16/DC-17

- DC-12 (patron service layer): cubierto en `3-service-selector-contratos-telemetry-at.md`.
- DC-13 (router dinamico y contexto tenant): cubierto por middleware y aislamiento de eventos por tenant.
- DC-16 (contratos inter-app): cubierto por contratos `telemetry.contract.v1` y endpoints de inspeccion/push.
- DC-17 (diccionario de datos logico): cubierto por modelo de eventos, campos de correlacion y restricciones de payload sin PII.
