# US-CORE-01 — Estructura Base del Proyecto Django

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-17

**ID:** US-CORE-01
**Epic:** [EPI-CORE — Factory SaaS](EPI-CORE-factory-saas.md)
**Prioridad:** 1
**SP:** 2 | **Sprint:** Sprint-0 | **Estado:** Planned
**Design Anchor:** `Docs/2-Design-Concept/0-Factory-Saas/4-estructura-de-carpetas-fs.md`, `Docs/2-Design-Concept/0-Factory-Saas/5-configuracion-poetry-fs.md`

---

## Historia

**Como** equipo base de la Factory
**Quiero** una estructura inicial consistente de proyecto Django y carpetas de apps
**Para** que los epics posteriores construyan sobre un esqueleto estable, legible y trazable

---

## Criterios de Aceptación

- [ ] Existe la raíz de proyecto `factory_saas/` con `settings/`, `urls.py`, `wsgi.py`, `asgi.py` y `theme_defaults.py`
- [ ] Existe el contenedor `apps/` con `core/` y placeholders coherentes para las apps principales
- [ ] Existe `templates/fallback_layout.html` como layout mínimo compartido
- [ ] La estructura resultante coincide con el blueprint de EPI-CORE y con DC-4-FS
- [ ] La documentación de backlog referencia archivos reales, no solo intención arquitectónica

---

## Tasks

- [ ] **TASK-01** (0.5h) `@backend` — Crear estructura `factory_saas/settings/` con archivos `base.py`, `dev.py`, `test.py`, `prod.py`
- [ ] **TASK-02** (0.5h) `@backend` — Crear `factory_saas/urls.py`, `wsgi.py`, `asgi.py` y `theme_defaults.py`
- [ ] **TASK-03** (0.5h) `@backend` — Crear contenedor `apps/` y carpeta `apps/core/` con `__init__.py`
- [ ] **TASK-04** (0.5h) `@frontend` — Crear `templates/fallback_layout.html` como layout de degradación graciosa
- [ ] **TASK-05** (0.5h) `@docs` — Validar que la estructura final quede trazada en backlog y sprint backlog

---

## DoD Checklist

- [ ] La estructura existe en el repositorio y es navegable sin rutas rotas
- [ ] Las rutas base coinciden con EPI-CORE y DC-4-FS
- [ ] PR revisado y aprobado
