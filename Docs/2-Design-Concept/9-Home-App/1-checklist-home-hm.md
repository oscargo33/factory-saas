# Checklist — Home App

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** HM-1-CHK

Checklist mínima para Diseño Conceptual (0..8):

- [ ] Definir contratos públicos en DC-16 (selectors/services) y registrar owner.
- [ ] Modelos lógicos registrados en DC-17 (IDs, campos, PII si aplica).
- [ ] Flujos de datos: landing → dashboard widgets → product links → telemetry.
- [ ] Integración soft-deps: `product_orchestrator`, `marketing`, `telemetry`, `profile`.
- [ ] Runbooks básicos: cache warming, feature toggles, error fallbacks.
- [ ] NFRs iniciales: latency p95, availability SLO, throughput estimado.
- [ ] Contract-tests skeleton para widgets críticos y recomendaciones de fixtures.
- [ ] Trazabilidad a DC-12/DC-13/DC-16/DC-17/DC-19 (PlanMatrix) según corresponda.
