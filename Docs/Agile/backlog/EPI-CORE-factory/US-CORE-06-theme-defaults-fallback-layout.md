# US-CORE-06 — Theme Defaults y Fallback Layout Global

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-17

**ID:** US-CORE-06
**Epic:** [EPI-CORE — Factory SaaS](EPI-CORE-factory-saas.md)
**Prioridad:** 6
**SP:** 1 | **Sprint:** Sprint-0 | **Estado:** Planned
**Design Anchor:** `Docs/2-Design-Concept/0-Factory-Saas/14-pipeline-tailwind-cotton-fs.md`, `Docs/2-Design-Concept/0-Factory-Saas/21-product-visible-ux-fs.md`

---

## Historia

**Como** sistema con degradación graciosa obligatoria
**Quiero** un fallback visual base y tokens por defecto
**Para** que Home, Profiles y el resto de la UI no rompan cuando Theme todavía no esté instalado

---

## Criterios de Aceptación

- [ ] Existe `factory_saas/theme_defaults.py` con `DEFAULT_THEME_TOKENS`
- [ ] Existe `templates/fallback_layout.html`
- [ ] El fallback es funcional y no depende de Theme
- [ ] La historia refleja el principio de degradación graciosa de EPI-CORE

---

## Tasks

- [ ] **TASK-01** (0.5h) `@frontend` — Crear `factory_saas/theme_defaults.py` con tokens neutrales
- [ ] **TASK-02** (0.5h) `@frontend` — Crear `templates/fallback_layout.html` usable por apps UI

---

## DoD Checklist

- [ ] El fallback visual puede renderizar sin Theme
- [ ] Los tokens default son claros y reutilizables
- [ ] PR revisado y aprobado
