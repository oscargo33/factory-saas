# EPI-009 — Home: La Vitrina del SaaS y el Motor SEO

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** EPI-009
**Tipo:** Surface Epic — Capa 4, fachada pública y captación de leads
**Prioridad:** 4 — Primero viene la funcionalidad, luego la publicidad
**Sprint objetivo:** Sprint-2
**Dependencias:** EPI-000 Done, EPI-CORE Done, EPI-001 (Theme para UI), EPI-004 (Orchestrator para catálogo)
**Blueprints fuente:**
- `Docs/1-Core_Concept/9-home-app-cc.md`
- `Docs/2-Design-Concept/9-Home-App/` (11 documentos)

---

## § 1 — EL ALMA: Visión y Razón de Existir

### ¿Qué Problema Resuelve?

Un SaaS sin fachada pública depende del boca a boca y del marketing directo. Sin una landing page, sin SEO, sin un catálogo público accesible: ningún motor de búsqueda lo indexa, ningún prospecto que lo encuentre por Google puede ver qué hace ni cuánto cuesta.

EPI-009 construye la **vitrina del SaaS**: la primera impresión para todo visitante que llegue. Agrega el catálogo del Orchestrator, las ofertas de Marketing, el contexto de identidad de Profiles — todo para proyectar una imagen sólida, comercial y optimizada para buscadores.

Su característica más importante: **siempre funciona**, incluso si todos los demás sistemas están caídos. Si Orchestrator no responde → "Próximamente". Si Marketing no tiene ofertas → precios estándar. Si Theme no está → layout minimalista HTML funcional e indexable.

### La Promesa

`get_home_view_data(user)` — un solo call que agrega todo lo que la landing necesita. El resultado es determinista, cacheable, y cada sección tiene fallback explícito. El sitio nunca devuelve 500 al público.

---

## § 2 — LA FILOSOFÍA: Principios Fundacionales Aplicados

| Principio | Cómo se aplica en EPI-009 |
|---|---|
| **Degradación Graciosa** | Orchestrator caído → "Próximamente". Marketing caído → sin banners de oferta. Theme caído → `landing_minimal.html` (indexable). |
| **Aislamiento Total** | `LandingPage`, `SEOConfig`, `Lead` en schema `tenant_{slug}`. Configuración de la landing de Acme no afecta la de Globex. |
| **Aggregator Pattern** | Home no tiene lógica comercial propia. `get_home_view_data` es únicamente un recolector de datos de otras apps via selectors públicos. |
| **SEO por Construcción** | OpenGraph, Twitter Cards, JSON-LD y Sitemap no son un afterthought — son parte del DoD de este Epic. |

---

## § 3 — LA ARQUITECTURA: Lo Que EPI-009 Crea

### Estructura de Archivos

```
apps/home/
├── models.py          ← LandingPage, HeroSection, SEOConfig, Lead
├── services.py        ← register_lead, get_home_view_data (aggregator)
├── selectors.py       ← get_seo_config, get_active_landing, get_leads_count
├── sitemaps.py        ← DynamicSitemap: recorre catálogo de Orchestrator
├── seo_engine.py      ← inject_metadata, generate_json_ld, build_og_tags
├── exceptions.py      ← LeadError, SEOConfigError
├── migrations/
│   └── 0001_initial.py
├── templates/
│   ├── home/
│   │   ├── landing.html           ← layout principal con bloques temáticos
│   │   └── fallback/
│   │       └── landing_minimal.html  ← HTML puro indexable (sin Theme, sin JS)
│   └── cotton/
│       ├── hero_section.html          ← Alpine.js fade-in (no penaliza LCP)
│       ├── pricing_table.html         ← toggle Mensual/Anual con Alpine.js
│       └── testimonial_slider.html
└── tests/
    ├── test_aggregator.py
    ├── test_seo_engine.py
    └── test_lead_capture.py
```

### Modelos de Datos

**`LandingPage`** (schema `tenant_{slug}`)
| Campo | Descripción |
|---|---|
| `id` UUID | — |
| `tenant_slug` CharField | — |
| `slug` CharField | `/` para raíz, `/pricing` para precios |
| `title` CharField | — |
| `is_published` BooleanField | visible al público |
| `published_at` DateTime null | — |

**`HeroSection`** (schema `tenant_{slug}`)
| Campo | Descripción |
|---|---|
| `landing` OneToOneFK | — |
| `headline` CharField | titular principal |
| `subtitle` CharField | — |
| `cta_text` CharField | texto del botón de acción |
| `cta_url` URLField | — |
| `hero_image_url` URLField null | — |

**`SEOConfig`** (schema `tenant_{slug}`)
| Campo | Descripción |
|---|---|
| `landing` OneToOneFK | — |
| `meta_title` CharField | — |
| `meta_description` CharField(160) | — |
| `og_image_url` URLField null | imagen OpenGraph |
| `json_ld_type` CharField | `SoftwareApplication`, `Service` |

