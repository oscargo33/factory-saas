# Order Lifecycle, Outbox and Fallbacks

**ID:** OD-5-OPS

Order lifecycle (resumen): Draft -> Pending -> Paid -> Processing -> Fulfilled/Completed -> Cancelled

Requisitos operativos clave:

- **Atomic snapshot + outbox:** `freeze_cart` must persist `Order`, `OrderLine` and `PriceSnapshot` and create `OutboxEvent(event_type=order.created)` within the same DB transaction to guarantee at-least-once downstream delivery.
- **Idempotency:** All handlers must be idempotent by `operation_id` (order creation, payment confirmation, provisioning). Use `operation_id` recorded in `OutboxEvent.payload`.
- **Retries and backoff:** Exponential backoff with jitter for consumer retries. `max_retries=5` default; move to `failed/poison` after that.
- **Poison queue:** Provide `outbox.poison` monitoring and automatic support ticket creation when poison events detected.

Fallback behaviours:
- If `payments` unavailable at checkout, allow `Order` creation with `status=pending` and flag `requires_payment=true`; provide user-friendly flow to retry payment later.
- If `product_orchestrator` unavailable: allow `demo` products and flag `provisioning_skipped=true` in order metadata; automatic reconciliation when orchestrator back.

Observability:
- Metrics: `orders_created_total`, `orders_pending_total`, `order_payment_confirmed_total`, `order_outbox_pending_count`, `order_outbox_failed_total`.
- Telemetry events: emit `order.created`, `order.payment.confirmed`, `order.provision.requested` with `tenant_id, order_id, operation_id, matrix_version`.
