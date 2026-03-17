Este es el Documento Maestro de Jerarquía y Profundidad Arquitectónica. Define el orden de precedencia y la estructura de dependencias de la Factory SaaS, organizada desde el cimiento transversal (Capa 1) hasta la superficie de consumo (Capa 9).

Documento Maestro: Jerarquía de Profundidad (Estructura SaaS)
Este documento establece el orden lógico de construcción y dependencia. Una capa superior no puede operar si las capas inferiores no están inicializadas, siguiendo el principio de inversión de dependencias y desacoplamiento de dominios.

Capa I: Infraestructura de ADN (Cimientos)
1. App Theme (Transversalidad Visual y Lingüística)
Es la raíz del sistema. Provee los contratos de diseño (tokens), el pipeline de assets y el motor de glosarios (i18n). Sin esta app, el sistema carece de "lenguaje" y "estética" para comunicarse con el usuario o con otras apps.

Dependencia: Ninguna (Autónoma).

Persistencia: Assets, diccionarios JSONB y configuraciones de marca.

2. App Api / Telemetry (Observabilidad Operativa)
Actúa como el sistema nervioso central. Debe existir en la base para registrar la actividad, errores y latencias de todas las capas superiores. Permite la trazabilidad end-to-end.

Dependencia: Mínima de conectividad.

Responsabilidad: Ingesta de señales y salud del sistema.

Capa II: Infraestructura de Identidad (El Chasis)
3. App Profiles (Identidad y Tenancy)
Define al sujeto (User) y al entorno (Tenant). Gestiona la lógica de aislamiento de esquemas y la jerarquía de cuentas. Es el guardián de acceso para las capas comerciales.

Dependencia: Theme (para interfaz de usuario) y Telemetry (para auditoría).

Responsabilidad: Auth, RBAC y enrutamiento de esquemas.

4. App Product Orchestrator (Orquestación Funcional)
El adaptador universal hacia el Product Core. Transforma la funcionalidad técnica en un "producto comercializable". Define qué verticales están conectadas y bajo qué configuraciones técnicas.

Dependencia: Profiles (para contextualizar el tenant) y Theme.

Responsabilidad: Adapter Pattern, configuración de Verticales y Entitlements.

Capa III: Ciclo de Negocio (Lógica Comercial)
5. App Marketing (Estrategia de Captación)
Gestiona el motor de ofertas, cupones y campañas. Su lógica de precios y promociones debe estar definida antes de que se inicie cualquier proceso de compra.

Dependencia: Orchestrator (para saber qué productos existen).

Responsabilidad: Motor de reglas comerciales y descuentos.

6. App Orders (Gestión de Intención)
Consolida la intención de compra. Estructura la orden tomando datos del catálogo (Orchestrator) y aplicando la lógica de precios (Marketing). Es el nexo transaccional.

Dependencia: Marketing y Orchestrator.

Responsabilidad: Persistencia de carritos, órdenes y wishlists.

7. App Payment (Ejecución Financiera)
La capa de conversión monetaria. Se encarga de la comunicación con pasarelas y de la confirmación de pago para activar los derechos de uso.

Dependencia: Orders (para el monto y desglose) y Profiles (para el cliente).

Responsabilidad: Transaccionalidad, conciliación y webhooks financieros.

Capa IV: Capa de Relación y Superficie (Interacción)
8. App Support (Atención y Retención)
Sistema de gestión de incidencias y relación post-venta. Utiliza el historial de todas las capas anteriores para dar soporte al cliente.

Dependencia: Profiles, Orders y Payment.

Responsabilidad: Ticketing, mensajería y automatización agéntica.

9. App Home (Fachada Pública)
Es la capa más superficial. Funciona como un orquestador de presentación que consume datos de todas las apps inferiores para presentarlos en una vitrina comercial coherente.

Dependencia: Todas las apps anteriores.

Responsabilidad: Captación de tráfico, UX de aterrizaje y SEO dinámico.

Matriz de Dependencia Crítica

Profundidad,Aplicación,Función Crítica,Consumidor Principal
1 (Base),Theme,Assets / i18n,Todas las capas
2,Telemetry,Observabilidad,Infraestructura Central
3,Profiles,Tenancy / Auth,Orchestrator / Payment
4,Orchestrator,Conectividad Core,Orders / Home
5,Marketing,Precios / Ofertas,Orders
6,Orders,Intención,Payment
7,Payment,Cobro,Orchestrator (Entitlements)
8,Support,Retención,Profiles / Orders
9 (Superficie),Home,Conversión,Usuario Final

Este orden garantiza que el desarrollo de la Factory SaaS siga un flujo lógico donde cada módulo encuentra su soporte en la capa inmediata inferior.