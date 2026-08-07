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

## Estrategia

Consultá `docs/03_software_development_plan/COMPLETE_TESTING_STRATEGY.md` y `docs/04_user_documentation/TESTING_TOOLS.md` antes de tocar la suite.
