# Documento: Service, Selector y Contratos - App Profile

**ID:** PR-3-SVC
**Ubicacion:** `./Docs/2-Design-Concept/3-Profile-App/3-service-selector-contratos-profile-pr.md`
**Anchor Docs:** `Docs/1-Core_Concept/3-profile-app-cc.md`, `Docs/2-Design-Concept/0-Factory-Saas/12-patron-service-layer-fs.md`, `Docs/2-Design-Concept/0-Factory-Saas/16-contratos-inter-app-fs.md`

---

## 1. Proposito

Definir interfaces publicas de Profile para identidad, contexto tenant y composicion de dashboard por dependencias suaves.

---

## 2. Services publicos (escritura)

| Funcion | Firma | Efecto |
|---|---|---|
| `create_membership` | `(user_id: int, tenant_id: UUID, role: str) -> UUID` | Alta de membresia |
| `switch_tenant` | `(user_id: int, tenant_id: UUID) -> dict` | Valida membresia y cambia contexto |
| `invite_user_to_tenant` | `(email: str, tenant_id: UUID, role: str, actor_id: int) -> dict` | Invitacion con RBAC |
| `update_profile_preferences` | `(user_id: int, tenant_slug: str, payload: dict) -> None` | Actualiza `Profile` |

Reglas:
- Escritura atomica.
- Validacion estricta de rol y pertenencia antes de mutar datos.

---

## 3. Selectors publicos (lectura)

| Funcion | Firma | Retorna |
|---|---|---|
| `get_active_context` | `(request) -> dict` | `{user, tenant, membership}` |
| `get_profile_for_user` | `(user_id: int, tenant_id: UUID) -> dict | None` | Perfil resumido |
| `get_user_tenants` | `(user_id: int) -> list[dict]` | Tenants accesibles |
| `get_dashboard_composition` | `(user_id: int, tenant_id: UUID) -> dict` | Secciones agregadas (orders/support) |

---

## 4. Contratos inter-app

Version inicial: `profile.contract.v1`

| Contrato | Tipo | Entrada | Salida |
|---|---|---|---|
| `profile.active_context.v1` | Selector | `{request}` | `{user, tenant, membership}` |
| `profile.display_name.v1` | Selector | `{user_id, tenant_id}` | `{display_name}` |
| `profile.switch_tenant.v1` | Service | `{user_id, tenant_id}` | `{redirect_url, tenant_slug}` |
| `profile.dashboard.v1` | Selector | `{user_id, tenant_id}` | `{orders, tickets, ...}` |

Fallbacks:
- Sin Orders: `orders=[]`.
- Sin Support: `tickets=[]`.
- Sin Telemetry: evento no emitido, operacion principal continua.

---

## 5. Reglas de seguridad contractual

- Verificar `is_active` en membership antes de exponer contexto.
- Rol requerido para acciones administrativas (owner/admin).
- Eventos de cambio de rol/tenant deben emitirse a auditoria.

---

## 6. Criterios de aceptacion

- [ ] Contratos v1 documentados y versionados.
- [ ] Ninguna app importa modelos Profile directamente.
- [ ] Fallback por dependencia suave definido para dashboard.
