# Documento: Sistema de Notificaciones Transaccionales

**Versión del documento:** 1.0
**Última actualización:** 2026-03-16

**ID:** DC-24-FS
**Ubicacion:** `./Docs/2-Design-Concept/0-Factory-Saas/24-sistema-notificaciones-fs.md`
**Anchor Docs:** `DC-11-FS` (Redis/Celery), `DC-18-FS` (Seguridad/GDPR), `DC-16-FS` (Contratos inter-app)
**Backlog:** PB-019

---

## 1. Proposito

Define la arquitectura completa del sistema de notificaciones transaccionales de Factory-SaaS: como se envian emails de sistema, que eventos los disparan en cada app, como se gestionan reintentos y rebotes, y como cumplir con GDPR y anti-spam.

Sin este sistema, los flujos criticos de onboarding, pagos y soporte son inutilizables: el usuario no recibira confirmacion de registro, recibos de pago, ni actualizaciones de tickets.

---

## 2. Proveedor y Configuracion

### 2.1. Proveedor recomendado: Amazon SES (principal) + SendGrid (fallback)

| Criterio | Amazon SES | SendGrid |
|---|---|---|
| Costo | Muy bajo (USD 0.10/1000 emails) | Medio (free tier 100/dia) |
| Deliverability | Alta si DKIM/SPF configurados | Alta |
| Integracion Django | `django-ses` o `anymail` | `anymail` |
| Uso en Factory | Produccion principal | Fallback o staging |

**Libreria unica de abstraccion:** `django-anymail` — permite cambiar de proveedor sin tocar el codigo de negocio. Se configura via variable de entorno `EMAIL_BACKEND`.

### 2.2. Variables de entorno requeridas

```bash
EMAIL_BACKEND=anymail.backends.amazon_ses.EmailBackend
ANYMAIL_AMAZON_SES_CLIENT_PARAMS__region_name=us-east-1
AWS_ACCESS_KEY_ID=<secret>
AWS_SECRET_ACCESS_KEY=<secret>
DEFAULT_FROM_EMAIL=noreply@factory-saas.com
SERVER_EMAIL=alerts@factory-saas.com

# Fallback para desarrollo
# EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

---

## 3. Arquitectura: Envio Asincrono por Celery

Ningun email se envia de forma sincrona en una vista. El flujo obligatorio es:

```
Vista / Service
    │
    ▼
notification_service.queue_email(event_type, recipient, context)
    │
    ▼
Celery Task: send_transactional_email.delay(...)
    │── Primer intento
    │── Reintento 1 (30s)
    │── Reintento 2 (5min)
    │── Reintento 3 (30min)
    │── Si falla: marca NotificationLog como 'failed', alerta a staff
    ▼
SES / SendGrid API
    │
    ▼
NotificationLog (registro de envio)
```

### Modelo `NotificationLog`

**Owner App:** `apps.telemetry` (para mantener App Profiles sin logica de envio)
**Schema:** `public`

| Campo | Tipo | Descripcion |
|---|---|---|
| `id` | UUID PK | Identificador unico |
| `event_type` | CharField | Tipo de notificacion (ver Seccion 4) |
| `recipient_email` | CharField | Email destinatario (hasheado en logs de telemetria) |
| `tenant_id` | UUID FK nullable | Tenant asociado (null si es sistema global) |
| `status` | CharField | `queued`, `sent`, `failed`, `bounced` |
| `attempts` | IntegerField | Numero de intentos realizados |
| `sent_at` | DateTimeField nullable | Timestamp de envio exitoso |
| `error_message` | TextField nullable | Motivo de fallo si aplica |
| `operation_id` | UUID unique | Para idempotencia (evitar envio duplicado) |

---

## 4. Catalogo de Notificaciones por App

### 4.1. App Profiles

| Event Type | Disparador | Destinatario | Asunto |
|---|---|---|---|
| `user.registered` | Registro exitoso | Usuario nuevo | "Bienvenido a Factory-SaaS — confirma tu email" |
| `user.email_confirmed` | Confirmacion de email | Usuario | "Email confirmado — ya puedes iniciar sesion" |
| `user.password_reset_requested` | Solicitud de reset | Usuario | "Restablece tu contrasena (expira en 1 hora)" |
| `user.password_changed` | Password actualizado | Usuario | "Tu contrasena ha sido cambiada" |
| `tenant.member_invited` | Admin invita miembro | Invitado | "Te han invitado a unirte a [Tenant Name]" |
| `tenant.invitation_accepted` | Invitado acepta | Admin del tenant | "[Nombre] se unio a tu organizacion" |
| `tenant.member_role_changed` | Cambio de rol | Miembro afectado | "Tu rol en [Tenant] ha cambiado a [Nuevo Rol]" |

### 4.2. App Payments

| Event Type | Disparador | Destinatario | Asunto |
|---|---|---|---|
| `payment.succeeded` | Pago exitoso | Owner del tenant | "Pago recibido — recibo #[ID]" |
| `payment.failed` | Pago fallido | Owner del tenant | "Hubo un problema con tu pago" |
| `payment.receipt_generated` | Recibo creado | Owner del tenant | "Tu recibo de [Producto] esta listo" |
| `subscription.created` | Suscripcion nueva | Owner del tenant | "Suscripcion activada: [Plan]" |
| `subscription.renewing_soon` | 7 dias antes de renovacion | Owner | "Tu suscripcion se renueva el [Fecha]" |
| `subscription.cancelled` | Cancelacion | Owner del tenant | "Suscripcion cancelada — acceso hasta [Fecha]" |
| `subscription.payment_failed_dunning` | Cobro fallido en dunning | Owner | "No pudimos procesar tu renovacion (intento [N] de 3)" |

### 4.3. App Support

| Event Type | Disparador | Destinatario | Asunto |
|---|---|---|---|
| `ticket.created` | Ticket nuevo | Creador del ticket | "Ticket #[ID] recibido — te responderemos pronto" |
| `ticket.reply_received` | Agente responde | Creador del ticket | "Nueva respuesta en tu ticket #[ID]" |
| `ticket.status_changed` | Cambio de estado | Creador del ticket | "Tu ticket #[ID] esta [Estado]" |
| `ticket.closed` | Ticket cerrado | Creador del ticket | "Tu ticket #[ID] fue cerrado — cuéntanos tu experiencia" |
| `ticket.escalated` | Escalacion | Staff asignado | "Ticket #[ID] escalado — requiere tu atencion" |

### 4.4. App Orders

| Event Type | Disparador | Destinatario | Asunto |
|---|---|---|---|
| `order.confirmed` | Orden confirmada | Comprador | "Orden #[ID] confirmada" |
| `order.cancelled` | Orden cancelada | Comprador | "Orden #[ID] cancelada" |

### 4.5. Sistema (Alertas a staff)

| Event Type | Disparador | Destinatario | Asunto |
|---|---|---|---|
| `system.migration_failed` | migrate_all_tenants con error | Staff interno | "ALERTA: Migracion fallida en tenant [slug]" |
| `system.payment_review_required` | Pago en revision manual | Staff interno | "Pago [ID] requiere revision manual" |
| `system.celery_dead` | Worker Celery sin respuesta | Staff interno | "ALERTA: Celery worker sin respuesta" |

---

## 5. Contratos del Servicio de Notificaciones

**Owner App:** `apps.telemetry` expone el servicio; las demas apps lo consumen sin importar logica de envio.

### 5.1. Interfaz publica (contrato)

```python
# apps/telemetry/services.py

