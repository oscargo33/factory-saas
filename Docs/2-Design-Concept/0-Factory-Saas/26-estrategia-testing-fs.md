# Documento: Estrategia de Testing Transversal

**Versión del documento:** 1.0
**Última actualización:** 2026-03-16

**ID:** DC-26-FS
**Ubicacion:** `./Docs/2-Design-Concept/0-Factory-Saas/26-estrategia-testing-fs.md`
**Anchor Docs:** `DC-12-FS` (Service Layer), `DC-16-FS` (Contratos inter-app), `DC-13-FS` (Multi-tenancy)
**Backlog:** PB-021

---

## 1. Proposito

Define los estandares de testing que aplican a todas las apps de Factory-SaaS: tipos de tests, herramientas, cobertura minima, convencion de nombres, mocking de dependencias suaves y el CI gate que bloquea merges si no se cumplen los criterios.

Sin esta estrategia cada app implementa tests con criterios distintos, haciendo imposible medir la calidad global del sistema.

---

## 2. Piramide de Testing de la Factory

```
         /\
        /E2E\          — Menor cantidad, mayor costo
       /------\        — Tests de journey completo en browser
      /  Integ  \      — Tests de contratos entre apps
     /------------\    — Tests de flujos criticos (DB + Celery)
    /  Unit Tests  \   — Mayor cantidad, menor costo
   /----------------\  — Services, Selectors, modelos, utils
```

### Proporciones objetivo por app

| Tipo | % del total de tests | Ejecuta en |
|---|---|---|
| Unit | 70% | CI en cada PR |
| Integration | 25% | CI en cada PR |
| E2E | 5% | CI en merge a main (staging) |

---

## 3. Herramientas

| Herramienta | Uso | Version |
|---|---|---|
| `pytest` | Framework principal de tests | 8.x |
| `pytest-django` | Integracion con Django ORM y settings | 4.x |
| `pytest-cov` | Reporte de cobertura | 4.x |
| `factory_boy` | Fixtures de modelos (reemplaza fixtures de Django) | 3.x |
| `faker` | Datos falsos en factories | |
| `responses` / `httpretty` | Mock de HTTP externos (gateway, SES, La Central) | |
| `freezegun` | Congelar tiempo en tests de expiracion | |
| `playwright` | E2E en browser (solo para journeys criticos) | |
| `ruff` | Linter de codigo | |
| `black` | Formatter | |

---

## 4. Unit Tests

### 4.1. Que se testea

- **Services (`services.py`):** toda funcion de negocio con logica condicional.
- **Selectors (`selectors.py`):** queries con filtros complejos.
- **Modelos:** metodos custom (`clean()`, `save()` override, propiedades calculadas).
- **Utilities y helpers** de la app.

### 4.2. Que NO se testea unitariamente

- Vistas simples sin logica (solo renderizan template).
- Migraciones (no contienen logica por diseno — ver DC-23).
- Configuraciones de Django (`settings.py`).

### 4.3. Convencion de nombres

```
tests/
  unit/
    apps/
      orders/
        test_order_service.py      # tests de services.py
        test_order_selectors.py    # tests de selectors.py
        test_order_models.py       # tests de modelos
```

### 4.4. Patron de test unitario

```python
# tests/unit/apps/orders/test_order_service.py
import pytest
from apps.orders.services import create_order
from tests.factories import TenantFactory, UserFactory, ProductFactory

@pytest.mark.django_db
class TestCreateOrder:
    def test_creates_order_with_price_snapshot(self, tenant, user):
        product = ProductFactory(tenant=tenant, price=Decimal('99.00'))
        order = create_order(user_id=user.id, product_id=product.id, tenant_id=tenant.id)

        assert order.status == 'pending'
        assert order.price_snapshot['unit_price'] == '99.00'

    def test_raises_if_no_entitlement(self, tenant, user):
        product = ProductFactory(tenant=tenant)
        with pytest.raises(PermissionDenied):
            create_order(user_id=user.id, product_id=product.id, tenant_id=tenant.id)
```

---

## 5. Integration Tests

### 5.1. Que se testea

- **Contratos inter-app:** un servicio de App A invoca un contrato de App B y el resultado es correcto.
- **Flujos con base de datos real:** multi-tenant: que un tenant no ve datos de otro.
- **Flujos con Celery:** que una tarea se encola y produce el efecto esperado.
- **Webhooks:** que el endpoint recibe, valida HMAC y procesa correctamente.

### 5.2. Convencion de nombres

