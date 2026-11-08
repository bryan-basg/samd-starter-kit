---
description: Antes de escribir un validador, un try/except, un if de guarda, un tipo más estricto o un envoltorio sobre código que YA EXISTE — test decisivo para saber si arreglás el defecto o solo lo tapás.
---

Vas a tocar código que ya existe en el proyecto {{PROJECT_NAME}} y estás por **añadir protección** a su alrededor. **Parate un momento: ¿estás arreglando o envolviendo?**

## Cuándo aplica (basta UNA señal)

1. Vas a escribir un `try`/`except`, un `if x is None` de guarda, un `assert`, un validador **sobre un dato que ya está dentro del sistema**, un tipo más estricto o una función que envuelve a otra.
2. Tu arreglo **no borra líneas** del archivo donde vive el defecto (solo añade).
3. La ficha de deuda dice «validar», «blindar», «proteger», «defensivo».
4. Estás en el archivo del **síntoma**, no en el del **origen**.
5. Ya existe una comprobación parecida del mismo dato en otra capa.

## El filo — NO deroga la validación obligatoria

Siguen siendo innegociables: **(a)** validación de **FRONTERA** (dato externo entrando, una vez, donde entra); **(b)** **fail-safe clínico** declarado (ISO 14971: más alerta, `estimated`/`unclassified`, fusible 503); **(c)** **guardas de seguridad en el punto de decisión** (JWT, portero de acceso). La protección legítima vive en la frontera y corre UNA vez; la prohibida vive encima de la lógica y se repite.

## Los 5 pasos

1. **Nombrá el defecto en una frase, sin la palabra «validar».** ¿Por qué llega mal el dato?
2. **Buscá el productor, no el consumidor** (`grep` el origen).
3. **¿Puede el estado inválido dejar de EXISTIR?** Mejor a peor: hacer el estado imposible → puerta única derivada → validar en la frontera → ❌ envolver el uso.
4. **Si igual añadís protección, justificá EN EL CÓDIGO** por qué no se puede reescribir (solo 3 motivos: es la frontera · es fail-safe clínico con su referencia a la matriz de riesgos · el productor es de terceros). «No me animo» / «rompe tests» = ficha en `TECHNICAL_DEBT_SUMMARY.md`, no justificación.
5. **Test decisivo:** llamá a la función original **saltándote tu protección**. Si el defecto vuelve, escribiste un consejo, no un control.

## Al terminar, reportá

Líneas añadidas vs quitadas en el archivo del defecto · por qué otras puertas puede volver el defecto · bajo cuál de los 3 motivos válidos va cualquier protección añadida (o ficha de deuda abierta).

Procedimiento completo, patrones y anti-patrones: skill `/arreglar-no-envolver`.
