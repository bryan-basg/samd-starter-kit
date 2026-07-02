---
name: captura-sin-login
description: Monta un harness efímero de dev-server + navegador headless para screenshotear una pantalla detrás de login sin levantar el backend, y lo borra al final. Usala cuando {{OWNER}} pida ver cómo quedó una pantalla, componente o flujo del frontend que vive detrás de auth, y no valga la pena levantar el stack completo (emuladores/BD + backend + dev-server) solo para una captura.
---

# captura-sin-login — harness efímero de screenshot detrás de login

Para mostrarle a {{OWNER}} cómo se ve una pantalla del frontend ({{FRONTEND_STACK}}) que vive detrás del login, SIN levantar el stack completo (emuladores/BD + backend + dev-server), el truco es montar un harness de captura temporal que importa el componente REAL con sus estilos reales, mockea sólo los hooks/servicios que sin backend auto-ocultan el contenido, screenshotea con un navegador headless local (ej. Playwright/Chromium), y se borra después.

## Cuándo usarla

- Piden ver/revisar visualmente una pantalla o componente que está detrás de login (auth, permisos, datos de usuario).
- No hace falta ejercitar lógica de negocio real contra el backend — solo ver el render.
- Levantar emuladores + backend + dev-server completos sería desproporcionado para una simple captura.
- Se necesita iterar rápido sobre ajustes visuales de un componente sin pagar el costo de arrancar todo el stack en cada vuelta.

## Procedimiento

1. **Andamiaje efímero en el proyecto frontend** (todo temporal, se borra al final):
   - Una carpeta de preview (p. ej. `src/__preview/`) con un entry que renderiza el componente REAL del target (import por su ruta real, con sus estilos reales).
   - Un HTML mínimo que carga ese entry.
   - Un config de build/dev alternativo (p. ej. un config de Vite/webpack aparte) con un plugin que **intercepta imports por basename** para mockear los hooks/servicios que sin backend dejan la pantalla vacía (p. ej. hooks de datos de usuario, auth, preferencias, queries de red). Devolvé datos de ejemplo para que el contenido se muestre en vez de auto-ocultarse.

2. **Levantar el preview y capturar con un navegador headless local** (si dependés de una extensión de navegador conectada y no está disponible, usá una instancia local del navegador):
   - Viewport acorde al dispositivo objetivo (ej. ancho móvil ~430px), `fullPage: true` si querés la pantalla entera.
   - Si querés otro idioma/locale, forzalo antes de renderizar (ej. seteando la clave de idioma en `localStorage` o el mecanismo de i18n del proyecto).
   - Guardá el PNG en una carpeta de trabajo temporal fuera del control de versiones.

3. **Cortar la tira si es larga** (gotcha real): una captura fullPage muy alta (ej. varios miles de píxeles de alto) puede no visualizarse bien en el visor de imágenes de quien la revisa. Cortala en franjas de ancho/alto manejable antes de mostrarla.

4. **Iterar sobre la captura**: si piden ajustes visuales, tocá el componente real, re-corré el preview, re-capturá. No inventes un mockup — usá el componente y assets REALES del producto.

5. **Borrar el andamiaje al terminar**: la carpeta de preview, el HTML de entrada, el config alternativo y las capturas de trabajo. NO se commitea nada de esto.

## Alternativa (auditoría de muchas pantallas)

Para barrer varias pantallas detrás de login de una, se puede usar un spec E2E efímero que reuse el fixture de sesión autenticada del proyecto (el que levanta emulador/BD + backend + dev-server por su config habitual) y fuerce idioma/locale por el mismo mecanismo que usa la app en producción. Más caro (sí levanta el stack completo) pero cubre flujos completos. Borrar el spec al final.

## Reglas duras

- Todo el andamiaje es EFÍMERO — se borra al cerrar, NO entra en ningún commit.
- Usar el componente y estilos REALES, nunca un mockup inventado.
- Mockear sólo lo mínimo (los hooks/servicios que sin backend ocultan el render); no falsear el layout ni el contenido semántico.
- Si el PNG queda gigante, cortarlo en franjas antes de mostrarlo.
