# Checklist — App Payments

**ID:** PY-1-CHECK

Checklist mínimo para entregar el paquete de diseño y pasar a implementación:

- [ ] `0..8` package completo y revisado.
- [ ] Modelos alineados con `DC-17` y soportan `PriceSnapshot` referencias.
- [ ] Handlers idempotentes para webhooks y outbox persistente en transacciones.
- [ ] Dunning / retry policy documentada y runbooks de recuperación.
- [ ] Esqueletos de pruebas/contratos añadidos y fixtures disponibles.
- [ ] Telemetry con `plan_id` y `matrix_version` incluida en eventos de pago.
