# Modelos de Datos — App Orders

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** OD-2-MDL

Propósito: definir `Cart`, `Order`, `OrderLine` y artefactos auxiliares (PriceSnapshot) con exigencias operativas.

Entidades principales (esquema `tenant_{slug}`):

1. `Cart`
 - `id`: UUID PK
 - `tenant_id`: UUID
 - `user_id`: int
 - `items`: JSONB (lista temporal de `product_id`, `quantity`, `metadata`)
 - `updated_at`

2. `Order`
 - `id`: UUID PK
 - `tenant_id`: UUID
 - `user_id`: int
 - `status`: `draft|pending|paid|processing|fulfilled|cancelled`
 - `total_amount`: Decimal(12,2)
 - `currency`: CharField(3)
 - `metadata`: JSONB
 - `created_at`, `updated_at`

3. `OrderLine` (por cada item en la orden)
 - `id`: UUID PK
 - `order_id`: UUID (referencia lógica)
 - `product_id`: UUID
 - `quantity`: PositiveInteger
 - `unit_price`: Decimal(10,2)
 - `product_type`: CharField(30)  — copiar desde `ProductDetail` (`subscription|one_time|metered`)
 - `price_snapshot_id`: UUID -> referencia a `PriceSnapshot` (lógica)

4. `PriceSnapshot` (cross-app)
 - `id`: UUID PK
 - `order_line_id`: UUID
 - `product_id`: UUID
 - `price`: Decimal(10,2)
 - `currency`: CharField(3)
 - `price_version_id`: CharField
 - `applied_taxes`: JSONB
 - `captured_at`: DateTime

5. `OutboxEvent` (ver DC-17)

Reglas y constraints:
- Al crear `Order` (freeze_cart) copiar `product_type` y crear `PriceSnapshot` por cada `OrderLine` en la misma transacción.
- `OrdersService.freeze_cart` debe invocar `product_orchestrator.enforce_plan_policy(tenant_id, product_id, vertical_key)` y fallar si `denied`.
- Al persistir `Order` en estado `pending`, crear `OutboxEvent` con `event_type=order.created` y payload con `order_id, tenant_id, operation_id, items[]`.
- Evitar FK duras a apps externas; usar IDs lógicas y contratos/DTOs.
