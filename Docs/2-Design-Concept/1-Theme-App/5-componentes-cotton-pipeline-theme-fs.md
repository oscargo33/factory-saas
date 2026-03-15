# Documento: Componentes Cotton y Pipeline Visual — App Theme

**ID:** TH-5-UI
**Ubicación:** `./Docs/2-Design-Concept/1-Theme-App/5-componentes-cotton-pipeline-theme-fs.md`
**Anchor Docs:** `Docs/1-Core_Concept/1-theme-app-cc.md`, `Docs/2-Design-Concept/0-Factory-Saas/14-pipeline-tailwind-cotton-fs.md`

---

## 1. Propósito

Definir estándar de componentes UI reutilizables y su integración con Tailwind + Alpine en todas las apps consumidoras.

---

## 2. Estructura de componentes

Ruta base:

`templates/cotton/`

Estructura mínima:

- `button.html`
- `input.html`
- `card.html`
- `modal.html`
- `alert.html`
- `layout/topbar.html`
- `layout/sidebar.html`

---

## 3. Convenciones de API de componente

| Convención | Regla |
|---|---|
| Props | Definidas explícitamente en `c-vars` |
| Variantes | `variant=primary|secondary|danger|ghost` |
| Estados | `disabled`, `loading`, `error` |
| Theming | Sin colores hardcodeados; siempre CSS vars |
| Accesibilidad | Soporte `aria-*`, `role`, foco visible |

---

## 4. Pipeline Tailwind

Reglas:
- Tailwind compila en build y produce CSS estático.
- `content` incluye templates Django y Cotton.
- Tokens visuales consumen CSS vars (`--color-primary`, etc.).

Objetivo:
- Permitir que cada tenant cambie look & feel sin recompilar CSS.

---

## 5. Alpine.js

Uso permitido:
- Estado de componentes atómicos (`loading`, `open`, `expanded`).
- Stores globales ligeros (`ui`, `auth`, `tenant`) cuando sea estrictamente necesario.

Uso no permitido:
- Lógica de negocio de dominio.
- Estado complejo que debería vivir en backend.

---

## 6. Matriz de fallback para consumidores

| Escenario | Respuesta esperada |
|---|---|
| Theme instalado y sano | Render normal con tokens tenant |
| Theme instalado, sin `ThemeConfig` | Render con `DEFAULT_THEME_TOKENS` |
| Theme no instalado | Cada app usa `fallback_layout.html` propio |
| Componente Cotton faltante | Render degradado HTML semántico básico |

---

## 7. Criterios de aceptación

- [ ] Los componentes base existen y están versionados.
- [ ] No hay hardcode de colores fuera de defaults.
- [ ] Las apps consumidoras pueden renderizar sin Theme.
- [ ] Se mantiene accesibilidad mínima en componentes críticos.
