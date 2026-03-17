# Documento: Matriz de Trazabilidad - App Profile

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PR-6-TRA
**Ubicacion:** `./Docs/2-Design-Concept/3-Profile-App/6-matriz-trazabilidad-profile-pr.md`
**Anchor Docs:** `Docs/1-Core_Concept/3-profile-app-cc.md`, `Docs/2-Design-Concept/0-Factory-Saas/13-router-dinamico-esquemas-fs.md`

---

## 1. Proposito

Asegurar trazabilidad entre requerimientos de identidad/tenancy y artefactos de diseno Profile.

---

## 2. Matriz Requerimiento -> Diseno -> Evidencia

| Req ID | Requerimiento | Documento | Evidencia |
|---|---|---|---|
| PR-R01 | Gestion de identidad global multi-tenant | `2-modelos-profile-pr.md` | User/Tenant/Membership en `public` |
| PR-R02 | Preferencias por tenant | `2-modelos-profile-pr.md` | `Profile` en schema tenant |
| PR-R03 | Cambio seguro de tenant | `3-service-selector-contratos-profile-pr.md` | `switch_tenant` con validacion membership |
| PR-R04 | Dashboard por composicion | `5-dashboard-fallback-composition-profile-pr.md` | Secciones opcionales por soft-dependency |
| PR-R05 | Fallback sin Theme | `5-dashboard-fallback-composition-profile-pr.md` | `dashboard_basic.html` |
| PR-R06 | Seguridad RBAC | `4-views-endpoints-middleware-profile-pr.md` | Restriccion owner/admin en acciones sensibles |
| PR-R07 | Aislamiento de tenant | `4-views-endpoints-middleware-profile-pr.md` | Integracion con tenant middleware/router |
| PR-R08 | Dashboard muestra productos comprados | `5-dashboard-fallback-composition-profile-pr.md` | Seccion `products` con fallback `[]` |
| PR-R09 | Dashboard muestra cupones y descuentos | `5-dashboard-fallback-composition-profile-pr.md` | Seccion `coupons/discounts` con fallback `[]` |
| PR-R10 | Dashboard muestra pagos realizados | `5-dashboard-fallback-composition-profile-pr.md` | Seccion `payments` con fallback `[]` |
| PR-R11 | Dashboard aplica color themes | `3-service-selector-contratos-profile-pr.md` | `theme_tokens` o `DEFAULT_THEME_TOKENS` |

---

## 3. Criterios de aceptacion

- [ ] PR-R01..PR-R11 trazados a artefactos concretos.
- [ ] Evidencia de cada requerimiento definida para Sprint Review.
- [ ] Sin huecos entre Core y Design.

## 4. Cobertura obligatoria DC-12/DC-13/DC-16/DC-17

- DC-12 (patron service layer): cubierto en `3-service-selector-contratos-profile-pr.md`.
- DC-13 (router dinamico y contexto tenant): cubierto por `switch_tenant` y middleware de aislamiento.
- DC-16 (contratos inter-app): cubierto por contratos para dashboard/composicion con apps consumidoras.
- DC-17 (diccionario de datos logico): cubierto por entidades globales (`User`, `Tenant`, `Membership`) y `Profile` por schema tenant.
