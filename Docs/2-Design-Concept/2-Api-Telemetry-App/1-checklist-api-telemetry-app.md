# Checklist de Diseno - App 2 Api Telemetry

**ID:** AT-1-CK
**Ubicacion:** `./Docs/2-Design-Concept/2-Api-Telemetry-App/1-checklist-api-telemetry-app.md`
**Anchor Doc:** `Docs/1-Core_Concept/2-api-app-cc.md`
**Estado:** v1.0

---

## Control de Versiones

| Version | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | 2026-03-15 | Arq. IA (GitHub Copilot) | Creacion inicial del paquete de diseno Api/Telemetry |

---

## Bloques de diseno

### A. Modelo de datos

- [x] Definicion de `TelemetryEvent` inmutable.
- [x] Definicion de `PendingMetrics` como buffer de resiliencia.
- [x] Definicion de `AuditLog` para eventos sensibles.

### B. Service/Selector

- [x] Contratos de captura de eventos para apps consumidoras.
- [x] Contratos de lectura agregada para endpoints Pull.
- [x] Contratos de envio Push con firma y trazabilidad.

### C. Middleware y endpoints

- [x] Diseno de middleware para `X-Trace-ID`.
- [x] Diseno de endpoints Pull (`inspect`, `ping`).
- [x] Reglas de autenticacion con `X-Factory-Token`.

### D. Operacion y resiliencia

- [x] Push periodico con Celery (cola `telemetry`).
- [x] Retry con backoff exponencial y jitter.
- [x] Fail-soft: no bloquear flujo principal del SaaS.

### E. Seguridad y cumplimiento

- [x] Definicion de payload sin PII.
- [x] Rotacion/TTL de JWT saliente.
- [x] Retencion y purga de metricas.

---

## Criterio de Cierre (Diseno App 2)

- [ ] Todos los documentos AT-2 a AT-5 aprobados por revision arquitectonica.
- [ ] Trazabilidad completa a DC-11, DC-15, DC-18.
- [ ] Contratos publicos versionados y publicados en DC-16.
