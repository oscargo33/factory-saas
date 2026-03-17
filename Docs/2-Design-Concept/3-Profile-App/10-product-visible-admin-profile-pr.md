# Documento: Producto Visible + Admin App 3 Profile

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PR-10-PV  
**Ubicacion:** `./Docs/2-Design-Concept/3-Profile-App/10-product-visible-admin-profile-pr.md`  
**Anchor Docs:** `3-profile-app-cc.md`, `13-router-dinamico-esquemas-fs.md`, `21-product-visible-ux-fs.md`

## 1. Objetivo

Definir UX visible para identidad/tenancy y administracion de usuarios/roles en Django Admin.

## 2. CRUD en Django Admin (Profiles)

| Modelo | C | R | U | D | Notas UI Admin |
|---|---|---|---|---|---|
| User | Si | Si | Si | No (desactivar) | Busqueda por email/estado/MFA |
| Tenant | Si | Si | Si | No (suspender) | Mostrar slug, schema y plan |
| Membership | Si | Si | Si | Si | Edicion rapida de rol por tenant |
| Profile | Si | Si | Si | Si | Gestion de preferencias por tenant |

Criterios admin:
- Accion masiva de suspender/reactivar tenant.
- Validacion de unicidad en slug y membresias duplicadas.

## 3. Interfaz de producto visible (usuario final)

Pantallas minimas:
- Login/registro.
- Selector de tenant.
- Perfil de usuario.
- Dashboard agregador.

Estados UX obligatorios:
- `loading`, `empty`, `error`, `success`.

## 4. Criterios de aceptacion

- Flujo login -> tenant -> dashboard definido y testeable.
- Cambios de rol reflejan permisos de UI.
- Fallback de login en HTML puro disponible sin Theme.
