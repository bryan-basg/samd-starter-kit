---
name: revision-visual
description: 'INVOCAR cuando {{OWNER}} pida una mirada de diseñador sobre una pantalla o pieza de {{PROJECT_NAME}} (landing, inicio, panel profesional, logo, íconos): «¿se ve bien?», «está amontonado», «revisá el diseño». Saca la foto REAL, la revisa con 6 lentes de diseño dentro de las reglas de UX clínica y devuelve un MENÚ de mejoras para que {{OWNER}} elija. NO aplica nada sin su elección.'
argument-hint: '<pantalla o pieza, ej. landing | inicio | panel-profesional | logo> [pregunta concreta]'
---
Vas a hacer de **diseñador gráfico con las reglas del proyecto en la cabeza**. No sos el que decide: traés un menú con evidencia, **{{OWNER}} elige**, y lo elegido lo aplica el agente `frontend`.

> **Leé primero el manual de marca: [reference.md](reference.md)** — logo, color, tipografía, forma, íconos y **§7 el gusto de {{OWNER}}** (lo que ya rechazó: no se vuelve a proponer). Si está sin llenar, decilo al abrir: sin él opinás como un diseñador genérico.

## Antes de empezar — dos frenos

1. **Zona off-limits** (p. ej. las pantallas del paciente y las utilities globales): **mirar y proponer, sí; tocar, solo con pedido dirigido de {{OWNER}}** (`CLAUDE.md` §Zonas off-limits). Si una mejora del panel interno cambia un token global, avisá ANTES de que caiga en cascada sobre el usuario final.
2. **Costo**: en el chat principal no cuesta extra. Si son varias pantallas, **un** agente `frontend`: decile el costo a {{OWNER}} antes (estilo «Orquestador SaMD» §2, regla B).

## Paso 1 — la foto real, nunca un mockup

* Detrás del login: receta `/captura-sin-login`. Una página pública se abre directo.
* Viewport **móvil (~430 px) primero** si ahí vive tu usuario. Después escritorio si aplica.
* Cada tema que el producto tenga (claro, oscuro, perfiles de baja estimulación).
* **Solo datos de ejemplo o usuarios sembrados.** Nunca una captura con datos reales: esas fotos pueden salir del proyecto (ver «Ojo humano») y serían PHI.

## Paso 2 — las 6 lentes

| Lente | La pregunta | Señal de problema |
| --- | --- | --- |
| **Jerarquía** | ¿Qué ve primero el ojo? ¿Es lo más importante? | Todo grita igual; la acción principal compite con adornos |
| **Espaciado y ritmo** | ¿Los grupos respiran? ¿Los márgenes repiten un patrón? | Bloques pegados, márgenes de 5 valores distintos |
| **Tipografía** | ¿Cuántos tamaños/pesos hay? ¿Se lee de un vistazo? | Más de ~3 tamaños por pantalla, líneas larguísimas |
| **Color y contraste** | ¿El color dice algo o decora? ¿Contraste AA? | Color usado solo para lucirse; texto gris sobre gris |
| **Coherencia de marca** | ¿Parece de la misma familia que el logo? | Íconos de estilos mezclados, radios de borde distintos |
| **Carga sensorial** | ¿Una persona en un momento vulnerable se abruma acá? | Movimiento, muchos estímulos a la vez, avisos apilados |

La sexta lente **no es de diseño gráfico clásico**: es la que separa un SaMD de cualquier otra app. Ante choque entre «más lindo» y «menos carga», gana menos carga.

## Paso 3 — la cancha (lo que una propuesta NO puede romper)

Reglas de `.claude/rules/frontend-ux.md` (cargá la regla si no está en contexto) y sus guardianes en `frontend/src/__tests__/`:

* **Diseño plano** y **`prefers-reduced-motion` siempre respetado**: `disenoPlano.test.ts`.
* **Contraste WCAG AA** en cada par texto/fondo nuevo, y ≥ 3:1 en bordes de campo y anillo de foco (1.4.3, 1.4.11): `contraste.test.ts`. Un color nuevo sin su par rojea.
* **Componentes canónicos**: un solo `Modal` y un solo diálogo de confirmación; no se inventan overlays.
* **Sin fuentes ni recursos de terceros** salvo decisión registrada: privacidad y offline.
* **Glosario pre-certificación** en cualquier texto propuesto (`CLAUDE.md` §COMUNICACIÓN).

Una propuesta que rompe la cancha **no entra al menú**, ni como opción «arriesgada».

## Paso 4 — el menú para {{OWNER}}

Máximo ~6 mejoras, ordenadas por impacto. Cada una, en lenguaje cotidiano:

* **Qué se ve hoy** (sobre la captura) → **qué cambiaría** → **por qué** (en una frase, la lente que la justifica).
* **Tamaño**: pequeño (un estilo) · mediano (un componente) · grande (toca tokens o varias pantallas).
* **¿Toca una zona off-limits?** sí/no.

«La pantalla está bien, no cambiaría nada» **es un resultado válido**: prohibido inventar mejoras para justificar la revisión. Terminá con tu recomendación.

**Al cerrar**: si {{OWNER}} rechazó algo con un porqué que vale para la próxima, agregalo como una línea a `reference.md` §7.

## Paso 5 — aplicar lo elegido

* Lo aplica el agente `frontend` (o el chat principal si es de 1-2 líneas), con las reglas de capa precargadas.
* **Foto antes y después**, misma vista, y se la mostrás a {{OWNER}}.
* Verificación: los guardianes de `frontend/src/__tests__/` + los tests del componente tocado + `npm run typecheck` + `npm run lint`. La suite completa la decide el orquestador (regla dura 2).
* Si cambió un token o un color de marca: trazabilidad de producto y `/cierre-bloque`.

## Ojo humano — revisores externos (p. ej. un diseñador de confianza)

La skill no reemplaza a una persona con oficio. Si {{OWNER}} la quiere sumar:

* Se le mandan **capturas con datos de ejemplo**, una pantalla a la vez, con **una pregunta concreta** («¿qué ves primero?»), no «¿qué te parece?».
* Sus propuestas pasan por el **Paso 3** antes de aplicarse: el ojo humano opina de estética, la cancha la ponen las reglas.
* **Si su trabajo entra al producto** (ícono, ilustración, logo): cesión de derechos por escrito antes de usarlo.
