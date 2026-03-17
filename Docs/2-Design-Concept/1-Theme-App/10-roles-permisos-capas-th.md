# Documento: Roles, Permisos y Capas — App 1 Theme

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** TH-10-RBAC
**Ubicacion:** `./Docs/2-Design-Concept/1-Theme-App/10-roles-permisos-capas-th.md`
**Anchor Docs:** `1-theme-app-cc.md`, `22-roles-permisos-capas-ux-fs.md`

---

## 1. Roles que interactuan con Theme

| Rol | Relacion con la app |
|---|---|
| `anonymous` | Sin acceso directo; consume el CSS/JS generado por Theme |
| `member` | Solo lectura del preview de tema activo |
| `admin` | Edita configuracion visual del tenant |
| `owner` | Igual que admin; puede resetear al tema base |
| `staff` | Lee configuraciones cross-tenant; no edita temas de tenants |
| `superadmin` | Acceso total incluyendo componentes globales del sistema |

---

## 2. Capa Publica (anonymous)

| Pantalla / Recurso | Permitido | Restriccion |
|---|---|---|
| CSS y tokens compilados | Lectura (HTTP) | Solo los del tenant activo en el subdominio |
| Componentes Cotton renderizados | Lectura (HTML) | No expone datos de configuracion raw |
| Configuracion interna del tema | Prohibido | Requiere autenticacion |

---

## 3. Capa Privada (member / admin / owner)

| Pantalla / Accion | member | admin | owner |
|---|---|---|---|
| Ver preview de tema activo | Si | Si | Si |
| Editar tokens de color y tipografia | No | Si | Si |
| Publicar cambios de tema | No | Si | Si |
| Gestionar traducciones/glosario | No | Si | Si |
| Resetear tema al base de fabrica | No | No | Si |
| Ver historial de cambios de tema | No | Si | Si |

---

## 4. Capa Admin Django (staff / superadmin)

| Modelo | staff (lectura) | staff (escritura) | superadmin |
|---|---|---|---|
| ThemeConfig | Si | No (solo lectura cross-tenant) | CRUD completo |
| GlossaryTerm | Si | Si (global) | CRUD completo |
| ComponentVariant | Si | No | CRUD completo |

Restricciones criticas:
- Un `staff` no puede modificar el tema de un tenant; solo diagnosticar.
- Cambios en tokens globales son solo de `superadmin`.

---

## 5. Assets de Theme

| Asset | Operacion | anonymous | member | admin | owner | staff | superadmin |
|---|---|---|---|---|---|---|---|
| CSS compilado (output.css) | Leer | Si | Si | Si | Si | Si | Si |
| Tokens CSS por tenant | Leer | Si (via CSS) | Si | Si | Si | Si | Si |
| Tokens CSS por tenant | Editar | No | No | Si | Si | No | Si |
| Archivos de fuentes tipograficas | Leer | Si | Si | Si | Si | Si | Si |
| Archivos de fuentes tipograficas | Cargar/borrar | No | No | No | Si | No | Si |
| Glosario CSV (export) | Exportar | No | No | Si | Si | Si | Si |

---

## 6. Notas de seguridad

- Los tokens de tema nunca se exponen como JSON en endpoints abiertos.
- La fallback visual (CSS base) se sirve siempre sin autenticacion para garantizar degradacion graciosa.
