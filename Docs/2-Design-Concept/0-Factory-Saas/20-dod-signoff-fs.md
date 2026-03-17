# DoD — Sign-off Checklist (Concept Design)

**ID:** DC-20-DOD

Propósito: lista de verificación mínima que debe cumplirse antes de cerrar la etapa de Concept Design y abrir implementación.

Checklist (mínimo exigible):

- [ ] **Contratos (DC-16):** cada app tiene su documento de contratos público (`3-service-selector-contratos-*.md`) y está referenciado desde DC-16.
- [ ] **Diccionario (DC-17):** todas las entidades usadas en contratos están definidas en DC-17 (IDs, campos críticos, PII marcado).
- [ ] **PlanMatrix (DC-19):** existe proceso de publicación/versionado y `PlanMatrixVersion` referenciado en flujos de aprovisionamiento.
- [ ] **Outbox / Idempotencia:** OutboxEvent payloads incluyen `operation_id` y consumidores deduplican por `operation_id`; índices/constraints recomendados aplicados o planificados.
- [ ] **PriceSnapshot:** Orders/Payments persisten `price_snapshot` en `OrderLine` y lo usan en Outbox/Telemetry para conciliación.
- [ ] **Traceability:** cada app checklist declara trazabilidad a DC-12/DC-13/DC-16/DC-17 (o explica por qué no aplica).
- [ ] **Ops Runbooks:** Outbox worker, poison handling, SLA/escalation y Telemetry push/pull runbooks están escritos y referenciados.
- [ ] **Security & PII:** matriz de clasificación (DC-18) aplicada y PII redaction rules definidas para Outbox/Telemetry/Support.
- [ ] **Contract-tests skeleton:** fixtures en `Docs/.../contracts-examples/` y tests esqueléticos en `tests/contracts/` presentes para cada dominio crítico (payments, orders, orchestrator, support).
- [ ] **Acceptance Criteria:** Para cada contrato/service clave se listan casos de aceptación reproducibles (en los `9-contract-tests-skeleton-*.md`).

Proceso de sign-off:

1. El arquitecto revisa esta lista y marca cada ítem con evidencia (archivo(s) y línea(s) donde se cumple).
2. Stakeholders (Payments, Orchestrator, Orders, Telemetry) validan y aprueban por mail/issue.
3. Al aprobar: cerrar DoD y abrir backlog de implementación con tickets por app.
