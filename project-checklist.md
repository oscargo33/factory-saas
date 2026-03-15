# Project Lifecycle Checklist — Factory-SaaS

> Version: 1.3
> Last updated: 2026-03-14
> Maintainer: Project Team

Propósito: checklist de ciclo de vida que cubre desde la concepción (`core_concept`) hasta el despliegue y operación. Está organizado en fases; cada fase contiene tareas detalladas, campos de seguimiento y criterios de aceptación. El checklist por app y el `core_concept` siguen en `Docs/2-Design-Concept/0-Factory-Saas/1-checklist-factory-saas.md`.

Nota sobre versionado
- Este documento es vivo: al modificar tareas, añadir o eliminar secciones, actualizar la `Version` y añadir una entrada en el `CHANGELOG`.
- Versionado semántico interno: `MAJOR.MINOR.PATCH` donde:
	- `MAJOR`: cambios estructurales (redefinición de fases, reorganización significativa).
	- `MINOR`: nuevas tareas o etapas añadidas (funcionalidad expansiva del checklist).
	- `PATCH`: correcciones menores, typos o aclaraciones.

Cómo registrar un cambio
1. Actualiza la sección `Version` y `Last updated` arriba.
2. Añade una línea en `CHANGELOG` (más abajo) con `version`, `date`, `author` y `summary`.
3. Si corresponde, marca tareas afectadas con notas en la tabla o añade `TODO:` en la tarea.

> Estado actual: **FASE 0 CERRADA** — Avanzando a Fase 1 (Diseño Técnico Detallado).

USO: Marca las casillas cuando completes la tarea. Actualiza `Owner` y `ETA` si corresponde.

## Fase 0 — Concepción (Idea / Core Concept)
Objetivo de la fase: validar la idea y definir el mapa funcional del producto, manteniendo la independencia de apps como regla crítica.

Regla crítica de Fase 0
- [x] Las apps se tratan como unidades independientes con acoplamiento suave.
- [x] Se documenta degradación graciosa: si una app no está disponible, el sistema sigue operando.
- [x] Política de independencia publicada en `Docs/1-Core_Concept/10-politica-independencia-apps-cc.md`.

### 0.A Visión y alcance del producto
- [x] Existe visión global del producto en `Docs/1-Core_Concept/0-factory_saas-cc.md`.
- [x] Se definió propósito del sistema y núcleo arquitectónico general.
- [x] Se definieron capas y principio de resiliencia.
- [ ] Falta definir criterios formales de cierre de Fase 0 (gate de aprobación).

### 0.B Dominio funcional por app (independencia por diseño)
- [x] Existe conceptualización de `Theme` en `Docs/1-Core_Concept/1-theme-app-cc.md`.
- [x] Existe conceptualización de `Api/Telemetry` en `Docs/1-Core_Concept/2-api-app-cc.md`.
- [x] Existe conceptualización de `Profiles` en `Docs/1-Core_Concept/3-profile-app-cc.md`.
- [x] Existe conceptualización de `Product Orchestrator` en `Docs/1-Core_Concept/4-product-orchestrator-app-cc.md`.
- [x] Existe conceptualización de `Marketing` en `Docs/1-Core_Concept/5-marketing-app-cc.md`.
- [x] Existe conceptualización de `Orders` en `Docs/1-Core_Concept/6-orders-app-cc.md`.
- [x] Existe conceptualización de `Payment` en `Docs/1-Core_Concept/7-payment-app-cc.md`.
- [x] Existe conceptualización de `Support` en `Docs/1-Core_Concept/8-support-app-cc.md`.
- [x] Existe conceptualización de `Home` en `Docs/1-Core_Concept/9-home-app-cc.md`.
- [x] Límites de responsabilidad (Scope/No Scope) definidos en `Docs/1-Core_Concept/10-politica-independencia-apps-cc.md`.

### 0.C Interacciones de alto nivel (sin diseño técnico)
- [x] Dependencias suaves y relación entre apps están descritas a nivel narrativo.
- [x] Flujo global de valor (captación -> orden -> pago -> activación -> soporte) es inferible desde los docs.
- [x] Diagrama conceptual alto nivel publicado en `Docs/1-Core_Concept/11-interacciones-alto-nivel-cc.md`.

### 0.D Datos y contexto de negocio (nivel conceptual)
- [x] Se define separación conceptual `public` vs `tenant`.
- [x] Se define modelo conceptual de identidad (`User`, `Tenant`, `Membership`).
- [x] Se define concepto de snapshot transaccional en órdenes.
- [x] Glosario conceptual integrado en `0-factory_saas-cc.md` (sección Global) y en cada doc de app.

