# Documento: NFR, Seguridad y Operación - App Theme

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** TH-7-NFR
**Ubicación:** `./Docs/2-Design-Concept/1-Theme-App/7-nfr-seguridad-operacion-theme-th.md`
**Anchor Docs:** `Docs/2-Design-Concept/0-Factory-Saas/18-matriz-seguridad-compliance-fs.md`, `Docs/2-Design-Concept/0-Factory-Saas/14-pipeline-tailwind-cotton-fs.md`

---

## 1. Propósito

Definir requerimientos no funcionales (NFR) para App Theme en rendimiento, seguridad, disponibilidad y operación.

---

## 2. NFR de rendimiento

| NFR ID | Objetivo | Meta |
|---|---|---|
| TH-NFR-01 | Lectura de tokens de tema | p95 < 25 ms (cache hit) |
| TH-NFR-02 | Resolución de traducción por key | p95 < 40 ms (cache hit) |
| TH-NFR-03 | Latencia en fallback DB | p95 < 120 ms |
| TH-NFR-04 | Fallo de proveedor externo | No bloquear render de UI |

---

## 3. NFR de disponibilidad

| NFR ID | Objetivo | Regla |
|---|---|---|
| TH-NFR-05 | Degradación segura | Sin Theme, app consumidora mantiene operación |
| TH-NFR-06 | Modo no saludable | Defaults visuales + texto neutral |
| TH-NFR-07 | Compatibilidad | Product Core debe renderizar con tokens o fallback |

---

## 4. Seguridad

| Control | Aplicación |
|---|---|
| Validación de payload | Sanitizar tokens CSS y entradas de glosario |
| Prevención XSS | No interpolar HTML sin escape en traducciones |
| Control de acceso | Endpoints internos protegidos por rol |
| PII | Traducciones no deben almacenar datos personales |

---

## 5. Operación y monitoreo

Métricas mínimas:
- `theme_tokens_cache_hit_ratio`
- `theme_translation_cache_hit_ratio`
- `theme_translation_fallback_db_total`
- `theme_translation_fallback_provider_total`
- `theme_provider_errors_total`

Alertas sugeridas:
- Cache hit ratio < 80% en 15 min.
- Errores del proveedor de traducción > 10% en 10 min.
- Más de 100 claves faltantes por hora.

---

## 6. Criterios de aceptación

- [ ] NFR de rendimiento definidos con métricas p95.
- [ ] Modo degradado probado para ausencia/no salud de Theme.
- [ ] Controles de seguridad de traducción y tokens documentados.
- [ ] Métricas operativas y umbrales de alerta definidos.
