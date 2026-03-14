Este es el **Documento Maestro 6: App Orders (Gestión de Intención y Carrito)**. En el engranaje de la Factory, esta aplicación es el "Contrato", encargado de congelar la voluntad del usuario en una estructura formal que luego será cobrada por Payment.

---

# Documento Maestro 6: App Orders (Gestión de Intención)

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

**¿Procedemos con el Documento Maestro 7: App Payment (Pasarelas y Suscripciones)?** SUSTITUTO_IMAGEN_1