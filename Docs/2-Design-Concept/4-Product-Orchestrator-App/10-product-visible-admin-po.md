# Documento: Producto Visible + Admin App 4 Product Orchestrator

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PO-10-PV  
**Ubicacion:** `./Docs/2-Design-Concept/4-Product-Orchestrator-App/10-product-visible-admin-po.md`  
**Anchor Docs:** `4-product-orchestrator-app-cc.md`, `16-contratos-inter-app-fs.md`, `21-product-visible-ux-fs.md`

## 1. Objetivo

Definir interfaz visible de catalogo/entitlements y administracion del portafolio comercial.

## 2. CRUD en Django Admin (Orchestrator)

| Modelo | C | R | U | D | Notas UI Admin |
|---|---|---|---|---|---|
| Product | Si | Si | Si | Si | Campos de publicacion y versionado |
| Vertical | Si | Si | Si | Si | Asociacion con productos y compatibilidad |
| Entitlement | No (derivado de pago) | Si | Si (override controlado) | No | Auditoria obligatoria en overrides |
| AdapterConfig | Si | Si | Si | Si | Validacion de credenciales por entorno |

Criterios admin:
- Filtros por tenant, plan, vigencia y estado entitlement.
- Accion segura: revocar/acotar entitlement con motivo.

## 3. Interfaz de producto visible

Pantallas minimas:
- Catalogo de capacidades.
- Detalle de producto.
- Estado de habilitacion por tenant.

Estados UX obligatorios:
- `loading`, `empty`, `error`, `success`.

## 4. Criterios de aceptacion

- Catalogo se muestra aunque falte Marketing (sin promociones).
- Entitlement no habilita features si pago no confirmado.
- Mensajes claros cuando Product Core externo no responde.
