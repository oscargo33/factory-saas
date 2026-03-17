# Matriz de Trazabilidad — Orders

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** OD-6-TRAZ

Interacciones y eventos trazables:

- `Order -> Payment`: `order.created` -> `payments.start_session(order_id)` -> `payment.confirmed` -> `orders.mark_as_paid(order_id)`
- `Order -> ProductOrchestrator`: after `mark_as_paid`, create `OutboxEvent` `provision.requested` with `order_line` snapshots for provisioning entitlements.
- `Order -> Telemetry`: emit `order.created`, `payment.confirmed`, `provision.requested` including `matrix_version` and `price_snapshot` pointers.
- `Order -> Support`: on payment failure retries exceeded, open ticket automatic.

Payload minimal fields for correlation:
- `tenant_id`, `order_id`, `operation_id`, `profile_id`, `items[]` (product_id, product_type, price_snapshot_id), `matrix_version`.

## Cobertura obligatoria DC-12/DC-13/DC-16/DC-17

- DC-12 (patron service layer): aplica en servicios de checkout, pricing y orquestacion de estado de orden.
- DC-13 (router dinamico y contexto tenant): aplica en ciclo de vida de ordenes por schema tenant.
- DC-16 (contratos inter-app): cubierto por eventos `order.created`, `payment.confirmed`, `provision.requested`.
- DC-17 (diccionario de datos logico): cubierto por `Order`, `OrderLine`, `PriceSnapshot`, `OutboxEvent` y campos de correlacion.
