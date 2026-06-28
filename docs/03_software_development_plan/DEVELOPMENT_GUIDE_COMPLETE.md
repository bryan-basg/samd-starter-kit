# Guía de Desarrollo Completa

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v0.1 · **Fecha:** 2026-01-01

> Plantilla del SaMD Starter Kit. Reemplazá los comandos placeholder por los reales de tu stack.

---

## 1. Setup del entorno

| Requisito | Valor |
|---|---|
| Frontend | {{FRONTEND_STACK}} |
| Backend | {{BACKEND_STACK}} |
| Base de datos | {{DB_STACK}} |
| Cloud | {{CLOUD_STACK}} |
| Gestor de secretos | <Secret Manager / Vault / .env local> |

```bash
# 1. Clonar e instalar dependencias
git clone <repo> && cd {{PROJECT_NAME}}
# Frontend
<comando-instalar-deps-frontend>      # ej. npm ci
# Backend (entorno aislado obligatorio)
<crear-entorno-virtual> && <activar>  # ej. python -m venv venv && source venv/bin/activate
<comando-instalar-deps-backend>       # ej. pip install -r requirements.txt

# 2. Variables de entorno (NUNCA commitear secretos reales)
cp .env.example .env                  # completar valores locales

# 3. Servicios locales (BD, emuladores, etc.)
<comando-levantar-servicios-locales>
```

---

## 2. Comandos core

```bash
# Desarrollo
<dev-frontend>          # ej. npm run dev
<dev-backend>           # ej. uvicorn app.main:app --reload

# Tests
<test-frontend>         # ej. npm run test
<test-backend>          # ej. pytest
<cobertura>             # ej. pytest --cov  (umbral según política)
<tipos>                 # ej. mypy . / tsc --noEmit

# Migraciones
<crear-migracion>       # ej. alembic revision --autogenerate
<aplicar-migracion>     # ej. alembic upgrade head  (MANUAL solo para recuperación)

# CI local pre-push
<ci-local>              # ej. bash scripts/run_local_ci.sh

# Stack de calidad SaMD (lentos — correr cuando aplique, piden OK por costo)
<mutation>              # mutation testing (frontend/backend)
<sast>                  # análisis estático de seguridad
<dast>                  # análisis dinámico
<deps-cve>              # escaneo de CVEs en dependencias
```

---

## 3. Estándares de backend

- **Identidad solo desde token verificado.** Nunca aceptar `id` de sujeto desde body o query.
- **Asincronía máxima**: prohibido I/O bloqueante; usar primitivas async.
- **Tipado estricto**: prohibido el tipo dinámico/`any`; validación de esquemas en frontera.
- **Errores empáticos**: nunca devolver tracebacks, SQL, metadatos internos o logs técnicos al cliente; solo mensaje claro + código HTTP correcto.
- **Cifrado en reposo** de campos sensibles; clave gestionada por el gestor de secretos, nunca hardcodeada ni reutilizada.
- **Auditoría**: persistir mutaciones (POST/PUT/PATCH/DELETE) para trazabilidad; lecturas a logs estructurados.
- **`.env.example` cubre todo el código vivo**: variable nueva en config → agregarla con comentario.

## 4. Estándares de frontend

- **Offline-first**: toda mutación pasa por el almacén local → outbox → sync. Nunca saltearlo.
- **Cache/fetch** vía la librería de data-fetching estándar del proyecto.
- **Accesibilidad WCAG 2.1 AA**: etiquetas semánticas + ARIA correctas; contraste verificado; respetar `prefers-reduced-motion` incondicionalmente.
- **Componentes canónicos**: reusar el modal/diálogo base; prohibido crear overlays nuevos.
- **Mensajes al usuario** claros y empáticos, sin jerga técnica; toasts con `id` único anti-flood.

---

## 5. Definition of Done

Una tarea está "lista" solo si cumple TODO:

- [ ] Código tipado, sin warnings nuevos respecto al techo del repo.
- [ ] Tests vinculados escritos (con aserciones reales, no de humo) y **verdes**; números reportados.
- [ ] Análisis de impacto hecho: todos los consumidores del símbolo revisados/actualizados.
- [ ] Fail-safe verificado para los modos de fallo del cambio.
- [ ] Sin tracebacks ni PII/PHI expuestos al cliente ni a logs.
- [ ] Accesibilidad verificada (si tocó UI).
- [ ] Trazabilidad: REQ/Risk + `archivo:línea` + nombre de test.
- [ ] Documentación actualizada junto con el cambio (Master Map / deuda / RFC según aplique).
- [ ] Boy Scout: al menos un pedazo de deuda del archivo tocado quedó más limpio.

---

## 6. Flujo de Pull Request

1. **Rama** desde la rama principal; nunca commitear directo a la principal.
2. **Commits atómicos**; mensaje describe el qué y el porqué.
3. **CI local** verde antes de abrir PR.
4. **PR** describe: cambio, impacto, tests corridos (números), trazabilidad, riesgos.
5. **Revisión**: al menos un revisor; cambios clínicos/seguridad requieren **revisión adversarial**.
6. **Auditoría** del changeset según `AUDIT_PROTOCOL.md` si toca capa regulada.
7. **Merge** tras aprobación; **deploy y push a remoto solo con OK explícito del propietario**.

---

## 7. Versionado de este documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v0.1 | 2026-01-01 | {{OWNER}} | Plantilla inicial |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
