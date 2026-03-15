# Documento: 14-pipeline-tailwind-cotton-fs.md

**ID:** DC-14-FS
**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/14-pipeline-tailwind-cotton-fs.md`
**Referencia Core:** `0-factory_saas-cc.md`, `1-theme-app-cc.md`
**Capa:** 6 — Frontend (Tailwind CSS + Django Cotton + Alpine.js)
**Apellido:** **-fs**

---

## 1. Propósito

La Capa 6 define el sistema de diseño frontend de la Factory. Su objetivo es proporcionar:
- Una **librería de componentes atómicos** (Cotton) reutilizables en todas las apps.
- Un **sistema de tokens de diseño** (CSS Variables) que el **Theme App** personaliza por tenant.
- **Reactividad ligera** (Alpine.js) sin necesidad de un framework SPA completo.
- Cobertura visual homogénea para todas las apps y Product Core integrado.

---

## 2. Arquitectura del Pipeline de Estilos

```
Theme App (DB)
    │ Genera: --color-primary, --font-body, etc.
    ▼
base.html (inyection de CSS variables en <style> tag)
    │
    ▼
Tailwind CSS (usa las variables como utilidades)
    │
    ▼
Django Cotton Components (templates/cotton/)
    │
    ▼
Alpine.js (reactividad client-side ligera)
```

---

## 3. Tailwind CSS: Configuración

### 3.1. Integración con Django

Tailwind se compila durante el build de Docker (o `npm run build` en desarrollo). El resultado es un único archivo `output.css` que se coloca en `staticfiles/`.

| Aspecto | Decisión de diseño |
|---|---|
| Versión | Tailwind CSS v3.x (CDN de producción **prohibido**; siempre build propio) |
| Modo JIT | Activado por defecto (genera solo clases usadas) |
| Archivo de entrada | `static/src/css/input.css` |
| Archivo de salida | `static/dist/css/output.css` → colectado por `collectstatic` |
| Toolchain | Node.js + PostCSS (solo en build; no en runtime del servidor) |

### 3.2. `tailwind.config.js`: Rutas de Content

El scanner de Tailwind debe incluir todos los templates de Django y Cotton:

| Ruta añadida a `content` | Razón |
|---|---|
| `**/templates/**/*.html` | Templates estándar de Django |
| `**/templates/cotton/**/*.html` | Componentes Cotton |
| `**/forms/**/*.py` | Clases de formulario que emiten clases CSS |
| `**/static/src/js/**/*.js` | Alpine.js con clases Tailwind en strings |

### 3.3. Design Tokens como CSS Variables

Los tokens se definen en la configuración de Tailwind como extensiones del tema:

| Token | Variable CSS | Ejemplo de valor default |
|---|---|---|
| Color primario | `--color-primary` | `#4F46E5` (indigo) |
| Color secundario | `--color-secondary` | `#7C3AED` (violeta) |
| Color de fondo | `--color-bg` | `#F9FAFB` |
| Color de texto | `--color-text` | `#111827` |
| Fuente body | `--font-body` | `'Inter', sans-serif` |
| Fuente heading | `--font-heading` | `'Lexend', sans-serif` |
| Border radius base | `--radius-base` | `0.375rem` |

El Theme App escribe los valores de estas variables en la DB. `base.html` inyecta un bloque `<style>:root { ... }</style>` con los valores específicos del tenant.

**Fallback:** Si el Theme App no está instalado (`apps.is_installed('apps.theme')` es False) o no está saludable (timeout/error), se usan los valores default hardcodeados en `tailwind.config.js`.

---

## 4. Django Cotton: Sistema de Componentes

### 4.1. Estructura de Directorio

```
templates/
└── cotton/
    ├── button.html           ← <c-button label="..." variant="primary" />
    ├── card.html             ← <c-card title="..."> ... </c-card>
    ├── form/
    │   ├── input.html        ← <c-form.input name="..." label="..." />
    │   └── select.html       ← <c-form.select name="..." options="..." />
    ├── layout/
    │   ├── sidebar.html      ← Layout con sidebar
    │   └── topbar.html       ← Header de navegación
    └── alert.html            ← <c-alert type="success|error|warning" />
```

### 4.2. Configuración en Django

| Setting | Valor |
|---|---|
| `COTTON_DIR` | `'templates/cotton'` |
| `INSTALLED_APPS` | Incluir `'django_cotton'` |
| `TEMPLATES[0]["DIRS"]` | Incluir `'templates'` como directorio raíz |

### 4.3. Convención de Componentes

Cada componente Cotton debe seguir las reglas:
- Props documentados en el `<c-vars>` del template.
- Variantes mediante un prop `variant` (ej. `primary`, `secondary`, `danger`).
- El componente siempre renderiza con los tokens CSS; nunca con colores hardcodeados.

---

## 5. Alpine.js: Reactividad Ligera

### 5.1. Integración

Alpine.js se carga desde el CDN en `base.html` durante desarrollo y desde `staticfiles/` en producción (para control de versión y CSP estricto).

| Aspecto | Decisión |
|---|---|
| Versión mínima | Alpine.js v3.x |
| Carga | `defer` en `<head>` (no `async`) para garantizar orden de plugins |
| Plugins usados | `Alpine.store` (estado global), `Alpine.data` (componentes reutilizables) |

### 5.2. Stores Globales

Alpine define stores globales para estado compartido entre componentes:

| Store | Datos que contiene |
|---|---|
| `auth` | `{ user_id, is_authenticated, role }` |
| `tenant` | `{ slug, name, plan }` |
| `ui` | `{ sidebar_open, theme_mode }` |

Los stores se inicializan desde el template `base.html` usando datos inyectados por Django en el context processor.

---

## 6. `base.html`: Template Raíz

El template `base.html` es el punto de integración de todos los sistemas de la Capa 6:

| Sección de `base.html` | Contenido |
|---|---|
| `<head>` CSS variables | `<style>:root { --color-primary: {{ theme.primary }}; ... }</style>` |
| `<head>` Tailwind | `<link rel="stylesheet" href="{% static 'dist/css/output.css' %}">` |
| `<body>` Alpine init | `<script>/* Alpine stores init */</script>` |
| `{% block content %}` | Punto de inserción para templates de cada vista |
| `<body>` Alpine.js | `<script src="{% static 'dist/js/alpine.js' %}" defer></script>` |

---

## 7. Relación con Otros Documentos

| Documento | Relación |
|---|---|
| `1-theme-app-cc.md` | El Theme App es quien provee los valores de CSS variables al template base |
| DC-8 `8-entrypoint-specs-fs.md` | `collectstatic` colecta el CSS compilado de Tailwind en startup |
| DC-16 `16-contratos-inter-app-fs.md` | Contrato para que el Theme App exponga los tokens al context processor |

---

## 8. Criterios de Aceptación del Diseño

- [ ] Tailwind se compila en build; no se usa CDN en producción.
- [ ] Todos los componentes Cotton usan tokens CSS variables, nunca colores hardcodeados.
- [ ] El fallback de theme funciona correctamente cuando el Theme App no está instalado.
- [ ] El fallback de theme funciona también cuando Theme está instalado pero no saludable.
- [ ] Alpine.js stores están definidos y documentados.
- [ ] `base.html` inyecta las CSS variables del tenant antes del CSS de Tailwind.
- [ ] Los componentes Cotton tienen su directorio en `templates/cotton/` y siguen la convención de naming.
- [ ] Product Core consume el mismo pipeline visual con degradación documentada.
