# US-001-01 — ThemeConfig Model + Migración

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** US-001-01
**Epic:** [EPI-001 — Theme / Base Visual e i18n](epic.md)
**Prioridad:** 5 (primer item post-infra)
**SP:** 3 | **Sprint:** Sprint-1 | **Estado:** Planned
**Design Anchor:** `Docs/2-Design-Concept/1-Theme-App/2-modelos-theme-th.md`
**Depende de:** US-000-02 (schema router activo)

---

## Historia

**Como** administrador de tenant
**Quiero** que exista el modelo `ThemeConfig` con tokens visuales por tenant
**Para** que las apps puedan leer colores, fuentes y radio de los componentes desde la base de datos

---

## Criterios de Aceptación

- [ ] Modelo `ThemeConfig` existe en `apps/theme/models.py` con todos los campos definidos en `TH-2-MDL`
- [ ] Solo 1 registro activo por `tenant_slug` (constraint `unique_together` o `unique`)
- [ ] Migración `apps/theme/migrations/0001_initial.py` corre en schema tenant sin errores
- [ ] Valores de color validados: validator que rechaza strings que no sean HEX (#RRGGBB)
- [ ] Si no existe `ThemeConfig` para el tenant, `ThemeSelector.get_config()` devuelve defaults globales definidos en `settings/theme_defaults.py`

---

## Tasks

- [ ] **TASK-01** (1h) `@backend` — Crear `apps/theme/models.py` con clase `ThemeConfig(models.Model)` y campos: `tenant_slug (unique)`, `primary_color`, `secondary_color`, `bg_color`, `text_color`, `font_body`, `font_heading`, `radius_base`, `is_active`, `created_at`, `updated_at`
- [ ] **TASK-02** (0.5h) `@backend` — Crear `apps/theme/validators.py` con `validate_hex_color(value)` que lanza `ValidationError` si el string no coincide con regex `^#([A-Fa-f0-9]{6})$`
- [ ] **TASK-03** (0.5h) `@backend` — Correr `python manage.py makemigrations theme` y verificar que `0001_initial.py` se genera con todos los campos; commitear
- [ ] **TASK-04** (1h) `@backend` — Crear `apps/theme/selectors.py` con `get_config(tenant_slug: str) -> dict` que intenta `ThemeConfig.objects.get(tenant_slug=tenant_slug, is_active=True)` y en `DoesNotExist` retorna `settings.THEME_DEFAULTS`
- [ ] **TASK-05** (0.5h) `@backend` — Crear `factory_saas/settings/theme_defaults.py` con dict `THEME_DEFAULTS` con valores fallback neutrales (blanco/negro, font sans-serif, radius 0.375rem)
- [ ] **TASK-06** (1h) `@backend` — Crear `tests/theme/test_theme_config.py` con 3 tests: crear `ThemeConfig`, validar color HEX inválido lanza error, `get_config` retorna defaults si no existe registro

---

## DoD Checklist

- [ ] `pytest tests/theme/` pasa con 0 fallos
- [ ] `python manage.py migrate --schema=test_tenant` crea tabla `theme_themeconfig`
- [ ] Validator rechaza `"red"` y acepta `"#FF0000"`
- [ ] PR revisado y aprobado
- [ ] CI pasa
