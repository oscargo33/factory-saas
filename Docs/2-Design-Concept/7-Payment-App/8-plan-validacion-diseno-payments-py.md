# Plan de Validación y Criterios — Payments

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PY-8-VALID

Criterios de aceptación (mínimos):

- `start_session` crea `PaymentIntent` con `operation_id` y referencia a `price_snapshot`.
- `handle_webhook` actualiza `PaymentIntent` y crea `OutboxEvent(payment.confirmed)` en la misma transacción.
- Webhook handlers son idempotentes y deduplican por `operation_id`.
- Dunning flow configurado y comprobado en pruebas de integración.

Casos de prueba de aceptación:
1. `start_session` returns payment session for an existing order and stores operation_id.
2. Simulate `webhook` for success -> `PaymentIntent` updated, Outbox event created, `orders.mark_as_paid` eventually called.
3. Duplicate webhook deliveries with same `operation_id` do not cause double-processing.
