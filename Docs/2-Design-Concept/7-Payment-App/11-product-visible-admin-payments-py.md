# Documento: Producto Visible + Admin App 7 Payments

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PY-11-PV  
**Ubicacion:** `./Docs/2-Design-Concept/7-Payment-App/11-product-visible-admin-payments-py.md`  
**Anchor Docs:** `7-payment-app-cc.md`, `18-matriz-seguridad-compliance-fs.md`, `21-product-visible-ux-fs.md`

## 1. Objetivo

Definir UX visible de checkout/pagos y administracion de conciliacion, webhooks y suscripciones.

## 2. CRUD en Django Admin (Payments)

| Modelo | C | R | U | D | Notas UI Admin |
|---|---|---|---|---|---|
| PaymentIntent | No (gateway/sistema) | Si | Si (reintento/control) | No | Evitar mutaciones de montos confirmados |
| Subscription | Si | Si | Si | Si (cancelacion) | Mostrar estado y proxima renovacion |
| WebhookEvent | No | Si | Si (reprocess flag) | No | Payload en solo lectura |
| Receipt | No (sistema) | Si | No | No | Descarga y reenvio por email |

Criterios admin:
- Panel de webhooks fallidos con accion reprocess.
- Distincion visual de pagos en revision manual.

## 3. Interfaz de producto visible

Pantallas minimas:
- Checkout final.
- Estado de pago (ok/fail/pending).
- Recibos y suscripcion.

Estados UX obligatorios:
- `loading`, `empty`, `error`, `success`.

## 4. Criterios de aceptacion

- Flujo de pago contempla exito, fallo y reintento.
- Sin confirmacion de gateway no se activa entitlement.
- Mensaje de revision manual disponible cuando aplica.
