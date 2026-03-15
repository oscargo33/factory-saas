# Matriz de Trazabilidad — Orders

**ID:** OD-6-TRAZ

Interacciones y eventos trazables:

- `Order -> Payment`: `order.created` -> `payments.start_session(order_id)` -> `payment.confirmed` -> `orders.mark_as_paid(order_id)`
- `Order -> ProductOrchestrator`: after `mark_as_paid`, create `OutboxEvent` `provision.requested` with `order_line` snapshots for provisioning entitlements.
- `Order -> Telemetry`: emit `order.created`, `payment.confirmed`, `provision.requested` including `matrix_version` and `price_snapshot` pointers.
- `Order -> Support`: on payment failure retries exceeded, open ticket automatic.

Payload minimal fields for correlation:
- `tenant_id`, `order_id`, `operation_id`, `profile_id`, `items[]` (product_id, product_type, price_snapshot_id), `matrix_version`.
