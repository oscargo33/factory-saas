# Endpoints — Home App

**ID:** HM-4-EP

API internas/externas relevantes:

- `GET /internal/home/widgets` — retorna `get_home_widgets` (service-token + tenant header).
- `GET /internal/home/snapshot/{snapshot_key}` — retorna `get_home_snapshot`.
- `POST /internal/home/interaction` — `report_widget_interaction` (rate-limited, idempotent for same `operation_id`).
- `GET /home/landing` — public landing (cached), rendered por frontend.

Caching & Idempotency:
- Snapshots usan `ETag`/`If-None-Match` y TTL definido en `HomeSnapshot.ttl_seconds`.
- `report_widget_interaction` acepta `operation_id` para evitar duplicados desde clientes/worker.

Seguridad:
- `GET /home/landing` puede ser pública o tenant-protected según configuración `tenant_home_public`.
