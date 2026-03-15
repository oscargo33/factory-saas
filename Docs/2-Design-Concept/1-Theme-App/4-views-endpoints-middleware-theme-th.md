# Documento: Middleware, Views y Endpoints — App Theme

**ID:** TH-4-API
**Ubicación:** `./Docs/2-Design-Concept/1-Theme-App/4-views-endpoints-middleware-theme-th.md`
**Anchor Doc:** `Docs/1-Core_Concept/1-theme-app-cc.md`
**Dependencias Globales:** `DC-13`, `DC-14`

---

## 1. Propósito

Definir capa de entrada de Theme para inyectar contexto visual/i18n y exponer endpoints internos de administración.

---

## 2. Middleware

### 2.1 `ThemeContextMiddleware`

Responsabilidad:
- Resolver tokens activos por tenant.
- Inyectar `request.theme_tokens` para template/context processor.

Flujo:
1. Obtener `tenant_slug` desde request ya resuelto por multi-tenancy.
2. Leer caché de tokens.
3. Si no existe, consultar selector `get_theme_for_tenant`.
4. Si falla, aplicar `DEFAULT_THEME_TOKENS`.

### 2.2 `LanguageResolverMiddleware`

Responsabilidad:
- Resolver idioma efectivo con prioridad:
1. Preferencia explícita de usuario.
2. Header `Accept-Language`.
3. Idioma por tenant.
4. Default global `es`.

Resultado: `request.ui_lang`.

---

## 3. Context processor

`theme_context_processor(request)` debe exponer:

| Clave | Origen |
|---|---|
| `theme` | `request.theme_tokens` |
| `ui_lang` | `request.ui_lang` |
| `theme_contract_version` | constante `theme.contract.v1` |

---

## 4. Endpoints internos (admin/ops)

Prefijo sugerido: `/internal/theme/`

| Método | Endpoint | Descripción | Permiso |
|---|---|---|---|
| `GET` | `/config/` | Obtener configuración visual vigente | owner/admin |
| `PUT` | `/config/` | Actualizar tokens visuales | owner/admin |
| `GET` | `/glossary/` | Buscar entradas de glosario | owner/admin/editor |
| `POST` | `/glossary/` | Crear/actualizar traducción | owner/admin/editor |
| `POST` | `/glossary/sync/` | Sincronización masiva | owner/admin |

### Reglas de seguridad

- Todos los endpoints requieren tenant activo.
- RBAC por rol de membership.
- Rate limit para sync masivo.

---

## 5. Degradación graciosa

Si Theme no está instalado:
- Los endpoints no existen (404 controlado por routing).
- Apps consumidoras deben renderizar con fallback local.
- No debe romperse ningún flujo transaccional.

---

## 6. Criterios de aceptación

- [ ] Middleware define `theme_tokens` y `ui_lang` en todos los requests de tenant.
- [ ] Endpoints internos tienen RBAC y aislamiento por tenant.
- [ ] Sin Theme instalado, el sistema mantiene operación con fallback.
