---
description: Reparte un trabajo grande en TANDAS de máximo 12 subagentes, con parada obligatoria y OK del dueño entre tanda y tanda — presupuesto medido, verificación del diff real y recuperación si una tanda muere a mitad.
argument-hint: <el trabajo a repartir, p.ej. "los 43 avisos de lint">
---

Vas a repartir un trabajo grande entre subagentes en el proyecto {{PROJECT_NAME}}. **El riesgo que este comando ataca NO es la calidad (eso es `/anti-drift`): es el CONSUMO.** Una tanda encadenada tras otra sin preguntar quema la cuota de {{OWNER}} en una tarde, y el modo de fallo real no es "sale caro": es que el límite se agote a mitad de una tanda y los agentes mueran **con el trabajo escrito y sin verificar**.

## Las 2 reglas duras

1. **Máximo 12 agentes por tanda** (regla B de `.claude/rules/orquestacion.md`), contando **todos**: los que trabajan Y los que verifican. Un pipeline de 12 ítems con 2 revisores cada uno son **36 agentes**, no 12.
2. **Entre tanda y tanda, PARÁS y PREGUNTÁS.** Nunca encadenes la siguiente por tu cuenta, aunque el plan la contemple. **"Vamos con todo" autoriza el PLAN, no el GASTO de cada tanda** — igual que no autoriza procesos pesados implícitos (regla dura 2 de orquestación).

## Presupuesto — decilo ANTES de lanzar

Órdenes de magnitud medidos en un proyecto SaMD real (recalibralos con tus corridas; lo que se porta es la relación):

| Tipo de brief | Por agente | Tanda de 12 |
| --- | --- | --- |
| **Mecánico** (refactor guiado, killers, patrón conocido) | ~95 k tokens | ~1,1 M |
| **Investigativo** (verificar la premisa antes de obedecer) | **~200 k tokens** | **~2,4 M** |

El investigativo cuesta el doble y **lo vale**: en la tanda que fijó ese número, cuatro agentes corrigieron la premisa, dos de ellas erróneas del propio orquestador. Si el trabajo total pide más de 2 tandas, decilo **antes de la primera**.

## Los pasos

1. **Listá el trabajo total** en unidades independientes. Agrupá **por archivo**, nunca por hallazgo: dos agentes sobre el mismo archivo se pisan.
2. **Partí en tandas de ≤12**, ordenadas por rendimiento: lo barato y de bajo riesgo primero, lo delicado al final.
3. **Presentá el plan con el costo estimado y esperá OK.**
4. **Lanzá UNA tanda.** Nunca dos a la vez (comparten máquina; puede haber otras ventanas abiertas — `.claude/rules/sesiones-paralelas.md`).
5. **Verificá vos el `git diff` REAL**, no el summary (`/anti-drift`): medida objetiva, type-check, tests del módulo y `git status` por temporales y huérfanos.
6. **Reportá y PREGUNTÁ**: qué se hizo, cuántos tokens costó, qué encontraron los revisores y qué falta.

## Si una tanda muere a mitad

No asumas que quedó ni bien ni roto: **medí**. Buscá **huérfanos** (archivo nuevo que nadie importa — el modo de fallo del ENCHUFE de `CLAUDE.md`), **temporales** (`git status --short | grep "^??"`), y anotá como deuda los **revisores que no llegaron a correr**: tests verdes ≠ revisión adversarial.

## Contrato de la tanda (literal en cada brief)

1. **No cambies un aviso de lint por un test rojo.** Prohibido subir el límite de un ratchet.
2. **Archivo nuevo ⇒ añadilo a la config del medidor de mutación**, o el score queda igual midiendo menos superficie.
3. **Corré los tests del DIRECTORIO**, no los del archivo.
4. **Sin huérfanos ni temporales.**
5. **Hay guardianes que leen TEXTO, no conducta** — el sabotaje de comportamiento es ciego ante ellos.
6. **Los killers de los módulos críticos son un CONTRATO**: tocar el literal obliga a tocar su killer en el mismo cambio.

Verificación adversarial con **lentes distintos** (equivalencia lógica · seguridad clínica · contratos y guardianes). En zona crítica, **basta que UN lente diga "rompe"** para bloquear.

Procedimiento completo y contexto: skill `/tandas-agentes`.
