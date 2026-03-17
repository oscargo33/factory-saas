# Documento: Estrategia de Ambientes y Staging

**Versión del documento:** 1.0
**Última actualización:** 2026-03-16

**ID:** DC-27-FS
**Ubicacion:** `./Docs/2-Design-Concept/0-Factory-Saas/27-estrategia-ambientes-fs.md`
**Anchor Docs:** `DC-6-FS` (Dockerfile), `DC-7-FS` (Docker Compose), `DC-3-FS` (Secretos), `DC-8-FS` (Entrypoint)
**Backlog:** PB-022

---

## 1. Proposito

Define los tres ambientes de ejecucion del proyecto (development, staging, production), sus diferencias de configuracion, el proceso de promocion de codigo entre ellos, la estrategia de seed de datos de prueba y el modelo de acceso por rol.

Esto elimina la ambiguedad de "funciona en mi maquina" y establece las bases para el pipeline de CI/CD de Fase 6 (PB-051..PB-055).

---

## 2. Mapa de Ambientes

| Propiedad | Development | Staging | Production |
|---|---|---|---|
| **Proposito** | Desarrollo local de cada dev | Pre-produccion, validacion de QA y demos | Usuarios reales |
| **URL base** | `localhost:8000` | `staging.factory-saas.com` | `factory-saas.com` |
| **Django `DEBUG`** | `True` | `False` | `False` |
| **Base de datos** | PostgreSQL local (Docker) | PostgreSQL dedicado (mismo esquema que prod) | PostgreSQL gestionado (RDS / Cloud SQL) |
| **Redis** | Redis local (Docker) | Redis dedicado | Redis gestionado (ElastiCache) |
| **Email** | `locmem` backend (no envia) | SES en modo sandbox | SES production / SendGrid |
| **Celery workers** | 1 worker local | 1-2 workers replica de prod | N workers escalados |
| **Archivos estaticos** | `runserver` sirve estaticos | Nginx + WhiteNoise | CDN (S3 + CloudFront) |
| **Secrets manager** | `.env` local (no commiteado) | Variables de entorno en CI + Vault | Vault / AWS Secrets Manager |
| **Multi-tenancy (schemas)** | Crea tenants manualmente via /admin | Seed automatico (ver Seccion 5) | Tenants reales |
| **Datos de prueba** | Factories y fixtures de dev | Seed automatico (dataset anonimizado) | Datos reales |
| **Acceso** | Local o tunel ngrok | Solo equipo + QA + stakeholders internos | Publico |

---

## 3. Perfiles de Configuracion Django (settings)

Estructura de configuracion:

```
config/
  settings/
    base.py         # Configuracion comun a todos los ambientes
    development.py  # Override para local
    staging.py      # Override para staging
    production.py   # Override para produccion
    test.py         # Override para pytest (sin emails, Celery eager)
```

### 3.1. `base.py` (comun)

```python
SECRET_KEY = env('SECRET_KEY')  # nunca hardcoded
INSTALLED_APPS = [...] # todas las apps
DATABASES = {'default': env.db('DATABASE_URL')}
REDIS_URL = env('REDIS_URL')
CELERY_BROKER_URL = REDIS_URL
```

### 3.2. `development.py`

```python
from .base import *
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*.ngrok.io']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
INTERNAL_IPS = ['127.0.0.1']
```

### 3.3. `staging.py`

```python
from .base import *
DEBUG = False
ALLOWED_HOSTS = ['staging.factory-saas.com', '*.staging.factory-saas.com']
EMAIL_BACKEND = 'anymail.backends.amazon_ses.EmailBackend'
ANYMAIL = {'AMAZON_SES_CLIENT_PARAMS': {'region_name': 'us-east-1'}}
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 3.4. `production.py`

```python
from .base import *
DEBUG = False
ALLOWED_HOSTS = ['factory-saas.com', '*.factory-saas.com']
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 3.5. `test.py`

```python
from .base import *
DEBUG = False
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
DEFAULT_FILE_STORAGE = 'django.core.files.storage.InMemoryStorage'
```

---

## 4. Variables de Entorno por Ambiente

### Variables requeridas en todos los ambientes

| Variable | Descripcion | Ejemplo dev |
|---|---|---|
| `SECRET_KEY` | Django secret key (unica por ambiente) | `django-insecure-...` |
| `DATABASE_URL` | URL de conexion PostgreSQL | `postgres://user:pass@localhost:5432/factory` |
| `REDIS_URL` | URL de Redis | `redis://localhost:6379/0` |
| `DJANGO_SETTINGS_MODULE` | Perfil activo | `config.settings.development` |
| `ALLOWED_HOSTS` | Hosts validos (separados por coma) | `localhost,127.0.0.1` |
| `DEFAULT_FROM_EMAIL` | Email sender por defecto | `noreply@factory-saas.com` |

### Variables adicionales solo en staging/production

| Variable | Descripcion |
|---|---|
| `AWS_ACCESS_KEY_ID` | Credenciales SES |
| `AWS_SECRET_ACCESS_KEY` | Credenciales SES |
| `STRIPE_SECRET_KEY` | Gateway de pagos |
| `STRIPE_WEBHOOK_SECRET` | HMAC para webhooks de Stripe |
| `SENTRY_DSN` | Error tracking |
| `VAULT_ADDR` / `VAULT_TOKEN` | Acceso a Vault para secretos adicionales |

### Gestion de secretos por ambiente

| Ambiente | Mecanismo |
|---|---|
| Development | Archivo `.env` local (gitignored), copiado desde `.env.example` |
| Staging | Variables en el sistema de CI (GitHub Actions Secrets / GitLab CI Variables) |
| Production | Vault (HashiCorp) o AWS Secrets Manager; inyectadas al contenedor en runtime |

