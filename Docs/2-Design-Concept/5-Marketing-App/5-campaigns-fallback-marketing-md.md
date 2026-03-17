# Operación y Fallbacks — Campañas y Envíos

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** MA-5-OPS

Propósito: definir comportamientos cuando componentes externos no están disponibles y runbooks operativos para campañas.

Fallbacks clave:
- Si `email_provider` no está configurado: encolar envíos en `OutboxEvent` (tipo `marketing.email.send`) y exponer `campaign.status = queued`.
- Si `telemetry` no está instalado: guardar `MarketingEvent` localmente y marcar `telemetry_forwarded=false` para reintentos manuales.
- Si `orders`/`payments` no están disponibles al aplicar cupones, la validación se realiza con reglas estáticas y la respuesta incluye `requires_online_check: true`.

Runbook básico de entrega de campaña:
1. Crear campaña (`status=scheduled`).
2. Evaluar `audience_definition` y generar `recipients` (batch).
3. Para cada batch: generar `OutboxEvent` con `event_type=marketing.send` y `payload` minimal (recipient, template_ref, operation_id).
4. Worker `marketing.sender` procesa outbox, marca `sent` y emite `TelemetryEvent`.
5. En errores persistentes, mover a `poison_queue` y abrir ticket en `support`.

Operaciones de emergencia:
- Toggle `MARKETING_SEND_ENABLED=False` para pausar envíos.
