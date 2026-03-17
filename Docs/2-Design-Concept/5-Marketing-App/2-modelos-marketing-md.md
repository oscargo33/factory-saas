# Modelos de Datos — App Marketing

**ID:** MA-2-MDL

Propósito: definir las entidades principales que Marketing gestiona (campañas, cupones, segmentos, plantillas) respetando aislamiento por tenant.

Entidades principales (esquema `tenant_{slug}`):

1. `Campaign`
 - `id`: UUID PK
 - `tenant_id`: UUID
 - `name`: CharField(200)
 - `slug`: SlugField(120) único por tenant
 - `status`: CharField choices `draft|scheduled|running|paused|archived`
 - `channels`: JSONB (ej. `email`, `in_app`, `push`)
 - `audience_definition`: JSONB (segment selectors)
 - `content`: JSONB (per-channel payloads or template refs)
 - `start_at`, `end_at`: DateTime
 - `created_by`, `created_at`, `updated_at`

2. `Coupon`
 - `id` UUID PK
 - `tenant_id` UUID
 - `code` CharField unique por tenant
 - `discount_type` `percentage|fixed|free_trial`
 - `value` Decimal/Int
 - `valid_from`, `valid_until`
 - `usage_limit`, `used_count`
 - `applies_to_products` JSONB (lista de `product_id`)

3. `Segment`
 - Definición lógica de audiencia (traits, events, order_history, profile attributes)

4. `EmailTemplate` / `ChannelTemplate`
 - Plantillas parametrizables que no contienen PII en el repositorio público.

5. `MarketingEvent` (tracking)
 - Registro local de eventos de interacción (`event_type`, `actor_profile_id`, `metadata`) para reenvío a Telemetry/Outbox.

Reglas:
- No dependencias hard FK hacia `orders`/`payments`/`product_orchestrator` (usar IDs lógicas).
- Respetar retención de datos y flags de consentimiento por tenant/usuario.
