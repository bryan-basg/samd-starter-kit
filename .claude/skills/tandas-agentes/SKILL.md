---
name: tandas-agentes
description: Reparte un trabajo grande en TANDAS de máximo 12 subagentes, con parada obligatoria y OK del dueño entre tanda y tanda — presupuesto estimado antes de lanzar, verificación del diff real y recuperación si una tanda muere a mitad. Usala cuando el trabajo no cabe en una sola tanda de agentes, o cuando vayas a encadenar una segunda ola de subagentes.
---

# tandas-agentes — Repartir sin quemar la cuota

Vas a repartir un trabajo grande entre subagentes. **El riesgo que esta skill ataca NO es la calidad (eso es `/anti-drift`): es el CONSUMO.** Una tanda encadenada tras otra sin preguntar quema la cuota de {{OWNER}} en una tarde, y el modo de fallo no es "sale caro": es que **el límite se agota a mitad de una tanda y los agentes mueren con el trabajo escrito y sin verificar** — el peor estado posible, porque parece hecho.

## Cuándo usarla

- El trabajo no cabe en una sola tanda de ≤12 agentes (contando verificadores).
- Vas a lanzar una **segunda** ola de agentes después de una primera.
- El dueño pidió "vamos con todo" sobre un plan que implica varias tandas.

**Cuándo NO**: el trabajo cabe en ≤3 agentes (lanzalos y ya, sin ceremonia); es de 1-2 archivos o diagnóstico abierto (chat principal, regla E de `.claude/rules/orquestacion.md`); el dueño pidió algo rápido y barato (hacelo a mano y decile cuánto habría costado con agentes).

## Las 2 reglas duras

1. **Máximo 12 agentes por tanda.** Es el tope de la regla B de `.claude/rules/orquestacion.md`, y cuenta **todos** los agentes de la tanda: los que hacen el trabajo Y los que verifican. Un pipeline de 12 ítems con 2 revisores cada uno son **36 agentes**, no 12.
2. **Entre tanda y tanda, PARÁS y PREGUNTÁS.** Nunca encadenes la siguiente por tu cuenta, aunque el plan la contemple y aunque el dueño haya dicho "vamos con todo". **"Vamos con todo" autoriza el PLAN, no el GASTO de cada tanda** — igual que no autoriza los procesos pesados implícitos (regla dura 2 de orquestación).

## Presupuesto — estimalo ANTES, no después

**El tipo de brief cambia el costo por agente más que el número de agentes.** Órdenes de magnitud medidos en un proyecto SaMD real (recalibralos contra tus propias corridas; lo que se porta es la relación, no la cifra exacta):

| Tipo de brief | Costo por agente | Tanda de 12 |
| --- | --- | --- |
| **Mecánico** (refactor guiado, killers de mutación, aplicar un patrón conocido) | ~95 k tokens | ~1,1 M |
| **Investigativo** (el brief pide *verificar la premisa antes de obedecer*: leer la ficha entera, reproducir el defecto, refutar el arreglo propuesto, sabotear) | **~200 k tokens** | **~2,4 M** |

El brief investigativo cuesta el **doble** y **vale la pena**: en la tanda que fijó ese número, cuatro agentes corrigieron la premisa — dos de ellas erróneas del propio orquestador — y sin esa instrucción habrían entregado cuatro arreglos plausibles sobre diagnósticos falsos.

Antes de lanzar, decile al dueño el número: *"esta tanda son N agentes ≈ X millones de tokens"*. Si el trabajo total pide más de 2 tandas, **decilo antes de la primera** — que decida el alcance sabiendo el precio, no a mitad de camino.

## Los pasos