### 0.E Riesgos y resiliencia del concepto
- [x] Cada app contempla fallback o comportamiento degradado.
- [x] Se describe comportamiento fail-soft para integraciones críticas (ej. telemetry/pasarelas).
- [x] Riesgos conceptuales integrados en `0-factory_saas-cc.md` (sección Global) y en cada doc de app.

### 0.F Criterios de salida de Fase 0 (gate)
- [x] Aprobación de concepción por documento (`Owner`, `Reviewer`, `Approval Date`) en `Docs/1-Core_Concept/14-registro-aprobaciones-fase0-cc.md`.
- [x] Política de independencia de apps publicada y validada.
- [x] Diagrama conceptual de interacción entre apps publicado.
- [x] Glosario conceptual de entidades de negocio aprobado.
- [x] Riesgos conceptuales priorizados y documentados.

Resumen de avance Fase 0 (CERRADA — 2026-03-14)
- Completado: 31
- Pendiente: 0
- Avance: 100% ✅

> **FASE 0 CERRADA.** Todos los documentos de concepción (0-9) revisados, defectos corregidos y aprobados en `14-registro-aprobaciones-fase0-cc.md`.

### Scrum habilitado para seguimiento
- [x] Estructura Scrum creada en `Docs/Agile/`.
- [x] Product Backlog inicial creado (`Docs/Agile/1-product-backlog.md`).
- [x] Sprint Backlog inicial creado (`Docs/Agile/2-sprint-backlog.md`).
- [x] DoR y DoD definidos (`Docs/Agile/3-definition-of-ready-dor.md`, `Docs/Agile/4-definition-of-done-dod.md`).
- [x] Plantillas de ceremonias listas (`Docs/Agile/5-sprint-planning-template.md` a `Docs/Agile/8-sprint-retrospective-template.md`).

## Fase 1 — Diseño Conceptual (Design-Concept)

| ID | Tarea | Owner | Priority | ETA | Estado |
|---:|:------|:------|:--------:|:---:|:------|
| 1.1 | Completar `5-configuracion-poetry-fs.md` (dependencias, Python, Ruff) |  | High |  | [ ] Not started |
| 1.2 | Completar `6-dockerfile-maestro-fs.md` (multi-stage, usuario non-root) |  | High |  | [ ] Not started |
| 1.3 | Completar `7-docker-compose-specs-fs.md` (servicios, redes, healthchecks) |  | High |  | [ ] Not started |
| 1.4 | Redactar `8-entrypoint-specs-fs.md` (migraciones public y bootstrap) |  | High |  | [ ] Not started |
| 1.5 | Validar `3-gestion-de-secretos-fs.md` (strategy de secretos) |  | Medium |  | [ ] Not started |
| 1.6 | Publicar matriz de contratos inter-app (payloads, errores, responsabilidades) |  | High |  | [ ] Not started |
| 1.7 | Publicar diccionario de datos lógico (entidades, ownership por app, fronteras) |  | High |  | [ ] Not started |
| 1.8 | Publicar matriz de seguridad/compliance conceptual-técnica (PCI/PII/retención) |  | High |  | [ ] Not started |

### Subtareas ejemplo (1.1)
- [ ] Enumerar dependencias `main`, `dev`, `test`
- [ ] Añadir configuración `tool.ruff` al `pyproject.toml` propuesto
- [ ] Establecer `virtualenvs.in-project = true` en docs

## Fase 2 — Scaffolding & Infra mínima

| ID | Tarea | Owner | Priority | ETA | Estado |
|---:|:------|:------|:--------:|:---:|:------|
| 2.1 | Crear `pyproject.toml` inicial (Poetry) |  | High |  | [ ] Not started |
| 2.2 | Generar `.gitignore`, `README.md` (quickstart) y `Makefile` |  | Medium |  | [ ] Not started |
| 2.3 | Crear `Dockerfile` (multi-stage) según especificación |  | High |  | [ ] Not started |
| 2.4 | Crear `entrypoint.sh` con migraciones public + bootstrap básico |  | High |  | [ ] Not started |
| 2.5 | Crear `docker-compose.yml` con `db`, `redis`, `app`, `nginx` y healthchecks |  | High |  | [ ] Not started |
| 2.6 | Crear `.env.example` con variables esenciales |  | Medium |  | [ ] Not started |

### Subtareas ejemplo (2.3)
- [ ] Implementar etapa `builder` con caché de dependencias
- [ ] Implementar etapa `runtime` con usuario no-root y `STOPSIGNAL`
- [ ] Añadir `HEALTHCHECK` y `EXPOSE` en runtime

## Fase 3 — Implementación Inicial (apps & core)

