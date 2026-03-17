# US-000-04 — Redis + Celery Worker Baseline

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** US-000-04
**Epic:** [EPI-000 — Core Infra](epic.md)
**Prioridad:** 4
**SP:** 2 | **Sprint:** Sprint-0 | **Estado:** Planned
**Design Anchor:** `Docs/2-Design-Concept/0-Factory-Saas/11-configuracion-redis-celery-fs.md`

---

## Historia

**Como** sistema de backend
**Quiero** un worker Celery conectado a Redis que procese tareas asíncronas
**Para** desacoplar operaciones pesadas (emails, webhooks, jobs) del ciclo request-response

---

## Criterios de Aceptación

- [ ] `celery -A factory_saas worker --loglevel=info` arranca sin errores dentro del contenedor `worker`
- [ ] Una tarea `apps.core.tasks.health_check` se registra y ejecuta exitosamente
- [ ] El resultado de la tarea se puede inspeccionar con `AsyncResult(task_id).get(timeout=5)`
- [ ] Redis como broker y como result-backend configurados en settings
- [ ] Celery beat configurado para tareas periódicas (mínimo: `health_check` cada 5 minutos)

---

## Tasks

- [ ] **TASK-01** (1h) `@backend` — Crear `factory_saas/celery.py` con `app = Celery("factory_saas")`, `app.config_from_object("django.conf:settings", namespace="CELERY")`, `app.autodiscover_tasks()`
- [ ] **TASK-02** (0.5h) `@backend` — Agregar en `factory_saas/settings/base.py`: `CELERY_BROKER_URL = env("REDIS_URL")`, `CELERY_RESULT_BACKEND = env("REDIS_URL")`, `CELERY_BEAT_SCHEDULE = {"health-check": {"task": "apps.core.tasks.health_check", "schedule": 300}}`
- [ ] **TASK-03** (0.5h) `@backend` — Crear `apps/core/tasks.py` con `@shared_task def health_check(): return "ok"`
- [ ] **TASK-04** (0.5h) `@backend` — Agregar `CELERY_TASK_ALWAYS_EAGER = True` solo en `settings/test.py` para que tests no requieran broker real
- [ ] **TASK-05** (0.5h) `@backend` — Crear `tests/test_celery_baseline.py` con test: llama `health_check.delay()` y verifica `result.get() == "ok"` (usando ALWAYS_EAGER)

---

## DoD Checklist

- [ ] `pytest tests/test_celery_baseline.py` pasa
- [ ] Worker arranca en contenedor docker y log muestra `[tasks] . apps.core.tasks.health_check`
- [ ] PR revisado y aprobado
- [ ] CI pasa
