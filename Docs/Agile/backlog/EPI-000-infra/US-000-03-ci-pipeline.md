# US-000-03 — CI Pipeline (pytest + linting)

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-17

**ID:** US-000-03
**Epic:** [EPI-000 — Core Infra](epic.md)
**Prioridad:** 3
**SP:** 3 | **Sprint:** Sprint-0 | **Estado:** Planned
**Design Anchor:** `Docs/2-Design-Concept/0-Factory-Saas/2-Core Automation-specs-fs.md`

---

## Historia

**Como** equipo de desarrollo
**Quiero** un pipeline CI que ejecute tests y checks de estilo automáticamente en cada PR
**Para** detectar regresiones antes de mergear y mantener calidad de código consistente

---

## Criterios de Aceptación

- [ ] CI se dispara en cada `push` a `main` y en cada PR
- [ ] Pasos: `black --check`, `flake8`, `pytest --tb=short`
- [ ] Si cambia `Docs/`, el pipeline valida consistencia mínima de cabeceras documentales sin depender de registro maestro consolidado
- [ ] El pipeline falla si alguno de los pasos falla
- [ ] Tiempo total de CI < 3 minutos en repositorio base
- [ ] Badge de estado en `README.md`

---

## Tasks

- [ ] **TASK-01** (1h) `@infra` — Crear `.github/workflows/ci.yml` con trigger `push`/`pull_request`, job `test` con steps: `checkout`, `setup-python 3.12`, `pip install poetry`, `poetry install`, `black --check .`, `flake8 .`, `pytest`
- [ ] **TASK-02** (0.5h) `@infra` — Crear `pyproject.toml` sección `[tool.black]` con `line-length = 120` y sección `[tool.flake8]` con `max-line-length = 120, extend-ignore = E203`
- [ ] **TASK-03** (0.5h) `@infra` — Crear `pytest.ini` con `[pytest] python_files = test_*.py, testpaths = tests, addopts = -v --tb=short`
- [ ] **TASK-04** (0.5h) `@backend` — Crear `tests/__init__.py` y `tests/test_smoke.py` con un test `test_django_check` que corre `call_command("check")` y no lanza excepciones
- [ ] **TASK-05** (0.5h) `@docs` — Agregar badge CI en `README.md` raíz: `![CI](https://github.com/ORG/REPO/actions/workflows/ci.yml/badge.svg)`
- [ ] **TASK-06** (0.5h) `@docs` — Definir validación liviana de cabeceras documentales en fase de documentación
- [ ] **TASK-07** (0.5h) `@docs` — Crear workflow dedicado de gobernanza documental sin dependencia a registro maestro consolidado

---

## DoD Checklist

- [ ] CI verde en PR de prueba
- [ ] `pytest tests/test_smoke.py` pasa localmente
- [ ] Black y flake8 no reportan errores en el codebase
- [ ] Validación documental definida para fase activa y ejecutada sin errores
- [ ] README actualizado con badge
- [ ] PR revisado y aprobado
