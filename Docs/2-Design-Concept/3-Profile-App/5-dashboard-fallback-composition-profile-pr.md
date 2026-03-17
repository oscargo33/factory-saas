# Documento: Dashboard, Composicion y Fallback - App Profile

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PR-5-UI
**Ubicacion:** `./Docs/2-Design-Concept/3-Profile-App/5-dashboard-fallback-composition-profile-pr.md`
**Anchor Docs:** `Docs/1-Core_Concept/3-profile-app-cc.md`, `Docs/2-Design-Concept/0-Factory-Saas/14-pipeline-tailwind-cotton-fs.md`

---

## 1. Proposito

Definir UX funcional del dashboard de Profile como agregador no-dueno de datos, con degradacion segura por dependencia.

---

## 2. Patron de composicion

El dashboard consulta contratos publicos de otras apps y renderiza secciones si estan disponibles.

Fuentes:
- Product-Orchestrator: productos comprados/activos del tenant.
- Marketing: cupones y descuentos vigentes.
- Orders: recientes y estado.
- Payment: pagos recientes, estado y metodos asociados.
- Support: tickets abiertos y SLA.
- Theme: tokens y componentes visuales.

Regla:
- Si Product-Orchestrator no esta/no responde: `products=[]`.
- Si Marketing no esta/no responde: `coupons=[]`, `discounts=[]`.
- Si Orders no esta/no responde: `orders=[]`.
- Si Payment no esta/no responde: `payments=[]`.
- Si Support no esta/no responde: `tickets=[]`.
- Si Theme no esta/no saludable: `theme_tokens=DEFAULT_THEME_TOKENS` y layout fallback.

---

## 3. Fallback visual

Ruta fallback:
- `templates/profiles/fallback/dashboard_basic.html`

Condiciones de activacion:
- Theme no instalado.
- Theme no saludable (timeout/error).

Contenido minimo fallback:
- contexto activo de tenant
- datos basicos de cuenta
- lista de secciones disponibles

---

## 4. Componentes sugeridos

- `c-user-avatar`
- `c-tenant-switcher`
- `c-profile-card`
- `c-membership-badge`

Todos con versionado interno y tokens de Theme cuando disponible.

---

## 5. Criterios de aceptacion

- [ ] Dashboard opera con composicion parcial sin fallar.
- [ ] Fallback visual de Profile funciona sin Theme.
- [ ] Secciones ausentes por dependencia suave no rompen respuesta.
