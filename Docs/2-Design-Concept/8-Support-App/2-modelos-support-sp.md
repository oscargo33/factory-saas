# Modelos de Datos — App Support

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** SP-2-MDL

Propósito: definir entidades de tickets, comentarios, SLA y automations para soporte.

Entidades principales (esquema `tenant_{slug}`):

1. `SupportTicket`
 - `id`: UUID PK
 - `tenant_id`: UUID
 - `profile_id`: UUID (referencia lógica a Profile)
 - `subject`: CharField(300)
 - `body`: TextField (sanitized)
 - `status`: `open|in_progress|waiting_on_customer|resolved|closed`
 - `priority`: `low|medium|high|critical`
 - `source`: `web|email|outbox|system`
 - `related_order_id`: UUID nullable
 - `related_payment_id`: UUID nullable
 - `assigned_to_id`: int nullable
 - `created_at`, `updated_at`

2. `SupportComment`
 - `id`: UUID
 - `ticket_id`: UUID
 - `author_profile_id`: UUID
 - `body`: TextField
 - `internal`: Bool
 - `created_at`

3. `SLA` / `EscalationPolicy`
 - Definition of response and resolution times per priority

4. `SupportAutomation` (rules)
 - Automations that create tickets from Outbox events or telemetry thresholds

Reglas:
- Tickets created from Outbox or telemetry must include `operation_id` for idempotency.
- PII in ticket body must be sanitized; store consent flags and redaction markers.
# Modelos de Datos — App Support

**ID:** SP-2-MDL

Propósito: definir `SupportTicket`, `TicketEvent`, `Escalation` y artefactos auxiliares para rastrear incidencias y acciones de soporte.

Entidades principales (esquema `tenant_{slug}`):

1. `SupportTicket`
 - `id`: UUID PK
 - `tenant_id`: UUID
 - `profile_id`: UUID (referencia lógica al Profile)
 - `order_id`: UUID nullable
 - `subject`: CharField(300)
 - `body`: TextField (sanitized)
 - `status`: `open|in_progress|waiting_customer|resolved|closed`
 - `priority`: `low|medium|high|critical`
 - `assigned_to_id`: int nullable
 - `metadata`: JSONB
 - `created_at`, `updated_at`

2. `TicketEvent`
 - `id`: UUID
 - `ticket_id`: UUID
 - `actor_id`: int or system
 - `type`: `comment|status_change|escalation|automation`
 - `payload`: JSONB (redacted for PII)
 - `created_at`

3. `Escalation`
 - `id`: UUID
 - `ticket_id`: UUID
 - `level`: int
 - `escalated_at`, `resolved_at`
 - `notes`

4. `SupportAudit` (public) — events emitted to Telemetry/Outbox for cross-app correlation

Reglas:
- Payloads persisted must be sanitized (PII redaction) before being stored or emitted.
- On creation of high-priority tickets, create `OutboxEvent(event_type=support.ticket.created)` to notify downstream ops and owners.
- Tickets may reference `order_id`, `payment_intent_id` or `operation_id` for traceability but should not hard FK to those models.
