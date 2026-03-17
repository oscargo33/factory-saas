# Trazabilidad — Home App

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

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

## Cobertura obligatoria DC-12/DC-13/DC-16/DC-17

- DC-12 (patron service layer): aplica en composicion de widgets/snapshot y selectores de feed.
- DC-13 (router dinamico y contexto tenant): aplica en generacion de home por tenant/perfil.
- DC-16 (contratos inter-app): cubierto por contrato `get_home_widgets` y eventos `home.snapshot.generated`.
- DC-17 (diccionario de datos logico): cubierto por `HomeWidget`, `HomeSnapshot` y campos de correlacion (`tenant_id`, `operation_id`, `snapshot_key`).
