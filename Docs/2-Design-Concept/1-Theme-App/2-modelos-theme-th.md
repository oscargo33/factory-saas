# Documento: Modelos de Datos — App Theme

**ID:** TH-2-MDL
**Ubicación:** `./Docs/2-Design-Concept/1-Theme-App/2-modelos-theme-th.md`
**Anchor Doc:** `Docs/1-Core_Concept/1-theme-app-cc.md`
**Dependencias Globales:** `DC-9`, `DC-13`, `DC-17`

---

## 1. Propósito

Definir las entidades de datos de Theme para personalización visual e internacionalización dinámica por tenant.

---

## 2. Entidad `Glossary`

**Owner:** App Theme
**Schema:** `tenant_{slug}`
**Rol:** Diccionario dinámico de traducciones por clave funcional.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id` | UUID PK | requerido | Identificador único |
| `key` | CharField(190) | unique por tenant, indexado | Clave semántica (`ui.buttons.save`) |
| `translations` | JSONB | requerido | Mapa `{lang_code: text}` |
| `is_verified` | BooleanField | default `False` | Traducción validada manualmente |
| `source` | CharField(30) | `manual`/`ai` | Origen de la traducción |
| `created_at` | DateTime | auto | Creación |
| `updated_at` | DateTime | auto | Actualización |

### Reglas

- `key` usa naming de punto jerárquico: `scope.section.item`.
- `translations` debe contener al menos un idioma base (`es` o `en`).
- No se almacenan textos con secretos o credenciales.

---

## 3. Entidad `ThemeConfig`

**Owner:** App Theme
**Schema:** `tenant_{slug}`
**Rol:** Tokens de identidad visual aplicados en runtime.

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id` | UUID PK | requerido | Identificador |
| `tenant_slug` | CharField(63) | unique | Relación lógica con tenant activo |
| `primary_color` | CharField(15) | formato HEX válido | Color primario |
| `secondary_color` | CharField(15) | formato HEX válido | Color secundario |
| `bg_color` | CharField(15) | formato HEX válido | Fondo principal |
| `text_color` | CharField(15) | formato HEX válido | Texto base |
| `font_body` | CharField(120) | requerido | Fuente de lectura |
| `font_heading` | CharField(120) | requerido | Fuente de títulos |
| `radius_base` | CharField(20) | requerido | Radio base (`0.375rem`, etc.) |
| `is_active` | BooleanField | default `True` | Config vigente |
| `created_at` | DateTime | auto | Creación |
| `updated_at` | DateTime | auto | Actualización |

### Reglas

- Debe existir solo una configuración activa por tenant.
- Validación fuerte de colores para evitar CSS malformado.
- Si no existe `ThemeConfig`, el consumidor usa defaults globales.

---

## 4. Índices y rendimiento

| Entidad | Índice | Motivo |
|---|---|---|
| `Glossary` | `(key)` y GIN en `translations` | búsqueda rápida por clave/idioma |
| `ThemeConfig` | `(tenant_slug, is_active)` | resolución en middleware |

---

## 5. Relación con otros documentos

| Documento | Relación |
|---|---|
| `Docs/2-Design-Concept/0-Factory-Saas/14-pipeline-tailwind-cotton-fs.md` | Consume tokens de `ThemeConfig` |
| `Docs/2-Design-Concept/0-Factory-Saas/16-contratos-inter-app-fs.md` | Contratos públicos de lectura de theme |
| `Docs/2-Design-Concept/0-Factory-Saas/17-diccionario-datos-logico-fs.md` | Alineación de entidad `Glossary` |

---

## 6. Criterios de aceptación

- [ ] `Glossary` y `ThemeConfig` tienen ownership claro en App Theme.
- [ ] Ambos modelos viven en schema tenant, no en `public`.
- [ ] Existen reglas explícitas de fallback para consumidores.
