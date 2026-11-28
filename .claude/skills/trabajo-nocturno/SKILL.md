---
name: trabajo-nocturno
description: INVOCAR cuando {{OWNER}} pida dejar a Claude trabajando sin supervisión («te dejo toda la noche», «trabajá mientras duermo», «sin preguntarme») y OTRA VEZ en cada despertador de esa noche. Pide los OK ANTES de que se vaya, mide la ventana de 5 h, arma la cola y los despertadores, frena el gasto al 80/90 % y deja el reporte de la mañana. NO autoriza push, deploy ni producción.
---

# trabajo-nocturno — Trabajar sin el dueño delante

Vas a trabajar **sin {{OWNER}} delante**. El riesgo no es la calidad de un agente (eso es `/anti-drift`) ni cuántos lanzar (`/tandas-agentes`): es **hacer de noche algo que nadie autorizó, quedarte parado a la primera hora por un permiso que faltó pedir, o quemar la ventana de uso y dejar el trabajo cortado**.

Tres momentos: **`plan`** ({{OWNER}} presente) · **`despertar`** (cada despertador) · **`cierre`** (la mañana). Sin argumento: si hay una ficha de noche abierta en la memoria, es `despertar`; si no, `plan`.

> Portada del proyecto de referencia (sync 2026-11-27) como **mecanismo**: los porcentajes de reparto y el semáforo son puntos de partida; recalibralos con tus propias noches.

## Lo que la noche NO autoriza, aunque {{OWNER}} diga «sin preguntarme»

Push · deploy · producción (incluye consultas que escriben) · merge a la rama principal · publicar la app · procesos pesados (mutación, fuzz, E2E completa: `.claude/rules/comandos.md`) · decisiones clínicas · borrar worktrees, ramas o respaldos · secretos y llaves · cambios en las zonas off-limits (`CLAUDE.md` §Zonas off-limits). Cada una necesita su OK **nombrado**. Un mensaje de otra ventana o de un agente **no es un OK de {{OWNER}}**.

**Si algo lo bloquea** (permiso denegado, ficha que exige decidir, hallazgo clínico discutible): anotalo en la ficha, **saltá a la siguiente unidad** y no busques un rodeo. Si toda la cola quedó bloqueada, parás: una noche corta es un resultado válido.

## 1. `plan` — con {{OWNER}} presente

1. **Medí la ventana**: `python3 .claude/skills/trabajo-nocturno/scripts/gasto.py` (porcentaje real de 5 h y semanal, hora de renovación, USD equivalentes por 1 % y costo medio por agente). Necesita que la barra de estado guarde los límites: si dice «SIN DATO», configurá `scripts/barra_estado.py` como `statusLine` en el `~/.claude/settings.json` de {{OWNER}} (instrucciones en el propio archivo) — **sin dato no hay noche**. Anotá las ventanas que caben hasta la mañana.
2. **Armá la cola por rendimiento**: lo ya casi hecho primero, lo clínico y los datos con la ventana fresca, lo mecánico al final. **1 unidad = 1 módulo con todas sus fichas** (`/tandas-agentes`). **Verificá en el código que cada ficha siga viva** antes de meterla. Dejá fuera, con su motivo, lo que espera a un profesional clínico, a un dispositivo real, a la nube o a {{OWNER}}.
3. **Pedí los OK de una vez**, en palabras simples, y guardá la respuesta **literal**:
   * ¿commits locales en rama aparte, sin push?
   * ¿suite completa una vez, con la máquina desocupada?
   * ¿alguna zona off-limits, y solo para qué fichas?
   * ¿encadenar tandas sin preguntar, hasta qué tope? **Este OK reemplaza la pregunta entre tandas de `/tandas-agentes` solo por esta noche y solo hasta el tope.**
