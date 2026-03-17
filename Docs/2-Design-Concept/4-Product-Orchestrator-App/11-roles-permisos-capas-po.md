# Documento: Roles, Permisos y Capas — App 4 Product Orchestrator

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PO-11-RBAC
**Ubicacion:** `./Docs/2-Design-Concept/4-Product-Orchestrator-App/11-roles-permisos-capas-po.md`
**Anchor Docs:** `4-product-orchestrator-app-cc.md`, `22-roles-permisos-capas-ux-fs.md`

---

## 1. Roles que interactuan con Product Orchestrator

| Rol | Relacion con la app |
|---|---|
| `anonymous` | Lee catalogo publico (si el tenant tiene productos publicados) |
| `member` | Ve capacidades activas del tenant; no puede comprar directamente |
| `admin` | Configura verticales y adaptadores del tenant |
| `owner` | Igual que admin; puede publicar/despublicar productos del tenant |
| `staff` | Gestiona catalogo global y diagnostica entitlements cross-tenant |
| `superadmin` | Control total del catalogo maestro |

---

## 2. Capa Publica (anonymous)

| Pantalla / Accion | Permitido | Restriccion |
|---|---|---|
| Catalogo de productos (si publicado) | Si | Solo campos no-PII y no-internos |
| Detalle de producto | Si | Sin configuracion tecnica ni entitlements |
| Precio base de producto | Si | Sin descuentos calculados (eso es Marketing) |
| Usar cualquier capacidad del Product Core | No | Requiere entitlement activo (login + pago) |

---

## 3. Capa Privada por rol

| Pantalla / Accion | member | admin | owner |
|---|---|---|---|
| Ver capacidades activas del tenant | Si | Si | Si |
| Ver estado de entitlements del tenant | Si (propios) | Si (todos) | Si |
| Configurar adaptadores del Product Core | No | Si | Si |
| Activar/desactivar verticales del tenant | No | Si | Si |
| Ver log de uso de capacidades | Si (propio) | Si (tenant) | Si |
| Solicitar demostracion/trial | Si | Si | Si |
| Publicar producto en Home (catalogo publico) | No | No | Si |

---

## 4. Capa Admin Django (staff / superadmin)

| Modelo | staff (lectura) | staff (escritura) | superadmin |
|---|---|---|---|
| Product | Si | Si | CRUD completo |
| Vertical | Si | Si | CRUD completo |
| Entitlement | Si | Si (override con motivo) | CRUD completo |
| AdapterConfig | Si | Si | CRUD completo |

Restricciones criticas:
- Override de `Entitlement` por `staff` require campo `motivo` y genera evento de auditoria.
- `Entitlement` no se crea directamente sin orden de pago confirmada, excepto por `superadmin`.

---

## 5. Assets de Product Orchestrator

| Asset | Operacion | anonymous | member | admin | owner | staff | superadmin |
|---|---|---|---|---|---|---|---|
| Imagen/icono de producto | Ver | Si (si publicado) | Si | Si | Si | Si | Si |
| Imagen/icono de producto | Cargar | No | No | No | Si | Si | Si |
| Documentacion de vertical (tecnica) | Ver | No | Si | Si | Si | Si | Si |
| Credenciales de AdapterConfig | Ver | No | No | Si | Si | Si | Si |
| Credenciales de AdapterConfig | Editar | No | No | Si | Si | Si | Si |
| Credenciales de AdapterConfig | Exportar | No | No | No | No | No | Si |
| Reports de entitlements | Exportar | No | No | Si | Si | Si | Si |

---

## 6. Notas de seguridad

- Las credenciales de `AdapterConfig` se almacenan cifradas; nunca en logs.
- Entitlements caducados se marcan como `expired`, no se borran (auditoria).
