# Checklist de Diseño — App 1 Theme

**ID:** TH-1-CK
**Ubicación:** `./Docs/2-Design-Concept/1-Theme-App/1-checklist-theme-app.md`
**Anchor Doc:** `Docs/1-Core_Concept/1-theme-app-cc.md`
**Estado:** v1.0

---

## Control de Versiones

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v1.0 | 2026-03-14 | Arq. IA (GitHub Copilot) | Creación inicial del paquete de diseño Theme |
| v1.1 | 2026-03-14 | Arq. IA (GitHub Copilot) | Alineación explícita de alcance global, fallback e i18n multiidioma |

---

## Bloques de diseño

### A. Modelo de datos

- [x] Definición conceptual de `Glossary`.
- [x] Definición conceptual de `ThemeConfig`.
- [x] Reglas de validación por tenant y fallback por defecto.

### B. Service/Selector

- [x] Contratos de lectura públicos para otras apps.
- [x] Contratos de escritura y control de cambios de tema.
- [x] Flujo de traducción con caché + fallback.

### C. Middleware y endpoints

- [x] Diseño de `ThemeContextMiddleware`.
- [x] Diseño de `LanguageResolverMiddleware`.
- [x] Diseño de endpoints internos de administración de tema y glosario.

### D. UI y componentes

- [x] Convención de componentes Cotton base.
- [x] Integración con pipeline Tailwind/Alpine.
- [x] Reglas de versionado y compatibilidad visual.

### E. Independencia y resiliencia

- [x] Contrato para consumidores cuando Theme está instalado.
- [x] Política para consumidores cuando Theme no está instalado.
- [x] Riesgos principales y mitigaciones de diseño.

### F. Cobertura global e i18n

- [x] Theme cubre todas las apps consumidoras y Product Core integrado.
- [x] Todas las apps deben tener `fallback_layout.html` si Theme falla/no está.
- [x] Idioma base definido: español (`es`) y no se traduce.
- [x] Matriz inicial definida: 6 idiomas totales (`es` + `en`, `it`, `fr`, `de`, `pt`).

---

## Criterio de Cierre (Diseño App 1)

- [ ] Todos los documentos TH-2 a TH-5 aprobados por revisión arquitectónica.
- [ ] Trazabilidad completa a Core Concept y a DC globales.
- [ ] Lista de interfaces públicas estable y versionada.
- [ ] Matriz de idiomas inicial (6) validada por negocio y producto.
