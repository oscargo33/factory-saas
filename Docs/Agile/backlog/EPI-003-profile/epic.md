# EPI-003 — Profiles: El Corazón de la Identidad y la Membresía

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** EPI-003
**Tipo:** Context Epic — Capa 2, núcleo operativo de usuarios y tenants
**Prioridad:** 2 — Requerido por todas las apps transaccionales
**Sprint objetivo:** Sprint-1
**Dependencias:** EPI-000 Done, EPI-CORE Done (EPI-001/002 paralelos)
**Blueprints fuente:**
- `Docs/1-Core_Concept/3-profile-app-cc.md`
- `Docs/2-Design-Concept/3-Profile-App/` (11 documentos)

---

## § 1 — EL ALMA: Visión y Razón de Existir

### ¿Qué Problema Resuelve?

¿Quién es el usuario? ¿A qué tenant pertenece? ¿Qué puede hacer? Estas tres preguntas son la base de cualquier interacción en el SaaS. Sin responderlas, no hay autenticación, no hay autorización, no hay contexto.

EPI-003 es el **corazón operativo del SaaS**: gestiona que una misma persona puede ser administradora de "Acme Inc." y usuaria regular de "Globex Corp." con una sola cuenta, y que cuando entra a Acme ve sus datos de Acme, y cuando entra a Globex ve sus datos de Globex — sin mezclas, sin confusión.

### La Promesa

El Dashboard de Usuario es el hub de todo: muestra sus órdenes, sus pagos, sus tickets activos, sus productos contratados — todo en un solo lugar, agregando datos de todas las apps instaladas. Si una app no está, esa sección simplemente no aparece.

El sistema de roles (RBAC) garantiza que un `Member` no pueda cambiar el plan del tenant, pero un `Owner` sí.

---

## § 2 — LA FILOSOFÍA: Principios Fundacionales Aplicados

| Principio | Cómo se aplica en EPI-003 |
|---|---|
| **Degradación Graciosa** | Dashboard muestra secciones vacías `[]` si Orders/Payment/Support no están. Login siempre funciona con fallback HTML puro. |
| **Aislamiento Total** | `User` y `Membership` en schema `public`. `Profile` en schema `tenant_{slug}`. Datos de perfil de un tenant son invisibles para otro. |
| **No Cross-App Imports** | Orders/Payment/Support no importan `User` directamente. Solo consumen `get_display_name(user_id)` y `get_active_context(request)`. |
| **RBAC por Contrato** | `has_permission(user, tenant, permission_code)` es el único guardián de acceso para todas las apps. |

---

## § 3 — LA ARQUITECTURA: Lo Que EPI-003 Crea

### Estructura de Archivos

```
apps/profiles/
├── models.py          ← Profile (preferencias en tenant schema), RBACPermission
├── services.py        ← create_profile, invite_user, switch_tenant, update_preferences
├── selectors.py       ← get_display_name, get_active_context, get_dashboard_data, has_permission
├── middleware.py      ← ProfileContextMiddleware (añade profile al request)
├── exceptions.py      ← ProfileNotFoundError, MembershipError, PermissionDenied
├── migrations/
│   └── 0001_initial.py
├── templates/
│   ├── profiles/
│   │   ├── dashboard.html       ← agregador UI (composition pattern)
│   │   ├── settings.html
│   │   └── fallback/
│   │       └── dashboard_basic.html  ← HTML puro sin Theme
│   └── cotton/
│       ├── user_avatar.html
│       ├── tenant_switcher.html  ← Alpine.js dropdown de organizaciones
│       └── profile_card.html
└── tests/
    ├── test_models.py
    ├── test_selectors.py
    └── test_dashboard_aggregation.py
```

### Modelos de Datos

**`User`** (schema `public` — extendido de `auth.User`)
— Credenciales, email, MFA; definido en EPI-CORE como parte del core.

**`Tenant`** (schema `public` — definido en EPI-CORE)
— Registro de instancia SaaS con slug, dominio, estado activo.

**`Membership`** (schema `public` — definido en EPI-CORE)
— Relación `User ↔ Tenant` con `role`: `owner`, `admin`, `member`.

**`Profile`** (schema `tenant_{slug}` — propio de EPI-003)
| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID PK | — |
| `user_id` | IntegerField | FK lógico a `auth.User` (sin FK real cross-schema) |
| `display_name` | CharField(120) | nombre visible en el tenant |
| `avatar_url` | URLField null | imagen de perfil |
| `preferred_language` | CharField(5) | `es`, `en`, etc. Override del tenant lang |
| `notification_prefs` | JSONB | configuración de notificaciones |
| `created_at` | DateTime | — |

