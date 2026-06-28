# Visión de Arquitectura

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v0.1 · **Fecha:** 2026-01-01

> Plantilla del SaMD Starter Kit. Reemplazá los marcadores `{{...}}` y ajustá el diagrama a tu topología real.

---

## 1. Principios de arquitectura

1. **Offline-first**: toda mutación de datos pasa primero por un almacén local (cola/outbox) → sincronización. Nunca eludir el motor de sincronización.
2. **Identidad desde el token**: la identidad del sujeto se deriva exclusivamente del token verificado, nunca de un `id` recibido en body o query.
3. **Fail-safe explícito** (ISO 14971): el fallo degrada de forma segura y visible.
4. **Asincronía**: I/O no bloqueante en el backend.
5. **Tipado estricto y errores empáticos**: sin tracebacks ni metadatos internos hacia el cliente.

---

## 2. Diagrama de alto nivel

```
            ┌─────────────────────────────────────────────────────────┐
            │  CLIENTE (offline-first)  ──  {{FRONTEND_STACK}}         │
            │                                                         │
            │   UI ──► Cache/Query ──► Almacén local ──► Outbox ──┐    │
            │    ▲                          (IndexedDB/SQLite)    │    │
            │    └──────────── render ◄──── Sync engine ◄─────────┘    │
            └──────────────────────────────┬──────────────────────────┘
                                           │  HTTPS + token verificado
                                           ▼
            ┌─────────────────────────────────────────────────────────┐
            │  BACKEND (API + lógica)  ──  {{BACKEND_STACK}}           │
            │   Auth ─► Routers ─► Services ─► Audit middleware        │
            │     │         │           │                              │
            │     │         │           └─► Fail-safe (503 + Retry)    │
            └─────┼─────────┼───────────────────────┬─────────────────┘
                  │         │                        │
                  ▼         ▼                        ▼
        ┌──────────────┐ ┌──────────────┐  ┌────────────────────────┐
        │ Auth/Identidad│ │ BASE DE DATOS│  │ Servicios externos     │
        │  (proveedor)  │ │ {{DB_STACK}} │  │ (IA, email, pagos...)  │
        └──────────────┘ │ cifrado en   │  └────────────────────────┘
                         │ reposo       │
                         └──────────────┘
                                  ▲
                                  │
            ┌─────────────────────┴───────────────────────────────────┐
            │  PLATAFORMA CLOUD  ──  {{CLOUD_STACK}}                   │
            │   Cómputo · Migraciones · Scheduler · Secret Manager ·  │
            │   Logs estructurados · Monitoring                       │
            └─────────────────────────────────────────────────────────┘
```

---

## 3. Decisiones clave de arquitectura

| ID | Decisión | Motivo | RFC |
|---|---|---|---|
| ADR-001 | Offline-first con outbox | Continuidad de uso sin red; integridad de datos clínicos | _(RFC-XXX)_ |
| ADR-002 | Identidad solo desde token verificado | Anti-IDOR; evita suplantación | _(RFC-XXX)_ |
| ADR-003 | Cifrado en reposo de campos sensibles | Protección de PHI/PII | _(RFC-XXX)_ |
| ADR-004 | Migraciones automáticas con aborto ante fallo | Proteger producción | _(RFC-XXX)_ |
| ADR-005 | _(añadir)_ | _(motivo)_ | _(RFC-XXX)_ |

---

## 4. Ítems de software y clase de seguridad (IEC 62304 §5.3)

> Clasificá cada ítem: **A** (no contribuye a daño), **B** (daño no serio posible), **C** (daño serio o muerte posible). El producto hereda la clase del ítem más alto salvo segregación demostrada.

| Ítem de software | Descripción | Clase de seguridad | Justificación |
|---|---|---|---|
| Motor de algoritmo clínico | _(qué calcula/decide)_ | _(A/B/C)_ | _(daño posible si falla)_ |
| Motor de sincronización offline | Persistencia y orden de mutaciones | _(A/B/C)_ | _(pérdida/corrupción de datos)_ |
| Capa de autenticación/identidad | Resolución del sujeto | _(A/B/C)_ | _(acceso indebido a PHI)_ |
| Capa de notificaciones/alertas | Avisos clínicos al usuario | _(A/B/C)_ | _(alerta perdida)_ |
| UI de cliente | Presentación e interacción | _(A/B/C)_ | _(error de interpretación)_ |
| Integraciones externas (IA/3os) | _(qué proveen)_ | _(A/B/C)_ | _(dato erróneo a decisión)_ |

---

## 5. Puntos de fail-safe (ISO 14971)

| Punto | Modo de fallo | Comportamiento seguro esperado |
|---|---|---|
| Pérdida de red en cliente | Sin backend | Operar offline; encolar mutaciones; avisar estado, no bloquear |
| Backend saturado (pool BD agotado) | 503 | Degradar con `503 + Retry-After`; mensaje empático; sin traceback |
| Fallo de algoritmo clínico | Excepción | No mostrar resultado dudoso; estado "no disponible"; registrar incidente |
| Fallo de servicio de IA | Timeout/error | Degradar a flujo sin IA; nunca inventar dato clínico |
| Fallo de migración | Schema inconsistente | Abortar deploy; mantener versión previa |

---

## 6. Versionado de este documento

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v0.1 | 2026-01-01 | {{OWNER}} | Plantilla inicial |
