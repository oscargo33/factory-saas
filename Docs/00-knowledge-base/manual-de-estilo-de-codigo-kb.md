# Manual de Estilo de Código: Factory SaaS (IA-Ready)

Este manual define los estándares de codificación para garantizar que cada aplicación sea **autónoma, resiliente y modular**.

## 1. Estructura de Archivos Estándar por App

Cada aplicación debe seguir estrictamente esta organización de archivos para que la IA sepa dónde leer y escribir:

* `services.py`: Lógica de **escritura** (crear, actualizar, borrar). Único punto de entrada para otras apps.
* `selectors.py`: Lógica de **lectura** (filtros complejos, queries optimizadas).
* `templates/cotton/`: Componentes UI atómicos de la aplicación.
* `templates/[app]/fallback/`: Layouts mínimos para degradación graciosa.

## 2. Protocolo de Comunicación Inter-App (Service Layer)

**Regla de Oro:** Prohibido importar modelos de otra app (`from app_b.models import ...` es ERROR).

### Patrón de Invocación Resiliente:

Para que la IA genere código que no se rompa si falta una app, debe usar este bloque estandarizado:

```python
from django.apps import apps

def get_external_service(app_label, service_name):
    """Retorna el servicio si la app está instalada, de lo contrario un Mock funcional."""
    if apps.is_installed(app_label):
        # Importación dinámica para evitar errores de carga
        module = __import__(f"{app_label}.services", fromlist=[service_name])
        return getattr(module, service_name)()
    return None # O un objeto Mock con métodos que devuelvan valores neutros

```

## 3. Estándar de Componentes (Cotton + Alpine.js)

Al pedirle a la IA que cree un componente visual, debe seguir esta estructura para asegurar el *look and feel* y la autonomía:

```html
<div x-data="{ open: false }" class="p-4 {{ attrs.class }}">
    <button @click="open = !open" class="bg-[var(--color-primary)] text-white">
        {{ title }}
    </button>
    
    <div x-show="open" x-transition>
        {{ slot }}
    </div>
</div>

```

## 4. Manejo de "Valores Neutros" (Soft-Dependency)

Cuando la IA escriba lógica que dependa de otra app, debe implementar siempre un **Fallback**:

| Si la IA pide... | Fallback si la App no está / falla: |
| --- | --- |
| **Precio/Descuento** | Devolver `Decimal('0.00')` |
| **Permiso/Acceso** | Devolver `False` (Seguridad primero) |
| **Traducción** | Devolver la `Key` original o texto en inglés |
| **Identidad (Logo)** | Devolver un `placeholder.svg` local |

## 5. El "Prompt Maestro" para tu IA

Copia y pega este texto cada vez que inicies un chat con una IA para desarrollar una app de la Factory:

> "Actúa como un Senior Django Developer. Vamos a trabajar en la App **[Nombre de la App]** de la **Factory SaaS**.
> **Reglas críticas:**
> 1. Sigue el **Service Layer Pattern**: toda lógica de negocio en `services.py`.
> 2. Implementa **Soft-Dependencies**: si usas servicios de otra app, verifica si está instalada con `apps.is_installed` y usa valores de respaldo neutros.
> 3. **UI Resiliente:** Usa **Django Cotton** y **Alpine.js**. Si la App 'Theme' no está, usa el layout básico de la carpeta `fallback`.
> 4. **No importes modelos** de otras aplicaciones directamente. Usa importaciones dinámicas dentro de los métodos de servicio."
> 
> 

---

## 6. Checklist de Validación para la IA

Antes de aceptar el código que la IA te entregue, verifica:

* [ ] ¿El código usa `try/except` o `is_installed` al llamar a otras apps?
* [ ] ¿Hay lógica de negocio en las `views.py`? (Si la hay, dile que la mueva a `services.py`).
* [ ] ¿El componente Cotton usa variables CSS (`var(--...)`) para los colores?
* [ ] ¿Existe un `fallback_layout.html` básico en la carpeta de templates?

