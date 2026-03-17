# EPI-004 — Product Orchestrator: El Guardián del Catálogo y los Derechos

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** EPI-004
**Tipo:** Context Epic — Capa 2, adaptador entre el SaaS y el Product Core
**Prioridad:** 2 — Requerido por Orders, Payment, Home
**Sprint objetivo:** Sprint-1
**Dependencias:** EPI-000 Done, EPI-CORE Done, EPI-003 (Profiles para contexto de quien pide acceso)
**Blueprints fuente:**
- `Docs/1-Core_Concept/4-product-orchestrator-app-cc.md`
- `Docs/2-Design-Concept/4-Product-Orchestrator-App/` (11 documentos)

---

## § 1 — EL ALMA: Visión y Razón de Existir

### ¿Qué Problema Resuelve?

El Product Core (el producto que vende el SaaS) es una pieza de software independiente. No sabe nada de tenants, planes, ni restricciones de uso. Sin intermediario, cualquier tenant podría usar cualquier feature del core sin pagar, sin límites, sin control.

EPI-004 es el **guardián de la propiedad intelectual del Product Core**: define *qué productos existen*, *qué características técnicas (Verticals) incluye cada producto*, y *si un tenant específico tiene derecho a usar una feature específica en este momento*. Antes de que cualquier feature del core se ejecute, pasa por el Orchestrator.

### La Promesa

`enforce_plan_policy(tenant_id, product_id, vertical_key)` — una sola función. Si el tenant tiene entitlement activo para esa feature → continúa. Si no → `AccessDenied`. Si el Product Core está caído → mensaje amigable "Servicio temporalmente no disponible", nunca un stack trace.

El Adapter Pattern garantiza que si mañana el Product Core cambia su API, solo se actualiza `adapters/core_app.py` — el resto del SaaS no se toca.

---

## § 2 — LA FILOSOFÍA: Principios Fundacionales Aplicados

| Principio | Cómo se aplica en EPI-004 |
|---|---|
| **Degradación Graciosa** | Payment no disponible → Orchestrator activa modo Demo (free tier limitado). Product Core caído → mensaje amigable, no 500. |
| **Aislamiento Total** | `Product`, `Entitlement` en schema `tenant_{slug}`. Catálogo y derechos de Acme son invisibles para Globex. |
| **Adapter Pattern** | Product Core externo se abstrae detrás de `adapters/base.py`. Cambiar proveedor de core = cambiar 1 archivo. |
| **PlanMatrix Enforcement** | Toda activación de feature pasa por `enforce_plan_policy()` que valida `plan_id → products → verticals`. |
| **Price Snapshot** | Al crear entitlement, se persiste el `price_snapshot` con `price, currency, price_version_id, captured_at`. |

---

## § 3 — LA ARQUITECTURA: Lo Que EPI-004 Crea

### Estructura de Archivos

```
apps/orchestrator/
├── models.py          ← Product, Vertical, Entitlement, PlanMatrix, Bundle
├── services.py        ← provision_tenant, enforce_plan_policy, activate_entitlement, change_plan
├── selectors.py       ← get_public_catalog, get_entitlements, get_plan_matrix, can_use_feature
├── adapters/
│   ├── base.py        ← AbstractCoreAdapter (interface)
│   └── core_app.py    ← InternalCoreAdapter (implementación real)
├── exceptions.py      ← EntitlementError, AccessDenied, ProductNotFoundError, PlanChangeFailed
├── migrations/
│   └── 0001_initial.py
├── templates/
│   ├── orchestrator/
│   │   ├── catalog.html
│   │   └── fallback/
│   │       └── feature_list_basic.html  ← lista simple sin Theme
│   └── cotton/
│       ├── feature_badge.html           ← "Activo" / "Bloqueado" / "Upgrade"
│       └── product_card.html
└── tests/
    ├── test_enforce_plan_policy.py
    ├── test_adapters.py
    └── test_entitlements.py
```

### Modelos de Datos

**`Product`** (schema `tenant_{slug}`)
| Campo | Descripción |
|---|---|
| `id` UUID | — |
| `name` CharField | nombre visible al cliente |
| `product_type` CharField | `subscription`, `one_time`, `metered` |
| `source_strategy` CharField | `core_only`, `local_only`, `hybrid_bundle` |
| `is_active` BooleanField | visible en catálogo |
| `base_price` DecimalField | precio base (snapshoteado en OrderLine) |

