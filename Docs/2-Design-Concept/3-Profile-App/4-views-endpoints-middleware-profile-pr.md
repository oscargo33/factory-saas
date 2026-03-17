# Documento: Endpoints y Middleware - App Profile

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PR-4-API
**Ubicacion:** `./Docs/2-Design-Concept/3-Profile-App/4-views-endpoints-middleware-profile-pr.md`
**Anchor Docs:** `Docs/1-Core_Concept/3-profile-app-cc.md`, `Docs/2-Design-Concept/0-Factory-Saas/13-router-dinamico-esquemas-fs.md`

---

## 1. Proposito

Definir superficie HTTP de Profile y middleware complementario para resolver contexto de usuario/tenant con seguridad.

---

## 2. Middleware de contexto

### 2.1 `ProfileContextMiddleware`

Responsabilidades:
- Leer `request.user` autenticado.
- Resolver tenant activo y membership.
- Inyectar `request.profile_context` para servicios y vistas.

Salida esperada:
`{"user": ..., "tenant": ..., "membership": ...}`

### 2.2 Integracion con `TenantMiddleware`

- Requiere tenant ya resuelto por Capa 5.
- Si tenant no existe o membership invalida: responder `403`.

---

## 3. Endpoints

Prefijo sugerido: `/api/profile/`

| Metodo | Endpoint | Descripcion | Permiso |
|---|---|---|---|
| `GET` | `/me/` | Contexto activo de usuario y tenant | autenticado |
| `PUT` | `/me/preferences/` | Actualizar preferencias (`locale`, `timezone`, etc.) | autenticado |
| `GET` | `/tenants/` | Listar tenants del usuario | autenticado |
| `POST` | `/switch-tenant/` | Cambio de tenant activo | membership activo |
| `POST` | `/memberships/invite/` | Invitar usuario a tenant | owner/admin |
| `GET` | `/dashboard/` | Dashboard agregador por composicion | autenticado |

---

## 4. Seguridad

- RBAC en base a `membership.role`.
- `switch-tenant` solo permite tenants del usuario.
- Limitar intentos de invitacion por actor/tenant.
- Auditar cambio de rol, invitacion y switch de tenant.

---

## 5. Degradacion graciosa

- Si Theme no esta/no saludable: render fallback en templates de profile.
- Si Orders/Support no estan: dashboard retorna secciones vacias.
- Si Telemetry no esta: no reportar evento y continuar flujo.

---

## 6. Criterios de aceptacion

- [ ] Endpoints principales cubren identidad, tenancy y dashboard.
- [ ] RBAC y pertenencia tenant validados en cada accion sensible.
- [ ] Fallback de dependencias suaves documentado y verificable.
