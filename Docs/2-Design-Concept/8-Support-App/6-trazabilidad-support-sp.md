# Trazabilidad — App Support

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** SP-6-TRZ

Traceability matrix (consumers / producers):

- Consumes:
  - `OutboxEvent` (produced by Orders/Payments/Product)
  - `TelemetryEvent` (produced globally)
  - `PriceSnapshot` (produced by Orders)

- Produces:
  - `SupportTicketCreated` telemetry event
  - `SupportTicketUpdated` telemetry event

Versioning:
- Contract versions follow the global `DC-16` scheme; Support increments consumer version when a non-backward-compatible change is required.

## Cobertura obligatoria DC-12/DC-13/DC-16/DC-17

- DC-12 (patron service layer): aplica en servicios de apertura/escalacion/auditoria de tickets.
- DC-13 (router dinamico y contexto tenant): aplica en creacion y seguimiento de tickets por tenant.
- DC-16 (contratos inter-app): cubierto por consumo de outbox/telemetria y publicacion de `SupportTicketCreated/Updated`.
- DC-17 (diccionario de datos logico): cubierto por entidades de ticket, auditoria y campos de correlacion (`tenant_id`, `operation_id`).
