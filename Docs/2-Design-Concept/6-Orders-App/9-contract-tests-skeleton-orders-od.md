# Orders — Contract Tests Skeleton

Propósito: casos mínimos para validar `freeze_cart`, `mark_as_paid`, PriceSnapshot y Outbox flows.

Archivos referenciados (fixtures):
- `../../0-Factory-Saas/contracts-examples/product_detail_example.json`
- `../../0-Factory-Saas/contracts-examples/price_snapshot_example.json`
- `../../0-Factory-Saas/contracts-examples/order_line_example.json`
- `../../0-Factory-Saas/contracts-examples/outbox_event_example.json`

Casos sugeridos:
1. `freeze_cart` happy path:
   - Fixture: cart with product `prod-uuid-a`.
   - Expect: Order created, PriceSnapshot created, OutboxEvent `order.created` persisted, `enforce_plan_policy` called and returns allowed.

2. `freeze_cart` with denied plan:
   - Simulate `enforce_plan_policy` denying product → `freeze_cart` fails with `plan_denied`.

3. `mark_as_paid` idempotency:
   - Simulate payment webhook twice with same `operation_id` → `mark_as_paid` processed once; duplicate ignored.

4. Outbox processing:
   - Insert `outbox_event_example.json` with `status=pending` → run worker → expect `sent` and telemetry emitted.

Notas: traducir a pytest fixtures que inyecten DB records and mock external adapters (payments, orchestrator).
