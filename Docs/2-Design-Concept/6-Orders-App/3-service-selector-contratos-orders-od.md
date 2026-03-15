# Service/Selector — Contratos Públicos (Orders)

**ID:** OD-3-CONTRATOS

Archivo: `apps/orders/selectors.py`, `apps/orders/services.py`

Funciones públicas (consumibles por otras apps):

- `freeze_cart(cart_id: UUID) -> OrderDTO`
  - Congela el carrito creando `Order` y `OrderLine` con `price_snapshot`.
  - Internamente llama a `product_orchestrator.enforce_plan_policy` para cada producto.

- `get_order_summary(order_id: UUID, tenant_id: UUID) -> OrderSummaryDTO`
- `mark_as_paid(order_id: UUID, payment_reference: dict) -> None` (idempotente)
- `get_open_orders_count(tenant_id: UUID) -> int`
- `get_order_by_id(order_id: UUID, tenant_id: UUID) -> OrderDTO | None`

Fallbacks y reglas:
- `freeze_cart` si `product_orchestrator` no disponible: validar `source_strategy` y permitir solo `local_only` o `is_demo` productos.
- `mark_as_paid` debe crear `OutboxEvent` con `event_type=payment.confirmed` y ser idempotente por `payment_reference.operation_id`.

Integración con Payments/Orchestrator:
- `Orders` no aplica cobros; Payments debe consumir `order_id` y confirmar mediante `mark_as_paid`.
- `Orders` es responsable de crear `price_snapshot` y exponer `order_line` con `product_type` para que `payments` y `orchestrator` actúen correctamente.
