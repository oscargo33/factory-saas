# Documento: 12-patron-service-layer-fs.md

**ID:** DC-12-FS
**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/12-patron-service-layer-fs.md`
**Referencia Core:** `0-factory_saas-cc.md`, `design-layers-kb.md`
**Capa:** 4 — Lógica de Negocio (Service/Selector Pattern)
**Apellido:** **-fs**

---

## 1. Propósito

La Capa 4 establece el **patrón arquitectónico obligatorio** para toda la lógica de negocio de la Factory. Este documento define la separación entre escritura de datos (Services) y lectura de datos (Selectors), garantizando:

- Código testeable y desacoplado.
- Claridad sobre qué tiene efectos secundarios y qué no.
- Independencia entre apps (ninguna importa modelos de otra).

---

## 2. Principios Fundamentales

| Principio | Descripción |
|---|---|
| **Single Responsibility** | `services.py` ejecuta una acción de dominio. `selectors.py` ejecuta una consulta. |
| **No Cross-App Model Import** | Ninguna app importa modelos de otra. Las interacciones son vía services/selectors. |
| **Side-Effect Separation** | Los selectors son puros: no modifican estado, no disparan señales. |
| **Data In, Data Out** | Los services reciben tipos primitivos o DTOs, no instancias de modelos externos. |

---

## 3. Estructura de Archivos por App

Cada app de la Factory tiene la siguiente estructura de capa de negocio:

```
apps/
└── {nombre_app}/
    ├── models.py         ← Solo definición de modelo (sin lógica)
    ├── services.py       ← Escritura: crear, actualizar, eliminar, transacciones
    ├── selectors.py      ← Lectura: consultas filtradas, agregaciones
    ├── exceptions.py     ← Excepciones de dominio propias del app
    ├── tasks.py          ← Tareas Celery (invocan services internamente)
    └── views.py          ← Solo orquestación: valida entrada → llama service/selector → retorna respuesta
```

---

## 4. Diseño de `services.py`

### 4.1. Responsabilidades

- Ejecutar operaciones de escritura (CREATE, UPDATE, DELETE).
- Coordinar transacciones de base de datos (`atomic()`).
- Disparar señales o eventos de dominio al final de la transacción.
- Llamar a servicios de otras apps **únicamente a través de su interfaz pública** (nunca importando modelos).

### 4.2. Convenciones de Naming

Formato: `{verbo}_{sustantivo}(param1, param2, ...) → DomainObject`

Ejemplos:
- `create_tenant(name: str, slug: str, owner_id: int) → Tenant`
- `activate_subscription(tenant_id: int, plan_id: int) → Subscription`
- `cancel_order(order_id: int, reason: str) → Order`
- `send_support_ticket(user_id: int, subject: str, body: str) → Ticket`

### 4.3. Manejo de Errores

Los services **nunca retornan None ni booleanos** para señalar fallo. Siempre elevan una excepción de dominio. Esto garantiza que el llamador debe manejar explícitamente el error.

Jerarquía de excepciones base (definida en `core/exceptions.py`):

```
FactoryBaseException
├── ServiceError              ← Error de lógica de negocio (no de infraestructura)
│   ├── ValidationError       ← Datos de entrada inválidos
│   ├── BusinessRuleViolation ← Operación prohibida por regla de dominio
│   └── StateConflict         ← El objeto está en un estado incompatible
├── NotFoundError             ← El recurso solicitado no existe
└── PermissionDenied          ← El actor no tiene autorización
```

---

## 5. Diseño de `selectors.py`

### 5.1. Responsabilidades

- Ejecutar consultas de base de datos (`SELECT` únicamente).
- Aplicar filtros, ordenamiento y paginación.
- Retornar `QuerySet`, `dict`, `list`, o dataclasses.
- **No modificar estado.** Si lo hace, es un service, no un selector.

### 5.2. Convenciones de Naming

Formato: `get_{sustantivo}[_by_{criterio}](param) → QuerySet | dict | list`

Ejemplos:
- `get_active_tenants() → QuerySet[Tenant]`
- `get_tenant_by_slug(slug: str) → Tenant`
- `get_orders_for_tenant(tenant_id: int, filters: dict) → QuerySet[Order]`
- `get_subscription_summary(tenant_id: int) → dict`

### 5.3. Regla de QuerySet Tardiamente Evaluado

Los selectors devuelven `QuerySet` sin evaluar cuando sea posible. La evaluación ocurre en la vista o en el template. Esto permite a la vista agregar paginación o filtros adicionales sin duplicar consultas.

---

## 6. Contrato de Comunicación Inter-App

Para que `app_A` use datos de `app_B`, el flujo es:

```
app_A/views.py
    │
    ├── from app_a.selectors import get_mi_dato       ← Solo su propio selector
    │
    └── from app_b.services import get_public_datum   ← Interface pública de app_B
            │  (Nunca: from app_b.models import ModelB)
            ▼
        app_b/services.py o selectors.py
```

El contrato público de cada app se documenta en DC-16 (`16-contratos-inter-app-fs.md`).

---

## 7. Vistas: Rol de Orquestador

La vista (`views.py`) tiene un rol **exclusivamente orquestador**. No contiene lógica de negocio ni consultas directas a modelos.

Flujo de ejecución de una vista típica:

```
request
    │
    1. Validate input (form/serializer)
    │
    2. Check permissions (decorators/mixins)
    │
    3. Call selector OR service
    │
    4. Return response (render / JsonResponse / redirect)
```

Tamaño objetivo: ninguna vista debe superar 30 líneas de código real.

---

## 8. Tareas Celery y Servicios

Las tareas Celery (`tasks.py`) son **orquestadores asíncronos**, no lógica de negocio. Deben:
1. Recibir solo IDs/primitivos en su payload (no objetos serializados complejos).
2. Hidratar el objeto desde la DB al inicio de la tarea.
3. Invocar el service correspondiente.
4. Manejar excepciones de dominio y decidir si reintentar.

---

## 9. Relación con Otros Documentos

| Documento | Relación |
|---|---|
| `design-layers-kb.md` | Fundamento teórico del patrón Service/Selector en el knowledge base |
| DC-16 `16-contratos-inter-app-fs.md` | Documenta la interfaz pública de cada app (lo que puede ser importado) |
| DC-11 `11-configuracion-redis-celery-fs.md` | Las tareas Celery de cada app siguen este patrón para invocar services |

---

## 10. Criterios de Aceptación del Diseño

- [ ] Ningún archivo `views.py` contiene llamadas directas al ORM (`.filter()`, `.save()`, etc.).
- [ ] Toda operación de escritura está en `services.py`.
- [ ] Todo selector retorna `QuerySet`, `dict`, `list`, o dataclass — nunca instancias de modelos de otra app.
- [ ] Todas las excepciones de dominio heredan de `FactoryBaseException`.
- [ ] Ninguna app importa modelos de otra app (`from other_app.models import X` está prohibido).
- [ ] Los services usan `atomic()` para operaciones que afectan múltiples tablas.
