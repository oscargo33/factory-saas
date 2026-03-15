# Matriz de Trazabilidad — Marketing

**ID:** MA-6-TRAZ

Registro de interacciones y dependencias entre Marketing y otras apps:

- `Campaign -> Orders`: cuando campaña genera `purchase` (promo), Marketing emite `marketing.coupon.redeemed` hacia Orders via Outbox.
- `Campaign -> Payments`: influjos de trial o descuentos informados a Payments para reconciliación de GMV.
- `Campaign -> ProductOrchestrator`: lectura de catálogo para `applies_to_products` y para mostrar tarjetas de producto en campañas.
- `Marketing -> Telemetry`: emitir eventos `marketing.campaign.sent`, `marketing.campaign.open`, `marketing.coupon.redeemed`.
- `Marketing -> Support`: en casos de `bounce` o `deliverability` alto, abrir ticket automático.

Trace keys (fields) obligatorios en payloads para correlación:
- `tenant_id`, `operation_id`, `campaign_id`, `profile_id`/`recipient_id`, `matrix_version` (si aplica)

Fallback behaviors: documentados en `5-campaigns-fallback-marketing-md.md`.
