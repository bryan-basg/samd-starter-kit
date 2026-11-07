# Instrucciones para Codex y otros agentes

Este proyecto ya tiene su guía de trabajo en `CLAUDE.md` y su configuración especializada en `.claude/`. Úsalas como fuente de las reglas del proyecto; no dupliques esas instrucciones aquí.

> **Plantilla del SaMD Starter Kit.** Este archivo es el punto de entrada para herramientas que leen `AGENTS.md` (Codex y similares) en vez de `CLAUDE.md`. No agrega reglas: solo lo conecta con la guía existente. Si tu equipo no usa esas herramientas, podés borrarlo.

## Al iniciar una tarea

1. Lee `CLAUDE.md` antes de cambiar código o documentación. La **Regla 0 (cumplimiento SaMD)** manda sobre cualquier conveniencia.
2. Revisa `git status --short` y conserva todo cambio preexistente. No lo sobrescribas, reviertas ni incluyas en tu trabajo.
3. Lee solo las reglas de `.claude/rules/` pertinentes a los archivos que vas a tocar (cada una declara en su frontmatter `paths:` a qué capa aplica). Las reglas transversales —las que no llevan `paths:`: `orquestacion.md`, `agentes.md`, `comandos.md`, `sesiones-paralelas.md`— aplican siempre.
4. Si una skill de `.claude/skills/` coincide con la tarea, lee su `SKILL.md` y sigue el procedimiento. Abre `reference.md` solo si necesitas sus casos o fundamentos.
5. Si una ficha de `.claude/agents/` coincide con la especialidad, úsala como guía de enfoque y límites. Es una referencia de instrucciones; no afirmes que se inició un agente Claude ni que se ejecutó un subagente si no ocurrió.

## Reglas de colaboración

- Responde y escribe documentación en el idioma que fija `CLAUDE.md` (`{{CHAT_LANG}}`), salvo que el usuario pida otro.
- Conserva las salvaguardas SaMD, privacidad, seguridad y trazabilidad descritas en `CLAUDE.md`.
- **No commitees ni pushees sin que el dueño lo pida** (`CLAUDE.md` §Git y commits). Los procesos pesados (mutación, fuzz, DAST, suites completas) piden OK cada vez (`.claude/rules/orquestacion.md`, regla dura 2).
- Prioriza las instrucciones explícitas y recientes del usuario cuando aclaren el alcance de una regla del proyecto.
- Los comandos de `.claude/commands/` describen flujos de trabajo de Claude Code. En otras herramientas, léelos y aplica sus pasos pertinentes manualmente; no digas que ejecutaste un comando slash de Claude.
- Los formatos y ajustes propios de Claude Code (hooks de `.claude/settings.json`, candados de `.claude/scripts/`) no se activan automáticamente en otras herramientas: **las reglas que esos candados hacen cumplir siguen vigentes aunque nada las bloquee mecánicamente**.
