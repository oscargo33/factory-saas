# Product Backlog — Factory SaaS

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-17

**Regla de lectura:** Backlog ordenado por prioridad de entrega. Cada Epic agrupa sus User Stories con SP y sprint asignado. La columna "Archivo US" linkea al documento con las tasks atómicas.

> Trazabilidad: `Core-Concept → Epic.md → User Story → Tasks atómicas (1-8h) → Sprint → DoD`
>
> **🔲 Sin US file** = Historia definida pero sin archivo individual. Crearla antes de asignarla a sprint (Definition of Ready).

---

## EPI-CORE — Factory SaaS: Esqueleto Global del Proyecto
> 📎 [epic.md](EPI-CORE-factory/EPI-CORE-factory-saas.md) · Design: `0-Factory-Saas/` (global) · **7 US · 15 SP · Sprint-0**
> ⚠️ PADRE DE TODOS — Define los principios, contratos y el esqueleto Django que todos heredan.

| # | US ID | Historia | SP | Sprint | Estado | Archivo |
|---|---|---|---|---|---|---|
| 1 | US-CORE-01 | Estructura `apps/` + `factory_saas/settings/` + `urls.py` raíz | 2 | Sprint-0 | Planned | [US-CORE-01](EPI-CORE-factory/US-CORE-01-project-skeleton.md) |
| 2 | US-CORE-02 | `apps/core/models.py`: Tenant, Membership + migración `public` | 3 | Sprint-0 | Planned | [US-CORE-02](EPI-CORE-factory/US-CORE-02-core-models-public.md) |
| 3 | US-CORE-03 | `apps/core/exceptions.py`: jerarquía FactoryBaseException | 1 | Sprint-0 | Planned | [US-CORE-03](EPI-CORE-factory/US-CORE-03-core-exceptions.md) |
| 4 | US-CORE-04 | `apps/core/middleware.py`: TenantMiddleware + TenantSchemaRouter | 3 | Sprint-0 | Planned | [US-CORE-04](EPI-CORE-factory/US-CORE-04-tenant-middleware-router.md) |
| 5 | US-CORE-05 | `apps/core/selectors.py`: get_tenant_by_slug, get_active_memberships | 2 | Sprint-0 | Planned | [US-CORE-05](EPI-CORE-factory/US-CORE-05-core-selectors.md) |
| 6 | US-CORE-06 | `factory_saas/theme_defaults.py` + `templates/fallback_layout.html` | 1 | Sprint-0 | Planned | [US-CORE-06](EPI-CORE-factory/US-CORE-06-theme-defaults-fallback-layout.md) |
| 7 | US-CORE-07 | `apps/core/services.py`: create_tenant, deactivate_tenant + tests aislamiento | 3 | Sprint-0 | Planned | [US-CORE-07](EPI-CORE-factory/US-CORE-07-core-services-isolation-tests.md) |

---

## EPI-000 — Infraestructura Base: Docker, PostgreSQL, CI, Redis
> 📎 [epic.md](EPI-000-infra/epic.md) · Design: `0-Factory-Saas/6..11` · **4 US · 13 SP · Sprint-0**
> ⚠️ BLOQUEANTE — ningún otro Epic puede comenzar sin este completado.

| # | US ID | Historia | SP | Sprint | Estado | Archivo |
|---|---|---|---|---|---|---|
| 8 | US-000-01 | Docker dev environment reproducible | 3 | Sprint-0 | Planned | [US-000-01](EPI-000-infra/US-000-01-docker-dev-environment.md) |
| 9 | US-000-02 | PostgreSQL multi-tenant + schema router | 5 | Sprint-0 | Planned | [US-000-02](EPI-000-infra/US-000-02-postgresql-schema-router.md) |
| 10 | US-000-03 | CI pipeline (pytest + flake8 + black) | 3 | Sprint-0 | Planned | [US-000-03](EPI-000-infra/US-000-03-ci-pipeline.md) |
| 11 | US-000-04 | Redis + Celery worker baseline | 2 | Sprint-0 | Planned | [US-000-04](EPI-000-infra/US-000-04-redis-celery-baseline.md) |

