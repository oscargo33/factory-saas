# Sprint-0 — Backlog

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**Período:** 2026-03-16 — 2026-03-29 (2 semanas)
**Objetivo:** Entorno de desarrollo reproducible + CI operativo + schema router multi-tenant listo. Al finalizar este sprint, cualquier desarrollador puede clonar el repo, ejecutar Docker y correr tests.
**Epic asociado:** [EPI-000 — Core Infra](../../backlog/EPI-000-infra/epic.md)
**Capacidad:** ~13 SP (equipo pequeño, sprint fundacional)

---

## Compromisos del Sprint

| Prioridad | US ID | Historia | SP | Owner | Estado |
|---|---|---|---|---|---|
| 1 | [US-000-01](../../backlog/EPI-000-infra/US-000-01-docker-dev-environment.md) | Docker dev environment reproducible | 3 | — | Planned |
| 2 | [US-000-02](../../backlog/EPI-000-infra/US-000-02-postgresql-schema-router.md) | PostgreSQL multi-tenant + schema router | 5 | — | Planned |
| 3 | [US-000-03](../../backlog/EPI-000-infra/US-000-03-ci-pipeline.md) | CI pipeline (pytest + flake8 + black) | 3 | — | Planned |
| 4 | [US-000-04](../../backlog/EPI-000-infra/US-000-04-redis-celery-baseline.md) | Redis + Celery worker baseline | 2 | — | Planned |

**Total comprometido:** 13 SP

---

## Tasks activadas (extraídas de cada US)

### US-000-01 — Docker
- [ ] TASK-01 (2h): Crear `Dockerfile.dev`
- [ ] TASK-02 (2h): Crear `docker-compose.dev.yml`
- [ ] TASK-03 (1h): Crear `scripts/entrypoint.sh`
- [ ] TASK-04 (1h): Crear `factory_saas/settings/dev.py`
- [ ] TASK-05 (0.5h): Crear `.env.dev.example`
- [ ] TASK-06 (0.5h): Actualizar `README.md` con instrucciones

### US-000-02 — PostgreSQL Schema Router
- [ ] TASK-01 (2h): Crear `factory_saas/db_router.py`
- [ ] TASK-02 (1h): Crear `factory_saas/middleware/tenant.py`
- [ ] TASK-03 (2h): Crear `apps/tenants/models.py` + migración `0001`
- [ ] TASK-04 (1h): Crear management command `create_tenant`
- [ ] TASK-05 (1h): Crear `tests/test_schema_router.py`
- [ ] TASK-06 (0.5h): Registrar middleware y router en settings

### US-000-03 — CI Pipeline
- [ ] TASK-01 (1h): Crear `.github/workflows/ci.yml`
- [ ] TASK-02 (0.5h): Configurar `pyproject.toml` (black + flake8)
- [ ] TASK-03 (0.5h): Crear `pytest.ini`
- [ ] TASK-04 (0.5h): Crear `tests/test_smoke.py`
- [ ] TASK-05 (0.5h): Badge CI en `README.md`
- [ ] TASK-06 (0.5h): Agregar `docs-sync` y `docs-check` al `Makefile`
- [ ] TASK-07 (0.5h): Crear workflow `docs-governance.yml` para validar cabeceras y registro maestro de `Docs/`

### US-000-04 — Redis + Celery
- [ ] TASK-01 (1h): Crear `factory_saas/celery.py`
- [ ] TASK-02 (0.5h): Configurar Celery en `settings/base.py`
- [ ] TASK-03 (0.5h): Crear `apps/core/tasks.py` con `health_check`
- [ ] TASK-04 (0.5h): `CELERY_TASK_ALWAYS_EAGER` en `settings/test.py`
- [ ] TASK-05 (0.5h): Crear `tests/test_celery_baseline.py`

---

## Definition of Done del Sprint-0

- [ ] `docker compose up --build` arranca sin errores en máquina limpia
- [ ] `pytest` verde — 0 fallos, 0 errores
- [ ] CI pipeline verde en PR real de prueba
- [ ] Schema router probado con 2 tenants aislados
- [ ] Celery worker procesa `health_check` task
- [ ] Toda US marcada Done con DoD checklist completo
- [ ] `README.md` actualizado con instrucciones de desarrollo

---

## Notas

- Daily log: `Docs/Agile/sprints/sprint-00/daily-log.md`
- Al cierre completar: `sprint-review.md` y `sprint-retrospective.md`
- Sprint-1 NO comienza hasta que EPI-000 esté en Done completo
