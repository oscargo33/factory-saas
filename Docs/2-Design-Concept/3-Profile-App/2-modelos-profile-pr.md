# Documento: Modelos de Datos - App Profile

**ID:** PR-2-MDL
**Ubicacion:** `./Docs/2-Design-Concept/3-Profile-App/2-modelos-profile-pr.md`
**Anchor Docs:** `Docs/1-Core_Concept/3-profile-app-cc.md`, `Docs/2-Design-Concept/0-Factory-Saas/13-router-dinamico-esquemas-fs.md`, `Docs/2-Design-Concept/0-Factory-Saas/17-diccionario-datos-logico-fs.md`

---

## 1. Proposito

Definir entidades de identidad y tenancy para aislamiento multi-tenant con RBAC y contexto de usuario.

---

## 2. Entidades en schema `public`

### 2.1 `User`

| Campo | Tipo | Restricciones | Descripcion |
|---|---|---|---|
| `id` | Integer PK | Django auth | Identificador global |
| `email` | EmailField | unique | Login principal |
| `password` | CharField | hash seguro | Credencial |
| `is_active` | BooleanField | default True | Estado de cuenta |
| `mfa_enabled` | BooleanField | default False | MFA habilitado |
| `created_at` | DateTime | auto | Alta |

### 2.2 `Tenant`

| Campo | Tipo | Restricciones | Descripcion |
|---|---|---|---|
| `id` | UUID PK | requerido | Identificador de tenant |
| `name` | CharField(200) | requerido | Nombre comercial |
| `slug` | SlugField(63) | unique | Subdominio |
| `schema_name` | CharField(80) | unique | Schema fisico |
| `status` | CharField(20) | `active/suspended/cancelled/pending` | Estado |
| `created_at` | DateTime | auto | Alta |

### 2.3 `Membership`

| Campo | Tipo | Restricciones | Descripcion |
|---|---|---|---|
| `id` | UUID PK | requerido | Identificador |
| `user_id` | IntegerField | indexado | FK logica a User |
| `tenant_id` | UUID | indexado | FK logica a Tenant |
| `role` | CharField(20) | `owner/admin/member/read_only` | Rol RBAC |
| `is_active` | BooleanField | default True | Membresia activa |
| `joined_at` | DateTime | auto | Fecha ingreso |

---

## 3. Entidad en schema `tenant_{slug}`

### 3.1 `Profile`

| Campo | Tipo | Restricciones | Descripcion |
|---|---|---|---|
| `id` | UUID PK | requerido | Identificador |
| `user_id` | IntegerField | indexado | Referencia logica a User global |
| `display_name` | CharField(150) | requerido | Nombre visible |
| `avatar_url` | URLField | nullable | Avatar |
| `locale` | CharField(10) | default `es` | Idioma de preferencia |
| `timezone` | CharField(50) | default `UTC` | Zona horaria |
| `notification_prefs` | JSONB | default {} | Preferencias |
| `created_at` | DateTime | auto | Alta |
| `updated_at` | DateTime | auto | Ultima actualizacion |

---

## 4. Reglas de consistencia

- `User`, `Tenant`, `Membership` solo en `public`.
- `Profile` solo en schema tenant.
- No FK fisica cross-schema; referencias logicas por ID.
- Cambios de rol deben quedar auditados.

---

## 5. Relacion con otros documentos

| Documento | Relacion |
|---|---|
| `Docs/2-Design-Concept/0-Factory-Saas/13-router-dinamico-esquemas-fs.md` | `search_path` y contexto tenant |
| `Docs/2-Design-Concept/0-Factory-Saas/16-contratos-inter-app-fs.md` | Contratos publicos de profile |
| `Docs/2-Design-Concept/0-Factory-Saas/18-matriz-seguridad-compliance-fs.md` | Controles de PII y RBAC |

---

## 6. Criterios de aceptacion

- [ ] Modelo separa claramente `public` vs `tenant`.
- [ ] RBAC en Membership definido y auditable.
- [ ] Reglas de integridad cross-schema documentadas.
