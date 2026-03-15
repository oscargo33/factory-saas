# Documento Maestro 1: App Theme (Motor de Diseño e i18n)

## 1. Identidad de la Aplicación

* **Nivel de Profundidad:** 1 (Base absoluta).
* **Rol:** Proveedor de Estética (Tailwind), Componentes (Cotton), Reactividad (Alpine.js) e Idioma (i18n).
* **Dependencias:** Ninguna. Es el "donante" de recursos para las demás.

## 2. Estructura de Archivos (Arquitectura de Carpetas)

Para que la IA estandarice la app, debe crear esta estructura:

```text
theme/
├── models.py          # Definición de Glossary (JSONB)
├── services.py        # Lógica de traducción y cambio de tema
├── selectors.py       # Consultas optimizadas de glosario (con Redis)
├── middleware.py      # Inyección de variables CSS y detección de idioma
├── templates/
│   ├── theme/
│   │   ├── base.html  # Layout Maestro con Tailwind/Alpine/Cotton
│   │   └── macros.html # Utilidades de template
│   └── cotton/        # Librería de componentes atómicos
│       ├── button.html
│       ├── input.html
│       ├── modal.html
│       └── card.html
└── static/
    └── theme/
        ├── css/       # Tailwind output
        └── js/        # Alpine.js init

```

## 3. Especificación del Modelo: Glossary

El glosario no usa archivos `.po`, usa la base de datos para ser dinámico.

* **Campos:** * `key` (CharField, unique): Ej: `ui.buttons.save`.
* `translations` (JSONB): Ej: `{"es": "Guardar", "en": "Save"}`.
* `is_verified` (BooleanField): Para marcar si la traducción de la IA (LibreTranslate) fue revisada.



## 4. El Layout Maestro (`base.html`)

El archivo `base.html` debe inyectar dinámicamente el *Look and Feel* del Tenant.

```html
<!DOCTYPE html>
<html lang="{{ request.LANGUAGE_CODE }}">
<head>
    <style>
        :root {
            /* Tokens dinámicos desde la base de datos */
            --color-primary: {{ theme.primary_color|default:'#000' }};
            --color-secondary: {{ theme.secondary_color|default:'#fff' }};
            --font-main: {{ theme.font_family|default:'sans-serif' }};
        }
    </style>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script> </head>
<body class="font-[var(--font-main)]">
    <div id="app-root">
        {% block content %}{% endblock %}
    </div>
</body>
</html>

```

## 5. Componentes Cotton (Ejemplo de Estándar)

Cada componente debe ser autónomo y usar Alpine.js para su estado interno.

```html
<button 
    x-data="{ loading: false }" 
    @click="loading = true"
    :class="loading ? 'opacity-50 cursor-not-allowed' : ''"
    class="px-4 py-2 rounded bg-[var(--color-primary)] text-white transition {{ attrs.class }}"
>
    <span x-show="!loading">{{ slot }}</span>
    <span x-show="loading">...</span>
</button>

```

## 6. Lógica de i18n (Service Layer)

El `services.py` debe manejar el caché para no saturar PostgreSQL.

* **Método `translate(key, lang)`:**
1. Busca en Redis.
2. Si no está, busca en `Glossary` (PostgreSQL).
3. Si no está, llama a la API de **LibreTranslate** (Sidecar), guarda en DB y Redis, y devuelve el resultado.



## 7. Instrucción de Codificación para la IA (System Prompt)

Cuando estés listo para programar esta app, copia este prompt:

> "Genera el código para la App **Theme** de una Factory SaaS.
> 1. Usa **Django Cotton** para componentes en `templates/cotton/`.
> 2. Implementa un modelo `Glossary` con un campo **JSONB** para traducciones.
> 3. Crea un `middleware` que inyecte variables CSS en el context.
> 4. Usa **Alpine.js** para la reactividad de los componentes.
> 5. Configura un sistema de traducción en `services.py` que use **Redis** como caché y **LibreTranslate** como fallback asíncrono.
> 6. El layout base debe ser altamente extensible mediante bloques de Django."
> 
> 

---

### Verificación de Autonomía

La App Theme es la única que **no tiene fallback**, porque ella **es el origen del estilo**. Si ella falla, las Apps 3-9 activarán sus propios `fallback_layout.html`.

---

## Independencia y Contexto de Ecosistema

### Scope / No Scope
- **Scope:** Design system, tokens CSS via variables CSS, componentes atómicos Cotton, sistema i18n con Redis + PostgreSQL + LibreTranslate.
- **No Scope:** Cobros, órdenes, entitlements, lógica de negocio transaccional.

### Interacciones con otras apps
- **Provee a:** todas las apps (2-9) — estilos, componentes Cotton y traducciones.
- **Consume de:** ninguna app. Theme es el donante de recursos base; no tiene dependencias suaves.
- **Fallback propio:** Theme no tiene fallback porque es el origen del estilo. Si falla, las Apps 3-9 activan sus propios `fallback_layout.html`.

### Entidades de negocio propias
| Entidad | Descripción |
|---|---|
| Glossary | Glosario de traducciones almacenado en JSONB, cacheado en Redis |

> Theme no posee entidades de negocio transaccionales. Sus modelos son infraestructura de presentación.

### Riesgos conceptuales aplicables
| ID | Riesgo | Mitigación |
|---|---|---|
| R-01 | Otras apps importan modelos de Theme directamente | Toda referencia a Theme via `apps.is_installed('theme')` |
| R-02 | Apps 3-9 sin `fallback_layout.html` propio | Cada app debe definir su fallback; es parte de su DoD |

