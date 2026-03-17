# Análisis profundo y mejoras aplicadas — Orders

**ID:** OD-10-ANALYSIS

Resumen de análisis y mejoras aplicadas en este diseño:

1) Consistencia transaccional
- Problema identificado: riesgo de pérdida de eventos o provisioning fuera de sincronía si Outbox no se persiste atómicamente con Order.
- Mejora aplicada: documentación explícita que exige persistencia de `Order`, `OrderLine`, `PriceSnapshot` y `OutboxEvent` en la misma transacción; se recomienda patrón `transaction + outbox table` y worker con idempotency por `operation_id`.

2) Idempotencia y deduplicación
- Problema: webhooks duplicados pueden provocar dobles marcados como pagado o dobles provisioning.
- Mejora aplicada: `mark_as_paid` y handlers deben usar `operation_id`/`payment_intent_id` para deduplicación; añadir `Idempotency-Key` middleware y `operation_id` stored in Outbox payload.

3) PlanMatrix enforcement integration
- Problema: inconsistent enforcement across checkout/payment/provisioning could open access gaps.
- Mejora aplicada: `freeze_cart` must call `enforce_plan_policy` for each product; `payments` and `orchestrator` must include `matrix_version` in telemetry to audit decisions.

4) PriceSnapshot model and retention
- Mejora applied: `PriceSnapshot` introduced as a first-class artifact; recommend masked archival for GDPR while keeping billing traceability.

5) Observability and runbooks
- Mejora applied: explicit metrics and TelemetryEvent types defined; poison queue runbook and auto-ticketing rule described.

6) Testability
- Mejora applied: added contract-test skeletons and fixtures to validate enforcement, snapshoting and outbox flows.

Acciones recomendadas para implementación inmediata
- Implementar `outbox.processor` worker with concurrency and backoff parameters documented in telemetry runbook.
- Add DB unique constraint on `(tenant_id, operation_id, event_type)` to prevent duplicate outbox rows.
- Implement Idempotency table or store operation results keyed by `operation_id`.
- Create pytest harness that runs the skeletons against a test DB and mocked adapters.
