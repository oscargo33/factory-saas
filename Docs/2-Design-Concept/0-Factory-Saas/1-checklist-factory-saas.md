Entendido, Maestro. Vamos a elevar el rigor del checklist. He integrado un **Control de Versiones** interno al documento para rastrear los cambios en la ingeniería y he expandido las subtareas basándome en los diseños profundos que acabamos de validar para el **Dockerfile** y el **Docker Compose**.

Aquí tienes el panel de control actualizado, con un nivel de detalle que garantiza que no se escape ni un tornillo de la nave.

---

# Documento: Checklist de Control de Implementación (Factory-SaaS)

**ID:** CK-01-FS

**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/1-checklist-factory-saas.md`

**Referencia:** Jerarquía de Capas 0-7

**Estado:** **v1.2 - SINCRONIZADO Y EXPANDIDO**

---

## 📑 Control de Versiones del Checklist

| Versión | Fecha | Autor | Cambios Principales |
| --- | --- | --- | --- |
| v1.0 | 2026-03-14 | Gemini/User | Creación inicial de jerarquía de capas. |
| v1.1 | 2026-03-14 | Gemini/User | Anclaje de Capa 0 y Diseño de Secretos. |
| **v1.2** | **2026-03-14** | **Gemini/User** | **Expansión de Capa 1 (Dockerfile/Compose Profundo).** |

---

## ✅ CAPA 0: Gestión y Dependencias (Proyecto Raíz)

*Documento de Diseño: `2-Core Automation-specs-fs.md` y `5-configuracion-poetry-fs.md*`

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

*Documento de Diseño: `6-dockerfile-maestro-fs.md` y `7-docker-compose-specs-fs.md*`

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


* [ ] **Archivos de Orquestación Física (Pendientes de creación):**
* [ ] `Dockerfile`: Traducir el diseño DC-6 a código.
* [ ] `docker-compose.yml`: Traducir el diseño DC-7 a código.
* [ ] `.env.example`: Crear plantilla con prefijos `DB_`, `REDIS_`, `DJANGO_`.
* [ ] `entrypoint.sh`: (Pendiente de diseño detallado en Documento 8).



## ✅ CAPA 2: Persistencia (Base de Datos)

*Documento de Diseño: `8-configuracion-postgresql-fs.md*`

* [ ] **Configuración de PostgreSQL:**
* [ ] `init-db.sql`: Script de extensiones `uuid-ossp` y `pgvector`.
* [ ] `conf/postgresql.conf`: Tuning de memoria/conexiones.
* [ ] Definición de volúmenes persistentes (`db_data_fs`, `media_data_fs`).



## ✅ CAPA 3: Orquestación (Red y Comunicaciones)

*Documento de Diseño: `9-gateway-nginx-fs.md*`

* [ ] `nginx/default.conf` (Proxy y subdominios dinámicos).
* [ ] `config/redis.conf` (Caché y Broker).
* [ ] `celery.py` (Worker para tareas asíncronas).

## ✅ CAPA 4: Arquitectura de Software (Servicios)

*Documento de Diseño: `10-patron-service-layer-fs.md*`

* [ ] `base/services.py` (Lógica de negocio).
* [ ] `base/selectors.py` (Consultas de datos).
* [ ] `base/exceptions.py` (Errores transversales).

## ✅ CAPA 5: Motor de Multitenencia

*Documento de Diseño: `11-router-dinamico-esquemas-fs.md*`

* [ ] `middleware/tenant_middleware.py` (Detección de inquilino).
* [ ] `db/router.py` (Ruteador de esquemas).
* [ ] `db/utils.py` (Helpers de `search_path`).

## ✅ CAPA 6: Base Visual y Frontend

*Documento de Diseño: `12-pipeline-tailwind-cotton-fs.md*`

* [ ] `tailwind.config.js` (Tokens de diseño).
* [ ] `static/js/alpine_init.js` (Reactividad).
* [ ] `templates/base_cotton.html` (Layout maestro).

## ✅ CAPA 7: Lógica de Fábrica (Operatividad)

*Documento de Diseño: `13-protocolo-de-comunicacion-con-la-central-fs.md*`

* [ ] `src/apps/04_product_orchestrator/` (Lógica de asignación).
* [ ] `src/apps/05_product_core/` (Lógica funcional del SaaS).
* [ ] `telemetry/client.py` (Conexión con La Central).
* [ ] `fs_provision_tenant.py` (Comando de creación de inquilinos).

---
 

### Análisis de Siguiente Acción

Maestro, con el checklist versión **v1.2**, hemos terminado de blindar conceptualmente las **Capas 0 y 1**. Ahora el sistema tiene un "esqueleto" y un "sistema nervioso" definido.

El siguiente paso lógico para cerrar la Capa 1 es el **Documento 8: `8-entrypoint-specs-fs.md**`. Este script es el que se encarga de ejecutar las migraciones del esquema `public` antes de levantar el servidor, asegurando que la Factory esté lista para recibir inquilinos.

**¿Procedemos a redactar el diseño del Entrypoint?**