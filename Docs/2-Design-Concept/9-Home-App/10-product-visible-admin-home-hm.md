# Documento: Producto Visible + Admin App 9 Home

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** HM-10-PV  
**Ubicacion:** `./Docs/2-Design-Concept/9-Home-App/10-product-visible-admin-home-hm.md`  
**Anchor Docs:** `9-home-app-cc.md`, `14-pipeline-tailwind-cotton-fs.md`, `21-product-visible-ux-fs.md`

## 1. Objetivo

Definir experiencia visible publica (landing/SEO/conversion) y CRUD editorial desde admin.

## 2. CRUD en Django Admin (Home)

| Modelo | C | R | U | D | Notas UI Admin |
|---|---|---|---|---|---|
| LandingPage | Si | Si | Si | Si | Editor de bloques con preview |
| HeroSection | Si | Si | Si | Si | Validar responsive y contraste |
| SEOConfig | Si | Si | Si | No | Campos OG/Twitter/JSON-LD |
| Testimonial/FeatureBlock | Si | Si | Si | Si | Orden por prioridad y vigencia |

Criterios admin:
- Preview antes de publicar cambios.
- Historial de publicaciones y rollback simple.

## 3. Interfaz de producto visible

Pantallas minimas:
- Landing principal.
- Pricing/features.
- CTA a signup/login.

Estados UX obligatorios:
- `loading`, `empty`, `error`, `success`.

## 4. Criterios de aceptacion

- Landing permanece operativa aun si faltan apps comerciales.
- SEO dinamico definido por pantalla clave.
- CTA principal direcciona correctamente a flujo de onboarding.
