# EPI-008 — Support: El Conserje Inteligente y el Guardián de la Retención

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** EPI-008
**Tipo:** Relation Epic — Capa 4, sistema de soporte híbrido IA + humano
**Prioridad:** 4 — Mejora retención post-venta; operaciones independientes del flujo de compra
**Sprint objetivo:** Sprint-2
**Dependencias:** EPI-000 Done, EPI-CORE Done, EPI-003 (Profiles para historial del usuario)
**Blueprints fuente:**
- `Docs/1-Core_Concept/8-support-app-cc.md`
- `Docs/2-Design-Concept/8-Support-App/` (15 documentos)

---

## § 1 — EL ALMA: Visión y Razón de Existir

### ¿Qué Problema Resuelve?

El 80% de las preguntas de soporte son repetitivas: "¿Cómo actualizo mi plan?", "¿Dónde están mis facturas?", "¿Qué significa este error?". Cada una de esas preguntas con un agente humano cuesta tiempo y dinero. Con un agente IA bien entrenado, se resuelven en segundos, a las 3 AM, sin necesidad de un humano.

EPI-008 construye el **conserje inteligente del SaaS**: un agente de IA con RAG (Retrieval-Augmented Generation) que responde basándose exclusivamente en la base de conocimiento del producto. No alucina — si no sabe, escala automáticamente a un ticket humano. Y cuando el cliente está frustrado con un cobro incorrecto, el agente ya tiene en contexto sus órdenes y pagos para darle respuesta inmediata.

### La Promesa

`ask_ai(query, user_id)` — el usuario pregunta, el agente busca en KnowledgeBase, genera la respuesta con contexto de quién es el usuario, y retorna. Si la confianza es baja o el usuario lo pide → `escalate_to_human(chat_history)` convierte la conversación en un Ticket formal con toda la historia.

Si el LLM está caído → formulario HTML de "Déjanos tu mensaje". Nunca un error 500 en la cara del usuario.

---

## § 2 — LA FILOSOFÍA: Principios Fundacionales Aplicados

| Principio | Cómo se aplica en EPI-008 |
|---|---|
| **Degradación Graciosa** | LLM no disponible → formulario HTML básico. Orders/Payment no instalados → agente opera sin contexto de compras. Telemetry fuera → alerta a La Central no emitida pero ticket se crea. |
| **Aislamiento Total** | `Ticket` y `KnowledgeArticle` en schema `tenant_{slug}`. Historial de soporte de Acme es invisible para Globex. |
| **RAG Obligatorio** | El LLM solo puede responder con información de `KnowledgeBase`. Sin artículo relevante → escala a humano. Cero alucinaciones por diseño. |
| **No Cross-App Imports** | Contexto de órdenes y pagos consumido via `orders_selectors.get_recent(user_id)` con `apps.is_installed` guard. |

---

## § 3 — LA ARQUITECTURA: Lo Que EPI-008 Crea

### Estructura de Archivos

```
apps/support/
├── models.py          ← Ticket, TicketMessage, KnowledgeArticle, ChatSession
├── services.py        ← ask_ai, escalate_to_human, create_ticket, resolve_ticket
├── selectors.py       ← get_active_tickets, get_faq_articles, get_ticket_by_id
├── ai_agents/
│   ├── brain.py       ← RAG engine: query → retrieve articles → LLM → response
│   └── vector_db.py   ← pgvector connector para búsqueda semántica
├── exceptions.py      ← TicketError, AIEscalationRequired, LLMUnavailableError
├── migrations/
│   └── 0001_initial.py
├── consumers.py       ← Django Channels WebSocket consumer (chat en vivo)
├── routing.py         ← WebSocket URL routing
├── templates/
│   ├── support/
│   │   ├── chat.html
│   │   └── fallback/
│   │       └── contact_form.html  ← formulario HTML puro (LLM caído)
│   └── cotton/
│       ├── chat_bubble.html       ← widget flotante Alpine.js
│       ├── ticket_status.html     ← estado de tickets activos
│       └── faq_accordion.html     ← x-data Alpine.js collapse
└── tests/
    ├── test_rag_engine.py
    ├── test_ticket_lifecycle.py
    └── test_ai_fallback.py
```

### Modelos de Datos

**`Ticket`** (schema `tenant_{slug}`)
| Campo | Descripción |
|---|---|
| `id` UUID | — |
| `user_id` IntegerField | usuario que abrió el ticket |
| `tenant_slug` CharField | — |
| `status` CharField | `new`, `in_progress`, `waiting_user`, `resolved`, `closed` |
| `subject` CharField | resumen del problema |
| `created_at` DateTime | — |
| `assigned_to` IntegerField null | ID de agente humano asignado |

