# EPI-CORE — Factory SaaS: Fundamentos, Arquitectura Global y Contratos del Sistema

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** EPI-CORE
**Tipo:** Portfolio Epic — Padre de todos los Epics
**Prioridad:** ABSOLUTA — Define las reglas que gobiernan cada decisión del proyecto
**Sprint objetivo:** Pre-Sprint (diseño) + Sprint-0 (materialización del esqueleto)
**Blueprints fuente:**
- `Docs/1-Core_Concept/0-factory_saas-cc.md`
- `Docs/2-Design-Concept/0-Factory-Saas/` (27 documentos de diseño global)

---

## § 1 — EL ALMA: Visión y Razón de Existir

### ¿Qué es Factory SaaS?

Factory SaaS es una **plataforma multi-tenant** que actúa como fábrica de productos digitales. Su propósito es permitir que múltiples clientes (tenants) operen instancias independientes de un producto (el **Product Core**) sobre una infraestructura compartida, sin que ningún tenant pueda ver ni afectar los datos de otro.

No es un monolito que sirve a un cliente. No es un sistema de microservicios separados por cliente. Es un **SaaS factory**: una sola aplicación Django que al recibir una petición web identifica el tenant, activa su contexto de datos aislado, y sirve la experiencia correcta al usuario correcto.

### El Problema que Resuelve

Un cliente (tenant) quiere:
- Su propio look and feel (colores, fuentes, idioma)
- Sus propios usuarios, roles y permisos
- Su propia instancia del producto con su catálogo y precios
- Sus propias órdenes y transacciones financieras
- Soporte independiente

Sin tener que pagar ni operar su propia infraestructura.

### La Filosofía Fundacional

**Tres principios que gobiernan absolutamente cada decisión técnica:**

| Principio | Enunciado | Consecuencia en código |
|---|---|---|
| **Degradación Graciosa** | Si la App X no está, la App Y sigue funcionando con valor neutro | Toda dependencia entre apps tiene fallback explícito: `0`, `False`, `[]`, key original |
| **Aislamiento Total de Tenants** | Un tenant jamás puede ver ni modificar datos de otro, por construcción | Schema PostgreSQL separado por tenant; ninguna query sin filtro de tenant |
| **Independencia de Apps** | Ninguna app importa modelos de otra; todas se comunican por contratos | Escritura solo por `services.py`, lectura solo por `selectors.py` de la app dueña |

Estos principios **no son sugerencias**. Son restricciones de diseño. Si una propuesta técnica viola uno de ellos, la propuesta está mal.

---

## § 2 — LA PROMESA: Mapa del Sistema y Capas

### Arquitectura en Capas (Quién Depende de Quién)

```
┌─────────────────────────────────────────────────┐
│  CAPA 4: Relación y Superficie                  │
│  App 8 Support       App 9 Home                 │
├─────────────────────────────────────────────────┤
│  CAPA 3: Comercial / Transaccional              │
│  App 5 Marketing   App 6 Orders   App 7 Payment │
├─────────────────────────────────────────────────┤
│  CAPA 2: Contexto e Integración                 │
│  App 3 Profiles    App 4 Product Orchestrator   │
├─────────────────────────────────────────────────┤
│  CAPA 1: ADN (Cimientos del Sistema)            │
│  App 1 Theme (Design + i18n)                    │
│  App 2 API / Telemetry (Observabilidad)         │
├─────────────────────────────────────────────────┤
│  CAPA 0: Infraestructura (EPI-000)              │
│  Django Project + PostgreSQL + Redis + Docker   │
└─────────────────────────────────────────────────┘
```

**Flujo de valor de una compra:**
```
Home (vitrina) → Profiles (identidad) → Orchestrator (catálogo)
→ Marketing (precio) → Orders (carrito) → Payment (cobro)
→ Profiles (activación entitlement) → Support (asistencia)
→ API/Telemetry (observabilidad de todo)
```

Cualquier eslabón puede fallar. El sistema debe degradar, no romper.

