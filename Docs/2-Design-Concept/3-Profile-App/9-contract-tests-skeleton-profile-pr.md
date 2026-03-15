# Profile — Contract Tests Skeleton

Propósito: validar selectors públicos y payloads usados por Telemetry y Outbox.

Archivos de ejemplo referenciados:
- `../../0-Factory-Saas/contracts-examples/profile_example.json` (fixture)

Casos mínimos sugeridos:
1. `get_display_name` selector
   - Input: `profile_example.json` con `profile_id, user_id, display_name`.
   - Expect: llamada retorna `{profile_id, display_name}` y `profile_id` es UUID.

2. `get_active_context` telemetry identity
   - Input: request simulado con user y tenant.
   - Expect: `telemetry_identity` contenga `user_id`, `profile_id`, `tenant_slug`.

Notas: estos skeletons se pueden implementar en pytest con fixtures que carguen `profile_example.json` en la DB tenant.
