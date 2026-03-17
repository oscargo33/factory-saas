# Service / Selector & Contratos — App Support

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

Propósito: definir las interfaces públicas que el Support App expone y los contratos que otros servicios pueden llamar.

API públicas (contratos):

1. `create_support_ticket(profile_id, subject, body, metadata) -> SupportTicketDTO`
 - Crea un ticket y encola `OutboxEvent(support.ticket.created)`.

2. `add_ticket_comment(ticket_id, actor_id, comment) -> TicketEventDTO`

3. `change_ticket_status(ticket_id, status, actor_id) -> SupportTicketDTO`

4. `list_tickets(tenant_id, filters) -> [SupportTicketDTO]` — paginado

5. `get_ticket(ticket_id) -> SupportTicketDTO`

Idempotency & Safety:
- `create_support_ticket` acepta `operation_id` header to ensure idempotent creation from external systems.
- Ticket mutations validate tenant isolation: operations require tenant context and fail if cross-tenant references detected.

Outbox & Telemetry:
- Emit `support.ticket.created`, `support.ticket.updated`, `support.ticket.escalated`, `support.ticket.resolved` as OutboxEvents with minimal PII.

Errors:
- Use typed errors: `TenantNotFound`, `TicketNotFound`, `OperationConflict`, `InvalidStatusTransition`.
