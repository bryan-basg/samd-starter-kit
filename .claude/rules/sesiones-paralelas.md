# SESIONES PARALELAS — varias ventanas sin choques (consecuencia SaMD §5.7 — verificación fiable)

> Regla **transversal** del cerebro SaMD, en archivo aparte por legibilidad del core — **NO lleva `paths:`**, así que carga en cada sesión igual que `CLAUDE.md`. Mapa completo: `CLAUDE.md` §MAPA DE ESTE CEREBRO.
>
> **Esto es OTRA cosa que la orquestación de sub-agentes** (`.claude/rules/orquestacion.md`): aquello es un agente repartiendo trabajo; **esto es el dueño con varias ventanas de su herramienta de IA abiertas a la vez**, cada una con su propio contexto y sin saber de las otras.

## Por qué esta regla existe

El choque entre dos ventanas **no** es que "hablen a la vez": es que **editen el mismo archivo** o que **compartan un recurso de verificación**. Lo primero se resuelve repartiendo zonas. Lo segundo es más traicionero, porque no rompe nada visible — **devuelve un verde que miente**, y en un contexto regulado ese es el modo de fallo más caro que existe: firmás una verificación que nunca ocurrió.

## Repartí el repo en carriles, uno por ventana

Un reparto típico (adaptalo a tu estructura):

| Ventana | Zona del repo | Qué NO toca |
| --- | --- | --- |
| **A — Backend** | `app/`, `alembic/`, `tests/`, `scripts/*.py` | nada bajo `frontend/` |
| **B — Frontend** | `frontend/src/`, `frontend/e2e/` | nada bajo `app/`; ni los locales (son de C) |
| **C — Infra, idiomas y docs** | `.github/`, `scripts/*.sh`, locales, capa nativa, `docs/` | código de `app/` y `frontend/src/` |

**Las tareas que cruzan zonas NO se reparten.** Se hacen **de a una, con las otras ventanas quietas**: los tipos generados del contrato, los campos que atraviesan backend↔frontend, la medición de mutación, el techo del pool. Ante la duda de si una tarea cruza: **cruza**.

## Reglas duras de convivencia

1. **`git add` explícito, archivo por archivo. NUNCA `git add -A` ni `-u`.** Con varias ventanas, un `-A` se lleva al commit el trabajo a medias de las otras.

   ⚠️ **Y el `add` explícito NO alcanza — esto es mecánica de git, no descuido.** El índice de git es **UNO por repositorio**. Si la otra ventana ya preparó sus archivos, un `git commit` normal **se los lleva igual**, por más cuidado que hayas tenido con tu `add`, dentro de un commit cuyo mensaje no los describe. La forma que sí protege es:

   ```bash
   git commit -m "<mensaje>" -- <tus rutas>
   ```

   Ignora el índice para todo lo que no nombres y **deja intacto lo que la otra ventana tenía preparado**. Comprobación previa innegociable: `git diff --cached --name-only` **justo antes de commitear** — si ahí aparece algo que no es tuyo, la forma con rutas pasa de preferible a **obligatoria**.

   Esto protege lo tuyo de irse; **no impide** que la otra ventana se lo lleve con un `-A`. Desde una sola ventana no se puede garantizar en ambos sentidos.
2. **Un solo escritor de documentos.** Las ventanas de código dejan sus notas de cierre en un archivo propio del scratchpad y la ventana de docs las consolida al cerrar. Varias ventanas escribiendo el mismo `.md` es el conflicto garantizado.
3. **Tipos generados del contrato: nunca en paralelo.** Si una ventana cambia un endpoint, avisa; la otra regenera **después**, jamás a la vez — y desde un `git worktree` limpio cuando hay trabajo sin commitear.
4. **Procesos pesados: uno a la vez en toda la máquina.** Mutación, cobertura completa, suite E2E, escaneos. Un "vamos con todo" en una ventana **no** autoriza que otra lance lo suyo en paralelo.
5. **Los tests que comparten recurso necesitan aislamiento por proceso.** Dos corridas simultáneas de la suite que usan el mismo archivo de base de datos **se la borran entre sí**. Sufijá el recurso con el PID del proceso para que cada corrida tenga el suyo, y verificalo con sabotaje (sin el sufijo, debe romper).
6. **Bajá la concurrencia de las suites E2E cuando la máquina está compartida.** El techo pensado para "una sola cosa corriendo" satura la máquina entera si hay otras dos ventanas trabajando.
7. **Antes de cantar verde, mirá el `git status` completo, no solo tus archivos.** Si aparece trabajo de otra ventana a medio hacer, tu type-check o tu lint puede estar leyendo un archivo a mitad de edición. **El verde no vale hasta repetirlo con el árbol quieto.**

## Cómo arranca cada ventana

Al abrir una ventana, decile en qué carril está:

> Carril **A (backend)**. Lote de hoy: los índices y constraints de la base. No toco `frontend/` ni `docs/`.
