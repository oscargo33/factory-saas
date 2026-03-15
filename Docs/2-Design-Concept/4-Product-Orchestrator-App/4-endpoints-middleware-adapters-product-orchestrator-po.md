# Documento: Endpoints, Middleware y Adapters - App Product Orchestrator

**ID:** PO-4-API
**Ubicacion:** `./Docs/2-Design-Concept/4-Product-Orchestrator-App/4-endpoints-middleware-adapters-product-orchestrator-po.md`
**Anchor Docs:** `Docs/1-Core_Concept/4-product-orchestrator-app-cc.md`, `Docs/2-Design-Concept/0-Factory-Saas/13-router-dinamico-esquemas-fs.md`

---

## 1. Proposito

Definir superficie HTTP y arquitectura de adaptacion externa para Product Core, preservando aislamiento tenant y resiliencia.

---

## 2. Middleware y contexto

- Requiere tenant resuelto por middleware global (`tenant_slug`, `tenant_id`).
- Requiere usuario autenticado para endpoints privados.
- Requiere validacion de membership activa para acciones de provision y revocacion.

Regla critica:
- Ninguna operacion de catalogo/autorizacion se ejecuta sin contexto tenant valido.

---

## 3. Endpoints (diseno)

| Metodo | Ruta | Descripcion | Permisos |
|---|---|---|---|
| `GET` | `/api/orchestrator/catalog` | Lista productos activos del tenant | `member+` |
| `GET` | `/api/orchestrator/catalog/{product_id}` | Detalle de producto | `member+` |
| `GET` | `/api/orchestrator/features/{feature_key}/state` | Estado de capacidad y cuota | `member+` |
| `POST` | `/api/orchestrator/provision` | Provision post-compra o admin | `admin+` |
| `POST` | `/api/orchestrator/features/{feature_key}/revoke` | Revoca entitlement | `owner/admin` |
| `POST` | `/api/orchestrator/catalog/sync` | Sincroniza catalogo desde Product Core | `owner/admin` |

---

## 4. Adapter Pattern

Estructura recomendada:

```text
apps/product_orchestrator/adapters/
  base.py        # Interface abstracta
  core_app.py    # Cliente real Product Core
  mock_demo.py   # Implementacion local para modo demo/testing
```

Interface minima (`base.py`):
- `fetch_catalog(tenant_id) -> list[dict]`
- `provision_feature(tenant_id, feature_key, payload) -> dict`
- `revoke_feature(tenant_id, feature_key) -> dict`
- `healthcheck() -> bool`

Reglas:
- Timeouts estrictos por llamada.
- Retry acotado con backoff.
- Errores normalizados a codigos de dominio (`core_unavailable`, `timeout`, `invalid_payload`).

---

## 5. Fallback operativo

- Si Product Core no responde: responder `503` controlado y no exponer stacktrace.
- Si adapter primario falla y existe `mock_demo`: fallback a modo demo solo para features marcadas demo.
- Si Telemetry no esta disponible: continuar flujo y registrar warning local.

---

## 6. Criterios de aceptacion

- [ ] Endpoints privados con control por rol y tenant.
- [ ] Adapter Pattern desacoplado y testeable.
- [ ] Politicas de timeout/retry/error normalizadas.
