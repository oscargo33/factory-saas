# Documento: Producto Visible + Admin App 8 Support

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** SP-11-PV  
**Ubicacion:** `./Docs/2-Design-Concept/8-Support-App/11-product-visible-admin-support-sp.md`  
**Anchor Docs:** `8-support-app-cc.md`, `16-contratos-inter-app-fs.md`, `21-product-visible-ux-fs.md`

## 1. Objetivo

Definir UX visible de tickets/soporte y operacion de backoffice para equipos de atencion.

## 2. CRUD en Django Admin (Support)

| Modelo | C | R | U | D | Notas UI Admin |
|---|---|---|---|---|---|
| Ticket | Si | Si | Si | No (cierre, no borrado) | Cola por prioridad y SLA |
| TicketMessage | Si | Si | Si | Si (moderacion) | Historial por conversacion |
| KnowledgeArticle | Si | Si | Si | Si | Versionado y estado publicado |
| EscalationRule | Si | Si | Si | Si | Simulador de reglas |

Criterios admin:
- Filtros por SLA, prioridad, estado y asignado.
- Acciones masivas: asignar, escalar, cerrar.

## 3. Interfaz de producto visible

Pantallas minimas:
- Crear ticket.
- Historial y detalle de ticket.
- Centro de ayuda/knowledge base.

Estados UX obligatorios:
- `loading`, `empty`, `error`, `success`.

## 4. Criterios de aceptacion

- Si IA falla, UI continua con formulario de ticket tradicional.
- Usuario puede ver trazabilidad de su ticket.
- Operador puede cumplir SLA con tablero de prioridades.
