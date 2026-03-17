Entendido, Maestro. Si el `docker-compose.yml` es el manifiesto de vuelo, el **Dockerfile** es la ingeniería estructural de la nave. Un diseño pobre aquí significa una imagen pesada, lenta de compilar y vulnerable.

Vamos a reconstruir el **DC-6-FS** con un enfoque de **Ingeniería de Producción**, asegurando que cada instrucción tenga una razón de ser técnica.

---

# Documento: 6-dockerfile-maestro-fs.md (Versión Detallada)

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** DC-6-FS

**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/6-dockerfile-maestro-fs.md`

**Referencia Core:** `0-factory_saas-cc.md`

**Apellido:** **-fs**

## 1. Estrategia de Multi-Etapa (Multi-Stage)

Dividimos la construcción en dos fases para separar el entorno de compilación (sucio/pesado) del entorno de ejecución (limpio/ligero).

### Etapa A: `builder-stage`

* **Imagen Base:** `python:3.12-slim-bookworm` (Debian estable y ligera).
* **Dependencias de Compilación:** Instalación de `build-essential` y `libpq-dev` (necesarios para compilar `psycopg` y otras extensiones de C).
* **Gestión de Poetry:** * Instalación de Poetry versión fija para evitar cambios inesperados.
* Configuración de `POETRY_VIRTUALENVS_IN_PROJECT=true` para que el `.venv` se cree en el directorio de trabajo.


* **Proceso:** Se copian *solo* los archivos de dependencias (`pyproject.toml` y `poetry.lock`) y se ejecuta `poetry install --no-root --only main`. Esto crea una capa de caché persistente.

### Etapa B: `runtime-stage` (La Nave Operativa)

* **Imagen Base:** `python:3.12-slim-bookworm`.
* **Higiene de Imagen:** * Se copian solo los binarios y librerías del `.venv` de la etapa anterior.
* No se instalan compiladores ni herramientas innecesarias, reduciendo la superficie de ataque.


* **Usuario de Sistema:** Creación de `factory_user` con UID/GID fijo. Queda **estrictamente prohibido** ejecutar la aplicación como `root`.
* **Directorio de Trabajo:** `/app` con permisos ajustados para el usuario no-privilegiado.

## 2. Variables de Entorno de Sistema (Hard-coded en Imagen)

Estas variables garantizan que Python se comporte correctamente en contenedores:

* `PYTHONDONTWRITEBYTECODE=1`: Evita que Python escriba archivos `.pyc` en el disco del contenedor.
* `PYTHONUNBUFFERED=1`: Fuerza a que los logs salgan inmediatamente a la consola (vital para Cloud Logging).
* `PATH="/app/.venv/bin:$PATH"`: Asegura que los comandos de las librerías instaladas (como `gunicorn`) sean prioritarios.

## 3. Manejo de Capas y Orden de Copia

Para optimizar el tiempo de construcción (Build Time):

1. `COPY --from=builder`: Traemos las dependencias ya listas.
2. `COPY ./scripts/entrypoint.sh`: Copiamos el script de arranque y damos permisos de ejecución.
3. `COPY ./src`: Copiamos el código fuente al final. Al ser lo que más cambia, evitamos que Docker invalide el caché de las capas anteriores.

## 4. Puerto y Señales

* **EXPOSE:** Se declara el puerto `8000`.
* **STOPSIGNAL:** Se define `SIGTERM` para permitir que Gunicorn cierre las conexiones de los Tenants de forma elegante antes de apagarse.

---

# Documento: Checklist de Control de Implementación (Factory-SaaS)

**ID:** CK-01-FS

**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/1-checklist-factory-saas.md`

**Estado:** **SINCRONIZADO**

## ✅ CAPA 0: Gestión y Dependencias (Proyecto Raíz)

* [x] **Estructura Física de Directorios** (DC-4).
* [x] **Estándar de Automatización Híbrido** (DC-2).
* [x] **Configuración de Entorno Python** (DC-5).

## ✅ CAPA 1: Entorno de Ejecución (Contenedores)

* [x] **Gestión de Secretos** (DC-3).
* [x] **Dockerfile (Diseño Profundo)** (DC-6).
* [x] Implementación Multi-stage (Builder vs Runtime).
* [x] Configuración de Usuario No-root.
* [x] Optimización de Capas de Caché.


* [x] **docker-compose.yml (Diseño Profundo)** (DC-7).
* [ ] `.env.example` físico.
* [ ] `entrypoint.sh` (Siguiente paso: Es el script que une el Dockerfile con la App).
