# US-000-01 — Docker Dev Environment Reproducible

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** US-000-01
**Epic:** [EPI-000 — Core Infra](epic.md)
**Prioridad:** 1
**SP:** 3 | **Sprint:** Sprint-0 | **Estado:** Planned
**Design Anchor:** `Docs/2-Design-Concept/0-Factory-Saas/6-dockerfile-maestro-fs.md`, `7-docker-compose-specs-fs.md`

---

## Historia

**Como** desarrollador nuevo en el proyecto
**Quiero** un entorno Docker que arranque con `docker compose up --build`
**Para** poder contribuir sin instalar dependencias locales ni conflictos de versiones

---

## Criterios de Aceptación

- [ ] `docker compose up --build` arranca los servicios `web`, `db`, `redis`, `worker` sin errores en < 90s
- [ ] `http://localhost:8000` responde HTTP 200
- [ ] `python manage.py check` pasa limpio dentro del contenedor `web`
- [ ] Variables sensibles se leen de `.env.dev` (no hardcodeadas en compose)
- [ ] El volumen `postgres_data` persiste datos entre reinicios

---

## Tasks

- [ ] **TASK-01** (2h) `@infra` — Crear `Dockerfile.dev` con imagen `python:3.12-slim`, instalar Poetry, copiar `pyproject.toml` y ejecutar `poetry install --no-root`
- [ ] **TASK-02** (2h) `@infra` — Crear `docker-compose.dev.yml` con services: `db` (postgres:16), `redis` (redis:7-alpine), `web` (build: Dockerfile.dev, command: gunicorn), `worker` (command: celery -A factory_saas worker)
- [ ] **TASK-03** (1h) `@infra` — Crear `scripts/entrypoint.sh` con: wait-for-db loop, `python manage.py migrate --noinput`, `exec "$@"`
- [ ] **TASK-04** (1h) `@backend` — Crear `factory_saas/settings/dev.py` leyendo `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY` de `os.environ`
- [ ] **TASK-05** (0.5h) `@infra` — Crear `.env.dev.example` con todas las variables requeridas documentadas
- [ ] **TASK-06** (0.5h) `@docs` — Agregar sección "Desarrollo local" en `README.md` raíz con el comando `docker compose -f docker-compose.dev.yml up --build`

---

## DoD Checklist

- [ ] Smoke test: `docker compose up --build && curl -f http://localhost:8000`
- [ ] `.env.dev.example` commiteado, `.env.dev` en `.gitignore`
- [ ] PR revisado y aprobado por 1 peer
- [ ] CI pasa (lint + tests)
