---
name: ci-rojo
description: Diagnóstico de un workflow de CI en rojo — logs frescos, reproducir barato en local, distinguir fallo ambiental vs de código; reset del runner self-hosted si aplica. Úsala cuando un workflow de GitHub Actions (o CI equivalente) falla y hay que decidir si es una regresión real de código o un problema ambiental antes de tocar nada.
---

# ci-rojo — Diagnóstico de un CI en rojo

Diagnosticá un CI en rojo sin teorizar sobre el código antes de mirar los logs REALES. (IEC 62304 §5.6 — análisis de impacto: primero evidencia, después hipótesis.)

## Cuándo usarla

- Un workflow de GitHub Actions (o el CI del proyecto) quedó en rojo y hay que decidir el siguiente paso.
- Antes de asumir que un fallo de CI es una regresión de código: hay que descartar causa ambiental (runner, timeout, recurso compartido) primero.
- El runner self-hosted del proyecto quedó en un estado sucio (permisos, archivos huérfanos) y el checkout del siguiente job falla.
- Un ítem de un backlog/checklist de auditoría dispara la sospecha de que algo está roto, pero conviene verificar contra el estado real antes de invertir tiempo.

## Procedimiento

1. **Logs FRESCOS**: los logs de CI suelen **expirar o rotar** (por ejemplo, HTTP 410 en runs viejos de GitHub Actions). Re-disparar el workflow (`gh workflow run <wf>` o el equivalente del proveedor de CI) y leer el error de la corrida nueva, no de una vieja. Si el workflow tiene un modo barato/parcial (dispatch incremental, subset de tests, dry-run), usarlo primero para acortar el ciclo de diagnóstico.

2. **Reproducir lo barato en local** antes de asumir bug de código/config. Si se puede correr el mismo comando que corre el CI en la máquina local en segundos/minutos, hacerlo antes de especular.

3. **¿Ambiental o de código?** Una caída puede ser **ambiental** (OOM del runner, timeout, recurso compartido ocupado — puerto, lock, contenedor — o test flaky por timing) y no una regresión real de código. Antes de asumir regresión: reproducir 2-3 veces en local y volver a disparar el workflow; si a veces pasa y a veces no con el mismo código, es ambiental, no de código.

4. **Corolario**: ítems de un backlog/checklist de auditoría que dispararon el diagnóstico pueden estar obsoletos (ya resueltos, o su premisa ya no es cierta) — verificar contra el estado REAL del repo/infra antes de invertir tiempo arreglando algo que ya no aplica.

## Runner self-hosted sucio

Aplica cuando el CI corre en infraestructura propia, no 100% gestionada por el proveedor.

- Si el workspace de trabajo del runner queda sucio (archivos con otro dueño/permisos, típicamente de un job que corrió en un contenedor con otro usuario, ej. `root`, dejando archivos que el siguiente job — con otro usuario — no puede borrar), el checkout del siguiente job revienta con errores de permiso (`EACCES`, locks de VCS que no se pueden borrar, etc).
- Reset: borrar el directorio de trabajo del runner para ese repo (recreación limpia en el próximo job). Esta limpieza normalmente requiere privilegios elevados → que la corra quien administra la máquina del runner, no el agente.
- Regla de fondo para evitar que se ensucie de nuevo: si un job corre dentro de un contenedor con un usuario distinto al que corren los demás jobs sobre el mismo workspace, aislarlo (runner/workspace dedicado) o evitar mezclar "container job" con "host job" en el mismo directorio de trabajo. Un runner self-hosted único además implica que los jobs corren en SERIE, no en paralelo — tenerlo en cuenta al medir cuánto debería tardar un push.
