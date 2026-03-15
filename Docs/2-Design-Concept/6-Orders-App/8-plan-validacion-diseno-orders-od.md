# Plan de Validación y Criterios — Orders

**ID:** OD-8-VALID

Criterios de aceptación (mínimos):

- `freeze_cart` crea `Order`, `OrderLine` y `PriceSnapshot` en una transacción y genera `OutboxEvent`.
- `freeze_cart` invoca `enforce_plan_policy` y falla con razón clara en caso de `denied`.
- `mark_as_paid` es idempotente por `payment_reference.operation_id` y genera `provision.requested` outbox.
- Workers de Outbox procesan y actualizan `status` correctamente con reintentos y poison handling.
- Telemetry events emitidos con `matrix_version` y `price_snapshot` metadata.

Casos de prueba de aceptación (mínimos):
1. Crear `Cart` con productos permitidos → `freeze_cart` → Order creado y Outbox event creado.
2. Simular `payment.confirmed` webhook → `mark_as_paid` idempotente → Outbox `provision.requested` creado.
3. Simular `product_orchestrator` no disponible → `freeze_cart` solo permite `local_only`/`is_demo`.
