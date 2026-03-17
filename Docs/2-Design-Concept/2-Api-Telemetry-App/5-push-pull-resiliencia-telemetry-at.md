# Documento: Push/Pull y Resiliencia - App Api Telemetry

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

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

## 8. Outbox Worker Runbook (integracion cross-app)

Objetivo: procesar la tabla `OutboxEvent` de forma confiable, exponiendo metricas operativas y evitando duplicados en consumidores externos.

Parametros recomendados:
- Worker: `outbox.processor` (Celery beat + worker).
- Concurrency: 4 workers por servicio (ajustable por carga).
- Batch size: 50 eventos por ciclo.
- Timeout HTTP: 10s por envio.
- Max retries por evento: 5 (backoff exponencial con jitter).

Flujo de trabajo:
1. Seleccionar `OutboxEvent` con `status = pending` ordenado por `created_at` (batch).
2. Marcar transaccionalmente `status = processing` y `processing_started_at`.
3. Enviar el `payload` al endpoint destino (adapters o La Central según `event_type`).
4. Si `2xx`: marcar `status = sent`, `sent_at` y emitir `TelemetryEvent(outbox.sent)`.
5. Si fallo transitorio: incrementar `retry_count`, calcular backoff y dejar `status = pending` para reintento; emitir `TelemetryEvent(outbox.retry)`.
6. Si supera `max_retries`: mover a `status = failed` y emitir `TelemetryEvent(outbox.failed)`; opcionalmente colocar en `poison_queue` para analisis humano.

Idempotencia y seguridad:
- Cada `OutboxEvent` debe incluir `operation_id` y `idempotency_key` en el `payload` para permitir reintentos seguros en el consumidor.
- Consumidores deben ser idempotentes por `operation_id`.

Metricas y alertas:
- `outbox_pending_count` (alerta: >1000 por 15m).
- `outbox_processing_duration_ms` (p95 > 5s alerta).
- `outbox_retry_failure_total` (tasa de fallos > 10% alerta).
- `outbox_poison_count` (cualquier valor > 0 alerta critica).

Observabilidad:
- Emitir `TelemetryEvent` para `outbox.sent`, `outbox.retry`, `outbox.failed`, `outbox.poison` con `aggregate_id, event_type, tenant_id, retry_count`.

Operaciones de emergencia:
- Toggle operativo `OUTBOX_ENABLED=False` para pausar envio sin borrar eventos.
- Script de reintroduccion: herramienta `outbox.replay(start_date, end_date, filter_event_types)` para reprocesar eventos fallidos tras resolver la causa raiz.

Integracion con alertas y runbook:
- On `outbox_poison_count > 0`: abrir ticket automatico en `support` con evidencia y payload (sanitize PII).
