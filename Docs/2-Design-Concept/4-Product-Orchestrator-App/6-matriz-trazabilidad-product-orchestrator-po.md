# Documento: Matriz de Trazabilidad - App Product Orchestrator

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PO-6-TRA
**Ubicacion:** `./Docs/2-Design-Concept/4-Product-Orchestrator-App/6-matriz-trazabilidad-product-orchestrator-po.md`
**Anchor Docs:** `Docs/1-Core_Concept/4-product-orchestrator-app-cc.md`, `Docs/2-Design-Concept/0-Factory-Saas/13-router-dinamico-esquemas-fs.md`

---

## 1. Proposito

Asegurar trazabilidad entre requerimientos de orquestacion funcional y artefactos de diseno Product Orchestrator.

---

## 2. Matriz Requerimiento -> Diseno -> Evidencia

| Req ID | Requerimiento | Documento | Evidencia |
|---|---|---|---|
| PO-R01 | Catalogo comercial por tenant | `2-modelos-product-orchestrator-po.md` | `Product` con `tenant_id`, `is_active` |
| PO-R02 | Mapeo producto -> capacidades tecnicas | `2-modelos-product-orchestrator-po.md` | `Vertical` ligada a `product_id` |
| PO-R03 | Derecho de uso con vigencia | `2-modelos-product-orchestrator-po.md` | `Entitlement` con `starts_at/ends_at/status` |
| PO-R04 | Autorizacion por feature | `3-service-selector-contratos-product-orchestrator-po.md` | `authorize_feature` con DTO de respuesta |
| PO-R05 | Provision post-compra | `5-catalogo-entitlements-fallback-product-orchestrator-po.md` | Flujo A de provision |
| PO-R06 | Integracion desacoplada con Product Core | `4-endpoints-middleware-adapters-product-orchestrator-po.md` | Adapter Pattern `base/core_app/mock_demo` |
| PO-R07 | Degradacion sin Payment | `3-service-selector-contratos-product-orchestrator-po.md` | Restriccion a productos demo |
| PO-R08 | Degradacion sin Product Core | `5-catalogo-entitlements-fallback-product-orchestrator-po.md` | `503` controlado o modo demo |
| PO-R09 | Aislamiento tenant en endpoints | `4-endpoints-middleware-adapters-product-orchestrator-po.md` | Contexto tenant obligatorio |
| PO-R10 | Telemetria degradable | `5-catalogo-entitlements-fallback-product-orchestrator-po.md` | Flujo continua sin Telemetry |
| PO-R11 | Vertical integra Product Core por configuracion | `2-modelos-product-orchestrator-po.md` | `provider_kind/adapter_key/external_feature_ref` |
| PO-R12 | Producto hibrido core+local | `3-service-selector-contratos-product-orchestrator-po.md` | `compose_hybrid_product` |
| PO-R13 | Operacion sin Product Core con perfil local vendible | `5-catalogo-entitlements-fallback-product-orchestrator-po.md` | Flujo E `local_only` |
| PO-R14 | Plan -> Product enforcement | `3-service-selector-contratos-product-orchestrator-po.md` | `PlanMatrix` + `enforce_plan_policy` |
| PO-R15 | Cambio de plan transaccional y seguro | `5-catalogo-entitlements-fallback-product-orchestrator-po.md` | Flujo F `plan.change.*` |
| PO-R16 | Pricing/versioning + idempotency/outbox | `7-nfr-seguridad-operacion-product-orchestrator-po.md` | `price_snapshot` + `outbox_events` |

---

## 3. Criterios de aceptacion

- [ ] PO-R01..PO-R16 trazados a artefactos concretos.
- [ ] Evidencia de cada requerimiento definida para Sprint Review.
- [ ] Sin huecos entre Core y Design.

## 4. Cobertura obligatoria DC-12/DC-13/DC-16/DC-17

- DC-12 (patron service layer): cubierto en `3-service-selector-contratos-product-orchestrator-po.md`.
- DC-13 (router dinamico y contexto tenant): cubierto en endpoints/adapters con tenant context obligatorio.
- DC-16 (contratos inter-app): cubierto por contratos de autorizacion/provision y eventos `provision.requested`.
- DC-17 (diccionario de datos logico): cubierto por entidades `Product`, `Vertical`, `Entitlement`, `PlanMatrix` y snapshots de pricing.
