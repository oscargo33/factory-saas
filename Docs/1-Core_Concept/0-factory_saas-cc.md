# Documento Maestro 0: El Plano de Ingeniería (Infraestructura)

**Core:** Django 5.1+ | PostgreSQL 16 (Esquemas) | Redis 7.2 | Docker Compose.
**Regla de Oro:** **Degradación Graciosa.** Si la App *X* no está, la App *Y* debe seguir funcionando con un valor neutro.

### 1. Arquitectura de Datos e Identidad

* **Esquema `public`:** Apps 1-9 y Usuarios Globales.
* **Esquemas `tenant`:** Datos operativos del **Product Core**.
* **Aislamiento:** Prohibido importar modelos entre aplicaciones. Comunicación exclusiva vía `services.py`.

### 2. Protocolo de Independencia de UI

* Cada app (3-9) debe poseer una carpeta `templates/[app]/fallback/`.
* Si la App 1 (Theme) no está instalada, la app carga su propio `fallback_layout.html` (HTML puro/minimalista).
* Los componentes visuales usan **Django Cotton** y **Alpine.js** con estados internos, no globales.

---

# Nivel 1: Capa de ADN (Cimientos)

## Documento Maestro 1: App Theme (Design System & i18n)

* **Función:** Capa de sobreescritura (Override). Provee la "belleza" y el "lenguaje".
* **Stack:** Tailwind (Tokens vía variables CSS), Django Cotton (Componentes), Alpine.js (Reactividad).
* **i18n:** Glosario en PostgreSQL (JSONB) + Caché en Redis + Fallback a **LibreTranslate** (Sidecar).
* **Resiliencia:** Si falla, las otras apps activan sus layouts de emergencia.

## Documento Maestro 2: App Api / Telemetry (El Sensor de La Central)

* **Función:** Nervio óptico. Único puente hacia **La Central** (Dashboard externo de monitoreo múltiple).
* **Data Points:** Ventas, órdenes, salud de Agentes IA, tickets y métricas de infraestructura.
* **Protocolo:** Envío asíncrono (Push vía Celery) y API de inspección (Pull vía DRF).
* **Resiliencia:** Si La Central no responde, guarda logs localmente (Fail-soft).

---

# Nivel 2: Capa de Contexto e Integración

## Documento Maestro 3: App Profiles (Identidad & Tenancy)

* **Función:** Gestión de usuarios globales y asignación de esquemas (Tenants).
* **Dashboard:** Agregador de lectura de `Orders`, `Payment` y `Support`.
* **Resiliencia:** En modo fallback (sin Theme), muestra un dashboard básico en lista HTML. No depende de Marketing ni Orchestrator para el login.

## Documento Maestro 4: App Product Orchestrator (El Adaptador)

* **Función:** Envuelve el **Product Core** (externo) y lo convierte en producto.
* **Verticals:** Mapeo técnico y configuración de instancias del core.
* **Entitlements:** Valida si el Tenant tiene derecho a usar una función según lo pagado.
* **Resiliencia:** Si el Product Core no responde, bloquea la función con un mensaje "Servicio temporalmente no disponible" sin romper el SaaS.

---

# Nivel 3: Capa Comercial (Transaccional)

## Documento Maestro 5: App Marketing (Estrategia)

* **Función:** Motor de reglas de descuento, cupones y banners promocionales.
* **Lógica:** Calcula precios dinámicos sin tocar la base de datos del Orchestrator.
* **Resiliencia:** Si falla o no está, las apps superiores asumen **Descuento = 0**.

## Documento Maestro 6: App Orders (Intención)

* **Función:** Gestor de carritos y formalización de órdenes (Snapshots).
* **Estados:** Draft -> Pending -> Processing -> Completed.
* **Resiliencia:** Si Marketing no está, procesa la orden al precio base. Usa su propio template de carrito si Theme falla.

## Documento Maestro 7: App Payment (Conversión)

* **Función:** Interfaz con pasarelas (Stripe/PayPal) y gestión de suscripciones.
* **Conciliación:** Procesamiento de Webhooks y generación de recibos.
* **Resiliencia:** Si falla la comunicación, marca el pago como "Revisión Manual". No activa Entitlements sin confirmación.

---

# Nivel 4: Capa de Relación y Superficie

## Documento Maestro 8: App Support (Asistencia e IA)

* **Función:** Soporte híbrido (Humano + Agente IA con RAG).
* **Knowledge Base:** Documentación dinámica servida por componentes Cotton.
* **Resiliencia:** Si la IA falla, el sistema degrada a un formulario de ticket tradicional.

## Documento Maestro 9: App Home (Fachada Pública)

* **Función:** Vitrina comercial y SEO. Orquestador de consumo total.
* **SEO:** Metadatos dinámicos y Sitemaps.
* **Resiliencia:** Si falta alguna app (ej. Marketing), la Home simplemente oculta los banners de oferta y muestra el catálogo estándar.

---

### Apéndice: Manual de Supervivencia para la IA (System Prompt)

Cada vez que pidas a una IA programar algo, asegúrate de que use este estándar:

1. **Lógica:** Todo en `services.py`. Prohibido importar modelos de otra app.
2. **UI:** Usa `c-components` de Cotton. Implementa `fallback_layout.html`.
3. **Dependencia:** Si necesitas la App *X*, usa `if apps.is_installed('X'):`. Si no está, devuelve un valor neutro (`0`, `False`, `[]`).

