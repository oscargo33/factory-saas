# EPI-002 — API / Telemetry: El Sistema Nervioso y el Ojo de La Central

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** EPI-002
**Tipo:** ADN Epic — Capa 1, conciencia operativa del sistema
**Prioridad:** 1 — Paralelo con EPI-001 en Sprint-1
**Sprint objetivo:** Sprint-1
**Dependencias:** EPI-000 Done, EPI-CORE Done
**Blueprints fuente:**
- `Docs/1-Core_Concept/2-api-app-cc.md`
- `Docs/2-Design-Concept/2-Api-Telemetry-App/` (11 documentos)

---

## § 1 — EL ALMA: Visión y Razón de Existir

### ¿Qué Problema Resuelve?

Un SaaS multi-tenant sin observabilidad es una caja negra. El operador no sabe cuántas ventas hay, cuántos errores ocurren, qué tenant está teniendo problemas ahora mismo. Si algo falla a las 3 AM, ¿cómo lo sabes antes de que lo reporte el cliente?

EPI-002 construye el **sistema nervioso del SaaS**: cada request tiene un `X-Trace-ID` único que permite rastrear exactamente qué pasó en toda la cadena de ejecución. Las métricas de ventas, tickets y salud técnica se envían periódicamente a **La Central** (sistema externo de monitoreo del operador). Si La Central no está disponible, los datos se acumulan en un buffer local y se envían cuando regresa.

### La Promesa

Cuando un cliente llama diciendo "mi orden no procesó", el operador puede buscar el `X-Trace-ID` del request en La Central y ver exactamente: qué tenant era, qué endpoint se llamó, cuánto tardó, qué error se lanzó, en qué línea del código. Sin adivinar.

### Por Qué Es Opcional pero Imprescindible

La app se puede desinstalar (`apps.is_installed('apps.api')` = False) y el SaaS sigue funcionando — los services de las demás apps tienen fallbacks locales. Pero en producción, operar sin telemetría es operar a ciegas.

---

## § 2 — LA FILOSOFÍA: Principios Fundacionales Aplicados

| Principio | Cómo se aplica en EPI-002 |
|---|---|
| **Degradación Graciosa** | Si La Central no responde → métricas en `PendingMetrics`. Si Telemetry no está instalado → apps continúan con logs locales. |
| **Aislamiento Total** | `TelemetryEvent` y `PendingMetrics` viven en schema del tenant respectivo. Métricas de un tenant no contaminan las de otro. |
| **Service/Selector** | `record_event` es un service (escribe `TelemetryEvent`). `get_health_status` es un selector (lectura pura para La Central). |
| **Auditoría Inmutable** | `TelemetryEvent` es append-only. No se puede modificar ni borrar un evento registrado. |

---

## § 3 — LA ARQUITECTURA: Lo Que EPI-002 Crea

### Estructura de Archivos

```
apps/api/
├── models.py          ← TelemetryEvent (inmutable), PendingMetrics (buffer), AuditLog
├── services.py        ← record_event, flush_pending_metrics, record_audit
├── selectors.py       ← get_health_status, get_metrics_for_period, get_audit_trail
├── middleware.py      ← TelemetryMiddleware: X-Trace-ID por request, latencia
├── tasks.py           ← push_metrics_to_central (Celery periódico cada 5min)
├── managers.py        ← AppHealthManager (queries de reportes de salud)
├── api/               ← Endpoints DRF para consultas pull de La Central
│   ├── serializers.py
│   ├── views.py       ← health_check, metrics, audit_trail (auth por token)
│   └── urls.py
├── exceptions.py      ← TelemetryError, CentralUnavailableError
├── migrations/
│   └── 0001_initial.py
└── tests/
    ├── test_middleware.py
    ├── test_services.py
    └── test_push_task.py
```

### Modelos de Datos

**`TelemetryEvent`** (append-only, schema: `tenant_{slug}`)
| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID PK | — |
| `trace_id` | CharField(36) | UUID del X-Trace-ID del request origen |
| `event_type` | CharField(60) | `order.created`, `payment.confirmed`, `support.ticket.opened` |
| `tenant_slug` | CharField(63) | tenant propietario del evento |
| `user_id` | IntegerField null | usuario que originó el evento (si aplica) |
| `payload` | JSONB | datos del evento específico |
| `severity` | CharField(10) | `info`, `warning`, `error` |
| `recorded_at` | DateTime | auto, no editable |

