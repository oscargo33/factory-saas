# Documento: Service, Selector y Contratos - App Api Telemetry

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** AT-3-SVC
**Ubicacion:** `./Docs/2-Design-Concept/2-Api-Telemetry-App/3-service-selector-contratos-telemetry-at.md`
**Anchor Docs:** `Docs/1-Core_Concept/2-api-app-cc.md`, `Docs/2-Design-Concept/0-Factory-Saas/12-patron-service-layer-fs.md`

---

## 1. Proposito

Definir interfaces publicas de telemetria para captura de eventos inter-app y lectura agregada para inspeccion externa.

---

## 2. Services publicos (escritura)

| Funcion | Firma | Efecto |
|---|---|---|
| `record_event` | `(event_type: str, app_label: str, tenant_slug: str, payload: dict, severity='info', trace_id=None) -> UUID` | Persiste `TelemetryEvent` |
| `record_audit` | `(action: str, tenant_slug: str, actor_id: int | None, metadata: dict, trace_id=None) -> UUID` | Persiste `AuditLog` |
| `queue_pending_metric` | `(event_id: UUID, error: str, next_retry_at: datetime) -> None` | Alta/actualiza `PendingMetrics` |
| `flush_pending_metrics` | `(batch_size: int = 500) -> dict` | Envia lote a La Central |

Reglas:
- Todos los services de escritura son atomicos.
- Errores de transporte no se propagan a app consumidora (fail-soft).

---

## 3. Selectors publicos (lectura)

| Funcion | Firma | Retorna |
|---|---|---|
| `get_health_snapshot` | `(tenant_slug: str | None = None) -> dict` | Estado tecnico y colas pendientes |
| `get_business_snapshot` | `(tenant_slug: str | None = None, since=None) -> dict` | KPI agregados de negocio |
| `get_pending_metrics_count` | `() -> int` | Eventos no entregados |

---

## 4. Contratos inter-app

Version inicial: `telemetry.contract.v1`

| Contrato | Tipo | Payload entrada | Payload salida |
|---|---|---|---|
| `telemetry.record_event.v1` | Service | `{event_type, app_label, tenant_slug, payload, severity, trace_id}` | `{event_id}` |
| `telemetry.record_audit.v1` | Service | `{action, tenant_slug, actor_id, metadata, trace_id}` | `{audit_id}` |
| `telemetry.health_snapshot.v1` | Selector | `{tenant_slug?}` | `{status, latency_ms, pending_count, ...}` |
| `telemetry.business_snapshot.v1` | Selector | `{tenant_slug?, since?}` | `{orders_total, revenue_total, tickets_open, ...}` |

Fallback si Telemetry no instalado:
- Las apps consumidoras registran log local y continúan flujo principal.
- Retorno neutral: `{event_id: null}` o estructura vacia no bloqueante.

---

## 5. Seguridad contractual

- `payload` de entrada validado contra schema permitido por `event_type`.
- Rechazo de PII por lista de campos prohibidos.
- `trace_id` requerido para eventos de severidad `error` o `critical`.

---

## 6. Criterios de aceptacion

- [ ] Contratos v1 versionados y documentados.
- [ ] Ninguna app consumidora requiere import de modelos telemetry.
- [ ] Fallback no bloqueante definido para ausencia de telemetry.
