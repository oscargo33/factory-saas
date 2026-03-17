# Support — Contract Tests Skeleton

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

Proposito: casos minimos para validar contratos publicos de soporte, runbook de escalacion y correlacion con Orders/Payments.

Archivos referenciados (fixtures):
- `../../0-Factory-Saas/contracts-examples/outbox_event_example.json`
- `../../0-Factory-Saas/contracts-examples/order_line_example.json`
- `../../0-Factory-Saas/contracts-examples/price_snapshot_example.json`

Casos minimos sugeridos:
1. `create_system_ticket` desde fallo de pago
   - Input: evento `payment.failed` con `tenant_id`, `order_id`, `operation_id`.
   - Expect: ticket creado con prioridad y metadata de correlacion.

2. Escalacion por SLA
   - Input: ticket sin respuesta sobre umbral SLA.
   - Expect: cambio de estado/escalacion y notificacion a owner/staff.

3. Integracion con Outbox poison
   - Input: evento en estado fallido recurrente.
   - Expect: ticket de soporte creado automaticamente con evidencia minima.

4. PII redaction en auditoria
   - Input: mensaje con datos sensibles en cuerpo de ticket.
   - Expect: almacenamiento redacted en auditoria y payload para telemetria sin PII.

Acceptance criteria reproducibles:
- [ ] Cada caso define input fixture y output esperado verificable.
- [ ] Cada caso incluye campos de correlacion (`tenant_id`, `operation_id`).
- [ ] Ningun caso valida datos de usuario en texto plano dentro de telemetria.
