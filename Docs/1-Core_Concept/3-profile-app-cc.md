Este es el **Documento Maestro 3: App Profiles (Gestión de Identidad y Tenancy)**. Siguiendo la jerarquía, esta aplicación es la "Capa de Contexto", encargada de definir quién es el usuario y en qué entorno (Tenant) está operando.

---

# Documento Maestro 3: App Profiles (Identidad y Tenancy)

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

## 1. Identidad de la Aplicación

* **Nivel de Profundidad:** 3 (Capa de Contexto).
* **Rol:** Gestor de cuentas de usuario, perfiles y el motor de multitenencia (esquemas).
* **Dependencias Suaves:** Apps 1 (Theme) y 2 (Telemetry). Consume datos (lectura) de Apps 4, 5, 6, 7 y 8 para el Dashboard.

## 2. Estructura de Archivos (Arquitectura de Carpetas)

```text
profiles/
├── models.py          # User (Global), Tenant, y Membership (Roles)
├── services.py        # Lógica de creación de cuentas, invitaciones y cambio de tenant
├── selectors.py       # Agregador de datos para el Dashboard (historial de órdenes, tickets)
├── middleware.py      # Database Router para conmutación de esquemas
├── templates/
│   ├── profiles/
│   │   └── fallback/  # Layout HTML puro si App Theme no existe
│   │       └── dashboard_basic.html
│   └── cotton/        # Componentes de perfil
│       ├── user_avatar.html
│       ├── tenant_switcher.html
│       └── profile_card.html

```

## 3. Modelo de Datos: Identidad Global vs. Datos de Tenant

Para permitir que un usuario pertenezca a varios SaaS con una sola cuenta:

* **`User` (Esquema Public):** Credenciales básicas (email, password, MFA).
* **`Tenant` (Esquema Public):** Registro de la instancia SaaS (dominio, esquema de BD).
* **`Membership` (Esquema Public):** Vincula `User` con `Tenant` y asigna un `Role` (Owner, Admin, Member).
* **`Profile` (Esquema Tenant):** Preferencias específicas del usuario dentro de esa empresa (avatar, configuración de notificaciones).

## 4. El Dashboard Agregador (Pattern: UI Composition)

El Dashboard de perfiles no es "dueño" de los datos, los solicita mediante **Soft-Dependencies**:

* Si la **App 4 (Product Orchestrator)** está instalada, invoca a `ProductSelector.get_purchased_products(user, tenant)`.
* Si la **App 5 (Marketing)** está instalada, invoca a `MarketingSelector.get_available_coupons(user, tenant)`.
* Si la **App 6 (Orders)** está instalada, invoca a `OrdersSelector.get_recent(user)`.
* Si la **App 7 (Payment)** está instalada, invoca a `PaymentSelector.get_recent_payments(user, tenant)`.
* Si la **App 8 (Support)** está instalada, invoca a `SupportSelector.get_active_tickets(user)`.
* Si la **App 1 (Theme)** está instalada y saludable, aplica tokens visuales y componentes; si no, usa fallback visual local.
* **Resiliencia:** Si alguna app falta, la sección correspondiente en el dashboard simplemente no se renderiza (devuelve una lista vacía `[]`).

## 5. Implementación UI con Cotton y Alpine.js

* **`c-tenant-switcher`:** Componente Cotton que usa Alpine.js para mostrar un dropdown reactivo con las organizaciones del usuario y permite cambiar de contexto sin recargas pesadas.
* **Fallback UI:** En `templates/profiles/fallback/`, se define un CSS básico incrustado para que el formulario de Login y el cambio de Password sean siempre funcionales, incluso si falla el CDN de Tailwind o la App Theme.

## 6. Contratos de Interfaz (Service Layer)

* **`ProfilesService.get_active_context(request)`:** Retorna el objeto `User` y el `Tenant` actual.
* **`ProfilesService.switch_tenant(user, tenant_id)`:** Valida la membresía y redirige al dominio/esquema correspondiente.
* **Protocolo de Resiliencia:** Si la App 2 (Telemetry) no está, la creación de perfil no se reporta a La Central, pero el usuario se crea exitosamente en la base de datos local.

