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

## Los rojos que NO se ven (§5.7 — un gate que no avisa no es un gate)

Un gate roto que **rojea** se arregla el mismo día. Un gate roto que **no aparece en rojo** puede llevar meses sin auditar nada, y en SaMD eso es evidencia de verificación que nunca existió. Los cuatro modos de fallo conocidos:

* ⚠️ **Un job que agota su `timeout-minutes` termina `cancelled`, NO `failure` — y un `cancelled` no se lee como rojo.** No sale en rojo en la lista de corridas, ni en el correo, ni de un vistazo. Un job de accesibilidad que muere clavado con su reloj **no auditó nada y nadie se entera**. Lo mismo cuando un job espera un runner apagado y el proveedor lo cancela tras horas en cola. Dos reglas derivadas:
  * **Un job CENTINELA por workflow con jobs largos**: `needs` de **todos** los jobs, `if: ${{ !cancelled() }}` (no `always()`: si el dueño cancela la corrida entera a mano, el centinela no la pinta de rojo; si el cancelado es UN job, sí corre), **sin `continue-on-error`**, y falla si alguno no terminó en `success`. La lista del `needs` es inevitablemente manual ⇒ el centinela **compara esa lista contra los jobs declarados en el propio archivo** y rojea si alguno quedó fuera: así **un job nuevo entra en la vigilancia por existir**, no por acordarse.
  * **El paso que puede colgarse muere ANTES que el job**: dale un presupuesto propio (`timeout` de coreutils o `timeout-minutes` del step) **estrictamente menor** que el reloj del job. Esa desigualdad ES el arreglo — falla el PASO (rojo visible) en vez de agotarse el JOB (invisible) — y hay que rehacer la aritmética al cambiar cualquiera de los dos números.
* ⚠️ **`continue-on-error: true` (y los `optional: true` de una matriz) absorben el rojo.** Un job marcado así puede llevar meses muriendo con el workflow reportándose VERDE. Meta a sostener: **0 jobs con `continue-on-error` en todo el repo**; si un job es tan frágil que lo necesita, el problema es el job. Verificable: `grep -rn "continue-on-error\|optional: true" .github/workflows/`.
* ⚠️ **`cancel-in-progress` incondicional se come la evidencia de los crones.** En una corrida programada, la que cancelás es la ÚNICA muestra del día: se pierde la medición **y** queda como `cancelled`, dos avisadores rotos por un solo campo. Gatealo por evento: `cancel-in-progress: ${{ github.event_name == 'pull_request' }}`.
* ⚠️ **Un cron retirado deja el gate sin corridas programadas y la regla lo sigue dando por vivo.** Si un gate depende de una corrida periódica, su existencia se verifica contra el disco (`grep -n "cron:" .github/workflows/*.yml`), no contra lo que dice la documentación. Importa para §5.7: la evidencia que depende de que alguien la dispare a mano, en la práctica no se dispara.

## Mediciones y umbrales

* **Primero "¿la medición sirve?", después "¿los números cumplen?".** Un gate de rendimiento o accesibilidad tiene que separar **"no pude medir"** (el informe no produjo valor: `NaN`, herramienta caída, página que no cargó) de **"mediste mal"** (el número no cumple el umbral). Si ambos dan el mismo rojo, el final del camino es marcar el gate como opcional y perderlo. Patrón: un validador exige que la mayoría de los informes traiga valores, con UN reintento, y si sigue sin valor **rojea diciendo "no pude medir"**.
* **Un umbral calibrado en una máquina NO vale en otra.** Las métricas dominadas por CPU (tiempo de bloqueo, latencia) pueden variar **decenas de veces** entre el escritorio del dev y un runner gestionado — sobre el MISMO commit. Si el gate se muda de entorno, **no se afloja el umbral** (suele ser un requisito de rendimiento trazado): se declara un tope aparte para ese entorno, o el job se ancla al entorno donde se calibró. Aflojar el umbral para tapar el ruido del entorno es perder el requisito.
* **Serializá los jobs que miden.** Medir bajo contención de CPU reproduce falsos rojos: si varios jobs comparten máquina, poné el que mide detrás de los demás con `needs:` y con `!cancelled()` para que **mida aunque otro job rojee**.

## Runner self-hosted (si lo usás)

* **NO mezclar `container:` (root) con jobs en el host (usuario normal) en el mismo runner.** El runner reusa una sola carpeta de trabajo entre jobs: un job con `container:` corre como root y deja archivos que el siguiente job **no puede borrar** → el checkout revienta con errores de permisos. Regla dura: o todos los jobs del runner usan contenedor, o ninguno. El "arranque limpio" lo da el checkout, no el contenedor.
* **Un solo runner = jobs en SERIE**, no en paralelo como el CI gestionado: un push que dispara varios workflows tarda la suma, no el máximo. Si molesta, se levantan varios runners en la misma máquina — **pero entonces la regla se INVIERTE y hay que anotarlo**: los jobs pasan a correr **en paralelo compitiendo por los mismos núcleos**, así que dos jobs pesados a la vez se estorban y un rojo puede ser contención de CPU y no código. Con varios runners, un workflow pesado se pone en fila con `needs:` en vez de confiar en que el runner lo serialice. Verificá cuántos hay antes de razonar sobre esto: una regla que describe "un solo runner" cuando ya hay tres lleva a diagnósticos al revés.
* **Reset del directorio de trabajo sucio** (leftovers de root) necesita permisos de administrador → **lo corre el dueño**, no el agente.
* **Los crons pesados van al CI gestionado**, no al runner de escritorio: si la máquina está apagada, el cron simplemente no corre y nadie se entera.
