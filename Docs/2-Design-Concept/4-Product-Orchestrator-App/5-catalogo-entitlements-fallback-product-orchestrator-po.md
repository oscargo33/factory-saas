# Documento: Catalogo, Entitlements y Fallback - App Product Orchestrator

**ID:** PO-5-OPS
**Ubicacion:** `./Docs/2-Design-Concept/4-Product-Orchestrator-App/5-catalogo-entitlements-fallback-product-orchestrator-po.md`
**Anchor Docs:** `Docs/1-Core_Concept/4-product-orchestrator-app-cc.md`, `Docs/2-Design-Concept/0-Factory-Saas/15-protocolo-comunicacion-central-fs.md`

---

## 1. Proposito

Definir flujos operativos de catalogo/autorizacion y degradacion segura de Product Orchestrator.

---

## 2. Flujo A: Provision post-pago

1. Payment emite evento de compra aprobada.
2. Product Orchestrator valida producto y verticales activas.
3. Se crean/actualizan `Entitlement` por `feature_key`.
4. Adapter provisiona capacidades en Product Core.
5. Telemetry registra evento `orchestrator.provision.success`.

Fallbacks:
- Sin Payment: no se ejecuta flujo comercial; solo modo demo/admin.
- Product Core no saludable: se crea entitlement en estado `paused` y warning operativo.

---

## 3. Flujo B: Autorizacion en tiempo de uso

1. Consumidor llama `authorize_feature(tenant_id, feature_key)`.
2. Se verifica entitlement activo y vigencia.
3. Si hay cuota, se calcula restante y se bloquea sobreconsumo.
4. Respuesta con `allowed/reason/remaining_quota`.

Causas comunes de denegacion:
- `entitlement_missing`
- `entitlement_expired`
- `quota_exceeded`
- `profile_unavailable`

---

## 4. Flujo C: Sincronizacion de catalogo

1. Job o endpoint admin invoca `sync_catalog_from_core`.
2. Adapter obtiene catalogo remoto.
3. Se aplica upsert de Product/Vertical.
4. Se inactivan items retirados segun politica.

Seguridad:
- Solo `owner/admin` puede sincronizar.
- Toda sincronizacion deja traza auditable.

---

## 5. Flujo D: Composicion de producto hibrido

1. Admin define producto con `source_strategy=hybrid_bundle`.
2. Se asocian verticales `provider_kind=core` y `provider_kind=local`.
3. En provision, el adapter ejecuta solo verticales core disponibles.
4. Verticales locales quedan activas aun con core degradado.

Resultado:
- El producto se mantiene vendible aunque una parte del bundle sea local.

---

## 6. Flujo E: Perfil de producto local sin Product Core

1. Admin crea producto con `source_strategy=local_only`.
2. Se registran verticales locales (`provider_kind=local`, sin `external_feature_ref`).
3. Provision crea entitlements locales sin invocar adapter externo.
4. `authorize_feature` evalua entitlements igual que en capacidades core.

Resultado:
- Product Orchestrator funciona autonomamente y permite vender perfiles locales.

---

## 7. Flujo F: Cambio de Plan — Cutover transaccional (Spec corta)

Proposito: describir el corte de datos y recalculo de `Entitlement` cuando un tenant cambia de plan (upgrade/downgrade) sin dejar ventanas de sobre-acceso.

Pasos propuestos:

1. Iniciar cambio de plan en `PaymentsService` o Admin UI con `operation_id` idempotente.
2. Emitir evento `plan.change.requested` con `operation_id`, `tenant_id`, `from_plan`, `to_plan` y `requested_at` (outbox).
3. Orchestrator recoge el evento y crea una transaccion logica:
	- a) Cargar `PlanMatrixVersion` aplicable a `to_plan`.
	- b) Calcular `desired_entitlements` (set target) sin mutar primero.
	- c) Determinar `to_revoke` y `to_grant` comparando con entitlements actuales.
	- d) Marcar la transaccion como `in_progress` y persistir `operation_id` para idempotencia.
4. Aplicar cambios en orden seguro:
	- a) Crear nuevos `Entitlement` (pausados si requieren core provisioning).
	- b) Revocar/pausar entitlements que no aplican al nuevo plan.
	- c) Actualizar cuotas y vigencias de los entitlements existentes.
5. Emitir `plan.change.completed` con `operation_id` y resumen; si falla, emitir `plan.change.failed` y revertir parcialmente siguiendo compensaciones definidas.

Reglas de seguridad:

- Durante transición, las llamadas a `authorize_feature` usan la `deny by default` si existe ambigüedad hasta que la transacción finalice o se establezca `grace_window` controlada.
- Todas las acciones deben ser idempotentes por `operation_id`.

Evidencia y monitoreo:

- Generar eventos `plan.change.*` en Telemetry y registrar actividad en AuditLog.
- Monitor: tasa de revocaciones, errores de provisioning y tiempo de cutover por tenant.

---

## 7. Matriz de degradacion por dependencia

| Dependencia | Estado | Comportamiento |
|---|---|---|
| Payment | no instalada | solo productos demo (`is_demo=true`) |
| Profile | no instalada | bloquea features sensibles |
| Product Core | caido | `503` controlado y opcion demo |
| Telemetry | no instalada | flujo sigue sin reporte central |
| Theme | no instalada | UI neutral sin impacto en autorizacion |

---

## 8. Criterios de aceptacion

- [ ] Flujos de provision/autorizacion/sync documentados con fallback.
- [ ] Errores de negocio estandarizados.
- [ ] Degradacion no rompe disponibilidad base del tenant.
- [ ] Producto hibrido definido con comportamiento de degradacion parcial.
- [ ] Perfil local vendible sin Product Core definido y validable.
