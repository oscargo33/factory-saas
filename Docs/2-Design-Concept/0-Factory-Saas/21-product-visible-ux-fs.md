# Documento: 21-product-visible-ux-fs.md

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** DC-21-FS  
**Ubicacion:** `./Docs/2-Design-Concept/0-Factory-Saas/21-product-visible-ux-fs.md`  
**Referencia Core:** `0-factory_saas-cc.md`, `14-pipeline-tailwind-cotton-fs.md`, `16-contratos-inter-app-fs.md`  
**Capa:** Fase 1B - Producto Visible (UX/UI + Flujos + APIs publicas)  
**Apellido:** **-fs**

---

## 1. Proposito

Definir lo que ve y usa el usuario final (cliente, operador y admin) antes de implementar codigo de Fase 2.

Este documento cierra el gap entre diseno tecnico (backend/infra) y experiencia visible del producto.

---

## 2. Entregables obligatorios por app (Fase 1B)

Cada app debe publicar, como minimo:

- Mapa de pantallas (lista de vistas por rol).
- Flujo UX principal y alterno (happy path + errores).
- Contrato de interfaz publica (inputs/outputs visibles para frontend).
- Reglas de validacion y mensajes de error para usuario.
- Estados visuales: `loading`, `empty`, `error`, `success`.
- Criterios de aceptacion UX verificables.

Adicional obligatorio de trazabilidad:
- Un archivo dedicado por app con el patron `producto-visible-admin-*` donde se documenten:
	- CRUD de modelos en Django Admin (por modelo, con limites de operacion).
	- Pantallas y flujos visibles de la app para usuario final u operador.

---

## 3. Matriz de producto visible por app

| App | Pantallas minimas | Flujo principal | Rol primario |
|---|---|---|---|
| Theme | Tokens, selector de tema, preview componentes | Configurar tokens -> previsualizar -> publicar | Admin tenant |
| Api/Telemetry | Panel de salud y trazas (lectura) | Ver estado de eventos y errores | Operador |
| Profiles | Login, registro, perfil, cambio de tenant | Login -> seleccionar tenant -> dashboard | Usuario final |
| Product Orchestrator | Catalogo de capacidades, detalle de producto | Explorar catalogo -> ver compatibilidad | Operador/Cliente |
| Marketing | Cupones, campañas, banners | Crear promo -> activar -> medir conversion | Marketing admin |
| Orders | Carrito, checkout previo, historial de ordenes | Agregar al carrito -> confirmar orden | Cliente |
| Payment | Checkout final, estado de pago, recibos | Pagar -> confirmar webhook -> mostrar recibo | Cliente |
| Support | Crear ticket, historial, detalle ticket | Crear ticket -> seguimiento -> cierre | Cliente/Soporte |
| Home | Landing, pricing, features, CTA | Navegar landing -> CTA -> signup/login | Publico |

---

## 4. Fase 1B especifica: Django Admin con look and feel

El `Django Admin` forma parte del producto visible para equipos internos y debe diseñarse en Fase 1B.

### 4.1 Alcance minimo

- Branding visual consistente con Theme (logo, colores, tipografia).
- Variables CSS de tenant aplicadas al admin donde sea seguro.
- Modo claro/oscuro definido por token (si aplica).
- Layout legible para tablas largas (orders, payments, tickets).
- Mensajeria de validacion y estados de acciones masivos.

### 4.2 Criterios de aceptacion

- Existe guia de estilo de admin y mapa de pantallas admin por app.
- Admin refleja identidad visual del producto sin romper usabilidad.
- Formularios admin criticos incluyen ayuda contextual y validaciones claras.
- Hay fallback visual si Theme no esta disponible.

---

## 5. DoR y DoD para historias de producto visible

### Definition of Ready (UX)

Un item UX entra a sprint si:

- Tiene pantalla objetivo y rol definido.
- Tiene flujo principal y flujo de error.
- Tiene criterio verificable de aceptacion visual/funcional.
- Tiene Anchor Doc dentro de `Docs/2-Design-Concept/{App}/`.

### Definition of Done (UX)

Un item UX esta `Done` si:

- Se valida contra mock/wireframe acordado.
- Cubre estados `loading`, `empty`, `error`, `success`.
- Incluye evidencia en Sprint Review (capturas o demo).
- Se actualiza backlog y sprint backlog.

---

## 6. Salida de Fase 1B

Fase 1B se considera cerrada cuando:

- Cada app tiene su especificacion de producto visible publicada.
- Django Admin tiene guideline de look and feel aprobada.
- Product Backlog contiene roadmap completo de Fase 2 basado en estas especificaciones.
- Sprint Planning de implementacion inicia con historias UX + tecnicas trazables.
