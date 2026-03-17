# Endpoints, Middleware y Adapters — Marketing

**ID:** MA-4-ENDPOINTS

Endpoints públicos sugeridos:

- `GET /api/v1/marketing/campaigns/` — lista de campañas activas para tenant (paginated).
- `GET /api/v1/marketing/campaigns/{id}/` — detalle campaña.
- `POST /api/v1/marketing/track/` — endpoint ingest rápido para eventos cliente (debounce, rate limit).
- `POST /api/v1/marketing/coupons/validate/` — validar código de cupón (sin aplicar cobro).
- `POST /api/v1/marketing/webhooks/` — recibir webhooks de terceros (ad networks, SMTP delivery reports).

Middleware/concerns:
- `TenantAwareMiddleware` — resolver `tenant_id` desde subdominio/headers.
- `ConsentMiddleware` — valida consentimiento de tracking antes de aceptar `POST /track`.
- Rate limiting por `tenant_id` y `api_key`.

Adapters:
- `adapters/email_provider.py` — abstracción para enviar emails (providers: SES, Sendgrid, SMTP) con retry y webhooks.
- `adapters/push_provider.py` — abstracción para push notifications providers.

Seguridad:
- Firmas HMAC en webhooks, validación de `X-Provider-Signature`.
