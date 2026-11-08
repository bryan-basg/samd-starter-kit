---
description: Antes de lanzar una ola de auditoría con agentes (buscar defectos en una capa) y antes de fichar lo que traigan — brief obligatorio de 4 cláusulas, refutador independiente y clasificación en cubos 🔴/🟡/🧊.
---

Vas a lanzar agentes a **BUSCAR defectos**, no a arreglarlos, en el proyecto {{PROJECT_NAME}}. El riesgo propio no es el consumo (`/tandas-agentes`) ni la cohesión (`/anti-drift`): es **la veracidad del hallazgo** — que sea falso, que ya esté arreglado o que su arreglo sea peor que el defecto.

**Una ola no se juzga por cuántos hallazgos trae, sino por cuántos sobreviven a la refutación.**

## Las 5 trampas

1. La ficha **ya estaba arreglada**.
2. La **premisa del brief es falsa** (a veces escrita por el propio orquestador) y el agente la obedece.
3. El arreglo pedido es **PEOR que el defecto** ⇒ etiqueta **⛔ NO HACER**.
4. Un **test verde afirma el defecto** como contrato.
5. La **excusa heredada** («irreducible», «no cubrible») sobrevive porque nadie la remidió.

## Antes de lanzar

1. Recontá el inventario con **UNA sola implementación**; lo comparable es el delta.
2. Derivá la lista del **código o del disco**, nunca a mano.
3. Verificá vos lo barato (¿existe `ruta/archivo.py::símbolo`?): se lee, no se delega.
4. Decile a {{OWNER}} el **número de agentes y el costo estimado** antes de lanzar.

## Brief obligatorio — 4 cláusulas LITERALES en cada agente

1. **«REFUTÁ la premisa antes de obedecer.»** Si es falsa, decilo y pará.
2. **«No encontrar nada es un resultado válido.»** Prohibido inflar con observaciones de estilo.
3. **«Toda ficha declara su CUBO»**: 🔴 daña a un paciente / expone o pierde datos / impide usar la app · 🟡 WCAG, GDPR, ISO 14971, trazabilidad · 🧊 calidad interna o producto sin decidir (NO es deuda). La prioridad P1/P2/P3 no dice el cubo.
4. **«Traé EVIDENCIA ejecutable, no prosa»**: `archivo::símbolo` + comando que lo demuestra + qué verías si estuviera sano. Sin forma de reproducirlo, no se ficha.

## Hallazgo clínico o de seguridad

Lo **refuta otro agente** antes de tocar código (§5.6), con lentes distintos (correctitud · seguridad · «¿reproduce?»), no revisores repetidos.

## Al recibir

Leé el `git diff` REAL o abrí el `símbolo` citado (nunca el summary) · recontá con la misma implementación y reportá el delta · **clasificá en cubos ANTES de escribir el índice** · un hallazgo no verificado ≠ deuda (se reporta como descartado y por qué) · cerrá por `/cierre-bloque`.

Procedimiento completo y razonamiento de cada trampa: skill `/ola-auditoria`.
