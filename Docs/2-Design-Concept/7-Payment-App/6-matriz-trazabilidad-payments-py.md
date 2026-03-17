# Matriz de Trazabilidad — Payments

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PY-6-TRAZ

Interacciones trazables:

- `Orders -> Payments`: Orders emits `order.created`, Payments `start_session` consumes and creates `PaymentIntent`.
- `Payments -> Orders`: on `payment.confirmed` Outbox event triggers `orders.mark_as_paid`.
- `Payments -> Orchestrator`: after confirmation, create `provision.requested` outbox for Orchestrator to enable entitlements.
- `Payments -> Telemetry`: emit `payment.confirmed` with `tenant_id, order_id, operation_id, plan_id, matrix_version, amount`.

Correlation fields required: `tenant_id`, `order_id`, `operation_id`, `provider_intent_id`, `price_snapshot_id`, `matrix_version`.

## Cobertura obligatoria DC-12/DC-13/DC-16/DC-17

- DC-12 (patron service layer): aplica en servicios de sesion de pago, confirmacion e idempotencia.
- DC-13 (router dinamico y contexto tenant): aplica en procesamiento de intents por tenant.
- DC-16 (contratos inter-app): cubierto por eventos `payment.confirmed` y contrato de provision hacia Orchestrator.
- DC-17 (diccionario de datos logico): cubierto por `PaymentIntent`, referencias a `Order/PriceSnapshot` y campos de correlacion.
