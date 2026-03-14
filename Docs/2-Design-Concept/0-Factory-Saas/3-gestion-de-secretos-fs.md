# Documento: Gestión de Secretos y Configuración - fs

**ID:** DC-4-FS

**Ubicación:** `./docs/1-Design-Concept/0-Factory-SaaS/gestion-de-secretos-fs.md`

**Referencia Core:** `0-factory-saas-cc.md`

**Apellido:** **-fs**

## 1. El Estándar `.env` (Twelve-Factor App)

Para garantizar la portabilidad de la nave, toda configuración que varíe entre entornos (Desarrollo, Staging, Producción) debe residir en variables de entorno.

### Jerarquía de Archivos:

1. `.env.example`: **Obligatorio en Git.** Contiene las llaves necesarias pero con valores vacíos o de ejemplo. Sirve como mapa para nuevos desarrolladores.
2. `.env`: **Prohibido en Git.** Contiene las credenciales reales. Este archivo debe estar listado en el `.gitignore`.

## 2. Tipología de Variables

Para mantener el orden operativo, clasificamos los secretos por su impacto en las capas de ingeniería:

| Prefijo | Capa | Ejemplo | Propósito |
| --- | --- | --- | --- |
| `DB_` | 2 | `DB_PASSWORD` | Credenciales del motor PostgreSQL. |
| `REDIS_` | 3 | `REDIS_URL` | Conexión al broker de mensajería y caché. |
| `DJANGO_` | 4 | `DJANGO_SECRET_KEY` | Seguridad criptográfica y firma de tokens. |
| `TENANT_` | 5 | `TENANT_DOMAIN_SUFFIX` | Base para la resolución de subdominios. |
| `CENTRAL_` | 7 | `CENTRAL_API_KEY` | Token de autenticación con La Central. |

## 3. Inyección de Secretos en el Entorno Contenerizado

El anclaje operacional dicta que Docker no debe "quemar" las variables en la imagen (build-time), sino leerlas en tiempo de ejecución (run-time).

* **Mecánica:** El archivo `docker-compose.yml` debe utilizar la directiva `env_file: .env`.
* **Seguridad:** En entornos de producción, se priorizará la inyección de variables directamente en la memoria del contenedor a través de la interfaz de orquestación, evitando la presencia de archivos físicos `.env` en el disco del servidor siempre que sea posible.

## 4. Validación de Integridad (Bootstrap Check)

La Factory SaaS no debe iniciar su ejecución si existen inconsistencias en la configuración. Se debe implementar un script de validación en la **Capa 4 (Servicios)** que realice lo siguiente:

1. Escanee las variables requeridas definidas en un esquema de validación al arrancar Django.
2. Lanze una excepción de sistema (`ImproperlyConfigured`) con un mensaje claro si una variable esencial es nula o tiene un formato incorrecto.

