---
paths:
  - ".github/workflows/*.yml"
  - ".github/workflows/*.yaml"
---

# CI / GITHUB ACTIONS (consecuencia SaMD §5.7 — verificación reproducible)

> Regla **por-capa** del cerebro SaMD; las reglas **transversales** viven en `CLAUDE.md`. Esta regla carga sola cuando el agente lee/edita un workflow. Es una **CONSECUENCIA PRÁCTICA de la Regla 0** (cumplimiento SaMD): no es opcional. Capa/agente dueño: `cloud-ops`.
>
> **Adaptá esta regla a tu proveedor de CI real** si no usás GitHub Actions.

## Reglas duras

* **Workflow en rojo → logs FRESCOS antes de teorizar** (§5.6): reproducí lo barato en local antes de asumir bug de código o config; la caída puede ser **ambiental** (timeout, OOM del runner, flaky), no de código. Diagnóstico paso a paso: skill `/ci-rojo`.
* **Optimizaciones obligatorias en todo workflow nuevo**: cancelación de runs duplicados (`concurrency`), cache de dependencias, `timeout-minutes` duro y filtros por `paths` cuando el repo crece.
* **Acciones de terceros pineadas por SHA, no por tag.** Un tag (`@v4`) lo puede mover su dueño hacia otro commit en cualquier momento; en un contexto regulado eso es una cadena de suministro sin control de configuración (IEC 62304 §8). Pineá al SHA completo con el tag como comentario (`uses: org/action@<sha>  # v4.4.0`) y **unificá la misma versión en todos los usos** — el mismo repo referenciando una acción de dos formas distintas es drift.
* **Un baseline que se regenera en cada corrida no es un baseline.** Si un gate compara contra una línea base (cobertura, número de warnings, hallazgos de seguridad), esa base debe **persistir entre corridas** y actualizarse solo con intención explícita. Si la corrida roja la sobrescribe, el gate deja de detectar regresiones justo cuando hace falta.
* **El artefacto de evidencia se sube desde donde el script lo escribe.** Un workflow que sube el reporte desde una ruta que el script no usa termina en verde **sin evidencia** — y en SaMD la evidencia ES el entregable (§5.7). Verificá la ruta real, no la esperada.
* **Un gate que escanea un objetivo inexistente da verde falso.** Si el escaneo (DAST, fuzz, link-checker) apunta a URLs o rutas que devuelven 404, pasa sin haber mirado nada. Todo gate debe **fallar si su objetivo no existe**, nunca aprobar por vacío.
* **Ningún workflow guarda secretos en texto plano** ni los imprime en logs. Los secretos vienen del gestor del proveedor de CI.

## Runner self-hosted (si lo usás)

* **NO mezclar `container:` (root) con jobs en el host (usuario normal) en el mismo runner.** El runner reusa una sola carpeta de trabajo entre jobs: un job con `container:` corre como root y deja archivos que el siguiente job **no puede borrar** → el checkout revienta con errores de permisos. Regla dura: o todos los jobs del runner usan contenedor, o ninguno. El "arranque limpio" lo da el checkout, no el contenedor.
* **Un solo runner = jobs en SERIE**, no en paralelo como el CI gestionado. Un push que dispara varios workflows tarda la suma, no el máximo. Si molesta, levantar varios runners en la misma máquina.
* **Reset del directorio de trabajo sucio** (leftovers de root) necesita permisos de administrador → **lo corre el dueño**, no el agente.
* **Los crons pesados van al CI gestionado**, no al runner de escritorio: si la máquina está apagada, el cron simplemente no corre y nadie se entera.
