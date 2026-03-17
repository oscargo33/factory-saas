# Registro Maestro de Ultima Version de Docs

**Versión del documento:** 2026.03.16
**Última actualización:** 2026-03-16
**Total de artefactos registrados:** 184

Este registro es la referencia canónica para consultar la última versión conocida de cada artefacto dentro de `Docs/`.

## 00-knowledge-base

| Ruta | Tipo | Versión | Ultima actualización | Título / identificador |
|---|---|---|---|---|
| `Docs/00-knowledge-base/Depth Architecture-kb.md` | md | 1.0.0 | 2026-03-16 | Este es el Documento Maestro de Jerarquía y Profundidad Arquitectónica. Define el orden de precedencia y la estructura de dependencias de la Factory SaaS, organizada desde el cimiento transversal (Capa 1) hasta la superficie de consumo (Capa 9). |
| `Docs/00-knowledge-base/design-layers-kb.md` | md | 1.0.0 | 2026-03-16 | Este es el documento de referencia técnica para tu base de conocimiento. Define la jerarquía de construcción y ejecución de la plataforma, estableciendo el orden de dependencia desde el entorno de ejecución hasta la lógica de negocio final. |
| `Docs/00-knowledge-base/manual-de-estilo-de-codigo-kb.md` | md | 1.0.0 | 2026-03-16 | Manual de Estilo de Código: Factory SaaS (IA-Ready) |

## 1-Core_Concept

| Ruta | Tipo | Versión | Ultima actualización | Título / identificador |
|---|---|---|---|---|
| `Docs/1-Core_Concept/0-factory_saas-cc.md` | md | 1.0.0 | 2026-03-16 | Documento Maestro 0: El Plano de Ingeniería (Infraestructura) |
| `Docs/1-Core_Concept/1-theme-app-cc.md` | md | 1.0.0 | 2026-03-16 | Documento Maestro 1: App Theme (Motor de Diseño e i18n) |
| `Docs/1-Core_Concept/14-registro-aprobaciones-fase0-cc.md` | md | 1.0.0 | 2026-03-16 | Documento Maestro 14: Registro de Aprobaciones de Fase 0 |
| `Docs/1-Core_Concept/2-api-app-cc.md` | md | 1.0.0 | 2026-03-16 | Este es el **Documento Maestro 2: App Api / Telemetry (El Sensor de La Central)**. Como programador, este documento te servirá para instruir a la IA en la creación del "nervio óptico" que conecta tu SaaS con el dashboard global de monitoreo. |
| `Docs/1-Core_Concept/3-profile-app-cc.md` | md | 1.0.0 | 2026-03-16 | Este es el **Documento Maestro 3: App Profiles (Gestión de Identidad y Tenancy)**. Siguiendo la jerarquía, esta aplicación es la "Capa de Contexto", encargada de definir quién es el usuario y en qué entorno (Tenant) está operando. |
| `Docs/1-Core_Concept/4-product-orchestrator-app-cc.md` | md | 1.0.0 | 2026-03-16 | Este es el **Documento Maestro 4: App Product Orchestrator (El Puente al Product Core)**. En la jerarquía de la Factory, esta aplicación es el "Traductor", encargado de convertir las funciones técnicas del core en productos que se pueden vender y gestionar. |
| `Docs/1-Core_Concept/5-marketing-app-cc.md` | md | 1.0.0 | 2026-03-16 | Este es el **Documento Maestro 5: App Marketing (Estrategia y Descuentos)**. En la jerarquía de la Factory, esta aplicación es el "Optimizador de Conversión", encargado de aplicar capas de incentivos económicos sobre los productos definidos en el Orchestrator. |
| `Docs/1-Core_Concept/6-orders-app-cc.md` | md | 1.0.0 | 2026-03-16 | Este es el **Documento Maestro 6: App Orders (Gestión de Intención y Carrito)**. En el engranaje de la Factory, esta aplicación es el "Contrato", encargado de congelar la voluntad del usuario en una estructura formal que luego será cobrada por Payment. |
| `Docs/1-Core_Concept/7-payment-app-cc.md` | md | 1.0.0 | 2026-03-16 | Este es el **Documento Maestro 7: App Payment (Gestión Financiera)**. En la jerarquía de la Factory, esta aplicación es el "Cajero", responsable de transformar la validación de la orden en flujo de caja real y de asegurar que el acceso al producto esté sincronizado con el estado financiero. |
| `Docs/1-Core_Concept/8-support-app-cc.md` | md | 1.0.0 | 2026-03-16 | Este es el **Documento Maestro 8: App Support (Relación y Asistencia Agéntica)**. En el ecosistema de la Factory, esta aplicación es el "Conserje Inteligente", encargado de reducir la fricción del usuario y proteger la retención mediante una mezcla de automatización con IA y gestión humana de incidencias. |
| `Docs/1-Core_Concept/9-home-app-cc.md` | md | 1.0.0 | 2026-03-16 | Este es el **Documento Maestro 9: App Home (La Vitrina y el SEO Final)**. Cerramos el círculo de la Estructura SaaS con la "Capa de Superficie". Esta aplicación es el director de orquesta que consume el trabajo de las otras 8 para proyectar una imagen sólida, comercial y optimizada al mundo exterior. |

