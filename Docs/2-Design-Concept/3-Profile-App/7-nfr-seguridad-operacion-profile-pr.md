# Documento: NFR, Seguridad y Operacion - App Profile

**ID:** PR-7-NFR
**Ubicacion:** `./Docs/2-Design-Concept/3-Profile-App/7-nfr-seguridad-operacion-profile-pr.md`
**Anchor Docs:** `Docs/2-Design-Concept/0-Factory-Saas/18-matriz-seguridad-compliance-fs.md`, `Docs/2-Design-Concept/0-Factory-Saas/13-router-dinamico-esquemas-fs.md`

---

## 1. Proposito

Definir requerimientos no funcionales de Profile para login/contexto tenant robusto y seguro.

---

## 2. NFR de rendimiento

| NFR ID | Objetivo | Meta |
|---|---|---|
| PR-NFR-01 | Resolucion de contexto activo | p95 < 80 ms |
| PR-NFR-02 | Cambio de tenant | p95 < 150 ms |
| PR-NFR-03 | Dashboard composicion parcial | p95 < 250 ms |

---

## 3. NFR de disponibilidad

| NFR ID | Objetivo | Regla |
|---|---|---|
| PR-NFR-04 | Falla de Theme | Profile sigue operativo con fallback |
| PR-NFR-05 | Falla de Orders/Support | Dashboard sigue operativo con secciones vacias |
| PR-NFR-06 | Aislamiento tenant | Cero fugas cross-tenant |

---

## 4. Seguridad

| Control | Aplicacion |
|---|---|
| RBAC | Validacion por membership role |
| Tenant boundary | Todas las lecturas tenant-aware |
| Auditabilidad | Eventos sensibles a AuditLog/Telemetry |
| PII | Minimizar exposicion en respuestas publicas |

---

## 5. Operacion y monitoreo

Metricas minimas:
- `profile_active_context_latency_ms`
- `profile_switch_tenant_total`
- `profile_switch_tenant_denied_total`
- `profile_dashboard_partial_render_total`

Alertas sugeridas:
- incrementos de `denied_total` > umbral
- errores de contexto tenant > 1% en 10 min

---

## 6. Criterios de aceptacion

- [ ] NFR definidos con metas medibles.
- [ ] Controles RBAC y tenant boundary documentados.
- [ ] Metrica y alertas operativas definidas.
