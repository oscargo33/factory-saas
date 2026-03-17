# Documento: Plan de Validacion de Diseno - App Product Orchestrator

**ID:** PO-8-VAL
**Ubicacion:** `./Docs/2-Design-Concept/4-Product-Orchestrator-App/8-plan-validacion-diseno-product-orchestrator-po.md`
**Anchor Docs:** `Docs/2-Design-Concept/4-Product-Orchestrator-App/1-checklist-product-orchestrator-app.md`, `Docs/2-Design-Concept/4-Product-Orchestrator-App/6-matriz-trazabilidad-product-orchestrator-po.md`

---

## 1. Proposito

Definir validacion de diseno Product Orchestrator para asegurar catalogo, autorizacion y degradacion segura por tenant.

---

## 2. Escenarios de validacion (diseno)

| Caso | Objetivo | Evidencia esperada |
|---|---|---|
| PO-VAL-01 | Catalogo por tenant | `get_available_products` no mezcla tenants |
| PO-VAL-02 | Feature habilitada por entitlement activo | `authorize_feature` retorna `allowed=true` |
| PO-VAL-03 | Feature expirada | `authorize_feature` retorna `entitlement_expired` |
| PO-VAL-04 | Cuota excedida | denegacion `quota_exceeded` |
| PO-VAL-05 | Provision post-pago exitoso | entitlements creados y adapter invocado |
| PO-VAL-06 | Payment no instalado | solo productos demo provisionables |
| PO-VAL-07 | Product Core no saludable | respuesta `503` controlada o modo demo |
| PO-VAL-08 | Revocacion por admin | estado final `revoked` auditable |
| PO-VAL-09 | Telemetry ausente | flujo continua sin fallo |
| PO-VAL-10 | RBAC/tenant isolation | rutas admin bloqueadas a `member`; no fuga cross-tenant |
| PO-VAL-11 | Vertical mapea feature externa core | `external_feature_ref` y `adapter_key` coherentes |
| PO-VAL-12 | Producto hibrido core+local | `compose_hybrid_product` genera bundle valido |
| PO-VAL-13 | Sin Product Core | `create_local_product_profile` y provision local operan sin adapter |

---

## 3. Evidencia minima para Sprint Review

- Matriz PO-R01..PO-R13 validada.
- Checklist PO completo por secciones A..G.
- Simulaciones de degradacion (Payment/Core/Telemetry) y seguridad tenant.
- Evidencia de cumplimiento NFR PO.

---

## 4. Criterios de aceptacion

- [ ] Casos PO-VAL-01..PO-VAL-13 con evidencia.
- [ ] Sin brechas entre trazabilidad y validacion.
- [ ] App Product Orchestrator lista para pasar de diseno a implementacion.

---

## 5. Notas adicionales

- Se agregaron los casos PO-VAL-14, PO-VAL-15 y PO-VAL-16 referentes a `Plan enforcement`, `Cambio de plan transaccional` y `Pricing/versioning + idempotency/outbox`.
- Estos casos deben incluirse en la evidencia mínima del Sprint Review y en los playbooks de runbook/reconciliación.
