# Documento: 18-matriz-seguridad-compliance-fs.md

**ID:** DC-18-FS
**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/18-matriz-seguridad-compliance-fs.md`
**Referencia Core:** `0-factory_saas-cc.md`, `3-gestion-de-secretos-fs.md`
**Capa:** Transversal — Seguridad y Compliance
**Apellido:** **-fs**

---

## 1. Propósito

Este documento es la **ancla de seguridad** de la Factory. Define:
- Los controles de seguridad mandatorios por capa.
- La clasificación de datos (PII, financieros, sensibles).
- Las medidas de compliance aplicables (OWASP Top 10, GDPR/LGPD, PCI DSS básico).
- La política de retención y eliminación de datos.

---

## 2. Clasificación de Datos

| Clase | Descripción | Ejemplos | Protección Requerida |
|---|---|---|---|
| **PII** (Datos Personales) | Identifica a una persona física | Email, nombre, dirección, IP, avatar | Cifrado en tránsito, acceso auditado, retención limitada |
| **Financiero** | Datos de pago y facturación | Número de tarjeta, CVV, IBAN | Nunca almacenar en la Factory; delegar a gateway PCI-DSS |
| **Sensible de Negocio** | Datos confidenciales del tenant | Precios, catálogos, configuraciones | Aislamiento de esquema, acceso por rol |
| **Operacional** | Logs, métricas, telemetría | Event types, contadores, errores | Retención definida, sin PII en telemetría |
| **Público** | Sin restricciones | Landing pages, documentación | Sin controles especiales |

---

## 3. OWASP Top 10: Controles por Capa

### 3.1. A01 — Broken Access Control

| Control | Implementación |
|---|---|
| Aislamiento de tenant | `TenantMiddleware` + `search_path` garantiza que ningún usuario lee datos de otro tenant |
| Autorización por rol | Decoradores `@permission_required` o mixins basados en `Membership.role` |
| IDOR prevention | Todas las queries incluyen `tenant_id` como filtro implícito; nunca por ID solo |
| Admin Django | Solo accesible en red privada (`backnet_fs`); no expuesto en Nginx para subdominio de tenants |

### 3.2. A02 — Cryptographic Failures

| Control | Implementación |
|---|---|
| HTTPS obligatorio | Nginx termina SSL; Django `SECURE_SSL_REDIRECT = True` en producción |
| Passwords | Django `argon2` como hasher de contraseñas (por encima del default PBKDF2) |
| Secretos | Variables de entorno desde vault; nunca en código. Ver DC-3 |
| Cookies | `SESSION_COOKIE_SECURE = True`, `CSRF_COOKIE_SECURE = True`, `SESSION_COOKIE_HTTPONLY = True` |
| Telemetría | PII no viaja en payloads de telemetría (DC-15) |

### 3.3. A03 — Injection (SQL, XSS, Command)

| Tipo | Control |
|---|---|
| SQL Injection | ORM de Django con queries parametrizadas. Raw SQL prohibido salvo DBA-reviewed migrations |
| XSS | Auto-escaping de Django templates habilitado. Alpine.js nunca usa `innerHTML` con datos del usuario |
| Command Injection | No se ejecutan comandos shell con input del usuario. `subprocess` prohibido en views/services |
| Template Injection | Cotton components usar `{{ var }}` (auto-escaped), nunca `{% autoescape off %}` |

### 3.4. A04 — Insecure Design

| Control | Implementación |
|---|---|
| Threat modeling | Este documento es el artefacto de diseño de amenazas de la Factory |
| Defense in depth | Layers: Nginx → Django Middleware → View Permissions → Service validation → DB isolation |
| Least Privilege | `factory_user` en PostgreSQL sin SUPERUSER. Docker container como `factory_user` sin root |

### 3.5. A05 — Security Misconfiguration

| Control | Implementación |
|---|---|
| `DEBUG = False` en producción | Controlado por `APP_ENV` env var en `entrypoint.sh` |
| `ALLOWED_HOSTS` | Solo los dominios de la instancia; nunca `*` en producción |
| Headers de seguridad | Nginx añade `X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection` |
| Django Admin | URL randomizada; no en `/admin/` en producción |
| Servicios internos | Redis y PostgreSQL solo en `backnet_fs`; no expuestos al host |

### 3.6. A06 — Vulnerable Components

| Control | Implementación |
|---|---|
| Dependencias | Poetry con `poetry.lock` para versiones fijas |
| Auditoría | `pip audit` / `safety check` en pipeline CI/CD |
| Imagen base | `python:3.12-slim` actualizada en cada build; no `latest` |
| OS del container | Actualizaciones de `apt` durante el build de Docker |

### 3.7. A07 — Auth Failures

| Control | Implementación |
|---|---|
| Rate limiting en login | `django-ratelimit` o equivalente en endpoint de login (max 5 intentos / 15 min) |
| MFA | Diseñado como feature de la app `core`; requerido para roles `owner` y `admin` |
| Token JWT | TTL ≤ 60s para comunicación con La Central (DC-15) |
| Session fixation | `SESSION_COOKIE_AGE` definido; rotación de session ID en login |

### 3.8. A08 — Software Integrity Failures

| Control | Implementación |
|---|---|
| Pipeline CI/CD | Builds reproducibles desde `poetry.lock` + `Dockerfile` versionado |
| No `eval()` | Prohibido `eval()` y `exec()` con input externo en cualquier parte |
| Serialización | Celery usa `json` serializer (no `pickle`). DC-11 |

### 3.9. A09 — Logging & Monitoring Failures

| Control | Implementación |
|---|---|
| Access log | Nginx registra todos los accesos con IP, status, y `X-Trace-ID` |
| Application log | Django logging a `stdout` (capturado por Docker logging driver) |
| Audit log | Acciones sensibles (login, create_tenant, change_role) registradas en tabla `AuditLog` |
| Error monitoring | `TelemetryEvent` tipo `error.500` para correlación con La Central (DC-15) |
| Log retention | Logs de aplicación: 30 días. Audit log: 1 año |

### 3.10. A10 — SSRF

| Control | Implementación |
|---|---|
| URL del usuario | Ningún servicio de la Factory realiza requests HTTP a URLs provistas por el usuario sin validación |
| Webhooks salientes | Lista blanca de dominios permitidos para webhooks configurados por el tenant |
| La Central | URL hardcodeada en `CENTRAL_API_URL`; no configurable por el tenant |

---

## 4. Datos PII: Inventario y Política

| Entidad | Campo PII | App Owner | Retención | Acción en eliminación |
|---|---|---|---|---|
| `User` | `email`, `username` | `core` | Vida de la cuenta | Anonimizar al borrar cuenta |
| `Profile` | `display_name`, `bio`, `avatar_url` | `profile` | Vida de la membresía | Eliminar físicamente |
| `SupportTicket` | `body` (puede contener PII) | `support` | 2 años post-cierre | Archivar cifrado |
| `Order` | `shipping_address` (si aplica) | `orders` | 5 años (fiscal) | Retener cifrado |
| `Membership` | `user_id` (referencia a PII) | `core` | Vida del tenant | Desvincular al cancelar |

---

## 5. Política de Retención de Datos

| Tipo de dato | Retención | Método de eliminación |
|---|---|---|
| Sesiones | 2 semanas desde último acceso | Auto-expiración en Redis |
| Logs de acceso | 30 días | Rotación por Docker logging |
| Audit log | 1 año | Archivado + purga automática |
| TelemetryEvents enviados | 30 días post-envío | Purga programada (`prune` task) |
| Datos de tenant cancelado | 90 días post-cancelación | Notificación → export → DROP SCHEMA |

---

## 6. PCI DSS: Alcance y Delegación

La Factory **no almacena, procesa, ni transmite datos de tarjetas de pago (CHD)**. El procesamiento de pagos es delegado completamente al gateway externo (Stripe, Conekta, etc.).

| Elemento | Política |
|---|---|
| Número de tarjeta (PAN) | Jamás almacenado en la Factory. Solo `last4` y `brand` para display |
| CVV/CVC | Jamás almacenado |
| Datos de facturación | Solo nombre y país del titular (para display) |
| Tokenización | El gateway provee un token; la Factory almacena solo el token |

---

## 7. Hardening de Configuración Django (Producción)

| Setting | Valor seguro |
|---|---|
| `DEBUG` | `False` |
| `SECRET_KEY` | 50+ caracteres aleatorios, desde secrets vault |
| `ALLOWED_HOSTS` | Lista explícita de dominios |
| `SECURE_HSTS_SECONDS` | `31536000` (1 año) |
| `SECURE_HSTS_INCLUDE_SUBDOMAINS` | `True` |
| `SECURE_CONTENT_TYPE_NOSNIFF` | `True` |
| `X_FRAME_OPTIONS` | `'SAMEORIGIN'` |
| `CSRF_COOKIE_SECURE` | `True` |
| `SESSION_COOKIE_SECURE` | `True` |
| `SESSION_COOKIE_HTTPONLY` | `True` |
| `SESSION_COOKIE_SAMESITE` | `'Lax'` |

---

## 8. Relación con Otros Documentos

| Documento | Relación |
|---|---|
| DC-3 `3-gestion-de-secretos-fs.md` | Gestión de secretos y variables sensibles |
| DC-10 `10-gateway-nginx-fs.md` | Headers de seguridad HTTP configurados en Nginx |
| DC-13 `13-router-dinamico-esquemas-fs.md` | Aislamiento de datos a nivel de esquema PostgreSQL |
| DC-15 `15-protocolo-comunicacion-central-fs.md` | Protocolo seguro para telemetría (JWT, no-PII) |
| DC-17 `17-diccionario-datos-logico-fs.md` | Inventario de entidades con clasificación PII |

---

## 9. Criterios de Aceptación del Diseño

- [ ] Los 10 controles OWASP Top 10 tienen una medida de mitigación documentada.
- [ ] Ningún campo PII viaja en payloads de telemetría.
- [ ] Los datos de tarjeta (PAN, CVV) nunca son almacenados en ninguna tabla de la Factory.
- [ ] La política de retención define períodos específicos para cada tipo de dato.
- [ ] Todos los settings de hardening Django están documentados con su valor de producción.
- [ ] El audit log cubre: login, create_tenant, change_role y change_subscription.
