# Documento: Roles, Permisos y Capas — App 8 Support

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** SP-12-RBAC
**Ubicacion:** `./Docs/2-Design-Concept/8-Support-App/12-roles-permisos-capas-support-sp.md`
**Anchor Docs:** `8-support-app-cc.md`, `22-roles-permisos-capas-ux-fs.md`

---

## 1. Roles que interactuan con Support

| Rol | Relacion con la app |
|---|---|
| `anonymous` | Puede leer knowledge base publica y enviar formulario de contacto |
| `member` | Crea tickets y hace seguimiento de sus casos |
| `admin` | Ve y gestiona tickets del tenant; puede asignar a agentes |
| `owner` | Igual que admin; puede escalar a staff |
| `agent` (staff de soporte) | Atiende tickets; accede a herramientas IA y escalacion |
| `staff` | Soporte interno de la Factory; ve tickets cross-tenant |
| `superadmin` | Acceso total; gestiona reglas de escalacion globales |

---

## 2. Capa Publica (anonymous)

| Pantalla / Accion | Permitido | Restriccion |
|---|---|---|
| Knowledge base / Centro de ayuda | Si | Solo articulos marcados como publicos |
| Busqueda en knowledge base | Si | Solo contenido publico indexado |
| Formulario de contacto (lead/prospecto) | Si | No crea ticket; genera lead para Profiles |
| Ver estado de ticket | No | Requiere login y ser el creador |

---

## 3. Capa Privada por rol

| Pantalla / Accion | member | admin | owner | agent |
|---|---|---|---|---|
| Crear ticket | Si | Si | Si | Si |
| Ver historial de tickets propios | Si | Si | Si | Si |
| Ver tickets de todo el tenant | No | Si | Si | Si |
| Responder a mensaje de ticket propio | Si | Si | Si | Si |
| Adjuntar archivos a ticket | Si | Si | Si | Si |
| Asignar ticket a agente | No | Si | Si | Si |
| Cambiar prioridad de ticket | No | Si | Si | Si |
| Escalar ticket a staff de Factory | No | No | Si | Si |
| Cerrar ticket | Si (propio) | Si | Si | Si |
| Ver y editar knowledge base interna | No | No | No | Si |
| Publicar articulo en knowledge base | No | No | No | Si (con revision) |
| Ver metricas de SLA del tenant | No | Si | Si | Si |
| Configurar reglas de escalacion | No | No | No | No (solo staff/superadmin) |

---

## 4. Capa Admin Django (staff / superadmin)

| Modelo | staff/agent (lectura) | staff/agent (escritura) | superadmin |
|---|---|---|---|
| Ticket | Si | Si (asignar, escalar, cerrar) | CRUD completo |
| TicketMessage | Si | Si (moderacion de contenido) | CRUD completo |
| KnowledgeArticle | Si | Si (crear, editar, publicar) | CRUD completo |
| EscalationRule | Si | No | CRUD completo |

Restricciones criticas:
- Tickets cerrados son de solo lectura; no se pueden reabrir sin flujo formal.
- `EscalationRule` solo es modificable por `superadmin`.

---

## 5. Assets de Support

| Asset | Operacion | anonymous | member | admin | owner | agent | staff | superadmin |
|---|---|---|---|---|---|---|---|---|
| Articulos knowledge base publicos | Ver | Si | Si | Si | Si | Si | Si | Si |
| Articulos internos (privados) | Ver | No | No | No | No | Si | Si | Si |
| Adjuntos de ticket | Ver | No | Si (propio ticket) | Si | Si | Si | Si | Si |
| Adjuntos de ticket | Cargar | No | Si | Si | Si | Si | No | Si |
| Adjuntos de ticket | Borrar | No | No | Si | Si | Si | No | Si |
| Export de tickets (CSV) | Exportar | No | No | Si (tenant) | Si | Si | Si (cross) | Si |
| Grabaciones de sesion IA (si aplica) | Ver | No | Si (propias) | No | No | Si | Si | Si |
| Grabaciones de sesion IA (si aplica) | Borrar | No | No | No | No | No | No | Si |

---

## 6. Notas de seguridad

- Adjuntos de tickets se escanean por malware antes de almacenarse.
- Los datos de conversacion con IA no se reentrenan con PII del cliente sin consentimiento explicito.
- Tickets eliminados (soft delete) permanecen auditables por `superadmin`.
