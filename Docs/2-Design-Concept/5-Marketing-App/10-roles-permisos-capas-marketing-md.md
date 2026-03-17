# Documento: Roles, Permisos y Capas — App 5 Marketing

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** MD-10-RBAC
**Ubicacion:** `./Docs/2-Design-Concept/5-Marketing-App/10-roles-permisos-capas-marketing-md.md`
**Anchor Docs:** `5-marketing-app-cc.md`, `22-roles-permisos-capas-ux-fs.md`

---

## 1. Roles que interactuan con Marketing

| Rol | Relacion con la app |
|---|---|
| `anonymous` | Ve banners y promociones activas publicadas |
| `member` | Aplica cupones y ve las ofertas disponibles para su tenant |
| `admin` | Crea y gestiona campanas y cupones del tenant |
| `owner` | Igual que admin; puede archivar campanas de forma permanente |
| `staff` | Lee campanas cross-tenant; diagnostica reglas de conflicto |
| `superadmin` | Control total incluyendo campanas globales |

---

## 2. Capa Publica (anonymous)

| Pantalla / Accion | Permitido | Restriccion |
|---|---|---|
| Ver banners promocionales activos | Si | Solo banners marcados como publicos |
| Ver precios con descuento | Si | Solo precio final; sin ver la regla de calculo |
| Aplicar cupon | No | Requiere login para validar y asociar el beneficio |

---

## 3. Capa Privada por rol

| Pantalla / Accion | member | admin | owner |
|---|---|---|---|
| Ver cupones disponibles para mi cuenta | Si | Si | Si |
| Aplicar cupon en checkout | Si | Si | Si |
| Ver detalle de la regla de descuento | No | Si | Si |
| Crear campana | No | Si | Si |
| Editar campana activa | No | Si | Si |
| Pausar / finalizar campana | No | Si | Si |
| Crear cupon individual o lote | No | Si | Si |
| Desactivar cupon | No | Si | Si |
| Ver metricas de conversion de campana | No | Si | Si |
| Archivar campana de forma permanente | No | No | Si |
| Configurar banners por seccion | No | Si | Si |

---

## 4. Capa Admin Django (staff / superadmin)

| Modelo | staff (lectura) | staff (escritura) | superadmin |
|---|---|---|---|
| Campaign | Si | No | CRUD completo |
| Coupon | Si | Si (desactivar abuso) | CRUD completo |
| Banner | Si | No | CRUD completo |

Restricciones criticas:
- `staff` puede desactivar cupones abusados, pero no crear ni modificar reglas de descuento.
- Campanas globales (cross-tenant) solo son creadas por `superadmin`.

---

## 5. Assets de Marketing

| Asset | Operacion | anonymous | member | admin | owner | staff | superadmin |
|---|---|---|---|---|---|---|---|
| Imagen de banner | Ver | Si | Si | Si | Si | Si | Si |
| Imagen de banner | Cargar/borrar | No | No | Si | Si | No | Si |
| Listado de cupones usados | Exportar | No | No | Si | Si | Si | Si |
| Reporte de conversion de campana | Exportar | No | No | Si | Si | Si | Si |
| Reglas de descuento (JSON) | Ver | No | No | Si | Si | Si | Si |
| Reglas de descuento (JSON) | Editar | No | No | Si | Si | No | Si |

---

## 6. Notas de seguridad

- Las reglas de descuento no se exponen en endpoints publicos para evitar ingenieria inversa.
- Cupones de un uso se invalidan atomicamente para prevenir race conditions.
