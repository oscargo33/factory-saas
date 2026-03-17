# Documento: Endpoints y Middleware - App Api Telemetry

**ID:** AT-4-API
**Ubicacion:** `./Docs/2-Design-Concept/2-Api-Telemetry-App/4-endpoints-middleware-telemetry-at.md`
**Anchor Docs:** `Docs/1-Core_Concept/2-api-app-cc.md`, `Docs/2-Design-Concept/0-Factory-Saas/15-protocolo-comunicacion-central-fs.md`

---

## 1. Proposito

Definir la superficie HTTP de telemetria para modo Pull y el middleware de trazabilidad transversal.

---

## 2. Middleware `TelemetryTraceMiddleware`

Responsabilidades:
- Resolver `X-Trace-ID` de entrada o generarlo (`uuid4`).
- Inyectar `trace_id` en contexto de request y en respuesta.
- Medir `request_duration_ms` para metricas de salud.

Flujo:
1. Leer `X-Trace-ID` de headers.
2. Si falta, generar UUID.
3. Adjuntar `request.trace_id`.
4. Ejecutar request.
5. Adjuntar `X-Trace-ID` a response.
6. Publicar evento tecnico si duracion excede umbral.

---

## 3. Endpoints Pull (DRF)

Prefijo: `/api/telemetry/`

| Metodo | Endpoint | Auth | Respuesta |
|---|---|---|---|
| `GET` | `/ping/` | Publico | `{"status":"ok","version":"x.y.z"}` |
| `GET` | `/inspect/` | `X-Factory-Token` | Snapshot de salud y negocio |
| `GET` | `/events/` | `X-Factory-Token` | Eventos recientes filtrables |

Filtros sugeridos en `/events/`:
- `tenant_slug`
- `app_label`
- `severity`
- `since`
- `limit`

---

## 4. Seguridad de endpoints

- `inspect` y `events` requieren `X-Factory-Token` valido.
- Rate limit por IP y por token.
- Respuestas sin PII por defecto.
- Logging de acceso con `trace_id`.

Codigos esperados:
- `200` ok
- `401` token faltante/invalido
- `403` token sin permisos
- `429` rate limit

---

## 5. Degradacion graciosa

Si App Telemetry no esta instalada:
- Endpoints no registrados (404 controlado).
- Apps consumidoras no se bloquean: solo log local.

Si esta instalada pero La Central no responde:
- Endpoints Pull siguen operativos localmente.
- Push pasa a modo buffer (`PendingMetrics`).

---

## 6. Criterios de aceptacion

- [ ] Todo request/respuesta incluye `X-Trace-ID`.
- [ ] Endpoints Pull protegidos por token excepto `/ping/`.
- [ ] Ningun endpoint expone PII en payload por defecto.
