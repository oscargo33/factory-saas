# Documento: Modelos de Datos - App Product Orchestrator

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PO-2-MDL
**Ubicacion:** `./Docs/2-Design-Concept/4-Product-Orchestrator-App/2-modelos-product-orchestrator-po.md`
**Anchor Docs:** `Docs/1-Core_Concept/4-product-orchestrator-app-cc.md`, `Docs/2-Design-Concept/0-Factory-Saas/17-diccionario-datos-logico-fs.md`

---

## 1. Proposito

Definir entidades logicas de Product Orchestrator para catalogo comercial, capacidades tecnicas y autorizacion por tenant.

---

## 2. Entidades

### 2.1 Product

Oferta comercial visible al cliente y consumida por Orders/Marketing/Home.

| Campo | Tipo | Regla |
|---|---|---|
| `id` | UUID PK | Identificador global |
| `tenant_id` | UUID | Referencia logica a tenant propietario |
| `name` | CharField(200) | Requerido |
| `slug` | SlugField(120) | Unico por tenant |
| `description` | TextField | Opcional |
| `price` | Decimal(10,2) | `>= 0` |
| `currency` | CharField(3) | ISO 4217 |
| `product_type` | CharField(30) | `subscription`, `one_time`, `metered` |
| `fulfillment_strategy` | CharField(30) | `digital`, `manual`, `third_party` |
| `is_active` | BooleanField | Publicable en catalogo |
| `is_demo` | BooleanField | Producto habilitable sin Payment |
| `source_strategy` | CharField(20) | `core_only`, `local_only`, `hybrid_bundle` |
| `bundle_definition` | JSONB | Componentes locales/core del producto |
| `metadata` | JSONB | Parametros de UI/segmentacion |
| `created_at` | DateTimeField | UTC |
| `updated_at` | DateTimeField | UTC |

Indices:
- `(tenant_id, slug)` unico.
- `(tenant_id, is_active)` para listados.

### 2.2 Vertical

Capacidad tecnica del Product Core que puede ser asignada a un producto.

| Campo | Tipo | Regla |
|---|---|---|
| `id` | UUID PK | Identificador global |
| `tenant_id` | UUID | Aislamiento por tenant |
| `product_id` | UUID | Referencia logica a Product |
| `feature_key` | CharField(120) | Unico por tenant |
| `name` | CharField(200) | Requerido |
| `provider_kind` | CharField(20) | `core`, `local`, `hybrid` |
| `adapter_key` | CharField(80) | Adapter objetivo (`core_app`, `mock_demo`, etc.) |
| `external_feature_ref` | CharField(180) | Identificador remoto en Product Core (nullable) |
| `quota_limit` | IntegerField | `>= 0`, null para ilimitado |
| `is_active` | BooleanField | Habilita autorizacion |
| `metadata` | JSONB | Parametros tecnicos |
| `created_at` | DateTimeField | UTC |
| `updated_at` | DateTimeField | UTC |

Indices:
- `(tenant_id, feature_key)` unico.
- `(tenant_id, product_id, is_active)` para resolucion de capacidades activas.

### 2.3 Entitlement

Derecho de uso de una capacidad tecnica para un tenant en una ventana de vigencia.

| Campo | Tipo | Regla |
|---|---|---|
| `id` | UUID PK | Identificador global |
| `tenant_id` | UUID | Tenant autorizado |
| `vertical_id` | UUID | Referencia logica a Vertical |
| `source` | CharField(20) | `payment`, `admin`, `demo` |
| `status` | CharField(20) | `active`, `paused`, `expired`, `revoked` |
| `starts_at` | DateTimeField | Inicio de vigencia |
| `ends_at` | DateTimeField | Fin de vigencia (nullable) |
| `quota_used` | IntegerField | `>= 0` |
| `quota_reset_at` | DateTimeField | Reset de consumo |
| `created_at` | DateTimeField | UTC |
| `updated_at` | DateTimeField | UTC |

Indices:
- `(tenant_id, vertical_id, status)` para autorizacion.
- `(tenant_id, ends_at)` para tareas de expiracion.

---

## 3. Reglas de negocio de modelo

- Un `Product` puede agrupar multiples `Vertical`.
- `Vertical` puede mapear capacidad remota del Product Core o capacidad local del Orchestrator segun `provider_kind`.
- `source_strategy=hybrid_bundle` permite combinar verticales `core` y `local` en una sola oferta comercial.
- `source_strategy=local_only` permite crear perfil vendible aunque no exista Product Core.
- `Entitlement` siempre referencia una `Vertical` activa al momento de provision.
- `authorize_feature` debe considerar `status`, vigencia y cuota.
- `quota_used` nunca puede exceder `quota_limit` cuando hay limite definido.
- Revocaciones no eliminan registros; se marca `status=revoked` (auditable).
 - `product_type` define la modalidad comercial y afecta facturacion/checkout.
 - `fulfillment_strategy` define el flujo de entrega (digital/operativo) y habilita hooks en `orders`/`support`.

---

## 4. Relacion con diccionario global

Alineado con DC-17 para `Product` y extendido con entidades propias de orquestacion:
- `Vertical`
- `Entitlement`

Se propone registrar ambas entidades en DC-17 durante permeacion global del sprint.

---

## 5. Criterios de aceptacion

- [ ] Entidades Product/Vertical/Entitlement definidas con aislamiento por tenant.
- [ ] Reglas de vigencia y cuota expresadas en campos y constraints.
- [ ] Sin dependencias de FK duras a modelos de otras apps.
