# Trazabilidad — Home App

**ID:** HM-6-TRZ

Producers / Consumers:

- Produce: `home.snapshot.generated`, `home.widget.interaction` (TelemetryEvent)
- Consumes: `RecommendationFeed`/`marketing` data, `product_orchestrator` product detail, `telemetry` for usage aggregates

Contract mapping:
- `get_home_widgets` documentado en DC-16 (añadir referencia).
- Modelos `HomeWidget` y `HomeSnapshot` referenciados en DC-17.

Correlation fields:
- `tenant_id`, `operation_id`, `profile_id` (cuando aplica), `snapshot_key`.

Versioning:
- Incluir `home_api_version` in telemetry and snapshot metadata for rollback/troubleshooting.
