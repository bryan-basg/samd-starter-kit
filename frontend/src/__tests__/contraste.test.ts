import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, it, expect } from "vitest";

/**
 * Guardián de contraste WCAG 2.1 AA (1.4.3). `vite.config.ts` corre con `css: false`, así que
 * ningún test de componente ve el CSS: este lee `App.css` directo. Existe por un defecto
 * real: el hover del botón ACLARABA el fondo (#0d9488 con texto blanco = 3,74:1 < 4,5:1).
 * Los scripts de npm corren desde `frontend/`, de ahí la ruta relativa al cwd.
 */
const css = readFileSync(resolve(process.cwd(), "src/App.css"), "utf-8");

function luminancia(hex: string): number {
  const canal = (desde: number): number => {
    const c = parseInt(hex.slice(desde, desde + 2), 16) / 255;
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  };
  return 0.2126 * canal(1) + 0.7152 * canal(3) + 0.0722 * canal(5);
}

function contraste(a: string, b: string): number {
  const la = luminancia(a);
  const lb = luminancia(b);
  return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
}

function variable(nombre: string): string {
  const hex = css.match(new RegExp(`${nombre}:\\s*(#[0-9a-fA-F]{6})`))?.[1];
  if (!hex) throw new Error(`falta la variable ${nombre} en App.css`);
  return hex;
}

function fondoDe(selector: string): string {
  const escapado = selector.replace(/[()]/g, "\\$&");
  const cuerpo = css.match(new RegExp(`${escapado}\\s*\\{([^}]*)\\}`))?.[1];
  if (cuerpo === undefined) throw new Error(`falta la regla ${selector} en App.css`);
  const fondo = cuerpo.match(/background:\s*(?:var\((--[\w-]+)\)|(#[0-9a-fA-F]{6}))/);
  const hex = fondo?.[2];
  if (hex) return hex;
  const nombre = fondo?.[1];
  if (!nombre) throw new Error(`la regla ${selector} no declara background`);
  return variable(nombre);
}

describe("contraste del botón (WCAG 2.1 AA, texto normal ≥ 4,5:1)", () => {
  const texto = "#ffffff";

  it("en reposo", () => {
    expect(contraste(texto, fondoDe("button"))).toBeGreaterThanOrEqual(4.5);
  });

  it("en hover (el hover oscurece, no aclara)", () => {
    const hover = fondoDe("button:hover:not(:disabled)");
    expect(contraste(texto, hover)).toBeGreaterThanOrEqual(4.5);
    expect(luminancia(hover)).toBeLessThanOrEqual(luminancia(fondoDe("button")));
  });
});
