# Documento: Push/Pull y Resiliencia - App Api Telemetry

**ID:** AT-5-OPS
**Ubicacion:** `./Docs/2-Design-Concept/2-Api-Telemetry-App/5-push-pull-resiliencia-telemetry-at.md`
**Anchor Docs:** `Docs/1-Core_Concept/2-api-app-cc.md`, `Docs/2-Design-Concept/0-Factory-Saas/11-configuracion-redis-celery-fs.md`, `Docs/2-Design-Concept/0-Factory-Saas/15-protocolo-comunicacion-central-fs.md`

---

## 1. Proposito

Definir operacion runtime de telemetria, tolerancia a fallos y controles de entrega para comunicacion con La Central.

---

## 2. Modo Push

Task principal: `telemetry.push_metrics`

| Parametro | Valor inicial |
|---|---|
| Cola Celery | `telemetry` |
| Frecuencia | cada 5 minutos |
| Batch maximo | 500 eventos |
| Timeout HTTP | 10s |
| Reintentos maximos | 10 |

Pipeline Push:
1. Seleccionar eventos pendientes/no enviados.
2. Serializar batch sin PII.
3. Firmar JWT (`CENTRAL_SECRET`, TTL 60s).
4. `POST /api/v1/ingest/` en La Central.
5. Si `201`: marcar enviados y purgar buffer.
6. Si fallo: incrementar retry y programar `next_retry_at`.

---

## 3. Modo Pull

Objetivo: inspeccion inmediata cuando La Central o soporte necesita diagnostico.

Contenido de snapshot:
- salud app (`status`, uptime, version)
- latencia media y p95
- errores 5xx ultimos N minutos
- `pending_metrics_count`
- KPI negocio agregados (sin PII)

---

## 4. Retry y backoff

Politica:
- Exponencial con jitter: `min(2^n, 300) + random(0..10)` segundos.
- `max_retries = 10`.
- Si supera maximo, evento queda en estado `dead_letter` para revision operativa.

---

## 5. Configuracion operativa

| Setting | Default | Uso |
|---|---|---|
| `TELEMETRY_ENABLED` | `True` | Activar/desactivar app sin romper consumers |
| `TELEMETRY_PUSH_INTERVAL` | `300` | Intervalo Push |
| `TELEMETRY_MAX_BATCH_SIZE` | `500` | Tamano de lote |
| `TELEMETRY_MAX_RETRIES` | `10` | Limite de reintentos |
| `CENTRAL_API_URL` | requerido | URL base La Central |
| `CENTRAL_SECRET` | requerido | Firma JWT |
| `FACTORY_PULL_TOKEN` | requerido | Auth endpoint Pull |

---

## 6. Observabilidad

Metricas minimas:
- `telemetry_push_success_total`
- `telemetry_push_failure_total`
- `telemetry_push_duration_ms`
- `telemetry_pending_count`
- `telemetry_dead_letter_count`

Alertas sugeridas:
- pending > 1000 por mas de 15 min
- failure ratio > 20% en 10 min
- dead-letter > 0

---

## 7. Criterios de aceptacion

- [ ] Push nunca bloquea transacciones de negocio.
- [ ] Pull responde con token valido aun cuando Push esta degradado.
- [ ] Retry/backoff y dead-letter documentados y verificables.
- [ ] `TELEMETRY_ENABLED=False` mantiene operacion normal del SaaS.
