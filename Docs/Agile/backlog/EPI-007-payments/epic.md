# EPI-007 — Payments: El Cajero Seguro del SaaS

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** EPI-007
**Tipo:** Commercial Epic — Capa 3, conversión financiera y suscripciones
**Prioridad:** 3 — Núcleo del modelo de revenue del SaaS
**Sprint objetivo:** Sprint-1
**Dependencias:** EPI-000 Done, EPI-CORE Done, EPI-006 (Orders para obtener monto e ID de orden)
**Blueprints fuente:**
- `Docs/1-Core_Concept/7-payment-app-cc.md`
- `Docs/2-Design-Concept/7-Payment-App/` (12 documentos)

---

## § 1 — EL ALMA: Visión y Razón de Existir

### ¿Qué Problema Resuelve?

El dinero es el punto más sensible del SaaS. Un webhook de pago duplicado puede activar dos suscripciones. Un fallo en la pasarela puede dejar al cliente en un limbo donde pagó pero no recibió el servicio. Sin PCI-DSS, almacenar datos de tarjeta es responsabilidad legal y técnica imposible de asumir.

EPI-007 resuelve estos problemas con cuatro pilares:
1. **Abstracción de pasarelas** (Provider Pattern): el SaaS no habla con Stripe, habla con un `PaymentProvider` genérico. Cambiar de Stripe a PayPal = cambiar 1 archivo.
2. **Idempotencia total**: cada webhook se procesa exactamente una vez, identificado por `payment_intent_id` o `operation_id`. Duplicados son detectados y descartados.
3. **Vaulting zero**: nunca se almacenan números de tarjeta. Solo `payment_intent_id` o `subscription_id` del proveedor.
4. **Dunning management**: cuando una tarjeta falla en una suscripción recurrente, el sistema notifica al cliente antes de cortar el servicio.

### La Promesa

`handle_webhook(payload)` — el momento en que llega la confirmación de pago. En esta función, en la misma transacción atómica, se marca la Order como pagada, se emite `OutboxEvent("payment.confirmed")` con `operation_id`, y Orchestrator activa los entitlements. Si algo falla, el webhook se puede reprocesar de forma segura por idempotencia.

---

## § 2 — LA FILOSOFÍA: Principios Fundacionales Aplicados

| Principio | Cómo se aplica en EPI-007 |
|---|---|
| **Degradación Graciosa** | Telemetry caído → pago procesado con log de contingencia. Pasarela caída → "Modo Revisión Manual" activado. |
| **Aislamiento Total** | `PaymentIntent`, `Subscription`, `Invoice` en schema `tenant_{slug}`. Facturas de Acme son invisibles para Globex. |
| **PCI-DSS por Delegación** | Datos de tarjeta NUNCA almacenados. Solo tokens de la pasarela (`payment_intent_id`). Responsabilidad PCI delegada al proveedor. |
| **Idempotencia** | `operation_id` previene doble-activación. Webhook procesado 2 veces → segundo procesamiento es no-op con OK. |
| **Outbox Pattern** | `OutboxEvent("payment.confirmed")` + `OutboxEvent("provision.requested")` en una sola transacción atómica con la confirmación del pago. |

---

## § 3 — LA ARQUITECTURA: Lo Que EPI-007 Crea

### Estructura de Archivos

```
apps/payments/
├── models.py          ← PaymentIntent, Subscription, Invoice, OutboxEvent, WebhookLog
├── services.py        ← start_session, handle_webhook, process_dunning, cancel_subscription
├── selectors.py       ← get_subscription_status, get_recent_invoices, get_payment_history
├── providers/
│   ├── base.py        ← AbstractPaymentProvider (interface)
│   ├── stripe.py      ← StripeProvider (implementación real)
│   └── paypal.py      ← PayPalProvider (implementación real)
├── api/               ← Endpoints de webhooks seguros
│   ├── views.py       ← stripe_webhook (verifica firma), paypal_webhook
│   └── urls.py
├── exceptions.py      ← PaymentError, WebhookFailed, SubscriptionError, DunningError
├── tasks.py           ← process_outbox_events (Celery), dunning_check (Celery beat)
├── migrations/
│   └── 0001_initial.py
├── templates/
│   ├── payments/
│   │   ├── checkout.html
│   │   └── fallback/
│   │       └── payment_pending.html  ← mensaje "Pago en Revisión" sin Theme
│   └── cotton/
│       ├── checkout_form.html         ← encapsula SDK Stripe Elements
│       ├── subscription_badge.html    ← estado de suscripción del tenant
│       └── invoice_row.html
└── tests/
    ├── test_webhook_idempotency.py
    ├── test_providers.py
    └── test_dunning.py
```

### Modelos de Datos

