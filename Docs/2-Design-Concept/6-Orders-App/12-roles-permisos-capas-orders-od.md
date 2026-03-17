# Documento: Roles, Permisos y Capas — App 6 Orders

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** OD-12-RBAC
**Ubicacion:** `./Docs/2-Design-Concept/6-Orders-App/12-roles-permisos-capas-orders-od.md`
**Anchor Docs:** `6-orders-app-cc.md`, `22-roles-permisos-capas-ux-fs.md`

---

## 1. Roles que interactuan con Orders

| Rol | Relacion con la app |
|---|---|
| `anonymous` | Sin acceso; las ordenes requieren identidad |
| `member` | Crea y gestiona sus propias ordenes |
| `admin` | Ve y gestiona todas las ordenes del tenant |
| `owner` | Igual que admin; puede cancelar con reembolso iniciado |
| `staff` | Lee ordenes cross-tenant; asiste en resoluciones |
| `superadmin` | Acceso total; puede modificar estados de emergencia |

---

## 2. Capa Publica (anonymous)

| Pantalla / Accion | Permitido | Restriccion |
|---|---|---|
| Ver resumen de orden publica | No | Las ordenes son privadas por diseno |
| Iniciar o ver carrito | No | El carrito requiere sesion activa |

---

## 3. Capa Privada por rol

| Pantalla / Accion | member | admin | owner |
|---|---|---|---|
| Ver propio carrito | Si | Si | Si |
| Agregar/quitar items del carrito | Si | Si | Si |
| Ver resumen de orden propia | Si | Si | Si |
| Ver historial de ordenes propias | Si | Si | Si |
| Ver todas las ordenes del tenant | No | Si | Si |
| Cancelar orden propia (si estado permitido) | Si | Si | Si |
| Cancelar orden de otro miembro | No | Si | Si |
| Ver detalle de snapshot de precio | Si (propio) | Si | Si |
| Exportar historial de ordenes | No | Si | Si |
| Iniciar reembolso | No | Si (notifica a Payment) | Si |

---

## 4. Capa Admin Django (staff / superadmin)

| Modelo | staff (lectura) | staff (escritura) | superadmin |
|---|---|---|---|
| Cart | Si | Si (limpieza controlada) | CRUD completo |
| Order | Si | Si (transiciones de estado con motivo) | CRUD completo |
| OrderItem | Si | Si (ajuste con auditoria) | CRUD completo |
| PriceSnapshot | Si | No (inmutable) | Solo lectura |

Restricciones criticas:
- `PriceSnapshot` es completamente inmutable; no se puede modificar ni borrar.
- Transiciones de estado de `Order` por `staff` requieren campo `motivo` y crean audit log.

---

## 5. Assets de Orders

| Asset | Operacion | member | admin | owner | staff | superadmin |
|---|---|---|---|---|---|---|
| Snapshot de orden (PDF/HTML) | Ver | Si (propio) | Si | Si | Si | Si |
| Snapshot de orden (PDF/HTML) | Generar de nuevo | No | Si | Si | Si | Si |
| Export CSV de ordenes | Exportar | No | Si (tenant) | Si | Si (cross-tenant) | Si |
| Adjunto de orden (si aplica) | Ver | Si (propio) | Si | Si | Si | Si |
| Adjunto de orden (si aplica) | Cargar | Si | Si | Si | No | Si |
| Adjunto de orden (si aplica) | Borrar | No | Si | Si | No | Si |

---

## 6. Notas de seguridad

- El `PriceSnapshot` guarda el precio exacto al momento de la orden; garantiza trazabilidad fiscal.
- Ordenes en estado `completed` no son modificables; solo cancelables con proceso de reembolso.
