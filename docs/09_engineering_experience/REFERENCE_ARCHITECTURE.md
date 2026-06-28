# Arquitectura de referencia — Plataforma SaMD offline-first

> **English abstract:** The hybrid, offline-first architecture pattern behind a production Class B SaMD platform — and the *why* behind each decision. A teaching document, not a spec: it explains the trade-offs so you can reuse the pattern (or knowingly diverge).

Este documento describe el patrón de arquitectura que sostuvo una plataforma SaMD real en producción. No es "la única forma": es una forma **probada bajo regulación**, con las razones detrás de cada decisión para que las copies o las descartes a sabiendas.

## Vista de 10.000 pies

```
┌─────────────────────────────────────────────────────────────────┐
│  CLIENTE (offline-first)                                          │
│  UI accesible (WCAG 2.1 AA)                                       │
│  ├─ Estado local: IndexedDB                                       │
│  ├─ Outbox de mutaciones ──┐                                      │
│  └─ Librería de fetch+cache │ (sync cuando hay red)               │
└────────────────────────────┼─────────────────────────────────────┘
                             │  HTTP + token (identidad)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  BACKEND (API + lógica de negocio)                               │
│  ├─ Auth: user_id SOLO del token decodificado                    │
│  ├─ Audit middleware: persiste mutaciones, loggea lecturas       │
│  ├─ Fusibles: 503 + Retry-After ante presión de recursos         │
│  └─ Módulos clínicos con fail-safe explícito                     │
└──────────────┬──────────────────────────────┬───────────────────┘
               │                              │
               ▼                              ▼
┌──────────────────────────┐   ┌──────────────────────────────────┐
│  BD TRANSACCIONAL         │   │  PLATAFORMA CLOUD                 │
│  + auditoría              │   │  ├─ Gestor de secretos            │
│  + cifrado en reposo      │   │  ├─ Scheduler externo (cron)      │
│    (AES-256-GCM/columna)  │   │  ├─ IA gestionada                 │
│  + migraciones atómicas   │   │  └─ Logging + monitoring          │
└──────────────────────────┘   └──────────────────────────────────┘
```

## Las decisiones y su porqué

### 1. Offline-first de verdad, no "con cache"
**Decisión:** toda mutación se escribe primero en una cola local (IndexedDB/outbox) y sincroniza después; nunca va directo a la red.
**Por qué:** los usuarios clínicos usan la app en lugares con red mala o nula (consultorios, transporte, crisis). Si una acción depende de la red, se pierde justo cuando más importa. El outbox convierte "sin red" en un estado normal, no en un error.
**Trade-off:** complejidad de reconciliación e idempotencia. Vale la pena solo si el offline es un requisito real — pero en salud, suele serlo.

### 2. Identidad por token, nunca por cliente
**Decisión:** el `user_id` proviene exclusivamente del token decodificado por el proveedor de auth.
**Por qué:** cualquier identidad que venga del cliente (body/query/header) es falsificable. En un sistema con PHI, eso es exposición de datos de un paciente a otro — un riesgo clínico, no solo de privacidad.
**Consecuencia dura:** validar *audience* e *issuer*, no solo la firma. Las foreign keys apuntan a la tabla de usuarios real, nunca a un id provisto.

### 3. Dos bases de datos, cada una para lo suyo
**Decisión:** una BD del cliente (sync/outbox, estado offline) y una BD transaccional en el servidor (reglas de negocio, auditoría, datos clínicos cifrados).
**Por qué:** las propiedades que necesita el borde (latencia cero, offline) son opuestas a las del centro (consistencia transaccional, auditoría inmutable). Forzar una sola BD para ambas termina en un mal compromiso.

### 4. Cifrado en reposo a nivel columna
**Decisión:** los campos PII/PHI se cifran con AES-256-GCM a nivel columna, con la clave en un gestor de secretos, **separada** de la clave de firma de sesión.
**Por qué:** cifrar la BD entera (tipo disco) protege contra robo del disco, pero no contra un dump por SQL. El cifrado a nivel columna mantiene el dato ilegible incluso si la query se filtra. Llaves separadas → comprometer una no compromete la otra.
**Ver:** `docs/05_design_decisions/RFC-001-encryption-at-rest.md`.

### 5. Auditoría que no se come el pool
**Decisión:** el audit middleware persiste a BD solo las **mutaciones** (POST/PUT/DELETE/PATCH); las lecturas van a logging estructurado.
**Por qué:** auditar cada lectura en la BD consume conexiones del pool en el path caliente y lo satura. La trazabilidad de cambios (lo que exige SaMD §5.7) se mantiene; las lecturas quedan en logging, fuera del pool.

### 6. Scheduling externo, no en el proceso de la app
**Decisión:** los jobs periódicos los dispara un cron gestionado externo; el scheduler interno queda como opt-in solo para dev local.
**Por qué:** un scheduler dentro del proceso se multiplica por cada instancia (N instancias = N veces el job) y consume pool de BD. Un cron externo único es predecible y desacopla el trabajo periódico del ciclo de vida de las instancias.
**Ver:** `docs/05_design_decisions/RFC-003-external-scheduler.md`.

### 7. Fusibles antes que cascadas
**Decisión:** cada recurso compartido bajo presión responde `503 + Retry-After`, no `500`.
**Por qué:** un `500` seco propaga la falla aguas arriba y cae en cascada. Un `503 + Retry-After` le dice al cliente "esperá tanto y reintentá" → el sistema se autorregula en vez de derrumbarse. En un dispositivo médico, la degradación tiene que ser **predecible**.

## Cómo mapea a los agentes del kit

| Capa de la arquitectura | Agente responsable |
|---|---|
| Cliente offline-first, UI accesible | `frontend` |
| API, auth, audit, fusibles, módulos clínicos | `backend` |
| BD transaccional, migraciones, cifrado, pool | `db-architect` |
| Secretos, scheduler, IA, monitoring, deploys | `cloud-ops` |
| Verificación (mutation) | `qa-mutation` |
| Superficie de ataque, cifrado, JWT | `security-samd` |

## Cuándo NO usar este patrón

- Si tu app **no** necesita offline real, el outbox es complejidad pura — usá fetch+cache directo.
- Si no manejás PHI, el cifrado a nivel columna y la auditoría estricta son sobre-ingeniería.
- La arquitectura sigue al **uso previsto** y a la **clase de seguridad**, no al revés. Clasificá primero (`SOFTWARE_SAFETY_CLASSIFICATION.md`), arquitecturá después.

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
