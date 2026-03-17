# EPI-001 — Theme: El Motor de Identidad Visual e Idioma del SaaS

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** EPI-001
**Tipo:** ADN Epic — Capa 1, proveedora de recursos para todas las apps
**Prioridad:** 1 — Bloqueante para cualquier Epic con UI
**Sprint objetivo:** Sprint-1
**Dependencias:** EPI-000 Done, EPI-CORE Done
**Blueprints fuente:**
- `Docs/1-Core_Concept/1-theme-app-cc.md`
- `Docs/2-Design-Concept/1-Theme-App/` (10 documentos)

---

## § 1 — EL ALMA: Visión y Razón de Existir

### ¿Qué Problema Resuelve?

En un SaaS multi-tenant, cada cliente espera ver _su marca_, no la marca del proveedor. El tenant "Acme Inc." quiere sus colores corporativos, su fuente, su tono de comunicación en el idioma de su mercado. Sin Theme, todo el SaaS tendría el mismo look genérico para todos los clientes — un producto imposible de vender.

Theme resuelve dos problemas fundamentales:
1. **Identidad visual dinámica:** Los colores, fuentes y radios del diseño se cambian en runtime sin un deploy, directamente desde la base de datos, por tenant.
2. **Internacionalización activa:** Las traducciones no son archivos `.po` estáticos que requieren un deploy para cambiar. Son entradas en base de datos que cualquier administrador puede actualizar y que LibreTranslate puede generar automáticamente.

### La Promesa

Cualquier app del sistema puede llamar a `get_theme_for_tenant(slug)` y recibir los tokens CSS correctos para ese tenant, sin saber ni importar nada del modelo `ThemeConfig`. Si Theme no está instalado, recibe los tokens por defecto. Nunca rompe.

Cualquier app puede llamar a `get_translation("ui.buttons.save", "fr", slug)` y recibir "Enregistrer". Si la clave no existe, recibe `"ui.buttons.save"` — nunca `None`, nunca una excepción.

---

## § 2 — LA FILOSOFÍA: Principios Fundacionales Aplicados

| Principio | Cómo se aplica en EPI-001 |
|---|---|
| **Degradación Graciosa** | Sin ThemeConfig → `DEFAULT_THEME_TOKENS`. Sin traducción → retorna la `key` original. Sin LibreTranslate → retorna español base. |
| **Aislamiento Total** | `ThemeConfig` y `Glossary` viven en `schema: tenant_{slug}`. Tenant A nunca contamina el tema de Tenant B. |
| **Service/Selector** | `get_theme_for_tenant` y `get_translation` son selectors puros (cachéables). `set_active_theme` y `upsert_translation` son services con transacciones atómicas. |
| **No Cross-App Imports** | Ninguna otra app importa `ThemeConfig` o `Glossary`. Consumo únicamente por contratos `theme.get_tokens.v1` y `theme.translate.v1`. |

---

## § 3 — LA ARQUITECTURA: Lo Que EPI-001 Crea

### Estructura de Archivos

```
apps/theme/
├── models.py          ← ThemeConfig (tokens visuales), Glossary (i18n JSONB)
├── services.py        ← upsert_translation, bulk_sync_translations, set_active_theme, translate_with_fallback
├── selectors.py       ← get_theme_for_tenant, get_translation, get_translations_batch, get_language_matrix
├── middleware.py      ← ThemeContextMiddleware (inyecta theme tokens en request context)
├── validators.py      ← validate_hex_color, validate_font_name
├── exceptions.py      ← ThemeNotFoundError, TranslationError
├── migrations/
│   └── 0001_initial.py
├── templates/
│   ├── theme/
│   │   └── base.html  ← Layout maestro con tokens CSS dinámicos y bloques extensibles
│   └── cotton/        ← Librería de componentes atómicos reutilizables
│       ├── button.html
│       ├── input.html
│       ├── modal.html
│       ├── card.html
│       └── alert.html
├── static/theme/
│   ├── css/           ← Tailwind output compilado
│   └── js/            ← Alpine.js init, utilities
└── tests/
    ├── test_models.py
    ├── test_selectors.py
    └── test_services.py
```

### Modelos de Datos

**`ThemeConfig`** (schema: `tenant_{slug}`)
| Campo | Tipo | Regla |
|---|---|---|
| `id` | UUID PK | — |
| `tenant_slug` | CharField(63) | unique por tenant |
| `primary_color` | CharField(15) | formato `#RRGGBB` validado |
| `secondary_color` | CharField(15) | formato `#RRGGBB` validado |
| `bg_color` | CharField(15) | formato `#RRGGBB` validado |
| `text_color` | CharField(15) | formato `#RRGGBB` validado |
| `font_body` | CharField(120) | — |
| `font_heading` | CharField(120) | — |
| `radius_base` | CharField(20) | ej. `0.375rem` |
| `is_active` | BooleanField | solo 1 config activa por tenant |

**`Glossary`** (schema: `tenant_{slug}`)
| Campo | Tipo | Regla |
|---|---|---|
| `id` | UUID PK | — |
| `key` | CharField(190) | formato `scope.section.item`, unique por tenant |
| `translations` | JSONB | contiene obligatoriamente `es` |
| `is_verified` | BooleanField | `False` = generado por IA, pendiente revisión |
| `source` | CharField(30) | `manual` / `ai` |