---

## EPI-001 — Theme: Motor de Identidad Visual e i18n
> 📎 [epic.md](EPI-001-theme/epic.md) · Design: `1-Theme-App/` · **5 US · 16 SP · Sprint-1/2**
> Depende de: EPI-000 Done, EPI-CORE Done

| # | US ID | Historia | SP | Sprint | Estado | Archivo |
|---|---|---|---|---|---|---|
| 12 | US-001-01 | `ThemeConfig` model + `get_theme_for_tenant` selector + defaults | 3 | Sprint-1 | Planned | [US-001-01](EPI-001-theme/US-001-01-themeconfig-model.md) |
| 13 | US-001-02 | `Glossary` model + i18n engine (Redis + LibreTranslate) | 5 | Sprint-1 | 🔲 Sin US file | — |
| 14 | US-001-03 | Cotton components library (button, input, modal, card) | 3 | Sprint-1 | 🔲 Sin US file | — |
| 15 | US-001-04 | `base.html` layout maestro + ThemeContextMiddleware | 3 | Sprint-1 | 🔲 Sin US file | — |
| 16 | US-001-05 | Tailwind pipeline + admin ThemeConfig + scripts | 2 | Sprint-2 | 🔲 Sin US file | — |

---

## EPI-002 — API / Telemetry: Observabilidad y La Central
> 📎 [epic.md](EPI-002-api/epic.md) · Design: `2-Api-Telemetry-App/` · **4 US · 12 SP · Sprint-1/2**
> Depende de: EPI-000 Done, EPI-CORE Done

| # | US ID | Historia | SP | Sprint | Estado | Archivo |
|---|---|---|---|---|---|---|
| 17 | US-002-01 | `TelemetryEvent` model + `TelemetryMiddleware` (X-Trace-ID) | 3 | Sprint-1 | 🔲 Sin US file | — |
| 18 | US-002-02 | `PendingMetrics` + push task Celery + retry backoff | 4 | Sprint-1 | 🔲 Sin US file | — |
| 19 | US-002-03 | DRF endpoints pull: health, metrics, audit trail | 3 | Sprint-1 | 🔲 Sin US file | — |
| 20 | US-002-04 | `AuditLog` service para acciones sensibles | 2 | Sprint-2 | 🔲 Sin US file | — |

---

## EPI-003 — Profiles: Identidad, Tenancy y RBAC
> 📎 [epic.md](EPI-003-profile/epic.md) · Design: `3-Profile-App/` · **5 US · 14 SP · Sprint-1/2**
> Depende de: EPI-000 Done, EPI-CORE Done

| # | US ID | Historia | SP | Sprint | Estado | Archivo |
|---|---|---|---|---|---|---|
| 21 | US-003-01 | `Profile` model + `get_display_name` + `get_active_context` selectors | 3 | Sprint-1 | 🔲 Sin US file | — |
| 22 | US-003-02 | RBAC: roles Owner/Admin/Member + `has_permission` selector | 3 | Sprint-1 | 🔲 Sin US file | — |
| 23 | US-003-03 | `invite_user` + `switch_tenant` services | 3 | Sprint-1 | 🔲 Sin US file | — |
| 24 | US-003-04 | Dashboard aggregator (composition pattern) + cotton components | 3 | Sprint-2 | 🔲 Sin US file | — |
| 25 | US-003-05 | Fallback login/dashboard HTML puro (sin Theme) | 2 | Sprint-2 | 🔲 Sin US file | — |

---

## EPI-004 — Product Orchestrator: Catálogo, Entitlements y PlanMatrix
> 📎 [epic.md](EPI-004-orchestrator/epic.md) · Design: `4-Product-Orchestrator-App/` · **5 US · 16 SP · Sprint-1/2**
> Depende de: EPI-000 Done, EPI-CORE Done, EPI-003 (Profiles para contexto de acceso)

