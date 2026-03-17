Este es el **Documento Maestro 6: App Orders (Gestión de Intención y Carrito)**. En el engranaje de la Factory, esta aplicación es el "Contrato", encargado de congelar la voluntad del usuario en una estructura formal que luego será cobrada por Payment.

---

# Documento Maestro 6: App Orders (Gestión de Intención)

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

## 1. Identidad de la Aplicación

* **Nivel de Profundidad:** 6 (Capa de Transacción).
* **Rol:** Gestión de carritos de compra, persistencia de "deseos" (Wishlist) y formalización de órdenes de venta.
* **Dependencias Suaves:** App 4 (Orchestrator) para validar existencia de productos; App 5 (Marketing) para aplicar descuentos finales.

## 2. Estructura de Archivos (Arquitectura de Carpetas)

```text
orders/
├── models.py          # Cart, CartItem, Order, OrderItem, Wishlist
├── services.py        # Lógica de transición Carrito -> Orden
├── selectors.py       # Consultas de historial de pedidos para el usuario
├── state_machine.py   # Definición de estados (Draft, Pending, Paid, Canceled)
├── templates/
│   ├── orders/
│   │   └── fallback/  # Resumen de carrito en tabla HTML pura
│   └── cotton/        # Componentes de flujo de compra
│       ├── cart_drawer.html
│       ├── order_summary.html
│       └── add_to_cart_btn.html

```

## 3. Arquitectura: El "Snapshot" de Datos

Para que la IA no cometa errores de integridad financiera, debe entender que una **Order** no puede apuntar solo al precio actual del Orchestrator:

* **Cart:** Es dinámico. Si el precio del producto cambia, el carrito se actualiza.
* **Order:** Es un **Snapshot**. Al crear la orden, se deben copiar los campos `price`, `tax` y `discount` en ese instante. Si el precio sube mañana, la orden ya creada mantiene el precio pactado.

Requerimientos operativos adicionales (core-level):

- **`OrderLine.price_snapshot`**: Cada `OrderItem`/`OrderLine` debe persistir un objeto `price_snapshot` que incluya `price`, `currency`, `price_version_id`, `applied_taxes` y `captured_at`.
- **`OrderLine.product_type`**: Copiar el `product_type` desde el `ProductDetail` retornado por el `Orchestrator` (`subscription|one_time|metered`) y persistirlo en la línea de la orden para decisiones posteriores (facturación/fulfillment).

## 4. Máquina de Estados (Order Lifecycle)

La IA debe implementar un control de flujo estricto:

1. **Draft:** Carrito convertido en orden, esperando selección de método de pago.
2. **Pending:** Comunicación iniciada con la App 7 (Payment).
3. **Processing/Paid:** Pago confirmado, disparando señal al Orchestrator para activar servicios.
4. **Completed:** Recursos entregados y factura generada.

## 5. Implementación UI con Cotton y Alpine.js

* **`c-cart-drawer`:** Un panel lateral que usa Alpine.js para mostrar el contenido del carrito en tiempo real sin recargar la página.
* **`x-on:cart-updated.window`:** Uso de eventos globales de Alpine para que, al añadir un producto desde la App `Home`, el contador del carrito en el header se actualice instantáneamente.

## 6. Contratos de Interfaz (Service Layer & Resiliencia)

* **`OrdersService.freeze_cart(cart_id)`:** Toma el carrito y crea una `Order` con todos los precios inmutables.
* **PlanMatrix enforcement:** Antes de convertir carrito → orden, `OrdersService.freeze_cart` debe invocar `product_orchestrator.enforce_plan_policy(tenant_id, product_id, vertical_key)` para validar que el tenant puede comprar ese `product_id`. Si `enforce_plan_policy` devuelve `denied`, la creación de la orden falla con razón explícita.
* **Outbox on order creation:** Al crear la `Order` (estado `Pending`) la app `orders` debe persistir un `OutboxEvent` con `event_type = "provision.requested"` y `payload` que incluya `order_id, tenant_id, operation_id, items[]` (cada item con `product_id, product_type, price_snapshot`). Esto garantiza entrega confiable hacia `payments`/`orchestrator` para pasos posteriores.
* **Protocolo de Resiliencia:** * Si la **App 5 (Marketing)** no responde, la orden se crea al precio de lista del Orchestrator sin detener el checkout.
* Si la **App 2 (Telemetry)** falla, se guarda un log local del intento de compra para conciliación posterior en La Central.
* El `fallback_layout.html` muestra una tabla simple con los ítems y un botón de "Confirmar", funcional sin CSS avanzado.



## 7. Instrucción de Codificación para la IA (System Prompt)

Usa este prompt para construir esta app:

> "Genera el código para la App **Orders** de una Factory SaaS.
> 1. Crea modelos para `Cart` (volátil) y `Order` (snapshot inmutable).
> 2. Implementa una **Máquina de Estados** para las órdenes (Draft -> Pending -> Paid).
> 3. En `services.py`, crea la función `checkout` que convierta un carrito en orden copiando los precios actuales para evitar cambios futuros.
> 4. Usa **Django Cotton** para el 'Cart Drawer' y el 'Order Summary'.
> 5. La UI debe ser reactiva usando **Alpine.js** (especialmente para actualizar cantidades y totales mediante fetch asíncrono).
> 6. Implementa **Soft-Dependencies**: si 'Marketing' está instalado, llama a su servicio para restar descuentos antes de congelar la orden."
> 
> 

---

### Verificación de Autonomía

La App Orders es el puente entre el catálogo (Orchestrator) y el dinero (Payment). Puede funcionar perfectamente sin Marketing (no hay descuentos) o sin Support. Su único "piso" obligatorio es tener un producto que vender y un usuario a quién cargárselo.

---

## Independencia y Contexto de Ecosistema

### Scope / No Scope
- **Scope:** Carrito de compras (dinámico), snapshot inmutable de orden, máquina de estados de orden, ciclo de vida completo hasta entrega a Payment.
- **No Scope:** Ejecución financiera real, procesamiento de pagos, autenticación de usuarios.

### Interacciones con otras apps
- **Provee a:** App 7 (Payment) — monto e ID de orden para cobrar; App 8 (Support) — contexto de reclamos; App 3 (Profiles) — historial de pedidos para dashboard.
- **Consume de (soft-dependency):**
  - App 4 (Orchestrator): valida existencia y precio de productos. Fallback: bloquea el checkout si el producto no existe.
  - App 5 (Marketing): aplica descuentos. Fallback: orden se crea al precio de lista (`Decimal('0.00')` de descuento).
  - App 2 (Telemetry): reporta intentos de compra. Fallback: log local para conciliación posterior.

### Entidades de negocio propias
| Entidad | Descripción |
|---|---|
| Cart | Intención de compra editable; precio actualizable mientras está activo |
| Order | Snapshot inmutable de todos los precios, impuestos y descuentos al momento del checkout |
| OrderItem | Línea de producto dentro de la orden (precio congelado) |

### Riesgos conceptuales aplicables
| ID | Riesgo | Mitigación |
|---|---|---|
| R-01 | Payment consulta Cart/Order directamente via modelos | Solo acceso via `OrdersService.freeze_cart()` y `OrdersSelector` |
| R-02 | Marketing falla durante checkout → precio indefinido | Fallback explícito: `descuento = Decimal('0.00')` si Marketing no responde |
