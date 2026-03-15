# NFR, Seguridad y Operación — Marketing

**ID:** MA-7-NFR

No funcionales y controles operativos mínimos:

- **Privacidad / Consent:** implementar `ConsentMiddleware` y almacenar `consent_status` por `profile_id`. No enviar comunicaciones sin consentimiento.
- **Rate limits:** `POST /track` y `POST /webhooks` limitados por `tenant_id`.
- **Datos PII:** templates no deben persistir PII en el repositorio; los `payloads` en Outbox deben sanearse.
- **Retención:** eventos de marketing retener por defecto 90 días (configurable por tenant), soportar `right-to-be-forgotten`.
- **Seguridad de webhooks:** verificar firmas HMAC y rotar claves periódicamente.
- **Observabilidad:** métricas mínimas: `marketing_campaigns_sent_total`, `marketing_campaigns_failed_total`, `marketing_outbox_pending_count`, `marketing_delivery_bounce_rate`.
- **Alta disponibilidad:** workers idempotentes y retry/backoff para proveedores de email/push.
