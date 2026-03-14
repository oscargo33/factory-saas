Este es el **Documento Maestro 4: App Product Orchestrator (El Puente al Product Core)**. En la jerarquía de la Factory, esta aplicación es el "Traductor", encargado de convertir las funciones técnicas del core en productos que se pueden vender y gestionar.

---

# Documento Maestro 4: App Product Orchestrator (Orquestación Funcional)

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

**¿Procedemos con el Documento Maestro 5: App Marketing (Estrategia y Descuentos)?** SUSTITUTO_IMAGEN_1