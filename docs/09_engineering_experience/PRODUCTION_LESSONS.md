# Field Notes — Lecciones de producción

> **English abstract:** Hard-won lessons from running a Class B SaMD platform in production. Each note follows *symptom → root cause → lesson*. Generalized from real incidents; no product specifics. This is the "the oven burns on the left, I learned the hard way" layer of the kit.

Estas no son teorías de manual: son cosas que rompieron en producción y lo que se aprendió arreglándolas. Cada lección está generalizada (sin datos del producto) para que te las ahorres en tu propio dispositivo.

Formato: **Síntoma → Causa → Lección.**

---

## Datos y base de datos

### El pool de conexiones agotado se disfraza de "problema de auth"
- **Síntoma:** oleada de `401` masivos + `500` sin autenticar, simultáneos, sin que nadie tocara las credenciales.
- **Causa:** el pool de conexiones de la BD estaba agotado. El camino de auth no conseguía conexión y fallaba como si el token fuera inválido.
- **Lección:** un `401 masivo + 500 sin auth` casi nunca es un problema de credenciales — es **presión de pool**. Antes de tocar el proveedor de identidad, mirá las conexiones de la BD. Y hacé que el camino de auth degrade con `503 + Retry-After` ante timeout de BD, no con un `401` falso.

### El techo de conexiones se calcula sumando TODOS los engines
- **Síntoma:** la app aguanta en pruebas pero colapsa bajo carga real con varias instancias.
- **Causa:** se dimensionó el pool principal pero se olvidaron los engines secundarios (logs, sync, migraciones). El total superó el límite del tier de la BD.
- **Lección:** el techo agregado es `max_instances × (pool_principal + pool_logs) + baseline_sync`, y tiene que ser **menor** que las conexiones del tier. Si subís el tier o la concurrency, reevaluá los tres engines juntos, no solo el principal.

### Migrar columnas con datos en un solo paso es una bomba de tiempo
- **Lección:** nunca dropees ni renombres una columna con datos en una sola migración. Fase intermedia obligatoria: *deprecate → backfill → drop*, en releases separados. Un `downgrade()` real (no `pass`) es parte de la red de seguridad.

---

## Deploy e infraestructura

### El "verde" de la migración puede estar mintiendo
- **Síntoma:** el CI marca la migración en verde, pero en producción la BD no quedó en la revisión esperada.
- **Causa:** el CI migra contra SQLite, donde no aparecen los errores específicos del driver de producción (ej. el greenlet de un driver async). El verde era contra una BD distinta a la real.
- **Lección:** **nunca confíes en el verde de una migración sin verificar la revisión REAL aplicada** en el entorno destino. El deploy debe migrar de forma atómica y **abortar si falla**, antes de publicar. Y backup de la BD antes del primer deploy de una migración irreversible.

### `--set-env-vars` reemplaza; `--update-env-vars` mergea
- **Síntoma:** un servicio que andaba perfecto empieza a fallar (IA caída, features muertas) justo después de un deploy que "solo cambiaba una variable".
- **Causa:** el comando de deploy **reemplazó toda la lista** de variables de entorno en vez de mergear. Las demás se perdieron.
- **Lección:** usá siempre el modo merge para env vars. Si tenés que reemplazar, leé el estado actual primero y reconstruí la lista completa. Este footgun es recurrente — vale un check en el runbook de deploy.

### Los secretos tienen doble fuente
- **Lección:** el `.env` del repo NO afecta producción; en prod manda el gestor de secretos. Cambiar un secreto exige **dos pasos**: actualizarlo en el gestor *y* reiniciar el servicio para que lo recargue. Si te olvidás el segundo, el cambio no toma efecto y perdés una hora buscando un bug que no existe.

### Pin de imagen por digest, no por tag
- **Lección:** deployá por `@sha256:...`, no por `:latest`. El tag mutable te deja sin saber qué se está corriendo realmente y hace imposible un rollback limpio en medio de un incidente.

