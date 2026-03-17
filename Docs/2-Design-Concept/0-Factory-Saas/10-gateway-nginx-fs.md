# Documento: 10-gateway-nginx-fs.md

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** DC-10-FS
**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/10-gateway-nginx-fs.md`
**Referencia Core:** `0-factory_saas-cc.md`
**Capa:** 3 — Orquestación y Entrada (Red)
**Apellido:** **-fs**

---

## 1. Propósito

Nginx actúa como el **punto de entrada único** de toda la Factory. Su rol es:
- Enrutar tráfico HTTP/HTTPS entrante hacia el proceso Django/Gunicorn.
- Resolver **subdominios dinámicos** para identificar al tenant antes de que el request llegue a Django.
- Servir archivos estáticos directamente sin pasar por el proceso Python.
- Terminar SSL (en producción) mediante certificados por tenant o wildcard.

---

## 2. Arquitectura de Subdominios (Multi-Tenancy)

El modelo de URL de la Factory es `{tenant-slug}.factory.com`. Nginx recibe el request y lo pasa a Gunicorn con el header `Host` intacto. El middleware de Django (DC-13) extrae el subdominio del header `Host` para identificar el tenant.

```
Internet
    │
    ▼
[Nginx: frontnet_fs]
    │  recibe: GET https://acme.factory.com/dashboard
    │  header Host: acme.factory.com
    │
    ▼
[Gunicorn: backnet_fs :8000]
    │  Django Middleware lee Host → slug = "acme"
    │  Router inyecta search_path = tenant_acme
    │
    ▼
[PostgreSQL: backnet_fs :5432]
    │  schema: tenant_acme
```

---

## 3. Configuración de Nginx

### 3.1. Estructura de Archivos

```
nginx/
├── nginx.conf              ← Configuración global (worker_processes, events)
├── conf.d/
│   ├── factory.conf        ← Virtual host principal (catch-all para subdominios)
│   └── static.conf         ← Configuración de archivos estáticos
└── ssl/                    ← Certificados (montados como volumen en producción)
    ├── factory.crt
    └── factory.key
```

### 3.2. Configuración Global (`nginx.conf`)

Parámetros clave:

| Parámetro | Valor | Razón |
|---|---|---|
| `worker_processes` | `auto` | Usar todos los núcleos disponibles |
| `worker_connections` | `1024` | Conexiones simultáneas por worker |
| `keepalive_timeout` | `65` | Tiempo de conexión keep-alive |
| `gzip` | `on` | Comprimir respuestas `text/html`, `application/json` |
| `client_max_body_size` | `10m` | Límite de upload (ajustar para archivos de tenant) |

### 3.3. Virtual Host para la Factory (`factory.conf`)

El diseño usa un bloque `server` con **wildcard de subdominio** para capturar todos los tenants:

```
Patrón de server_name: *.factory.com factory.com
```

**Secciones del bloque server:**

| Sección | Configuración | Propósito |
|---|---|---|
| `location /static/` | `alias /app/staticfiles/; expires 30d;` | Servir CSS/JS sin tocar Gunicorn |
| `location /media/` | `alias /app/media/; expires 7d;` | Servir archivos de usuario |
| `location /` | `proxy_pass http://app:8000;` | Todo lo demás va a Django |

**Headers que Nginx inyecta al proxy:**

| Header | Valor | Uso en Django |
|---|---|---|
| `X-Forwarded-For` | `$proxy_add_x_forwarded_for` | IP real del cliente |
| `X-Forwarded-Proto` | `$scheme` | Detectar HTTP vs HTTPS |
| `Host` | `$host` | Middleware de tenant extrae el subdominio |

### 3.4. Configuración SSL (Producción)

- **Protocolo mínimo:** TLSv1.2 (deshabilitar SSLv2, SSLv3, TLSv1.0, TLSv1.1).
- **Cipher suite:** `ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384` (seguros, sin RC4 ni 3DES).
- **HSTS:** `Strict-Transport-Security: max-age=31536000; includeSubDomains`.
- **Estrategia de certificados:** Wildcard `*.factory.com` via Let's Encrypt (Certbot sidecar o DNS challenge).

---

## 4. Servicio de Nginx en Docker Compose

El servicio `nginx` se define en `docker-compose.yml` (DC-7) con:

| Propiedad | Valor | Descripción |
|---|---|---|
| Imagen | `nginx:1.27-alpine` | Versión estable ligeraño |
| Red | `frontnet_fs` y `backnet_fs` | Gateway entre internet y app |
| Puertos | `80:80`, `443:443` | Solo los puertos de Nginx se exponen al host |
| Volúmenes | `static_fs:/app/staticfiles:ro`, `media_fs:/app/media:ro` | Acceso de solo lectura a statics |
| `depends_on` | `app` | No arranca hasta que Gunicorn esté disponible |

---

## 5. Seguridad de Nginx

| Riesgo | Mitigación |
|---|---|
| Exposición de cabeceras de servidor | `server_tokens off;` oculta la versión de Nginx |
| Clickjacking | Header `X-Frame-Options: SAMEORIGIN` |
| XSS | Header `X-Content-Type-Options: nosniff` |
| Acceso a archivos ocultos | `location ~ /\. { deny all; }` bloquea `.env`, `.git` |
| Rate limiting básico | `limit_req_zone` sobre la dirección IP del cliente |

---

## 6. Relación con Otros Documentos

| Documento | Relación |
|---|---|
| DC-7 `7-docker-compose-specs-fs.md` | Define el servicio `nginx` y las redes `frontnet_fs`/`backnet_fs` |
| DC-8 `8-entrypoint-specs-fs.md` | `collectstatic` produce los archivos que Nginx sirve directamente |
| DC-13 `13-router-dinamico-esquemas-fs.md` | Explica cómo Django procesa el header `Host` pasado por Nginx |

---

## 7. Criterios de Aceptación del Diseño

- [ ] Nginx es el único servicio con puertos expuestos al host (80, 443).
- [ ] Los archivos estáticos y media son servidos por Nginx sin pasar por Gunicorn.
- [ ] El header `Host` llega intacto a Django para la detección de tenant.
- [ ] SSL con TLSv1.2 mínimo y HSTS habilitado en producción.
- [ ] `server_tokens off` y headers de seguridad configurados.
- [ ] Acceso a archivos `.` (dot files) bloqueado.
