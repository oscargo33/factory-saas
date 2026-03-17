Este es el **Documento Maestro 2: App Api / Telemetry (El Sensor de La Central)**. Como programador, este documento te servirá para instruir a la IA en la creación del "nervio óptico" que conecta tu SaaS con el dashboard global de monitoreo.

---

# Documento Maestro 2: App Api / Telemetry (Enlace y Observabilidad)

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

## 1. Identidad de la Aplicación

* **Nivel de Profundidad:** 2 (Capa de Consciencia).
* **Rol:** Agente emisor de métricas y receptor de inspecciones desde **La Central**.
* **Dependencias:** Ninguna (Autónoma). Registra eventos de las Apps 3 a la 9.

## 2. Estructura de Archivos (Arquitectura de Carpetas)

```text
telemetry/
├── api/               # Endpoints exclusivos para La Central (DRF)
│   ├── serializers.py
│   └── views.py
├── services.py        # Lógica de envío asíncrono y agregación de métricas
├── middleware.py      # Captura de Trace-ID y tiempos de respuesta
├── tasks.py           # Tareas de Celery para el "Push" a La Central
├── models.py          # Registro inmutable de Auditoría y Logs locales
└── managers.py        # Lógica de filtrado para reportes de salud

```

## 3. Protocolo de Comunicación con La Central

La app opera bajo dos modos de flujo de datos:

* **Modo PUSH (Métricas de Negocio):** Cada 5 minutos (configurable), una tarea de Celery agrupa las ventas, tickets y actividad de IA, enviándolas vía HTTPS a La Central.
* **Modo PULL (Inspección en Vivo):** La Central solicita mediante un Token seguro el estado actual de un Tenant específico o logs de error en tiempo real.

## 4. El "Middleware" de Rastreo (Tracing)

Debe generar un `X-Trace-ID` único por petición. Este ID se inyecta en los headers y permite que, si algo falla, puedas buscar en La Central exactamente qué pasó en toda la cadena de ejecución.

```python
# telemetry/middleware.py (Lógica simplificada para la IA)
import uuid

class TelemetryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        trace_id = request.headers.get('X-Trace-ID', str(uuid.uuid4()))
        # Inyectar en el hilo de ejecución para que Structlog lo capture
        response = self.get_response(request)
        response['X-Trace-ID'] = trace_id
        return response

```

## 5. Dominios de Datos (Métricas Críticas)

La IA debe configurar la recolección de los siguientes puntos de datos:

1. **Ventas/Órdenes:** Montos totales y volumen transaccional.
2. **Soporte:** Tiempo de respuesta de la IA y ratio de tickets abiertos.
3. **Salud Técnica:** Latencia de base de datos, uso de memoria y errores 500.

## 6. Lógica de Resiliencia (Fail-Soft)

Si La Central no está disponible (error de red o mantenimiento), la app **no debe detener el SaaS**.

* **Buffer de Emergencia:** Las métricas se guardan en una tabla local de PostgreSQL llamada `PendingMetrics`.
* **Retry Logic:** Celery reintenta el envío con un *exponential backoff* (espera progresiva).

## 7. Instrucción de Codificación para la IA (System Prompt)

Cuando decidas programar esta app, utiliza este prompt:

> "Genera el código para la App **Api / Telemetry** de una Factory SaaS.
> 1. Crea un `Middleware` que genere y propague un **X-Trace-ID** en cada request.
> 2. Implementa **Django Rest Framework (DRF)** para crear endpoints que permitan a un sistema externo (La Central) consultar métricas de salud y ventas.
> 3. Usa **Celery** para programar tareas de 'Push' que envíen datos agregados de negocio a una URL externa.
> 4. Configura un sistema de **Auditoría Inmutable** en `models.py` para registrar cambios sensibles (login, pagos, cambios de plan).
> 5. Asegúrate de que todas las llamadas externas estén envueltas en bloques `try/except` para no bloquear el flujo principal del SaaS si La Central falla."
> 
> 

---

### Verificación de Autonomía

La App Telemetry debe poder activarse y desactivarse sin afectar el despliegue. Si no está presente, los `Services` de las otras apps simplemente detectarán que el servicio de telemetría es `None` y continuarán su proceso normal.

---

## Independencia y Contexto de Ecosistema

### Scope / No Scope
- **Scope:** Trazabilidad, métricas operativas y comerciales, push asíncrono a La Central (Celery), API de inspección pull (DRF), registro de auditoría inmutable.
- **No Scope:** Lógica comercial, checkout, descuentos, autenticación de usuarios.

### Interacciones con otras apps
- **Provee a:** La Central (sistema externo) — envía métricas de todas las apps.
- **Consume de (soft-dependency):** recibe eventos de Apps 3-9. Si Telemetry no está, cada app guarda logs locales y continúa funcionando.
- **Fallback si Telemetry no está:** métricas almacenadas en tabla `PendingMetrics` local; retry con exponential backoff cuando La Central vuelva.

### Entidades de negocio propias
| Entidad | Descripción |
|---|---|
| TelemetryEvent | Evento operativo/comercial de observabilidad (inmutable) |
| PendingMetrics | Buffer local de métricas cuando La Central no está disponible |

### Riesgos conceptuales aplicables
| ID | Riesgo | Mitigación |
|---|---|---|
| R-02 | La Central no disponible → pérdida de métricas | `PendingMetrics` + Celery retry con exponential backoff |
| R-04 | Inconsistencia de eventos entre apps | `X-Trace-ID` propagado en cada request via `TelemetryMiddleware` |