| # | US ID | Historia | SP | Sprint | Estado | Archivo |
|---|---|---|---|---|---|---|
| 26 | US-004-01 | `Product` + `Vertical` models + `get_public_catalog` selector | 3 | Sprint-1 | 🔲 Sin US file | — |
| 27 | US-004-02 | `Entitlement` model + `enforce_plan_policy` service | 4 | Sprint-1 | 🔲 Sin US file | — |
| 28 | US-004-03 | Adapter Pattern: `base.py` + `core_app.py` implementación | 3 | Sprint-1 | 🔲 Sin US file | — |
| 29 | US-004-04 | `PlanMatrix` + `change_plan` transaccional + OutboxEvent | 4 | Sprint-2 | 🔲 Sin US file | — |
| 30 | US-004-05 | Cotton components: feature_badge, product_card + fallback UI | 2 | Sprint-2 | 🔲 Sin US file | — |

---

## EPI-006 — Orders: Carrito, Snapshot y Ciclo de Vida de Orden
> 📎 [epic.md](EPI-006-orders/epic.md) · Design: `6-Orders-App/` · **4 US · 14 SP · Sprint-1/2**
> Depende de: EPI-000 Done, EPI-CORE Done, EPI-004 (Orchestrator para validar productos)

| # | US ID | Historia | SP | Sprint | Estado | Archivo |
|---|---|---|---|---|---|---|
| 31 | US-006-01 | `Cart` + `CartItem` models + add_to_cart / remove_from_cart | 3 | Sprint-1 | 🔲 Sin US file | — |
| 32 | US-006-02 | `Order` + `OrderLine` con price_snapshot + state_machine | 4 | Sprint-1 | 🔲 Sin US file | — |
| 33 | US-006-03 | `freeze_cart` transaccional + OutboxEvent(provision.requested) | 4 | Sprint-1 | 🔲 Sin US file | — |
| 34 | US-006-04 | Cotton: cart_drawer, order_summary, add_to_cart_btn (Alpine.js) | 3 | Sprint-2 | 🔲 Sin US file | — |

---

## EPI-007 — Payments: Pasarelas, Webhooks e Idempotencia
> 📎 [epic.md](EPI-007-payments/epic.md) · Design: `7-Payment-App/` · **5 US · 17 SP · Sprint-1/2**
> Depende de: EPI-000 Done, EPI-CORE Done, EPI-006 (Orders para monto e ID de orden)

| # | US ID | Historia | SP | Sprint | Estado | Archivo |
|---|---|---|---|---|---|---|
| 35 | US-007-01 | Provider Pattern: `base.py` + `stripe.py` + `start_session` service | 4 | Sprint-1 | 🔲 Sin US file | — |
| 36 | US-007-02 | `handle_webhook` idempotente + OutboxEvent en transacción atómica | 4 | Sprint-1 | 🔲 Sin US file | — |
| 37 | US-007-03 | `Subscription` model + dunning logic + `cancel_subscription` | 4 | Sprint-2 | 🔲 Sin US file | — |
| 38 | US-007-04 | `Invoice` model + `get_recent_invoices` selector | 2 | Sprint-2 | 🔲 Sin US file | — |
| 39 | US-007-05 | Cotton: checkout_form (Stripe Elements), subscription_badge | 3 | Sprint-2 | 🔲 Sin US file | — |

---

## EPI-005 — Marketing: Descuentos, Cupones y Campañas
> 📎 [epic.md](EPI-005-marketing/epic.md) · Design: `5-Marketing-App/` · **4 US · 11 SP · Sprint-2**
> Depende de: EPI-000 Done, EPI-CORE Done, EPI-004 (Orchestrator para precios base)

| # | US ID | Historia | SP | Sprint | Estado | Archivo |
|---|---|---|---|---|---|---|
| 40 | US-005-01 | `DiscountRule` + `Coupon` models + `validate_coupon` service | 3 | Sprint-2 | 🔲 Sin US file | — |
| 41 | US-005-02 | `apply_marketing_to_product` engine (mejor precio) | 3 | Sprint-2 | 🔲 Sin US file | — |
| 42 | US-005-03 | `Campaign` model + `get_active_promos` + `get_featured_promos` | 2 | Sprint-2 | 🔲 Sin US file | — |
| 43 | US-005-04 | Cotton: promo_banner, coupon_input (Alpine.js), countdown_timer | 3 | Sprint-2 | 🔲 Sin US file | — |

