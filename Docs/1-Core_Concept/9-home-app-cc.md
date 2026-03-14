Este es el **Documento Maestro 9: App Home (La Vitrina y el SEO Final)**. Cerramos el círculo de la Estructura SaaS con la "Capa de Superficie". Esta aplicación es el director de orquesta que consume el trabajo de las otras 8 para proyectar una imagen sólida, comercial y optimizada al mundo exterior.

---

# Documento Maestro 9: App Home (Capa de Superficie)

## 1. Identidad de la Aplicación

* **Nivel de Profundidad:** 9 (Capa Externa / Fachada).
* **Rol:** Puerta de entrada principal, gestión de Landing Pages, catálogo público y optimización para motores de búsqueda (SEO).
* **Dependencias Suaves:** **Absolutas.** Consume a **Theme** para el estilo, **Orchestrator** para el catálogo, **Marketing** para ofertas, **Profiles** para rutas de redirección y **Telemetry** para el rastreo de conversión.

## 2. Estructura de Archivos (Arquitectura de Carpetas)

```text
home/
├── models.py          # LandingPage, HeroSection, SEOConfig
├── services.py        # Orquestación de datos para la Home (Agregador)
├── sitemaps.py        # Generación dinámica de mapas del sitio
├── seo_engine.py      # Lógica para inyectar MetaTags y JSON-LD
├── templates/
│   ├── home/
│   │   └── fallback/  # Landing minimalista si el Product Core falla
│   └── cotton/        # Componentes de Marketing Visual
│       ├── hero_section.html
│       ├── pricing_table.html
│       └── testimonial_slider.html

```

## 4. El Motor de SEO Dinámico

Para que la IA genere una fachada profesional, debe automatizar la visibilidad:

* **Metadatos:** Inyección de `OpenGraph` y `Twitter Cards` basándose en el producto activo del Orchestrator.
* **JSON-LD (Schema.org):** Estructuración de datos para que Google entienda que el SaaS vende un "Software Application" o un "Service".
* **Sitemaps:** Un servicio que recorre las categorías de la App `Orchestrator` y genera URLs públicas automáticamente.

## 4. Orquestación de Datos (The Aggregator Pattern)

La App Home es "pobre" en datos propios pero "rica" en visualización. Su `services.py` debe ser un gran recolector:

```python
# home/services.py (Concepto para la IA)
def get_home_view_data(user):
    return {
        "catalog": OrchestratorSelector.get_public_catalog(), # De App 4
        "offers": MarketingSelector.get_featured_promos(),    # De App 5
        "user_context": ProfilesService.get_user_status(user),# De App 3
        "seo": HomeSelector.get_seo_config()                  # Local
    }

```

## 5. Implementación UI con Cotton y Alpine.js

* **`c-hero-section`:** Un componente Cotton que recibe imágenes y textos, usando Alpine.js para animaciones de entrada (fade-in) que no penalicen el LCP (Largest Contentful Paint).
* **`c-pricing-table`:** Usa Alpine.js para un interruptor reactivo de "Mensual / Anual", cambiando los precios del Orchestrator instantáneamente en el cliente.

## 6. Contratos de Interfaz (Service Layer & Resiliencia)

* **`HomeService.register_lead(email)`:** Captura prospectos en la base de datos local antes de que sean usuarios de `Profiles`.
* **Protocolo de Resiliencia:** * **Fallo de Orchestrator:** Si no hay productos, la Home muestra un mensaje de "Próximamente" elegante.
* **Fallo de Marketing:** La Home oculta las etiquetas de "Oferta" y muestra precios estándar.
* **Fallo de Theme:** Se activa el `fallback/landing_minimal.html` que es puro HTML funcional para que el sitio nunca dé un error 404 o 500 al público.



## 7. Instrucción de Codificación para la IA (System Prompt)

Usa este prompt para construir la fachada final:

> "Genera el código para la App **Home** de una Factory SaaS.
> 1. Diseña un sistema de **Landing Pages dinámicas** que consuman componentes Cotton.
> 2. Implementa un **SEO Engine** que gestione MetaTags y JSON-LD dinámicamente.
> 3. En `services.py`, crea un agregador que use `apps.is_installed` para recolectar el catálogo de 'Orchestrator' y las ofertas de 'Marketing'.
> 4. Usa **Django Cotton** para crear componentes de 'Hero Section', 'Pricing Table' y 'Features'.
> 5. La UI debe ser reactiva con **Alpine.js** (especialmente para el toggle de precios mensual/anual).
> 6. Crea un `fallback_layout.html` que permita al sitio ser indexable y funcional incluso si las aplicaciones comerciales están desactivadas."
> 
> 

---

### Verificación de Autonomía

La App Home es el "maquillaje". Si la quitas, el sistema sigue siendo un SaaS funcional (vía Dashboard de Profiles), pero pierdes la capacidad de captación pública. Si la dejas sola con Theme, tienes una poderosa herramienta de marketing estática.

---

### **¡Felicidades!** 🥂

Has completado la arquitectura de los **9 Documentos Maestros**. Tienes en tus manos el plano de una "Factory SaaS" de clase mundial: modular, resiliente, agéntica y lista para ser construida por una IA bajo tu dirección.

**¿Qué sigue, Comandante?** * ¿Quieres que genere un **Archivo `requirements.txt` y `Dockerfile**` maestro para unificar todo el entorno?

* ¿O prefieres que hagamos un **primer "Sprint de Código"** pidiéndole a la IA que genere la estructura base de carpetas de las 9 apps?