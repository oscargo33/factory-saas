# Modelos de Datos — Home App

**ID:** HM-2-MDL

Propósito: entidades ligeras que sirven al dashboard y landing por tenant. Todas viven en esquema `tenant_{slug}` salvo cachés globales.

Entidades principales:

1. `HomeWidget`
 - `id`: UUID PK
 - `tenant_id`: UUID
 - `widget_key`: CharField(120)  # ej. `recent_orders`, `recommended_products`
 - `title`: CharField(200)
 - `settings`: JSONB  # configuración del widget (limit, filters)
 - `is_enabled`: Bool
 - `created_at`, `updated_at`

2. `HomeSnapshot` (opcional, cache de render)
 - `id`: UUID
 - `tenant_id`: UUID
 - `snapshot_key`: CharField
 - `payload`: JSONB
 - `generated_at`: DateTime
 - `ttl_seconds`: Int

3. `RecommendationFeed` (referencia a marketing/product)
 - `id`, `tenant_id`, `feed_type`, `items` JSONB, `updated_at`

Reglas y privacidad:
- No persistir PII en `HomeSnapshot.payload`; solo IDs y métricas agregadas.
- Todas las referencias a perfiles/ordenes usan IDs lógicos (no FK duro) conforme DC-17.