1. **Medí el trabajo total** y hacé la lista completa de unidades (1 unidad = 1 archivo o 1 tarea independiente). Agrupá **por archivo**, nunca por hallazgo: dos agentes sobre el mismo archivo se pisan.
2. **Partí en tandas de ≤12** y ordenalas por **rendimiento**: primero lo barato y de bajo riesgo, al final lo delicado. Si la cuota se acaba, que se acabe con lo difícil pendiente y lo fácil hecho.
3. **Presentá el plan con el costo estimado y esperá OK.**
4. **Lanzá UNA tanda.** Nunca dos a la vez sin decirlo: comparten la máquina del dueño, que además puede tener otras ventanas abiertas (`.claude/rules/sesiones-paralelas.md`).
5. **Al terminar, verificá vos** — el `git diff` REAL, no el summary (`/anti-drift`): contador o medida objetiva, type-check, tests del módulo, y `git status` en busca de temporales y huérfanos.
6. **Reportá y PREGUNTÁ**: qué se hizo, **cuántos tokens costó**, qué encontraron los revisores y **qué falta**. Recién con el OK lanzás la siguiente.

## Si una tanda muere a mitad

Al agotarse el límite de sesión, los agentes mueren **después de guardar sus cambios y antes de verificarlos**. Protocolo:

* **No asumas que quedó roto ni que quedó bien.** Medí: lint/contador, type-check y los tests de los módulos tocados.
* **Buscá huérfanos**: archivos creados que nadie importa. Un agente que muere entre "crear la pieza" y "enchufarla" deja **islas de código muerto** — es el mismo modo de fallo que el ENCHUFE de `CLAUDE.md` §Análisis de impacto. Para cada archivo nuevo: buscá un importador REAL distinto de sí mismo.
* **Buscá temporales**: `git status --short | grep "^??"`.
* **Los revisores que no corrieron son deuda, no un detalle**: anotala explícitamente en `TECHNICAL_DEBT_SUMMARY.md`. Tests verdes ≠ revisión adversarial.

## Contrato de la tanda — metelo LITERAL en el brief de cada agente

Cada punto salió de un fallo real que ya costó caro:

1. **No cambies un aviso de lint por un TEST ROJO.** Bajar complejidad *añadiendo* líneas puede cruzar un ratchet de tamaño. Un aviso tiene techo tolerado; un test rojo corta el CI. **Prohibido subir el límite de un ratchet** para que pase tu cambio.
2. **Si creás archivos nuevos, el medidor de mutación se queda ciego.** Las configs scoped listan archivos **a mano**: sacar código de un archivo listado hacia archivos nuevos deja el score **igual midiendo menos superficie**. Añadí las rutas nuevas a la config en el mismo cambio.
3. **Corré los tests del DIRECTORIO, no los del archivo.** El guardián que se rompe suele vivir en otro archivo de test del mismo módulo.
4. **No dejes código huérfano ni temporales.** Cada archivo nuevo necesita un importador real.
5. **Hay guardianes que leen TEXTO, no conducta.** Un test que lee el archivo con `readFileSync` y exige una forma concreta se rompe con un cambio que al ejecutarse es idéntico (`if (!x) return;` en vez de `if (x) { … }`). ⇒ El sabotaje de comportamiento es **ciego** ante ellos: mirá también si el diff cambió la FORMA que alguien vigila.
6. **La suite de mutación de los módulos críticos es un CONTRATO** (regla dura 5 de orquestación): literales empáticos, logs, etiquetas ARIA y fórmulas. Tocar el literal obliga a tocar su killer en el mismo cambio. **Prohibido aflojar un killer para que pase un refactor** — si hace falta aflojarlo, el refactor está mal.

## Verificación adversarial: lentes distintos, no revisores repetidos

Para lo clínico y lo de seguridad, 3 revisores con **puntos de vista diferentes** cazan más que 3 iguales:

* **Equivalencia lógica** — ternario invertido · `if (x)` convertido en `x !== null` (difieren en `0`, `""`, `[]`) · `??` por `||` · caso del switch perdido · dependencias de hooks alteradas.
* **Seguridad clínica** — *¿puede una persona en crisis ver u oír algo distinto? ¿puede un profesional leer un riesgo equivocado?*
* **Contratos y guardianes** — *¿alguien aflojó un killer, rompió un ratchet o dejó ciego un medidor para que su cambio pasara?*

En zona crítica **basta que UN lente diga "rompe"** para bloquear: no se vota por mayoría cuando hay un botón de pánico de por medio.
