# Documento: Checklist de Control de Implementación (Factory-SaaS)

**ID:** CK-01-FS

**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/1-checklist-factory-saas.md`

**Referencia:** Jerarquía de Capas 0-7

**Estado:** **v2.0 — FASE 1 DISEÑO GLOBAL CERRADA**

---

## 📑 Control de Versiones del Checklist

| Versión | Fecha | Autor | Cambios Principales |
| --- | --- | --- | --- |
| v1.0 | 2026-03-14 | Gemini/User | Creación inicial de jerarquía de capas. |
| v1.1 | 2026-03-14 | Gemini/User | Anclaje de Capa 0 y Diseño de Secretos. |
| v1.2 | 2026-03-14 | Gemini/User | Expansión de Capa 1 (Dockerfile/Compose Profundo). |
| **v2.0** | **2026-03-14** | **Arq. IA (GitHub Copilot)** | **Documentos DC-8 a DC-18 creados. Fase 1 Global Design cerrada.** |

---

## ✅ CAPA 0: Gestión y Dependencias (Proyecto Raíz)

*Documentos de Diseño: `2-Core Automation-specs-fs.md`, `3-gestion-de-secretos-fs.md`, `4-estructura-de-carpetas-fs.md`, `5-configuracion-poetry-fs.md`*

* [x] **Estructura Física de Directorios** (Diseño: `4-estructura-de-carpetas-fs.md`).
* [x] **Estándar de Automatización Híbrido** (Diseño: `2-Core Automation-specs-fs.md`).
* [x] **Configuración de Entorno Python** (Diseño: `5-configuracion-poetry-fs.md`).
* [x] Definición de Python 3.12+.
* [x] Política de `virtualenvs.in-project = true`.
* [x] Selección de `Ruff` como estándar de calidad.
* [x] Definición de grupos `main`, `dev`, `test`.


* [ ] **Archivos de Configuración Física (Pendientes de creación):**
* [ ] `pyproject.toml`: Implementar grupos y configuración de Ruff.
* [ ] `poetry.lock`: Generación post-instalación.
* [ ] `.gitignore`: Incluir `.venv`, `.env`, `__pycache__`, `db_data`.
* [ ] `README.md`: Guía de arquitectura de capas para devs.
* [ ] `Makefile`: Implementar reglas `build`, `up`, `down`, `shell`, `install`.



## ✅ CAPA 1: Entorno de Ejecución (Contenedores)

*Documentos de Diseño: `6-dockerfile-maestro-fs.md`, `7-docker-compose-specs-fs.md`, `8-entrypoint-specs-fs.md` (DC-8-FS)*

* [x] **Gestión de Secretos** (Diseño: `3-gestion-de-secretos-fs.md`).
* [x] **Diseño de Dockerfile Maestro** (Diseño: `6-dockerfile-maestro-fs.md`).
* [x] Definición de Multi-stage build (Builder vs Runtime).
* [x] Configuración de usuario `factory_user` (No-root).
* [x] Optimización de capas de caché para Python.
* [x] Definición de `STOPSIGNAL` y `EXPOSE`.


* [x] **Diseño de Docker Compose** (Diseño: `7-docker-compose-specs-fs.md`).
* [x] Segmentación de redes: `backnet_fs` (Interna) y `frontnet_fs` (Gateway).
* [x] Implementación de `Healthchecks` (`pg_isready` para DB).
* [x] Definición de volúmenes nombrados para persistencia.

* [x] **Diseño de Entrypoint** (Diseño: `8-entrypoint-specs-fs.md` — DC-8-FS). ✅
* [x] Máquina de estado: DB gate → migrate public → collectstatic → gunicorn.
* [x] Polling `pg_isready` (30 intentos, 2s intervalo).
* [x] `exec gunicorn` como PID 1 con configuración de workers/timeout.
* [x] Variante de desarrollo con `runserver`.

* [ ] **Archivos de Orquestación Física (Pendientes de creación):**
* [ ] `Dockerfile`: Traducir el diseño DC-6 a código.
* [ ] `docker-compose.yml`: Traducir el diseño DC-7 a código.
* [ ] `.env.example`: Crear plantilla con prefijos `DB_`, `REDIS_`, `DJANGO_`.
* [ ] `entrypoint.sh`: Implementar según DC-8-FS.



## ✅ CAPA 2: Persistencia (Base de Datos) — DC-9-FS

*Documento de Diseño: `9-configuracion-postgresql-fs.md` (DC-9-FS)*

* [x] **Diseño de PostgreSQL** (Diseño: `9-configuracion-postgresql-fs.md`). ✅
* [x] Estrategia schema-per-tenant (`public` + `tenant_{slug}`).
* [x] Extensiones requeridas: `uuid-ossp`, `pgvector`.
* [x] Parámetros de tuning: `shared_buffers`, `max_connections`, `log_min_duration_statement`.
* [x] Estrategia de volúmenes: `db_data_fs`, `db_init_fs`.
* [x] Seguridad: `factory_user` sin SUPERUSER.

* [ ] **Archivos Físicos (Pendientes de creación):**
* [ ] `init-db.sql`: Script de extensiones `uuid-ossp` y `pgvector`.
* [ ] `conf/postgresql.conf`: Tuning de memoria/conexiones.



## ✅ CAPA 3: Orquestación (Red y Mensajería) — DC-10-FS, DC-11-FS

*Documentos de Diseño: `10-gateway-nginx-fs.md` (DC-10-FS), `11-configuracion-redis-celery-fs.md` (DC-11-FS)*

* [x] **Diseño de Nginx** (Diseño: `10-gateway-nginx-fs.md`). ✅
* [x] Wildcard subdomains, proxy a Gunicorn, servicio de estáticos.
* [x] Headers de seguridad: `X-Frame-Options`, `X-Content-Type-Options`, HSTS, `server_tokens off`.
* [x] SSL TLSv1.2 mínimo.

* [x] **Diseño de Redis + Celery** (Diseño: `11-configuracion-redis-celery-fs.md`). ✅
* [x] Bases de datos Redis 0-4 asignadas por función.
* [x] 5 colas Celery: `default`, `telemetry`, `emails`, `payments`, `slow`.
* [x] Backoff exponencial con jitter para reintentos.
* [x] `task_acks_late = True` para at-least-once delivery.

* [ ] **Archivos Físicos (Pendientes):**
* [ ] `nginx/nginx.conf` y `nginx/conf.d/factory.conf`.
* [ ] `celery_app.py` y configuración de colas.



## ✅ CAPA 4: Arquitectura de Software (Service Layer) — DC-12-FS

*Documento de Diseño: `12-patron-service-layer-fs.md` (DC-12-FS)*

* [x] **Diseño del patrón Service/Selector** (Diseño: `12-patron-service-layer-fs.md`). ✅
* [x] Estructura `services.py` / `selectors.py` / `exceptions.py` por app.
* [x] Jerarquía de excepciones: `FactoryBaseException` → `ServiceError`, `NotFoundError`, `PermissionDenied`.
* [x] Regla: ninguna app importa modelos de otra app.
* [x] Vistas como orquestadores puros (≤ 30 líneas).

* [ ] **Archivos Físicos (Pendientes):**
* [ ] `core/exceptions.py`: Jerarquía base de excepciones.
* [ ] Template `services.py` y `selectors.py` vacíos por app.



## ✅ CAPA 5: Motor de Multi-Tenancy — DC-13-FS

*Documento de Diseño: `13-router-dinamico-esquemas-fs.md` (DC-13-FS)*

* [x] **Diseño del TenantMiddleware y SchemaRouter** (Diseño: `13-router-dinamico-esquemas-fs.md`). ✅
* [x] Extracción de slug desde header `Host`.
* [x] Caché de tenant en Redis DB 0 (TTL 300s, invalidación por signal).
* [x] Respuestas 404/403 JSON para tenants no encontrados o suspendidos.
* [x] Comando `bootstrap_tenant`: CREATE SCHEMA → migrate → seed.
* [x] Context manager `with tenant_context(tenant)` para tareas Celery.

* [ ] **Archivos Físicos (Pendientes):**
* [ ] `middleware/tenant_middleware.py`.
* [ ] `db/router.py` con inyección de `search_path`.
* [ ] `management/commands/bootstrap_tenant.py`.



## ✅ CAPA 6: Base Visual y Frontend — DC-14-FS

*Documento de Diseño: `14-pipeline-tailwind-cotton-fs.md` (DC-14-FS)*

* [x] **Diseño del pipeline Tailwind + Cotton + Alpine.js** (Diseño: `14-pipeline-tailwind-cotton-fs.md`). ✅
* [x] Tailwind JIT con rutas `content` para templates y Cotton.
* [x] CSS Variables como design tokens (7 tokens base).
* [x] `COTTON_DIR = 'templates/cotton'` con estructura de componentes.
* [x] Alpine.js stores globales: `auth`, `tenant`, `ui`.
* [x] Fallback: si Theme App no instalado → CSS variables default.

* [ ] **Archivos Físicos (Pendientes):**
* [ ] `tailwind.config.js` con tokens de diseño.
* [ ] `templates/cotton/` con componentes base.
* [ ] `templates/base.html` con inyección de CSS variables.



## ✅ CAPA 7: Telemetría y Control de La Central — DC-15-FS

*Documento de Diseño: `15-protocolo-comunicacion-central-fs.md` (DC-15-FS)*

* [x] **Diseño del protocolo de telemetría** (Diseño: `15-protocolo-comunicacion-central-fs.md`). ✅
* [x] Modo Push: batch Celery cada 5 min → HTTPS POST con JWT (TTL 60s).
* [x] Buffer `PendingMetrics` para resiliencia offline.
* [x] Modo Pull: endpoint `/api/telemetry/inspect/` con token API.
* [x] Header `X-Trace-ID` para correlación.
* [x] No-PII en payload de `TelemetryEvent`.

* [ ] **Archivos Físicos (Pendientes):**
* [ ] `telemetry/models.py` (`TelemetryEvent`, `PendingMetrics`).
* [ ] `telemetry/tasks.py` (`push_metrics`).
* [ ] `telemetry/views.py` (endpoint pull).



## ✅ TRANSVERSAL: Contratos, Datos y Seguridad — DC-16, DC-17, DC-18

*Documentos: `16-contratos-inter-app-fs.md`, `17-diccionario-datos-logico-fs.md`, `18-matriz-seguridad-compliance-fs.md`*

* [x] **Contratos inter-app** (DC-16-FS): interfaces públicas de las 8 apps documentadas. ✅
* [x] **Diccionario de datos** (DC-17-FS): 10 entidades con campos, schemas y owners. ✅
* [x] **Matriz de seguridad** (DC-18-FS): OWASP Top 10, PII, PCI DSS, retención de datos. ✅

---

## 🎯 Resumen de Estado — Fase 1 Diseño Global

| Capa | Documentos de Diseño | Estado |
|---|---|---|
| Capa 0 - Gestión | DC-2, DC-3, DC-4, DC-5 | ✅ Diseño completo |
| Capa 1 - Contenedores | DC-6, DC-7, DC-8 | ✅ Diseño completo |
| Capa 2 - PostgreSQL | DC-9 | ✅ Diseño completo |
| Capa 3 - Nginx + Redis | DC-10, DC-11 | ✅ Diseño completo |
| Capa 4 - Service Layer | DC-12 | ✅ Diseño completo |
| Capa 5 - Multi-Tenancy | DC-13 | ✅ Diseño completo |
| Capa 6 - Frontend | DC-14 | ✅ Diseño completo |
| Capa 7 - Telemetría | DC-15 | ✅ Diseño completo |
| Transversal | DC-16, DC-17, DC-18 | ✅ Diseño completo |

**FASE 1 DISEÑO GLOBAL: ✅ CERRADA — Listo para diseño individual de apps**

---

## Siguiente Acción

Con el diseño global de Fase 1 completado, el siguiente paso es el diseño individual de cada app. Se recomienda empezar por **App 1 (Theme)** al ser la base del sistema visual de todas las demás.

Cada app requiere su propia carpeta en `Docs/2-Design-Concept/{N}-{App-Name}/` con al menos:
- Un documento de diseño de modelos.
- Un documento de diseño de vistas/endpoints.
- Un documento de contratos expuestos (referenciando DC-16).

**Estado:** docs 10-18 creados y este checklist actualizado a v2.0. Ejecutar `git commit` para cerrar Fase 1.