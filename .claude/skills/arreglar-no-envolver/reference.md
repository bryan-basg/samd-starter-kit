# `/arreglar-no-envolver` — anexo: patrones y anti-patrones

> Anexo de `SKILL.md`. Se lee cuando el procedimiento no alcanza para decidir: para ver qué cuenta como «reescribir» y para no repetir un anti-patrón típico. **Agregá acá los casos medidos de tu propio proyecto** (fecha, símbolo, qué se borró): un anexo con casos reales enseña más que uno genérico.

## Ejemplo de la señal 1

Si un mismo campo (p. ej. el nivel de sobrecarga de un usuario) se comprueba en el router, en el servicio y en el helper, el problema no es que falte una cuarta comprobación: es que **el dato no nace válido**. Se resuelve con una puerta única (ver «Puerta única compartida» abajo).

## El caso que ilustra la señal 2

Un `except: pass` alrededor de la redacción de logs dejaba salir el dato sensible EN CLARO cuando la redacción fallaba: el envoltorio defensivo **causó** la fuga que decía prevenir. El `try` que no sabe nombrar qué falla no protege; oculta.

## Patrones que SÍ son «reescribir para simplificar» (no son envoltorios)

Estos **quitan** caminos aunque añadan un archivo. La prueba es que el código resultante tiene **menos** ramas, no más:

- **Puerta única compartida.** Tres consumidores adivinando lo mismo con tres listas de substrings → una función que lo deriva, y los tres la llaman. Se verifica **sabotando el vocabulario compartido**: si rojean los tests de los tres consumidores, la puerta está enchufada a todos.
- **Hacer el estado imposible con el tipo.** No «validar que el estado sea válido», sino que **no exista** un valor inválido. Ej.: un `Record<Salida, Estado>` — una salida nueva sin estado **no compila**. Antes, cada consumidor re-declaraba su copia de la unión a mano y no rojeaba si se olvidaba de crecer.
- **Que la función devuelva QUÉ PASÓ en vez de que el llamador lo adivine.** Pasar de `Promise<void>` —donde «no lanzó» se lee como ÉXITO— a devolver `applied | not_found | nothing_to_do` **borra** la necesidad de un `try` defensivo en el llamador.
- **Extraer para no duplicar un criterio.** Legítimo **solo si** los dos sitios pasan a usar la misma pieza y hay un test que rompe si divergen. Extraer y dejar la copia vieja viva es duplicar con más pasos.
- **Re-anclar un guardián a la fuente viva** en vez de copiar el valor. Si un guardián busca un literal (`setLevel(logging.ERROR)`) y al ponerle nombre a la constante se queda **ciego**, la salida NO es copiar el número —segunda fuente de verdad— sino resolver el nombre contra su asignación en el mismo módulo.

## Anti-patrones típicos (no los repitas)

- **El `try` que traga y devuelve el fallback amable.** Convierte un error de programación en un mensaje empático: el test falla diciendo *«Lo siento, necesito un momento»* en vez de señalar la línea. Si envolvés, **logueá el tipo real** de la excepción o vas a depurar a ciegas.
- **La lista de perdonados que documenta el arreglo correcto.** Un guardián que ve el defecto, lo diagnostica bien, escribe al lado cómo se arregla y lo mete en una lista de excepciones. Eso no es un trinquete: es **deuda con coartada**. Una excepción tolerada necesita ficha y condición de retiro.
- **El validador que se aplica a UNA de dos puertas gemelas.** Si el símbolo tiene dos caminos de entrada, proteger uno deja el otro abierto y da falsa tranquilidad. Buscá la gemela **por concepto**, no por nombre.
- **El tipo estricto que solo vive en el borde.** Declarar `NonEmpty` en la firma y hacer `cast` dos líneas después es teatro de tipos.
