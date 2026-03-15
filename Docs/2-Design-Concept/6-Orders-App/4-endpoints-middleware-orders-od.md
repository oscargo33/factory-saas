# Endpoints, Middleware y Webhooks — Orders

**ID:** OD-4-ENDPOINTS

Endpoints sugeridos:

- `POST /api/v1/carts/{cart_id}/freeze/` — invoca `freeze_cart` y crea `Order`.
- `GET /api/v1/orders/{order_id}/` — detalle de orden.
- `POST /api/v1/orders/{order_id}/pay/` — inicia sesión de pago (redirige a `payments` provider).
- `POST /api/v1/webhooks/payments/` — handler idempotente para webhooks de pasarela que llaman `mark_as_paid`.
- `POST /api/v1/orders/{order_id}/fulfill/` — (internal) endpoint para disparar fulfillment / orquestación.

Middleware/concerns:
- `TenantAwareMiddleware` — resolver `tenant_id`.
- `IdempotencyMiddleware` — validar `Idempotency-Key` para endpoints mutantes (`freeze`, `pay`).
- Validación de payloads contra DTOs.

Seguridad:
- Validar esquemas y permisos; solo `mark_as_paid` aceptará webhooks firmados y encriptados según provider.
