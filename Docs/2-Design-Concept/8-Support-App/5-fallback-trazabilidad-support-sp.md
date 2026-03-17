# Fallbacks y Trazabilidad — Support App

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

Fallbacks:
- If external enrichment fails (e.g., order service down), persist ticket with `enrichment_status=deferred` and schedule retry via Outbox/Retry queue.

Traceability:
- All user-facing actions should include `operation_id` and `request_id` for cross-service tracing.
- SupportAudit events must contain `tenant_id`, `ticket_id`, `trace` (array of operation_ids) and a `correlation_id` when created from an external workflow.

Observability:
- Metrics: `support.tickets.created_total`, `support.tickets.resolved_total`, `support.tickets.escalated_total`, `support.enrichment_failures_total`.
- Traces: capture ticket lifecycle (create → assign → resolve) with spans on external calls (orders, payments).
