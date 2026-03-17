# Documento: NFR, Seguridad y Operación - App Api Telemetry

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** AT-7-NFR
**Ubicación:** `./Docs/2-Design-Concept/2-Api-Telemetry-App/7-nfr-seguridad-operacion-telemetry-at.md`
**Anchor Docs:** `Docs/2-Design-Concept/0-Factory-Saas/15-protocolo-comunicacion-central-fs.md`, `Docs/2-Design-Concept/0-Factory-Saas/18-matriz-seguridad-compliance-fs.md`

---

## 1. Propósito

Definir NFR operativos y de seguridad para que Api/Telemetry sea robusta, observable y no intrusiva al negocio.

---

## 2. NFR de rendimiento y entrega

| NFR ID | Objetivo | Meta |
|---|---|---|
| AT-NFR-01 | Latencia endpoint `/ping/` | p95 < 50 ms |
| AT-NFR-02 | Latencia endpoint `/inspect/` | p95 < 250 ms |
| AT-NFR-03 | Tiempo promedio de Push batch | < 5 s por lote |
| AT-NFR-04 | Entrega eventual | >= 99% eventos entregados en 30 min |

---

## 3. NFR de disponibilidad y resiliencia

| NFR ID | Objetivo | Regla |
|---|---|---|
| AT-NFR-05 | Falla de La Central | Nunca bloquear operaciones de negocio |
| AT-NFR-06 | Backoff controlado | Reintentos con exponencial + jitter |
| AT-NFR-07 | Operación en modo degradado | Pull local disponible aunque Push falle |

---

## 4. Seguridad

| Control | Aplicación |
|---|---|
| Auth Pull | `X-Factory-Token` obligatorio en `/inspect/` y `/events/` |
| Auth Push | JWT con TTL <= 60 s |
| PII | Bloqueo y sanitización de payload sensible |
| Trazabilidad | `X-Trace-ID` obligatorio en eventos de error/critical |
| Auditoría | Registro inmutable de acciones sensibles |

---

## 5. Operación y monitoreo

Métricas mínimas:
- `telemetry_push_success_total`
- `telemetry_push_failure_total`
- `telemetry_pending_count`
- `telemetry_dead_letter_count`
- `telemetry_pull_requests_total`

Alertas sugeridas:
- pending > 1000 por más de 15 min
- failure ratio > 20% en 10 min
- inspect auth failures > 30 en 5 min

---

## 6. Criterios de aceptación

- [ ] NFR de rendimiento y resiliencia definidos con metas medibles.
- [ ] Controles de seguridad de Push/Pull documentados.
- [ ] Política de alertas operativas definida para producción.
