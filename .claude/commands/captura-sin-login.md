---
description: Monta un harness efímero de dev-server + navegador headless para screenshotear una pantalla detrás de login sin levantar el backend, y lo borra al final.
argument-hint: <componente o pantalla a capturar, ej. UserSettingsPanel>
---

Sos un asistente que necesita mostrarle a {{OWNER}} cómo se ve una pantalla del frontend ({{FRONTEND_STACK}}) que vive detrás del login, SIN levantar el stack completo (emuladores/BD + backend + dev-server). El truco: montar un harness de captura temporal que importa el componente REAL + sus estilos reales, mockea sólo los hooks/servicios que sin backend auto-ocultan el contenido, screenshotea con un navegador headless local (ej. Playwright/Chromium), y se borra después.

## Receta

1. **Andamiaje efímero en el proyecto frontend** (todo temporal, se borra al final):
   - Una carpeta de preview (p.ej. `src/__preview/`) con un entry que renderiza el componente REAL de `$ARGUMENTS` (import por su ruta real, con sus estilos reales).
   - Un HTML mínimo que carga ese entry.
   - Un config de build/dev alternativo (p.ej. un config de Vite/webpack aparte) con un plugin que **intercepta imports por basename** para mockear los hooks/servicios que sin backend dejan la pantalla vacía (p.ej. hooks de datos de usuario, auth, preferencias, queries de red). Devolvé datos de ejemplo para que el contenido se muestre en vez de auto-ocultarse.

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

Pantalla/componente a capturar: $ARGUMENTS
