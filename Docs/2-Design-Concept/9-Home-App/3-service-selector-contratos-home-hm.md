# Contratos — Home App

**ID:** HM-3-CT

Objetivo: definir selectors y services que `Home` expone a otras apps y consumir.

Exposición (selectors/services públicos):

- `get_home_widgets(tenant_id: UUID) -> list[HomeWidgetDTO]` — lista widgets activos y configuración.
- `get_home_snapshot(tenant_id: UUID, snapshot_key: str) -> JSON | None` — snapshot cache para render rápido.
- `report_widget_interaction(tenant_id: UUID, widget_key: str, profile_id: UUID, metadata: dict) -> None` — telemetría de interacción (no PII).

Consumo (soft-deps):
- `product_orchestrator.get_product_detail` — para enlazar productos en widgets.
- `marketing.track_event` / `RecommendationFeed` — para mostrar campañas/personalización.
- `profile.get_display_name` — solo para mostrar nombres en widgets cuando esté disponible.

Seguridad y Tenancy:
- Todos los DTOs aceptan/retornan `tenant_id` y validan contexto en middleware.
- Telemetry: `report_widget_interaction` emite `TelemetryEvent(home.widget.interaction)` sin PII.

Versionado:
- Publicar versión en DC-16 al exponer nuevos widgets o cambiar payloads.
