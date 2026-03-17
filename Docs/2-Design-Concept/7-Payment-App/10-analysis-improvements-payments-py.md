# Análisis profundo y mejoras aplicadas — Payments

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PY-10-ANALYSIS

Análisis y mejoras incorporadas en este diseño:

1) Idempotency and deduplication
- Problema: webhooks duplicados y retries pueden provocar dobles cargas o dobles activaciones.
- Mejora aplicada: `PaymentIntent.operation_id` único por tenant; webhook handler deduplica por `operation_id` y `provider_intent_id`. Recomendado: tabla `idempotency` o unique constraints.

2) Atomic outbox writes
- Problema: pérdida de notifications si outbox no se escribe atomically.
- Mejora aplicada: documentación de persistencia `PaymentIntent + OutboxEvent` en misma transacción; sugerir constraint `(tenant_id, operation_id, event_type)` unique to prevent duplicates.

3) Reconciliation and orphan detection
- Mejora aplicada: nightly `payments.reconcile` job spec, and rules for auto-ticketing and reconciler report with candidate fixes.

4) Dunning as a first-class flow
- Mejora aplicada: dunning schedule and telemetry hooks; recommend implementing `dunning` service that triggers `payment.retry` and communicates with `orders`/`support`.

5) Telemetry and PlanMatrix alignment
- Mejora aplicada: require `matrix_version` in PaymentIntent metadata and telemetry for every `payment.confirmed` event to ensure auditability.

6) Security and PCI considerations
- Mejora aplicada: explicit guidance not to store card data, use provider tokens, and verify webhooks; recommend periodic penetration tests and provider key rotation SOP.

7) Testability
- Mejora aplicada: contract skeletons and fixtures; recommend adding CI job to run these against a lightweight test harness that mocks providers.

Acciones recomendadas para la implementación inmediata
- Add DB unique indexes on `(tenant_id, operation_id)` for `PaymentIntent` and `(tenant_id, provider_intent_id)`.
- Implement idempotency table to store results of operations keyed by `operation_id`.
- Build `payments.reconcile` and `dunning` services and schedule via cron/Celery beat.
- Add CI pytest job that runs `payments` contract tests with mocked gateway adapters.