## 2-Design-Concept

| Ruta | Tipo | Versión | Ultima actualización | Título / identificador |
|---|---|---|---|---|
| `Docs/2-Design-Concept/0-Factory-Saas/0-index.md` | md | 2.0 | 2026-03-16 | Índice de Documentos de Diseño Global — Factory-SaaS |
| `Docs/2-Design-Concept/0-Factory-Saas/1-checklist-factory-saas.md` | md | 1.0.0 | 2026-03-16 | Documento: Checklist de Control de Implementación (Factory-SaaS) |
| `Docs/2-Design-Concept/0-Factory-Saas/10-gateway-nginx-fs.md` | md | 1.0.0 | 2026-03-16 | Documento: 10-gateway-nginx-fs.md |
| `Docs/2-Design-Concept/0-Factory-Saas/11-configuracion-redis-celery-fs.md` | md | 1.0.0 | 2026-03-16 | Documento: 11-configuracion-redis-celery-fs.md |
| `Docs/2-Design-Concept/0-Factory-Saas/12-patron-service-layer-fs.md` | md | 1.0.0 | 2026-03-16 | Documento: 12-patron-service-layer-fs.md |
| `Docs/2-Design-Concept/0-Factory-Saas/13-router-dinamico-esquemas-fs.md` | md | 1.0.0 | 2026-03-16 | Documento: 13-router-dinamico-esquemas-fs.md |
| `Docs/2-Design-Concept/0-Factory-Saas/14-pipeline-tailwind-cotton-fs.md` | md | 1.0.0 | 2026-03-16 | Documento: 14-pipeline-tailwind-cotton-fs.md |
| `Docs/2-Design-Concept/0-Factory-Saas/15-protocolo-comunicacion-central-fs.md` | md | 1.0.0 | 2026-03-16 | Documento: 15-protocolo-comunicacion-central-fs.md |
| `Docs/2-Design-Concept/0-Factory-Saas/16-contratos-inter-app-fs.md` | md | 1.0.0 | 2026-03-16 | Documento: 16-contratos-inter-app-fs.md |
| `Docs/2-Design-Concept/0-Factory-Saas/17-diccionario-datos-logico-fs.md` | md | 1.0.0 | 2026-03-16 | Documento: 17-diccionario-datos-logico-fs.md |
| `Docs/2-Design-Concept/0-Factory-Saas/18-matriz-seguridad-compliance-fs.md` | md | 1.0.0 | 2026-03-16 | Documento: 18-matriz-seguridad-compliance-fs.md |
| `Docs/2-Design-Concept/0-Factory-Saas/19-plan-matrix-fs.md` | md | 1.0.0 | 2026-03-16 | Documento: PlanMatrix Governance |
| `Docs/2-Design-Concept/0-Factory-Saas/2-Core Automation-specs-fs.md` | md | 1.0.0 | 2026-03-16 | Documento: Especificación del Motor de Automatización - fs |
| `Docs/2-Design-Concept/0-Factory-Saas/20-dod-signoff-fs.md` | md | 1.0.0 | 2026-03-16 | DoD — Sign-off Checklist (Concept Design) |
| `Docs/2-Design-Concept/0-Factory-Saas/21-product-visible-ux-fs.md` | md | 1.0.0 | 2026-03-16 | Documento: 21-product-visible-ux-fs.md |
| `Docs/2-Design-Concept/0-Factory-Saas/22-roles-permisos-capas-ux-fs.md` | md | 1.0.0 | 2026-03-16 | Documento: 22-roles-permisos-capas-ux-fs.md |
| `Docs/2-Design-Concept/0-Factory-Saas/23-estrategia-migraciones-db-fs.md` | md | 1.0 | 2026-03-16 | Documento: Estrategia de Migraciones de Base de Datos |
| `Docs/2-Design-Concept/0-Factory-Saas/24-sistema-notificaciones-fs.md` | md | 1.0 | 2026-03-16 | Documento: Sistema de Notificaciones Transaccionales |
| `Docs/2-Design-Concept/0-Factory-Saas/25-flujo-onboarding-e2e-fs.md` | md | 1.0 | 2026-03-16 | Documento: Flujo de Onboarding End-to-End |
| `Docs/2-Design-Concept/0-Factory-Saas/26-estrategia-testing-fs.md` | md | 1.0 | 2026-03-16 | Documento: Estrategia de Testing Transversal |
| `Docs/2-Design-Concept/0-Factory-Saas/27-estrategia-ambientes-fs.md` | md | 1.0 | 2026-03-16 | Documento: Estrategia de Ambientes y Staging |
| `Docs/2-Design-Concept/0-Factory-Saas/3-gestion-de-secretos-fs.md` | md | 1.0.0 | 2026-03-16 | Documento: Gestión de Secretos y Configuración - fs |
| `Docs/2-Design-Concept/0-Factory-Saas/4-estructura-de-carpetas-fs.md` | md | 1.0.0 | 2026-03-16 | Documento: Estructura de Repositorio y Carpetas Raíz - fs |
| `Docs/2-Design-Concept/0-Factory-Saas/5-configuracion-poetry-fs.md` | md | 1.0.0 | 2026-03-16 | Entendido, Maestro. Con este árbol visual, el panorama es cristalino. Has organizado la **Base de Conocimiento (Capa 00)** como el manual de vuelo, el **Core Concept (Capa 1)** como la misión y el **Design Concept (Capa 2)** como los planos de ingeniería. |
| `Docs/2-Design-Concept/0-Factory-Saas/6-dockerfile-maestro-fs.md` | md | 1.0.0 | 2026-03-16 | Entendido, Maestro. Si el `docker-compose.yml` es el manifiesto de vuelo, el **Dockerfile** es la ingeniería estructural de la nave. Un diseño pobre aquí significa una imagen pesada, lenta de compilar y vulnerable. |
| `Docs/2-Design-Concept/0-Factory-Saas/7-docker-compose-specs-fs.md` | md | 1.0.0 | 2026-03-16 | Tienes razón, Maestro. El `docker-compose.yml` es el **Manifiesto de Vuelo**. Si lo dejamos superficial, la comunicación entre las capas se vuelve inestable. Vamos a profundizar en la ingeniería de este archivo para que soporte la escala de la Factory. |
| `Docs/2-Design-Concept/0-Factory-Saas/8-entrypoint-specs-fs.md` | md | 1.0.0 | 2026-03-16 | Documento: 8-entrypoint-specs-fs.md |
| `Docs/2-Design-Concept/0-Factory-Saas/9-configuracion-postgresql-fs.md` | md | 1.0.0 | 2026-03-16 | Documento: 9-configuracion-postgresql-fs.md |
| `Docs/2-Design-Concept/0-Factory-Saas/contracts-examples/home_snapshot_example.json` | json | 1.0.0 | 2026-03-16 | home_snapshot_example.json |
| `Docs/2-Design-Concept/0-Factory-Saas/contracts-examples/home_widgets_example.json` | json | 1.0.0 | 2026-03-16 | home_widgets_example.json |
| `Docs/2-Design-Concept/0-Factory-Saas/contracts-examples/order_line_example.json` | json | 1.0.0 | 2026-03-16 | order_line_example.json |
| `Docs/2-Design-Concept/0-Factory-Saas/contracts-examples/outbox_event_example.json` | json | 1.0.0 | 2026-03-16 | outbox_event_example.json |
| `Docs/2-Design-Concept/0-Factory-Saas/contracts-examples/plan_matrix_example.json` | json | 1.0.0 | 2026-03-16 | plan_matrix_example.json |
| `Docs/2-Design-Concept/0-Factory-Saas/contracts-examples/price_snapshot_example.json` | json | 1.0.0 | 2026-03-16 | price_snapshot_example.json |
| `Docs/2-Design-Concept/0-Factory-Saas/contracts-examples/product_detail_example.json` | json | 1.0.0 | 2026-03-16 | product_detail_example.json |
| `Docs/2-Design-Concept/0-Factory-Saas/contracts-examples/profile_example.json` | json | 1.0.0 | 2026-03-16 | profile_example.json |
| `Docs/2-Design-Concept/0-Factory-Saas/contracts-examples/telemetry_event_example.json` | json | 1.0.0 | 2026-03-16 | telemetry_event_example.json |
| `Docs/2-Design-Concept/1-Theme-App/0-index.md` | md | 1.0 | 2026-03-16 | Índice de Diseño App 1 — Theme |
| `Docs/2-Design-Concept/1-Theme-App/1-checklist-theme-app.md` | md | 1.0.0 | 2026-03-16 | Checklist de Diseño — App 1 Theme |
| `Docs/2-Design-Concept/1-Theme-App/10-roles-permisos-capas-th.md` | md | 1.0.0 | 2026-03-16 | Documento: Roles, Permisos y Capas — App 1 Theme |
| `Docs/2-Design-Concept/1-Theme-App/2-modelos-theme-th.md` | md | 1.0.0 | 2026-03-16 | Documento: Modelos de Datos — App Theme |
| `Docs/2-Design-Concept/1-Theme-App/3-service-selector-contratos-theme-th.md` | md | 1.0.0 | 2026-03-16 | Documento: Service, Selector y Contratos — App Theme |
| `Docs/2-Design-Concept/1-Theme-App/4-views-endpoints-middleware-theme-th.md` | md | 1.0.0 | 2026-03-16 | Documento: Middleware, Views y Endpoints — App Theme |
| `Docs/2-Design-Concept/1-Theme-App/5-componentes-cotton-pipeline-theme-th.md` | md | 1.0.0 | 2026-03-16 | Documento: Componentes Cotton y Pipeline Visual — App Theme |
| `Docs/2-Design-Concept/1-Theme-App/6-matriz-trazabilidad-theme-th.md` | md | 1.0.0 | 2026-03-16 | Documento: Matriz de Trazabilidad - App Theme |
| `Docs/2-Design-Concept/1-Theme-App/7-nfr-seguridad-operacion-theme-th.md` | md | 1.0.0 | 2026-03-16 | Documento: NFR, Seguridad y Operación - App Theme |
| `Docs/2-Design-Concept/1-Theme-App/8-plan-validacion-diseno-theme-th.md` | md | 1.0.0 | 2026-03-16 | Documento: Plan de Validacion de Diseno - App Theme |
| `Docs/2-Design-Concept/1-Theme-App/9-product-visible-admin-th.md` | md | 1.0.0 | 2026-03-16 | Documento: Producto Visible + Admin App 1 Theme |
| `Docs/2-Design-Concept/2-Api-Telemetry-App/0-index.md` | md | 1.0 | 2026-03-16 | Indice de Diseno App 2 - Api Telemetry |
| `Docs/2-Design-Concept/2-Api-Telemetry-App/1-checklist-api-telemetry-app.md` | md | 1.0.0 | 2026-03-16 | Checklist de Diseno - App 2 Api Telemetry |
| `Docs/2-Design-Concept/2-Api-Telemetry-App/10-product-visible-admin-at.md` | md | 1.0.0 | 2026-03-16 | Documento: Producto Visible + Admin App 2 Api/Telemetry |
| `Docs/2-Design-Concept/2-Api-Telemetry-App/11-roles-permisos-capas-at.md` | md | 1.0.0 | 2026-03-16 | Documento: Roles, Permisos y Capas — App 2 Api/Telemetry |
| `Docs/2-Design-Concept/2-Api-Telemetry-App/2-modelos-telemetry-at.md` | md | 1.0.0 | 2026-03-16 | Documento: Modelos de Datos - App Api Telemetry |
| `Docs/2-Design-Concept/2-Api-Telemetry-App/3-service-selector-contratos-telemetry-at.md` | md | 1.0.0 | 2026-03-16 | Documento: Service, Selector y Contratos - App Api Telemetry |
| `Docs/2-Design-Concept/2-Api-Telemetry-App/4-endpoints-middleware-telemetry-at.md` | md | 1.0.0 | 2026-03-16 | Documento: Endpoints y Middleware - App Api Telemetry |
| `Docs/2-Design-Concept/2-Api-Telemetry-App/5-push-pull-resiliencia-telemetry-at.md` | md | 1.0.0 | 2026-03-16 | Documento: Push/Pull y Resiliencia - App Api Telemetry |
| `Docs/2-Design-Concept/2-Api-Telemetry-App/6-matriz-trazabilidad-telemetry-at.md` | md | 1.0.0 | 2026-03-16 | Documento: Matriz de Trazabilidad - App Api Telemetry |
| `Docs/2-Design-Concept/2-Api-Telemetry-App/7-nfr-seguridad-operacion-telemetry-at.md` | md | 1.0.0 | 2026-03-16 | Documento: NFR, Seguridad y Operación - App Api Telemetry |
| `Docs/2-Design-Concept/2-Api-Telemetry-App/8-plan-validacion-diseno-telemetry-at.md` | md | 1.0.0 | 2026-03-16 | Documento: Plan de Validacion de Diseno - App Api Telemetry |
| `Docs/2-Design-Concept/2-Api-Telemetry-App/9-contract-tests-skeleton-telemetry-at.md` | md | 1.0.0 | 2026-03-16 | Api Telemetry — Contract Tests Skeleton |
| `Docs/2-Design-Concept/3-Profile-App/0-index.md` | md | 1.0 | 2026-03-16 | Indice de Diseno App 3 - Profile |
| `Docs/2-Design-Concept/3-Profile-App/1-checklist-profile-app.md` | md | 1.0.0 | 2026-03-16 | Checklist de Diseno - App 3 Profile |
| `Docs/2-Design-Concept/3-Profile-App/10-product-visible-admin-profile-pr.md` | md | 1.0.0 | 2026-03-16 | Documento: Producto Visible + Admin App 3 Profile |
| `Docs/2-Design-Concept/3-Profile-App/11-roles-permisos-capas-profile-pr.md` | md | 1.0.0 | 2026-03-16 | Documento: Roles, Permisos y Capas — App 3 Profile |
| `Docs/2-Design-Concept/3-Profile-App/2-modelos-profile-pr.md` | md | 1.0.0 | 2026-03-16 | Documento: Modelos de Datos - App Profile |
| `Docs/2-Design-Concept/3-Profile-App/3-service-selector-contratos-profile-pr.md` | md | 1.0.0 | 2026-03-16 | Documento: Service, Selector y Contratos - App Profile |
| `Docs/2-Design-Concept/3-Profile-App/4-views-endpoints-middleware-profile-pr.md` | md | 1.0.0 | 2026-03-16 | Documento: Endpoints y Middleware - App Profile |
| `Docs/2-Design-Concept/3-Profile-App/5-dashboard-fallback-composition-profile-pr.md` | md | 1.0.0 | 2026-03-16 | Documento: Dashboard, Composicion y Fallback - App Profile |
| `Docs/2-Design-Concept/3-Profile-App/6-matriz-trazabilidad-profile-pr.md` | md | 1.0.0 | 2026-03-16 | Documento: Matriz de Trazabilidad - App Profile |
| `Docs/2-Design-Concept/3-Profile-App/7-nfr-seguridad-operacion-profile-pr.md` | md | 1.0.0 | 2026-03-16 | Documento: NFR, Seguridad y Operacion - App Profile |
| `Docs/2-Design-Concept/3-Profile-App/8-plan-validacion-diseno-profile-pr.md` | md | 1.0.0 | 2026-03-16 | Documento: Plan de Validacion de Diseno - App Profile |
| `Docs/2-Design-Concept/3-Profile-App/9-contract-tests-skeleton-profile-pr.md` | md | 1.0.0 | 2026-03-16 | Profile — Contract Tests Skeleton |
| `Docs/2-Design-Concept/4-Product-Orchestrator-App/0-index.md` | md | 1.0 | 2026-03-16 | Indice de Diseno App 4 - Product Orchestrator |
| `Docs/2-Design-Concept/4-Product-Orchestrator-App/1-checklist-product-orchestrator-app.md` | md | 1.0.0 | 2026-03-16 | Checklist de Diseno - App 4 Product Orchestrator |
| `Docs/2-Design-Concept/4-Product-Orchestrator-App/10-product-visible-admin-po.md` | md | 1.0.0 | 2026-03-16 | Documento: Producto Visible + Admin App 4 Product Orchestrator |
| `Docs/2-Design-Concept/4-Product-Orchestrator-App/11-roles-permisos-capas-po.md` | md | 1.0.0 | 2026-03-16 | Documento: Roles, Permisos y Capas — App 4 Product Orchestrator |
| `Docs/2-Design-Concept/4-Product-Orchestrator-App/2-modelos-product-orchestrator-po.md` | md | 1.0.0 | 2026-03-16 | Documento: Modelos de Datos - App Product Orchestrator |
| `Docs/2-Design-Concept/4-Product-Orchestrator-App/3-service-selector-contratos-product-orchestrator-po.md` | md | 1.0.0 | 2026-03-16 | Documento: Service, Selector y Contratos - App Product Orchestrator |
| `Docs/2-Design-Concept/4-Product-Orchestrator-App/4-endpoints-middleware-adapters-product-orchestrator-po.md` | md | 1.0.0 | 2026-03-16 | Documento: Endpoints, Middleware y Adapters - App Product Orchestrator |
| `Docs/2-Design-Concept/4-Product-Orchestrator-App/5-catalogo-entitlements-fallback-product-orchestrator-po.md` | md | 1.0.0 | 2026-03-16 | Documento: Catalogo, Entitlements y Fallback - App Product Orchestrator |
| `Docs/2-Design-Concept/4-Product-Orchestrator-App/6-matriz-trazabilidad-product-orchestrator-po.md` | md | 1.0.0 | 2026-03-16 | Documento: Matriz de Trazabilidad - App Product Orchestrator |
| `Docs/2-Design-Concept/4-Product-Orchestrator-App/7-nfr-seguridad-operacion-product-orchestrator-po.md` | md | 1.0.0 | 2026-03-16 | Documento: NFR, Seguridad y Operacion - App Product Orchestrator |
| `Docs/2-Design-Concept/4-Product-Orchestrator-App/8-plan-validacion-diseno-product-orchestrator-po.md` | md | 1.0.0 | 2026-03-16 | Documento: Plan de Validacion de Diseno - App Product Orchestrator |
| `Docs/2-Design-Concept/4-Product-Orchestrator-App/9-contract-tests-skeleton-product-orchestrator-po.md` | md | 1.0.0 | 2026-03-16 | Product Orchestrator — Contract Tests Skeleton |
| `Docs/2-Design-Concept/5-Marketing-App/0-index.md` | md | 1.0.0 | 2026-03-16 | Documento: App 5 — Marketing |
| `Docs/2-Design-Concept/5-Marketing-App/1-checklist-marketing-app.md` | md | 1.0.0 | 2026-03-16 | Checklist — App Marketing |
| `Docs/2-Design-Concept/5-Marketing-App/10-roles-permisos-capas-marketing-md.md` | md | 1.0.0 | 2026-03-16 | Documento: Roles, Permisos y Capas — App 5 Marketing |
| `Docs/2-Design-Concept/5-Marketing-App/2-modelos-marketing-md.md` | md | 1.0.0 | 2026-03-16 | Modelos de Datos — App Marketing |
| `Docs/2-Design-Concept/5-Marketing-App/3-service-selector-contratos-marketing-md.md` | md | 1.0.0 | 2026-03-16 | Service/Selector — Contratos Públicos (Marketing) |
| `Docs/2-Design-Concept/5-Marketing-App/4-endpoints-middleware-marketing-md.md` | md | 1.0.0 | 2026-03-16 | Endpoints, Middleware y Adapters — Marketing |
| `Docs/2-Design-Concept/5-Marketing-App/5-campaigns-fallback-marketing-md.md` | md | 1.0.0 | 2026-03-16 | Operación y Fallbacks — Campañas y Envíos |
| `Docs/2-Design-Concept/5-Marketing-App/6-matriz-trazabilidad-marketing-md.md` | md | 1.0.0 | 2026-03-16 | Matriz de Trazabilidad — Marketing |
| `Docs/2-Design-Concept/5-Marketing-App/7-nfr-seguridad-operacion-marketing-md.md` | md | 1.0.0 | 2026-03-16 | NFR, Seguridad y Operación — Marketing |
| `Docs/2-Design-Concept/5-Marketing-App/8-plan-validacion-diseno-marketing-md.md` | md | 1.0.0 | 2026-03-16 | Plan de Validación y Criterios — Marketing |
| `Docs/2-Design-Concept/5-Marketing-App/9-product-visible-admin-marketing-md.md` | md | 1.0.0 | 2026-03-16 | Documento: Producto Visible + Admin App 5 Marketing |
| `Docs/2-Design-Concept/6-Orders-App/0-index.md` | md | 1.0.0 | 2026-03-16 | Documento: App 6 — Orders |
| `Docs/2-Design-Concept/6-Orders-App/1-checklist-orders-app.md` | md | 1.0.0 | 2026-03-16 | Checklist — App Orders |
| `Docs/2-Design-Concept/6-Orders-App/10-analysis-improvements-orders-od.md` | md | 1.0.0 | 2026-03-16 | Análisis profundo y mejoras aplicadas — Orders |
| `Docs/2-Design-Concept/6-Orders-App/11-product-visible-admin-orders-od.md` | md | 1.0.0 | 2026-03-16 | Documento: Producto Visible + Admin App 6 Orders |
| `Docs/2-Design-Concept/6-Orders-App/12-roles-permisos-capas-orders-od.md` | md | 1.0.0 | 2026-03-16 | Documento: Roles, Permisos y Capas — App 6 Orders |
| `Docs/2-Design-Concept/6-Orders-App/2-modelos-orders-od.md` | md | 1.0.0 | 2026-03-16 | Modelos de Datos — App Orders |
| `Docs/2-Design-Concept/6-Orders-App/3-service-selector-contratos-orders-od.md` | md | 1.0.0 | 2026-03-16 | Service/Selector — Contratos Públicos (Orders) |
| `Docs/2-Design-Concept/6-Orders-App/4-endpoints-middleware-orders-od.md` | md | 1.0.0 | 2026-03-16 | Endpoints, Middleware y Webhooks — Orders |
| `Docs/2-Design-Concept/6-Orders-App/5-order-lifecycle-fallback-od.md` | md | 1.0.0 | 2026-03-16 | Order Lifecycle, Outbox and Fallbacks |
| `Docs/2-Design-Concept/6-Orders-App/6-matriz-trazabilidad-orders-od.md` | md | 1.0.0 | 2026-03-16 | Matriz de Trazabilidad — Orders |
| `Docs/2-Design-Concept/6-Orders-App/7-nfr-seguridad-operacion-orders-od.md` | md | 1.0.0 | 2026-03-16 | NFR, Seguridad y Operación — Orders |
| `Docs/2-Design-Concept/6-Orders-App/8-plan-validacion-diseno-orders-od.md` | md | 1.0.0 | 2026-03-16 | Plan de Validación y Criterios — Orders |
| `Docs/2-Design-Concept/6-Orders-App/9-contract-tests-skeleton-orders-od.md` | md | 1.0.0 | 2026-03-16 | Orders — Contract Tests Skeleton |
| `Docs/2-Design-Concept/7-Payment-App/0-index.md` | md | 1.0.0 | 2026-03-16 | Documento: App 7 — Payments |
| `Docs/2-Design-Concept/7-Payment-App/1-checklist-payments-app.md` | md | 1.0.0 | 2026-03-16 | Checklist — App Payments |
| `Docs/2-Design-Concept/7-Payment-App/10-analysis-improvements-payments-py.md` | md | 1.0.0 | 2026-03-16 | Análisis profundo y mejoras aplicadas — Payments |
| `Docs/2-Design-Concept/7-Payment-App/11-product-visible-admin-payments-py.md` | md | 1.0.0 | 2026-03-16 | Documento: Producto Visible + Admin App 7 Payments |
| `Docs/2-Design-Concept/7-Payment-App/12-roles-permisos-capas-payments-py.md` | md | 1.0.0 | 2026-03-16 | Documento: Roles, Permisos y Capas — App 7 Payments |
| `Docs/2-Design-Concept/7-Payment-App/2-modelos-payments-py.md` | md | 1.0.0 | 2026-03-16 | Modelos de Datos — App Payments |
| `Docs/2-Design-Concept/7-Payment-App/3-service-selector-contratos-payments-py.md` | md | 1.0.0 | 2026-03-16 | Service/Selector — Contratos Públicos (Payments) |
| `Docs/2-Design-Concept/7-Payment-App/4-endpoints-webhooks-payments-py.md` | md | 1.0.0 | 2026-03-16 | Endpoints y Webhooks — Payments |
| `Docs/2-Design-Concept/7-Payment-App/5-webhooks-outbox-dunning-payments-py.md` | md | 1.0.0 | 2026-03-16 | Webhooks, Outbox, Dunning and Reconciliation — Payments |
| `Docs/2-Design-Concept/7-Payment-App/6-matriz-trazabilidad-payments-py.md` | md | 1.0.0 | 2026-03-16 | Matriz de Trazabilidad — Payments |
| `Docs/2-Design-Concept/7-Payment-App/7-nfr-seguridad-operacion-payments-py.md` | md | 1.0.0 | 2026-03-16 | NFR, Seguridad y Operación — Payments |
| `Docs/2-Design-Concept/7-Payment-App/8-plan-validacion-diseno-payments-py.md` | md | 1.0.0 | 2026-03-16 | Plan de Validación y Criterios — Payments |
| `Docs/2-Design-Concept/7-Payment-App/9-contract-tests-skeleton-payments-py.md` | md | 1.0.0 | 2026-03-16 | Payments — Contract Tests Skeleton |
| `Docs/2-Design-Concept/8-Support-App/0-index-support-sp.md` | md | 1.0.0 | 2026-03-16 | Support App — Design Package (0..8) |
| `Docs/2-Design-Concept/8-Support-App/0-index.md` | md | 1.0.0 | 2026-03-16 | Documento: App 8 — Support |
| `Docs/2-Design-Concept/8-Support-App/1-checklist-support-app.md` | md | 1.0.0 | 2026-03-16 | Checklist — App Support |
| `Docs/2-Design-Concept/8-Support-App/11-product-visible-admin-support-sp.md` | md | 1.0.0 | 2026-03-16 | Documento: Producto Visible + Admin App 8 Support |
| `Docs/2-Design-Concept/8-Support-App/12-roles-permisos-capas-support-sp.md` | md | 1.0.0 | 2026-03-16 | Documento: Roles, Permisos y Capas — App 8 Support |
| `Docs/2-Design-Concept/8-Support-App/2-modelos-support-sp.md` | md | 1.0.0 | 2026-03-16 | Modelos de Datos — App Support |
| `Docs/2-Design-Concept/8-Support-App/3-contratos-support-sp.md` | md | 1.0.0 | 2026-03-16 | Contratos — App Support |
| `Docs/2-Design-Concept/8-Support-App/3-service-selector-contratos-support-sp.md` | md | 1.0.0 | 2026-03-16 | Service / Selector & Contratos — App Support |
| `Docs/2-Design-Concept/8-Support-App/4-endpoints-support-sp.md` | md | 1.0.0 | 2026-03-16 | Endpoints — App Support |
| `Docs/2-Design-Concept/8-Support-App/5-fallback-trazabilidad-support-sp.md` | md | 1.0.0 | 2026-03-16 | Fallbacks y Trazabilidad — Support App |
| `Docs/2-Design-Concept/8-Support-App/5-ops-support-sp.md` | md | 1.0.0 | 2026-03-16 | Operaciones & Runbook — App Support |
| `Docs/2-Design-Concept/8-Support-App/6-runbook-support-sp.md` | md | 1.0.0 | 2026-03-16 | Runbook — Support App (operaciones) |
| `Docs/2-Design-Concept/8-Support-App/6-trazabilidad-support-sp.md` | md | 1.0.0 | 2026-03-16 | Trazabilidad — App Support |
| `Docs/2-Design-Concept/8-Support-App/7-nfr-support-sp.md` | md | 1.0.0 | 2026-03-16 | NFR — App Support |
| `Docs/2-Design-Concept/8-Support-App/8-validacion-support-sp.md` | md | 1.0.0 | 2026-03-16 | Validación — App Support |
| `Docs/2-Design-Concept/8-Support-App/9-checklist-complete-support-sp.md` | md | 1.0.0 | 2026-03-16 | Checklist de Entrega — Support App (paquete 0..8) |
| `Docs/2-Design-Concept/8-Support-App/9-contract-tests-skeleton-support-sp.md` | md | 1.0.0 | 2026-03-16 | Support — Contract Tests Skeleton |
| `Docs/2-Design-Concept/9-Home-App/0-index-home-hm.md` | md | 1.0.0 | 2026-03-16 | Home App — Design Package (0..8) |
| `Docs/2-Design-Concept/9-Home-App/1-checklist-home-hm.md` | md | 1.0.0 | 2026-03-16 | Checklist — Home App |
| `Docs/2-Design-Concept/9-Home-App/10-product-visible-admin-home-hm.md` | md | 1.0.0 | 2026-03-16 | Documento: Producto Visible + Admin App 9 Home |
| `Docs/2-Design-Concept/9-Home-App/11-roles-permisos-capas-home-hm.md` | md | 1.0.0 | 2026-03-16 | Documento: Roles, Permisos y Capas — App 9 Home |
| `Docs/2-Design-Concept/9-Home-App/2-modelos-home-hm.md` | md | 1.0.0 | 2026-03-16 | Modelos de Datos — Home App |
| `Docs/2-Design-Concept/9-Home-App/3-service-selector-contratos-home-hm.md` | md | 1.0.0 | 2026-03-16 | Contratos — Home App |
| `Docs/2-Design-Concept/9-Home-App/4-endpoints-home-hm.md` | md | 1.0.0 | 2026-03-16 | Endpoints — Home App |
| `Docs/2-Design-Concept/9-Home-App/5-ops-home-hm.md` | md | 1.0.0 | 2026-03-16 | Operaciones & Runbook — Home App |
| `Docs/2-Design-Concept/9-Home-App/6-trazabilidad-home-hm.md` | md | 1.0.0 | 2026-03-16 | Trazabilidad — Home App |
| `Docs/2-Design-Concept/9-Home-App/7-nfr-home-hm.md` | md | 1.0.0 | 2026-03-16 | NFR — Home App |
| `Docs/2-Design-Concept/9-Home-App/8-validacion-home-hm.md` | md | 1.0.0 | 2026-03-16 | Validación — Home App |
| `Docs/2-Design-Concept/9-Home-App/9-contract-tests-skeleton-home-hm.md` | md | 1.0.0 | 2026-03-16 | Contract-tests Skeleton — Home App |

