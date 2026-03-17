# Documento: PlanMatrix Governance

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** DC-19-PLANMATRIX
**Ubicacion:** `./Docs/2-Design-Concept/0-Factory-Saas/19-plan-matrix-fs.md`
**Capa:** Transversal — Gobernanza de políticas comerciales

## 1. Proposito

Definir el proceso operativo y API para publicar, versionar y auditar la `PlanMatrix` que mapea planes comerciales a productos y capacidades (verticals). Esta governance evita cambios ambiguos que puedan causar fugas de acceso entre tenants.

## 2. Artefactos

- `PlanMatrix` (tabla versionada) — modelo canónico de la política.
- API de publicación: `POST /api/admin/plan-matrix/publish` que crea una nueva `version` inmutable.
- `PlanMatrixVersion` — referencia incluida en eventos de aprovisionamiento y enforcement.

## 3. Flujo de publicación

1. Owner/Admin prepara un draft `PlanMatrix` en UI o mediante `POST /api/admin/plan-matrix/draft`.
2. Validaciones automáticas se ejecutan (formato, referencias a `product_id` existentes, no solapamiento de versiones coexistentes con fechasEffective conflicting).
3. Publicación crea `PlanMatrixVersion` y emite `planmatrix.published` con metadata (`version`, `created_by`, `effective_from`).
4. Los sistemas consumidores deben exponer un endpoint `GET /api/plan-matrix/active?tenant_id=<id>` que devuelve la versión efectiva para un tenant.

## 4. Gobernanza y acceso

- Solo roles `owner` o `billing_admin` pueden publicar.
- Cambios deben incluir `change_note` y estar auditados en `AuditLog`.

## 5. Compatibilidad y migraciones

- Nuevas versiones son inmutables; para corregir errores se publica una nueva versión y se documenta la migración. El enforcement usa la `matrix_version` presente en la transacción de aprovisionamiento para trazabilidad histórica.

## 6. Ejemplo de payload `PlanEntitlementsDTO`

```json
{
  "tenant_id": "11111111-1111-1111-1111-111111111111",
  "plan_id": "22222222-2222-2222-2222-222222222222",
  "matrix_version": "v2026-03-15-001",
  "allowed_products": [
    {"product_id": "33333333-3333-3333-3333-333333333333", "allowed_verticals": ["inventory","ai-agent"]}
  ]
}
```

## 7. Telemetría mínima

- `planmatrix.published` — versión publicada.
- `planmatrix.enforcement` — emitted by `enforce_plan_policy` decisions.
