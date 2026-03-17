# Documento: Producto Visible + Admin App 6 Orders

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** OD-11-PV  
**Ubicacion:** `./Docs/2-Design-Concept/6-Orders-App/11-product-visible-admin-orders-od.md`  
**Anchor Docs:** `6-orders-app-cc.md`, `17-diccionario-datos-logico-fs.md`, `21-product-visible-ux-fs.md`

## 1. Objetivo

Definir experiencia visible de carrito/orden y administracion operativa del ciclo de vida de orden.

## 2. CRUD en Django Admin (Orders)

| Modelo | C | R | U | D | Notas UI Admin |
|---|---|---|---|---|---|
| Cart | No (sistema) | Si | Si | Si | Recuperacion y limpieza controlada |
| Order | No (sistema) | Si | Si (estado) | No | Transiciones por maquina de estados |
| OrderItem | No (derivado) | Si | Si (ajuste permitido) | Si | Auditoria de cambios en precio |
| PriceSnapshot | No | Si | No | No | Solo lectura para trazabilidad |

Criterios admin:
- Acciones de transicion: pending -> processing -> completed/cancelled.
- Bloqueo de edicion de snapshots historicos.

## 3. Interfaz de producto visible

Pantallas minimas:
- Carrito.
- Resumen de orden.
- Historial de ordenes.

Estados UX obligatorios:
- `loading`, `empty`, `error`, `success`.

## 4. Criterios de aceptacion

- Flujo carrito -> orden confirmado documentado.
- Si Marketing no esta, UI muestra precio base sin romper checkout.
- Historial permite seguimiento de estado por orden.
