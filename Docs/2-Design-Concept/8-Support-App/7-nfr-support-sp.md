# NFR — App Support

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** SP-7-NFR

Non-functional requirements:

- Availability: 99.95% for internal APIs
- Latency: read < 200ms p95, create < 500ms p95
- Throughput: handle 200 events/s peak for Outbox consumer
- Data retention: ticket bodies retained for 7 years; PII redaction rules apply

Scaling:
- Horizontal for read paths; bounded worker pools for Outbox processing
# Non-Functional Requirements — Support App

- SLA: P1 tickets must be acknowledged within 15 minutes; P2 within 2 hours.
- Throughput: support app must handle 200 req/s for ticket creation in peak for large tenants.
- Storage: ticket attachments limited and stored in tenant-scoped blob storage.
- Security: RBAC for agents; redact PII before emitting telemetry.
- Multi-tenancy: strict tenant isolation, no cross-tenant ticket visibility.
