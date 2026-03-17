# Documento: NFR, Seguridad y Operacion - App Product Orchestrator

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PO-7-NFR
**Ubicacion:** `./Docs/2-Design-Concept/4-Product-Orchestrator-App/7-nfr-seguridad-operacion-product-orchestrator-po.md`
**Anchor Docs:** `Docs/2-Design-Concept/0-Factory-Saas/18-matriz-seguridad-compliance-fs.md`, `Docs/2-Design-Concept/0-Factory-Saas/11-configuracion-redis-celery-fs.md`

---

## 1. NFR de rendimiento

| NFR | Objetivo |
|---|---|
| Latencia autorizacion | p95 <= 120ms sin llamada externa |
| Latencia catalogo | p95 <= 250ms con cache local |
| Provision sincrono | p95 <= 900ms (si Product Core saludable) |
| Disponibilidad | >= 99.5% mensual para `authorize_feature` |

---

## 2. NFR de resiliencia

| NFR | Objetivo |
|---|---|
| Error budget core externo | fallback operativo sin caida total |
| Reintentos | max 2 reintentos con backoff exponencial |
| Circuit breaker | apertura ante 5xx repetidos del Product Core |
| Degradacion controlada | modo demo para features elegibles |

---

## 3. Seguridad

- Tenant isolation obligatorio en toda consulta de Product/Vertical/Entitlement.
- RBAC minimo:
  - `member+`: lectura de catalogo/estado.
  - `admin+`: provision/sync.
  - `owner/admin`: revocacion.
- No exponer secretos ni payloads sensibles en respuestas.
- Auditoria obligatoria para provision/revocacion/sync.
- No registrar PII innecesaria en telemetria.

---

## 4. Operacion y observabilidad

Metricas recomendadas:
- `orchestrator_authorize_total{result}`
- `orchestrator_provision_total{source,result}`
- `orchestrator_core_latency_ms`
- `orchestrator_core_error_total{code}`

Alertas recomendadas:
- tasa de denegacion > umbral esperado por tenant.
- errores 5xx del core externo por encima de baseline.
- aumento anomalo en revocaciones.

Runbook minimo:
- revisar salud adapter.
- verificar cola/eventos de provision.
- activar temporalmente politica demo si aplica.

---

## 6. Pricing, Versioning y Patrón Idempotency/Outbox (Spec corta)

Propósito: definir reglas mínimas para snapshot de precios en checkout, versionado de tarifas y evitar provisiones/cobros duplicados.

Pricing/versioning:

- `price_snapshot` por `order_line` al momento de checkout: captura `product_id`, `price`, `currency`, `price_version_id`, `applied_taxes`.
- Mantener `PriceCatalog` versionado con `price_version_id` y fecha de vigencia.
- Renovaciones y reembolsos deben referenciar el `price_snapshot` original para consistencia contable.

Idempotency / Outbox pattern:

- Todas las operaciones críticas (webhook de pago, provision_tenant, sync_catalog) deben recibir/emitir un `operation_id` idempotente.
- Implementar Outbox (tabla `outbox_events`) para persistir eventos de negocio dentro de la misma transacción que las mutaciones del modelo y publicarlos de forma reliably por worker.
- Consumers usan deduplicacion por `operation_id` y status (`pending|sent|failed`).

Reconciliación y seguridad:

- Reconciliación periódica entre `outbox_events` y la cola externa para asegurar idempotencia y entrega (exponiendo métricas `outbox_pending_count`).
- En caso de doble provisión detectada, usar `operation_id` para revertir o consolidar y generar `audit` con causa.

Evidencia operativa:

- Métricas: `provisioning_idempotency_conflicts_total`, `outbox_pending_count`, `price_snapshot_mismatch_total`.

---

## 5. Criterios de aceptacion

- [ ] NFR cuantificados para latencia/disponibilidad/resiliencia.
- [ ] Controles de seguridad por tenant y rol definidos.
- [ ] Metricas, alertas y runbook base documentados.