Requerimientos operativos adicionales (core-level):

- **`get_display_name` y `profile_id` en selectors:** Los `selectors` expuestos por `profiles` deben garantizar que `get_display_name(user_id, tenant_id)` retorna además `profile_id` (UUID) y `display_name`. Esto facilita traza y correlación en Telemetry y en Outbox payloads.
- **Contexto para Telemetry:** `ProfilesService.get_active_context` debe añadir un `telemetry_identity` que incluya `user_id`, `profile_id` y `tenant_slug` para que eventos emitidos por otras apps (orders, payments, orchestrator) puedan correlacionarse con un sujeto humano identificable sin exponer PII.

## 7. Instrucción de Codificación para la IA (System Prompt)

Cuando pidas a la IA generar esta aplicación, usa este prompt:

> "Genera el código para la App **Profiles** de una Factory SaaS.
> 1. Implementa un sistema de **Multitenancy** donde los usuarios vivan en el esquema público y puedan pertenecer a múltiples Tenants (esquemas).
> 2. En `services.py`, crea la lógica para invitar usuarios y validar roles (RBAC).
> 3. El Dashboard debe ser un agregador: usa `apps.is_installed` para intentar cargar datos de 'Product Orchestrator', 'Marketing', 'Orders', 'Payment' y 'Support'. Si no están, devuelve listas vacías.
> 4. Crea componentes **Django Cotton** para el avatar y el selector de tenant, usando **Alpine.js** para la interactividad.
> 5. Provee un `fallback_layout.html` en `templates/profiles/fallback/` con HTML puro para que el login nunca falle."
> 
> 

---

### Verificación de Autonomía

La App Profiles es el "corazón operativo". Puede funcionar perfectamente solo con la App 1 y 2. Si las Apps comerciales (4-9) desaparecen, el usuario aún puede gestionar su cuenta y sus organizaciones, garantizando que el sistema nunca sea un "ladrillo" (brick).

---

## Independencia y Contexto de Ecosistema

### Scope / No Scope
- **Scope:** Identidad global de usuarios, multitenancy (esquema PostgreSQL por tenant), membresías y roles (RBAC), dashboard agregador de lectura.
- **No Scope:** Pricing, pagos, descuentos, catálogo de productos.

### Interacciones con otras apps
- **Provee a:** App 4 (Orchestrator) — contexto de quién solicita acceso; App 8 (Support) — historial del usuario; App 9 (Home) — rutas de redirección post-login.
- **Consume de (soft-dependency):**
  - App 1 (Theme): estilos y color themes. Fallback: `templates/profiles/fallback/dashboard_basic.html`.
  - App 2 (Telemetry): reporta creación de perfil. Fallback: perfil se crea igualmente, sin reporte.
  - App 4 (Product Orchestrator): productos comprados/activos para dashboard. Fallback: sección no se renderiza (`[]`).
  - App 5 (Marketing): cupones y descuentos disponibles. Fallback: sección no se renderiza (`[]`).
  - App 6 (Orders): historial de pedidos para dashboard. Fallback: sección no se renderiza (`[]`).
  - App 7 (Payment): historial de pagos realizados. Fallback: sección no se renderiza (`[]`).
  - App 8 (Support): tickets activos para dashboard. Fallback: sección no se renderiza (`[]`).

### Entidades de negocio propias
| Entidad | Descripción |
|---|---|
| User | Identidad global en esquema `public` (email, password, MFA) |
| Tenant | Organización aislada por esquema PostgreSQL |
| Membership | Relación User-Tenant con rol (Owner, Admin, Member) |
| Profile | Preferencias del usuario dentro del tenant (esquema tenant) |

### Riesgos conceptuales aplicables
| ID | Riesgo | Mitigación |
|---|---|---|
| R-01 | Otras apps importan modelos User/Tenant directamente | Solo acceso via `ProfilesService` / `ProfilesSelector` |
| R-05 | Fuga de datos entre tenants | Aislamiento por esquema PostgreSQL + middleware router de esquemas |
