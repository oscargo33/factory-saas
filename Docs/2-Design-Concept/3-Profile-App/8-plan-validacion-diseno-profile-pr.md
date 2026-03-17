# Documento: Plan de Validacion de Diseno - App Profile

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PR-8-VAL
**Ubicacion:** `./Docs/2-Design-Concept/3-Profile-App/8-plan-validacion-diseno-profile-pr.md`
**Anchor Docs:** `Docs/2-Design-Concept/3-Profile-App/1-checklist-profile-app.md`, `Docs/2-Design-Concept/3-Profile-App/6-matriz-trazabilidad-profile-pr.md`

---

## 1. Proposito

Definir validacion de diseno Profile para asegurar que identidad/tenancy y dashboard degradan de forma segura.

---

## 2. Escenarios de validacion (diseno)

| Caso | Objetivo | Evidencia esperada |
|---|---|---|
| PR-VAL-01 | Usuario multi-tenant | `get_user_tenants` retorna membresias correctas |
| PR-VAL-02 | Cambio tenant autorizado | `switch_tenant` exitoso con pertenencia activa |
| PR-VAL-03 | Cambio tenant no autorizado | Respuesta `403` |
| PR-VAL-04 | Theme no instalado | `dashboard_basic.html` renderizado |
| PR-VAL-05 | Product-Orchestrator faltante | `products=[]` sin error |
| PR-VAL-06 | Marketing faltante | `coupons/discounts=[]` sin error |
| PR-VAL-07 | Payment faltante | `payments=[]` sin error |
| PR-VAL-08 | Orders/Support faltantes | Dashboard parcial sin error |
| PR-VAL-09 | Theme no saludable | `theme_tokens` default + fallback visual |
| PR-VAL-10 | Aislamiento tenant | No lectura de datos de otro schema |

---

## 3. Evidencia minima para Sprint Review

- Matriz PR-R01..PR-R11 validada.
- Checklist PR completo por secciones A..G.
- Simulaciones de degradacion y de seguridad tenant.
- Evidencia de cumplimiento NFR PR.

---

## 4. Criterios de aceptacion

- [ ] Casos PR-VAL-01..PR-VAL-10 con evidencia.
- [ ] Sin brechas entre trazabilidad y validacion.
- [ ] App Profile lista para pasar de diseno a implementacion.
