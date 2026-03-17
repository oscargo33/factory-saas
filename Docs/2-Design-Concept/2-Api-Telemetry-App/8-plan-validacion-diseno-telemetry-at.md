# Documento: Plan de Validacion de Diseno - App Api Telemetry

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** AT-8-VAL
**Ubicación:** `./Docs/2-Design-Concept/2-Api-Telemetry-App/8-plan-validacion-diseno-telemetry-at.md`
**Anchor Docs:** `Docs/2-Design-Concept/2-Api-Telemetry-App/1-checklist-api-telemetry-app.md`, `Docs/2-Design-Concept/2-Api-Telemetry-App/6-matriz-trazabilidad-telemetry-at.md`

---

## 1. Proposito

Definir validacion del diseno Api/Telemetry para garantizar trazabilidad, resiliencia y seguridad antes de implementacion.

---

## 2. Escenarios de validacion (diseno)

| Caso | Objetivo | Evidencia esperada |
|---|---|---|
| AT-VAL-01 | Push exitoso | Lote marcado enviado, buffer reducido |
| AT-VAL-02 | Falla de La Central | Evento en `PendingMetrics` + retry programado |
| AT-VAL-03 | Pull autenticado | `/inspect/` responde 200 con token valido |
| AT-VAL-04 | Pull sin token | `/inspect/` responde 401/403 |
| AT-VAL-05 | Trace distribuido | `X-Trace-ID` presente en request/response/evento |
| AT-VAL-06 | Payload con PII bloqueado | Validacion rechaza datos sensibles |
| AT-VAL-07 | Telemetry desactivado | Flujo principal de negocio no se bloquea |

---

## 3. Evidencia minima para Sprint Review

- Matriz AT-R01..AT-R07 validada.
- Checklist AT con secciones A..G completas.
- Simulacion de degradacion Push con Pull operativo.
- Validacion de NFR AT con metas p95 y entrega eventual.

---

## 4. Criterios de aceptacion

- [ ] Todos los casos AT-VAL-01..AT-VAL-07 tienen evidencia.
- [ ] La degradacion fail-soft esta demostrada.
- [ ] App Api/Telemetry lista para pasar de diseno a implementacion.