### Mapa de Responsabilidades y Límites

| App | Scope (qué hace) | No Scope (qué NO hace) |
|---|---|---|
| 1 Theme | Design system, tokens CSS, Cotton, i18n | Cobros, órdenes, entitlements |
| 2 API/Telemetry | Métricas, push/pull con La Central, trazabilidad | Lógica comercial y checkout |
| 3 Profiles | Identidad, tenancy, membresías, RBAC | Pricing, pagos, descuentos |
| 4 Product Orchestrator | Catálogo funcional, adaptadores al core, entitlements | Procesamiento de pago |
| 5 Marketing | Reglas de promociones y cupones | Persistencia financiera |
| 6 Orders | Carrito, snapshots, ciclo de vida de orden | Ejecución financiera real |
| 7 Payment | Pasarelas, webhooks, conciliación, suscripciones | Ownership de catálogo |
| 8 Support | Tickets, asistencia IA, retención | Autorización de acceso al producto |
| 9 Home | Fachada pública, SEO, agregación visual | Reglas de negocio transaccionales |

---

## § 3 — EL CEREBRO: Arquitectura Global y Reglas No Negociables

### 3.1 Estructura de Carpetas del Proyecto

Lo que crea EPI-CORE — el esqueleto sobre el que todos los Epics añaden carne:

```
factory_saas/               ← proyecto Django raíz
├── settings/
│   ├── base.py             ← INSTALLED_APPS, MIDDLEWARE, DB, CACHES, CELERY
│   ├── dev.py              ← overrides locales
│   ├── test.py             ← CELERY_ALWAYS_EAGER=True, DB en memoria
│   └── prod.py             ← SECURE_*, ALLOWED_HOSTS, sentry
├── urls.py                 ← router raíz (incluye urls de cada app)
├── celery.py               ← app Celery + autodiscover
├── wsgi.py / asgi.py
└── theme_defaults.py       ← DEFAULT_THEME_TOKENS (fallback global de colores)

apps/                       ← contenedor de todas las apps
├── __init__.py
├── core/                   ← tenants, usuarios globales, excepciones base
│   ├── models.py           ← Tenant(slug, name, is_active), Membership
│   ├── services.py         ← create_tenant(), deactivate_tenant()
│   ├── selectors.py        ← get_tenant_by_slug(), get_active_memberships()
│   ├── exceptions.py       ← FactoryBaseException, ServiceError, NotFoundError…
│   ├── middleware.py       ← TenantMiddleware (resolución de slug → schema)
│   ├── db_router.py        ← TenantSchemaRouter (SET search_path)
│   └── tests/
│       └── test_tenancy.py
├── theme/                  ← (creado por EPI-001)
├── api/                    ← (creado por EPI-002)
├── profiles/               ← (creado por EPI-003)
├── orchestrator/           ← (creado por EPI-004)
├── marketing/              ← (creado por EPI-005)
├── orders/                 ← (creado por EPI-006)
├── payments/               ← (creado por EPI-007)
├── support/                ← (creado por EPI-008)
└── home/                   ← (creado por EPI-009)

templates/
├── base.html               ← layout raíz (hereda tokens de Theme o usa defaults)
└── fallback_layout.html    ← layout de emergencia sin Theme

static/                     ← CSS compilado, JS init
tests/
├── contracts/              ← contract tests inter-app
└── test_smoke.py           ← django check + health básico
```

### 3.2 Patrón Service/Selector (DC-12 — obligatorio en toda la fábrica)

```
models.py    ← solo definición de campos. Cero lógica.
services.py  ← escritura, transacciones, eventos. Nunca retorna None.
selectors.py ← lectura pura. Sin side-effects. Cacheable.
views.py     ← orquesta: valida entrada → llama service/selector → retorna respuesta
tasks.py     ← Celery tasks. Invocan services internamente.
exceptions.py← excepciones de dominio propias del app.
```

