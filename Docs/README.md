# Docs — Factory SaaS

**Versión del documento:** 2026.03.16
**Última actualización:** 2026-03-16

## Propósito

Centralizar la documentación viva del proyecto y asegurar que cada artefacto tenga una versión explícita y un registro maestro consultable desde la raíz de `Docs/`.

## Convención de versionado

- Todo documento Markdown dentro de `Docs/` debe incluir `Versión del documento` y `Última actualización` en la cabecera.
- Los artefactos no Markdown de `Docs/` se registran en el maestro de versiones aunque no soporten cabecera embebida.
- La referencia de última versión consolidada del corpus vive en `Docs/REGISTRO-ULTIMA-VERSION.md`.
- Cuando un documento cambie de fondo, debe actualizarse su versión documental antes de cerrar el item asociado.

## Cobertura actual

- Archivos documentales registrados: 184
- Documentos Markdown normalizados: 175
- Versión actual del corpus Docs: 2026.03.16

## Registro maestro

Ver `Docs/REGISTRO-ULTIMA-VERSION.md` para la versión más reciente de cada documento y artefacto documental.

## Automatización

- `make docs-sync`: regenera cabeceras versionadas y el registro maestro usando la fecha actual.
- `make docs-check`: valida en modo no destructivo si el sincronizador dejaría cambios pendientes en `Docs/`.
- El workflow `.github/workflows/docs-governance.yml` corre automáticamente en PRs y pushes a `main` cuando cambian artefactos documentales o el sincronizador.

## Paquetes principales

- `00-knowledge-base/`: criterios y estándares base.
- `1-Core_Concept/`: visión conceptual y documentos ancla del producto.
- `2-Design-Concept/`: diseño global y por app.
- `Agile/`: backlog y artefactos Scrum activos.
