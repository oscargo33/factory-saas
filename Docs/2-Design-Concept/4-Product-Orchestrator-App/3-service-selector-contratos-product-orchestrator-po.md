# Documento: Service, Selector y Contratos - App Product Orchestrator

**ID:** PO-3-SVC
**Ubicacion:** `./Docs/2-Design-Concept/4-Product-Orchestrator-App/3-service-selector-contratos-product-orchestrator-po.md`
**Anchor Docs:** `Docs/1-Core_Concept/4-product-orchestrator-app-cc.md`, `Docs/2-Design-Concept/0-Factory-Saas/16-contratos-inter-app-fs.md`, `Docs/2-Design-Concept/0-Factory-Saas/12-patron-service-layer-fs.md`

---

## 1. Proposito

Definir interfaces publicas de App Product Orchestrator para catalogo y autorizacion de capacidades del Product Core.

---

## 2. Contratos publicos (selectores)

| Funcion | Firma | Retorna | Consumidores |
|---|---|---|---|
| `get_available_products` | `(tenant_id: UUID) -> list[ProductDTO]` | Productos activos por tenant | orders, marketing, home, profile |
| `get_product_detail` | `(tenant_id: UUID, product_id: UUID) -> ProductDetailDTO | None` | Detalle de producto | orders, home |
| `get_feature_state` | `(tenant_id: UUID, feature_key: str) -> FeatureStateDTO` | Estado de capacidad y cuota | profile, support |
| `list_entitlements` | `(tenant_id: UUID) -> list[EntitlementDTO]` | Derechos activos y su vigencia | profile, payment |

Fallback si app no instalada:
- `get_available_products`: `[]`
- `get_product_detail`: `None`
- `get_feature_state`: `{"enabled": false, "reason": "orchestrator_unavailable"}`
- `list_entitlements`: `[]`

---

## 3. Contratos publicos (services)

| Funcion | Firma | Retorna | Regla |
|---|---|---|---|
| `authorize_feature` | `(tenant_id: UUID, feature_key: str, consume: int = 0) -> AuthorizationResultDTO` | `allowed`, `reason`, `remaining_quota` | Evalua vigencia, estado y cuota |
| `provision_tenant` | `(tenant_id: UUID, product_id: UUID, source: str) -> ProvisionResultDTO` | `provisioned_verticals`, `warnings` | Crea/actualiza entitlements |
| `revoke_entitlement` | `(tenant_id: UUID, feature_key: str, reason: str) -> RevokeResultDTO` | Estado final | Revocacion auditable |
| `sync_catalog_from_core` | `(tenant_id: UUID) -> SyncResultDTO` | Conteos de upsert | Usa adapter contra Product Core |
| `compose_hybrid_product` | `(tenant_id: UUID, payload: HybridProductPayload) -> ProductDTO` | Producto comercial compuesto | Mezcla componentes core/local |
| `create_local_product_profile` | `(tenant_id: UUID, payload: LocalProductPayload) -> ProductDTO` | Perfil de producto local | Vendible sin Product Core |

Fallbacks:
- Sin Payment instalado: `provision_tenant` solo admite productos `is_demo=true`.
- Sin Profile instalado: `authorize_feature` devuelve `allowed=false` con `reason="profile_unavailable"` para capacidades sensibles.
- Sin Telemetry instalado: servicios no fallan; se omite emision de eventos.
- Sin Product Core instalado/no saludable:
    - `sync_catalog_from_core` retorna `warnings=["core_unavailable"]` sin cortar operacion local.
    - `compose_hybrid_product` permite solo componentes locales disponibles.
    - `create_local_product_profile` permanece totalmente operable.

---

## 4. DTOs de referencia

```python
FeatureStateDTO = {
    "feature_key": str,
    "enabled": bool,
    "quota_limit": int | None,
    "quota_used": int,
    "remaining_quota": int | None,
    "source": "payment" | "admin" | "demo",
}

AuthorizationResultDTO = {
    "allowed": bool,
    "reason": str | None,
    "remaining_quota": int | None,
    "expires_at": str | None,
}
```

---

## 5. Patrón de importacion segura

- Toda llamada inter-app debe usar importacion tardia y `apps.is_installed`.
- No exponer modelos Django entre apps; solo DTOs y tipos basicos.

---

## 6. Plan -> Product Enforcement (Spec corta)

Proposito: garantizar que la habilitacion de `Product`/`Vertical` siga la matriz de elegibilidad por `Plan` del tenant y que ningun consumidor pueda invocar capacidades core sin pasar por esta politica.

Reglas y contratos mínimos:

- Datos de referencia: `PlanMatrix` (versionable) con filas `plan_id -> allowed_products[] -> allowed_verticals[]`.
- Selector público: `get_plan_entitlements(tenant_id: UUID) -> PlanEntitlementsDTO` que devuelve el set efectivo de `product_id` y `feature_key` permitidos para el tenant.
- Enforcement API: `enforce_plan_policy(tenant_id, product_id, vertical_key) -> EnforcementResultDTO` que devuelve `allowed|denied` y `reason`.

Comportamiento operacional:

- Todas las rutas que aprovisionan entitlements o ejecutan `authorize_feature` deben llamar internamente a `enforce_plan_policy` antes de continuar.
- `enforce_plan_policy` se implementa con importacion tardia y debe validar contra `get_active_subscription` del app `payments` y contra la `PlanMatrix` versionada.
- Si la `PlanMatrix` cambia, la aplicacion debe presentar `PlanMatrixVersion` y usar versión en la transacción de aprovisionamiento para trazabilidad.

Datos de auditoría:

- Cada decisión de `enforce_plan_policy` debe producir un `TelemetryEvent` con `tenant_id`, `plan_id`, `product_id`, `vertical_key`, `result`, `matrix_version`.

## 6. Criterios de aceptacion

- [ ] Contratos publicos de selector/service definidos y versionables.
- [ ] Fallbacks declarados para ausencia de apps dependientes.
- [ ] Reglas de consumo por cuota expresadas en `authorize_feature`.
