Este es el **Documento Maestro 5: App Marketing (Estrategia y Descuentos)**. En la jerarquía de la Factory, esta aplicación es el "Optimizador de Conversión", encargado de aplicar capas de incentivos económicos sobre los productos definidos en el Orchestrator.

---

# Documento Maestro 5: App Marketing (Estrategia de Captación)

## 1. Identidad de la Aplicación

* **Nivel de Profundidad:** 5 (Capa de Estrategia).
* **Rol:** Motor de reglas para descuentos, gestión de cupones y banners promocionales.
* **Dependencias Suaves:** App 4 (Orchestrator) para conocer los precios base; App 2 (Telemetry) para reportar conversión.

## 2. Estructura de Archivos (Arquitectura de Carpetas)

```text
marketing/
├── models.py          # DiscountRule, Coupon, Campaign
├── services.py        # Lógica de cálculo de descuentos y validación de cupones
├── selectors.py       # Consultas de ofertas activas para la Home
├── templates/
│   ├── marketing/
│   │   └── fallback/  # Mensajes básicos de "Sin ofertas"
│   └── cotton/        # Componentes de urgencia y promoción
│       ├── promo_banner.html
│       ├── coupon_input.html
│       └── countdown_timer.html

```

## 3. Modelo de Datos: Reglas y Cupones

Para que la IA genere un motor flexible:

* **`DiscountRule`:** Define una rebaja automática (ej. "10% de descuento en Navidad").
* **`Coupon`:** Código alfanumérico que el usuario ingresa manualmente. Incluye límites de uso y expiración.
* **`Campaign`:** Agrupador de reglas y cupones bajo un concepto de marketing (ej. "Black Friday 2026").

## 4. Lógica de Cálculo (Price Resolver)

El servicio de Marketing es consultivo. No modifica el producto, solo "sugiere" un precio mejorado.

```python
# marketing/services.py (Concepto para la IA)
def apply_marketing_to_product(product, user, coupon_code=None):
    """Calcula el mejor precio posible aplicando reglas y cupones."""
    base_price = product.price
    discount = 0
    
    # 1. Buscar reglas automáticas vigentes
    # 2. Validar cupón si existe
    # 3. Retornar el precio final y el ahorro
    return final_price, savings_data

```

## 5. Implementación UI con Cotton y Alpine.js

* **`c-coupon-input`:** Un componente que usa Alpine.js para hacer una petición `fetch` asíncrona al servidor, validando el cupón sin refrescar la página.
* **`c-countdown-timer`:** Un componente reactivo que muestra el tiempo restante de una campaña, aumentando el sentido de urgencia (FOMO).

## 6. Contratos de Interfaz (Service Layer & Resiliencia)

* **`MarketingService.get_active_promos()`:** Retorna los banners que deben aparecer en la App `Home`.
* **Protocolo de Resiliencia:** * Si la **App 4 (Orchestrator)** no está, Marketing no tiene sobre qué aplicar descuentos y devuelve una lista vacía.
* Si la **App 6 (Orders)** llama a Marketing y esta falla, Orders asume **Descuento = 0**.
* El `fallback_layout.html` simplemente no muestra banners promocionales si la App Theme está ausente.



## 7. Instrucción de Codificación para la IA (System Prompt)

Usa este prompt para construir esta app:

> "Genera el código para la App **Marketing** de una Factory SaaS.
> 1. Crea modelos para `DiscountRule` (porcentajes/montos fijos) y `Coupon` (con límites de uso).
> 2. Implementa un servicio en `services.py` que calcule el precio final de un producto basándose en las ofertas activas.
> 3. Usa **Django Cotton** para crear un componente de 'Promo Banner' y un 'Coupon Input'.
> 4. El componente de cupón debe usar **Alpine.js** para validar el código contra una API interna de forma asíncrona.
> 5. Implementa **Soft-Dependencies**: si 'Telemetry' está instalado, reporta cada vez que un cupón es validado exitosamente.
> 6. El código debe ser capaz de manejar múltiples descuentos concurrentes (elegir el mejor para el cliente)."
> 
> 

---

### Verificación de Autonomía

La App Marketing es un "satélite". Si la borras, el SaaS sigue vendiendo (a precio completo). Si la instalas, el SaaS se vuelve comercialmente agresivo. Esta independencia permite probar diferentes estrategias de venta sin tocar el núcleo de facturación.

**¿Procedemos con el Documento Maestro 6: App Orders (Gestión de Carritos e Intención)?**