**Regla de naming de services:**
- Formato: `{verbo}_{sustantivo}(params) → DomainObject`
- Ejemplo: `create_tenant(name, slug, owner_id) → Tenant`
- Los services **nunca retornan None** para señalar fallo — elevan excepción de dominio

**Jerarquía de excepciones base (en `apps/core/exceptions.py`):**
```python
FactoryBaseException
├── ServiceError
│   ├── ValidationError
│   ├── BusinessRuleViolation
│   └── StateConflict
├── NotFoundError
└── TenantNotFoundError
```

### 3.3 Aislamiento Multi-Tenant: Schema-per-Tenant (DC-13)

```
PostgreSQL (única instancia)
├── schema: public           ← auth_user, core_tenant, core_membership
├── schema: tenant_acme      ← todas las tablas de negocio del tenant "acme"
└── schema: tenant_globex    ← todas las tablas de negocio del tenant "globex"
```

**Flujo de un request:**
```
Request https://acme.factory.com/dashboard/
  → Nginx → TenantMiddleware
  → extrae slug "acme" del Host
  → busca en Redis cache (TTL 5 min) → si no, SELECT public.core_tenant WHERE slug='acme'
  → si no existe → 404 {"error": "tenant_not_found"}
  → si existe → request.tenant = <Tenant>
  → TenantSchemaRouter: SET search_path TO tenant_acme, public
  → View: queries ORM operan en tenant_acme automáticamente
```

**Regla absoluta:** Ninguna query de negocio sin `tenant_id` / `tenant_slug` implícito en el search_path. El ORM no necesita filtros manuales por tenant — el schema lo garantiza por construcción.

### 3.4 Contratos Públicos Inter-App (DC-16 — la única forma de comunicación)

Ninguna app importa modelos de otra. Toda comunicación es por estos contratos:

**App `core` (Tenants y Usuarios) — disponible para todas las apps:**
| Función | Tipo | Firma |
|---|---|---|
| `get_tenant_by_slug` | Selector | `(slug: str) → Tenant \| None` |
| `get_user_by_id` | Selector | `(user_id: int) → User \| None` |
| `get_active_memberships` | Selector | `(tenant_id: int) → QuerySet` |
| `create_tenant` | Service | `(name, slug, owner_id) → Tenant` |

**Valores neutrales de fallback cuando una app no está instalada:**
```python
if not apps.is_installed('apps.theme'):
    return {"theme": DEFAULT_THEME_TOKENS}
# Marketing no disponible → descuento = Decimal('0.00')
# Theme no disponible → renders fallback_layout.html
# AI Support no disponible → formulario HTML básico
```

**Verificación obligatoria antes de consumir una app:**
```python
from django.apps import apps
if apps.is_installed('apps.marketing'):
    discount = marketing_selectors.get_discount(tenant_slug, product_id)
else:
    discount = Decimal('0.00')
```

### 3.5 Seguridad Global (DC-18 — controles no negociables)

| Amenaza OWASP | Control implementado |
|---|---|
| A01 Broken Access Control | `TenantMiddleware` + `search_path` + RBAC por `Membership.role` |
| A02 Cryptographic Failures | HTTPS en Nginx, argon2 para passwords, secretos en env vars (DC-3) |
| A03 Injection | ORM parametrizado, raw SQL prohibido en views/services, auto-escape en templates |
| A04 Insecure Design | Defense in depth: Nginx → Middleware → View Permissions → Service → DB |
| A05 Misconfiguration | `DEBUG=False` en prod, `ALLOWED_HOSTS` estricto, Admin URL randomizada |

**Reglas absolutas de seguridad en código:**
- `subprocess` prohibido en views y services
- `{% autoescape off %}` prohibido en templates
- `innerHTML` con datos de usuario prohibido en Alpine.js
- Datos financieros (tarjeta, CVV) nunca almacenados — delegado a gateway PCI-DSS

---

## § 4 — LOS CONTRATOS: Lo que EPI-CORE Entrega a los Demás

