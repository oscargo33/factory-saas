# Documento: 11-configuracion-redis-celery-fs.md

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** DC-11-FS
**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/11-configuracion-redis-celery-fs.md`
**Referencia Core:** `0-factory_saas-cc.md`
**Capa:** 3 — Orquestación y Entrada (Mensajería y Caché)
**Apellido:** **-fs**

---

## 1. Propósito

Redis y Celery forman la columna vertebral de **procesamiento asíncrono** de la Factory:

- **Redis** — Servidor de caché y broker de mensajes. Almacena sesiones, caché de internacionalización (i18n), y la cola de tareas de Celery.
- **Celery** — Ejecutor de tareas en segundo plano. Procesa telemetría, envío de correos, webhooks y sincronizaciones.

---

## 2. Redis: Diseño de Base de Datos

Redis permite múltiples bases de datos numéricas (`DB 0` a `DB 15`). Se asigna una base de datos por función para garantizar aislamiento y limpieza selectiva.

| DB | Función | Tiempo de Vida (TTL) | Cliente |
|---|---|---|---|
| `0` | Caché Django (i18n, fragmentos HTML) | Variable por vista (5 min – 24 h) | Django `django-redis` |
| `1` | Sesiones de usuario | 2 semanas (configurable) | Django `django-redis` session backend |
| `2` | Broker de Celery (colas de tareas) | Hasta consumirse | Celery broker |
| `3` | Backend de resultados de Celery | 1 hora | Celery result backend |
| `4` | Rate limiting (django-ratelimit o similar) | Ventana de tiempo de la regla | Django middleware |

### 2.1. Configuración del Servicio Redis

| Parámetro | Valor | Razón |
|---|---|---|
| Imagen Docker | `redis:7.2-alpine` | Versión LTS ligera |
| Puerto interno | `6379` | Solo en `backnet_fs`, no expuesto al host |
| Persistencia | `--appendonly yes` + `--save 60 1` | AOF + RDB para durabilidad |
| Límite de memoria | `maxmemory 256mb` | Prevenir consumo descontrolado |
| Política de evicción | `maxmemory-policy allkeys-lru` | Desalojar las claves menos usadas |
| Volumen | `redis_data_fs:/data` | Persistir datos entre reinicios |

---

## 3. Diseño de Colas de Celery

### 3.1. Colas y Prioridades

La Factory define colas especializadas para segmentar carga y garantizar SLAs:

| Cola | Prioridad | Tareas asignadas |
|---|---|---|
| `default` | Normal | Procesamiento general, notificaciones secundarias |
| `telemetry` | Normal | Envío de métricas a La Central (DC-15) |
| `emails` | Alta | Confirmaciones, alertas críticas de usuario |
| `payments` | Crítica | Webhooks de pago, actualizaciones de suscripción |
| `slow` | Baja | Generación de reportes, exportaciones masivas |

### 3.2. Configuración del Worker Celery

| Parámetro | Valor | Razón |
|---|---|---|
| `concurrency` | `4` | Número de procesos worker (ajustar según CPU del host) |
| `loglevel` | `INFO` (prod) / `DEBUG` (dev) | Nivel de log del worker |
| `max_tasks_per_child` | `1000` | Reiniciar worker tras N tareas para prevenir memory leaks |
| `task_soft_time_limit` | `300` (5 min) | Levantar `SoftTimeLimitExceeded` si tarda más |
| `task_time_limit` | `360` (6 min) | Matar el worker si `soft_limit` es ignorado |
| `task_acks_late` | `True` | El task se confirma solo al completarse, no al recibirse |

### 3.3. Estrategia de Reintentos (Retry Policy)

Para garantizar entrega ante fallos de red o externos, todas las tareas críticas adoptan **backoff exponencial con jitter**:

```
Intento 1: espera 2s
Intento 2: espera 4s
Intento 3: espera 8s
...
Intento N: espera min(2^N, 300) s + jitter(0..10s)
Máximo de reintentos: 10
```

| Parámetro Celery | Valor |
|---|---|
| `autoretry_for` | `(ConnectionError, TimeoutError, ServiceUnavailable)` |
| `retry_backoff` | `True` |
| `retry_backoff_max` | `300` |
| `retry_jitter` | `True` |
| `max_retries` | `10` |

---

## 4. Celery Beat (Tareas Programadas)

Celery Beat ejecuta las tareas periódicas. El scheduler usa la base de datos de Django (`django-celery-beat`) para persistencia de schedules, permitiendo configuración dinámica sin redesplegar.

| Tarea periódica | Frecuencia | Cola | Descripción |
|---|---|---|---|
| `telemetry.push_metrics` | Cada 5 min | `telemetry` | Enviar batch de métricas a La Central |
| `tenants.prune_inactive` | Diario 02:00 UTC | `slow` | Marcar tenants inactivos por 90 días |
| `payments.sync_subscriptions` | Cada hora | `payments` | Reconciliar estado de suscripciones con gateway |
| `support.escalate_stale_tickets` | Cada 30 min | `default` | Escalar tickets sin respuesta en SLA |

---

## 5. Configuración Django

Parámetros a incluir en `settings/base.py`:

| Setting Django | Valor |
|---|---|
| `CELERY_BROKER_URL` | `redis://redis:6379/2` |
| `CELERY_RESULT_BACKEND` | `redis://redis:6379/3` |
| `CACHES["default"]["BACKEND"]` | `django_redis.cache.RedisCache` |
| `CACHES["default"]["LOCATION"]` | `redis://redis:6379/0` |
| `SESSION_ENGINE` | `django.contrib.sessions.backends.cache` |
| `SESSION_CACHE_ALIAS` | `default` |

---

## 6. Seguridad

| Riesgo | Mitigación |
|---|---|
| Redis expuesto en red pública | Solo accesible en `backnet_fs`; puerto 6379 no mapeado al host |
| Inyección de comandos via Redis | Deshabilitar comandos peligrosos: `RENAME-COMMAND FLUSHALL ""` |
| Datos de sesión robados en memoria | TTL corto en sesiones + `SESSION_COOKIE_SECURE = True` en Django |
| Tareas sensibles en cola legible | Serialización `json` (no pickle) + datos mínimos en payload (solo IDs) |

---

## 7. Relación con Otros Documentos

| Documento | Relación |
|---|---|
| DC-7 `7-docker-compose-specs-fs.md` | Define los servicios `redis` y `celery_worker`, volumen `redis_data_fs` |
| DC-15 `15-protocolo-comunicacion-central-fs.md` | La tarea `telemetry.push_metrics` usa la cola `telemetry` aquí diseñada |
| DC-12 `12-patron-service-layer-fs.md` | Las tareas Celery invocan servicios (`services.py`) internamente |

---

## 8. Criterios de Aceptación del Diseño

- [ ] Redis usa `DB 0-4` con funciones claramente aisladas.
- [ ] Celery define al menos 5 colas con prioridades documentadas.
- [ ] La política de retry usa backoff exponencial con jitter.
- [ ] Redis solo es accesible en `backnet_fs`.
- [ ] `FLUSHALL` y `FLUSHDB` deshabilitados en producción.
- [ ] Serialización de tareas en formato `json` (nunca `pickle`).
- [ ] `task_acks_late = True` para garantizar entrega at-least-once.
