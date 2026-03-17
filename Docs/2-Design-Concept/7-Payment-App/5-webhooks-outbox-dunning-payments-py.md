# Webhooks, Outbox, Dunning and Reconciliation — Payments

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PY-5-OPS

Runbook resumen:

1. `start_session(order_id)` creates `PaymentIntent` with `operation_id` and persists it.
2. Frontend redirects to provider; provider calls `webhook` on status updates.
3. `handle_webhook` verifies signature and status, updates `PaymentIntent` and in same transaction creates `OutboxEvent(event_type=payment.confirmed)`.
4. `orders.mark_as_paid(order_id, payment_reference)` should be called by consumer of outbox or directly by payments via safe contract.

Dunning policy:
- Retry schedule: day 0 (immediate), day 3 (email), day 7 (email + in-app), day 14 (suspend entitlements), day 21 (cancel subscription).
- On each retry failure, emit telemetry `payment.dunning.attempt` with `attempt_number`.

Reconciliation:
- Nightly job `payments.reconcile_failed` compares provider transactions with local `PaymentIntent`s and attempts to reconcile `missing` or `orphaned` payments.

Idempotency and safety:
- `PaymentIntent.operation_id` must be used by webhook handlers to prevent double processing.
- Persist `provider_intent_id` and add unique index on `(tenant_id, provider_intent_id)`.
