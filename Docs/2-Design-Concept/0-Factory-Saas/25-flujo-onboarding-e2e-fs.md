# Documento: Flujo de Onboarding End-to-End

**Versión del documento:** 1.0
**Última actualización:** 2026-03-16

**ID:** DC-25-FS
**Ubicacion:** `./Docs/2-Design-Concept/0-Factory-Saas/25-flujo-onboarding-e2e-fs.md`
**Anchor Docs:** `DC-21-FS` (producto visible), `DC-22-FS` (RBAC), `DC-24-FS` (notificaciones), `DC-19-FS` (PlanMatrix)
**Backlog:** PB-020

---

## 1. Proposito

Define el journey completo desde que un usuario anonimo llega al SaaS hasta que completa su primer uso real del producto. Este es el flujo de mayor impacto comercial del sistema: cada friccion en este journey reduce la conversion.

---

## 2. Mapa del Journey Completo

```
[ETAPA 0] Usuario anonimo llega al sitio
    │
    ▼
[ETAPA 1] Descubrimiento: Home (App 9)
    │  Ve: landing, propuesta de valor, precios, features
    │  Accion: hace clic en "Empezar gratis" o "Ver precios"
    ▼
[ETAPA 2] Registro de identidad (App 3 Profiles)
    │  Completa: email + password
    │  Sistema: crea User global, envia email user.registered
    │  Estado post-etapa: User activo, sin tenant
    ▼
[ETAPA 3] Confirmacion de email
    │  Recibe: email con link de confirmacion (expira 24h)
    │  Accion: hace clic en link
    │  Sistema: activa User, envia email user.email_confirmed
    │  Estado post-etapa: User verificado
    ▼
[ETAPA 4] Creacion del primer Tenant
    │  Pantalla: "Crea tu espacio de trabajo"
    │  Completa: nombre del negocio (slug auto-generado)
    │  Sistema: crea Tenant + schema PostgreSQL + Membership(role=owner)
    │  Estado post-etapa: Tenant activo, usuario es owner
    ▼
[ETAPA 5] Seleccion de Plan
    │  Pantalla: pricing table de App 4 (Product Orchestrator)
    │  Usuario selecciona plan (free, starter, pro, enterprise)
    │  Para plan free: va directo a Etapa 7
    │  Para planes de pago: va a Etapa 6
    ▼
[ETAPA 6] Checkout y Pago (App 7 Payments)
    │  Pantalla: formulario de pago (Stripe hosted o embedded)
    │  Pago exitoso: crea Subscription + genera Receipt
    │  Sistema: envia payment.succeeded, subscription.created
    │  Estado post-etapa: suscripcion activa
    ▼
[ETAPA 7] Provision de Entitlements (App 4 Orchestrator)
    │  Automatico: PlanMatrix determina que capacidades corresponden al plan
    │  Sistema: crea Entitlement(s) para el tenant
    │  Estado post-etapa: tenant tiene permisos de uso del producto
    ▼
[ETAPA 8] Configuracion inicial del Tenant (opcional, recomendado)
    │  Pantalla: "Personaliza tu espacio" (App 1 Theme)
    │  Acciones opcionales: subir logo, elegir colores, configurar idioma
    │  Skip disponible: puede hacerse despues
    ▼
[ETAPA 9] Primer uso del Product Core
    │  Pantalla: dashboard principal (App 3 Profiles — dashboard agregado)
    │  Ve: capacidades activas, accesos directos al producto
    │  Realiza primera accion de valor (depende del producto)
    │  CONVERSION COMPLETADA
```

---

## 3. Estados del Onboarding por Etapa

| Etapa | Estado del User | Estado del Tenant | Entitlements | Suscripcion |
|---|---|---|---|---|
| 0 — Anonimo | N/A | N/A | N/A | N/A |
| 1 — Descubrimiento | N/A | N/A | N/A | N/A |
| 2 — Registro | `is_active=False` | N/A | N/A | N/A |
| 3 — Email confirmado | `is_active=True` | N/A | N/A | N/A |
| 4 — Tenant creado | `is_active=True` | `status=active` | Ninguno | N/A |
| 5 — Plan seleccionado (free) | Activo | Activo | Pendiente provision | N/A |
| 6 — Pago exitoso | Activo | Activo | Pendiente provision | `status=active` |
| 7 — Entitlements provisionados | Activo | Activo | `status=active` | Activo |
| 8 — Configuracion inicial | Activo | Activo + Theme config | Activo | Activo |
| 9 — Primer uso | **CONVERTIDO** | Activo | Activo | Activo |

---

## 4. Pantallas por Etapa (Referencia a Diseño)

