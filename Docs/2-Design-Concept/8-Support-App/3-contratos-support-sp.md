# Contratos — App Support

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** SP-3-CT

Objetivo: definir los contratos y DTOs que Support expone y consume.

Consumo:
- `OutboxEvent` (consume): para crear tickets desde eventos de dominio.
- `TelemetryEvent` (consume): para crear alerts/automations.
- `OrderSnapshot` / `PriceSnapshot` (consume): para investigar pagos/ordenes.

Exposición (API interna):
- `CreateSupportTicketDTO`:
  - `operation_id`: UUID (idempotency)
  - `profile_id`: UUID
  - `subject`: str
  - `body`: str
  - `source`: enum
  - `related_order_id`?: UUID
  - `related_payment_id`?: UUID

- `SupportTicketDTO` (read): includes `id`, `status`, `priority`, `assigned_to`, `created_at`

Seguridad y Tenancy:
- Todos los DTOs llevan `tenant_id` o se validan en middleware con el token.
- `operation_id` obligatorio para eventos entrantes (Outbox/Telemetry) para prevenir duplicados.