def queue_notification(
    event_type: str,
    recipient_email: str,
    context: dict,
    tenant_id: UUID | None = None,
    operation_id: UUID | None = None,  # para idempotencia
) -> NotificationLog:
    """
    Encola un email transaccional para envio asincrono.
    Si operation_id ya existe en NotificationLog -> no encola (idempotencia).
    Retorna el NotificationLog creado o existente.
    """
    ...
```

### 5.2. Patron de uso en otras apps

```python
# Ejemplo en apps/payments/services.py
from django.apps import apps

def confirm_payment(payment_intent_id: UUID) -> PaymentIntent:
    intent = PaymentIntent.objects.get(id=payment_intent_id)
    intent.status = 'succeeded'
    intent.save()

    # Notificacion: soft-dependency
    if apps.is_installed('apps.telemetry'):
        from apps.telemetry.services import queue_notification
        queue_notification(
            event_type='payment.succeeded',
            recipient_email=intent.owner_email,
            context={'receipt_id': str(intent.receipt_id), 'amount': str(intent.amount)},
            tenant_id=intent.tenant_id,
            operation_id=intent.id,  # idempotencia: mismo intent = mismo email
        )

    return intent
```

---

## 6. Configuracion DKIM / SPF / DMARC

Para garantizar deliverability en produccion:

| Registro DNS | Valor | Proposito |
|---|---|---|
| SPF | `v=spf1 include:amazonses.com ~all` | Autoriza SES como remitente |
| DKIM | Generado por SES (3 registros CNAME) | Firma criptografica de emails |
| DMARC | `v=DMARC1; p=quarantine; rua=mailto:dmarc@factory-saas.com` | Politica de rechazo de spoofing |

> Estos registros deben configurarse en el DNS del dominio ANTES del primer envio en produccion. SES rechaza emails si DKIM no esta configurado.

---

## 7. Manejo de Rebotes (Bounce Handling)

SES envia notificaciones de bounce y complaint por SNS (Simple Notification Service):

```
SES → SNS Topic → POST /api/internal/ses-webhook/

Handler en apps/telemetry/views.py:
  - Bounce permanente (tipo=Permanent): desactiva email en User, registra en NotificationLog
  - Bounce temporal (tipo=Transient): registra advertencia, reintenta en siguiente envio
  - Complaint (spam): desactiva email de marketing para ese usuario
```

---

## 8. Plantillas de Email

- Todas las plantillas usan Django template engine: `templates/notifications/<event_type>.html` y `.txt`.
- Formato multipart (HTML + texto plano) obligatorio.
- Tokens de CSS inline (Tailwind no aplica en email; usar estilos inline).
- Contenido minimo: logo del tenant (si existe) o logo de Factory, mensaje, CTA, footer con enlace de desuscripcion (GDPR).
- El footer incluye siempre: "Para dejar de recibir estos emails, [haz clic aqui]".

---

## 9. GDPR y Compliance

| Requisito | Implementacion |
|---|---|
| Consentimiento | Emails transaccionales no requieren opt-in (son consecuencia directa de la accion del usuario). Emails de marketing si requieren opt-in explicito. |
| Derecho al olvido | `delete_user_notifications(user_id)` en `notification_service` anonimiza `recipient_email` en `NotificationLog`. |
| Retencion de logs | `NotificationLog` se retiene 90 dias. Despues se anonimiza (email → hash). |
| Opt-out | Enlace de desuscripcion en todo email. Respetado en < 10 dias (GDPR exige < 10 dias activos). |

---

## 10. DoD de este Documento

- [ ] Catalogo completo de event types por app definido.
- [ ] Contrato de `queue_notification` especificado con idempotencia.
- [ ] Patron de uso en apps consumidoras documentado (soft-dependency).
- [ ] Configuracion DKIM/SPF/DMARC documentada.
- [ ] Bounce handling especificado.
- [ ] GDPR: retencion, opt-out y right-to-erasure cubiertos.
- [ ] Indexado en `0-index.md` de Factory-SaaS global.
