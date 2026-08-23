---
description: Actualiza la memoria privada del agente al cerrar una jornada o lote — ficha por tema, una línea en el índice, y compresión de las viejas en la MISMA pasada.
---

Sos el que guarda lo aprendido en la **memoria privada del agente** (la carpeta `memory/` de este proyecto y su índice `MEMORY.md`). **No es el expediente DHF ni `CLAUDE.md`**: acá van *snapshots* y *lecciones*, no reglas ni inventarios.

## PASO 0 — el filtro (lo que más ahorra)

**NO va a memoria**: una regla estable (→ `CLAUDE.md` o `.claude/rules/`), un procedimiento repetible (→ una skill), el inventario de deuda o un cierre (→ `docs/08_verification_and_audits/`), la estructura del código o la historia de un fix (→ el repo ya lo guarda), algo que solo importa en esta conversación (→ ningún sitio).

**SÍ va**: el estado con el que hay que **RETOMAR** y las **lecciones que costaron caro** (modos de fallo, premisas falsas, trampas de herramienta). Si dudás: *¿me haría falta dentro de un mes, y no puedo deducirlo del repo?*

## PASO 1 — la ficha (una por TEMA, no una por sesión)

Frontmatter: `name` (slug kebab), `description` (una línea con los números y la lección), `metadata.type` ∈ `user`·`feedback`·`project`·`reference`. Reglas: fechas **absolutas**; **números medidos con su fuente**; la **lección primero y en una frase**; enlaces `[[slug]]` a fichas relacionadas; **≤ ~6 KB**. ⚠️ `[[…]]` es sintaxis de memoria — **nunca en `docs/`**, ahí rompe el link-checker.

## PASO 2 — actualizá primero, creá después

Buscá si ya existe una ficha del tema antes de crear otra. Si una ficha resultó **falsa**, borrala: una ficha equivocada es peor que ninguna.

## PASO 3 — el índice, y la regla que impide que explote

`MEMORY.md` se carga **entero en cada sesión**: cada byte se paga siempre. Una línea por ficha (`- [Título](archivo.md) — gancho`), nunca contenido. 🔒 **Comprimí las viejas en la MISMA pasada en que añadís** — no "después". Un lote cerrado y ya en producción baja a 2-3 líneas con su commit.

## PASO 4 — verificación (números, no impresión)

`wc -c` del índice **antes y después**; barrido de `[[slug]]` rotos contra los archivos de la carpeta; `ls -S | head -5` por si alguna ficha se pasó de ~6 KB. Un `[[slug]]` roto no es un marcador de trabajo futuro: es un error de tecleo que nadie va a encontrar.

## PASO 5 — lo que NO se escribe nunca

Un estado como si fuera un hecho presente (toda ficha es **una foto del pasado** — y al leerla, verificá contra `git log` y el código antes de creerle); un logro sin su límite; secretos, credenciales o PHI.

## Cierre

Reportá: fichas creadas/actualizadas/borradas, tamaño de `MEMORY.md` antes y después, y enlaces rotos encontrados. Si el índice creció, explicá por qué.

Procedimiento completo: skill `/memoria`.
