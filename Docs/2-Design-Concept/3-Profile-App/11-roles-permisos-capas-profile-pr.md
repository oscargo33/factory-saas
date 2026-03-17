# Documento: Roles, Permisos y Capas — App 3 Profile

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PR-11-RBAC
**Ubicacion:** `./Docs/2-Design-Concept/3-Profile-App/11-roles-permisos-capas-profile-pr.md`
**Anchor Docs:** `3-profile-app-cc.md`, `22-roles-permisos-capas-ux-fs.md`

---

## 1. Roles que interactuan con Profiles

| Rol | Relacion con la app |
|---|---|
| `anonymous` | Puede registrarse y hacer login |
| `authenticated` | Sesion abierta; debe seleccionar o crear tenant |
| `member` | Usuario activo dentro de un tenant |
| `admin` | Gestiona miembros y configuracion del tenant |
| `owner` | Control total del tenant; puede suspenderlo |
| `staff` | Diagnostica usuarios y tenants; no edita sin motivo |
| `superadmin` | Acceso total al sistema de identidad |

---

## 2. Capa Publica (anonymous)

| Pantalla / Accion | Permitido | Restriccion |
|---|---|---|
| Formulario de registro | Si | Solo Email + Password; MFA se configura post-registro |
| Formulario de login | Si | Rate limiting activo |
| Recuperacion de contrasena | Si | Expiracion de token a 1 hora |
| Ver perfil publico de otro usuario | No | Perfiles son privados por diseno |

---

## 3. Capa Privada por rol

| Pantalla / Accion | authenticated | member | admin | owner |
|---|---|---|---|---|
| Ver lista de tenants propios | Si | Si | Si | Si |
| Crear nuevo tenant | Si | No (lo hace desde su cuenta base) | No | No |
| Cambiar de tenant activo | N/A | Si | Si | Si |
| Ver y editar propio perfil | Si | Si | Si | Si |
| Ver perfil de otro miembro | No | Si (nombre, rol) | Si | Si |
| Invitar nuevos miembros | No | No | Si | Si |
| Cambiar rol de miembro | No | No | Si (hasta admin) | Si (hasta owner) |
| Suspender/reactivar miembro | No | No | No | Si |
| Ver dashboard agregado | No | Si (propio) | Si | Si |
| Configurar ajustes del tenant | No | No | Si | Si |
| Suspender/eliminar tenant | No | No | No | Si |

---

## 4. Capa Admin Django (staff / superadmin)

| Modelo | staff (lectura) | staff (escritura) | superadmin |
|---|---|---|---|
| User | Si | Si (reset password, desactivar) | CRUD completo |
| Tenant | Si | Si (suspender/reactivar) | CRUD completo |
| Membership | Si | Si (ajustar rol con motivo) | CRUD completo |
| Profile | Si | Si | CRUD completo |

Restricciones criticas:
- `staff` no puede borrar `User`; solo desactivar.
- Cambios de `Membership` de `staff` requieren campo `motivo` obligatorio auditado.

---

## 5. Assets de Profiles

| Asset | Operacion | anonymous | member | admin | owner | staff | superadmin |
|---|---|---|---|---|---|---|---|
| Avatar de usuario | Ver | No | Si (propio) | Si | Si | Si | Si |
| Avatar de usuario | Cargar/cambiar | No | Si (propio) | No | No | No | Si |
| Avatar de usuario | Borrar | No | Si (propio) | No | Si | No | Si |
| Export de miembros del tenant | Exportar CSV | No | No | Si | Si | Si | Si |
| Datos de tenant (schema slug) | Ver | No | Si | Si | Si | Si | Si |
| Datos de tenant (schema slug) | Editar | No | No | No | Si | No | Si |
| Logs de acceso y sesiones | Ver | No | Si (propios) | No | Si (tenant) | Si | Si |
| Logs de acceso y sesiones | Borrar | No | No | No | No | No | Si |

---

## 6. Notas de seguridad

- El `schema slug` del tenant nunca se expone en URLs publicas; solo en contexto autenticado.
- Invitaciones caducan a las 48 horas.
- MFA obligatorio para `owner` en produccion.
