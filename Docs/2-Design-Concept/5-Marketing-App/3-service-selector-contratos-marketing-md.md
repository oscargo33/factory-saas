# Service/Selector — Contratos Públicos (Marketing)

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** MA-3-CONTRATOS

Archivo: `apps/marketing/selectors.py`, `apps/marketing/services.py`

Funciones públicas (consumibles por otras apps):

- `track_event(event_name: str, tenant_id: UUID, profile_id: UUID, metadata: dict) -> None`
  - Uso: event tracking (consumidor principal: Telemetry). Debe escribir `MarketingEvent` y encolar Outbox/Telemetry.

- `get_active_campaigns(tenant_id: UUID) -> list[CampaignDTO]`
- `get_campaign_detail(campaign_id: UUID, tenant_id: UUID) -> CampaignDetailDTO`
- `create_campaign(tenant_id: UUID, payload: dict) -> CampaignDTO`
- `list_coupons(tenant_id: UUID) -> list[CouponDTO]`
- `validate_coupon(code: str, tenant_id: UUID, product_id: UUID) -> CouponValidationResultDTO`
- `apply_coupon(code: str, order_id: UUID, tenant_id: UUID) -> CouponApplyResultDTO`
- `get_segments(tenant_id: UUID) -> list[SegmentDTO]`

Fallbacks si `marketing` no está instalado:
- `get_active_campaigns` → `[]` (vacio)
- `validate_coupon` → retorna `denied` con razón `marketing_unavailable`
- `track_event` → escribe a `TelemetryEvent` directamente (si Telemetry disponible) o log local.

Reglas de integración:
- `apply_coupon` no debe aplicar descuentos — solo retornar resultado; la aplicación monetaria ocurre en `orders` durante checkout bajo el control de `OrdersService`.
- Todas las funciones públicas deben validar `tenant_id` y comportarse en modo seguro si la app depende de otros módulos faltantes.
