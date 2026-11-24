import { readdirSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { describe, it, expect } from "vitest";

/**
 * Guardián de diseño plano y movimiento reducido (`.claude/rules/frontend-ux.md`).
 * `vite.config.ts` corre con `css: false`, así que ningún test de componente ve el CSS:
 * este lee los archivos del disco. La lista se DERIVA de `src/`: un archivo nuevo entra solo.
 */
const SRC = resolve(process.cwd(), "src");
const sinComentarios = (texto: string): string =>
  texto.replace(/\/\*[\s\S]*?\*\//g, "").replace(/^\s*\/\/.*$/gm, "");

const archivos = readdirSync(SRC, { recursive: true, encoding: "utf-8" })
  .filter((ruta) => /\.(css|tsx|ts)$/.test(ruta) && !ruta.includes("__tests__"))
  .map((ruta) => ({ ruta, texto: sinComentarios(readFileSync(join(SRC, ruta), "utf-8")) }));

const css = archivos.filter(({ ruta }) => ruta.endsWith(".css"));

describe("diseño plano (sin vidrio translúcido)", () => {
  it("encuentra archivos que mirar", () => {
    expect(css.length).toBeGreaterThan(0);
    expect(archivos.length).toBeGreaterThan(css.length);
  });

  it.each(archivos)("$ruta no usa desenfoque de fondo", ({ texto }) => {
    expect(texto).not.toMatch(/backdrop-?(filter|blur)|\bblur\(/i);
  });

  it.each(css)("$ruta no pinta fondos translúcidos", ({ texto }) => {
    const fondos = texto.match(/background(-color)?\s*:[^;}]*/gi) ?? [];
    const alfa = String.raw`(0?\.\d+|\d{1,2}%)\s*\)`; // 4.º valor (coma) o tras la barra
    const translucido = new RegExp(
      String.raw`(rgb|hsl)a?\((([^,)]*,){3}\s*|[^/)]*\/\s*)${alfa}|#([0-9a-f]{4}|[0-9a-f]{8})\b`,
      "i",
    );
    const translucidos = fondos.filter((fondo) => translucido.test(fondo));
    expect(translucidos).toEqual([]);
  });
});

describe("prefers-reduced-motion", () => {
  it("apaga animaciones y transiciones en TODO elemento", () => {
    const bloques = css
      .map(({ texto }) => texto)
      .join("\n")
      .match(/@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{\s*\*[^{]*\{[^}]*\}/g);
    const bloque = bloques?.join("\n") ?? "";
    expect(bloque).toMatch(/transition:\s*none\s*!important/);
    expect(bloque).toMatch(/animation:\s*none\s*!important/);
  });
});
