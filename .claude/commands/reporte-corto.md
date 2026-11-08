---
description: Antes de escribir el mensaje con el que le cerrás a {{OWNER}} una tarea, un paso o una tanda (o resumís lo que devolvió un agente o un CI) — formato corto de ~6 líneas (qué pasó, qué necesita de él, qué recomendás).
---

Vas a cerrarle a {{OWNER}} una tarea del proyecto {{PROJECT_NAME}}. {{OWNER}} lee el **resultado**, no el camino. El reporte cabe en la pantalla de un celular: **~6 líneas como máximo, sin títulos ni tablas**.

## Formato

```
✅ <qué quedó hecho, una línea, con el dato que lo prueba: hash, «188 tests ✅», «CI 6/6 ✅»>
⚠️ <solo si algo salió distinto de lo esperado o apareció un riesgo nuevo>
⏳ <solo si algo sigue corriendo o esperando>
👉 <solo si necesito algo de vos: la decisión o el OK, con la palabra exacta que lo dispara>
💡 Recomiendo: <una frase>.
```

⚠️, ⏳ y 👉 van **solo si tienen contenido**. Una tarea limpia son 2 líneas (✅ + 💡).

## Qué SÍ entra

El resultado y su prueba en un número · lo que salió distinto (un rojo, una sorpresa, un supuesto falso) · lo que espera una decisión de {{OWNER}} · un riesgo nuevo (clínico, de seguridad, de datos o de costo).

## Qué NO entra

Cómo lo hice (comandos, `git add` explícito, hooks) · reglas que cumpliste · rutas y citas de código salvo que {{OWNER}} deba abrir el archivo · lo que ya sabe · verificaciones normales una por una (eso queda en `docs/`).

> Esto acota lo que se **cuenta**, no lo que se **hace**: trazabilidad, verificación con números y poda siguen siendo obligatorias (Regla 0). Callar un rojo, un riesgo nuevo o una verificación que no pudo correrse **no es brevedad, es ocultar**: va siempre, en ⚠️.

## Cuándo puede ser largo (solo 3)

1. Lectura guiada del diff antes de un commit con código.
2. Hallazgo clínico o de seguridad, incidente en producción o algo que se rompió.
3. {{OWNER}} pide el detalle.

Un agente que devuelve 80 líneas se reporta en ≤ 6. Modo tutor comprimido: el término nuevo necesario para decidir lleva una analogía corta entre paréntesis; lo demás se ofrece.

Procedimiento completo y ejemplo antes/después: skill `/reporte-corto`.
