# Documento: 22-roles-permisos-capas-ux-fs.md

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** DC-22-FS
**Ubicacion:** `./Docs/2-Design-Concept/0-Factory-Saas/22-roles-permisos-capas-ux-fs.md`
**Referencia Core:** `0-factory_saas-cc.md`, `18-matriz-seguridad-compliance-fs.md`, `21-product-visible-ux-fs.md`
**Capa:** Fase 1B — Roles, Permisos y Capas de Interfaz (RBAC de UX)
**Apellido:** **-fs**

---

## 1. Proposito

Definir la taxonomia de roles del sistema y el estandar con que cada app especifica:
- Que puede ver y hacer cada rol en la **capa publica** (anonimo).
- Que puede ver y hacer cada rol en la **capa privada** (autenticado).
- Que puede ver y hacer cada rol en la **capa admin** (Django Admin).
- Que **assets** maneja la app y quien tiene permisos de lectura, escritura, borrado sobre ellos.

Este documento no reemplaza a los permisos tecnicos (decoradores, policies, RBAC en codigo); define el **diseño de lo que el usuario ve y puede hacer** antes de implementar.

---

## 2. Taxonomia de Roles — Factory SaaS

| Rol | Descripcion | Ambito |
|---|---|---|
| `anonymous` | Visitante sin sesion | Global (sin tenant) |
| `authenticated` | Usuario con sesion, sin tenant asignado aun | Global |
| `member` | Usuario activo dentro de un tenant con acceso basico | Tenant |
| `admin` | Usuario con permisos elevados dentro de un tenant | Tenant |
| `owner` | Propietario del tenant con control total | Tenant |
| `staff` | Operador interno de la Factory (no cliente) | Cross-tenant |
| `superadmin` | Django superuser, acceso total al sistema | Sistema |

Reglas de herencia de privilegios:
- `owner` hereda todos los permisos de `admin`.
- `admin` hereda todos los permisos de `member`.
- `staff` tiene acceso cross-tenant en modo lectura salvo que sea `superadmin`.
- `anonymous` solo accede a lo explicitamente marcado como publico.

---

## 3. Tres capas de interfaz por app

Cada app debe documentar sus tres capas:

### Capa Publica (anonymous)
- Que pantallas son accesibles sin login.
- Que acciones estan permitidas.
- Que datos se exponen (sin PII).

### Capa Privada (member / admin / owner)
- Que pantallas y acciones tiene cada rol.
- Diferencias de visibilidad entre roles.
- Que queda oculto o bloqueado por rol insuficiente.

### Capa Admin (Django Admin — staff / superadmin)
- Que modelos administra cada rol Django.
- Acciones permitidas (CRUD, bulk actions).
- Restricciones de mutacion (ej: no borrar registros auditados, no modificar snapshots).

---

## 4. Assets por app

Cada app debe declarar los assets que genera o administra:

| Tipo de asset | Ejemplos | Quien puede crear | Quien puede leer | Quien puede borrar |
|---|---|---|---|---|
| Archivos estaticos | CSS, JS, imagenes de UI | staff / superadmin | anonymous | staff |
| Archivos de usuario | Avatares, adjuntos de ticket | member | member (propio) / admin | owner / staff |
| Documentos generados | Recibos PDF, reportes | sistema (automatico) | member (propio) / admin / staff | staff |
| Datos sensibles | Tokens, credenciales de gateway | staff / superadmin | staff | superadmin |

Cada documento de app usa esta plantilla adaptada a sus modelos especificos.

---

## 5. Formato de documento por app

Cada app publica un archivo con el patron `roles-permisos-capas-[app]-[sufijo].md` con:

1. Roles que interactuan con la app.
2. Capa publica: pantallas y acciones por rol anonimo.
3. Capa privada: tabla `rol x pantalla x accion permitida`.
4. Capa admin: tabla `modelo x operacion x rol Django`.
5. Assets: tabla `asset x operacion x rol`.

---

## 6. Criterios de salida (DoD de este entregable)

- Cada app tiene su documento de roles/permisos/capas publicado.
- El documento distingue los tres perfiles: publico, privado, admin.
- Los assets estan declarados con sus permisos por rol.
- No hay pantalla o accion sin rol asignado.
- Las restricciones de mutacion de datos sensibles estan documentadas.
