
# Índice Operativo de Implementación (0-Factory-SaaS)

**Ubicación:** `./docs/1-Design-Concept/0-Factory-SaaS/00-indice-operativo-fs.md`

**Referencia:** Jerarquía de Capas + Gestión de Entorno

**Apellido de Trazabilidad:** **-fs**

## Capa 0: Gestión y Dependencias (El Contenedor del Proyecto)

*Antes de Docker, está el código y sus librerías.*

* `configuracion-poetry-fs.md`: Definición de `pyproject.toml`, grupos de dependencias (dev, prod, test) y gestión de versiones de Python.
* `estructura-de-carpetas-raiz-fs.md`: Organización del repositorio (donde va el código, los documentos, los estáticos y los scripts de gestión).
* `scripts-de-automatizacion-fs.md`: Comandos personalizados (Makefiles o scripts de Python) para levantar el entorno con un solo comando.

## Capa 1: Entorno de Ejecución (Contenerización)

* `dockerfile-maestro-fs.md`: Especificación de la imagen base (Debian/Alpine), capas de optimización y usuario no-root para seguridad.
* `docker-compose-orquestacion-fs.md`: Definición de los servicios, redes internas y política de reinicio.
* `variables-de-entorno-fs.md`: Especificación del archivo `.env.example` y la jerarquía de carga de secretos.

## Capa 2: Persistencia y Almacenamiento

* `configuracion-postgresql-fs.md`: Extensiones (`pgvector`), límites de conexión y *tuning* del motor.
* `estrategia-de-volumenes-fs.md`: Mapeo de carpetas locales vs contenedores para base de datos y archivos media.

## Capa 3: Orquestación y Entrada (Redes)

* `gateway-nginx-fs.md`: Configuración de bloques de servidor para subdominios dinámicos y certificados SSL.
* `configuracion-redis-fs.md`: Uso de Redis como caché y como broker para Celery.

## Capa 4: Arquitectura de Software (Servicios)

* `patron-service-layer-fs.md`: Guía de implementación de los archivos `services.py` y `selectors.py` en cada app.
* `gestion-de-señales-y-eventos-fs.md`: Cómo las apps se comunican de forma asíncrona mediante señales de Django o eventos de Redis.

## Capa 5: Motor de Multitenencia

* `middleware-deteccion-tenant-fs.md`: Lógica para capturar el subdominio y validar el inquilino.
* `router-dinamico-esquemas-fs.md`: El código que inyecta el `search_path` de PostgreSQL en cada petición.
* `bootstrap-de-nuevo-tenant-fs.md`: El proceso automatizado de crear el esquema y correr migraciones al registrar una nueva empresa.

## Capa 6: Base Visual y Frontend

* `pipeline-tailwind-cotton-fs.md`: Cómo se compilan los estilos y cómo se registran los componentes de la App 1.
* `estandar-de-reactividad-alpine-fs.md`: Reglas de uso de Alpine.js para mantener el frontend ligero pero potente.

## Capa 7: Lógica de Fábrica (Operatividad)

* `monitoreo-y-telemetria-local-fs.md`: Cómo la App 2 recolecta datos antes de mandarlos a La Central.
* `flujo-de-onboarding-global-fs.md`: El paso a paso desde que la Home crea un prospecto hasta que Profiles habilita el Dashboard.

---

### ¿Cómo usar este índice?

Este índice es tu **Checklist de Construcción**. Cada vez que la IA o tú terminen un archivo de configuración (como el `pyproject.toml`), marcas este índice.

**¿Te parece si empezamos por la Capa 0 con el documento `configuracion-poetry-fs.md` para definir exactamente qué librerías y qué versión de Python usará el motor de la Factory?**