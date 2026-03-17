Este es el **Documento Maestro 4: App Product Orchestrator (El Puente al Product Core)**. En la jerarquía de la Factory, esta aplicación es el "Traductor", encargado de convertir las funciones técnicas del core en productos que se pueden vender y gestionar.

---

# Documento Maestro 4: App Product Orchestrator (Orquestación Funcional)

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

## 1. Identidad de la Aplicación

* **Nivel de Profundidad:** 4 (Capa de Adaptación).
* **Rol:** Define qué funciones del **Product Core** están disponibles, bajo qué límites (cuotas) y para qué Tenants.
* **Dependencias Suaves:** App 3 (Profiles) para saber quién pide el acceso; App 7 (Payment) para saber si pagó.

## 2. Estructura de Archivos (Arquitectura de Carpetas)

```text
orchestrator/
├── models.py          # Product, Vertical, Bundle y Entitlement
├── services.py        # Lógica de aprovisionamiento y validación de derechos
├── selectors.py       # Consultas de catálogo y límites de uso
├── adapters/          # Lógica específica para hablar con el Product Core
│   ├── base.py        # Clase abstracta/Interface
│   └── core_app.py    # Implementación real para tu App de negocio
├── templates/
│   ├── orchestrator/
│   │   └── fallback/  # Lista básica de funciones si Theme no existe
│   └── cotton/        # Componentes de catálogo
│       ├── feature_badge.html
│       └── product_card.html

```

## 3. Conceptos Core: Products vs. Verticals

Para que la IA entienda la lógica:

* **Vertical:** Es la conexión técnica con una funcionalidad del core (ej. "Módulo de Inventario", "Agente de IA de Ventas").
* **Product:** Es la oferta comercial. Un producto puede agrupar varias *Verticals*.
* **Entitlement (Derecho):** El registro de que el `Tenant A` tiene acceso a la `Vertical B` hasta la `Fecha X`.

## 4. El Motor de Entitlements (Autorización)

Esta es la lógica que protege al Product Core. Antes de ejecutar cualquier función pesada, el sistema consulta al Orchestrator:

```python
# orchestrator/services.py (Concepto para la IA)
def can_use_feature(tenant, feature_id):
    """Verifica si el tenant tiene una suscripción activa para la función."""
    entitlement = Entitlement.objects.filter(tenant=tenant, feature__id=feature_id).first()
    if not entitlement or not entitlement.is_active():
        return False
    return True

```

## 5. Implementación UI con Cotton y Alpine.js

* **`c-feature-badge`:** Un componente que muestra si una función está "Bloqueada" o "Activa" basándose en el estado de la suscripción.
* **`x-data` para Cuotas:** Alpine.js puede manejar barras de progreso que muestran cuánto del límite mensual (ej. "5 de 10 reportes usados") ha consumido el usuario en tiempo real.

## 6. Contratos de Interfaz (Service Layer & Resiliencia)

* **`OrchestratorService.provision_tenant(tenant, product_id)`:** Prepara el entorno en el Product Core para el nuevo cliente.
* **Protocolo de Resiliencia:** * Si la **App 7 (Payment)** no está, el Orchestrator puede entrar en "Modo Demo" permitiendo acceso gratuito limitado.
* Si el **Product Core** está caído, el adaptador debe capturar el error y devolver un mensaje amigable al usuario en lugar de un error de sistema.

## 8. Especificaciones adicionales de Core

Estas especificaciones se agregan para asegurar consistencia operativa entre el `core` y `orchestrator` desde la perspectiva del concepto de producto y la facturación.

- **PlanMatrix (enforcement):** El Orchestrator aplica una `PlanMatrix` versionada que mapea `plan_id -> allowed_products[] -> allowed_verticals[]`. Ninguna app debe invocar capacidades core sin pasar por `enforce_plan_policy(tenant_id, product_id, vertical_key)` que valida la elegibilidad del tenant y emite un `TelemetryEvent` para auditoría.