**`Lead`** (schema `tenant_{slug}`) — prospecto pre-registro
| Campo | Descripción |
|---|---|
| `id` UUID | — |
| `email` EmailField | — |
| `source` CharField | `hero_cta`, `pricing_table`, `footer` |
| `captured_at` DateTime | — |
| `converted_to_user` BooleanField | si ya se registró en Profiles |

### Aggregator Pattern

```python
# home/services.py
def get_home_view_data(user=None, tenant_slug=None):
    data = {
        "landing": selectors.get_active_landing(tenant_slug),
        "seo": selectors.get_seo_config(tenant_slug),
    }
    # Catálogo: Orchestrator o fallback
    if apps.is_installed('apps.orchestrator'):
        data["catalog"] = orchestrator_selectors.get_public_catalog()
    else:
        data["catalog"] = []  # → UI muestra "Próximamente"
    
    # Ofertas: Marketing o fallback
    if apps.is_installed('apps.marketing'):
        data["featured_promos"] = marketing_selectors.get_featured_promos(tenant_slug)
    else:
        data["featured_promos"] = []  # → UI oculta labels de oferta
    
    # Contexto de usuario si autenticado
    if user and apps.is_installed('apps.profiles'):
        data["user_status"] = profiles_selectors.get_user_status(user)
    
    return data
```

### SEO Engine (Estructura)

```python
# home/seo_engine.py
def inject_metadata(landing, seo_config):
    return {
        "title": seo_config.meta_title,
        "description": seo_config.meta_description,
        "og_title": seo_config.meta_title,
        "og_image": seo_config.og_image_url,
        "json_ld": generate_json_ld(seo_config.json_ld_type, landing),
    }

# Genera JSON-LD para Google: SoftwareApplication con precio
def generate_json_ld(schema_type, landing):
    return {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": landing.title,
        "offers": {"@type": "Offer", "price": "..."}
    }
```

---

## § 4 — EL ÁRBOL: User Stories de Cimientos a Acabados

| US ID | Historia | SP | Sprint | Estado |
|---|---|---|---|---|
| US-009-01 | `LandingPage` + `HeroSection` + `SEOConfig` models + admin básico | 3 | Sprint-2 | 🔲 Sin US file |
| US-009-02 | `get_home_view_data` aggregator + fallbacks explícitos | 3 | Sprint-2 | 🔲 Sin US file |
| US-009-03 | SEO Engine: MetaTags, OpenGraph, JSON-LD + Sitemap dinámico | 3 | Sprint-2 | 🔲 Sin US file |
| US-009-04 | `Lead` model + `register_lead` service | 2 | Sprint-2 | 🔲 Sin US file |
| US-009-05 | Cotton components: hero_section (Alpine fade-in), pricing_table (toggle mes/año) | 3 | Sprint-3 | 🔲 Sin US file |

### Dependencias

```
US-009-01 (Models) ──→ US-009-02 (aggregator necesita LandingPage)
                   ──→ US-009-03 (SEO engine necesita SEOConfig)
                   ──→ US-009-04 (Lead es propio de Home)
US-009-01 + US-009-02 + US-009-03 ──→ US-009-05 (Cotton consume todo)
```

---

## § 5 — BLUEPRINTS DE REFERENCIA

| ID | Documento | Qué gobierna |
|---|---|---|
| CC-9 | `Docs/1-Core_Concept/9-home-app-cc.md` | Visión, Aggregator Pattern, SEO dinámico |
| HM-2 | `9-Home-App/2-modelos-home-hm.md` | Modelos exactos |
| HM-3 | `9-Home-App/3-service-selector-contratos-home-hm.md` | Contratos públicos |
| HM-4 | `9-Home-App/4-endpoints-home-hm.md` | Endpoints públicos y SEO |

---

## § 6 — DEFINITION OF DONE

EPI-009 está Done cuando:

- [ ] Landing pública renderiza con catálogo de Orchestrator (o "Próximamente" si no instalado)
- [ ] Pricing table tiene toggle Mensual/Anual reactivo con Alpine.js
- [ ] `<meta>` OpenGraph y JSON-LD correcto en `<head>` de la landing (verificable con Google Rich Results Test)
- [ ] `register_lead("prospect@email.com", source="hero_cta")` crea Lead en DB
- [ ] Con Theme no instalado → `landing_minimal.html` carga correctamente, sin errores JS, con HTML válido
- [ ] `GET /sitemap.xml` retorna URLs válidas del catálogo público
- [ ] Marketing no instalado → precios sin etiquetas de oferta, sin errores
- [ ] `pytest apps/home/` pasa con tests de aggregator (mock de apps externas) y fallbacks
- [ ] `product-backlog.md` actualizado: US-009-01..05 con estados correctos
