# Endpoints — App Support

**ID:** SP-4-EP

API interna (service-to-service):

- `POST /internal/support/tickets` — Create ticket (expects `CreateSupportTicketDTO`)
  - Auth: service-token + tenant header
  - Validations: `operation_id` required for events

- `GET /internal/support/tickets/{ticket_id}` — Read ticket

- `POST /internal/support/tickets/{ticket_id}/comments` — Add internal/external comment

Webhook / Integrations:
- `POST /webhook/support/outbox` — endpoint for Outbox worker to deliver events (signed)

Idempotency:
- All create endpoints accept `operation_id` and support idempotency keys stored in `tenant_operation_ids` table.
# Endpoints & Integration — Support App

Endpoints (HTTP / gRPC):

1. POST `/v1/support/tickets/` — create ticket
 - Body: `profile_id`, `subject`, `body`, `metadata`, optional `operation_id`
 - Response: `201 Created` with `SupportTicketDTO`

2. POST `/v1/support/tickets/{id}/comments/` — add comment

3. PATCH `/v1/support/tickets/{id}/` — update status/assignee

4. GET `/v1/support/tickets/` — list tickets (filters: status, priority, profile_id, order_id)

Integration notes:
- Webhooks: support app subscribes to `order.updated`, `payment.confirmed` to enrich tickets with order/payment context.
- For long-running automations (auto-triage), use `operation_id` and produce OutboxEvent for follow-up actions.
