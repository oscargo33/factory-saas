# Documento: Roles, Permisos y Capas — App 9 Home

**Versión del documento:** 1.0.0
**Última actualización:** 2026-03-16

**ID:** HM-11-RBAC
**Ubicacion:** `./Docs/2-Design-Concept/9-Home-App/11-roles-permisos-capas-home-hm.md`
**Anchor Docs:** `9-home-app-cc.md`, `22-roles-permisos-capas-ux-fs.md`

---

## 1. Roles que interactuan con Home

| Rol | Relacion con la app |
|---|---|
| `anonymous` | Audiencia principal; ve la landing, precios y features |
| `authenticated` | Redirigido al dashboard de su tenant tras login |
| `admin` / `owner` | Puede configurar contenido editorial del tenant via admin |
| `staff` | Gestiona SEO y contenido global de la fabrica |
| `superadmin` | Control total de landing pages y configuracion SEO global |

---

## 2. Capa Publica (anonymous)

| Pantalla / Accion | Permitido | Restriccion |
|---|---|---|
| Landing page principal | Si | Carga con CSS base si Theme falla |
| Pagina de precios/features | Si | Precios del catalogo publico; sin datos de entitlements |
| CTAs (registro, login) | Si | Redirigen a Profiles |
| Sitemap XML | Si | Solo rutas publicas |
| Busqueda interna | Si | Solo contenido publico indexado |
| Pagina de error 404/500 | Si | Paginas de error con fallback visual |

---

## 3. Capa Privada por rol

| Pantalla / Accion | authenticated | admin | owner |
|---|---|---|---|
| Ver landing publica | Si (puede ir al dashboard) | Si | Si |
| Ser redirigido al dashboard | Si | Si | Si |
| Editar hero section del tenant | No | Si | Si |
| Editar pricing table del tenant | No | Si | Si |
| Publicar cambios de landing | No | Si | Si |
| Configurar metadatos SEO del tenant | No | Si | Si |
| Ver metricas de conversion (CTA clicks) | No | Si | Si |
| Gestionar testimoniales y feature blocks | No | Si | Si |

---

## 4. Capa Admin Django (staff / superadmin)

| Modelo | staff (lectura) | staff (escritura) | superadmin |
|---|---|---|---|
| LandingPage | Si | Si | CRUD completo |
| HeroSection | Si | Si | CRUD completo |
| SEOConfig | Si | Si | CRUD completo |
| Testimonial / FeatureBlock | Si | Si | CRUD completo |

Restricciones criticas:
- Cambios en `SEOConfig` global solo pueden hacerlos `staff` y `superadmin`.
- El historial de versiones de `LandingPage` se mantiene para rollback; no se borra.

---

## 5. Assets de Home

| Asset | Operacion | anonymous | authenticated | admin | owner | staff | superadmin |
|---|---|---|---|---|---|---|---|
| Imagenes de hero y features | Ver | Si | Si | Si | Si | Si | Si |
| Imagenes de hero y features | Cargar/reemplazar | No | No | Si | Si | Si | Si |
| Imagenes de hero y features | Borrar | No | No | No | Si | Si | Si |
| Sitemap XML generado | Ver | Si | Si | Si | Si | Si | Si |
| Configuracion SEO (JSON-LD raw) | Ver | No | No | Si | Si | Si | Si |
| Configuracion SEO (JSON-LD raw) | Editar | No | No | Si | Si | Si | Si |
| Metricas de conversion | Exportar | No | No | Si | Si | Si (cross) | Si |
| Videos/media embebidos | Ver | Si | Si | Si | Si | Si | Si |
| Videos/media embebidos | Cargar/borrar | No | No | Si | Si | Si | Si |

---

## 6. Notas de seguridad

- El contenido de landing se sanitiza antes de renderizarse para prevenir XSS.
- Los CTAs no exponen parametros internos de tenant en URLs publicas.
- Las metricas de conversion no incluyen fingerprinting ni PII.
