---
name: reporte-corto
description: INVOCAR ANTES de escribir el mensaje con el que le cerrás a {{OWNER}} una tarea, un paso o una tanda (también cuando resumís lo que devolvió un agente o cómo terminó un CI). Da el formato corto —qué pasó, qué necesita de él, qué recomendás— y la lista de lo que NO se cuenta (el procedimiento común).
---

# reporte-corto — {{OWNER}} lee el resultado, no el camino

> El problema que ataca: un reporte de cierre con demasiado contexto entierra lo único que {{OWNER}} necesita saber —qué quedó hecho, si algo salió distinto, qué se espera de él— bajo el relato de cómo se hizo. Quien dirige un proyecto SaMD tiene que decidir, y decide peor con 25 líneas que con 6.

El reporte de cierre cabe en la pantalla de un celular: **~6 líneas como máximo**, sin títulos y sin tablas.

## Formato

```
✅ <qué quedó hecho, en una línea, con el dato que lo prueba: hash, «188 tests ✅», «CI 6/6 ✅»>
⚠️ <solo si algo salió distinto de lo esperado o apareció un riesgo nuevo>
⏳ <solo si algo sigue corriendo o esperando>
👉 <solo si necesito algo de vos: la decisión o el OK, con la palabra exacta que lo dispara>
💡 Recomiendo: <una frase>.
```

Las líneas ⚠️, ⏳ y 👉 van **solo si tienen contenido**. Una tarea limpia son 2 líneas (✅ + 💡). La línea 💡 es la regla del core («terminá siempre con una recomendación, justificada en una frase corta»): este formato no la reemplaza, la encaja.

## Qué SÍ entra (lo relevante)

- El **resultado** y su prueba en un número.
- Lo que salió **distinto** de lo esperado: un rojo, una sorpresa, un hallazgo, un supuesto que resultó falso.
- Lo que espera **una decisión de {{OWNER}}**, con la palabra que la dispara («decime "subí"»).
- Un **riesgo nuevo**: clínico, de seguridad, de datos o de costo (tokens, horas de máquina).

## Qué NO entra (procedimiento común)

- **Cómo lo hice**: comandos, flags, `git add` explícito, «commit con rutas», «revisé el índice», hooks que pasaron.
- **Reglas que cumpliste**: si es la regla, se cumple sin anunciarlo.
- **Rutas de archivo y citas de código**, salvo que {{OWNER}} tenga que abrir el archivo.
- **Lo que {{OWNER}} ya sabe**: repetir el plan, recapitular turnos anteriores, re-explicar un concepto ya explicado.
- **Verificaciones que salieron normales**, una por una («0 enlaces rotos», «poda 0 elegibles»): eso queda en `docs/`. En el chat alcanza con el número de tests o «verificado ✅».

> ⚠️ **Esto acota lo que se CUENTA en el chat, no lo que se HACE.** La trazabilidad, la verificación con números y la poda siguen siendo obligatorias (Regla 0): solo que su evidencia vive en `docs/` y en el commit, no en el mensaje de cierre. Callar un rojo, un riesgo nuevo o una verificación que no pudo correrse **no es brevedad, es ocultar**: eso va siempre, en ⚠️.

## El modo tutor, comprimido

El modo tutor del core sigue, pero **en una línea**: el término nuevo que {{OWNER}} necesita **para decidir** lleva una analogía corta entre paréntesis. Lo demás se ofrece («¿te explico X?»). Nunca un párrafo de teoría dentro de un reporte de cierre.

## Cuándo el reporte puede ser largo (solo estas 3)

1. **Lectura guiada del diff antes de un commit con código**: una línea por cambio más el balance de líneas añadidas contra borradas.
2. **Hallazgo clínico o de seguridad, incidente en producción o algo que se rompió**: ahí el detalle ES lo relevante.
3. **{{OWNER}} pide el detalle** («explicame», «mostrame», «¿por qué?»).

## Ejemplo

❌ **Antes** (~25 líneas): títulos «Qué quedó guardado / Cómo va el CI / Lo que falta», una analogía de taller, que el índice no traía nada ajeno, qué ficha se cerró y cuál se abrió, por qué la medición no podía arrancar…

✅ **Después**:

```
✅ Commit `dfadb7a` guardado en tu PC (los 3 documentos de la capa 0). No lo subí.
⏳ El CI anterior sigue corriendo en tu PC.
💡 Recomiendo: cuando termine, decime «subí los docs»; la medición va después y pide tu OK.
```

## Informes de agentes y de CI

Mismo filtro: un agente que devuelve 80 líneas se reporta en ≤ 6. El detalle queda en el `git diff` y en `docs/`; si {{OWNER}} lo quiere, lo pide. (Para el `git diff` real y no el resumen del agente: `/anti-drift`.)
