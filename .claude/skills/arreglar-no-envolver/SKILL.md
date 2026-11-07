---
name: arreglar-no-envolver
description: INVOCAR ANTES de escribir un validador, un `try`/`except`, un `if` de guarda, un tipo más estricto o un envoltorio sobre código que YA EXISTE — y ante cualquier arreglo que no borre líneas del archivo con el defecto. Da el test decisivo para saber si estás arreglando o solo tapando.
---

# `/arreglar-no-envolver` — ¿arreglás o solo tapás?

## 🔔 CUÁNDO SE DISPARA (no hace falta que nadie la invoque a mano)

Se activa **sola**, antes de escribir el código, en cuanto se cumple **una** de estas:

1. **Vas a escribir** un `try`/`except`/`catch`, un `if x is None` de guarda, un `assert`, un validador de schema **sobre un dato que ya está dentro del sistema**, un tipo más estricto, o una función que envuelve a otra.
2. **Tu arreglo NO borra líneas** del archivo donde vive el defecto (solo añade, ahí o al lado).
3. **La ficha de deuda usa las palabras** «validar», «comprobar», «blindar», «proteger», «asegurar que no sea nulo», «defensivo».
4. **Estás en el archivo del síntoma, no en el del origen** — el dato llegó mal desde otro sitio y lo estás corrigiendo donde explota.
5. **Ya existe una comprobación parecida** del mismo dato en otra capa (router / servicio / helper / componente).

Si ninguna se cumple, seguí sin más: esta skill no aplica a código nuevo ni a la frontera. Es un criterio, no un procedimiento con comandos: leé las señales, respondé el **test decisivo** (paso 5) y, si igual hay que añadir protección, dejá la justificación escrita **en el código** o en la ficha de deuda.

> Los **patrones que SÍ son reescribir** y los **anti-patrones típicos**: [reference.md](reference.md) — leelo cuando el procedimiento no alcance para decidir.

## ⚠️ EL FILO — esto NO deroga la validación obligatoria

Esta skill **no** dice «quitá validaciones». Tres capas de protección son **innegociables**:

1. **Validación de FRONTERA** — lo que entra del exterior (schemas de request, validador del cliente, `max_length` de un campo que escribe un usuario). Un dato ajeno se valida **una vez, donde entra**.
2. **Fail-safe clínico (ISO 14971)** — degradar hacia MÁS alerta ante lo desconocido, el marcador `estimated`, el estado `unclassified`, el fusible 503. Es **comportamiento del producto**, no protección de código.
3. **Guardas de seguridad en el punto de decisión** — el JWT, el portero de acceso, el tope de escritura. Uno, en su sitio, derivado de una fuente viva.

**La diferencia, en una frase:** la protección legítima vive **en la frontera y se ejecuta UNA vez**; la que esta skill prohíbe vive **encima de la lógica y se repite** porque nadie confía en lo que hay debajo.

## Las 6 señales de que estás ENVOLVIENDO en vez de arreglar

Si marcás **una sola**, no escribas el parche: seguí al procedimiento.

1. **El mismo dato se valida en tres sitios distintos.** El problema no es que falte una cuarta comprobación: es que **el dato no nace válido**. Que nazca válido, o una **puerta única** que lo derive.
2. **Tu `try/except` (o `try/catch`) no puede nombrar qué falla.** `except Exception: pass` no protege: oculta (y a veces **causa** la fuga que decía prevenir: ver el anexo).
3. **Añadís un tipo más estricto para que el compilador avise de algo que el código ya no debería poder hacer.** Si necesitás `NonEmptyList`, preguntate por qué la función acepta listas vacías: muchas veces **hace dos cosas** y hay que partirla.
4. **El envoltorio tiene el mismo nombre que lo envuelto, con un prefijo** (`safeGetUser`, `validatedParse`, `checkedDivide`, `_wrapped_send`): casi siempre significa *«lo de abajo no se puede usar tal cual y no me atreví a tocarlo»*.
5. **El código crece en el sitio equivocado.** Si el archivo con el defecto queda igual y el de al lado crece 40 líneas, envolviste.
6. **El defecto puede volver por otra puerta.** *«Si mañana alguien llama a la función original sin pasar por mi envoltorio, ¿vuelve el defecto?»* Si sí, tu arreglo es un consejo, no un control.

## Procedimiento (5 pasos, en orden)

1. **Nombrá el defecto en una frase, sin la palabra «validar».** Si solo sabés decir *«hay que validar que X no sea nulo»*, todavía no entendiste: ¿**por qué** llega nulo? ¿Quién lo produce?
2. **Buscá el productor, no el consumidor** (`grep` el origen). ¿Entrada de usuario ⇒ frontera, validá ahí UNA vez? ¿BD ⇒ ¿falta un `NOT NULL` o un `CHECK`? ¿Otra función nuestra ⇒ **ese** es el defecto, no el sitio donde explota.
3. **Preguntate si el estado inválido puede dejar de EXISTIR.** De mejor a peor:

   | | Estrategia | Ejemplo |
   |---|---|---|
   | 🥇 | **Hacer el estado imposible** | Un `Record<Salida, Estado>` que **no compila** si añadís una salida sin estado |
   | 🥈 | **Puerta única derivada** | Una función que traduce el dato, usada por TODOS los consumidores |
   | 🥉 | **Validar en la frontera** | Un `max_length` en el schema de entrada, una vez |
   | ❌ | **Envolver el uso** | Un `if` defensivo en cada sitio que lo consume |

4. **Si vas a añadir protección, justificá EN EL CÓDIGO por qué NO se puede reescribir.** Vale por tres motivos y solo tres: **es la frontera** · **es fail-safe clínico declarado** (con su referencia a la matriz de riesgos) · **el productor es de terceros**. «No me animo a tocarlo», «rompe muchos tests», «lo hago después» **no es justificación: es una ficha de deuda** en `TECHNICAL_DEBT_SUMMARY.md`. Un envoltorio sin ficha es deuda invisible.
5. **Verificá con el test decisivo**: llamá a la función original **saltándote tu protección**. Si el defecto vuelve, no cerraste nada. El control real es el que **no se puede eludir**. (Es el mismo sabotaje del ENCHUFE de `CLAUDE.md` §Análisis de impacto, aplicado a un arreglo defensivo.)

## Qué reportar al terminar

1. **¿Borré código o lo apilé?** Líneas añadidas vs quitadas **en el archivo del defecto**.
2. **¿El defecto puede volver por otra puerta?** Nombrá las puertas y decí cuál cubre tu arreglo.
3. **Si añadí protección, ¿bajo cuál de los tres motivos válidos?** Si no encaja en ninguno, el envoltorio va con **ficha de deuda abierta**, no en silencio.
