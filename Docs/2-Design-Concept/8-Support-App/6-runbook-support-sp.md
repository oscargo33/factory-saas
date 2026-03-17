# Runbook — Support App (operaciones)

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

1. Incident Triage
 - On alert `support.tickets.critical` route to on-call via PagerDuty.
 - Enrich ticket with `order_id` / `payment_intent_id` if present.

2. Outbox Poison Handling
 - If Outbox event fails after N retries, move to `outbox_poison` table and create ticket with `priority=high`.

3. Dunning & Escalation
 - For unresolved tickets older than SLA thresholds escalate level and notify managers.

4. Data Retention & PII
 - Ticket payloads containing PII must be redacted in `SupportAudit` and removed after retention window.
