# Payments — Contract Tests Skeleton

Propósito: casos mínimos para validar `start_session`, `handle_webhook`, Outbox and reconciliation.

Archivos referenciados (fixtures):
- `../../0-Factory-Saas/contracts-examples/order_line_example.json`
- `../../0-Factory-Saas/contracts-examples/price_snapshot_example.json`
- `../../0-Factory-Saas/contracts-examples/outbox_event_example.json`

Casos sugeridos:
1. `start_session` happy path:
   - Fixture: existing `Order` with `price_snapshot`.
   - Expect: `PaymentIntent` created with `operation_id`, provider session returned.

2. Webhook handling (idempotency):
   - Simulate webhook success twice with same `operation_id` -> `PaymentIntent` updated once, Outbox `payment.confirmed` created once.

3. Reconciliation job:
   - Simulate provider transactions missing locally -> reconcile marks differences and creates tickets.

Notas: implementar pytest fixtures that mock gateways (stripe/paypal) and use DB test harness.