| Etapa | App | Pantalla | Referencia de diseno |
|---|---|---|---|
| 1 | Home (App 9) | Landing principal | HM-10-PV, HM-11-RBAC |
| 2 | Profiles (App 3) | Formulario de registro | PR-10-PV, PR-11-RBAC |
| 3 | Profiles (App 3) | Pagina de confirmacion de email | PR-10-PV |
| 4 | Profiles (App 3) | Creacion de tenant ("espacio de trabajo") | PR-10-PV |
| 5 | Orchestrator (App 4) | Pricing table / seleccion de plan | PO-10-PV |
| 6 | Payments (App 7) | Checkout / formulario de pago | PY-11-PV, PY-12-RBAC |
| 7 | Orchestrator (App 4) | Pantalla "Tu plan esta activo" | PO-10-PV |
| 8 | Theme (App 1) | Wizard de configuracion inicial | TH-9-PV |
| 9 | Profiles (App 3) | Dashboard principal del tenant | PR-10-PV |

---

## 5. Notificaciones por Etapa

| Etapa | Event Type | Destinatario | Cuando |
|---|---|---|---|
| 2 | `user.registered` | Nuevo usuario | Inmediato tras registro |
| 3 | `user.email_confirmed` | Nuevo usuario | Inmediato tras confirmacion |
| 4 | (ninguna) | — | — |
| 6 | `payment.succeeded` | Owner | Inmediato tras pago |
| 6 | `payment.receipt_generated` | Owner | Tras generar recibo |
| 6 | `subscription.created` | Owner | Tras crear suscripcion |
| 7 | (ninguna visible; log interno) | — | — |
| 9 | `onboarding.completed` | Owner | Primer uso detectado (telemetria) |

---

## 6. Manejo de Errores y Estados de Abandono

| Punto de abandono | Accion del sistema |
|---|---|
| Usuario registrado pero no confirmo email | Reenvio automatico a las 24h. Expira a las 48h. |
| Usuario confirmo pero no creo tenant | Pantalla de bienvenida muestra CTA de creacion al siguiente login. |
| Usuario selecciono plan de pago pero no pago | Orden queda en estado `pending` por 24h. Luego se cancela. No hay Entitlements. |
| Pago fallo | App Payments muestra pantalla de error con opcion de reintentar. Email `payment.failed`. |
| Provision de Entitlements fallo | Error critico: alerta a staff via `system.payment_review_required`. User ve mensaje "Activando tu plan..." y se reintenta en background. |

---

## 7. Plan Free (Sin Pago)

El plan free salta la Etapa 6 (checkout) completamente:

```
Etapa 5 (selecciona Free) → Etapa 7 (provision automatica de entitlements limitados)
```

Entitlements del plan free: definidos en `PlanMatrix` con `allowed_products` y `max_usage` restrictivos.

---

## 8. Flujo de Invitacion (Onboarding de Miembros)

Para usuarios invitados a un tenant existente (no crean su propia cuenta desde Home):

```
Owner/Admin envia invitacion (App 3)
    │  Sistema: crea InvitationToken (expira 48h), envia tenant.member_invited
    ▼
Invitado recibe email → hace clic en link
    │  Si ya tiene cuenta: va directamente a Etapa 4 (aceptar Membership)
    │  Si no tiene cuenta: va a Etapa 2 (registro) con tenant pre-asociado
    ▼
Acepta invitacion → crea Membership(role=member)
    │  Sistema: envia tenant.invitation_accepted al admin
    ▼
Accede al dashboard del tenant como member
```

---

## 9. Metricas de Conversion a Trackear (Telemetria)

| Paso | Event de telemetria | Calcula |
|---|---|---|
| Llegada a landing | `home.landing_viewed` | Visitantes unicos |
| Clic en CTA | `home.cta_clicked` | CTR de landing |
| Registro completado | `user.registered` | Conversion landing → registro |
| Email confirmado | `user.email_confirmed` | Tasa de verificacion |
| Tenant creado | `tenant.created` | Activation rate |
| Plan seleccionado | `plan.selected` | Preferencia de plan |
| Pago exitoso | `payment.succeeded` | Conversion a pago |
| Primer uso | `product.first_use` | Time-to-value |

---

## 10. DoD de este Documento

- [ ] Journey de 9 etapas documentado con estados por etapa.
- [ ] Pantallas de diseno referenciadas por etapa.
- [ ] Notificaciones por etapa mapeadas a DC-24 event types.
- [ ] Manejo de abandono y errores cubierto.
- [ ] Flujo de invitacion documentado.
- [ ] Metricas de conversion definidas para telemetria.
- [ ] Indexado en `0-index.md` de Factory-SaaS global.
