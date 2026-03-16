# Trazabilidad — App Support

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
