# Documento: Estrategia de Migraciones de Base de Datos

**Versión del documento:** 1.0
**Última actualización:** 2026-03-16

**ID:** DC-23-FS
**Ubicacion:** `./Docs/2-Design-Concept/0-Factory-Saas/23-estrategia-migraciones-db-fs.md`
**Anchor Docs:** `DC-9-FS` (PostgreSQL), `DC-13-FS` (Router de esquemas), `DC-8-FS` (Entrypoint)
**Backlog:** PB-018

---

## 1. Proposito

Este documento define la estrategia completa para ejecutar, gobernar y revertir migraciones de base de datos en un entorno multi-tenant de schema-per-tenant. Es el documento de referencia obligatorio para cualquier cambio de modelo Django en produccion.

El problema central: en Factory-SaaS, `manage.py migrate` debe ejecutarse sobre el schema `public` (entidades globales) y sobre N schemas de tenant (entidades de negocio). Un error en produccion puede corromper todos los tenants simultaneamente.

---

## 2. Clasificacion de Migraciones por Schema

### 2.1. Migraciones de Schema `public`

Afectan a las tablas globales del sistema. Son las mas criticas porque impactan a todos los usuarios sin excepcion.

**Apps que generan migraciones en `public`:**
- `apps.profiles` → User, Tenant, Membership
- `apps.telemetry` → AuditLog, TelemetryEvent, PendingMetrics
- `django.contrib.auth`, `django.contrib.contenttypes`, `django.contrib.sessions`

**Comando:**
```bash
python manage.py migrate --schema=public
```

### 2.2. Migraciones de Schema `tenant_{slug}`

Afectan a las tablas de negocio de cada tenant individualmente.

**Apps que generan migraciones en tenant schemas:**
- `apps.orchestrator` → Product, Vertical, Entitlement
- `apps.marketing` → Campaign, Coupon, Banner
- `apps.orders` → Cart, Order, OrderItem, PriceSnapshot
- `apps.payments` → PaymentIntent, Subscription, Receipt
- `apps.support` → Ticket, TicketMessage, KnowledgeArticle

**Comando (por tenant individual):**
```bash
python manage.py migrate --schema=tenant_acme
```

**Comando (todos los tenants, via script):**
```bash
python manage.py migrate_all_tenants  # custom management command — ver Seccion 4
```

### 2.3. Migraciones del App Theme

`apps.theme` (ThemeConfig, GlossaryTerm) reside en `public` para ser accesible transversalmente. Sus migraciones van junto a las de `public`.

---

## 3. Flujo de Migraciones por Ambiente

### 3.1. Desarrollo Local

```
1. Desarrollador crea/modifica modelo → genera migration con:
   python manage.py makemigrations apps.<nombre_app>

2. Aplica en local:
   python manage.py migrate --schema=public
   python manage.py migrate --schema=tenant_dev  (schema de prueba local)

3. Verifica que no hay conflictos:
   python manage.py showmigrations
```

### 3.2. Staging

```
1. CI ejecuta en pipeline antes de deploy:
   python manage.py migrate --check   (falla si hay migraciones sin aplicar)

2. Deploy script aplica en orden:
   a. python manage.py migrate --schema=public
   b. python manage.py migrate_all_tenants --verbosity=1

3. Si alguna falla → pipeline se detiene, se ejecuta rollback (Seccion 5).
```

### 3.3. Produccion (Zero-Downtime)

El orden es obligatorio y no negociable:

```
Paso 1: Backup completo (ANTES de cualquier migración)
  → pg_dump -Fc factory_db > backup_YYYYMMDD_HHMMSS.dump

Paso 2: Desplegar nueva version del codigo en modo "backward compatible"
  → La nueva version del codigo DEBE funcionar con el schema VIEJO.

Paso 3: Aplicar migraciones de public
  → python manage.py migrate --schema=public

Paso 4: Aplicar migraciones de todos los tenant schemas
  → python manage.py migrate_all_tenants

Paso 5: Verificar salud del sistema
  → Healthchecks + smoke tests automaticos

Paso 6: Si todo ok → activar el nuevo comportamiento (feature flag si aplica)
  → Si falla → ejecutar rollback (Seccion 5)
```

---

## 4. Custom Management Command: `migrate_all_tenants`

Este comando debe implementarse en `apps/core/management/commands/migrate_all_tenants.py`.

**Comportamiento:**
1. Consulta todos los `Tenant` con `status='active'` del schema `public`.
2. Para cada tenant: activa el `search_path` con `set_search_path(tenant.slug)` y ejecuta `call_command('migrate')`.
3. Registra en `AuditLog` cada migracion aplicada con `tenant_id`, `migration_name`, `applied_at`, `applied_by`.
4. En caso de error en un tenant: registra el error, continua con el siguiente (no detiene el proceso completo), y al final devuelve un reporte de tenants fallidos.

