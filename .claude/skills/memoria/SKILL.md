---
name: memoria
description: Actualiza la memoria privada del agente al cerrar una jornada o lote — ficha por tema, una línea en el índice, y compresión de las viejas en la MISMA pasada. Usala al cerrar un lote o jornada de trabajo, cuando haya algo que la próxima sesión necesite para RETOMAR, o cuando el dueño pida "acordate de esto".
---

# memoria — Guardar lo aprendido sin inflar el índice

Sos el que guarda lo aprendido en la **memoria privada del agente** (la carpeta `memory/` de este proyecto, con su índice `MEMORY.md`).
**No es el expediente DHF ni `CLAUDE.md`**: acá van *snapshots* y *lecciones*, no reglas ni inventarios.

## PASO 0 — ¿esto va a memoria? (el filtro que más ahorra)

**NO va a memoria** — si cae acá, escribilo en su sitio y salí:

| Lo que es | Dónde va DE VERDAD |
| --- | --- |
| Una regla estable que aplica siempre | `CLAUDE.md` (core) o `.claude/rules/*.md` |
| Un procedimiento repetible | una skill en `.claude/skills/` (+ su espejo en `.claude/commands/`) |
| El inventario de deuda, un cierre, trazabilidad | `docs/08_verification_and_audits/…` (manda sobre cualquier ficha) |
| Estructura del código, historia de un fix, `git log` | el repositorio ya lo guarda |
| Algo que solo importa en esta conversación | ningún sitio |

**SÍ va a memoria:** el estado con el que hay que **RETOMAR**, y las **lecciones** que costaron caro (modos de fallo, premisas que resultaron falsas, trampas de herramienta). Si dudás: *¿esto me haría falta dentro de un mes, y no puedo deducirlo del repo?*

## PASO 1 — la ficha (una por tema, no una por sesión)

Frontmatter obligatorio: `name` (slug kebab), `description` (una línea; es lo que se lee al decidir si abrirla — poné ahí los números y la lección), `metadata.type` ∈ `user` · `feedback` · `project` · `reference`.

* **Fechas relativas → absolutas.** "ayer" no significa nada dentro de un mes.
* **Números medidos, con su fuente.** "9949 passed" vale; "todo verde" no.
* **La lección va primero y en una frase**, antes del relato. Lo que se relee es la frase.
* **Enlazá con `[[slug]]`** a fichas relacionadas. Un `[[slug]]` que aún no existe está bien: marca algo que vale la pena escribir. ⚠️ **Pero un slug MAL ESCRITO no marca nada, solo rompe** — verificalo (paso 4).
* **Tope ~6 KB por ficha** (`CLAUDE.md` §Presupuesto de escritura). Si no entra, el detalle largo va al commit o al expediente, no acá.
* ⚠️ **`[[…]]` es sintaxis de MEMORIA. Nunca la escribas en `docs/`** (ni enlaces vacíos `](#)`): ahí rompe los guardianes del DHF y el link-checker.

## PASO 2 — actualizá primero, creá después

**Antes de crear una ficha, buscá si ya existe una que cubra el tema** (`ls` + `grep` sobre la carpeta). Actualizar la existente > duplicar. Si una ficha resultó **falsa**, borrala: una ficha equivocada es peor que ninguna.

## PASO 3 — el índice (`MEMORY.md`), y la regla que impide que explote

`MEMORY.md` se carga **entero en cada sesión**: cada byte se paga siempre.

* **Una línea por ficha**: `- [Título](archivo.md) — gancho`. Nunca contenido, nunca frontmatter.
* 🔒 **REGLA DURA: comprimí las viejas en la MISMA pasada en que añadís.** No "después". Medí el tamaño **antes y después** y **reportalo**: si `MEMORY.md` creció, comprimí más hasta que no crezca. Un lote cerrado y **ya en producción** baja a 2-3 líneas con su commit; el detalle vive en su ficha.
* Las entradas **agrupadas** (varios punteros en una línea) ya están comprimidas: no las toques.
* Si el índice viene **por encima de su límite** (~40 KB, `CLAUDE.md` §Presupuesto de escritura), la pasada tiene que dejarlo **más chico que como lo encontraste**, no solo "no peor".

## PASO 4 — verificación (números, no impresión)

```bash
M=<ruta de la carpeta memory/ de este proyecto>
wc -c "$M/MEMORY.md"                      # antes y después: ¿creció?
grep -oh "\[\[[a-z0-9_-]*\]\]" "$M"/*.md | tr -d '[]' | sort -u | while read -r s; do
  [ -f "$M/$s.md" ] || echo "ENLACE ROTO: [[$s]]"
done                                       # slug mal escrito ≠ ficha futura
ls -S "$M" | head -5 && du -sh "$M"        # ¿alguna ficha se pasó de ~6 KB?
```

Un `[[slug]]` roto **no es un marcador de trabajo futuro**: es un error de tecleo que nadie va a encontrar. Revisalo siempre.

## PASO 5 — lo que NO se escribe nunca

* **Un estado como si fuera un hecho presente.** Toda ficha es **una foto del pasado**. Escribila como foto ("al cerrar el 2026-08-22 quedaban 2 commits sin pushear"), no como verdad atemporal. Y al **leerla** en otra sesión: **verificá contra `git log` / el remoto / el código antes de creerle** — las cifras de deuda especialmente: **contá el índice**, nunca cites la ficha.
* **Un logro sin su límite.** Si algo quedó sin verificar, decilo en la misma línea. Una ficha que solo cuenta la parte buena hace daño dentro de un mes.
* Secretos, credenciales, PHI. Nunca.

## Cierre

Reportá al dueño: **qué fichas creaste/actualizaste/borraste**, el **tamaño de `MEMORY.md` antes y después**, y los **enlaces rotos que encontraste**. Si el índice creció, explicá por qué.
