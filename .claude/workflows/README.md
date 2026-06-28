# Workflows multi-agente

Scripts de orquestación determinista (loops, fan-out, pipelines, verificación adversarial) para tareas SaMD que un solo contexto no puede sostener: auditorías amplias, revisiones por dimensión, migraciones multi-archivo.

> Estos workflows se ejecutan con la herramienta `Workflow` de Claude Code. El usuario debe **optar explícitamente** por orquestación multi-agente (decir "usá un workflow" / "ultracode") antes de que el agente los lance — pueden consumir muchos tokens.

## Patrón canónico SaMD — revisión por dimensiones con verificación adversarial

`samd-review.workflow.js` revisa el diff de la rama actual contra varias dimensiones de riesgo (seguridad, fail-safe clínico, trazabilidad, neuro-UX) en paralelo, y **refuta cada hallazgo con un agente independiente** antes de reportarlo — consecuencia directa de SaMD §5.6 (verificación adversarial obligatoria sobre hallazgos clínicos/seguridad).

Pipeline: cada dimensión revisa → cada hallazgo se verifica apenas su dimensión termina (sin barrera) → se reportan solo los confirmados.

## Reglas heredadas del proyecto (NO anular)

1. El motor de mutation NUNCA en paralelo con agentes que escriben tests.
2. Procesos pesados locales (mutation full, fuzz, suites completas) piden OK CADA vez.
3. Verificación adversarial obligatoria sobre hallazgos clínicos/seguridad antes de actuar.
4. Tras cada agente, leer el `git diff` REAL, no el summary.
