# Documento: 16-contratos-inter-app-fs.md

**ID:** DC-16-FS
**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/16-contratos-inter-app-fs.md`
**Referencia Core:** `0-factory_saas-cc.md`, `design-layers-kb.md`
**Capa:** Transversal — Contratos de Servicios Inter-App
**Apellido:** **-fs**

---

## 1. Propósito

Este documento define los **contratos públicos** que cada app de la Factory expone para uso de otras apps. Un contrato define:
- Qué funciones/selectores puede invocar una app externa.
- Los tipos de datos de entrada y salida.
- El comportamiento de degradación cuando la app proveedora no está instalada.

La regla es absoluta: **ninguna app importa modelos de otra. Solo importa servicios o selectores públicos listados aquí.**

---

## 2. Registro de Contratos Públicos por App

### 2.1. App `core` (Tenants y Usuarios)

**Archivo:** `apps/core/services.py` y `apps/core/selectors.py`

| Función pública | Tipo | Firma | Retorna |
|---|---|---|---|
| `get_tenant_by_slug` | Selector | `(slug: str) → Tenant \| None` | Instancia Tenant o None |
| `get_user_by_id` | Selector | `(user_id: int) → User \| None` | Instancia User o None |
| `get_active_memberships` | Selector | `(tenant_id: int) → QuerySet` | QuerySet de Membership |
| `create_tenant` | Service | `(name, slug, owner_id) → Tenant` | Tenant creado |
| `deactivate_tenant` | Service | `(tenant_id: int) → Tenant` | Tenant desactivado |

**Consumidores:** Todas las apps (el Tenant es contexto global).

---

### 2.2. App `theme`

**Archivo:** `apps/theme/selectors.py`

| Función pública | Tipo | Firma | Retorna |
|---|---|---|---|
| `get_theme_for_tenant` | Selector | `(tenant_id: int) → ThemeConfig \| None` | Dict con CSS variables o None |

**Fallback si no instalado:**
```python
# En context_processors.py global
if not apps.is_installed('apps.theme'):
    return {"theme": DEFAULT_THEME_TOKENS}
```

**Consumidores:** Context processor global → `base.html`.

---

### 2.3. App `profile`

**Archivo:** `apps/profile/selectors.py`

| Función pública | Tipo | Firma | Retorna |
|---|---|---|---|
| `get_profile_for_user` | Selector | `(user_id: int, tenant_id: int) → ProfileSummary \| None` | Dataclass o None |
| `get_display_name` | Selector | `(user_id: int, tenant_id: int) → str` | Nombre a mostrar en UI |

**Fallback si no instalado:** Retornar `user.username` como display name.

**Consumidores:** `support` (asignar perfil a ticket), `orders` (datos de facturación).

---

### 2.4. App `orders`

**Archivo:** `apps/orders/selectors.py`

| Función pública | Tipo | Firma | Retorna |
|---|---|---|---|
| `get_open_orders_count` | Selector | `(tenant_id: int) → int` | Conteo de órdenes abiertas |
| `get_order_summary` | Selector | `(order_id: int) → OrderSummary \| None` | Dataclass resumen |

**Fallback si no instalado:** Retornar `0` para conteos.

**Consumidores:** `payments` (asociar cobro a orden), `support` (referenciar orden en ticket).

---

### 2.5. App `payments`

**Archivo:** `apps/payments/services.py` y `apps/payments/selectors.py`

| Función pública | Tipo | Firma | Retorna |
|---|---|---|---|
| `get_active_subscription` | Selector | `(tenant_id: int) → SubscriptionSummary \| None` | Dataclass o None |
| `is_feature_enabled` | Selector | `(tenant_id: int, feature: str) → bool` | Booleano |

**Fallback si no instalado:** `is_feature_enabled` retorna `True` (acceso libre por defecto).

**Consumidores:** Todas las apps para verificar si una feature está habilitada en el plan.

---

### 2.6. App `support`

**Archivo:** `apps/support/services.py`

| Función pública | Tipo | Firma | Retorna |
|---|---|---|---|
| `create_system_ticket` | Service | `(tenant_id: int, subject: str, body: str) → Ticket` | Ticket creado automáticamente |

**Fallback si no instalado:** No-op (silently return None).

**Consumidores:** `payments` (crear ticket automático en fallo de pago), telemetría de errores.

---

### 2.7. App `marketing`

**Archivo:** `apps/marketing/services.py`

| Función pública | Tipo | Firma | Retorna |
|---|---|---|---|
| `track_event` | Service | `(event_name: str, tenant_id: int, metadata: dict) → None` | None |

**Fallback si no instalado:** No-op.

**Consumidores:** `orders` (purchase event), `payments` (subscription event).

---

### 2.8. App `product_orchestrator`

**Archivo:** `apps/product_orchestrator/selectors.py`

| Función pública | Tipo | Firma | Retorna |
|---|---|---|---|
| `get_available_products` | Selector | `(tenant_id: int) → QuerySet` | QuerySet de productos activos |
| `get_product_detail` | Selector | `(product_id: int, tenant_id: int) → ProductDetail \| None` | Dataclass o None |

**Fallback si no instalado:** Retornar QuerySet vacío.

**Consumidores:** `orders` (líneas de pedido), `marketing` (catálogo en campañas).

---

## 3. Reglas de Uso de Contratos

| Regla | Descripción |
|---|---|
| **Solo interfaces públicas** | Solo las funciones listadas en este documento pueden ser importadas entre apps |
| **Verificar instalación primero** | Siempre usar `apps.is_installed('apps.{app}')` antes de importar |
| **Importación tardía** | Usar importaciones dentro de la función, no a nivel de módulo, para evitar circular imports |
| **No cachear objetos de otra app** | No guardar instancias de modelos de otras apps en memoria por periodos largos |

---

## 4. Patrón de Importación Segura

Para consumir un contrato de otra app de forma segura:

```
# En app_a/services.py
def do_something_with_profile(user_id, tenant_id):
    from django.apps import apps
    if apps.is_installed('apps.profile'):
        from apps.profile.selectors import get_display_name
        return get_display_name(user_id=user_id, tenant_id=tenant_id)
    return "Usuario"  # fallback neutral
```

---

## 5. Relación con Otros Documentos

| Documento | Relación |
|---|---|
| DC-12 `12-patron-service-layer-fs.md` | Define el patrón Service/Selector que habilita estos contratos |
| `0-factory_saas-cc.md` | Política global de independencia de apps (principios) |
| DC-17 `17-diccionario-datos-logico-fs.md` | Define las entidades que circulan en estos contratos |

---

## 6. Criterios de Aceptación del Diseño

- [ ] Cada app tiene documentado qué funciones expone como contrato público.
- [ ] Cada contrato incluye el comportamiento de fallback cuando la app no está instalada.
- [ ] No existen importaciones de modelos entre apps en ningún archivo del proyecto.
- [ ] El patrón de importación tardía (`apps.is_installed` + import dentro de función) está documentado y adoptado.
