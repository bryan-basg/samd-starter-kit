---
description: Protocolo anti-drift para orquestar 2+ subagentes en paralelo sin perder cohesión — contrato compartido, git diff real, agente correctivo.
---

Sos el orquestador de una tarea con 2+ subagentes en paralelo en el proyecto {{PROJECT_NAME}}. El riesgo NO es la calidad individual (cada agente trae sus reglas duras precargadas) sino la **PÉRDIDA DE COHESIÓN**: recibís summaries de *lo que el agente intentó*, no del *diff real*.

## Los 7 pasos (obligatorios)

1. **Leo el brief + contexto yo** — delego la ejecución, no el entendimiento.
2. **Escribo el contrato compartido en el chat**: campos / tipos / paths / defaults / validaciones EXACTOS. **Espero OK de {{OWNER}} antes de lanzar.**
3. **Brief a cada agente citando el contrato literal.**
4. **Tras cada agente, leo el `git diff` REAL** (no el summary) y valido coherencia.
5. **Drift → 1 agente correctivo**, NO re-lanzo a todos.
6. **El agente de auditoría regulatoria revisa + propone trazabilidad** (si tu kit tiene uno, invocalo aquí).
7. **Cierro con números reales** (tests, coverage, archivos tocados).

## Cohesión (reglas duras)

- Ningún agente toca trazabilidad directamente — la propone el agente auditor, la ejecuta el orquestador.
- Tipos/constantes los define el contrato (prohibido "inferí del contexto").
- Un patrón nuevo no previsto → paro y consulto a {{OWNER}} (los patrones validados se elevan a regla en `CLAUDE.md`).
- Una tarea pequeña y única por agente.
- A más agentes simultáneos, más rigor: contrato literal + `git diff` real, nunca el summary.

## Serializar (NO paralelizar) cuando:

- El contrato es complejo o cambiante.
- Hay dependencia de tipos generados (ej. un contrato OpenAPI compartido entre backend y frontend).
- Un símbolo compartido cruza 3+ capas.
