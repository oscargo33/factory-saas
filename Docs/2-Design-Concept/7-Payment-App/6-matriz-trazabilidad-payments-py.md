# Matriz de Trazabilidad — Payments

**ID:** PY-6-TRAZ

Interacciones trazables:

- `Orders -> Payments`: Orders emits `order.created`, Payments `start_session` consumes and creates `PaymentIntent`.
- `Payments -> Orders`: on `payment.confirmed` Outbox event triggers `orders.mark_as_paid`.
- `Payments -> Orchestrator`: after confirmation, create `provision.requested` outbox for Orchestrator to enable entitlements.
- `Payments -> Telemetry`: emit `payment.confirmed` with `tenant_id, order_id, operation_id, plan_id, matrix_version, amount`.

Correlation fields required: `tenant_id`, `order_id`, `operation_id`, `provider_intent_id`, `price_snapshot_id`, `matrix_version`.
