# Documento: Roles, Permisos y Capas — App 2 Api/Telemetry

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** AT-11-RBAC
**Ubicacion:** `./Docs/2-Design-Concept/2-Api-Telemetry-App/11-roles-permisos-capas-at.md`
**Anchor Docs:** `2-api-app-cc.md`, `22-roles-permisos-capas-ux-fs.md`

---

## 1. Roles que interactuan con Api/Telemetry

| Rol | Relacion con la app |
|---|---|
| `anonymous` | Sin acceso (todos los endpoints requieren autenticacion) |
| `member` | Puede leer sus propias metricas de uso (si aplica) |
| `admin` | Lee datos de telemetria del tenant |
| `owner` | Igual que admin |
| `staff` | Acceso cross-tenant de lectura y gestion de endpoints |
| `superadmin` | Acceso total; gestion de La Central |

---

## 2. Capa Publica (anonymous)

| Pantalla / Recurso | Permitido | Restriccion |
|---|---|---|
| Cualquier endpoint de telemetria | Prohibido | Requiere token API o sesion |
| Panel de operacion | Prohibido | Solo staff/superadmin |

---

## 3. Capa Privada (member / admin / owner)

| Pantalla / Accion | member | admin | owner |
|---|---|---|---|
| Ver metricas de uso propio (si habilitado) | Si | Si | Si |
| Ver panel de salud general del tenant | No | Si | Si |
| Ver log de errores del tenant | No | Si | Si |
| Exportar metricas del tenant | No | Si | Si |
| Configurar destino de La Central | No | No | Si |

---

## 4. Capa Admin Django (staff / superadmin)

| Modelo | staff (lectura) | staff (escritura) | superadmin |
|---|---|---|---|
| TelemetryEvent | Si | No | Lectura + purga controlada |
| PendingMetrics | Si | Si (retry flags) | CRUD completo |
| EndpointConfig | Si | Si | CRUD completo |
| AuditLog | Si | No | Lectura; borrado con motivo auditado |

Restricciones criticas:
- `TelemetryEvent` no se borra individualmente; solo por lotes aprobados por `superadmin`.
- `AuditLog` es inmutable para `staff`; solo lectura.

---

## 5. Assets de Telemetry

| Asset | Operacion | member | admin | owner | staff | superadmin |
|---|---|---|---|---|---|---|
| Reportes de metricas (JSON/CSV) | Exportar | No | Si (propio tenant) | Si | Si | Si |
| Logs de eventos | Leer | No | Si (propio tenant) | Si | Si (cross-tenant) | Si |
| Logs de eventos | Borrar | No | No | No | No | Si (lote + motivo) |
| Certificados JWT de La Central | Leer | No | No | No | No | Si |
| Certificados JWT de La Central | Rotar | No | No | No | No | Si |

---

## 6. Notas de seguridad

- Ningun payload de telemetria incluye PII (sin emails, nombres, IPs sin hash).
- Todos los endpoints de pull requieren Bearer token rotativo.
- El `X-Trace-ID` no expone datos de tenant en texto claro.
