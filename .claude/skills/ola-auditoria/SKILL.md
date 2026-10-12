---
name: ola-auditoria
description: Invocar ANTES de lanzar una ola de auditoría con agentes (buscar defectos en una capa), y ANTES de fichar lo que traigan. El riesgo no es el consumo ni la cohesión, es que el hallazgo sea FALSO, ya esté arreglado, o traiga un arreglo peor que el defecto. Trae el brief obligatorio y la clasificación en cubos (🔴/🟡/🧊).
---
Vas a lanzar agentes a **BUSCAR defectos**, no a arreglarlos. El riesgo propio es **la calidad del hallazgo**.

> **Las tres hermanas se usan juntas**: `/tandas-agentes` → el **CONSUMO** (tamaño, costo, parar entre tandas) · `/anti-drift` → la **COHESIÓN** (contrato literal, `git diff` real) · **esta** → la **VERACIDAD** de lo que se ficha.
> El razonamiento completo detrás de cada trampa: [reference.md](reference.md).

## La regla que gobierna todo lo demás

**A un agente al que le pedís que encuentre, encontrar es cómo justifica el viaje**: si no aparece nada, baja el umbral hasta encontrar algo — y lo que aparece con el umbral bajo tiende a ser ruido de prioridad baja por construcción, no señal real. ⇒ **Una ola no se juzga por cuántos hallazgos trae, sino por cuántos sobreviven a la refutación.**

## Las 5 trampas típicas de una ola de auditoría

1. **La ficha ya estaba arreglada** — se reabre algo que ya no existe en el código actual.
2. **La premisa del brief es falsa**, a veces escrita por el propio orquestador, y el agente la obedece sin chequearla.
3. **El arreglo que la ficha pide es PEOR que el defecto** ⇒ etiqueta **⛔ NO HACER** en vez de ejecutarlo.
4. **Un test verde AFIRMA el defecto como contrato**: el test verifica que el bug ocurra, no que esté ausente.
5. **La excusa heredada** («irreducible», «desproporcionado», «no cubrible») sobrevive solo porque nadie la remidió — remedida, casi siempre cae.

## Antes de lanzar

1. **Recontá el inventario con UNA sola implementación** — lo comparable es el **DELTA** antes/después con la misma, nunca el absoluto de otra sesión.
2. **Derivá la lista del CÓDIGO o del DISCO, nunca a mano**: una lista a mano incluye lo que ya no existe y no encuentra a la hermana.
3. **Verificá vos mismo lo barato.** «¿Existe X en `archivo:línea`?» se resuelve leyendo, no lanzando un agente.
4. **Decile a {{OWNER}} el número de agentes y el costo estimado ANTES de lanzar**: un brief que exige refutar la premisa cuesta sensiblemente más que uno mecánico — presupuestá por el TIPO de brief (`.claude/rules/orquestacion.md`, regla B).

## El brief obligatorio — 4 cláusulas, literales

Metelas **textuales** en cada agente; cada una ataca una de las trampas de arriba:

1. **«REFUTÁ la premisa antes de obedecer.»** Si el diagnóstico que te doy es falso, **decilo y pará** — no entregues un arreglo impecable sobre una premisa falsa.
2. **«No encontrar nada es un resultado válido.»** Reportá el área como limpia en vez de bajar el umbral. **Prohibido inflar con observaciones de estilo.**
3. **«Toda ficha que abras declara su CUBO»** — 🔴 (daña a un paciente · expone o pierde datos · impide usar la app) · 🟡 (WCAG · GDPR · ISO 14971 · trazabilidad) · 🧊 (calidad interna · producto sin decidir, **NO es deuda**). ⭐ **La prioridad nominal (P1/P2/P3) NO dice el cubo.** Test de bolsillo: *«si esto sigue roto un año, ¿alguien sale perjudicado, o solo el código es más feo?»*.
4. **«Traé EVIDENCIA ejecutable, no prosa.»** `archivo::símbolo` (la línea, solo como ayuda para encontrarlo hoy: lo que se escriba en `docs/` va por símbolo) + el comando que lo demuestra + qué verías si estuviera sano. Un hallazgo sin forma de reproducirlo **no se ficha**.

## Hallazgo clínico o de seguridad ⇒ REFUTADOR independiente (§5.6, obligatorio)

Un hallazgo que dispare cambio en algoritmo clínico, schema, regla de negocio o flujo de seguridad **lo refuta otro agente antes de tocar código**. No es opcional y no es el mismo agente. **Lentes distintos, no revisores repetidos** (correctitud · seguridad · «¿reproduce?»).

## Al recibir lo que traen

1. **Leé el `git diff` REAL, nunca el summary** (`/anti-drift`). En una ola de solo lectura el equivalente es **abrir el `archivo:línea` que citan**.
2. **Recontá con la MISMA implementación del paso 1** y reportá el delta.
3. **Clasificá en cubos ANTES de escribir el índice.** Sin esto la ola vuelca la mayoría de sus P2/P3 en 🔴 y deshace la separación en una sola tanda.
4. **Un hallazgo no verificado ≠ deuda.** Si no sobrevivió a la refutación, no se ficha: se reporta como descartado y **por qué**.
5. **Cerrá por `/cierre-bloque`** — trazabilidad DHF y poda, aunque la ola «solo mire».

## Cuándo NO usar esta skill

* **Arreglar** deuda ya fichada y verificada → `/tandas-agentes` a secas.
* **Elegir** mejoras de fondo con menú y decisión de {{OWNER}} → `/mesa-ingenieros`.
* **Un símbolo puntual** y sus consumidores → `/samd-trace`, sin agentes.
* **Diagnóstico abierto sin hipótesis** → chat principal (`.claude/rules/orquestacion.md`, regla E): repartir agentes sobre un problema que aún no entendés multiplica el ruido, no la señal.
