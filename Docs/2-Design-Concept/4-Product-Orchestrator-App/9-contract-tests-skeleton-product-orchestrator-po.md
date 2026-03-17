# Product Orchestrator — Contract Tests Skeleton

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

Propósito: definir casos de prueba y vectores JSON para validar contratos públicos y flujos críticos del Orchestrator.

Archivos de ejemplo referenciados:
- `../../0-Factory-Saas/contracts-examples/plan_matrix_example.json`
- `../../0-Factory-Saas/contracts-examples/product_detail_example.json`
- `../../0-Factory-Saas/contracts-examples/price_snapshot_example.json`
- `../../0-Factory-Saas/contracts-examples/outbox_event_example.json`
- `../../0-Factory-Saas/contracts-examples/order_line_example.json`

Casos mínimos sugeridos:
1. `PlanMatrix` enforcement
   - Input: `plan_matrix_example.json` y `enforce_plan_policy(tenant_id, product_id, vertical_key)`.
   - Expect: `allowed` para `prod-uuid-a`/`feature:reports`, `denied` para feature no listada.

2. `ProductDetail` DTO contract
   - Input: `product_detail_example.json`
   - Expect: `product_type` y `fulfillment_strategy` presentes y con valores permitidos (`subscription|one_time|metered`, `digital|manual|third_party`).

3. Price snapshot persistence
   - Input: creación de `Order` con `order_line_example.json`.
   - Expect: `price_snapshot` copiado y persistido; `price_version_id` no nulo.

4. Outbox + provisioning flow
   - Input: `outbox_event_example.json` con `event_type=provision.requested`.
   - Expect: processor marca `status=sent` tras entrega simulada; idempotencia probada re-enviando mismo `operation_id`.

Notas:
- Estos tests son skeletons: implementadores pueden traducirlos a pytest + fixtures que carguen los JSON en DB de pruebas y verifiquen selectores/servicios.

Acceptance criteria reproducibles:
- [ ] Cada caso define input fixture y output esperado verificable.
- [ ] Se valida enforcement por `plan_matrix` y respuesta `allowed/denied` trazable.
- [ ] Se valida idempotencia en reprocesamiento por `operation_id`.