---

## EPI-008 — Support: Ticketing y Agente IA con RAG
> 📎 [epic.md](EPI-008-support/epic.md) · Design: `8-Support-App/` · **5 US · 17 SP · Sprint-2/3**
> Depende de: EPI-000 Done, EPI-CORE Done, EPI-003 (Profiles para historial del usuario)

| # | US ID | Historia | SP | Sprint | Estado | Archivo |
|---|---|---|---|---|---|---|
| 44 | US-008-01 | `Ticket` model + `create_ticket` + state machine (new→resolved) | 3 | Sprint-2 | 🔲 Sin US file | — |
| 45 | US-008-02 | `KnowledgeArticle` + pgvector + búsqueda semántica | 4 | Sprint-2 | 🔲 Sin US file | — |
| 46 | US-008-03 | `ask_ai` RAG engine + `escalate_to_human` service | 4 | Sprint-2 | 🔲 Sin US file | — |
| 47 | US-008-04 | Django Channels WebSocket consumer (chat en tiempo real) | 3 | Sprint-3 | 🔲 Sin US file | — |
| 48 | US-008-05 | Cotton: chat_bubble (Alpine.js), faq_accordion, fallback contact form | 3 | Sprint-2 | 🔲 Sin US file | — |

---

## EPI-009 — Home: Vitrina Pública y SEO
> 📎 [epic.md](EPI-009-home/epic.md) · Design: `9-Home-App/` · **5 US · 14 SP · Sprint-2/3**
> Depende de: EPI-000 Done, EPI-CORE Done, EPI-001 (Theme), EPI-004 (Orchestrator catálogo)

| # | US ID | Historia | SP | Sprint | Estado | Archivo |
|---|---|---|---|---|---|---|
| 49 | US-009-01 | `LandingPage` + `HeroSection` + `SEOConfig` models + admin | 3 | Sprint-2 | 🔲 Sin US file | — |
| 50 | US-009-02 | `get_home_view_data` aggregator + fallbacks explícitos | 3 | Sprint-2 | 🔲 Sin US file | — |
| 51 | US-009-03 | SEO Engine: MetaTags, OpenGraph, JSON-LD + Sitemap dinámico | 3 | Sprint-2 | 🔲 Sin US file | — |
| 52 | US-009-04 | `Lead` model + `register_lead` service | 2 | Sprint-2 | 🔲 Sin US file | — |
| 53 | US-009-05 | Cotton: hero_section (Alpine fade-in), pricing_table (toggle mes/año) | 3 | Sprint-3 | 🔲 Sin US file | — |

---

## Resumen de carga por Sprint

| Sprint | US comprometidas | SP Total | Epics activos |
|---|---|---|---|
| Sprint-0 | 11 (US-CORE-01..07 + US-000-01..04) | 28 | EPI-CORE, EPI-000 |
| Sprint-1 | 18 (US-001..004 en paralelo) | ~52 | EPI-001, EPI-002, EPI-003, EPI-004, EPI-006, EPI-007 |
| Sprint-2 | 22 (US-003..009) | ~62 | EPI-003, EPI-004, EPI-005, EPI-006, EPI-007, EPI-008, EPI-009 |
| Sprint-3 | 3 (US-008-04, US-009-05) | ~9 | EPI-008, EPI-009 |

> **Regla de Sprint-1:** Sprint-1 NO comienza hasta que EPI-CORE Y EPI-000 estén en `Done` completo.

---

## Leyenda de estados

| Estado | Significado |
|---|---|
| `Planned` | US file existe, en backlog, no comprometida en sprint |
| `In Progress` | En sprint activo, asignada a un owner |
| `In Review` | PR abierto, esperando revisión |
| `Done` | DoD checklist completo, mergeado |
| `🔲 Sin US file` | Historia definida en epic.md pero sin archivo US individual — no DoR completo |
