# Documento: Matriz de Trazabilidad - App Theme

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** TH-6-TRA
**Ubicación:** `./Docs/2-Design-Concept/1-Theme-App/6-matriz-trazabilidad-theme-th.md`
**Anchor Docs:** `Docs/1-Core_Concept/1-theme-app-cc.md`, `Docs/2-Design-Concept/0-Factory-Saas/14-pipeline-tailwind-cotton-fs.md`, `Docs/2-Design-Concept/0-Factory-Saas/16-contratos-inter-app-fs.md`

---

## 1. Propósito

Asegurar trazabilidad completa entre requerimientos del Core Concept, decisiones de diseño y criterios de verificación de App Theme.

---

## 2. Matriz Requerimiento -> Diseño -> Evidencia

| Req ID | Requerimiento | Documento de Diseño | Criterio de Evidencia |
|---|---|---|---|
| TH-R01 | Theme controla look and feel de todas las apps y Product Core | `5-componentes-cotton-pipeline-theme-th.md` | Integración de tokens y fallback validado |
| TH-R02 | Apps consumidoras operan si Theme no está/no saludable | `4-views-endpoints-middleware-theme-th.md` | `fallback_layout.html` por app consumidora |
| TH-R03 | i18n por DB con Django + LibreTranslate | `3-service-selector-contratos-theme-th.md` | Flujo cache -> DB -> Django -> LibreTranslate |
| TH-R04 | Idioma base `es` no traducible | `2-modelos-theme-th.md` | Regla de validación obligatoria por `key` |
| TH-R05 | Matriz inicial 6 idiomas totales | `2-modelos-theme-th.md` | `es` + `en/it/fr/de/pt` documentados |
| TH-R06 | Contratos inter-app sin import de modelos cruzados | `3-service-selector-contratos-theme-th.md` | Publicación de contrato v1 en DC-16 |
| TH-R07 | Product Core consume contratos Theme | `3-service-selector-contratos-theme-th.md` | Consumo de `theme.get_tokens.v1` y `theme.translate.v1` |

---

## 3. Cobertura por Capa

| Capa | Cobertura Theme |
|---|---|
| Capa 4 | Service/Selector para tokens y traducciones |
| Capa 6 | Tailwind + Cotton + Alpine |
| Capa Transversal | Contratos inter-app, fallback y gobernanza de idioma |

---

## 4. Criterios de aceptación

- [ ] Todos los requerimientos TH-R01..TH-R07 trazados a documentos concretos.
- [ ] Cada requerimiento tiene evidencia verificable para revisión de sprint.
- [ ] No existen requerimientos sin artefacto de diseño asociado.

## 5. Cobertura obligatoria DC-12/DC-13/DC-16/DC-17

- DC-12 (patron service layer): cubierto en `3-service-selector-contratos-theme-th.md`.
- DC-13 (router dinamico y contexto tenant): aplica en consumo multi-tenant de tokens/traducciones y fallback por tenant.
- DC-16 (contratos inter-app): cubierto por `theme.get_tokens.v1` y `theme.translate.v1`.
- DC-17 (diccionario de datos logico): cubierto por entidades/atributos de tokens, traducciones y metadata de idioma.
