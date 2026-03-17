# Documento: Producto Visible + Admin App 1 Theme

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** TH-9-PV  
**Ubicacion:** `./Docs/2-Design-Concept/1-Theme-App/9-product-visible-admin-th.md`  
**Anchor Docs:** `1-theme-app-cc.md`, `14-pipeline-tailwind-cotton-fs.md`, `21-product-visible-ux-fs.md`

## 1. Objetivo

Definir la especificacion visible para usuario interno (admin) y para interfaz de producto en App Theme.

## 2. CRUD en Django Admin (Theme)

| Modelo | C | R | U | D | Notas UI Admin |
|---|---|---|---|---|---|
| ThemeConfig | Si | Si | Si | No (soft delete recomendado) | Preview de paleta y tipografia antes de guardar |
| GlossaryTerm/i18n entries | Si | Si | Si | Si | Filtro por idioma, namespace y estado |
| ComponentVariant | Si | Si | Si | Si | Vista con muestra visual del componente |

Criterios admin:
- Lista con filtros por tenant, estado y fecha.
- Formularios con ayuda contextual y validaciones de contraste/color.
- Acciones masivas seguras: publicar/despublicar tema.

## 3. Interfaz de producto visible (frontend)

Pantallas minimas:
- Configuracion de tema por tenant.
- Preview de componentes Cotton.
- Gestion de glosario/traducciones.

Estados UX obligatorios:
- `loading`, `empty`, `error`, `success`.

## 4. Criterios de aceptacion

- Existe flujo completo: editar tema -> preview -> publicar.
- Admin y frontend comparten tokens de diseno.
- Fallback visual activo cuando Theme no esta saludable.