| ID | Tarea | Owner | Priority | ETA | Estado |
|---:|:------|:------|:--------:|:---:|:------|
| 3.1 | Scaffolding Django: `src/` y `src/apps/01_theme`, `src/apps/03_profiles` |  | High |  | [ ] Not started |
| 3.2 | Implementar `patron-service-layer-fs.md` y ejemplos `services.py`/`selectors.py` |  | High |  | [ ] Not started |
| 3.3 | Implementar middleware de tenant y `db/router.py` |  | High |  | [ ] Not started |

### Subtareas (3.1)
- [ ] Crear app Django básica `01_theme` con `templates/cotton/` y token demo
- [ ] Crear endpoints de health y demo de onboarding

## Fase 4 — Integraciones y Lógica de Negocio

| ID | Tarea | Owner | Priority | ETA | Estado |
|---:|:------|:------|:--------:|:---:|:------|
| 4.1 | Implementar `05_marketing` (motor de reglas) |  | Medium |  | [ ] Not started |
| 4.2 | Implementar `06_orders` (carrito y snapshots) |  | High |  | [ ] Not started |
| 4.3 | Implementar `07_payment` (webhooks y conciliación) |  | High |  | [ ] Not started |
| 4.4 | Integrar RAG seguro en `08_support` |  | Medium |  | [ ] Not started |

## Fase 5 — Pruebas, Seguridad y Calidad

| ID | Tarea | Owner | Priority | ETA | Estado |
|---:|:------|:------|:--------:|:---:|:------|
| 5.1 | Configurar pytest, fixtures y tests de multitenancy |  | High |  | [ ] Not started |
| 5.2 | Configurar Ruff y pre-commit hooks |  | Medium |  | [ ] Not started |
| 5.3 | Ejecutar security review y escaneo de dependencias |  | High |  | [ ] Not started |

## Fase 6 — CI/CD y Despliegue

| ID | Tarea | Owner | Priority | ETA | Estado |
|---:|:------|:------|:--------:|:---:|:------|
| 6.1 | Pipeline CI: lint, tests, build image |  | High |  | [ ] Not started |
| 6.2 | CD: despliegue a staging (compose o k8s) |  | High |  | [ ] Not started |
| 6.3 | Definir backup/migration strategy y runbook |  | High |  | [ ] Not started |

## Fase 7 — Operaciones y Observabilidad

| ID | Tarea | Owner | Priority | ETA | Estado |
|---:|:------|:------|:--------:|:---:|:------|
| 7.1 | Configurar monitoring, logging y dashboards (La Central) |  | Medium |  | [ ] Not started |
| 7.2 | Crear runbooks para incidentes críticos |  | High |  | [ ] Not started |

## Fase 8 — Gobernanza y Mantenimiento

| ID | Tarea | Owner | Priority | ETA | Estado |
|---:|:------|:------|:--------:|:---:|:------|
| 8.1 | Crear `CONTRIBUTING.md`, `CHANGELOG.md` y asignar ownership |  | Medium |  | [ ] Not started |
| 8.2 | Definir roadmap y backlog priorizado |  | Medium |  | [ ] Not started |

## Artefactos transversales
- `Docs/00-knowledge-base/` — guía de decisiones arquitectónicas (siempre vigente)
- `Docs/1-Core_Concept/0-factory_saas-cc.md` — Core Concept maestro
- `Docs/2-Design-Concept/0-Factory-Saas/1-checklist-factory-saas.md` — checklist de seguimiento del core_concept

---

Acción inmediata recomendada
- Cerrar formalmente Fase 0 completando aprobaciones en `Docs/1-Core_Concept/14-registro-aprobaciones-fase0-cc.md`.
- Iniciar Fase 1 con `8-entrypoint-specs-fs.md` y continuar capas 2-7 de `Docs/2-Design-Concept/0-Factory-Saas/`.

## CHANGELOG
| Version | Date | Author | Summary |
|---|---|---|---|
| 1.3 | 2026-03-14 | Copilot + User | **FASE 0 CERRADA.** Docs 8/9 corregidos (jerarquía headings). Docs 10-13 integrados en 0 y en cada app. Doc 14 aprobado con 10 docs ✅. Estado actualizado a Fase 1. |
| 1.2 | 2026-03-14 | Copilot + User | Fase 0 alineada para cierre, artefactos de concepción creados (10-14), Scrum integrado con docs en `Docs/Agile/`. |
| 1.1 | 2026-03-14 | Copilot + User | Fase 0 separada de tareas de diseño y reforzada la independencia por app. |
| 1.0 | 2026-03-14 | Copilot + User | Estructura inicial del checklist de ciclo de vida. |