## Agile

| Ruta | Tipo | Versión | Ultima actualización | Título / identificador |
|---|---|---|---|---|
| `Docs/Agile/backlog/EPI-000-infra/US-000-01-docker-dev-environment.md` | md | 1.0.0 | 2026-03-16 | US-000-01 — Docker Dev Environment Reproducible |
| `Docs/Agile/backlog/EPI-000-infra/US-000-02-postgresql-schema-router.md` | md | 1.0.0 | 2026-03-16 | US-000-02 — PostgreSQL Multi-Tenant + Schema Router |
| `Docs/Agile/backlog/EPI-000-infra/US-000-03-ci-pipeline.md` | md | 1.0.0 | 2026-03-16 | US-000-03 — CI Pipeline (pytest + linting) |
| `Docs/Agile/backlog/EPI-000-infra/US-000-04-redis-celery-baseline.md` | md | 1.0.0 | 2026-03-16 | US-000-04 — Redis + Celery Worker Baseline |
| `Docs/Agile/backlog/EPI-000-infra/epic.md` | md | 1.0.0 | 2026-03-16 | EPI-000 — Infraestructura Base: El Suelo Sobre el Que Todo se Construye |
| `Docs/Agile/backlog/EPI-001-theme/US-001-01-themeconfig-model.md` | md | 1.0.0 | 2026-03-16 | US-001-01 — ThemeConfig Model + Migración |
| `Docs/Agile/backlog/EPI-001-theme/epic.md` | md | 1.0.0 | 2026-03-16 | EPI-001 — Theme: El Motor de Identidad Visual e Idioma del SaaS |
| `Docs/Agile/backlog/EPI-002-api/epic.md` | md | 1.0.0 | 2026-03-16 | EPI-002 — API / Telemetry: El Sistema Nervioso y el Ojo de La Central |
| `Docs/Agile/backlog/EPI-003-profile/epic.md` | md | 1.0.0 | 2026-03-16 | EPI-003 — Profiles: El Corazón de la Identidad y la Membresía |
| `Docs/Agile/backlog/EPI-004-orchestrator/epic.md` | md | 1.0.0 | 2026-03-16 | EPI-004 — Product Orchestrator: El Guardián del Catálogo y los Derechos |
| `Docs/Agile/backlog/EPI-005-marketing/epic.md` | md | 1.0.0 | 2026-03-16 | EPI-005 — Marketing: El Motor de Conversión y Descuentos |
| `Docs/Agile/backlog/EPI-006-orders/epic.md` | md | 1.0.0 | 2026-03-16 | EPI-006 — Orders: El Contrato Sagrado Entre Intención y Cobro |
| `Docs/Agile/backlog/EPI-007-payments/epic.md` | md | 1.0.0 | 2026-03-16 | EPI-007 — Payments: El Cajero Seguro del SaaS |
| `Docs/Agile/backlog/EPI-008-support/epic.md` | md | 1.0.0 | 2026-03-16 | EPI-008 — Support: El Conserje Inteligente y el Guardián de la Retención |
| `Docs/Agile/backlog/EPI-009-home/epic.md` | md | 1.0.0 | 2026-03-16 | EPI-009 — Home: La Vitrina del SaaS y el Motor SEO |
| `Docs/Agile/backlog/EPI-CORE-factory/EPI-CORE-factory-saas.md` | md | 1.0.0 | 2026-03-16 | EPI-CORE — Factory SaaS: Fundamentos, Arquitectura Global y Contratos del Sistema |
| `Docs/Agile/backlog/product-backlog.md` | md | 1.0.0 | 2026-03-16 | Product Backlog — Factory SaaS |
| `Docs/Agile/sprints/sprint-00/sprint-backlog.md` | md | 1.0.0 | 2026-03-16 | Sprint-0 — Backlog |

## README.md

| Ruta | Tipo | Versión | Ultima actualización | Título / identificador |
|---|---|---|---|---|
| `Docs/README.md` | md | 2026.03.16 | 2026-03-16 | Docs — Factory SaaS |

## REGISTRO-ULTIMA-VERSION.md

| Ruta | Tipo | Versión | Ultima actualización | Título / identificador |
|---|---|---|---|---|
| `Docs/REGISTRO-ULTIMA-VERSION.md` | md | 2026.03.16 | 2026-03-16 | Registro Maestro de Ultima Version de Docs |
