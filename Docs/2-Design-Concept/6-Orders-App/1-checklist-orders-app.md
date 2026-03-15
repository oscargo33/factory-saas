# Checklist — App Orders

**ID:** OD-1-CHECK

Checklist mínimo para entregar el paquete de diseño y pasar a implementación:

- [ ] `0..8` package completo y revisado.
- [ ] Modelos alineados con `DC-17` (usar IDs lógicos, evitar FK duras).
- [ ] `OrderLine.price_snapshot` y `product_type` definidos y validados en diseños dependientes.
- [ ] `enforce_plan_policy` integrado en `freeze_cart` y en validaciones de checkout.
- [ ] Outbox events definidos para `order.created`, `payment.confirmed`, `provision.requested`.
- [ ] Runbooks de Outbox, retries y poison queue definidos.
- [ ] Esqueletos de prueba contractuales añadidos y referenciados.
