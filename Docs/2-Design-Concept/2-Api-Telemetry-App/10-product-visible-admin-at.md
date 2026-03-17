# Documento: Producto Visible + Admin App 2 Api/Telemetry

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** AT-10-PV  
**Ubicacion:** `./Docs/2-Design-Concept/2-Api-Telemetry-App/10-product-visible-admin-at.md`  
**Anchor Docs:** `2-api-app-cc.md`, `15-protocolo-comunicacion-central-fs.md`, `21-product-visible-ux-fs.md`

## 1. Objetivo

Definir vistas operativas visibles para monitoreo y operacion, incluyendo administracion de eventos y buffers.

## 2. CRUD en Django Admin (Telemetry)

| Modelo | C | R | U | D | Notas UI Admin |
|---|---|---|---|---|---|
| TelemetryEvent | No (sistema) | Si | No | No | Solo lectura con busqueda por trace_id |
| PendingMetrics | No (sistema) | Si | Si (retry flags) | Si (purga controlada) | Accion masiva: reintentar envio |
| EndpointConfig | Si | Si | Si | Si | Validacion de URL, timeout y auth |

Criterios admin:
- Tablas con filtros por severidad, app, tenant y estado de entrega.
- Vista detalle con payload truncado y boton copiar trace id.

## 3. Interfaz de producto visible (operador)

Pantallas minimas:
- Dashboard de salud de telemetria.
- Lista de eventos fallidos y reintentos.
- Configuracion de endpoint de La Central.

Estados UX obligatorios:
- `loading`, `empty`, `error`, `success`.

## 4. Criterios de aceptacion

- Operador puede identificar fallos por app/tenant en menos de 3 clicks.
- Reintento manual de lotes disponible desde admin.
- Si La Central cae, interfaz informa degradacion sin bloquear operaciones.
