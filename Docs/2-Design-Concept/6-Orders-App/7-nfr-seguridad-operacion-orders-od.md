# NFR, Seguridad y Operación — Orders

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** OD-7-NFR

No funcionales y controles operativos:

- **Consistency:** `freeze_cart` must ensure snapshot atomicity; DB transactions and outbox in same transaction.
- **Idempotency:** expose `Idempotency-Key` for `freeze` and `pay` endpoints; handlers must dedupe by `operation_id`.
- **Performance:** Paginated queries for orders; `orders` should be read-optimized for dashboard queries.
- **Fault tolerance:** workers for outbox must be horizontally scalable; provide health-check endpoints.
- **Security:** webhooks require signature verification; only trusted origins allowed for `mark_as_paid`.
- **Retention & GDPR:** order and price_snapshots retention policy configurable; support purge on `right-to-be-forgotten` while preserving billing traceability in `price_snapshot` masked copies.
- **Observability:** required metrics listed in `5-order-lifecycle-fallback-od.md`.