- **Productos híbridos y `source_strategy`:** Un `Product` puede ser `core_only`, `local_only` o `hybrid_bundle`. En bundles híbridos, verticales `core` y `local` pueden coexistir; la prestación de las capacidades core depende del adapter y del estado del Product Core.

- **Perfil de producto local (`local_only`):** Permite definir y vender un producto aun cuando el Product Core esté ausente; el Orchestrator crea entitlements locales y gestiona autorizaciones sin invocar adaptadores externos.

- **Cambio de plan transaccional:** Cuando un tenant cambia de plan, el sistema debe ejecutar un cutover transaccional con `operation_id` idempotente, emitir eventos `plan.change.requested|completed|failed` y aplicar `deny-by-default` durante transiciones ambiguas hasta la reconciliación final.

- **Price snapshot y versionado:** El precio usado en la transacción debe guardarse como `price_snapshot` en el `order_line` para garantizar consistencia en cobros/renovaciones/reembolsos aun si el catálogo cambia después.

- **Outbox / idempotency pattern:** Operaciones críticas (webhooks de pago, provisioning, sync) deben usar `operation_id` y persistir eventos en una tabla `outbox_events` dentro de la misma transacción para publicación fiable y deduplicación por consumidores.



## 7. Instrucción de Codificación para la IA (System Prompt)

Usa este prompt para construir esta app:

> "Genera el código para la App **Product Orchestrator** de una Factory SaaS.
> 1. Crea modelos para `Product`, `Vertical` (funcionalidad técnica) y `Entitlement` (derecho de acceso).
> 2. Implementa un **Adapter Pattern** en `orchestrator/adapters/` para desacoplar el SaaS del Product Core.
> 3. Crea un servicio `authorize_feature(tenant, feature_key)` que valide si un cliente puede usar una herramienta.
> 4. Usa **Django Cotton** para crear componentes de 'Product Card' y 'Feature List'.
> 5. Implementa **Soft-Dependencies**: si 'Payment' no está instalado, permite definir productos como 'Siempre Activos' (Free tier).
> 6. El `fallback_layout.html` debe mostrar una lista simple de los servicios contratados por el tenant."
> 
> 

---

### Verificación de Autonomía

El Orchestrator puede vivir sin Marketing, Orders o Support. Su único trabajo es saber qué hay "en la estantería" y si el usuario tiene permiso para tocarlo. Es el guardián de la propiedad intelectual de tu Product Core.

---

## Independencia y Contexto de Ecosistema

### Scope / No Scope
- **Scope:** Catálogo funcional, adaptadores al Product Core externo, entitlements (derechos de acceso por tenant), configuración de Verticals y Products.
- **No Scope:** Procesamiento de pago, lógica de descuentos, gestión de sesiones de usuario.

### Interacciones con otras apps
- **Provee a:** App 6 (Orders) — existencia y precio de productos; App 9 (Home) — catálogo público; App 7 (Payment) — recibe activación de entitlements post-pago.
- **Consume de (soft-dependency):**
  - App 3 (Profiles): valida quién solicita el acceso. Fallback: bloquea la función con mensaje "no autorizado".
  - App 7 (Payment): valida si el tenant pagó. Fallback: modo Demo con acceso gratuito limitado.
  - App 2 (Telemetry): reporta aprovisionamiento. Fallback: proceso continúa sin reporte.

### Entidades de negocio propias
| Entidad | Descripción |
|---|---|
| Product | Oferta comercial visible al cliente |
| Vertical | Capacidad técnica específica del Product Core |
| Entitlement | Derecho de uso: tenant + feature + periodo activo |

### Riesgos conceptuales aplicables
| ID | Riesgo | Mitigación |
|---|---|---|
| R-01 | Acoplamiento directo con Payment o Profiles | Adapter Pattern; verificar con `apps.is_installed` antes de cualquier llamada |
| R-02 | Product Core caído sin mensaje amigable | Adaptador captura error y devuelve "Servicio temporalmente no disponible" |
| R-07 | Dependencia de un solo proveedor de core externo | Adapter Pattern con `adapters/base.py` abstracto; implementaciones intercambiables |
