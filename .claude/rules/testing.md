---
paths:
  - "frontend/src/**/*.test.ts"
  - "frontend/src/**/*.test.tsx"
  - "frontend/src/**/__tests__/**/*.ts"
  - "frontend/src/**/__tests__/**/*.tsx"
  - "frontend/stryker.conf*.json"
  - "frontend/vitest.config.ts"
  - "tests/**/*.py"
  - "**/conftest.py"
  - "pytest.ini"
---

# TESTING (consecuencia directa SaMD §5.7 — verificación)

> Regla **por-capa** del cerebro SaMD; las reglas **transversales** viven en `CLAUDE.md`. Esta regla carga sola cuando el agente lee/edita tests o configs de test. Es una **CONSECUENCIA PRÁCTICA de la Regla 0** (cumplimiento SaMD): no es opcional. Capa/agente dueño: `qa-mutation` (mutación) · `e2e-integration` (E2E) · `frontend`/`backend` (unidad). El régimen de olas multi-agente vive en `.claude/rules/orquestacion.md`.

SaMD Clase {{SAMD_CLASS}} exige verificación demostrable. Esto NO es negociable.

## Reglas duras

* **Tests rigurosos, no de humo:** "renderiza sin crashear" NO es un test SaMD. Exigir aserciones específicas sobre valores, llamadas y side effects.
* **Mutation score**: **≥90% SOLO en los módulos clínicos/críticos** (escalas y scoring, red de crisis, cifrado, sync offline — identificá los tuyos y listalos explícitamente acá), **≥75% como piso en el resto** (UI general, configuración, features sin riesgo clínico directo). Backend ≥80% en los módulos clínicos críticos. **No pongas el mismo umbral alto a TODO el frontend por igual**: sostener ≥90% en pantallas sin riesgo clínico cuesta más de lo que protege. Reservá el 90% para donde un mutante vivo puede llegar a lastimar a un usuario. Si un módulo crítico baja del umbral, intervenir.
* **Atacar el umbral POR ARCHIVO dentro de un módulo crítico, no en superficie**: un módulo que promedia 90% puede esconder un archivo clínico en 60%. Si un mutante es irreducible, un refactor de producción mínimo y justificado es preferible a cerrar el archivo por debajo del umbral.
* **Mutation testing es caro — configuralo o te come el día**: ignorá la mutación de constantes estáticas (suele ser la mayoría del tiempo desperdiciado) y subí el timeout del *dry run* para suites grandes. Una corrida completa de frontend puede tomar horas.
* **Mocks asíncronos firmes** + aislamiento de estado global en cada test (fixture de reseteo).
* **Si el código bajo test usa `hasattr`/duck-typing**, mockear con **whitelist explícita** de atributos. Un mock plano responde afirmativamente a cualquier consulta de atributo y deja mutantes vivos.
* **Tests de conexiones persistentes (WebSocket/SSE)**: usá un doble de la conexión sobre tu orquestador. Un cliente de test **síncrono** dispara el ciclo de vida de la app y envenena los tests asíncronos siguientes.
* **No correr el type-checker/tests unitarios mientras corre mutation testing** — son CPU-intensivos y los procesos se contaminan.
* **No improvisar detección de imports muertos a ojo** — usar el linter (riesgo de borrar imports usados vía side effects).
* **Un test que falla solo en la suite completa es state-leak, no flaky "de la vida"**: ver la skill `/diagnostico-state-leak` antes de tocar un fixture global.
* **Un límite de tiempo en un test se mide en CPU, no en reloj de pared.** El reloj de pared (`perf_counter`) cuenta también la espera por la CPU que se llevan los otros jobs o workers de la misma máquina: un test «responde rápido» pasa en tu equipo y rojea en el CI sin que el código haya empeorado. Medí con `time.process_time()` y quedate con el **mínimo de hasta N corridas** (cortando en cuanto una baja del límite): una regresión real gasta CPU en TODAS las corridas, el ruido del planificador solo en algunas. Verificación obligatoria por **sabotaje** (meté ~1 s de CPU en la función y confirmá que rojea): un test al que le aflojaste el reloj tiene que seguir cazando la regresión real.
* **Una aserción sobre logs depende del nivel de log que heredó el proceso.** Un test que compara la lista exacta de trazas puede ver (o no) las de INFO del constructor según el nivel que dejó el test anterior o el reparto de tests del CI: verde en local, rojo en el CI. Fijá el nivel (`caplog.set_level`) **antes** de construir el objeto y llamá `caplog.clear()` justo antes de la acción que medís; verificalo corriendo el archivo con `--log-level` en INFO, WARNING y DEBUG.
* **Buscar un valor con una cifra o palabra pelada da falsos rojos (aserción negativa) y falsos verdes (positiva).** «El valor `300` no aparece en la fila cifrada» choca con cualquier otro campo que lo contenga (un timestamp en milisegundos, un id). Buscá el valor **con su contexto** (`"dosis":300`), no la subcadena corta.

## Estrategia

Consultá `docs/03_software_development_plan/COMPLETE_TESTING_STRATEGY.md` y `docs/03_software_development_plan/TESTING_TOOLS.md` antes de tocar la suite.
