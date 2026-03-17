# NFR — Home App

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** HM-7-NFR

Non-functional requirements (conceptual):

- Availability: 99.9% for internal APIs
- Latency targets: widgets read p95 < 200ms, snapshot read p95 < 120ms
- Snapshot generation: should complete < 2s per tenant typical (depends on widgets)
- Throughput: support 500 rps aggregate for landing during peak campaigns; autoscale snapshot worker horizontally
- Data retention: `HomeSnapshot` TTL default 3600s (configurable)

Scalability:
- Read paths are cache-first; scale via CDN or edge cache for public landing.
