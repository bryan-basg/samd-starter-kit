---
name: matar-mutantes
description: Kit de recetas de killers puntuales de Stryker/mutation testing (i18n defaults, useState boolean SSR, módulos mockeados, prop-injection, constantes top-level). Úsala cuando un reporte de mutation testing muestra mutantes "Survived" raros o difíciles de matar y hace falta diagnosticar el patrón exacto antes de escribir el test killer, o cuando el usuario pregunta cómo matar un mutante superviviente concreto.
---

# matar-mutantes — Recetas de killers puntuales de mutation testing

Cada tipo de mutante "raro" que sobrevive en el frontend tiene una receta probada. El procedimiento es: diagnosticar el tipo de mutante en el reporte y aplicar la receta correspondiente. Antes de gastar una corrida completa de mutation testing, hacé sanity-check manual: mutá la línea a mano (sed/python) y verificá que el test rojea.

## Cuándo usarla

- Un reporte de Stryker (u otra herramienta de mutation testing equivalente) muestra mutantes `Survived` en literales i18n, `useState` booleano, módulos mockeados en el setup global, código gateado por constantes internas, o constantes top-level.
- Antes de gastar una corrida completa de mutation testing, para hacer el sanity-check manual de una línea puntual.
- Cuando hay que decidir si un mutante superviviente es equivalente real o reducible con un test killer.

## Procedimiento

### 1. StringLiteral DEFAULT de `t(key, "Default")` sobrevive (i18n)

Causa: el mock local `t: (key) => key` ignora el default, así que mutar `"Default"` → `""` es equivalente. Suele ser la palanca más grande de falsos-equivalentes en cualquier frontend con i18n mockeado en tests.

Cura — spy-`t()` hoisted y asertar los args:
```typescript
const { tSpy } = vi.hoisted(() => ({
  tSpy: vi.fn((key: string, _def?: unknown) => key),
}));
vi.mock("react-i18next", () => ({
  useTranslation: () => ({ t: tSpy, i18n: { language: "es" } }),
}));

// Killer:
expect(tSpy).toHaveBeenCalledWith("common.close", "Cerrar");
```
- **Key usada en 2+ sitios del mismo archivo**: `toHaveBeenCalledWith` se satisface con CUALQUIER call, así que mutar 1 sitio no rojea si otro llama bien. Cura: renderizar con props que activen SÓLO una línea, filtrar `tSpy.mock.calls` por key, asertar sobre el único call; o asertar el sink DOM exacto (aria-label/title/textContent) por call-site.
- **ObjectLiteral default** `t(key, {defaultValue: "..."})`: filtrar los calls por key y asertar `opts.defaultValue` / `opts.percent`.

### 2. BooleanLiteral de `useState(initial)` sobrevive cuando un `useEffect` lo sobrescribe

Causa: `render()` de RTL hace `act()` implícito y flush de effects → el primer DOM observable es post-effect, donde `true` vs `false` da el mismo render.

Cura — `renderToString` de `react-dom/server` (ejecuta SÓLO el render, NO effects):
```typescript
import { renderToString } from "react-dom/server";

it("useState(true) → initial render muestra loading", () => {
  const html = renderToString(<MyComponent />);
  expect(html).toContain('data-testid="loading"');
  expect(html).not.toContain('data-testid="empty"');
});
```
NO usar `vi.spyOn(React, "useState")` (falla en runtimes ESM recientes: "Cannot redefine property"). NO `vi.mock("react", ...)` (demasiado invasivo).

### 3. Archivo mockeado en el setup global de tests reporta NoCoverage bajo mutation testing

Causa: `vi.unmock` + `vi.importActual` re-importa desde el cache del setup global (sigue mockeado) — la herramienta de mutation testing NO rastrea `vi.importActual` como hit, el código real nunca corre instrumentado.

Cura — `vi.doUnmock` + `vi.resetModules` + dynamic `import()`:
```typescript
afterEach(() => {
  vi.doUnmock("../usePendingSyncCount");
  vi.resetModules();
});

it("...", async () => {
  vi.doUnmock("../usePendingSyncCount");
  vi.resetModules();
  const { usePendingSyncCount } = await import("../usePendingSyncCount");
  // test sobre el módulo REAL instrumentado
});
```
Aplicar siempre que el archivo bajo mutación esté mockeado en el setup global de tests (hooks con polling, contexts inertes). Dejá un comentario explicativo junto al mock global para que la próxima persona entienda por qué el archivo real necesita este patrón.

### 4. Código gateado por una constante interna (feature comentado, filtros, etc.)

Cura — prop-injection con default: exponer el valor por prop opcional con default = la constante interna:
```typescript
function ResourceLibrary({ fileTypeFilters = FILE_TYPE_FILTERS }: Props) { ... }
```
CERO cambio de comportamiento (el único consumidor sigue sin pasar la prop) → destraba los `NoCoverage` del feature gated. Si tu proyecto exige trazabilidad regulatoria (SaMD, ISO, etc.), documentá el refactor mínimo con esa justificación.

### 5. Constantes top-level (arrays/objetos a module-load) reportadas Survived bajo cobertura `perTest`

Causa: las expresiones top-level se evalúan UNA vez, antes de correr cualquier test → `coverageAnalysis: "perTest"` no mapea tests a esos mutantes.

Cura — en el config scoped de Stryker para ese archivo/carpeta:
```json
"coverageAnalysis": "off",
"ignoreStatic": false
```
Ambos juntos (Stryker exige que `ignoreStatic: false` para usar `off`). Costo: corre TODOS los tests contra TODOS los mutantes (más lento; puede ser excesivo para corridas de muchos archivos a la vez, mejor reservarlo para el archivo puntual). Detección: los Survived son `StringLiteral`/`ObjectLiteral`/`ArrayDeclaration` en una `const X = ...` top-level (no dentro de una función).

## Reglas duras

- Sanity-check manual (sed/python mutando la línea + test rojo) ANTES de gastar una corrida completa de mutation testing.
- Distinguir equivalente real (optional chaining sobre refs que nunca son null, guards de montaje, animaciones simétricas que el framework batchea) de reducible. Los equivalentes se documentan, no se fuerzan a cualquier costo.
- Si tu proyecto trata ciertos literales (mensajes empáticos, aria-labels, fórmulas de negocio críticas) como contrato verificado, tocar el literal de producción obliga a tocar su killer en el mismo cambio — no aflojar esos tests sin justificación documentada.