**`Vertical`** (schema `tenant_{slug}`) — capacidad técnica del core
| Campo | Descripción |
|---|---|
| `id` UUID | — |
| `key` CharField | clave funcional: `ai.sales.agent` |
| `product` FK | producto que la incluye |
| `is_core_vertical` BooleanField | requiere llamada al Product Core |

**`Entitlement`** (schema `tenant_{slug}`) — derecho de acceso de un tenant
| Campo | Descripción |
|---|---|
| `id` UUID | — |
| `tenant_slug` CharField | tenant beneficiario |
| `vertical` FK | feature autorizada |
| `valid_from` DateTime | inicio de validez |
| `valid_until` DateTime null | null = indefinido |
| `price_snapshot` JSONB | `{price, currency, price_version_id, captured_at}` |
| `operation_id` CharField(36) | UUID idempotente de la operación de activación |

### PlanMatrix y Outbox Pattern

```python
# Cambio de plan transaccional (idempotente)
def change_plan(tenant_id, new_plan_id, operation_id):
    with transaction.atomic():
        # 1. Verificar operation_id: si ya procesado, retornar idempotente
        # 2. Emitir event: plan.change.requested
        # 3. Aplicar deny-by-default hasta reconciliación
        # 4. Revocar entitlements del plan anterior
        # 5. Activar entitlements del nuevo plan
        # 6. Emitir event: plan.change.completed
        # 7. Persistir OutboxEvent: provision.requested con operation_id
```

---

## § 4 — EL ÁRBOL: User Stories de Cimientos a Acabados

| US ID | Historia | SP | Sprint | Estado |
|---|---|---|---|---|
| US-004-01 | `Product` + `Vertical` models + `get_public_catalog` selector | 3 | Sprint-1 | 🔲 Sin US file |
| US-004-02 | `Entitlement` model + `enforce_plan_policy` service | 4 | Sprint-1 | 🔲 Sin US file |
| US-004-03 | Adapter Pattern: `base.py` + `core_app.py` implementación | 3 | Sprint-1 | 🔲 Sin US file |
| US-004-04 | `PlanMatrix` + `change_plan` transaccional + OutboxEvent | 4 | Sprint-2 | 🔲 Sin US file |
| US-004-05 | Cotton components: feature_badge, product_card + fallback UI | 2 | Sprint-2 | 🔲 Sin US file |

---

## § 5 — BLUEPRINTS DE REFERENCIA

| ID | Documento | Qué gobierna |
|---|---|---|
| CC-4 | `Docs/1-Core_Concept/4-product-orchestrator-app-cc.md` | Visión, PlanMatrix, price snapshot, outbox |
| PO-2 | `4-Product-Orchestrator-App/2-modelos-product-orchestrator-po.md` | Modelos exactos |
| PO-3 | `4-Product-Orchestrator-App/3-service-selector-contratos-product-orchestrator-po.md` | enforce_plan_policy, contratos |
| PO-4 | `4-Product-Orchestrator-App/4-endpoints-middleware-adapters-product-orchestrator-po.md` | Adapter Pattern, endpoints |
| PO-5 | `4-Product-Orchestrator-App/5-catalogo-entitlements-fallback-product-orchestrator-po.md` | Catálogo y modo Demo |
| DC-19 | `0-Factory-Saas/19-plan-matrix-fs.md` | PlanMatrix versioning y enforcement |

---

## § 6 — DEFINITION OF DONE

EPI-004 está Done cuando:

- [ ] `enforce_plan_policy("acme", "product-pro", "ai.sales.agent")` retorna `True` si entitlement activo
- [ ] `enforce_plan_policy("acme", "product-pro", "ai.sales.agent")` retorna `AccessDenied` si no tiene entitlement
- [ ] `get_public_catalog()` retorna lista de productos activos con precios
- [ ] `change_plan` es idempotente: ejecutar 2 veces con mismo `operation_id` no duplica cambios
- [ ] Product Core caído → `provision_tenant` retorna mensaje amigable, no 500
- [ ] Payment no instalado → Orchestrator activa modo Demo para tenant
- [ ] `pytest apps/orchestrator/` pasa incluyendo tests de adapt y enforce_plan_policy
- [ ] `product-backlog.md` actualizado: US-004-01..05 con estados correctos
