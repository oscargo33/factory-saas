# Operaciones & Runbook — App Support

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** SP-5-OPS

Runbook principales:

1. Outbox Worker handling
 - Monitor: `outbox.delivery.latency`, `outbox.delivery.failures`
 - Retry policy: exponential backoff with jitter, 5 attempts then move to poison queue
 - Alert: on poison queue items > 10

2. SLA monitoring
 - Metrics: `support.ticket.response_time`, `support.ticket.resolution_time`
 - Escalation: auto-escalate tickets breaching SLA via automation rules

3. Incident Playbook
 - Triage steps, rollback operations, and communications templates.

Security:
- Service tokens rotated quarterly; access scoped by `support:write`, `support:read`.