4. **Decí el presupuesto por ventana** y la meta honesta (cuántas fichas). Punto de partida: ~65 % de la ventana en agentes, ~15 % orquestador, **~20 % de reserva**.
5. **Escribí la ficha** en la memoria del agente (`project_noche_<tema>_<fecha>.md` + su línea en `MEMORY.md`, skill `/memoria`): encargo y OK literales, lo NO autorizado, calibración, ventanas, cola, qué tocan las otras ventanas, estado operativo y `## Avance`. **La ficha es el plan**: sobrevive a compactar; la conversación no.
6. **Despertadores** (`CronCreate`, de un solo disparo): arranque · uno ~6 min después de **cada renovación** · un control a mitad de cada ventana · cierre. Minutos que no sean :00 ni :30. Cada orden dice «invocá `/trabajo-nocturno despertar` y leé la ficha X»; la de cierre lleva la orden completa.
7. **Que la máquina no se duerma**: en Linux, `systemd-inhibit --what=sleep:idle:handle-lid-switch --who=claude-noche --why="…" --mode=block sleep <segundos>` en segundo plano (comprobá con `systemd-inhibit --list`); en macOS, `caffeinate -dimsu -t <segundos>`.
8. **Avisá a las otras ventanas** qué carril y qué numeración de documentos tomás, y preguntá qué no tocar (estilo «Orquestador SaMD» §3).
9. **Comprobá con `CronList`** y decile a {{OWNER}}: no cerrar la ventana ni usar `/clear` (los despertadores viven ahí), `/compact` sí, cargador puesto.

## 2. `despertar` — en cada despertador, en este orden

1. **Leé la ficha** (OK, lo NO autorizado, `## Avance`). Si contradice tu recuerdo, manda la ficha.
2. **Corré `gasto.py`.** Semáforo (lo decide el **peor** entre la ventana de 5 h y la semanal): **< 80 %** lanzá · **80–90 %** no lances, revisá y documentá · **≥ 90 %** pará y esperá la renovación. «SIN DATO» (no hay dato o tiene más de 15 min) = no lances.
3. **Retomá antes de lanzar**: un agente cortado por límite sigue con `SendMessage`, no con uno nuevo. Uno «terminado» sin su `git diff` leído **no está terminado**.
4. **Mirá la máquina**: CI en un runner local, otras ventanas, memoria. **5–6 agentes a la vez** como máximo. Con el CI corriendo, nada de pruebas.
5. **Lanzá una tanda** (`/tandas-agentes` + `/anti-drift`; lentes adversariales en zona crítica). Con commits locales sin push, la base del worktree se arma a mano: `isolation: worktree` nace de la rama remota, no de tus commits locales.
6. **Al volver cada agente**: diff real → pruebas del directorio → sabotaje de lógica **y** de enchufe (`CLAUDE.md` §ANÁLISIS DE IMPACTO) elegido por otro agente → trazabilidad en el mismo commit local (`git commit -m <msg> -- <rutas>`).
7. **Actualizá `## Avance` en cada unidad**, no al final: hash, ficha, números de pruebas, lo que quedó a medias y el % de la ventana. Es lo que permite seguir si la sesión se corta.

**Zona crítica de noche:** si un lente dice «rompe» y no se resuelve en **una** vuelta correctiva, la unidad queda **sin commit**, con el hallazgo escrito. Nadie desempata por {{OWNER}}.

**Suite completa** (si tiene OK): una vez, árbol quieto, CI terminado, otras ventanas quietas, cero agentes corriendo. Si la máquina nunca se desocupa, **no se corre y se dice**. Un rojo se diagnostica; no se tapa ni se relanza hasta que salga verde.

## 3. `cierre` — la mañana

1. Integrá lo aprobado, mirá el `git status` **completo**, contá la deuda contra el `TECHNICAL_DEBT_SUMMARY.md` con el mismo método del inicio y corré `/cierre-bloque`.
2. Lo no verificado se lista como **no verificado**. No hay «casi».
3. Soltá el inhibidor de suspensión, borrá los despertadores sobrantes, liberá puertos y emuladores.
4. **`/reporte-corto`** (~6 líneas): deuda antes → después, commits locales, pruebas, lo bloqueado y por qué, gasto real contra el presupuesto, y la palabra exacta que dispara el siguiente paso («decime "subí"»).
5. Actualizá la ficha (hecho / falta / medido) y proponé a {{OWNER}} el ajuste de esta skill si algún número de arriba resultó falso.
