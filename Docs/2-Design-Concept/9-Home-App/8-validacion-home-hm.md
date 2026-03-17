# Validación — Home App

**ID:** HM-8-VAL

Checklist de validación en Diseño Conceptual:

- `get_home_widgets` DTOs definidos y mapeados a DC-16.
- `HomeWidget` y `HomeSnapshot` registrados en DC-17.
- Tests skeleton: fixtures para `home/widgets` y `home/snapshot` en `Docs/.../contracts-examples/`.
- Telemetry: eventos `home.widget.interaction` y `home.snapshot.generated` definidos.
- Seguridad: Asegurar que `HomeSnapshot.payload` no contenga PII.

Tests sugeridos (esqueletos):
- `tests/contracts/test_home_widgets.py` — validar contrato `get_home_widgets` y schema del DTO.
- `tests/contracts/test_home_snapshot.py` — validar snapshot TTL y ETag semantics.
