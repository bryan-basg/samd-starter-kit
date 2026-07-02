---
name: anti-drift
description: Protocolo anti-drift para orquestar 2+ subagentes en paralelo sin perder cohesión — contrato compartido, git diff real, agente correctivo. Usala cuando vayas a repartir una tarea entre 2 o más subagentes en paralelo, o cuando ya lanzaste agentes y sospechás que sus cambios divergieron entre sí.
---

# anti-drift — Protocolo de cohesión multi-agente

Cuando orquestás una tarea con 2+ subagentes en paralelo, el riesgo no es la calidad individual (cada agente trae sus reglas duras precargadas) sino la **pérdida de cohesión**: como orquestador recibís summaries de *lo que el agente intentó*, no del *diff real*.

## Cuándo usarla

- Antes de lanzar 2 o más subagentes en paralelo sobre una tarea con un contrato compartido (campos, tipos, paths, defaults).
- Cuando hay dependencia de tipos generados (por ejemplo un contrato OpenAPI compartido entre backend y frontend).
- Cuando un símbolo compartido cruza 3 o más capas del proyecto.
- Después de correr una ola de agentes, para verificar que no divergieron entre sí antes de dar por cerrado el trabajo.

## Los 7 pasos (obligatorios)

1. **Leé el brief y el contexto vos mismo** — delegás la ejecución, no el entendimiento.
2. **Escribí el contrato compartido en el chat**: campos / tipos / paths / defaults / validaciones EXACTOS. Esperá el OK del dueño del proyecto antes de lanzar.
3. **Armá el brief de cada agente citando el contrato literal.**
4. **Tras cada agente, leé el `git diff` REAL** (no el summary) y validá coherencia contra el contrato.
5. **Si hay drift, lanzá 1 agente correctivo** — NO re-lances a todos.
6. **El agente de auditoría regulatoria revisa y propone trazabilidad** (si tu kit tiene uno, invocalo en este paso).
7. **Cerrá con números reales** (tests, cobertura, archivos tocados).

## Cohesión (reglas duras)

- Ningún agente toca trazabilidad directamente — la propone el agente auditor, la ejecuta el orquestador.
- Tipos y constantes los define el contrato — prohibido que un agente "infiera del contexto".
- Un patrón nuevo no previsto → parás y consultás al dueño del proyecto (los patrones validados se elevan a regla en `CLAUDE.md`).
- Una tarea pequeña y única por agente.
- A más agentes simultáneos, más rigor: contrato literal + `git diff` real, nunca el summary.

## Serializar (NO paralelizar) cuando

- El contrato es complejo o cambiante.
- Hay dependencia de tipos generados (por ejemplo un contrato OpenAPI compartido entre backend y frontend).
- Un símbolo compartido cruza 3 o más capas.