> **Regla de seguridad:** Ningun secreto se commitea en el repositorio. `.env` siempre en `.gitignore`. Solo `.env.example` con valores vacios o ficticios se trackea.

---

## 5. Seed de Datos de Prueba (Staging)

El ambiente de staging debe tener datos realistas para QA y demos sin usar datos de usuarios reales.

### 5.1. Script de seed

`python manage.py seed_staging`

Este comando (custom management command):

1. Crea 3 tenants de prueba: `alpha-corp`, `beta-corp`, `gamma-demo`.
2. Crea usuarios de prueba con roles distintos por tenant:
   - `owner@alpha-corp.example.com` (rol: Owner)
   - `admin@alpha-corp.example.com` (rol: Admin)
   - `member@alpha-corp.example.com` (rol: Member)
3. Crea planes de prueba: Free, Pro, Enterprise.
4. Crea suscripciones activas para cada tenant.
5. Crea ordenes de ejemplo con distintos estados.
6. Crea tickets de soporte de ejemplo.

### 5.2. Reset de staging

`python manage.py reset_staging` — destruye y re-crea todos los datos de seed. Solo ejecutable con flag `--confirm`. Nunca disponible en production.

### 5.3. Dataset para tests E2E

El tenant `e2e_test_tenant` es exclusivo para Playwright E2E. Se resetea antes de cada run de E2E en CI.

---

## 6. Proceso de Promocion de Codigo

```
feature-branch  →  PR review  →  main (staging-auto)  →  tag vX.Y.Z  →  production
```

### 6.1. Dev → Staging (automatico)

- Cada merge a `main` dispara el pipeline de CI:
  1. Lint + format check (`ruff`, `black`)
  2. Tests + cobertura (minimo 80%)
  3. Build de imagen Docker
  4. Push de imagen a registry (ECR / Docker Hub)
  5. Deploy automatico a staging via `docker compose pull && docker compose up -d`

- Si cualquier paso falla: deploy cancelado, notificacion al autor del PR.

### 6.2. Staging → Production (manual con gate)

1. QA aprueba el build en staging (checklist manual o automatizado).
2. Tech Lead crea un tag: `git tag v1.2.3 && git push origin v1.2.3`.
3. Pipeline de release se activa solo con tags `v*.*.*`.
4. Deploy a produccion ejecuta zero-downtime migration (ver DC-23) antes de reiniciar workers.
5. Healthcheck automatico tras el deploy: si falla, rollback automatico a imagen anterior.

### 6.3. Rollback de emergencia

```bash
# Rollback a imagen anterior en produccion
docker compose pull factory-web:v1.2.2
docker compose up -d --no-deps factory-web
python manage.py check_migrations  # verifica estado de migraciones
```

---

## 7. Acceso por Ambiente

| Rol | Development | Staging | Production |
|---|---|---|---|
| Developer | Acceso total local | SSH / VPN + acceso a logs | Solo lectura de logs via Sentry/dashboards |
| QA Engineer | Acceso local | Acceso total a staging | Solo logs de errores |
| Tech Lead | Acceso total | Acceso total | Acceso al pipeline de release + monitoreo |
| DevOps | Acceso infraestructura | Acceso total | Acceso total |
| Stakeholders / Demo | N/A | Acceso a URL de staging (readonly demo) | Dash. de metricas (no datos sensibles) |

> **Principio de minimo privilegio:** Ningun developer tiene acceso SSH directo a la base de datos de produccion. Los accesos se gestionan via bastion host con auditoria.

---

## 8. Docker Compose por Ambiente

### 8.1. `docker-compose.yml` (base, production-ready)

Definicion canonica del stack completo. Ver DC-7-FS.

### 8.2. `docker-compose.override.yml` (desarrollo local, gitignored en casos sensibles)

```yaml
services:
  factory-web:
    build: .
    volumes:
      - .:/app  # hot-reload
    environment:
      DJANGO_SETTINGS_MODULE: config.settings.development
      DEBUG: "True"
  factory-worker:
    command: celery -A config worker --loglevel=debug
```

### 8.3. `docker-compose.staging.yml`

```yaml
services:
  factory-web:
    image: registry.example.com/factory-saas:${IMAGE_TAG}
    environment:
      DJANGO_SETTINGS_MODULE: config.settings.staging
```

---

## 9. Runbook de Deploy a Staging

```
1. $ git checkout main && git pull origin main
2. CI dispara automaticamente (ver Seccion 6.1)
3. Verificar GitHub Actions: todos los steps en verde
4. Acceder a https://staging.factory-saas.com/health/ → esperar {"status": "ok"}
5. Ejecutar smoke tests manuales: login, crear tenant, navegar dashboard
6. Notificar al equipo en canal #staging-deploys
```

---

## 10. DoD de este Documento

- [ ] Los 3 ambientes definidos con sus diferencias de configuracion.
- [ ] Estructura de settings por ambiente documentada con ejemplos de codigo.
- [ ] Variables de entorno requeridas listadas por ambiente.
- [ ] Estrategia de gestion de secretos establecida (no hay secretos en repo).
- [ ] Seed de datos de staging documentado con management commands.
- [ ] Proceso de promocion dev→staging→prod con gates definidos.
- [ ] Rollback de emergencia documentado.
- [ ] Modelo de acceso por rol establecido siguiendo principio de minimo privilegio.
- [ ] Docker Compose por ambiente especificado.
- [ ] Runbook de deploy basico documentado.
- [ ] Indexado en `0-index.md` de Factory-SaaS global.