**`PaymentIntent`** (schema `tenant_{slug}`) — intento de cobro
| Campo | Descripción |
|---|---|
| `id` UUID | — |
| `order_id` UUID | FK lógico a orders.Order |
| `gateway_intent_id` CharField | `pi_xxx` de Stripe o equivalente |
| `provider` CharField | `stripe`, `paypal` |
| `amount` DecimalField | monto cobrado |
| `currency` CharField(3) | `USD`, `EUR` |
| `status` CharField | `created`, `processing`, `succeeded`, `failed` |
| `operation_id` CharField(36) | UUID idempotente |
| `plan_id` CharField null | para Telemetry |
| `plan_matrix_version` CharField null | versión de PlanMatrix aplicada |

**`Subscription`** (schema `tenant_{slug}`) — cobro recurrente
| Campo | Descripción |
|---|---|
| `id` UUID | — |
| `tenant_slug` CharField | — |
| `product_id` UUID | producto suscrito |
| `gateway_subscription_id` CharField | ID en la pasarela |
| `status` CharField | `active`, `past_due`, `cancelled`, `trialing` |
| `current_period_end` DateTime | fin del período actual |
| `dunning_count` IntegerField | intentos de cobro fallidos |

**`Invoice`** (schema `tenant_{slug}`) — registro de cobro (NUNCA datos de tarjeta)
| Campo | Descripción |
|---|---|
| `id` UUID | — |
| `payment_intent` FK | — |
| `gateway_invoice_id` CharField | ID en la pasarela |
| `amount_paid` DecimalField | — |
| `issued_at` DateTime | — |
| `pdf_url` URLField null | URL en el proveedor (no archivo local) |

### Flujo handle_webhook (Transacción Atómica)

```python
def handle_webhook(provider: str, payload: dict, signature: str):
    # 1. Verificar firma del proveedor (HMAC) → si inválida, 400
    # 2. Extraer payment_intent_id como operation_id
    # 3. Idempotencia: si ya procesado → return 200 sin cambios
    with transaction.atomic():
        # 4. Actualizar PaymentIntent.status = 'succeeded'
        # 5. OutboxEvent("payment.confirmed", {order_id, tenant_id, plan_id, amount, operation_id})
        # 6. OutboxEvent("provision.requested", {order_id, tenant_id, operation_id, items[]})
        # 7. Registrar WebhookLog (para auditoría)
    # 8. Celery: process_outbox_events para push a Orchestrator/Orders
    return HttpResponse(status=200)
```

---

## § 4 — EL ÁRBOL: User Stories de Cimientos a Acabados

| US ID | Historia | SP | Sprint | Estado |
|---|---|---|---|---|
| US-007-01 | Provider Pattern: `base.py` + `stripe.py` + `start_session` service | 4 | Sprint-1 | 🔲 Sin US file |
| US-007-02 | `handle_webhook` idempotente + OutboxEvent en transacción atómica | 4 | Sprint-1 | 🔲 Sin US file |
| US-007-03 | `Subscription` model + dunning logic + `cancel_subscription` | 4 | Sprint-2 | 🔲 Sin US file |
| US-007-04 | `Invoice` model + `get_recent_invoices` selector | 2 | Sprint-2 | 🔲 Sin US file |
| US-007-05 | Cotton components: checkout_form (Stripe Elements), subscription_badge | 3 | Sprint-2 | 🔲 Sin US file |

---

## § 5 — BLUEPRINTS DE REFERENCIA

| ID | Documento | Qué gobierna |
|---|---|---|
| CC-7 | `Docs/1-Core_Concept/7-payment-app-cc.md` | Visión, Provider Pattern, idempotencia, outbox |
| PY-2 | `7-Payment-App/2-modelos-payments-py.md` | Modelos exactos |
| PY-3 | `7-Payment-App/3-service-selector-contratos-payments-py.md` | start_session, handle_webhook |
| PY-4 | `7-Payment-App/4-endpoints-webhooks-payments-py.md` | Endpoints de webhooks seguros |
| PY-5 | `7-Payment-App/5-webhooks-outbox-dunning-payments-py.md` | Dunning management y outbox |
| DC-18 | `0-Factory-Saas/18-matriz-seguridad-compliance-fs.md` | PCI-DSS, datos financieros, OWASP A02 |

---

## § 6 — DEFINITION OF DONE

EPI-007 está Done cuando:

- [ ] `start_session(order_id)` crea `PaymentIntent` y retorna URL/secreto para el frontend
- [ ] `handle_webhook(payload)` con firma válida procesa pago y emite OutboxEvents
- [ ] `handle_webhook` con mismo `payment_intent_id` procesado 2 veces → segundo es no-op (idempotente)
- [ ] Webhook con firma inválida → 400 rechazado (test de seguridad)
- [ ] `Invoice` nunca contiene número de tarjeta, CVV ni datos PAN
- [ ] Suscripción con `status=past_due` → Celery task de dunning notifica al usuario
- [ ] Con Payment no instalado → Orders crea order normalmente, Profiles muestra billing como `null`
- [ ] `pytest apps/payments/` pasa con tests de idempotencia, firma y dunning
- [ ] `product-backlog.md` actualizado: US-007-01..05 con estados correctos
