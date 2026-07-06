# Memory Index — {{PROJECT_NAME}}

> **Reglas estables del proyecto** (bugs conocidos, comandos, testing, protocolo con el dueño) viven en `CLAUDE.md`. Esta memoria es para **snapshots dinámicos** y estado puntual que cambia: estado de tests, hallazgos de sesión, lecciones puntuales, estado del plan.
>
> Entradas del índice = **1 línea** (`- [Título](archivo.md) — gancho`). El detalle vive en cada ficha. Mové el detalle a archivos por tema; no infles este índice.
>
> **¿Recién arrancás un SaMD con este kit?** Antes de crear tu primera memoria, leé
> [`docs/09_engineering_experience/STARTUP_DISCIPLINE.md`](../docs/09_engineering_experience/STARTUP_DISCIPLINE.md) —
> qué priorizar los primeros días (cumplimiento, memoria, shipping, UX), destilado de experiencia
> real construyendo un SaMD.

## Cómo funciona la memoria

Cada memoria es **un archivo = un hecho**, con frontmatter:

```markdown
---
name: <slug-en-kebab-case>
description: <resumen de una línea — sirve para decidir relevancia al recordar>
metadata:
  type: user | feedback | project | reference
---

<el hecho; para feedback/project, seguí con líneas **Por qué:** y **Cómo aplicarlo:**. Enlazá memorias relacionadas con [[su-name]].>
```

Tipos:

- **user** — quién es el dueño (rol, expertise, preferencias).
- **feedback** — guía sobre cómo trabajar (correcciones y enfoques confirmados); incluí el porqué.
- **project** — trabajo en curso, metas, restricciones no derivables del código o git. Convertí fechas relativas a absolutas.
- **reference** — punteros a recursos externos (URLs, dashboards, tickets).

Antes de guardar, buscá un archivo que ya cubra el tema y actualizalo en vez de duplicar. No guardes lo que el repo ya registra (estructura del código, fixes pasados, historia git, CLAUDE.md).

## Pendientes anotados

<!-- - [Título de la ficha](archivo.md) — gancho de una línea con estado. -->

## Plan maestro de mejoras

<!-- - [Plan principal](plan.md) — método y estado del recorrido. -->

## Último cierre (2026-07-05)

- [491a9a8a](https://github.com/bryan-basg/samd-starter-kit/commit/491a9a8a) — Sincronización de reglas de Boy Scout (oportunista) y mutation score (≥90% solo en clínicos, piso de ≥75% en resto) desde el proyecto de referencia. Agregada skill y comando `commit-selectivo-parcial`. (Autor: Claude Sonnet 5).
