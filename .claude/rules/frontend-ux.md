---
paths:
  - "frontend/src/**/*.ts"
  - "frontend/src/**/*.tsx"
  - "frontend/src/**/*.css"
---

# UX CLÍNICA Y ACCESIBILIDAD (consecuencia SaMD §5.4 + WCAG 2.1 AA + ISO 14971)

> Regla **por-capa** del cerebro SaMD; las reglas **transversales** viven en `CLAUDE.md`. Esta regla carga sola cuando el agente lee/edita el frontend. Es una **CONSECUENCIA PRÁCTICA de la Regla 0** (cumplimiento SaMD): no es opcional. Capa/agente dueño: `frontend` (+ `mobile-native` para la capa nativa).
>
> **Adaptá los `paths:` a tu estructura real** (`{{FRONTEND_STACK}}`).

En un SaMD, la persona del otro lado puede estar en un momento vulnerable. **Cada decisión de UX es una decisión clínica**, no una preferencia estética.

## Reglas duras

* **Offline-first cuando el uso previsto lo requiera**: toda mutación de datos pasa primero por la base local → outbox → sync. NUNCA eludir el motor de sincronización escribiendo directo al servidor desde un componente.
* **Capa de fetch/cache única y obligatoria**: un solo mecanismo de fetch + cache en todo el cliente. Componentes que hacen `fetch` a mano se saltan reintentos, invalidación y estados de error empáticos.
* **`prefers-reduced-motion` respetado incondicionalmente.** Cero animaciones agresivas en cualquier parte de la UI. No es una opción de accesibilidad "extra": para parte del público objetivo, el movimiento es un disparador.
* **Contraste WCAG AA verificado en cada par fg/bg nuevo.** Si tu sistema visual prohíbe un efecto (translucidez, texto sobre imagen, etc.), poné un **test-guardia anti-regresión** que rojee si reaparece — la prohibición escrita sola no aguanta el paso del tiempo.
* **Componentes canónicos, no overlays nuevos**: un único `Modal` para overlays y un único diálogo de confirmación para acciones destructivas. Prohibido crear overlays paralelos: divergen en foco, `Escape` y lectura por lector de pantalla.
* **Etiquetas semánticas + ARIA correctas** para lectores de pantalla. Encabezados en orden, sin saltos de nivel.
* **NO emoji en `aria-label` de elementos críticos** (botón de crisis/pánico, auto-cuidado, alertas). Los lectores de pantalla los pronuncian raro o los saltan. Solo texto plano — y con **test de regresión** en el componente crítico.
* **Toasts/avisos con `id` único** (anti-flood). Sin identificador, mensajes idénticos se acumulan y abruman a quien ya está sobrecargado.
* **Registro de íconos consistente**: si tenés un mapa nombre→ícono, cada nombre nuevo del tipo debe existir también en el mapa. Si falta, el componente devuelve `null` en silencio y el ícono nunca aparece en producción. Test anti-regresión obligatorio.
* **El almacenamiento del navegador NO es persistente dentro de un contenedor nativo**: las limpiezas del sistema operativo lo borran entre arranques. Para datos críticos del WebView (idioma, tokens, preferencias) usá la persistencia nativa como respaldo. (Ver el agente `mobile-native`.)
* **Nada de jerga técnica en pantalla**: ver `CLAUDE.md` §COMUNICACIÓN — EMPATÍA CON USUARIOS, incluido el glosario clínico pre-certificación.
