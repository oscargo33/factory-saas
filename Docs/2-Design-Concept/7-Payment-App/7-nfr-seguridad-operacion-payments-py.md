# NFR, Seguridad y Operación — Payments

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PY-7-NFR

No funcionales y controles operativos:

- **Availability:** Payment endpoints and webhooks must be highly available and horizontally scalable.
- **Consistency:** ensure transactionality for PaymentIntent and Outbox writes.
- **Idempotency:** webhook handlers must be idempotent by `operation_id` or `provider_intent_id`.
- **Latency:** `start_session` should respond within 500ms for typical cases; use async creation for heavy provider interactions.
- **Security:** webhooks signed, secrets rotated; PCI compliance guidance (never store card numbers).
- **Auditability:** preserve `price_snapshot` references and `matrix_version` for all confirmed payments.
- **Monitoring:** metrics: `payment_intent_created_total`, `payment_confirmed_total`, `payment_failed_total`, `payment_reconciliation_errors`.
