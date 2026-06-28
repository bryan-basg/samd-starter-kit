# RFC-003 — Scheduling de jobs periódicos vía cron externo gestionado

**Proyecto:** {{PROJECT_NAME}} · **Clase SaMD:** {{SAMD_CLASS}} · **Versión:** v1.0 · **Fecha:** 2026-01-29

> RFC del SaMD Starter Kit. Ejemplo didáctico de una decisión de diseño de la capa cloud/API. Documenta cómo se disparan los trabajos periódicos (recordatorios, avisos clínicos, mantenimiento de colas).

---

## Metadatos

| Campo | Valor |
|---|---|
| ID | RFC-003 |
| Estado | **Implementado** |
| Autor | Equipo de Plataforma / Cloud |
| Revisores | Responsable de Backend, Responsable de Gestión de Riesgo (ISO 14971) |
| Fecha de propuesta | 2026-01-23 |
| Fecha de decisión | 2026-01-29 |
| Capa afectada | cloud / API |
| Clase de seguridad del ítem | B |

---

## 1. Contexto

El sistema necesita disparar trabajos periódicos: comprobar eventos próximos, despachar la cola de notificaciones pendientes y reprocesar avisos pospuestos. Estos avisos son **clínicamente relevantes** (un recordatorio perdido es una falla del dispositivo, no una molestia cosmética).

El backend {{BACKEND_STACK}} corre en {{CLOUD_STACK}} con **autoescalado horizontal**: bajo carga puede haber N instancias del proceso de la app simultáneamente. Un scheduler embebido en el proceso (p. ej. un scheduler en memoria que arranca con la app) se ejecutaría **una vez por instancia**.

## 2. Problema

Con un scheduler interno por proceso y autoescalado, cada job se multiplica por el número de instancias: N instancias → N ejecuciones del mismo tick en la misma ventana. Esto (a) **duplica/multiplica notificaciones** al usuario (anti-patrón neuro-UX: floodear a una persona en crisis) y (b) **consume conexiones del pool de BD** en cada instancia, pudiendo agotar el tier de la base y tumbar el servicio. El techo de conexiones del tier debe respetarse: `max-instances × pool_por_instancia` no puede superar las conexiones disponibles, y un scheduler interno suma trabajo de fondo a ese cálculo.

## 3. Alternativas consideradas

| # | Alternativa | Pros | Contras | Riesgo SaMD |
|---|---|---|---|---|
| A | **Scheduler interno en el proceso de la app** (siempre activo) | Cero infraestructura extra; un solo despliegue; fácil en dev | Se ejecuta 1×/instancia → jobs multiplicados bajo autoescalado; consume pool de BD en cada instancia; no hay "líder" elegido; difícil de monitorear de forma agregada | Saturación de pool (servicio caído) + notificaciones duplicadas |
| B | **Cron externo gestionado** que invoca un endpoint idempotente (elegida) | Un solo disparo por tick, independiente del número de instancias; el trabajo de cola se hace en una request acotada; observable y reintentos gestionados por el cron; no acopla el ciclo de vida del job al de la app | Requiere un componente de infraestructura más (cron gestionado del {{CLOUD_STACK}}) y proteger el endpoint disparador | Aceptable: disparo único, pool acotado, aviso clínico entregado una vez |
| C | **Elección de líder entre instancias** (lock distribuido para que solo una corra el scheduler) | Un solo ejecutor sin componente externo | Complejidad alta (lock distribuido correcto es difícil); el lock vive en la BD/cache → más estado compartido frágil; modos de fallo sutiles (lock huérfano = ningún ejecutor = aviso perdido) | Riesgo de "ningún ejecutor" silencioso → aviso clínico perdido |
| D | No hacer nada / dejar el scheduler interno activo en prod | — | El problema A en producción real | INACEPTABLE |

## 4. Decisión

Se adopta la **Alternativa B**: en producción los jobs periódicos los dispara un **cron gestionado externo** del {{CLOUD_STACK}}, que invoca un endpoint idempotente del backend (p. ej. `POST /notifications/process-queue`) en cada tick. El **scheduler interno queda deshabilitado por defecto** y solo se activa opt-in en desarrollo local.

Detalles de construcción:
- **Flag de control**: variable de entorno `ENABLE_INTERNAL_SCHEDULER` con default `false`. En prod permanece `false`; en dev local sin cron externo se pone `true` para no depender de infraestructura.
- **Endpoint disparador**: idempotente y acotado en trabajo por invocación; protegido (secreto compartido / OIDC) para que solo el cron pueda invocarlo.
- **Cobertura**: el cron externo cubre los tres jobs (eventos próximos, despacho de cola, reprocesado de pospuestos) con un único tick periódico.
- **Alineación de pool** (§5.6): el cálculo del techo de conexiones (`max-instances × pool_por_instancia + baseline`) se reevalúa sin sumar trabajo de scheduler por instancia, porque ya no existe en prod.

## 5. Consecuencias

- **Positivas**: un solo disparo por tick sin importar cuántas instancias haya; pool de BD acotado y predecible; avisos clínicos entregados exactamente una vez; reintentos y observabilidad del cron gestionados por la plataforma.
- **Negativas / costo**: depende de un componente externo (si el cron del {{CLOUD_STACK}} falla o se desconfigura, no hay ticks → se necesita alerta de "cron no disparó en X minutos"); el endpoint disparador es superficie de ataque y debe protegerse.
- **Impacto en consumidores** (§5.6): cualquier código que asumiera "el scheduler corre dentro del proceso" debe migrar a "el trabajo se hace cuando llega el tick HTTP"; el arranque de la app ya no inicia jobs en prod.
- **Fail-safe**: si el endpoint falla en un tick, el cron reintenta; el trabajo es idempotente, por lo que un reintento no duplica avisos. Falta prolongada de ticks → alerta de monitoreo (no falla silenciosa).
- **Deuda técnica generada**: `D-CLOUD-CRON-MISSED-TICK-ALERT-01` — alerta que dispare si el endpoint no recibe un tick dentro de la ventana esperada; `D-CLOUD-CRON-SECRET-ROTATION-01` — endurecer el secreto del disparador (rotación / OIDC).

## 6. Trazabilidad

| Vínculo | Referencia |
|---|---|
| Requisito(s) | REQ-SYNC-02 — Entrega fiable y no duplicada de avisos/jobs periódicos (notificaciones clínicas) |
| Riesgo(s) ISO 14971 | R-NOTIF-01 — Saturación del pool de BD por jobs multiplicados → servicio caído / aviso clínico perdido o duplicado (Sev. Seria × Prob. Ocasional → INACEPTABLE → residual ALARP) |
| Código | `ENABLE_INTERNAL_SCHEDULER` (default `false`) en `app/core/config.py:NN`; endpoint disparador en `app/api/notifications.py:NN`; cron del {{CLOUD_STACK}} en infra/IaC |
| Test(s) de verificación | `test_internal_scheduler_disabled_by_default`, `test_process_queue_is_idempotent`, `test_process_queue_requires_auth` en `tests/test_external_scheduler.py` |
| Entrada en Master Map | v1.0 |

## 7. Historial

| Versión | Fecha | Autor | Cambio |
|---|---|---|---|
| v0.1 | 2026-01-23 | Equipo de Plataforma / Cloud | Propuesta inicial |
| v1.0 | 2026-01-29 | Equipo de Plataforma / Cloud | Aceptada e implementada; scheduler interno deshabilitado por default, cron externo en prod |

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