### Contratos Públicos Expuestos

| Contrato | Firma | Fallback | Consumidores |
|---|---|---|---|
| `get_display_name` | `(user_id, tenant_slug) → {display_name, profile_id}` | `{"display_name": "Usuario", "profile_id": None}` | Orders, Support, Telemetry |
| `get_active_context` | `(request) → {user, tenant, profile, telemetry_identity}` | — | Todas las apps con views autenticadas |
| `has_permission` | `(user_id, tenant_slug, perm) → bool` | `False` | Orders, Payment, Orchestrator |

### Dashboard Aggregator Pattern

```python
# profiles/selectors.py
def get_dashboard_data(user_id, tenant_slug):
    data = {"profile": get_profile(user_id, tenant_slug)}
    if apps.is_installed('apps.orders'):
        data["recent_orders"] = orders_selectors.get_recent(user_id)
    else:
        data["recent_orders"] = []
    if apps.is_installed('apps.payments'):
        data["billing"] = payment_selectors.get_subscription_status(tenant_slug)
    else:
        data["billing"] = None
    if apps.is_installed('apps.support'):
        data["active_tickets"] = support_selectors.get_active_tickets(user_id)
    else:
        data["active_tickets"] = []
    # ... Marketing, Orchestrator, etc.
    return data
```

---

## § 4 — EL ÁRBOL: User Stories de Cimientos a Acabados

| US ID | Historia | SP | Sprint | Estado |
|---|---|---|---|---|
| US-003-01 | `Profile` model + selectors: get_display_name, get_active_context | 3 | Sprint-1 | 🔲 Sin US file |
| US-003-02 | RBAC: roles Owner/Admin/Member + has_permission selector | 3 | Sprint-1 | 🔲 Sin US file |
| US-003-03 | invite_user + switch_tenant services | 3 | Sprint-1 | 🔲 Sin US file |
| US-003-04 | Dashboard aggregator (composition pattern) + cotton components | 3 | Sprint-2 | 🔲 Sin US file |
| US-003-05 | Fallback login/dashboard HTML puro (sin Theme) | 2 | Sprint-2 | 🔲 Sin US file |

### Dependencias

```
US-003-01 (Profile básico) ──→ US-003-02 (RBAC necesita Profile)
                           ──→ US-003-03 (invite necesita Profile)
US-003-01 + US-003-02      ──→ US-003-04 (Dashboard necesita ambos)
US-003-04                  ──→ US-003-05 (Fallback es versión degradada del dashboard)
```

---

## § 5 — BLUEPRINTS DE REFERENCIA

| ID | Documento | Qué gobierna |
|---|---|---|
| CC-3 | `Docs/1-Core_Concept/3-profile-app-cc.md` | Visión, modelos globales, dashboard aggregator |
| PR-2 | `3-Profile-App/2-modelos-profile-pr.md` | Campos exactos de Profile y membresías |
| PR-3 | `3-Profile-App/3-service-selector-contratos-profile-pr.md` | Contratos públicos, RBAC |
| PR-4 | `3-Profile-App/4-views-endpoints-middleware-profile-pr.md` | Views, endpoints, ProfileContextMiddleware |
| PR-5 | `3-Profile-App/5-dashboard-fallback-composition-profile-pr.md` | Dashboard composition pattern |
| DC-16 | `0-Factory-Saas/16-contratos-inter-app-fs.md` | Contrato get_user_by_id, get_active_memberships |

---

## § 6 — DEFINITION OF DONE

EPI-003 está Done cuando:

- [ ] Un usuario puede ser miembro de 2 tenants; `Profile` en cada uno es independiente
- [ ] `get_active_context(request)` retorna `{user, tenant, profile, telemetry_identity}` para request autenticado
- [ ] `has_permission(user_id, tenant_slug, "order.create")` retorna `False` para `role=member` sin permiso
- [ ] Dashboard renderiza con secciones vacías `[]` cuando Orders/Payment/Support no están instalados
- [ ] `templates/profiles/fallback/dashboard_basic.html` renderiza sin Theme (HTML puro funcional)
- [ ] Invitación de usuario crea `Membership` y envía email (o log en dev)
- [ ] `pytest apps/profiles/` pasa incluyendo test de dashboard con mock de apps externas
- [ ] `product-backlog.md` actualizado: US-003-01..05 con estados correctos
