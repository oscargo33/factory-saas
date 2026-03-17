# EPI-005 — Marketing: El Motor de Conversión y Descuentos

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** EPI-005
**Tipo:** Commercial Epic — Capa 3, optimizador de precio y captación
**Prioridad:** 3 — Mejora la tasa de conversión; no bloquea ventas base
**Sprint objetivo:** Sprint-2
**Dependencias:** EPI-000 Done, EPI-CORE Done, EPI-004 (Orchestrator para precios base)
**Blueprints fuente:**
- `Docs/1-Core_Concept/5-marketing-app-cc.md`
- `Docs/2-Design-Concept/5-Marketing-App/` (10 documentos)

---

## § 1 — EL ALMA: Visión y Razón de Existir

### ¿Qué Problema Resuelve?

Un SaaS puede vender sin Marketing — al precio de lista, sin descuentos, sin urgencia. Pero la diferencia entre una tasa de conversión del 2% y el 8% puede ser un cupón de bienvenida, un banner de campaña de temporada, o un contador de "Oferta termina en 24h".

EPI-005 es el **motor de incentivos económicos**: una capa que se aplica _encima_ del catálogo del Orchestrator para hacer que la decisión de compra sea más fácil y urgente. Si la desactivas, el SaaS sigue vendiendo a precio completo. Si la activas, el SaaS se vuelve comercialmente agresivo.

### La Promesa

`apply_marketing_to_product(product, user, coupon_code)` retorna el mejor precio posible aplicando todas las reglas vigentes. Nunca hace más de eso — no modifica productos, no procesa pagos, no guarda órdenes.

Si Marketing no está instalado, Orders asume `descuento = Decimal('0.00')` y continúa.

---

## § 2 — LA FILOSOFÍA: Principios Fundacionales Aplicados

| Principio | Cómo se aplica en EPI-005 |
|---|---|
| **Degradación Graciosa** | Marketing caído → Orders usa `Decimal('0.00')`. Orchestrator no disponible → Marketing devuelve `[]`. |
| **Aislamiento Total** | `DiscountRule`, `Coupon`, `Campaign` en schema `tenant_{slug}`. Cupones de Acme no afectan a Globex. |
| **Service/Selector** | `apply_marketing_to_product` es un service consultivo (no modifica productos). `get_active_promos` es un selector puro. |
| **El mejor precio gana** | Si un producto tiene múltiples reglas activas y un cupón, el sistema elige la combinación más beneficiosa para el cliente. |

---

## § 3 — LA ARQUITECTURA: Lo Que EPI-005 Crea

### Estructura de Archivos

```
apps/marketing/
├── models.py          ← DiscountRule, Coupon, Campaign, CouponUsage
├── services.py        ← apply_marketing_to_product, validate_coupon, deactivate_expired_campaigns
├── selectors.py       ← get_active_promos, get_featured_promos, get_discount_for_product
├── exceptions.py      ← CouponNotFound, CouponExpired, CouponLimitReached, DiscountError
├── migrations/
│   └── 0001_initial.py
├── templates/
│   ├── marketing/
│   │   └── fallback/
│   │       └── no_offers.html     ← mensaje "Sin ofertas activas" sin Theme
│   └── cotton/
│       ├── promo_banner.html
│       ├── coupon_input.html       ← Alpine.js fetch asíncrono para validar cupón
│       └── countdown_timer.html   ← urgencia con Alpine.js reactivo
└── tests/
    ├── test_discount_engine.py
    ├── test_coupon_validation.py
    └── test_promos.py
```

### Modelos de Datos

**`DiscountRule`** (schema `tenant_{slug}`)
| Campo | Descripción |
|---|---|
| `id` UUID | — |
| `name` CharField | "Descuento Navidad 2026" |
| `discount_type` CharField | `percentage`, `fixed_amount` |
| `discount_value` DecimalField | 10.00 = 10% o $10 fijos |
| `applies_to` JSONB | lista de `product_ids` o vacío = todos |
| `valid_from` DateTime | inicio de vigencia |
| `valid_until` DateTime null | null = indefinida |
| `campaign` FK null | agrupador Campaign |
| `is_active` BooleanField | — |

