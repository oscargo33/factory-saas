# DoD — Sign-off Checklist (Concept Design)

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** DC-20-DOD

Propósito: lista de verificación mínima que debe cumplirse antes de cerrar la etapa de Concept Design y abrir implementación.

Checklist (mínimo exigible):

- [x] **Contratos (DC-16):** cada app tiene su documento de contratos público (`3-service-selector-contratos-*.md`) y está referenciado desde DC-16.
- [x] **Diccionario (DC-17):** todas las entidades usadas en contratos están definidas en DC-17 (IDs, campos críticos, PII marcado).
- [x] **PlanMatrix (DC-19):** existe proceso de publicación/versionado y `PlanMatrixVersion` referenciado en flujos de aprovisionamiento.
- [x] **Outbox / Idempotencia:** OutboxEvent payloads incluyen `operation_id` y consumidores deduplican por `operation_id`; índices/constraints recomendados aplicados o planificados.
- [x] **PriceSnapshot:** Orders/Payments persisten `price_snapshot` en `OrderLine` y lo usan en Outbox/Telemetry para conciliación.
- [x] **Traceability:** trazabilidad normalizada por app con cobertura explícita a DC-12/DC-13/DC-16/DC-17 en todos los paquetes.
- [x] **Ops Runbooks:** Outbox worker, poison handling, SLA/escalation y Telemetry push/pull runbooks están escritos y referenciados.
- [x] **Security & PII:** matriz de clasificación (DC-18) aplicada y PII redaction rules definidas para Outbox/Telemetry/Support.
- [x] **Contract-tests skeleton:** fixtures y skeletons presentes en dominios clave, incluyendo `support` con convención `9-contract-tests-skeleton-support-sp.md`.
- [x] **Acceptance Criteria:** todos los `9-contract-tests-skeleton-*.md` existentes incluyen sección homogénea de criterios reproducibles.

---

## Resultado de Sign-off (ejecución PB-017)

**Fecha:** 2026-03-16
**Estado de gate Fase 2:** **GO (hallazgos H-1/H-2/H-3 cerrados)**

### Evidencia por ítem (archivo + línea)

1. **Contratos (DC-16)**
	- Registro por app en `Docs/2-Design-Concept/0-Factory-Saas/16-contratos-inter-app-fs.md:22`.
	- Contratos por app presentes desde línea 1 en:
	  - `Docs/2-Design-Concept/1-Theme-App/3-service-selector-contratos-theme-th.md:1`
	  - `Docs/2-Design-Concept/2-Api-Telemetry-App/3-service-selector-contratos-telemetry-at.md:1`
	  - `Docs/2-Design-Concept/3-Profile-App/3-service-selector-contratos-profile-pr.md:1`
	  - `Docs/2-Design-Concept/4-Product-Orchestrator-App/3-service-selector-contratos-product-orchestrator-po.md:1`
	  - `Docs/2-Design-Concept/5-Marketing-App/3-service-selector-contratos-marketing-md.md:1`
	  - `Docs/2-Design-Concept/6-Orders-App/3-service-selector-contratos-orders-od.md:1`
	  - `Docs/2-Design-Concept/7-Payment-App/3-service-selector-contratos-payments-py.md:1`
	  - `Docs/2-Design-Concept/8-Support-App/3-service-selector-contratos-support-sp.md:1`
	  - `Docs/2-Design-Concept/9-Home-App/3-service-selector-contratos-home-hm.md:1`

2. **Diccionario (DC-17)**
	- `PriceSnapshot` en `Docs/2-Design-Concept/0-Factory-Saas/17-diccionario-datos-logico-fs.md:195`.
	- `OutboxEvent` en `Docs/2-Design-Concept/0-Factory-Saas/17-diccionario-datos-logico-fs.md:210`.
	- Payload sin PII en `Docs/2-Design-Concept/0-Factory-Saas/17-diccionario-datos-logico-fs.md:298`.

3. **PlanMatrix (DC-19)**
	- `PlanMatrixVersion` definido en `Docs/2-Design-Concept/0-Factory-Saas/19-plan-matrix-fs.md:15`.
	- Publicación/versionado en `Docs/2-Design-Concept/0-Factory-Saas/19-plan-matrix-fs.md:21`.
	- Trazabilidad por `matrix_version` en `Docs/2-Design-Concept/0-Factory-Saas/19-plan-matrix-fs.md:31`.

4. **Outbox / Idempotencia**
	- Regla estándar en `Docs/2-Design-Concept/0-Factory-Saas/16-contratos-inter-app-fs.md:195`.
	- Recomendaciones/constraints en `Docs/2-Design-Concept/0-Factory-Saas/17-diccionario-datos-logico-fs.md:225` y `Docs/2-Design-Concept/0-Factory-Saas/17-diccionario-datos-logico-fs.md:227`.
	- Evidencia de tests en `tests/contracts/test_outbox_and_telemetry.py:4` y `tests/contracts/test_payments_idempotency_fixture.py:4`.

