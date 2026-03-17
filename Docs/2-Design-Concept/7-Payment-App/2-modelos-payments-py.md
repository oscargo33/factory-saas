# Modelos de Datos — App Payments

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PY-2-MDL

Propósito: definir los artefactos financieros: `PaymentIntent`, `Invoice`, `Subscription` y mecanismos de reconciliación.

Entidades principales (esquema `tenant_{slug}` o `public` según política):

1. `PaymentIntent`
 - `id`: UUID PK
 - `order_id`: UUID (referencia lógica a Order)
 - `tenant_id`: UUID
 - `amount`: Decimal(12,2)
 - `currency`: CharField(3)
 - `status`: `created|processing|succeeded|failed|requires_action`
 - `provider`: CharField (e.g., stripe, paypal)
 - `provider_intent_id`: CharField (ID en el gateway)
 - `operation_id`: CharField unique (idempotency key)
 - `metadata`: JSONB
 - `created_at`, `updated_at`

2. `Invoice`
 - `id`: UUID
 - `subscription_id`: UUID (nullable)
 - `order_id`: UUID (nullable)
 - `amount`, `currency`, `line_items` JSONB
 - `status`: `draft|issued|paid|cancelled`

3. `Subscription`
 - `id`: UUID
 - `tenant_id`: UUID
 - `plan_id`: UUID
 - `gateway_subscription_id`: CharField
 - `status`: `trialing|active|past_due|cancelled`
 - `current_period_start`, `current_period_end`

4. `PaymentEvent` / `OutboxEvent`
 - Payment actions persisted in outbox for downstream systems (orders, orchestrator) with `operation_id` and `idempotency` keys.

Reglas y constraints:
- `PaymentIntent.operation_id` must be unique per tenant to enforce idempotency.
- On webhook confirmation, persist `PaymentIntent` status and create `OutboxEvent(event_type=payment.confirmed)` in same transaction.
- Include `price_snapshot` metadata in telemetry and outbox events to guarantee billing traceability.