**`KnowledgeArticle`** (schema `tenant_{slug}`)
| Campo | Descripción |
|---|---|
| `id` UUID | — |
| `title` CharField | — |
| `content` TextField | cuerpo del artículo en Markdown |
| `embedding` VectorField | vector pgvector para búsqueda semántica |
| `category` CharField | `billing`, `technical`, `onboarding` |
| `is_published` BooleanField | visible para RAG y usuarios |

**`ChatSession`** (schema `tenant_{slug}`) — conversación de IA
| Campo | Descripción |
|---|---|
| `id` UUID | — |
| `user_id` IntegerField | — |
| `messages` JSONB | `[{role: 'user/assistant', content: '...', timestamp}]` |
| `escalated` BooleanField | si fue escalada a ticket humano |
| `ticket` FK null | ticket resultante de la escalación |

### RAG Engine (brain.py)

```python
def ask_ai(query: str, user_id: int, tenant_slug: str) -> dict:
    # 1. Construir contexto del usuario (Profiles + Orders si disponibles)
    user_ctx = profiles_selectors.get_display_name(user_id, tenant_slug)
    order_ctx = orders_selectors.get_recent(user_id) if apps.is_installed('apps.orders') else []
    
    # 2. Búsqueda semántica en KnowledgeBase via pgvector
    relevant_articles = vector_db.search(query, tenant_slug, top_k=3)
    
    if not relevant_articles:
        # Sin artículos relevantes → escalar directamente
        raise AIEscalationRequired("No relevant knowledge found")
    
    # 3. Construir prompt: contexto usuario + artículos + query
    response = llm_client.chat(prompt)
    
    # 4. Si confianza < threshold → raise AIEscalationRequired
    return {"answer": response.text, "sources": [a.id for a in relevant_articles]}
```

---

## § 4 — EL ÁRBOL: User Stories de Cimientos a Acabados

| US ID | Historia | SP | Sprint | Estado |
|---|---|---|---|---|
| US-008-01 | `Ticket` model + create_ticket + state machine (new→resolved) | 3 | Sprint-2 | 🔲 Sin US file |
| US-008-02 | `KnowledgeArticle` + pgvector + `vector_db.py` búsqueda semántica | 4 | Sprint-2 | 🔲 Sin US file |
| US-008-03 | `ask_ai` RAG engine + `escalate_to_human` service | 4 | Sprint-2 | 🔲 Sin US file |
| US-008-04 | Django Channels WebSocket consumer (chat en tiempo real) | 3 | Sprint-3 | 🔲 Sin US file |
| US-008-05 | Cotton components: chat_bubble (Alpine.js), faq_accordion, fallback contact form | 3 | Sprint-2 | 🔲 Sin US file |

### Dependencias

```
US-008-01 (Ticket) ──→ US-008-03 (escalate_to_human crea Ticket)
US-008-02 (RAG)    ──→ US-008-03 (ask_ai necesita vector search)
US-008-01 + US-008-03 ──→ US-008-04 (WebSocket consume services existentes)
US-008-03          ──→ US-008-05 (UI necesita servicio operativo)
```

---

## § 5 — BLUEPRINTS DE REFERENCIA

| ID | Documento | Qué gobierna |
|---|---|---|
| CC-8 | `Docs/1-Core_Concept/8-support-app-cc.md` | Visión, RAG, estado de tickets, infraestructura |
| SP-2 | `8-Support-App/2-modelos-support-sp.md` | Modelos exactos |
| SP-3 | `8-Support-App/3-service-selector-contratos-support-sp.md` | Contratos ask_ai, escalate |
| SP-4 | `8-Support-App/4-endpoints-support-sp.md` | Endpoints y WebSocket routing |
| SP-5 | `8-Support-App/5-fallback-trazabilidad-support-sp.md` | Fallbacks y trazabilidad |

---

## § 6 — DEFINITION OF DONE

EPI-008 está Done cuando:

- [ ] `ask_ai("¿Cómo cancelo mi plan?", user_id, tenant_slug)` retorna respuesta basada en KnowledgeBase
- [ ] `ask_ai` con query irrelevante → escala a ticket humano automáticamente (sin respuesta inventada)
- [ ] `escalate_to_human(chat_history)` crea Ticket con mensajes previos incluidos
- [ ] LLM no disponible → `ask_ai` retorna error amigable y `contact_form.html` se muestra
- [ ] Chat WebSocket: mensajes aparecen en tiempo real sin polling
- [ ] Ticket de Acme no visible en panel de soporte de Globex (aislamiento de schema)
- [ ] Con Support no instalado → Profiles muestra `active_tickets: []` sin errores
- [ ] `pytest apps/support/` pasa con tests de RAG y fallback
- [ ] `product-backlog.md` actualizado: US-008-01..05 con estados correctos
