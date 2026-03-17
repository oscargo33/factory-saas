Entendido, Maestro. Con este árbol visual, el panorama es cristalino. Has organizado la **Base de Conocimiento (Capa 00)** como el manual de vuelo, el **Core Concept (Capa 1)** como la misión y el **Design Concept (Capa 2)** como los planos de ingeniería.

Tu nomenclatura es impecable: **-kb**, **-cc** y **-fs** garantizan que nunca mezclemos niveles de abstracción.

Dado que ya tenemos la **Estructura de Carpetas (Archivo 4 en Design-Concept)**, el siguiente paso lógico para completar la **Capa 0 (Gestión)** es el archivo que define el "motor de combustión" del software: **Poetry y las dependencias**.

Siguiendo tu numeración, aquí tienes la propuesta para el archivo 5:

---

# Documento: 5-Configuracion-Poetry-fs.md

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** DC-5-FS

**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/5-configuracion-poetry-fs.md`

**Referencia Core:** `0-factory_saas-cc.md`

**Apellido:** **-fs**

## 1. Definición del Entorno Python

Para asegurar la estabilidad de la Factory, fijamos la versión del lenguaje.

* **Runtime:** Python 3.12+
* **Gestor:** Poetry (Determinismo absoluto de dependencias).

## 2. Grupos de Dependencias (Capa 0)

Dividiremos las librerías para mantener la imagen de producción ligera y el entorno de desarrollo potente.

### A. Grupo: Main (Núcleo Operativo)

* `django`: El framework base.
* `django-tenants`: El motor de aislamiento de esquemas PostgreSQL.
* `psycopg[binary]`: Driver de conexión a base de datos.
* `environs`: Manejo de variables de entorno (Capa 1).

### B. Grupo: Dev/Test (Herramientas de Control)

* `ruff`: Linter y formateador (Sustituye a Flake8/Black/Isort).
* `pytest-django`: Suite de pruebas.
* `factory-boy`: Generación de datos para pruebas de Tenants.

## 3. Configuración del Proyecto (`pyproject.toml`)

Para que la IA y los desarrolladores operen bajo el mismo estándar, el archivo de Poetry debe incluir:

* **In-project Venv:** El entorno virtual se creará en la raíz (`.venv`) para visibilidad directa de las herramientas de edición.
* **Ruff Config:** Definición de línea máxima (100 caracteres) y reglas de importación automáticas.

## 4. Estrategia de Actualización

* Las dependencias se actualizan mediante `poetry update` solo tras pasar los tests de la **App 02 (Telemetry)** en el entorno de Staging.
* El archivo `poetry.lock` es la única "fuente de verdad" para las versiones instaladas en los contenedores Docker.

---

### Trazabilidad con el Checklist

Al terminar este documento, podemos marcar en el archivo `1-checklist-factory-saas.md`:

* [x] Configuración de Poetry y dependencias.
* [x] Estándar de formateo de código (Ruff).