---

## Resiliencia y fail-safe (ISO 14971)

### Cuando un recurso compartido se satura, frená con cortesía
- **Lección:** ante presión de un recurso compartido (pool de BD, cuota de IA), respondé `503 + Retry-After` en vez de propagar un `500`. El cliente respeta el header con backoff. Un `500` seco cae en cascada; un `503` con Retry-After se autorregula. En un dispositivo médico, degradar **predecible** es un requisito, no un lujo.

### El usuario en crisis nunca debe ver un traceback
- **Lección:** los errores al usuario son mensajes empáticos + código HTTP correcto. Un traceback no solo asusta a alguien que ya está mal: además le regala a un atacante tu arquitectura, paths y versiones de dependencias. Es UX *y* seguridad a la vez.

---

## Sincronización offline-first

### Toda mutación pasa por la cola local, sin excepción
- **Síntoma:** datos que se pierden o se duplican cuando la red se cae a la mitad de una acción.
- **Causa:** una mutación nueva que escribió directo a la red, salteando el motor de sync.
- **Lección:** **toda** mutación va primero a la cola local (outbox) y de ahí sincroniza. Una sola excepción "porque era rápido" rompe la garantía offline-first para siempre. La regla es absoluta justamente para que no haya que pensarla cada vez.

### En móvil, el almacenamiento "persistente" a veces no lo es
- **Lección:** en algunos WebViews de Android, `localStorage` se borra entre arranques por limpiezas del sistema. Para datos críticos (idioma, tokens, preferencias) usá almacenamiento nativo como respaldo. Lo descubrís cuando un usuario "pierde la sesión" sin razón aparente.

---

## Testing y mutation

### Los tests de mutation son contratos, no decoración
- **Lección:** una vez que un test de mutation "fija" un literal clínico, un aria-label o una fórmula, ese literal es un **contrato verificado**. Si después tocás el literal de producción "porque es un typo" sin actualizar su killer, rompés el contrato silenciosamente. Tocar el literal obliga a tocar su test en el mismo PR.

### El motor de mutation congela la lista de tests en el arranque
- **Síntoma:** escribís tests nuevos para matar mutantes, corrés el motor, y los mutantes siguen vivos.
- **Causa:** el motor de mutation fija el conteo de tests en su *dry-run* inicial. Los tests creados después no entran.
- **Lección:** patrón canónico → primero escribís los tests, verificás la suite verde, **y recién entonces** corrés el motor de mutation. Nunca en paralelo con quien escribe tests.

### Los mocks globales se filtran entre tests
- **Lección:** un test que pasa aislado puede romper a otro en la suite completa por un mock global mal limpiado. `afterEach` robusto + **verificar siempre la suite COMPLETA** antes de cantar verde. "Pasa aislado" no es "pasa".

---

## Seguridad

### La identidad viene solo del token, jamás del cliente
- **Lección:** nunca aceptes `user_id` desde body, query ni header. Solo del token decodificado. Un endpoint que confíe en un id del cliente es escalada horizontal garantizada — alguien lee datos de otro paciente cambiando un número. Validá también *audience* e *issuer*, no solo la firma.

### Los logs de auditoría no llevan PII en claro
- **Lección:** el audit log lleva `user_id` (hash/UUID), endpoint, método, status, timestamp — **nunca** email, teléfono ni contenido clínico en claro. Un log es persistente: lo que filtres ahí, filtraste para siempre.

---

## Diagnóstico (la meta-lección)

### Investigá antes de fixear
- **La lección que más caro sale:** ante un bug reportado, investigá primero — no saltes a escribir código. Más de una vez "se arregló la voz" cuando el problema eran los audífonos del usuario. Un bug tras un deploy: leé los **logs estructurados** antes de teorizar sobre cache, Service Worker o navegador. El diagnóstico equivocado cuesta más que el bug.

---
**Navegación:** [Índice del DHF](../README.md) · [Master Map](../00_master/MASTER_MAP.md)
