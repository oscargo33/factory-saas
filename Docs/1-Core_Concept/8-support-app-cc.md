Este es el **Documento Maestro 8: App Support (Relación y Asistencia Agéntica)**. En el ecosistema de la Factory, esta aplicación es el "Conserje Inteligente", encargado de reducir la fricción del usuario y proteger la retención mediante una mezcla de automatización con IA y gestión humana de incidencias.

---

# Documento Maestro 8: App Support (Relación y Retención)

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

## 1. Identidad de la Aplicación

* **Nivel de Profundidad:** 8 (Capa de Relación).
* **Rol:** Gestión de tickets de soporte, base de conocimientos (Knowledge Base) y asistencia automatizada mediante un Agente de IA con RAG (Retrieval-Augmented Generation).
* **Dependencias Suaves:** App 3 (Profiles) para historial del usuario; App 6/7 (Orders/Payment) para contexto de reclamos; App 2 (Telemetry) para alertar a La Central sobre crisis de soporte.

## 2. Estructura de Archivos (Arquitectura de Carpetas)

```text
support/
├── ai_agents/         # Lógica de RAG y prompts para el Agente IA
│   ├── brain.py       # Integración con LLMs (OpenAI/Anthropic)
│   └── vector_db.py   # Conector para búsqueda semántica en la documentación
├── services.py        # Creación de tickets y escalamiento de IA a Humano
├── selectors.py       # Consultas de FAQs y estado de tickets del usuario
├── templates/
│   ├── support/
│   │   └── fallback/  # Formulario de contacto básico (HTML puro)
│   └── cotton/        # Componentes de interacción
│       ├── chat_bubble.html
│       ├── ticket_status.html
│       └── faq_accordion.html

```

## 3. El Agente IA (Híbrido RAG)

Para que la IA no invente respuestas (alucinaciones), debe seguir el patrón de **Generación Aumentada por Recuperación (RAG)**:

1. **Recuperación:** El usuario pregunta algo. La app busca en la "Knowledge Base" local los artículos más relevantes.
2. **Contexto:** Se le entrega a la IA el texto de esos artículos + los datos básicos del usuario (ej: "El usuario tiene el Plan Pro").
3. **Respuesta:** La IA genera una respuesta basada **únicamente** en esa información. Si no sabe la respuesta, ofrece abrir un ticket humano.

## 4. Ciclo de Vida del Ticket

La IA debe gestionar una máquina de estados para los hilos de soporte:

* **New:** Creado por el usuario o la IA.
* **In Progress:** Asignado a un agente humano en el panel administrativo.
* **Waiting User:** El agente respondió y espera confirmación del cliente.
* **Resolved/Closed:** Problema solucionado.

## 5. Implementación UI con Cotton y Alpine.js

* **`c-chat-bubble`:** Un componente flotante que usa Alpine.js para abrir/cerrar la ventana de chat y manejar el estado de "IA escribiendo..." mediante un pequeño spinner reactivo.
* **`c-faq-accordion`:** Usa `x-data="{ active: null }"` para permitir una navegación rápida por las dudas frecuentes sin recargar la página.

## 6. Contratos de Interfaz (Service Layer & Resiliencia)

* **`SupportService.ask_ai(query, user_id)`:** Procesa la pregunta del usuario y retorna la respuesta de la IA.
* **`SupportService.escalate_to_human(chat_history)`:** Convierte una conversación de IA en un ticket formal.
* **Protocolo de Resiliencia:** * Si el **Servicio de IA (LLM)** falla o no hay internet, el chat muestra automáticamente un formulario de "Déjanos tu mensaje" (`fallback_layout.html`).
* Si la **App 7 (Payment)** no está, el ticket no podrá mostrar automáticamente si la factura está pagada, pero el usuario podrá subir una captura de pantalla manualmente.



## 7. Especificación de Infraestructura y Herramientas

| Componente | Tecnología | Función |
| --- | --- | --- |
| **LLM Engine** | LangChain / OpenAI API | Cerebro del Agente IA. |
| **Vector Storage** | pgvector (PostgreSQL) | Búsqueda semántica en manuales de ayuda. |
| **Real-time** | Django Channels (WebSockets) | Chat en vivo sin refresco de página. |
| **UI Interaction** | **Alpine.js** | Micro-interacciones del chat y notificaciones. |

---

## 8. Instrucción de Codificación para la IA (System Prompt)

Usa este prompt para construir esta app:

> "Genera el código para la App **Support** de una Factory SaaS.
> 1. Implementa un sistema de **Ticketing** con estados (New, In Progress, Closed).
> 2. Diseña un servicio de **Agente IA** que use un patrón RAG para responder dudas basándose en una tabla de 'KnowledgeBase'.
> 3. En `services.py`, crea la lógica para convertir un chat fallido en un ticket humano automáticamente.
> 4. Usa **Django Cotton** para crear componentes de 'Chat Bubble' y 'FAQ Accordion'.
> 5. La UI debe ser reactiva usando **Alpine.js** para manejar el envío de mensajes vía fetch asíncrono.
> 6. Implementa **Soft-Dependencies**: si la App 'Telemetry' está instalada, reporta cada vez que un usuario califica negativamente una respuesta de la IA para que sea revisada en La Central."
> 
> 

---

### Verificación de Autonomía

La App Support puede vivir como un sistema de ayuda independiente. Si borras Orders o Payment, sigue siendo un centro de ayuda FAQ. Su valor reside en ser el "paracaídas" del sistema: si todo lo demás falla, Support es donde el usuario pide ayuda.

---

## Independencia y Contexto de Ecosistema

### Scope / No Scope
- **Scope:** Gestión de tickets de soporte, base de conocimiento (Knowledge Base), agente IA con RAG, escalamiento a humano, retención de clientes.
- **No Scope:** Autorización de acceso al producto, procesamiento de pagos, gestión de catálogo.

### Interacciones con otras apps
- **Provee a:** App 3 (Profiles) — tickets activos para dashboard de usuario.
- **Consume de (soft-dependency):**
  - App 3 (Profiles): historial del usuario para contextualizar tickets. Fallback: ticket se crea sin contexto de historial.
  - App 6 (Orders): contexto de órdenes en reclamos. Fallback: agente IA no muestra detalle de orden; usuario puede subir captura.
  - App 7 (Payment): estado de factura para reclamos de cobro. Fallback: idem Orders.
  - App 2 (Telemetry): alerta a La Central sobre crisis de soporte. Fallback: alerta no emitida; ticket se crea igualmente.

### Entidades de negocio propias
| Entidad | Descripción |
|---|---|
| Ticket | Caso de soporte con estados (New, In Progress, Waiting User, Resolved) |
| KnowledgeArticle | Entrada de base de conocimiento para el RAG del agente IA |

### Riesgos conceptuales aplicables
| ID | Riesgo | Mitigación |
|---|---|---|
| R-01 | Importación directa de modelos Order/Payment en Support | Solo acceso via `OrdersSelector` y `PaymentSelector` con `apps.is_installed` |
| R-08 | Alucinaciones del agente IA | Patrón RAG obligatorio: respuestas solo desde KnowledgeBase; escalamiento automático a humano si confianza baja |
