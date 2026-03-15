# Documento: 17-diccionario-datos-logico-fs.md

**ID:** DC-17-FS
**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/17-diccionario-datos-logico-fs.md`
**Referencia Core:** `0-factory_saas-cc.md`
**Capa:** Transversal — Diccionario de Datos Lógico
**Apellido:** **-fs**

---

## 1. Propósito

Este documento es el **glosario canónico de entidades de datos** de la Factory. Define cada entidad de negocio con sus campos, el esquema PostgreSQL donde reside, y el app propietario. Este diccionario es la referencia para el diseño de modelos Django y para la creación del `17-diccionario-datos-logico-fs.md` de implementación.

---

## 2. Convenciones

| Convención | Descripción |
|---|---|
| **Schema `public`** | Entidades del sistema: Tenant, User, Membership. Accesibles por todas las apps |
| **Schema `tenant_{slug}`** | Entidades de negocio de cada tenant. Aisladas por tenant |
| **Tipo UUID** | Todas las PKs primarias son `UUID v4` (`uuid-ossp`) |
| **`created_at` / `updated_at`** | Todos los modelos tienen timestamps UTC auto-gestionados |
| **Soft delete** | Entidades críticas usan `is_deleted` + `deleted_at` en lugar de `DELETE` físico |

---

## 3. Entidades del Esquema `public`

### 3.1. `Tenant`

**Owner App:** `core`
**Propósito:** Representa una instancia de negocio aislada (un cliente de la Factory).

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID PK | Identificador único |
| `name` | CharField(200) | Nombre del negocio |
| `slug` | SlugField(63) unique | Subdominio de acceso (`acme` → `acme.factory.com`) |
| `status` | CharField choices | `active`, `suspended`, `cancelled`, `pending` |
| `plan_id` | FK → Plan | Plan de suscripción activo |
| `created_at` | DateTimeField | Fecha de registro |
| `updated_at` | DateTimeField | Última modificación |

---

### 3.2. `User`

**Owner App:** Django `auth` (extendido por `core`)
**Propósito:** Cuenta de usuario global. Un usuario puede pertenecer a múltiples tenants vía Membership.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | AutoField (int) | PK estándar de Django auth |
| `email` | EmailField unique | Email de login (no username) |
| `username` | CharField | Username interno (puede ser igual al email) |
| `is_active` | BooleanField | Cuenta activa |
| `is_staff` | BooleanField | Acceso a Django Admin global |
| `created_at` | DateTimeField | Fecha de registro |

---

### 3.3. `Membership`

**Owner App:** `core`
**Propósito:** Relación M:N entre User y Tenant con rol asignado.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID PK | Identificador único |
| `user` | FK → User | Usuario |
| `tenant` | FK → Tenant | Tenant |
| `role` | CharField choices | `owner`, `admin`, `member`, `read_only` |
| `is_active` | BooleanField | Membresía activa |
| `joined_at` | DateTimeField | Fecha de incorporación |

---

## 4. Entidades del Esquema `tenant_{slug}`

Todas las entidades a continuación viven en el esquema del tenant y son completamente aisladas.

---

### 4.1. `Profile` (App: `profile`)

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID PK | Identificador único |
| `user_id` | int | FK conceptual a `public.users.id` (no hard FK) |
| `display_name` | CharField(150) | Nombre mostrado en UI |
| `avatar_url` | URLField | URL de avatar |
| `bio` | TextField | Descripción personal |
| `locale` | CharField(10) | Idioma preferido (ej. `es-MX`) |
| `timezone` | CharField(50) | Zona horaria (ej. `America/Mexico_City`) |

---

### 4.2. `Product` (App: `product_orchestrator`)

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID PK | Identificador único |
| `name` | CharField(200) | Nombre del producto |
| `slug` | SlugField | URL-friendly identifier |
| `description` | TextField | Descripción completa |
| `price` | DecimalField(10,2) | Precio base |
| `currency` | CharField(3) | ISO 4217 (ej. `MXN`, `USD`) |
| `is_active` | BooleanField | Visible en catálogo |
| `metadata` | JSONB | Atributos adicionales variables |

---

### 4.3. `Order` (App: `orders`)

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID PK | Identificador único |
| `user_id` | int | Referencia al usuario que ordenó |
| `status` | CharField choices | `draft`, `pending`, `paid`, `fulfilled`, `cancelled` |
| `total_amount` | DecimalField(12,2) | Total del pedido |
| `currency` | CharField(3) | Moneda del pedido |
| `metadata` | JSONB | Datos adicionales de la orden |
| `created_at` | DateTimeField | Fecha de creación |
| `updated_at` | DateTimeField | Última actualización |

### 4.4. `OrderLine` (App: `orders`)

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID PK | Identificador único |
| `order` | FK → Order | Pedido al que pertenece |
| `product_id` | UUID | ID del producto (sin FK duro entre apps) |
| `quantity` | PositiveIntegerField | Cantidad ordenada |
| `unit_price` | DecimalField(10,2) | Precio al momento de la compra |

---

### 4.5. `Subscription` (App: `payments`)

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID PK | Identificador único |
| `plan_id` | UUID | Plan contratado |
| `status` | CharField choices | `trialing`, `active`, `past_due`, `cancelled` |
| `current_period_start` | DateField | Inicio del periodo de facturación |
| `current_period_end` | DateField | Fin del periodo de facturación |
| `gateway_subscription_id` | CharField | ID en el gateway de pagos externo |

---

### 4.6. `SupportTicket` (App: `support`)

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID PK | Identificador único |
| `user_id` | int | Usuario que abrió el ticket |
| `subject` | CharField(300) | Asunto |
| `body` | TextField | Descripción del problema |
| `status` | CharField choices | `open`, `in_progress`, `resolved`, `closed` |
| `priority` | CharField choices | `low`, `medium`, `high`, `critical` |
| `assigned_to_id` | int | Agente asignado (nullable) |
| `created_at` | DateTimeField | Fecha de creación |
| `resolved_at` | DateTimeField | Fecha de resolución (nullable) |

---

### 4.7. `TelemetryEvent` (App: `core` / schema `public`)

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID PK | Identificador único |
| `event_type` | CharField(100) | Tipo de evento (ver DC-15) |
| `tenant_slug` | CharField(63) | Tenant origen (anonimizable) |
| `app_label` | CharField(50) | App que generó el evento |
| `payload` | JSONB | Datos del evento (sin PII) |
| `created_at` | DateTimeField | Timestamp UTC |
| `sent_at` | DateTimeField | Cuándo fue enviado a La Central (nullable) |

---

## 5. Diagrama de Relaciones Lógicas (Simplificado)

```
[public schema]
Tenant ──< Membership >── User

