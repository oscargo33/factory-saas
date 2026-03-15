
# Índice de Documentos de Diseño Global — Factory-SaaS

**ID:** DC-0-INDEX
**Ubicación:** `./Docs/2-Design-Concept/0-Factory-Saas/0-index.md`
**Referencia Core:** `0-factory_saas-cc.md`
**Versión:** 2.0 — Fase 1 Global Design completada
**Apellido de Trazabilidad:** **-fs**

---

Este índice lista todos los documentos de diseño de la infraestructura global de la Factory. Deben completarse en su totalidad antes de iniciar el diseño individual de cada app.

---

## Capa 0: Gestión y Dependencias

| # | Documento | ID | Estado |
|---|---|---|---|
| — | `1-checklist-factory-saas.md` | DC-1-FS | ✅ Activo (tracking) |
| — | `2-Core Automation-specs-fs.md` | DC-2-FS | ✅ Aprobado |
| — | `3-gestion-de-secretos-fs.md` | DC-3-FS | ✅ Aprobado |
| — | `4-estructura-de-carpetas-fs.md` | DC-4-FS | ✅ Aprobado |
| — | `5-configuracion-poetry-fs.md` | DC-5-FS | ✅ Aprobado |

## Capa 1: Entorno de Ejecución (Contenerización)

| # | Documento | ID | Estado |
|---|---|---|---|
| — | `6-dockerfile-maestro-fs.md` | DC-6-FS | ✅ Aprobado |
| — | `7-docker-compose-specs-fs.md` | DC-7-FS | ✅ Aprobado |
| — | `8-entrypoint-specs-fs.md` | DC-8-FS | ✅ Aprobado |

## Capa 2: Persistencia y Almacenamiento

| # | Documento | ID | Estado |
|---|---|---|---|
| — | `9-configuracion-postgresql-fs.md` | DC-9-FS | ✅ Aprobado |

## Capa 3: Orquestación y Entrada (Redes + Mensajería)

| # | Documento | ID | Estado |
|---|---|---|---|
| — | `10-gateway-nginx-fs.md` | DC-10-FS | ✅ Aprobado |
| — | `11-configuracion-redis-celery-fs.md` | DC-11-FS | ✅ Aprobado |

## Capa 4: Arquitectura de Software (Service Layer)

| # | Documento | ID | Estado |
|---|---|---|---|
| — | `12-patron-service-layer-fs.md` | DC-12-FS | ✅ Aprobado |

## Capa 5: Motor de Multi-Tenancy

| # | Documento | ID | Estado |
|---|---|---|---|
| — | `13-router-dinamico-esquemas-fs.md` | DC-13-FS | ✅ Aprobado |

## Capa 6: Base Visual y Frontend

| # | Documento | ID | Estado |
|---|---|---|---|
| — | `14-pipeline-tailwind-cotton-fs.md` | DC-14-FS | ✅ Aprobado |

## Capa 7: Telemetría y Control de La Central

| # | Documento | ID | Estado |
|---|---|---|---|
| — | `15-protocolo-comunicacion-central-fs.md` | DC-15-FS | ✅ Aprobado |

## Transversal: Contratos, Datos y Seguridad

| # | Documento | ID | Estado |
|---|---|---|---|
| — | `16-contratos-inter-app-fs.md` | DC-16-FS | ✅ Aprobado |
| — | `17-diccionario-datos-logico-fs.md` | DC-17-FS | ✅ Aprobado |
| — | `18-matriz-seguridad-compliance-fs.md` | DC-18-FS | ✅ Aprobado |

---

## Estado de la Fase 1 — Diseño Global

**Total documentos:** 18 (+ este índice = 19 archivos)
**Completos:** 18 / 18
**Estado:** ✅ FASE 1 DISEÑO GLOBAL CERRADA

---

## Siguiente Paso

Con el diseño global completado, el siguiente paso es el **diseño individual de cada app** (Fase 1 — App Design). Cada app tendrá su propia carpeta en `Docs/2-Design-Concept/` referenciando los documentos de esta base:

```
Docs/2-Design-Concept/
├── 0-Factory-Saas/      ← Diseño global (este directorio, CERRADO)
├── 1-Theme-App/         ← Siguiente a diseñar
├── 2-API-App/
├── 3-Profile-App/
├── 4-ProductOrchestrator-App/
├── 5-Marketing-App/
├── 6-Orders-App/
├── 7-Payment-App/
├── 8-Support-App/
└── 9-Home-App/
```