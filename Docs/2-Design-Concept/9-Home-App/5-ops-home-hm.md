# Operaciones & Runbook — Home App

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** HM-5-OPS

Runbook resumido:

1. Cache warming
 - Job: `home.cache.warm(tenant_id)` — genera `HomeSnapshot` por tenant en horario off-peak.
 - Métricas: `home.snapshot.generate_duration_ms`, `home.snapshot_hit_ratio`.

2. Monitoring
 - Latency p95 for `/internal/home/widgets` and `snapshot` endpoints.
 - Alert: `home_snapshot_hit_ratio < 0.6` por 10m.

3. Incident: stale snapshot
 - Detectar `snapshot.generated_at` > TTL → regenerar y emitir `TelemetryEvent(home.snapshot.stale)`.

4. Feature toggles
 - `HOME_RECOMMENDATIONS_ENABLED` toggle para desactivar recomendaciones si `marketing` no responde.

Emergency: toggle `HOME_CACHE_DISABLED=true` para servir render dinámico sin snapshots.