[tenant schema]
User.id ──< Profile
User.id ──< Order ──< OrderLine >── Product.id
Order.id ──< Payment (gateway)
User.id ──< SupportTicket
Tenant ──< Subscription
```

Nota: Las líneas que cruzan de `public` a `tenant` son **referencias lógicas por ID** (enteros o UUIDs), no Foreign Keys de base de datos, para mantener el aislamiento de esquema.

---

## 6. Relación con Otros Documentos

| Documento | Relación |
|---|---|
| DC-9 `9-configuracion-postgresql-fs.md` | Define la estrategia de esquemas donde estas entidades residen |
| DC-12 `12-patron-service-layer-fs.md` | Los services/selectors operan sobre estas entidades |
| DC-16 `16-contratos-inter-app-fs.md` | Los contratos retornan subconjuntos de estas entidades como DTOs |
| DC-18 `18-matriz-seguridad-compliance-fs.md` | Clasifica qué campos son PII y requieren protección especial |

---

## 7. Criterios de Aceptación del Diseño

- [ ] Todas las entidades tienen UUID como PK excepto `User` (que usa el int de Django auth).
- [ ] `Tenant`, `User`, `Membership` están en el esquema `public`.
- [ ] Las referencias entre esquemas son por ID (no FK de base de datos).
- [ ] Ninguna entidad del tenant contiene nombres, emails, u otros PII en campos no marcados como tal.
- [ ] Todas las entidades tienen `created_at` y `updated_at` gestionados automáticamente.
