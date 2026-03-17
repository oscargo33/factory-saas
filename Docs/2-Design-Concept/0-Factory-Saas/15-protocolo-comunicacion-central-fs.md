# Documento: 15-protocolo-comunicacion-central-fs.md

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** DC-15-FS
**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/15-protocolo-comunicacion-central-fs.md`
**Referencia Core:** `0-factory_saas-cc.md`
**Capa:** 7 — Telemetría y Control de La Central
**Apellido:** **-fs**

---

## 1. Propósito

La Capa 7 define el **protocolo de comunicación** entre una instancia de Factory-SaaS desplegada (un "Satélite") y el servidor maestro de monitoreo (**La Central**). La Central es el sistema que agrega métricas de todas las instancias Factory desplegadas para ofrecer visibilidad de negocio, salud del sistema, y telemetría de uso.

---

## 2. Modelo de Comunicación: Push + Pull

La Factory usa un modelo dual para maximizar la resiliencia:

| Modo | Dirección | Frecuencia | Canal |
|---|---|---|---|
| **Push** | Satélite → La Central | Cada 5 min (configurable) | HTTPS POST con JWT |
| **Pull** | La Central → Satélite | On-demand | HTTPS GET con token de API |

### 2.1. Modo Push (Batch de Telemetría)

La tarea Celery `telemetry.push_metrics` (cola `telemetry`) agrega un lote de `TelemetryEvent` y los envía a La Central. Si La Central no está disponible, los eventos se acumulan en la tabla buffer `PendingMetrics` hasta el siguiente intento.

```
Celery Beat (cada 5 min)
    │
    ▼
telemetry.push_metrics task
    │
    ├── 1. SELECT eventos pendientes de PendingMetrics (últimos 5 min)
    ├── 2. Serializar en TelemetryBatch (JSON)
    ├── 3. POST https://central.factory.com/api/v1/ingest/ (con JWT)
    │        │
    │        ├── 201 Created → marcar eventos como enviados, limpiar buffer
    │        └── 5xx / timeout → dejar en buffer, retry con backoff exponencial
    │
    └── 4. Log resultado en audit log
```

### 2.2. Modo Pull (Inspección On-Demand)

La Central puede consultar el estado actual de la instancia en cualquier momento:

| Endpoint DRF | Método | Autenticación | Respuesta |
|---|---|---|---|
| `/api/telemetry/inspect/` | `GET` | Token de API (`X-Factory-Token`) | JSON con métricas de salud |
| `/api/telemetry/ping/` | `GET` | Ninguno | `{"status": "ok", "version": "x.y.z"}` |

---

## 3. Modelo de Datos: `TelemetryEvent`

Cada evento es una unidad de telemetría atómica registrada por cualquier app de la Factory:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID | Identificador único del evento |
| `event_type` | `str` | Categoría del evento (ver tabla de tipos) |
| `tenant_slug` | `str` | Tenant que generó el evento (anonimizable) |
| `app_label` | `str` | App de origen (`orders`, `payments`, etc.) |
| `payload` | JSONB | Datos específicos del evento (sin PII) |
| `created_at` | `datetime` | Timestamp UTC de ocurrencia |
| `sent_at` | `datetime | null` | Cuándo fue enviado a La Central |

### 3.1. Catálogo de Tipos de Evento

| `event_type` | Origen | Descripción |
|---|---|---|
| `tenant.created` | Core | Nuevo tenant registrado |
| `tenant.activated` | Core | Tenant activó su cuenta |
| `subscription.started` | Payments | Suscripción inició |
| `subscription.cancelled` | Payments | Suscripción cancelada |
| `order.placed` | Orders | Pedido creado |
| `order.fulfilled` | Orders | Pedido completado |
| `support.ticket_opened` | Support | Ticket de soporte creado |
| `user.login` | Core | Sesión de usuario iniciada |
| `error.500` | Core | Error interno registrado |

---

## 4. Modelo `PendingMetrics` (Buffer de Resiliencia)

Tabla en el esquema `public` que actúa como buffer cuando La Central no está disponible:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | `BigAutoField` | PK |
| `event_id` | UUID | FK a `TelemetryEvent.id` |
| `retry_count` | `int` | Número de intentos fallidos |
| `next_retry_at` | `datetime` | Próximo intento (backoff exponencial) |
| `error_message` | `str` | Último mensaje de error del intento |

---

## 5. Seguridad del Canal

### 5.1. Autenticación Saliente (Push)

- La instancia Satélite se identifica con un **JWT firmado** (HS256 o RS256) que contiene el `instance_id` y la firma con el `CENTRAL_SECRET` almacenado en secretos (DC-3).
- El JWT tiene TTL de 60 segundos para limitar ventana de replay.
- Header de la petición: `Authorization: Bearer {jwt_token}`.

### 5.2. Autenticación Entrante (Pull)

- La Central presenta un `X-Factory-Token` pre-compartido para acceder al endpoint `/api/telemetry/inspect/`.
- El token se almacena como secreto en la instancia y nunca en el código.

### 5.3. Header de Trazabilidad

Todas las peticiones hacia La Central incluyen el header:
```
X-Trace-ID: {uuid4}
```
El mismo `X-Trace-ID` es registrado en el log de la instancia para correlación de eventos frente a reportes de La Central.

### 5.4. Seguridad de Datos

- El campo `payload` nunca contiene **PII** (nombre, email, dirección). Solo IDs, contadores y flags.
- El campo `tenant_slug` puede ser anonimizado (`SHA-256` del slug) para instancias con política de privacidad estricta, controlado por el setting `TELEMETRY_ANONYMIZE_TENANT`.

---

## 6. Configuración

| Setting | Default | Descripción |
|---|---|---|
| `TELEMETRY_ENABLED` | `True` | Habilitar/deshabilitar telemetría |
| `TELEMETRY_PUSH_INTERVAL` | `300` | Segundos entre envíos push |
| `TELEMETRY_MAX_BATCH_SIZE` | `500` | Máximo eventos por batch |
| `CENTRAL_API_URL` | (requerido) | URL base de La Central |
| `CENTRAL_SECRET` | (requerido) | Clave para firmar JWT |
| `TELEMETRY_ANONYMIZE_TENANT` | `False` | Anonimizar slug del tenant |

---

## 7. Relación con Otros Documentos

| Documento | Relación |
|---|---|
| DC-3 `3-gestion-de-secretos-fs.md` | `CENTRAL_SECRET` y `X-Factory-Token` son secretos gestionados aquí |
| DC-11 `11-configuracion-redis-celery-fs.md` | La tarea `telemetry.push_metrics` corre en la cola `telemetry` |
| DC-12 `12-patron-service-layer-fs.md` | Las apps registran eventos usando `telemetry_service.record_event()` |
| DC-18 `18-matriz-seguridad-compliance-fs.md` | Requisito de no incluir PII en telemetría |

---

## 8. Criterios de Aceptación del Diseño

- [ ] El buffer `PendingMetrics` garantiza que no se pierden eventos si La Central está caída.
- [ ] El JWT del push tiene TTL ≤ 60 segundos.
- [ ] El payload de `TelemetryEvent` no contiene ningún campo PII.
- [ ] `TELEMETRY_ENABLED = False` deshabilita completamente el push sin errores.
- [ ] El header `X-Trace-ID` es generado y registrado en cada petición saliente.
- [ ] El endpoint de pull requiere autenticación; acceso sin token retorna `403`.
