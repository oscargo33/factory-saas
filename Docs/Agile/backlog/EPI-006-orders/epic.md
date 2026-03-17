# EPI-006 — Orders: El Contrato Sagrado Entre Intención y Cobro

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** EPI-006
**Tipo:** Commercial Epic — Capa 3, formalización de la voluntad de compra
**Prioridad:** 3 — Requerido por Payment; núcleo del flujo de ventas
**Sprint objetivo:** Sprint-1
**Dependencias:** EPI-000 Done, EPI-CORE Done, EPI-004 (Orchestrator para validar productos)
**Blueprints fuente:**
- `Docs/1-Core_Concept/6-orders-app-cc.md`
- `Docs/2-Design-Concept/6-Orders-App/` (12 documentos)

---

## § 1 — EL ALMA: Visión y Razón de Existir

### ¿Qué Problema Resuelve?

El momento más delicado en un SaaS es la transición de "quiero comprar esto" a "esto está siendo cobrado". Si el precio cambia entre que el usuario lo seleccionó y el momento en que se cobra, hay un fraude o un malentendido. Si la orden se duplica por un doble-click, el cliente paga dos veces.

EPI-006 resuelve este problema con dos conceptos inseparables:
1. **Cart (Carrito):** Dinámico, mutable. El precio puede cambiar mientras el usuario navega.
2. **Order (Orden):** Snapshot inmutable. El instante en que el usuario confirma la compra, se congelan todos los precios, descuentos e impuestos en ese momento exacto. Nunca cambian.

### La Promesa

`freeze_cart(cart_id)` es la función más importante del SaaS. Toma el carrito, valida que los productos existen y el tenant puede comprarlos (`enforce_plan_policy`), aplica descuentos de Marketing (`0.00` si no hay), congela TODO en una `Order` con `price_snapshot` completo, y emite un `OutboxEvent("provision.requested")` en la misma transacción atómica. Payment recoge ese evento y toma el relevo.

---

## § 2 — LA FILOSOFÍA: Principios Fundacionales Aplicados

| Principio | Cómo se aplica en EPI-006 |
|---|---|
| **Degradación Graciosa** | Marketing no responde → orden a precio de lista. Telemetry falla → log local del intento. |
| **Aislamiento Total** | Cart y Order en schema `tenant_{slug}`. Carrito de Acme no es visible para Globex. |
| **Inmutabilidad Financiera** | `OrderLine.price_snapshot` nunca se modifica después de creado. La integridad financiera está garantizada por construcción. |
| **Outbox Pattern** | `OutboxEvent("provision.requested")` persiste en la misma transacción que la creación de la Order. No hay ventana de fallo entre "Order creada" y "Payment notificado". |
| **Idempotencia** | `freeze_cart` con mismo `cart_id` dos veces → retorna la Order existente. No duplica. |

---

## § 3 — LA ARQUITECTURA: Lo Que EPI-006 Crea

### Estructura de Archivos

```
apps/orders/
├── models.py          ← Cart, CartItem, Order, OrderLine, OutboxEvent
├── services.py        ← freeze_cart, add_to_cart, remove_from_cart, cancel_order
├── selectors.py       ← get_cart, get_order, get_recent_orders, get_order_by_id
├── state_machine.py   ← OrderStateMachine: Draft→Pending→Processing→Completed / Cancelled
├── exceptions.py      ← CartNotFound, OrderError, FreezeCartFailed, InvalidStateTransition
├── migrations/
│   └── 0001_initial.py
├── templates/
│   ├── orders/
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   └── fallback/
│   │       └── order_summary_basic.html  ← tabla HTML pura sin Theme
│   └── cotton/
│       ├── cart_drawer.html              ← panel lateral Alpine.js
│       ├── order_summary.html
│       └── add_to_cart_btn.html          ← Alpine.js reactive
└── tests/
    ├── test_freeze_cart.py
    ├── test_state_machine.py
    └── test_outbox.py
```

### Modelos de Datos

**`Cart`** (schema `tenant_{slug}`) — dinámico, mutable
| Campo | Descripción |
|---|---|
| `id` UUID | — |
| `user_id` IntegerField | dueño del carrito |
| `tenant_slug` CharField | — |
| `status` CharField | `active`, `converted`, `abandoned` |
| `created_at` / `updated_at` DateTime | — |

**`CartItem`** (schema `tenant_{slug}`)
| Campo | Descripción |
|---|---|
| `cart` FK | — |
| `product_id` UUID | FK lógico a Orchestrator.Product |
| `quantity` PositiveIntegerField | — |
| `current_price` DecimalField | precio actual del producto (actualizable) |

