# Validación — App Support

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** SP-8-VAL

Checklist de validación para la etapa de Diseño (DoR/DoD):

- Contract-tests: fixtures for `OutboxEvent` -> ticket creation and idempotency
- Security: token-scope verification and tenant validation
- Ops: runbook reviewed and alerts defined
- Data: PII redaction and retention policy confirmed
- Traceability: events mapping to telemetry and cross-app dependencies documented

Tests esquelétos:
- `tests/contracts/test_support_outbox.py` (fixture: `outbox/support_ticket_created.json`)
# Validación y Tests — Support App

Test skeletons:

- `tests/contracts/test_support_contracts.py` — examples:
  - create ticket idempotency with `operation_id` header
  - outbox emission on `support.ticket.created`
  - tenant isolation checks

JSON fixtures to add (suggested): `support_ticket_example.json`, `support_event_example.json`.
