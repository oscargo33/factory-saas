# Matriz de Trazabilidad — Marketing

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

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

## Cobertura obligatoria DC-12/DC-13/DC-16/DC-17

- DC-12 (patron service layer): aplica en servicios de campanas/cupons y selectores de segmentacion.
- DC-13 (router dinamico y contexto tenant): aplica en ejecucion de campanas aisladas por tenant.
- DC-16 (contratos inter-app): cubierto por eventos `marketing.campaign.*` y `marketing.coupon.redeemed`.
- DC-17 (diccionario de datos logico): cubierto por campos de correlacion (`tenant_id`, `operation_id`, `campaign_id`, `matrix_version`).