**`Order`** (schema `tenant_{slug}`) — snapshot INMUTABLE
| Campo | Descripción |
|---|---|
| `id` UUID | — |
| `cart` FK | carrito origen (referencia histórica) |
| `user_id` IntegerField | — |
| `tenant_slug` CharField | — |
| `status` CharField | `draft`, `pending`, `processing`, `completed`, `cancelled` |
| `operation_id` CharField(36) | UUID idempotente de esta transacción |
| `total_amount` DecimalField | suma de líneas (inmutable post-creación) |
| `created_at` DateTime | — |

**`OrderLine`** (schema `tenant_{slug}`) — snapshot de precio POR LÍNEA
| Campo | Descripción |
|---|---|
| `order` FK | — |
| `product_id` UUID | referencia a producto en el momento |
| `product_name` CharField | copiado del catálogo |
| `product_type` CharField | `subscription`, `one_time`, `metered` (copiado) |
| `quantity` PositiveIntegerField | — |
| `price_snapshot` JSONB | `{price, currency, price_version_id, applied_taxes, discount, captured_at}` |

### Flujo freeze_cart (Transacción Atómica)

```python
def freeze_cart(cart_id, operation_id=None):
    operation_id = operation_id or str(uuid4())
    with transaction.atomic():
        # 1. Idempotencia: si Order con este cart ya existe → retorna
        # 2. Cargar cart + items
        # 3. enforce_plan_policy(tenant_id, product_id) para cada item
        # 4. get_discount_for_product (Marketing, fallback Decimal('0.00'))
        # 5. Crear Order(status='pending', operation_id=operation_id)
        # 6. Crear OrderLine por item con price_snapshot completo
        # 7. OutboxEvent(event_type='provision.requested', payload={order_id, tenant_id, operation_id, items[]})
        # 8. Cart.status = 'converted'
        return order
```

---

## § 4 — EL ÁRBOL: User Stories de Cimientos a Acabados

| US ID | Historia | SP | Sprint | Estado |
|---|---|---|---|---|
| US-006-01 | `Cart` + `CartItem` models + add_to_cart / remove_from_cart services | 3 | Sprint-1 | 🔲 Sin US file |
| US-006-02 | `Order` + `OrderLine` models con price_snapshot + state_machine | 4 | Sprint-1 | 🔲 Sin US file |
| US-006-03 | `freeze_cart` service transaccional + OutboxEvent | 4 | Sprint-1 | 🔲 Sin US file |
| US-006-04 | Cotton components: cart_drawer, order_summary, add_to_cart_btn (Alpine.js) | 3 | Sprint-2 | 🔲 Sin US file |

### Dependencias

```
US-006-01 (Cart) ──→ US-006-02 (Order necesita Cart)
US-006-02        ──→ US-006-03 (freeze_cart necesita Order y OrderLine)
US-006-01 + US-006-02 + US-006-03 ──→ US-006-04 (UI necesita modelos completos)
```

---

## § 5 — BLUEPRINTS DE REFERENCIA

| ID | Documento | Qué gobierna |
|---|---|---|
| CC-6 | `Docs/1-Core_Concept/6-orders-app-cc.md` | Snapshot inmutable, outbox, price_snapshot |
| OD-2 | `6-Orders-App/2-modelos-orders-od.md` | Modelos exactos con todos los campos |
| OD-3 | `6-Orders-App/3-service-selector-contratos-orders-od.md` | freeze_cart, contratos |
| OD-5 | `6-Orders-App/5-order-lifecycle-fallback-od.md` | State machine y fallbacks |
| OD-9 | `6-Orders-App/9-contract-tests-skeleton-orders-od.md` | Contract tests con Payment y Orchestrator |

---

## § 6 — DEFINITION OF DONE

EPI-006 está Done cuando:

- [ ] `freeze_cart(cart_id)` crea Order con `price_snapshot` completo y `OutboxEvent("provision.requested")`
- [ ] `freeze_cart(cart_id)` ejecutado 2 veces con mismo `cart_id` retorna la Order existente (idempotente)
- [ ] Si `enforce_plan_policy` rechaza un item → `FreezeCartFailed` con razón explícita, sin Order creada
- [ ] Si Marketing no disponible → descuento en OrderLine = `Decimal('0.00')`, freeze continúa
- [ ] `OrderLine.price_snapshot` es inmutable (no existe endpoint ni service para modificarla)
- [ ] Máquina de estados: transición inválida (ej. `completed → pending`) levanta `InvalidStateTransition`
- [ ] `pytest apps/orders/` pasa incluyendo tests de outbox, idempotencia y state machine
- [ ] `product-backlog.md` actualizado: US-006-01..04 con estados correctos