### Contratos Públicos Expuestos (TH-3-SVC)

| Contrato | Firma | Fallback |
|---|---|---|
| `get_theme_for_tenant` | `(tenant_slug: str) → dict \| None` | `DEFAULT_THEME_TOKENS` |
| `get_translation` | `(key, lang, tenant_slug) → str` | retorna `key` original |
| `get_translations_batch` | `(keys, lang, tenant_slug) → dict` | retorna `{key: key}` |
| `get_language_matrix` | `(tenant_slug) → dict` | `{base: 'es', enabled: ['en']}` |

### Engine de Traducción (Flujo)

```
1. Resolver idioma con Django (LocaleMiddleware / translation.activate / gettext)
2. Buscar en Redis cache (TTL 10min): "theme:trans:{tenant}:{lang}:{key}"
3. Buscar en Glossary JSONB (PostgreSQL)
4. Si falta → llamar LibreTranslate sidecar (async via Celery)
5. Persistir en Glossary + Redis
6. Si LibreTranslate falla → retornar key o texto base en español
```

### Layout Base HTML

```html
<!-- templates/theme/base.html -->
<style>
  :root {
    --color-primary: {{ theme.primary_color|default:'#1a1a2e' }};
    --color-secondary: {{ theme.secondary_color|default:'#e94560' }};
    --font-body: {{ theme.font_body|default:'system-ui' }};
    --radius-base: {{ theme.radius_base|default:'0.375rem' }};
  }
</style>
```

---

## § 4 — EL ÁRBOL: User Stories de Cimientos a Acabados

| US ID | Historia | SP | Sprint | Archivo |
|---|---|---|---|---|
| US-001-01 | `ThemeConfig` model + selectors + defaults | 3 | Sprint-1 | [US-001-01](US-001-01-themeconfig-model.md) |
| US-001-02 | `Glossary` CRUD + i18n engine (Redis + LibreTranslate) | 5 | Sprint-1 | 🔲 Sin US file |
| US-001-03 | Cotton components library (button, input, modal, card) | 3 | Sprint-1 | 🔲 Sin US file |
| US-001-04 | `base.html` layout maestro + ThemeContextMiddleware | 3 | Sprint-1 | 🔲 Sin US file |
| US-001-05 | Tailwind pipeline + admin de ThemeConfig + scripts | 2 | Sprint-2 | 🔲 Sin US file |

### Dependencias

```
US-001-01 (ThemeConfig) ──→ US-001-03 (Cotton: necesita tokens activos)
                        ──→ US-001-04 (base.html: consume ThemeConfig)
US-001-02 (Glossary)    ──→ US-001-04 (base.html: consume traducciones)
US-001-01 + US-001-02   ──→ US-001-05 (Admin: gestiona ambos modelos)
```

---

## § 5 — BLUEPRINTS DE REFERENCIA

| ID | Documento | Qué gobierna |
|---|---|---|
| CC-1 | `Docs/1-Core_Concept/1-theme-app-cc.md` | Visión, layout base, política i18n |
| TH-2 | `2-Design-Concept/1-Theme-App/2-modelos-theme-th.md` | Campos exactos de ThemeConfig y Glossary |
| TH-3 | `2-Design-Concept/1-Theme-App/3-service-selector-contratos-theme-th.md` | Firmas de contratos y versioning |
| TH-4 | `2-Design-Concept/1-Theme-App/4-views-endpoints-middleware-theme-th.md` | ThemeContextMiddleware, endpoints admin |
| TH-5 | `2-Design-Concept/1-Theme-App/5-componentes-cotton-pipeline-theme-th.md` | Componentes Cotton, pipeline Tailwind |
| DC-14 | `0-Factory-Saas/14-pipeline-tailwind-cotton-fs.md` | Pipeline de compilación CSS |
| DC-16 | `0-Factory-Saas/16-contratos-inter-app-fs.md` | Registro global de contratos |

---

## § 6 — DEFINITION OF DONE

EPI-001 está Done cuando:

- [ ] `get_theme_for_tenant("acme")` retorna tokens correctos; `get_theme_for_tenant("inexistente")` retorna `DEFAULT_THEME_TOKENS` sin excepción
- [ ] `get_translation("ui.buttons.save", "fr", "acme")` retorna `"Enregistrer"` (o la key si no existe)
- [ ] CSS variables `--color-primary` y `--font-body` se inyectan en cada request del tenant correcto
- [ ] Tenant A no puede ver ni modificar el `Glossary` de Tenant B (test de aislamiento)
- [ ] Componentes Cotton: button, input, modal, card renderizan sin errores con tokens variables
- [ ] `pytest apps/theme/` pasa con ≥ 90% cobertura en services y selectors
- [ ] Admin de `ThemeConfig` y `Glossary` funcional con validación de colores HEX
- [ ] Si Theme no está en `INSTALLED_APPS`, ninguna otra app rompe (test de independencia)
- [ ] `product-backlog.md` actualizado: US-001-01..05 con estados correctos
