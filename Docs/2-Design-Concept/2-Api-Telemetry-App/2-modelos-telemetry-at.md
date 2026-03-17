# Documento: Modelos de Datos - App Api Telemetry

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** AT-2-MDL
**Ubicacion:** `./Docs/2-Design-Concept/2-Api-Telemetry-App/2-modelos-telemetry-at.md`
**Anchor Docs:** `Docs/1-Core_Concept/2-api-app-cc.md`, `Docs/2-Design-Concept/0-Factory-Saas/15-protocolo-comunicacion-central-fs.md`

---

## 1. Proposito

Definir entidades de telemetria y auditoria que soportan observabilidad end-to-end sin bloquear la operacion transaccional.

---

## 2. Entidad `TelemetryEvent`

**Owner:** App Api/Telemetry
**Schema:** `public`
**Rol:** Evento inmutable de observabilidad emitido por cualquier app.

| Campo | Tipo | Restricciones | Descripcion |
|---|---|---|---|
| `id` | UUID PK | requerido | Identificador unico |
| `event_type` | CharField(100) | indexado | Categoria del evento |
| `tenant_slug` | CharField(63) | indexado | Tenant origen (anonimizable) |
| `app_label` | CharField(50) | indexado | App origen |
| `trace_id` | UUID | indexado | Correlacion distribuida |
| `severity` | CharField(20) | `info/warn/error/critical` | Nivel de evento |
| `payload` | JSONB | sin PII | Datos del evento |
| `created_at` | DateTime | auto | Ocurrencia UTC |
| `sent_at` | DateTime | nullable | Fecha de entrega a La Central |

### Reglas

- Inmutable: no se actualiza payload luego de creado.
- `payload` no puede incluir email, nombre, direccion, telefono ni tokens.

---

## 3. Entidad `PendingMetrics`

**Owner:** App Api/Telemetry
**Schema:** `public`
**Rol:** Buffer de resiliencia para eventos no entregados.

| Campo | Tipo | Restricciones | Descripcion |
|---|---|---|---|
| `id` | BigAutoField PK | requerido | Identificador tecnico |
| `event_id` | UUID | FK logica a TelemetryEvent | Evento asociado |
| `retry_count` | IntegerField | default 0 | Intentos fallidos |
| `next_retry_at` | DateTime | indexado | Proxima reejecucion |
| `last_error` | TextField | nullable | Ultimo error de transporte |
| `created_at` | DateTime | auto | Alta en buffer |

### Reglas

- Solo se purga cuando el evento fue enviado con `201 Created`.
- `retry_count` maximo gobernado por setting (`TELEMETRY_MAX_RETRIES`).

---

## 4. Entidad `AuditLog`

**Owner:** App Api/Telemetry
**Schema:** `public`
**Rol:** Registro inmutable de acciones sensibles para auditoria.

| Campo | Tipo | Restricciones | Descripcion |
|---|---|---|---|
| `id` | UUID PK | requerido | Identificador |
| `action` | CharField(120) | indexado | Accion auditada |
| `actor_id` | IntegerField | nullable | Usuario actor |
| `tenant_slug` | CharField(63) | indexado | Contexto tenant |
| `trace_id` | UUID | indexado | Correlacion |
| `metadata` | JSONB | sin PII sensible | Contexto adicional |
| `created_at` | DateTime | auto | Timestamp UTC |

Eventos minimos: `login`, `change_role`, `change_subscription`, `create_tenant`.

---

## 5. Catalogo minimo de `event_type`

- `tenant.created`
- `tenant.activated`
- `user.login`
- `order.placed`
- `order.fulfilled`
- `subscription.started`
- `subscription.cancelled`
- `support.ticket_opened`
- `error.500`

---

## 6. Relacion con otros documentos

| Documento | Relacion |
|---|---|
| `Docs/2-Design-Concept/0-Factory-Saas/15-protocolo-comunicacion-central-fs.md` | Modelo Push/Pull y buffer de resiliencia |
| `Docs/2-Design-Concept/0-Factory-Saas/18-matriz-seguridad-compliance-fs.md` | Restriccion de payload sin PII |
| `Docs/2-Design-Concept/0-Factory-Saas/17-diccionario-datos-logico-fs.md` | Diccionario logico global |

---

## 7. Criterios de aceptacion

- [ ] `TelemetryEvent`, `PendingMetrics` y `AuditLog` definidos como inmutables funcionales.
- [ ] `payload` sin PII y con validacion de esquema.
- [ ] `trace_id` presente en todas las entidades de trazabilidad.