**Opciones del comando:**
```
--tenant=<slug>         Migrar solo un tenant especifico
--dry-run               Mostrar que se ejecutaria sin aplicar
--stop-on-error         Detener al primer error (modo conservador para produccion)
--verbosity=<0|1|2>     Nivel de detalle en consola
```

---

## 5. Procedimiento de Rollback

### 5.1. Rollback de una Migracion Especifica

```bash
# Revertir a la migracion anterior en schema public
python manage.py migrate apps.orders 0005 --schema=public

# Revertir en todos los tenants (con script)
python manage.py migrate_all_tenants --target-migration=apps.orders.0005
```

### 5.2. Rollback de Emergency (Restore de Backup)

Usar solo si el rollback por migracion no es viable:

```bash
# Detener la aplicacion
docker compose stop web celery

# Restaurar backup
pg_restore -Fc -d factory_db backup_YYYYMMDD_HHMMSS.dump

# Reactivar version anterior del codigo
git checkout <tag-version-anterior>
docker compose up -d

# Verificar salud
docker compose ps && curl http://localhost/health/
```

> El backup tomado en Paso 1 del flujo de produccion es el unico punto de recuperacion garantizado.

---

## 6. Governance de Migraciones

### 6.1. Reglas de Creacion

| Regla | Descripcion |
|---|---|
| Sin datos en migraciones | Las migraciones de schema NUNCA incluyen `RunPython` con datos de negocio. Los datos van en data migrations separadas. |
| Backward compatible primero | Toda migracion que rompe compatibilidad (drop de columna, rename) debe tener una migracion previa que haga la columna nullable o equivalente. |
| Sin `RunSQL` sin aprobacion | `RunSQL` requiere revision de arquitecto antes de mergear. |
| Nombres descriptivos | `makemigrations --name=agregar_campo_slug_a_tenant`. |
| Una app por migration file | No combinar cambios de multiples apps en una sola migracion. |

### 6.2. Checklist de Code Review para Migraciones

Antes de aprobar un PR que incluya migraciones:
- [ ] La migracion no contiene datos de negocio embebidos.
- [ ] Si hay `ALTER TABLE`, se verifica que es backward compatible.
- [ ] El campo nuevo tiene `null=True` o `default=` definido.
- [ ] El `migrate --check` pasa en CI.
- [ ] Si afecta tablas criticas (Order, Payment, Tenant), existe plan de rollback documentado en el PR.

### 6.3. Migraciones Falsas (--fake)

Se usa `--fake` solo en dos casos documentados:
1. **Squash de migraciones:** tras ejecutar `squashmigrations`, los tenants ya existentes se marcan con `--fake` porque el schema ya esta al dia.
2. **Migracion inicial de un tenant nuevo:** el schema se crea con `CREATE SCHEMA` y las tablas con un script template; luego se marca `--fake-initial` para alignar el estado con Django.

---

## 7. Squash de Migraciones

Cuando una app acumula mas de 30 migraciones, se ejecuta un squash para reducir la deuda tecnica:

```bash
python manage.py squashmigrations apps.orders 0001 0030
```

**Proceso post-squash:**
1. Aplicar la squashed migration regularmente en nuevos entornos.
2. En tenants/ambientes existentes: `migrate --fake apps.orders 0001_squashed_0030`.
3. Guardar el listado de tenants donde se aplico el fake en `AuditLog`.
4. Una vez todos los tenants confirmados: eliminar las migraciones originales del repo.

---

## 8. Monitoreo de Estado de Migraciones

En cada ambiente debe existir un endpoint de healthcheck que incluya el estado de migraciones:

```
GET /health/
{
  "status": "ok",
  "migrations_pending": 0,
  "tenants_pending": []
}
```

Si `migrations_pending > 0`, el healthcheck devuelve HTTP 503 y bloquea el deploy.

---

## 9. Integracion con DC-8-FS (Entrypoint)

El `entrypoint.sh` ejecuta en el arranque del contenedor:

```bash
# Solo en los roles web y worker, no en el scheduler
if [ "$FACTORY_ROLE" = "web" ]; then
  echo "Aplicando migraciones de public..."
  python manage.py migrate --schema=public --noinput

  echo "Aplicando migraciones de tenants..."
  python manage.py migrate_all_tenants --stop-on-error --verbosity=1
fi
```

En produccion, la variable `AUTO_MIGRATE=false` desactiva este comportamiento y las migraciones se aplican manualmente via el flujo de la Seccion 3.3.

---

## 10. DoD de este Documento

- [ ] Flujo de migraciones para los 3 ambientes documentado.
- [ ] `migrate_all_tenants` especificado con opciones y comportamiento de error.
- [ ] Procedimiento de rollback paso a paso disponible.
- [ ] Governance checklist para Code Review definido.
- [ ] Integracion con entrypoint.sh documentada.
- [ ] Indexado en `0-index.md` de Factory-SaaS global.