EPI-CORE no es solo configuración. Crea piezas concretas que todos los Epics posteriores consumen como dado:

| Artefacto creado en EPI-CORE | Consumido por |
|---|---|
| `apps/core/models.py` — Tenant, Membership | Todos los Epics |
| `apps/core/middleware.py` — TenantMiddleware | Todos los Epics (activa schema) |
| `apps/core/db_router.py` — TenantSchemaRouter | Todos los Epics (aislamiento DB) |
| `apps/core/exceptions.py` — jerarquía base | Todos los services de todos los Epics |
| `apps/core/selectors.py` — get_tenant_by_slug | EPI-001, EPI-002, EPI-003... |
| `factory_saas/theme_defaults.py` — DEFAULT_THEME_TOKENS | EPI-001-theme (fallback) |
| `templates/fallback_layout.html` | Todos los Epics UI |
| `factory_saas/settings/base.py` — INSTALLED_APPS base | Todos los Epics |
| `factory_saas/urls.py` raíz | Todos los Epics (registran sus prefijos aquí) |

---

## § 5 — EL ÁRBOL: User Stories de Cimientos a Acabados

### Sprint-0 — El Esqueleto Físico (EPI-000 gestiona este trabajo)

| US ID | Historia | Archivo |
|---|---|---|
| US-000-01 | Docker dev environment | [EPI-000-infra/US-000-01](../EPI-000-infra/US-000-01-docker-dev-environment.md) |
| US-000-02 | PostgreSQL + schema router | [EPI-000-infra/US-000-02](../EPI-000-infra/US-000-02-postgresql-schema-router.md) |
| US-000-03 | CI pipeline | [EPI-000-infra/US-000-03](../EPI-000-infra/US-000-03-ci-pipeline.md) |
| US-000-04 | Redis + Celery baseline | [EPI-000-infra/US-000-04](../EPI-000-infra/US-000-04-redis-celery-baseline.md) |

### Sprint-0 — El Esqueleto del Proyecto Django (EPI-CORE propio)

Las siguientes User Stories son propias de EPI-CORE y se ejecutan en paralelo con EPI-000:

| US ID | Historia | SP | Sprint |
|---|---|---|---|
| US-CORE-01 | Estructura de carpetas `apps/` + `factory_saas/settings/` + `urls.py` raíz | 2 | Sprint-0 |
| US-CORE-02 | `apps/core/models.py`: Tenant, Membership + migración 0001 en schema `public` | 3 | Sprint-0 |
| US-CORE-03 | `apps/core/exceptions.py`: jerarquía base de excepciones de dominio | 1 | Sprint-0 |
| US-CORE-04 | `apps/core/middleware.py`: TenantMiddleware + TenantSchemaRouter | 3 | Sprint-0 |
| US-CORE-05 | `apps/core/selectors.py`: get_tenant_by_slug, get_active_memberships | 2 | Sprint-0 |
| US-CORE-06 | `factory_saas/theme_defaults.py` + `templates/fallback_layout.html` | 1 | Sprint-0 |
| US-CORE-07 | `apps/core/services.py`: create_tenant, deactivate_tenant + tests de aislamiento | 3 | Sprint-0 |

### Sprint-1 y posteriores (Epics de apps individuales)

Cada Epic hijo arranca solo cuando EPI-CORE y EPI-000 están en Done:

| Epic | Qué añade encima de EPI-CORE | Sprint inicio |
|---|---|---|
| [EPI-001-theme](../EPI-001-theme/epic.md) | Design system, tokens CSS dinámicos, i18n | Sprint-1 |
| [EPI-002-api](../EPI-002-api/epic.md) | Telemetría, métricas, contratos de observabilidad | Sprint-1 |
| [EPI-003-profile](../EPI-003-profile/epic.md) | Identidad, membresías, RBAC | Sprint-1 |
| [EPI-004-orchestrator](../EPI-004-orchestrator/epic.md) | Catálogo, entitlements, Product Core adapter | Sprint-1 |
| [EPI-006-orders](../EPI-006-orders/epic.md) | Carrito, snapshots, ciclo de vida de orden | Sprint-1 |
| [EPI-007-payments](../EPI-007-payments/epic.md) | Pasarelas, webhooks, conciliación | Sprint-1 |
| [EPI-005-marketing](../EPI-005-marketing/epic.md) | Campañas, descuentos, promotions | Sprint-2 |
| [EPI-008-support](../EPI-008-support/epic.md) | Tickets, IA RAG, retención | Sprint-2 |
| [EPI-009-home](../EPI-009-home/epic.md) | Fachada pública, SEO, home personalizada | Sprint-2 |