```
tests/
  contracts/
    test_order_price_snapshot.py   # ya existe
    test_outbox_and_telemetry.py   # ya existe
    test_payments_idempotency_fixture.py  # ya existe
    test_planmatrix_contract.py    # ya existe
    test_tenant_isolation.py       # a crear en Fase 3
    test_onboarding_flow.py        # a crear en Fase 4
```

### 5.3. Patron de test de contrato (soft-dependency)

```python
# tests/contracts/test_theme_fallback.py
import pytest
from unittest.mock import patch

@pytest.mark.django_db
class TestThemeFallback:
    def test_renders_fallback_if_theme_not_installed(self, client, tenant):
        with patch('django.apps.apps.is_installed', return_value=False):
            response = client.get(f'https://{tenant.slug}.factory-saas.com/')
            assert response.status_code == 200
            assert 'fallback_layout' in response.templates[0].name
```

### 5.4. Patron de aislamiento multi-tenant

```python
@pytest.mark.django_db
class TestTenantIsolation:
    def test_tenant_a_cannot_see_tenant_b_orders(self, tenant_a, tenant_b, user_a):
        OrderFactory(tenant=tenant_b)
        set_tenant_context(tenant_a)
        orders = Order.objects.all()
        assert orders.count() == 0  # tenant_a no ve ordenes de tenant_b
```

---

## 6. E2E Tests (Playwright)

### 6.1. Journeys cubiertos

Solo los journeys de mayor impacto comercial justifican el costo de E2E:

| Journey | Archivo |
|---|---|
| Onboarding completo (registro → primer uso) | `e2e/test_onboarding_journey.py` |
| Checkout y pago exitoso | `e2e/test_checkout_journey.py` |
| Crear y resolver ticket de soporte | `e2e/test_support_journey.py` |

### 6.2. Configuracion

- E2E corren contra el ambiente de staging (no contra `localhost`).
- Usan un tenant de prueba dedicado (`e2e_test_tenant`) reseteado antes de cada run.
- Se ejecutan solo en merge a `main`, no en PRs.

---

## 7. Factories (factory_boy)

Todas las apps deben tener un archivo `tests/factories.py` con sus factories. Convencion global:

```python
# tests/factories.py (global, importable desde cualquier test)
import factory
from apps.profiles.models import Tenant, User, Membership

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    email = factory.Faker('email')
    is_active = True

class TenantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tenant
    name = factory.Faker('company')
    slug = factory.Sequence(lambda n: f'tenant-{n}')
    status = 'active'

class MembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Membership
    user = factory.SubFactory(UserFactory)
    tenant = factory.SubFactory(TenantFactory)
    role = 'member'
```

---

## 8. Mocking de Dependencias Externas

### 8.1. Gateway de pagos (Stripe/PayPal)

```python
# En conftest.py o en el test directamente
import responses

@responses.activate
def test_payment_webhook():
    responses.add(responses.POST, 'https://api.stripe.com/v1/charges', json={'id': 'ch_test'})
    ...
```

### 8.2. Amazon SES / email

```python
# En settings de test
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# En el test
from django.core import mail
assert len(mail.outbox) == 1
assert mail.outbox[0].subject == 'Bienvenido'
```

### 8.3. Celery (tareas en tests)

```python
# En settings de test
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
```

---

## 9. Cobertura Minima Requerida (CI Gate)

| Alcance | Cobertura minima |
|---|---|
| Global del proyecto | 80% |
| `services.py` por app | 90% |
| `selectors.py` por app | 85% |
| Flujos criticos (payments, orders, auth) | 95% |

**Configuracion de `pytest.ini` (o `pyproject.toml`):**

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
addopts = "--cov=apps --cov-fail-under=80 --cov-report=term-missing"
testpaths = ["tests"]
```

**CI Gate:** El pipeline de GitHub Actions falla si la cobertura cae por debajo del minimo. Un PR no puede mergearse con el gate rojo.

---

## 10. Linters y Formatters (Pre-commit)

Configuracion de `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        additional_dependencies: [django-stubs]
```

---

## 11. DoD de este Documento

- [ ] Piramide de testing con proporciones definida.
- [ ] Herramientas especificadas con versiones.
- [ ] Convencion de nombres de archivos de test establecida.
- [ ] Patron de unit, integration y E2E documentado con ejemplos.
- [ ] Factory pattern global documentado.
- [ ] Mocking de dependencias externas (payments, email, Celery) especificado.
- [ ] Cobertura minima por alcance definida con CI gate configurado.
- [ ] Pre-commit config documentada.
- [ ] Indexado en `0-index.md` de Factory-SaaS global.
