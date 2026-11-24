# Manual de marca de {{PROJECT_NAME}} — el criterio de `/revision-visual`

> **Plantilla: llenala con tu producto.** El código es la fuente de verdad: este manual describe el CRITERIO y apunta al archivo; los valores se leen ahí, no se copian acá (anti-drift, `CLAUDE.md` §ANÁLISIS DE IMPACTO). Si un archivo citado cambió, gana el archivo y se corrige este manual.

## 1. El logo

* **Fuente**: `<ruta del SVG maestro y sus variantes>`.
* **Reglas**: no se deforma, no se recolorea a mano, no se le agregan sombras ni brillos. Si tiene degradado, vive **en el logo**; no se esparce por la interfaz como decoración.

## 2. Color

* **Dónde viven los tokens**: en el esqueleto, `:root` de `frontend/src/App.css`.
* **¿El usuario puede cambiar la paleta o el tema?** `<sí/no>`. Si puede, una propuesta se revisa al menos en 2: la que solo se ve bien en una está mal.
* **Criterio**: el color **dice algo** (marca, estado, selección), no decora. El rojo, solo para peligro real: en un producto de salud, un rojo de adorno asusta.

## 3. Tipografía

* **Familia**: `<cuál y dónde se declara>`. El esqueleto usa las del sistema (sin terceros: privacidad y offline).
* **Criterio**: una sola familia por pantalla; jerarquía con **tamaño y peso**, no con fuentes nuevas.

## 4. Forma, profundidad e íconos

* **Radios y sombras**: `<tokens>`. Diseño **plano**: la sombra separa capas, no adorna.
* **Íconos**: `<set y molde>`. Un ícono nuevo sigue el molde; no se trae de otra librería.

## 5. Perfiles y accesibilidad

* `<perfiles de usuario que cambian movimiento, interlineado, foco…>`. Una propuesta se piensa **para todos**: si solo funciona con animación, rompe a quien pidió movimiento reducido.

## 6. Páginas públicas (landing)

* `<rutas>`. Es **la vidriera**: admite algo más de expresión, con la misma cancha (contraste, movimiento reducido, diseño plano, glosario).

## 7. El gusto de {{OWNER}} — se llena usándola

Cada vez que {{OWNER}} **rechaza** una propuesta y dice por qué, el porqué entra acá como una línea (fecha + regla). Así la skill no vuelve a proponerlo. Lo que pasa una sola vez no entra.

* *(vacío — se llena en el primer uso)*

## 8. Calibración con un revisor humano

Para medir si la skill ve lo que ve un diseñador:

1. Misma captura, misma pregunta concreta, **a ciegas**: ni la skill ve la respuesta del revisor ni al revisor se le muestra el menú antes.
2. Comparar en tres columnas: **coinciden** · **solo lo vio el humano** (falta una lente → se agrega al `SKILL.md`) · **solo lo propuso la skill y el humano lo descarta** (anotar por qué → §7).
3. Se anota solo el aprendizaje que se repite o que cambia una regla.
