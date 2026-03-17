Tienes razón, Maestro. El `docker-compose.yml` es el **Manifiesto de Vuelo**. Si lo dejamos superficial, la comunicación entre las capas se vuelve inestable. Vamos a profundizar en la ingeniería de este archivo para que soporte la escala de la Factory.

Aquí tienes la versión extendida y rigurosa del diseño de orquestación.

---

# Documento: 7-docker-compose-specs-fs.md (Versión Detallada)

**ID:** DC-7-FS

**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/7-docker-compose-specs-fs.md`

**Referencia Core:** `0-factory_saas-cc.md`

**Apellido:** **-fs**

## 1. Arquitectura de Servicios y Dependencias

El diseño se basa en un modelo de **Salud de Servicio (Healthcheck)**. No basta con que un contenedor esté "encendido"; debe estar "listo".

### A. Servicio: `db` (PostgreSQL 16)

* **Imagen:** `postgres:16-alpine` (por ligereza y seguridad).
* **Healthcheck:** Se ejecutará `pg_isready` cada 10 segundos. La App no arrancará hasta que este servicio pase la prueba.
* **Tuning:** Montaje de un archivo de configuración personalizado (`/etc/postgresql/postgresql.conf`) para optimizar el uso de RAM según la capacidad de la Factory.

### B. Servicio: `app` (Django / Gunicorn)

* **Build Context:** Carpeta raíz, usando el `Dockerfile` (DC-6).
* **Volúmenes de Desarrollo:**
* `./src:/app`: Para reflejar cambios de código instantáneamente.
* `poetry_cache:/home/factory_user/.cache`: Para no reinstalar librerías si se borra el contenedor.


* **Dependencias:** `depends_on` con condición `service_healthy` para la DB.

### C. Servicio: `redis` (Cache & Broker)

* **Imagen:** `redis:7-alpine`.
* **Comando:** `redis-server --save 60 1 --loglevel warning`.
* **Propósito:** Gestión de sesiones, caché de la App 01 (Theme) y broker para la App 02 (Telemetry).

## 2. Definición de Redes (Networking)

Diseñamos una red con **aislamiento de tráfico**:

* **`backnet_fs` (Internal):** Red de alta velocidad para la comunicación `App <-> DB <-> Redis`. No tiene acceso a internet por defecto (protección contra exfiltración de datos).
* **`frontnet_fs` (Gateway):** Red que conecta la App con el futuro Nginx (Capa 3). Es la única que recibe peticiones externas.

## 3. Persistencia y Gestión de Volúmenes

Definimos volúmenes nombrados para asegurar que los datos sobrevivan a la destrucción de los contenedores:

| Volumen | Ubicación Interna | Uso |
| --- | --- | --- |
| `db_data_fs` | `/var/lib/postgresql/data` | Datos de todos los esquemas (tenants). |
| `redis_data_fs` | `/data` | Persistencia de colas de tareas. |
| `media_fs` | `/app/media` | Archivos de usuario (Tenant-specific). |
| `static_fs` | `/app/staticfiles` | CSS/JS procesado por Tailwind/Cotton. |

## 4. Estrategia de Variables de Entorno

El orquestador mapeará las variables del archivo `.env` (DC-3) pero permitirá **Overrides** específicos:

* `POSTGRES_DB`: Siempre será `factory_db`.
* `POSTGRES_USER`: Inyectado desde secretos.
* `DATABASE_URL`: Construida dinámicamente: `postgres://${DB_USER}:${DB_PASSWORD}@db:5432/factory_db`.

---

# Checklist de Control de Implementación (Factory-SaaS)

**ID:** CK-01-FS

**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/1-checklist-factory-saas.md`

**Estado:** **ACTUALIZADO**

## ✅ CAPA 0: Gestión y Dependencias (Proyecto Raíz)

*Documentos: DC-2, DC-4, DC-5*

* [x] **Estructura Física de Directorios** (DC-4).
* [x] **Estándar de Automatización Híbrido** (DC-2).
* [x] **Configuración de Entorno Python** (DC-5).
* [ ] `pyproject.toml` físico.
* [ ] `Makefile` físico.

## ✅ CAPA 1: Entorno de Ejecución (Contenedores)

*Documentos: DC-3, DC-6, DC-7*

* [x] **Gestión de Secretos** (DC-3).
* [x] **Dockerfile** (Diseño: DC-6).
* [x] **docker-compose.yml** (Diseño Profundo: DC-7).
* [x] Definición de `Healthchecks`.
* [x] Segmentación de redes (`backnet` / `frontnet`).
* [x] Gestión de volúmenes persistentes.


* [ ] `.env.example` físico.
* [ ] `entrypoint.sh` (Pendiente diseño).

## 💡 CAPA 2 - 7: (Sin cambios en diseño)

*Trazabilidad mantenida.*

---

**Maestro, ¿este nivel de detalle en el orquestador te da la seguridad necesaria para el control de la nave?** Si es así, ahora sí tenemos una base sólida para el **Documento 8: `entrypoint.sh**`. Este script es el "piloto automático" que ejecutará los comandos de salud y preparación antes de entregarle el mando a Django. ¿Lo elaboramos?