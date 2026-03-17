# Indice de Diseno App 4 - Product Orchestrator

**ID:** PO-0-INDEX
**Ubicacion:** `./Docs/2-Design-Concept/4-Product-Orchestrator-App/0-index.md`
**Anchor Docs:** `Docs/1-Core_Concept/4-product-orchestrator-app-cc.md`, `Docs/1-Core_Concept/0-factory_saas-cc.md`
**Dependencia Global:** `Docs/2-Design-Concept/0-Factory-Saas/*`
**Estado:** v1.0 - Inicio de diseno individual

---

## Objetivo

Este paquete define el diseno funcional de App Product Orchestrator como capa de adaptacion comercial entre la Factory SaaS y el Product Core externo.

Alcance obligatorio del paquete:
- Gestionar catalogo comercial (`Product`) y capacidades tecnicas (`Vertical`).
- Gestionar derechos de uso por tenant (`Entitlement`) con vigencia y estado.
- Exponer contratos de autorizacion para consumidores internos.
- Implementar adaptadores desacoplados para integracion con Product Core externo.
- Degradar de forma segura cuando Payment, Profiles o Telemetry no esten instaladas/no saludables.

---

## Documentos del paquete Product Orchestrator

| # | Documento | ID | Rol |
|---|---|---|---|
| 0 | `0-index.md` | PO-0-INDEX | Indice y trazabilidad |
| 1 | `1-checklist-product-orchestrator-app.md` | PO-1-CK | Control de avance del diseno |
| 2 | `2-modelos-product-orchestrator-po.md` | PO-2-MDL | Modelo de datos (Product, Vertical, Entitlement) |
| 3 | `3-service-selector-contratos-product-orchestrator-po.md` | PO-3-SVC | Service/Selector y contratos inter-app |
| 4 | `4-endpoints-middleware-adapters-product-orchestrator-po.md` | PO-4-API | Endpoints, middleware y estrategia de adapters |
| 5 | `5-catalogo-entitlements-fallback-product-orchestrator-po.md` | PO-5-OPS | Flujos de provision, autorizacion y fallback |
| 6 | `6-matriz-trazabilidad-product-orchestrator-po.md` | PO-6-TRA | Trazabilidad Core -> Design -> Evidencia |
| 7 | `7-nfr-seguridad-operacion-product-orchestrator-po.md` | PO-7-NFR | NFR, seguridad y operacion |
| 8 | `8-plan-validacion-diseno-product-orchestrator-po.md` | PO-8-VAL | Plan de validacion del diseno |

---

## Reglas de alineacion obligatoria

- No importar modelos de otras apps.
- Toda comunicacion inter-app se ejecuta por contratos publicos de service/selector.
- Adapter Pattern obligatorio para Product Core externo.
- Tenancy por schema y contexto tenant obligatorio en toda autorizacion.
- Sin Payment, se aplica modo demo acotado por tenant y feature.

Patron de paquete completo obligatorio por app:
- Modelo de datos.
- Service/Selector/Contratos.
- Endpoints/Middleware/Adapters segun corresponda.
- Matriz de trazabilidad.
- NFR + seguridad + operacion.
- Plan de validacion del diseno.

---

## Estado de Fase 1 por App

**App 4 Product Orchestrator:** en diseno

Cierre de esta app requiere checklist PO-1 en estado completo.
