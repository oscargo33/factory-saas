# Endpoints y Webhooks — Payments

**ID:** PY-4-ENDPOINTS

Endpoints principales:

- `POST /api/v1/payments/start/` — inicia sesión de pago para `order_id` (internally calls `start_session`).
- `POST /api/v1/payments/webhook/` — webhook receiver for gateways (signed) that calls `handle_webhook`.
- `GET /api/v1/payments/subscriptions/{tenant_id}/` — subscription summary.
- `GET /api/v1/payments/invoices/{invoice_id}/` — invoice retrieval.

Middleware/concerns:
- `WebhookSignatureMiddleware` — validates gateway signature.
- `IdempotencyMiddleware` — dedupe by `Idempotency-Key` header for `start` and webhook deliveries.
- `TenantAwareMiddleware`.

Security:
- Strictly verify provider signatures and origins. Use rotating keys/secrets.
