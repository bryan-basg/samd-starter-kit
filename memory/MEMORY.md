# Memory Index — {{PROJECT_NAME}}

> **Reglas estables del proyecto** (bugs conocidos, comandos, testing, protocolo con el dueño) viven en `CLAUDE.md`. Esta memoria es para **snapshots dinámicos** y estado puntual que cambia: estado de tests, hallazgos de sesión, lecciones puntuales, estado del plan.
>
> Entradas del índice = **1 línea** (`- [Título](archivo.md) — gancho`). El detalle vive en cada ficha. Mové el detalle a archivos por tema; no infles este índice.

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

## Último cierre (YYYY-MM-DD)

<!-- - [Título](archivo.md) — qué se cerró, commit, estado en prod, pendientes. -->