**`Coupon`** (schema `tenant_{slug}`)
| Campo | Descripción |
|---|---|
| `id` UUID | — |
| `code` CharField | código alfanumérico único por tenant |
| `discount_type` CharField | `percentage`, `fixed_amount` |
| `discount_value` DecimalField | — |
| `max_uses` IntegerField null | null = uso ilimitado |
| `current_uses` IntegerField | — |
| `valid_until` DateTime null | — |
| `is_active` BooleanField | — |

**`Campaign`** (schema `tenant_{slug}`)
— Agrupador de DiscountRules y Coupons bajo un concepto: "Black Friday 2026".

### Contratos Públicos Expuestos

| Contrato | Firma | Fallback |
|---|---|---|
| `apply_marketing_to_product` | `(product, user, coupon_code?) → {final_price, savings, applied_rules}` | `{final_price: product.price, savings: 0, applied_rules: []}` |
| `get_featured_promos` | `(tenant_slug) → list[PromoData]` | `[]` |
| `get_active_promos` | `(tenant_slug) → list[Campaign]` | `[]` |

### Componente Cotton coupon_input (Alpine.js)

```html
<!-- templates/cotton/coupon_input.html -->
<div x-data="{ code: '', result: null, loading: false }">
  <input x-model="code" type="text" placeholder="Código de descuento" />
  <button @click="
    loading = true;
    fetch('/api/marketing/validate-coupon/', {method:'POST', body: JSON.stringify({code})})
      .then(r => r.json())
      .then(data => { result = data; loading = false; })
  " :disabled="loading">
    <span x-show="!loading">Aplicar</span>
    <span x-show="loading">Validando...</span>
  </button>
  <p x-show="result?.valid" class="text-green-500">Descuento aplicado</p>
  <p x-show="result?.error" class="text-red-500" x-text="result?.error"></p>
</div>
```

---

## § 4 — EL ÁRBOL: User Stories de Cimientos a Acabados

| US ID | Historia | SP | Sprint | Estado |
|---|---|---|---|---|
| US-005-01 | `DiscountRule` + `Coupon` models + `validate_coupon` service | 3 | Sprint-2 | 🔲 Sin US file |
| US-005-02 | `apply_marketing_to_product` engine (mejor precio) | 3 | Sprint-2 | 🔲 Sin US file |
| US-005-03 | `Campaign` model + `get_active_promos` + `get_featured_promos` selectors | 2 | Sprint-2 | 🔲 Sin US file |
| US-005-04 | Cotton components: promo_banner, coupon_input (Alpine), countdown_timer | 3 | Sprint-2 | 🔲 Sin US file |

### Dependencias

```
US-005-01 (Coupon) ──→ US-005-02 (engine necesita coupon validation)
US-005-03 (Campaign) → puede ir paralelo a US-005-01
US-005-01 + US-005-02 + US-005-03 ──→ US-005-04 (Cotton consume todo)
```

---

## § 5 — BLUEPRINTS DE REFERENCIA

| ID | Documento | Qué gobierna |
|---|---|---|
| CC-5 | `Docs/1-Core_Concept/5-marketing-app-cc.md` | Visión, Price Resolver, fallbacks |
| MK-2 | `5-Marketing-App/2-modelos-marketing-md.md` | Modelos exactos |
| MK-3 | `5-Marketing-App/3-service-selector-contratos-marketing-md.md` | apply_marketing_to_product |
| MK-4 | `5-Marketing-App/4-endpoints-middleware-marketing-md.md` | Endpoints de validación de cupón |
| MK-5 | `5-Marketing-App/5-campaigns-fallback-marketing-md.md` | Campaigns y fallback |

---

## § 6 — DEFINITION OF DONE

EPI-005 está Done cuando:

- [ ] `apply_marketing_to_product(product, user, "BFRIDAY25")` aplica descuento correcto si el cupón es válido
- [ ] Cupón con `max_uses=1` ya usado → `CouponLimitReached`, no se aplica
- [ ] Cupón expirado → `CouponExpired`, checkout continúa a precio de lista
- [ ] `get_featured_promos("acme")` retorna solo campañas activas del tenant "acme"
- [ ] Con Marketing no instalado → Orders crea orden con `discount=Decimal('0.00')` sin errores
- [ ] Componente `coupon_input` valida cupón vía fetch asíncrono sin recargar página
- [ ] `pytest apps/marketing/` pasa con tests del engine de descuentos y validación de cupones
- [ ] `product-backlog.md` actualizado: US-005-01..04 con estados correctos
