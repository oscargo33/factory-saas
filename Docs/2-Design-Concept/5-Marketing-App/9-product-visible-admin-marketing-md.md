# Documento: Producto Visible + Admin App 5 Marketing

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** MD-9-PV  
**Ubicacion:** `./Docs/2-Design-Concept/5-Marketing-App/9-product-visible-admin-marketing-md.md`  
**Anchor Docs:** `5-marketing-app-cc.md`, `16-contratos-inter-app-fs.md`, `21-product-visible-ux-fs.md`

## 1. Objetivo

Definir interfaz visible para promociones y CRUD administrativo de campanas/cupones.

## 2. CRUD en Django Admin (Marketing)

| Modelo | C | R | U | D | Notas UI Admin |
|---|---|---|---|---|---|
| Campaign | Si | Si | Si | Si | Fechas, audiencia y estado |
| Coupon | Si | Si | Si | Si | Validar expiracion, limite y stack rules |
| Banner | Si | Si | Si | Si | Preview responsive y prioridad |

Criterios admin:
- Reglas de conflicto de cupones visibles antes de activar.
- Acciones masivas: activar, pausar, finalizar.

## 3. Interfaz de producto visible

Pantallas minimas:
- Gestor de campanas.
- Gestor de cupones.
- Preview de banners por canal.

Estados UX obligatorios:
- `loading`, `empty`, `error`, `success`.

## 4. Criterios de aceptacion

- Preview de promocion antes de publicar.
- Orders funciona con precio base si Marketing falla.
- Mensajes de validacion de cupon claros para usuario final.