5. **PriceSnapshot**
	- Modelo lógico en `Docs/2-Design-Concept/0-Factory-Saas/17-diccionario-datos-logico-fs.md:195`.
	- Verificación de contrato en `tests/contracts/test_order_price_snapshot.py:1` y `tests/contracts/test_order_price_snapshot.py:3`.

6. **Traceability**
	- Matrices existentes: `Docs/2-Design-Concept/1-Theme-App/6-matriz-trazabilidad-theme-th.md:4`, `Docs/2-Design-Concept/2-Api-Telemetry-App/6-matriz-trazabilidad-telemetry-at.md:4`, `Docs/2-Design-Concept/3-Profile-App/6-matriz-trazabilidad-profile-pr.md:4`, `Docs/2-Design-Concept/4-Product-Orchestrator-App/6-matriz-trazabilidad-product-orchestrator-po.md:4`.
	- Home y Support tienen trazabilidad con nomenclatura distinta: `Docs/2-Design-Concept/9-Home-App/6-trazabilidad-home-hm.md:1`, `Docs/2-Design-Concept/8-Support-App/6-trazabilidad-support-sp.md:1`.
	- Cobertura explícita DC-12/DC-13/DC-16/DC-17 agregada en las 9 matrices por app.

7. **Ops Runbooks**
	- Push/Pull telemetría en `Docs/2-Design-Concept/0-Factory-Saas/15-protocolo-comunicacion-central-fs.md:28` y `Docs/2-Design-Concept/0-Factory-Saas/15-protocolo-comunicacion-central-fs.md:52`.
	- Outbox worker + poison handling en `Docs/2-Design-Concept/2-Api-Telemetry-App/5-push-pull-resiliencia-telemetry-at.md:79` y `Docs/2-Design-Concept/2-Api-Telemetry-App/5-push-pull-resiliencia-telemetry-at.md:91`.
	- SLA/escalation soporte en `Docs/2-Design-Concept/8-Support-App/6-runbook-support-sp.md:10`.

8. **Security & PII**
	- Clasificación PII en `Docs/2-Design-Concept/0-Factory-Saas/18-matriz-seguridad-compliance-fs.md:25`.
	- Regla no-PII en telemetría en `Docs/2-Design-Concept/0-Factory-Saas/18-matriz-seguridad-compliance-fs.md:52`.
	- Inventario/retención PII en `Docs/2-Design-Concept/0-Factory-Saas/18-matriz-seguridad-compliance-fs.md:127`.

9. **Contract-tests skeleton**
	- Fixtures disponibles en `Docs/2-Design-Concept/0-Factory-Saas/contracts-examples/`.
	- Skeletons presentes en: `Docs/2-Design-Concept/2-Api-Telemetry-App/9-contract-tests-skeleton-telemetry-at.md:1`, `Docs/2-Design-Concept/4-Product-Orchestrator-App/9-contract-tests-skeleton-product-orchestrator-po.md:1`, `Docs/2-Design-Concept/6-Orders-App/9-contract-tests-skeleton-orders-od.md:1`, `Docs/2-Design-Concept/7-Payment-App/9-contract-tests-skeleton-payments-py.md:1`.
	- Cobertura completada para `support` en `Docs/2-Design-Concept/8-Support-App/9-contract-tests-skeleton-support-sp.md:1`.
	- Cobertura completada para `profile` y `home` en `Docs/2-Design-Concept/3-Profile-App/9-contract-tests-skeleton-profile-pr.md:1` y `Docs/2-Design-Concept/9-Home-App/9-contract-tests-skeleton-home-hm.md:1`.

10. **Acceptance Criteria en skeletons**
	- Casos documentados en `Docs/2-Design-Concept/6-Orders-App/9-contract-tests-skeleton-orders-od.md:11`, `Docs/2-Design-Concept/7-Payment-App/9-contract-tests-skeleton-payments-py.md:10`, `Docs/2-Design-Concept/4-Product-Orchestrator-App/9-contract-tests-skeleton-product-orchestrator-po.md:12`.
	- Sección homogénea `Acceptance criteria reproducibles` presente en los 7 skeletons actuales.

### Hallazgos bloqueantes para abrir Fase 2 (estado)

- **H-1 (Traceability):** cerrado.
- **H-2 (Support contract skeleton):** cerrado.
- **H-3 (Cobertura de acceptance criteria):** cerrado.

### Decisión de gate

- **GO** para apertura de Fase 2 desde la perspectiva documental de DC-20.
- PB-017 puede pasar a `Done` una vez reflejado el estado en backlog/sprint.

Proceso de sign-off:

1. El arquitecto revisa esta lista y marca cada ítem con evidencia (archivo(s) y línea(s) donde se cumple).
2. Stakeholders (Payments, Orchestrator, Orders, Telemetry) validan y aprueban por mail/issue.
3. Al aprobar: cerrar DoD y abrir backlog de implementación con tickets por app.
