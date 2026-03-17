# Sprint-0 — Backlog

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-17

**Período:** 2026-03-16 — 2026-03-29 (2 semanas)
**Objetivo:** Materializar el esqueleto Django de la Factory junto con la base de infraestructura reproducible, CI operativo y router multi-tenant listo. Al finalizar este sprint, cualquier desarrollador puede clonar el repo, ejecutar Docker y contar con base Core + Infra trazable.
**Epics asociados:** [EPI-CORE — Factory SaaS](../../backlog/EPI-CORE-factory/EPI-CORE-factory-saas.md), [EPI-000 — Core Infra](../../backlog/EPI-000-infra/epic.md)
**Capacidad:** ~28 SP (sprint fundacional ampliado: Core + Infra)

---

## Compromisos del Sprint

| Prioridad | US ID | Historia | SP | Owner | Estado |
|---|---|---|---|---|---|
| 1 | [US-CORE-01](../../backlog/EPI-CORE-factory/US-CORE-01-project-skeleton.md) | Estructura base del proyecto Django | 2 | — | Planned |
| 2 | [US-CORE-02](../../backlog/EPI-CORE-factory/US-CORE-02-core-models-public.md) | Modelos Core `Tenant` y `Membership` en `public` | 3 | — | Planned |
| 3 | [US-CORE-03](../../backlog/EPI-CORE-factory/US-CORE-03-core-exceptions.md) | Jerarquía base de excepciones de dominio | 1 | — | Planned |
| 4 | [US-CORE-04](../../backlog/EPI-CORE-factory/US-CORE-04-tenant-middleware-router.md) | `TenantMiddleware` + `TenantSchemaRouter` | 3 | — | Planned |
| 5 | [US-CORE-05](../../backlog/EPI-CORE-factory/US-CORE-05-core-selectors.md) | Selectors base de tenant y membresías | 2 | — | Planned |
| 6 | [US-CORE-06](../../backlog/EPI-CORE-factory/US-CORE-06-theme-defaults-fallback-layout.md) | `theme_defaults` + fallback layout global | 1 | — | Planned |
| 7 | [US-CORE-07](../../backlog/EPI-CORE-factory/US-CORE-07-core-services-isolation-tests.md) | Services core y tests de aislamiento | 3 | — | Planned |
| 8 | [US-000-01](../../backlog/EPI-000-infra/US-000-01-docker-dev-environment.md) | Docker dev environment reproducible | 3 | — | Planned |
| 9 | [US-000-02](../../backlog/EPI-000-infra/US-000-02-postgresql-schema-router.md) | PostgreSQL multi-tenant + schema router | 5 | — | Planned |
| 10 | [US-000-03](../../backlog/EPI-000-infra/US-000-03-ci-pipeline.md) | CI pipeline (pytest + flake8 + black) | 3 | — | Planned |
| 11 | [US-000-04](../../backlog/EPI-000-infra/US-000-04-redis-celery-baseline.md) | Redis + Celery worker baseline | 2 | — | Planned |

**Total comprometido:** 28 SP

---

## Tasks activadas (extraídas de cada US)

### US-CORE-01 — Estructura base Django
- [ ] TASK-01 (0.5h): Crear estructura `factory_saas/settings/`
- [ ] TASK-02 (0.5h): Crear `urls.py`, `wsgi.py`, `asgi.py`, `theme_defaults.py`
- [ ] TASK-03 (0.5h): Crear contenedor `apps/` y `apps/core/`
- [ ] TASK-04 (0.5h): Crear `templates/fallback_layout.html`
- [ ] TASK-05 (0.5h): Reflejar la estructura en backlog y sprint backlog

### US-CORE-02 — Modelos core en public
- [ ] TASK-01 (1h): Crear `apps/core/models.py` con `Tenant` y `Membership`
- [ ] TASK-02 (0.5h): Definir constraints base
- [ ] TASK-03 (0.5h): Generar migración inicial
- [ ] TASK-04 (0.5h): Verificar ejecución sobre `public`
- [ ] TASK-05 (0.5h): Dejar evidencia en backlog/sprint backlog

### US-CORE-03 — Excepciones base
- [ ] TASK-01 (0.5h): Crear `apps/core/exceptions.py`
- [ ] TASK-02 (0.25h): Alinear nombres con DC-12-FS
- [ ] TASK-03 (0.25h): Reflejar trazabilidad documental

### US-CORE-04 — Middleware y router
- [ ] TASK-01 (1h): Crear `apps/core/middleware.py`
- [ ] TASK-02 (1h): Crear `apps/core/db_router.py`
- [ ] TASK-03 (0.5h): Definir manejo controlado de tenant inexistente
- [ ] TASK-04 (0.5h): Registrar integración prevista en settings

### US-CORE-05 — Selectors base
- [ ] TASK-01 (0.75h): Crear `get_tenant_by_slug`
- [ ] TASK-02 (0.5h): Crear `get_active_memberships`
- [ ] TASK-03 (0.25h): Alinear contratos públicos
- [ ] TASK-04 (0.5h): Conectar estas firmas en backlog y epic

### US-CORE-06 — Theme defaults y fallback
- [ ] TASK-01 (0.5h): Crear `DEFAULT_THEME_TOKENS`
- [ ] TASK-02 (0.5h): Crear `fallback_layout.html` usable por apps UI

### US-CORE-07 — Services core y tests
- [ ] TASK-01 (1h): Crear `create_tenant`
- [ ] TASK-02 (0.5h): Crear `deactivate_tenant`
- [ ] TASK-03 (1h): Crear tests base de aislamiento
- [ ] TASK-04 (0.5h): Referenciar evidencia en backlog y sprint backlog

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
- [ ] Esqueleto EPI-CORE disponible y trazable por archivos US
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
