# Contract-tests Skeleton — Home App

**ID:** HM-9-TESTS

Propósito: casos mínimos para validar contratos expuestos por `Home`.

1. `get_home_widgets`
 - Fixture: `Docs/2-Design-Concept/0-Factory-Saas/contracts-examples/home_widgets_example.json`
 - Checks: schema fields `widget_key`, `title`, `settings` present; `tenant_id` in metadata.

2. `get_home_snapshot`
 - Fixture: `Docs/2-Design-Concept/0-Factory-Saas/contracts-examples/home_snapshot_example.json`
 - Checks: `snapshot_key`, `generated_at`, `payload` minimal and no PII.

3. `report_widget_interaction` idempotency
 - Simulate duplicate `operation_id` → single telemetry event recorded.

Nota: implementar tests en `tests/contracts/` cuando entre en fase de verificación; por ahora son esqueletos para DoD.
