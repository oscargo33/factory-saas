# Profile — Contract Tests Skeleton

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

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

Acceptance criteria reproducibles:
- [ ] Cada caso define input fixture y output esperado verificable.
- [ ] El contexto de telemetria incluye `user_id`, `profile_id` y `tenant_slug`.
- [ ] Los selectores publicos conservan contrato backward-compatible de salida.
