
# Documento: Checklist de Control de Implementación (Factory-SaaS)

**ID:** CK-01-FS

**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/1-checklist-factory-saas.md`

**Referencia:** Jerarquía de Capas 0-7

**Estado:** **RESTURADO Y ACTUALIZADO**

---

## ✅ CAPA 0: Gestión y Dependencias (Proyecto Raíz)

*Documento de Diseño: `2-Core Automation-specs-fs.md` y `5-configuracion-poetry-fs.md*`

* [x] **Estructura Física de Directorios** (Diseño: `4-estructura-de-carpetas-fs.md`).
* [x] **Estándar de Automatización Híbrido** (Diseño: `2-Core Automation-specs-fs.md`).
* [ ] **Configuración de Entorno Python** (Diseño: `5-configuracion-poetry-fs.md`).
* [x] Definición de Python 3.12+.
* [x] Política de `virtualenvs.in-project = true`.
* [x] Selección de `Ruff` como estándar de calidad.
* [x] Definición de grupos `main`, `dev`, `test`.


* [ ] `pyproject.toml` físico (Pendiente).
* [ ] `poetry.lock` (Pendiente).
* [ ] `.gitignore` (Pendiente).
* [ ] `README.md` (Pendiente).
* [ ] `Makefile` físico (Pendiente).

## ✅ CAPA 1: Entorno de Ejecución (Contenedores)

*Documento de Diseño: `6-dockerfile-maestro-fs.md` (Siguiente)*

* [x] **Gestión de Secretos** (Diseño: `3-gestion-de-secretos-fs.md`).
* [ ] `Dockerfile` (Imagen base multi-etapa).
* [ ] `docker-compose.yml` (Orquestación de servicios y red `backnet_fs`).
* [ ] `.env.example` físico (Plantilla con prefijos definidos).
* [ ] `entrypoint.sh` (Script de inicialización).

## ✅ CAPA 2: Persistencia (Base de Datos)

*Documento de Diseño: `7-configuracion-postgresql-fs.md*`

* [ ] `init-db.sql` (Script de extensiones `uuid-ossp` y `pgvector`).
* [ ] `conf/postgresql.conf` (Tuning de rendimiento del motor).
* [ ] Definición de volúmenes persistentes (`db_data_fs`, `media_data_fs`).

## ✅ CAPA 3: Orquestación (Red y Comunicaciones)

*Documento de Diseño: `8-gateway-nginx-fs.md*`

* [ ] `nginx/default.conf` (Proxy y subdominios dinámicos).
* [ ] `config/redis.conf` (Caché y Broker).
* [ ] `celery.py` (Worker para tareas asíncronas).

## ✅ CAPA 4: Arquitectura de Software (Servicios)

*Documento de Diseño: `9-patron-service-layer-fs.md*`

* [ ] `base/services.py` (Lógica de negocio).
* [ ] `base/selectors.py` (Consultas de datos).
* [ ] `base/exceptions.py` (Errores transversales).

## ✅ CAPA 5: Motor de Multitenencia

*Documento de Diseño: `10-router-dinamico-esquemas-fs.md*`

* [ ] `middleware/tenant_middleware.py` (Detección de inquilino).
* [ ] `db/router.py` (Ruteador de esquemas).
* [ ] `db/utils.py` (Helpers de `search_path`).

## ✅ CAPA 6: Base Visual y Frontend

*Documento de Diseño: `11-pipeline-tailwind-cotton-fs.md*`

* [ ] `tailwind.config.js` (Tokens de diseño).
* [ ] `static/js/alpine_init.js` (Reactividad).
* [ ] `templates/base_cotton.html` (Layout maestro).

## ✅ CAPA 7: Lógica de Fábrica (Operatividad)

*Documento de Diseño: `12-protocolo-de-comunicacion-con-la-central-fs.md*`

* [ ] `src/apps/04_product_orchestrator/` (Lógica de asignación).
* [ ] `src/apps/05_product_core/` (Lógica funcional del SaaS).
* [ ] `telemetry/client.py` (Conexión con La Central).
* [ ] `fs_provision_tenant.py` (Comando de creación de inquilinos).

