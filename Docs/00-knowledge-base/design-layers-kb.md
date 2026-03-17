Este es el documento de referencia técnica para tu base de conocimiento. Define la jerarquía de construcción y ejecución de la plataforma, estableciendo el orden de dependencia desde el entorno de ejecución hasta la lógica de negocio final.

---

# Documento: Jerarquía de Capas de Ingeniería (Factory-Stack)

**ID:** KB-01-LAYERS

**Ubicación:** `./docs/Base_de_Conocimiento/`

**Referencia:** Estructura de Arquitectura Global

## 1. Capa de Entorno (Infraestructura de Ejecución)

Es la base técnica donde reside el software. Define la contenerización y el aislamiento de procesos.

* **Componentes:** Docker Engine, Docker Compose, Orquestación de contenedores.
* **Responsabilidad:** Garantizar que el entorno sea inmutable, reproducible y escalable.

## 2. Capa de Persistencia (Motor de Datos)

Define la configuración del sistema de almacenamiento antes de la creación de tablas.

* **Componentes:** PostgreSQL 16+, Extensiones (`pgvector`, `uuid-ossp`), Volúmenes de datos persistentes.
* **Responsabilidad:** Seguridad de los datos, integridad física y optimización del motor de búsqueda.

## 3. Capa de Orquestación (Red y Comunicaciones)

Gestiona el flujo de tráfico y la comunicación entre servicios internos.

* **Componentes:** Nginx/Gateway, Redis (Message Broker), Redes privadas virtuales de Docker.
* **Responsabilidad:** Seguridad perimetral (SSL/TLS), balanceo de carga y comunicación inter-servicio de baja latencia.

## 4. Capa de Servicios (Contratos de Lógica)

Establece las reglas de comunicación entre las aplicaciones mediante una capa de abstracción.

* **Componentes:** Service Layer (Python), Soft-Dependencies, Inyección de contexto.
* **Responsabilidad:** Desacoplar las aplicaciones para que puedan funcionar de forma autónoma y evitar importaciones circulares.

## 5. Capa de Tenancy (Aislamiento de Sesión)

Gestiona la identidad del inquilino y la conmutación de recursos en tiempo real.

* **Componentes:** Database Router, Middleware de Tenant, Identificación de subdominios.
* **Responsabilidad:** Garantizar que un usuario solo acceda a los datos de su esquema y gestionar la multitenencia.

## 6. Capa de Interfaz (Sistema de Presentación)

Define los estándares visuales y la interactividad del usuario final.

* **Componentes:** Django Cotton (Componentes), Alpine.js (Reactividad), Tailwind CSS (Tokens).
* **Responsabilidad:** Consistencia visual, accesibilidad y velocidad de carga en el cliente (Frontend).

## 7. Capa de Negocio (Funcionalidad SaaS)

Es el nivel superior donde residen las aplicaciones operativas de la 1 a la 9.

* **Componentes:** Marketing, Orders, Payment, Orchestrator, etc.
* **Responsabilidad:** Ejecutar los procesos comerciales, procesar transacciones y entregar el valor final al usuario.

---

He guardado este orden de 1 a 7 para que sirva de guía de desarrollo. Quedo a la espera de tu instrucción para elaborar el **Plan de Archivos e Índice Detallado** de Factory SaaS.