---

## § 6 — LA VERIFICACIÓN: Definition of Done del Epic CORE

Este Epic está Done cuando cualquier desarrollador nuevo puede:

- [ ] Clonar el repo y ejecutar `docker compose up --build` sin errores
- [ ] Correr `python manage.py create_tenant --slug=demo --name="Demo"` y verificar schema `tenant_demo` creado en PostgreSQL
- [ ] Correr `pytest apps/core/tests/` con 0 fallos incluyendo test de aislamiento entre 2 tenants
- [ ] Un request a subdominio inexistente devuelve `404 {"error": "tenant_not_found"}`
- [ ] Un request a subdominio válido activa el schema correcto (verificable en logs de DB)
- [ ] `from apps.core.exceptions import FactoryBaseException` importa sin errores desde cualquier app
- [ ] `from apps.core.selectors import get_tenant_by_slug` importa sin errores desde cualquier app
- [ ] `templates/fallback_layout.html` renderiza un HTML válido sin Theme instalado
- [ ] CI verde: pytest + flake8 + black en PR
- [ ] `product-backlog.md` actualizado con US-CORE-01..07 en estado Done

---

## Blueprints de Referencia Completos

| ID | Documento | Qué gobierna |
|---|---|---|
| CC-0 | `Docs/1-Core_Concept/0-factory_saas-cc.md` | Visión, capas, política de independencia |
| DC-2 | `Docs/2-Design-Concept/0-Factory-Saas/2-Core Automation-specs-fs.md` | Automatización core |
| DC-3 | `Docs/2-Design-Concept/0-Factory-Saas/3-gestion-de-secretos-fs.md` | Secretos y variables |
| DC-4 | `Docs/2-Design-Concept/0-Factory-Saas/4-estructura-de-carpetas-fs.md` | Estructura del proyecto |
| DC-5 | `Docs/2-Design-Concept/0-Factory-Saas/5-configuracion-poetry-fs.md` | Dependencias y pyproject |
| DC-9 | `Docs/2-Design-Concept/0-Factory-Saas/9-configuracion-postgresql-fs.md` | PostgreSQL y schemas |
| DC-12 | `Docs/2-Design-Concept/0-Factory-Saas/12-patron-service-layer-fs.md` | Service/Selector pattern |
| DC-13 | `Docs/2-Design-Concept/0-Factory-Saas/13-router-dinamico-esquemas-fs.md` | Multi-tenancy router |
| DC-16 | `Docs/2-Design-Concept/0-Factory-Saas/16-contratos-inter-app-fs.md` | Contratos inter-app |
| DC-17 | `Docs/2-Design-Concept/0-Factory-Saas/17-diccionario-datos-logico-fs.md` | Diccionario de datos |
| DC-18 | `Docs/2-Design-Concept/0-Factory-Saas/18-matriz-seguridad-compliance-fs.md` | Seguridad y OWASP |
| DC-23 | `Docs/2-Design-Concept/0-Factory-Saas/23-estrategia-migraciones-db-fs.md` | Estrategia de migraciones |
| DC-25 | `Docs/2-Design-Concept/0-Factory-Saas/25-flujo-onboarding-e2e-fs.md` | Onboarding de tenants |
| DC-26 | `Docs/2-Design-Concept/0-Factory-Saas/26-estrategia-testing-fs.md` | Estrategia de testing |
