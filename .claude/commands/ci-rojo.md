---
description: Diagnóstico de un workflow de CI en rojo — logs frescos, reproducir barato en local, distinguir fallo ambiental vs de código; reset del runner self-hosted si aplica.
argument-hint: <nombre del workflow en rojo>
---

Sos el diagnosticador de un CI en rojo para {{PROJECT_NAME}}. **NO teorices sobre el código antes de mirar los logs REALES.** (IEC 62304 §5.6 — análisis de impacto: primero evidencia, después hipótesis.)

## Pasos

1. **Logs FRESCOS**: los logs de CI suelen **expirar o rotar** (por ejemplo, HTTP 410 en runs viejos de GitHub Actions). Re-dispará el workflow (`gh workflow run <wf>` o el equivalente de tu proveedor de CI) y leé el error de la corrida nueva, no de una vieja. Si el workflow tiene un modo barato/parcial (dispatch incremental, subset de tests, dry-run), usalo primero para acortar el ciclo de diagnóstico.
2. **Reproducí lo barato en local** antes de asumir bug de código/config. Si podés correr el mismo comando que corre el CI en tu máquina en segundos/minutos, hacelo antes de especular.
3. **¿Ambiental o de código?** Una caída puede ser **ambiental** (OOM del runner, timeout, recurso compartido ocupado — puerto, lock, contenedor — o test flaky por timing) y no una regresión real de código. Antes de asumir regresión: reproducí 2-3 veces en local y volvé a disparar el workflow; si a veces pasa y a veces no con el mismo código, es ambiental, no de código.
4. **Corolario**: ítems de un backlog/checklist de auditoría que dispararon el diagnóstico pueden estar obsoletos (ya resueltos, o su premisa ya no es cierta) — verificá contra el estado REAL del repo/infra antes de invertir tiempo arreglando algo que ya no aplica.

## Runner self-hosted sucio (si tu CI corre en infraestructura propia, no 100% gestionada por el proveedor)

- Si el workspace de trabajo del runner queda sucio (archivos con otro dueño/permisos, típicamente de un job que corrió en un contenedor con otro usuario, ej. `root`, dejando archivos que el siguiente job — con otro usuario — no puede borrar), el checkout del siguiente job revienta con errores de permiso (`EACCES`, locks de VCS que no se pueden borrar, etc).
- Reset: borrar el directorio de trabajo del runner para ese repo (recreación limpia en el próximo job). Esta limpieza normalmente requiere privilegios elevados → que la corra quien administra la máquina del runner, no el agente.
- Regla de fondo para evitar que se ensucie de nuevo: si un job corre dentro de un contenedor con un usuario distinto al que corren los demás jobs sobre el mismo workspace, aislalo (runner/workspace dedicado) o evitá mezclar "container job" con "host job" en el mismo directorio de trabajo. Un runner self-hosted único además implica que los jobs corren en SERIE, no en paralelo — tenelo en cuenta al medir cuánto debería tardar un push.
