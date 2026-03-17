# Documento: Estructura de Repositorio y Carpetas Raíz - fs

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** DC-5-FS

**Ubicación:** `./docs/1-Design-Concept/0-Factory-SaaS/estructura-de-carpetas-fs.md`

**Referencia Core:** `0-factory-saas-cc.md`

**Apellido:** **-fs**

## 1. Filosofía de Organización

La estructura sigue un modelo de **Separación de Preocupaciones**, aislando la documentación, la configuración de infraestructura y el código fuente. El objetivo es que el repositorio sea navegable de forma intuitiva.

## 2. Árbol de Directorios Maestro

```text
factory-saas/
├── .envs/                  # Almacenamiento de archivos .env (locales/prod)
├── deploy/                 # Configuraciones específicas de servidor (Nginx, SSL)
├── docs/                   # La fuente de la verdad (Documentación)
│   ├── 0-Core_concept/     # El "Qué" (Documentos -cc)
│   └── 1-Design_Concept/   # El "Cómo" (Documentos -fs, -th, etc.)
├── scripts/                # Automatizaciones auxiliares (Bash/Python)
├── src/                    # Código Fuente del Proyecto (Capa 7)
│   ├── apps/               # Las 9 Apps Autónomas (01_theme a 09_home) y Product Core
│   ├── core/               # El "Pegamento" (Settings, WSGI, Management)
│   └── static_shared/      # Activos globales (Logo de Factory, fuentes)
├── tests/                  # Suite de pruebas unitarias e integración
├── docker-compose.yml      # Orquestación de Capa 1
├── Dockerfile              # Definición de imagen de Capa 1
├── Makefile                # El Cabo de Seguridad (Capa 0)
└── pyproject.toml          # Gestión de Poetry (Capa 0)

```

## 3. Reglas de Ubicación por Capa

Para mantener la trazabilidad, los elementos de las capas de ingeniería se ubican de la siguiente manera:

* **Capa 0 (Gestión):** Archivos en la raíz (`Makefile`, `pyproject.toml`).
* **Capa 1 (Entorno):** Archivos en la raíz (`Dockerfile`, `docker-compose.yml`).
* **Capa 2 y 3 (Persistencia/Red):** Carpetas de configuración en `deploy/` y volúmenes locales.
* **Capa 4 (Servicios):** Dentro de cada aplicación en `src/apps/[app_name]/services.py`.
* **Capa 5 (Tenancy):** Lógica centralizada en `src/core/db/` y `src/core/middleware/`.
* **Capa 6 y 7 (UI/Negocio):** Carpetas individuales dentro de `src/apps/`.

## 4. El Estándar `src/apps/`

Cada una de las 9 apps debe tener una estructura interna idéntica para facilitar la rotación de mantenimiento:

```text
src/apps/06_orders/
├── cotton/          # Componentes visuales exclusivos de la app
├── management/      # Comandos de Python exclusivos
├── migrations/      # Migraciones de base de datos del esquema de tenant
├── selectors.py     # Consultas de datos (Capa 4)
├── services.py      # Lógica de negocio (Capa 4)
├── models.py        # Definición de tablas
└── views.py         # Controladores de interfaz

```

## 5. Validación de Anclaje

Queda prohibido crear carpetas en la raíz que no estén definidas en este documento sin una actualización previa de la especificación de diseño.