**`PendingMetrics`** (buffer local cuando La Central no está disponible)
| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID PK | — |
| `tenant_slug` | CharField(63) | — |
| `period_start` | DateTime | inicio del período agregado |
| `period_end` | DateTime | fin del período |
| `metrics_payload` | JSONB | métricas de ventas, tickets, health |
| `retry_count` | IntegerField | intentos de envío fallidos |
| `next_retry_at` | DateTime | próximo intento (exponential backoff) |

### Protocolo Push/Pull con La Central

**Modo PUSH (Celery beat, cada 5min):**
```
Celery task: push_metrics_to_central()
  → agregar TelemetryEvents del período
  → POST https://central.factory.io/api/v1/metrics/ {payload, tenant_slug, signed_hash}
  → si 200 OK: borrar PendingMetrics del período
  → si error: guardar en PendingMetrics + schedule retry (backoff: 5min → 15min → 60min)
```

**Modo PULL (DRF endpoints, auth por token de La Central):**
```
GET /api/telemetry/health/          → estado actual del tenant (DB latency, error rate, active users)
GET /api/telemetry/metrics/?from=&to= → métricas del período solicitado
GET /api/telemetry/audit/?limit=100 → trail de auditoría de acciones sensibles
```

### TelemetryMiddleware

```python
class TelemetryMiddleware:
    def __call__(self, request):
        trace_id = request.headers.get('X-Trace-ID', str(uuid.uuid4()))
        request.trace_id = trace_id
        start = time.monotonic()
        response = self.get_response(request)
        duration_ms = (time.monotonic() - start) * 1000
        response['X-Trace-ID'] = trace_id
        # Record request telemetry asíncronamente (no bloquea response)
        record_request_event.delay(trace_id, request.path, response.status_code, duration_ms)
        return response
```

---

## § 4 — EL ÁRBOL: User Stories de Cimientos a Acabados

| US ID | Historia | SP | Sprint | Estado |
|---|---|---|---|---|
| US-002-01 | `TelemetryEvent` model + `TelemetryMiddleware` (X-Trace-ID) | 3 | Sprint-1 | 🔲 Sin US file |
| US-002-02 | `PendingMetrics` + push task Celery + retry backoff | 4 | Sprint-1 | 🔲 Sin US file |
| US-002-03 | DRF endpoints pull: health, metrics, audit trail | 3 | Sprint-1 | 🔲 Sin US file |
| US-002-04 | `AuditLog` service para acciones sensibles (login, pago, cambio de plan) | 2 | Sprint-2 | 🔲 Sin US file |

---

## § 5 — BLUEPRINTS DE REFERENCIA

| ID | Documento | Qué gobierna |
|---|---|---|
| CC-2 | `Docs/1-Core_Concept/2-api-app-cc.md` | Visión, protocolo Push/Pull, resiliencia |
| AT-2 | `2-Api-Telemetry-App/2-modelos-telemetry-at.md` | Modelos exactos |
| AT-3 | `2-Api-Telemetry-App/3-service-selector-contratos-telemetry-at.md` | Contratos públicos |
| AT-4 | `2-Api-Telemetry-App/4-endpoints-middleware-telemetry-at.md` | DRF endpoints y middleware |
| AT-5 | `2-Api-Telemetry-App/5-push-pull-resiliencia-telemetry-at.md` | Protocolo de resiliencia |
| DC-15 | `0-Factory-Saas/15-protocolo-comunicacion-central-fs.md` | Protocolo de comunicación con La Central |

---

## § 6 — DEFINITION OF DONE

EPI-002 está Done cuando:

- [ ] Todo request HTTP tiene `X-Trace-ID` en response headers (verificable en browser DevTools)
- [ ] `record_event("order.created", tenant_slug, payload)` crea un `TelemetryEvent` inmutable
- [ ] Si La Central responde 500 → métricas guardadas en `PendingMetrics` y retry programado
- [ ] `GET /api/telemetry/health/` con token válido retorna estado de salud del tenant
- [ ] `GET /api/telemetry/health/` sin token retorna 401
- [ ] Con Telemetry desinstalado (`INSTALLED_APPS` sin `apps.api`) → ninguna otra app rompe
- [ ] `pytest apps/api/` pasa: middleware, push task, retry logic
- [ ] `product-backlog.md` actualizado: US-002-01..04 con estados correctos
