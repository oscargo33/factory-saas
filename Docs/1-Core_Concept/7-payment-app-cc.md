Este es el **Documento Maestro 7: App Payment (Gestión Financiera)**. En la jerarquía de la Factory, esta aplicación es el "Cajero", responsable de transformar la validación de la orden en flujo de caja real y de asegurar que el acceso al producto esté sincronizado con el estado financiero.

---

# Documento Maestro 7: App Payment (Gestión Financiera)

## 1. Identidad de la Aplicación

* **Nivel de Profundidad:** 7 (Capa de Conversión).
* **Rol:** Ejecución de transacciones, gestión de suscripciones recurrentes y conciliación de pagos mediante pasarelas externas.
* **Dependencias Suaves:** App 6 (Orders) para obtener el monto y el ID de orden; App 2 (Telemetry) para reportar el GMV (Gross Merchandise Value) a La Central.

## 2. Estructura de Archivos (Arquitectura de Carpetas)

```text
payments/
├── api/               # Endpoints para Webhooks (Stripe, PayPal, etc.)
├── providers/         # Adaptadores para diferentes pasarelas
│   ├── base.py        # Clase abstracta para proveedores
│   ├── stripe.py      # Lógica específica de Stripe (dj-stripe)
│   └── paypal.py      # Lógica específica de PayPal
├── services.py        # Lógica de creación de sesiones y cobros recurrentes
├── selectors.py       # Consulta de facturas y estados de suscripción
├── templates/
│   ├── payments/
│   │   └── fallback/  # Mensaje de "Pago en revisión" si no hay UI avanzada
│   └── cotton/        # Componentes financieros
│       ├── checkout_form.html
│       ├── subscription_badge.html
│       └── invoice_row.html

```

## 3. Abstracción de Pasarelas (Provider Pattern)

Para que la IA no genere código acoplado a un solo banco, debe usar una capa de abstracción. El SaaS no habla con "Stripe", habla con un `PaymentProvider` genérico.

* **Webhook Handler:** Cada pasarela envía notificaciones asíncronas. La IA debe implementar una lógica de **Idempotencia** (asegurar que un pago no se registre dos veces si el webhook llega duplicado).
* **Vaulting:** Nunca se guardan números de tarjeta. Solo se almacenan `payment_intent_id` o `subscription_id`.

## 4. Gestión de Suscripciones (Recurrencia)

La IA debe manejar el ciclo de vida del dinero en el tiempo:

* **Sincronización:** Mapeo de `Product_ID` (Orchestrator) con el `Price_ID` de la pasarela.
* **Dunning:** Lógica para gestionar qué pasa cuando una tarjeta expira o un cobro falla (notificar al usuario antes de cortar el servicio).

## 5. Implementación UI con Cotton y Alpine.js

* **`c-checkout-form`:** Un componente que encapsula el SDK de la pasarela (ej. Stripe Elements) y usa Alpine.js para manejar el estado de "Cargando..." y los errores de validación del banco.
* **`x-init` para Montos:** Alpine.js puede formatear dinámicamente el precio según la moneda local detectada, mejorando la confianza del usuario.

## 6. Contratos de Interfaz (Service Layer & Resiliencia)

* **`PaymentService.start_session(order_id)`:** Crea el intento de pago y devuelve la URL o el secreto para el frontend.
* **`PaymentService.handle_webhook(payload)`:** Procesa la confirmación externa y, si es exitosa, llama a `OrdersService.mark_as_paid()`.
* **Protocolo de Resiliencia:** * Si la **App 2 (Telemetry)** no está, el pago se procesa igual, pero la métrica de venta se guarda en un log de contingencia para ser reportada manualmente a La Central.
* Si la pasarela está caída, el sistema ofrece un **"Modo de Pago en Revisión"** (ej. transferencia manual) mediante el `fallback_layout.html`.



## 7. Instrucción de Codificación para la IA (System Prompt)

Usa este prompt para construir esta app:

> "Genera el código para la App **Payment** de una Factory SaaS.
> 1. Implementa un sistema multicasarela usando el **Provider Pattern** (abstracción de Stripe/PayPal).
> 2. Crea un endpoint de **Webhook** seguro que verifique firmas y maneje la idempotencia.
> 3. En `services.py`, gestiona suscripciones recurrentes y el estado de 'Dunning' (reintentos de cobro).
> 4. Usa **Django Cotton** para el formulario de pago y la lista de facturas.
> 5. La UI debe usar **Alpine.js** para prevenir el doble clic en el botón de pagar y mostrar errores de pasarela en tiempo real.
> 6. Implementa **Soft-Dependencies**: tras un pago exitoso, dispara una señal para que el 'Orchestrator' active los servicios, pero captura cualquier error si esa app no está presente."
> 
> 

---

### Verificación de Autonomía

La App Payment es el filtro de seguridad financiera. Puede existir sin Support, Marketing o Home. Su única misión es asegurar que la relación entre la orden (Orders) y el derecho de uso (Orchestrator) esté mediada por un intercambio económico exitoso.

---

## Independencia y Contexto de Ecosistema

### Scope / No Scope
- **Scope:** Ejecución de transacciones con pasarelas (Stripe/PayPal), gestión de suscripciones recurrentes, webhooks, conciliación, generación de facturas.
- **No Scope:** Ownership del catálogo de productos, lógica de descuentos, autenticación de usuarios.

### Interacciones con otras apps
- **Provee a:** App 4 (Orchestrator) — notifica pago exitoso para activar entitlements; App 3 (Profiles) — estado de suscripción para dashboard.
- **Consume de (soft-dependency):**
  - App 6 (Orders): obtiene monto e ID de orden. Fallback: no inicia sesión de pago sin una orden válida.
  - App 2 (Telemetry): reporta GMV a La Central. Fallback: pago procesado; métrica guardada en log de contingencia.

### Entidades de negocio propias
| Entidad | Descripción |
|---|---|
| PaymentIntent | Intento de cobro vinculado a una orden y pasarela |
| Subscription | Relación de cobro recurrente (tenant + plan + pasarela) |
| Invoice | Registro de cobro emitido; nunca almacena datos de tarjeta |

### Riesgos conceptuales aplicables
| ID | Riesgo | Mitigación |
|---|---|---|
| R-01 | Orchestrator activa entitlements llamando modelos de Payment directamente | Solo via señal/servicio: `PaymentService.handle_webhook()` → `OrdersService.mark_as_paid()` |
| R-07 | Dependencia de una sola pasarela de pago | Provider Pattern: `payments/providers/base.py` abstracto; Stripe y PayPal como implementaciones |