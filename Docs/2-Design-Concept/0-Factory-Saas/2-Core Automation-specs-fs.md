
# Documento: Especificación del Motor de Automatización - fs

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** DC-3-FS

**Ubicación:** `./docs/1-Design-Concept/0-Factory-SaaS/2-core-automation-specs-fs.md`

**Referencia Core:** `0-factory_saas-cc.md`

**Apellido:** **-fs**

## 1. Naturaleza Técnica

Este documento define el sistema de control de mando (CLI) del Factory SaaS. Es un componente crítico de la **Capa 0 (Gestión)** y la **Capa 1 (Entorno)**. El cumplimiento de esta estructura es obligatorio para todas las apps del Product Core.

## 2. Implementación del Cabo de Seguridad (Makefile)

El archivo `Makefile` en la raíz del proyecto es el único punto de entrada permitido para operaciones de infraestructura.

### Comandos Mandatorios:

* `make build`: Orquestación de construcción de imágenes Docker y volúmenes.
* `make up` / `make down`: Control de estado de los servicios.
* `make shell`: Acceso directo al terminal del contenedor de la aplicación.
* `make test`: Ejecución de la suite de pruebas unitarias y de integración.
* `make docs-sync`: Regeneración del versionado documental y del registro maestro de `Docs/`.
* `make docs-check`: Validación no destructiva del gobierno documental; falla si el sincronizador deja cambios pendientes.

## 3. Implementación del Cerebro Operativo (Django Commands)

Las operaciones que requieren sensibilidad de datos o lógica del ORM se implementan como comandos de gestión dentro del contenedor.

### Espacio de Nombres de Comandos:

Todo comando de negocio debe seguir el prefijo de la app para mantener la trazabilidad:

* `python manage.py fs_provision_tenant`: Creación física de esquemas y registros base.
* `python manage.py th_sync_glossary`: Sincronización de traducciones desde JSON a DB.
* `python manage.py at_health_report`: Generación de snapshot de métricas para telemetría.

## 4. Protocolo de Delegación

El `Makefile` debe actuar como envolvedor (wrapper). Queda prohibido que el desarrollador tenga que entrar manualmente al contenedor para ejecutar comandos de negocio.

**Ejemplo de flujo obligatorio:**

```makefile
tenant-create:
	docker-compose exec app python manage.py fs_provision_tenant $(name)

```
