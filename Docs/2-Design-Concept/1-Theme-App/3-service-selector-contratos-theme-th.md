# Documento: Service, Selector y Contratos — App Theme

**ID:** TH-3-SVC
**Ubicación:** `./Docs/2-Design-Concept/1-Theme-App/3-service-selector-contratos-theme-th.md`
**Anchor Doc:** `Docs/1-Core_Concept/1-theme-app-cc.md`
**Dependencias Globales:** `DC-12`, `DC-16`

---

## 1. Propósito

Definir contratos públicos y privados de Theme bajo el patrón Service/Selector para mantener independencia inter-app.

---

## 2. Selectors públicos (lectura)

Estos selectors pueden ser consumidos por otras apps.

| Función | Firma | Retorna | Consumidores |
|---|---|---|---|
| `get_theme_for_tenant` | `(tenant_slug: str) -> dict | None` | Tokens activos | Todas las apps UI |
| `get_translation` | `(key: str, lang: str, tenant_slug: str) -> str` | Texto traducido o key fallback | Todas las apps |
| `get_translations_batch` | `(keys: list[str], lang: str, tenant_slug: str) -> dict[str, str]` | Mapa de traducciones | Home, Support, Orders |

### Comportamiento de fallback

- Sin Theme instalado: retorna defaults neutros (`DEFAULT_THEME_TOKENS`, `key` original).
- Sin key existente: retorna la `key` y genera evento para curación posterior.

---

## 3. Services internos (escritura)

| Función | Firma | Efecto |
|---|---|---|
| `upsert_translation` | `(key, lang, text, tenant_slug, source='manual') -> None` | Crea/actualiza glosario |
| `bulk_sync_translations` | `(items: list[dict], tenant_slug: str) -> int` | Sincronización masiva |
| `set_active_theme` | `(tenant_slug: str, payload: dict) -> None` | Actualiza `ThemeConfig` activo |
| `translate_with_fallback` | `(key, lang, tenant_slug) -> str` | Cache -> DB -> proveedor externo |

### Reglas

- Escritura solo vía services.
- Operaciones de escritura en transacción atómica.
- Se invalidan cachés de selector al modificar `Glossary` o `ThemeConfig`.

---

## 4. Contratos inter-app formales

Versión inicial: `theme.contract.v1`

| Contrato | Tipo | Payload entrada | Payload salida |
|---|---|---|---|
| `theme.get_tokens.v1` | Selector | `{tenant_slug}` | `{primary_color, secondary_color, ...}` |
| `theme.translate.v1` | Selector | `{key, lang, tenant_slug}` | `{text}` |
| `theme.translate_batch.v1` | Selector | `{keys, lang, tenant_slug}` | `{translations}` |

### Política de versión

- Cambios compatibles: misma versión.
- Cambios breaking: crear `v2` y mantener `v1` deprecado por al menos un sprint.

---

## 5. Relación con otros documentos

| Documento | Relación |
|---|---|
| `Docs/2-Design-Concept/0-Factory-Saas/12-patron-service-layer-fs.md` | Convenciones obligatorias de Service/Selector |
| `Docs/2-Design-Concept/0-Factory-Saas/16-contratos-inter-app-fs.md` | Registro global de contratos públicos |

---

## 6. Criterios de aceptación

- [ ] Todos los contratos públicos de Theme están versionados.
- [ ] Hay fallback neutral para falta de Theme o faltante de traducción.
- [ ] No existe escritura fuera de `services.py`.
