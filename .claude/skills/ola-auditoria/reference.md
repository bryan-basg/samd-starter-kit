# `/ola-auditoria` — anexo: por qué cada trampa ocurre

> Anexo de `SKILL.md`. Se lee para entender o recalibrar una cláusula; el procedimiento vive en `SKILL.md`.

## Por qué una ola infla los hallazgos

A un agente al que le pedís que encuentre defectos, volver con «está todo bien» se lee como que no trabajó — así que, sin una regla explícita que lo autorice, baja el umbral hasta encontrar algo. Lo que aparece con el umbral bajo (observaciones de estilo, nombres de variable, preferencias cosméticas) es ruido de prioridad baja por construcción, no una ola de hallazgos reales. Por eso la cláusula 2 del brief («no encontrar nada es un resultado válido») no es cortesía: es la que apaga ese incentivo.

## Las 5 trampas, con su mecanismo

| # | Trampa | Por qué pasa |
| --- | --- | --- |
| 1 | **La ficha ya estaba arreglada** | El agente lista hallazgos desde una copia vieja del código, un grep contra un commit anterior, o memoria de una sesión previa — nunca contra el estado actual del archivo. |
| 2 | **La premisa del brief es falsa** — y a veces la escribió el propio orquestador | Un brief que da por cierto un diagnóstico sin que el agente lo verifique primero hereda cualquier error de quien lo escribió, amplificado por N agentes en paralelo. |
| 3 | **El arreglo que la ficha pide es PEOR que el defecto** | Sin refutación independiente, un arreglo mecánico puede resolver el síntoma literal y romper algo que el síntoma protegía (ej. aflojar una validación para que un test pase). De ahí la etiqueta **⛔ NO HACER**: a veces la acción correcta es no aplicar el arreglo propuesto. |
| 4 | **Un test verde AFIRMA el defecto como contrato** | Si el test fue escrito para que pase, no para que verifique la ausencia del bug, un test "verde" certifica el comportamiento roto en vez de detectarlo. |
| 5 | **La excusa heredada** («irreducible», «desproporcionado», «no cubrible») | Una vez que alguien etiqueta algo como no-abordable, nadie vuelve a medirlo — y la cifra o el supuesto que la originó puede estar mal desde el principio. |

## De dónde salen las cláusulas del brief

* **Refutar la premisa** (cláusula 1) existe porque el costo de NO hacerlo es trabajo perdido o dañino sobre un diagnóstico que nunca fue cierto.
* **Cubos** (cláusula 3): sin separar por cubo, una ola que nace con la mayoría de sus hallazgos en prioridad nominal baja (P2/P3) los vuelca igual en la sección 🔴 del reporte, porque "prioridad baja" y "cubo bajo" no son lo mismo — un hallazgo P3 puede ser 🔴 si de verdad daña a un paciente o filtra datos. Detalle de la clasificación: cláusula 3 del brief obligatorio en `SKILL.md`.
* **Recontar con UNA sola implementación** (paso 1 de "antes de lanzar"): dos formas distintas de contar el mismo inventario (ej. un script vs. un grep manual) suelen discrepar entre sí — lo comparable es el DELTA entre dos corridas de la MISMA implementación, nunca el absoluto de otra sesión con otro método.
