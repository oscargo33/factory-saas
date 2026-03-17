# Plan de Validación y Criterios — Marketing

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** MA-8-VALID

Criterios de aceptación para considerar la App `marketing` como diseño-completo y lista para implementación:

- **Modelos:** `Campaign`, `Coupon`, `Segment` definidos y alineados con DC-17.
- **Contratos:** funciones públicas documentadas en `MA-3-CONTRATOS` y comportamientos de fallback claros.
- **Flows de entrega:** generación de OutboxEvents para envíos y reintentos documentados.
- **Privacidad:** consent y opt-out verificados en las rutas de tracking y envío.
- **Observabilidad:** métricas y Telemetry events definidos y mapeados en la matriz de trazabilidad.

Casos de prueba de aceptación (mínimos):
1. Crear campaña programada y ejecutar envío batch → verificar `OutboxEvent` creado por cada batch.
2. Validar cupón aplicable a `product_id` → `validate_coupon` retorna `allowed` y `apply_coupon` retorna `requires_online_check=false` cuando orders disponible.
3. `track_event` sin consentimiento → rechazado con `consent_required`.

Documentar pasos de prueba en `9-contract-tests-skeleton-marketing.md` (opcional).
