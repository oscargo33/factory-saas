# Service/Selector — Contratos Públicos (Payments)

**ID:** PY-3-CONTRATOS

Archivo: `apps/payments/services.py`, `apps/payments/selectors.py`

Funciones públicas (consumibles por otras apps):

- `start_session(order_id: UUID) -> PaymentSessionDTO`
  - Prepara intent de pago, calcula `amount` desde `Order` y retorna `provider` session info.

- `handle_webhook(payload: dict) -> None` (idempotent)
  - Procesa notificaciones de pasarelas y actualiza `PaymentIntent`.

- `get_active_subscription(tenant_id: UUID) -> SubscriptionSummaryDTO`
- `get_invoice(invoice_id: UUID) -> InvoiceDTO`

Reglas de integración:
- `start_session` debe read `Order`'s `price_snapshot` and include `matrix_version` in the `PaymentIntent.metadata`.
- `handle_webhook` on success must create `OutboxEvent(event_type=payment.confirmed)` with `order_id, operation_id, price_snapshot_id` and persist in same transaction.
- All public functions must validate `tenant_id` and respect soft-dependencies.

Fallbacks:
- If `orders` not available, `start_session` returns `error` with `requires_order` flag.
- If `telemetry` unavailable, persist telemetry to local contingency log.
