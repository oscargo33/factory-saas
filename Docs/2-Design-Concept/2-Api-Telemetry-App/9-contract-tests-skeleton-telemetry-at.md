# Api Telemetry — Contract Tests Skeleton

Propósito: casos mínimos para validar Outbox processing y eventos de telemetría emitidos por flujos cross-app.

Archivos de ejemplo referenciados:
- `../../0-Factory-Saas/contracts-examples/outbox_event_example.json`
- `../../0-Factory-Saas/contracts-examples/price_snapshot_example.json`
- `../../0-Factory-Saas/contracts-examples/product_detail_example.json`
- `../../0-Factory-Saas/contracts-examples/plan_matrix_example.json`

Casos mínimos sugeridos:
1. Outbox processing
   - Input: `outbox_event_example.json` con `status=pending`.
   - Expect: worker procesa y emite `TelemetryEvent(outbox.sent)`; `status` -> `sent`.

2. Telemetry push integrity
   - Input: batch que incluye `payment.confirmed` y `provision.requested` con `telemetry_identity`.
   - Expect: payload anonimizado, firma JWT válida y POST correcto a La Central (simulado).

3. Observability metrics
   - Verificar que `outbox_pending_count` y `telemetry_push_success_total` se incrementen adecuadamente cuando se simulan fallos y recuperaciones.

Notas: traducir estos skeletons a pruebas automatizadas que invoquen workers y endpoints con fixtures.
