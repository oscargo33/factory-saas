# Documento: Roles, Permisos y Capas — App 7 Payments

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** PY-12-RBAC
**Ubicacion:** `./Docs/2-Design-Concept/7-Payment-App/12-roles-permisos-capas-payments-py.md`
**Anchor Docs:** `7-payment-app-cc.md`, `22-roles-permisos-capas-ux-fs.md`, `18-matriz-seguridad-compliance-fs.md`

---

## 1. Roles que interactuan con Payments

| Rol | Relacion con la app |
|---|---|
| `anonymous` | Sin acceso; el pago requiere identidad para garantias legales |
| `member` | Realiza pagos y gestiona sus metodos de pago y suscripcion |
| `admin` | Ve pagos del tenant; no puede acceder a datos de tarjeta |
| `owner` | Igual que admin; puede cancelar suscripciones |
| `staff` | Diagnostica pagos fallidos; procesa revisiones manuales |
| `superadmin` | Acceso total; unico que puede ejecutar reembolsos masivos |

---

## 2. Capa Publica (anonymous)

| Pantalla / Accion | Permitido | Restriccion |
|---|---|---|
| Pagina de precios generica | Si (via Home/Orchestrator) | Sin datos de pago real |
| Formulario de pago | No | Requiere sesion autenticada y orden activa |
| Webhooks de gateway (POST entrante) | Si (via endpoint firmado) | Solo con firma HMAC verificada del gateway |

---

## 3. Capa Privada por rol

| Pantalla / Accion | member | admin | owner |
|---|---|---|---|
| Ver checkout de la orden activa | Si | Si | Si |
| Pagar con tarjeta/PayPal | Si | Si | Si |
| Ver estado de pago (ok/fail/pending) | Si (propio) | Si | Si |
| Descargar recibo de pago | Si (propio) | Si | Si |
| Ver historial de pagos | Si (propio) | Si (tenant) | Si |
| Gestionar metodo de pago (agregar/borrar) | Si (propio) | No | No |
| Ver/gestionar suscripcion del tenant | No | Si | Si |
| Cancelar suscripcion | No | No | Si |
| Ver reportes de facturacion | No | Si | Si |
| Solicitar reembolso | Si (propio; flujo de soporte) | Si (notifica a staff) | Si |

---

## 4. Capa Admin Django (staff / superadmin)

| Modelo | staff (lectura) | staff (escritura) | superadmin |
|---|---|---|---|
| PaymentIntent | Si | Si (marcar revision manual) | CRUD completo |
| Subscription | Si | Si (cancelar, pausar) | CRUD completo |
| WebhookEvent | Si | Si (reprocess flag) | CRUD completo |
| Receipt | Si | No | Lectura + reenvio |

Restricciones criticas:
- Ningun rol tiene acceso a datos de tarjeta (manejados exclusivamente por el gateway).
- `Receipt` no se puede borrar; es registro fiscal permanente.
- Reembolsos masivos solo via `superadmin` con flujo de aprobacion.

---

## 5. Assets de Payments

| Asset | Operacion | member | admin | owner | staff | superadmin |
|---|---|---|---|---|---|---|
| Recibo PDF | Ver | Si (propio) | Si | Si | Si | Si |
| Recibo PDF | Reenviar por email | Si (propio) | Si | Si | Si | Si |
| Recibo PDF | Borrar | No | No | No | No | No (fiscal) |
| Reporte de pagos CSV | Exportar | No | Si (tenant) | Si | Si (cross-tenant) | Si |
| Certificados/llaves de webhook | Ver | No | No | No | No | Si |
| Certificados/llaves de webhook | Rotar | No | No | No | No | Si |
| Metodos de pago tokenizados | Ver (parcial) | Si (propio; ultimos 4 digitos) | No | No | No | No |
| Metodos de pago tokenizados | Borrar | Si (propio) | No | No | No | Si |

---

## 6. Notas de seguridad

- PCI DSS: ningun dato de tarjeta toca la base de datos del SaaS; todo se tokeniza via gateway.
- Los webhooks se validan por HMAC antes de procesarse; payloads invalidos se descartan con log.
- Recibos son inmutables una vez generados.
