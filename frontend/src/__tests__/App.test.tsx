import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect } from "vitest";

import App from "../App";

/**
 * Tests RIGUROSOS (SaMD §5.7): aserciones sobre comportamiento y accesibilidad,
 * no "renderiza sin crashear".
 */
describe("App (esqueleto de ejemplo)", () => {
  it("muestra el título y el estado vacío", () => {
    render(<App />);
    expect(
      screen.getByRole("heading", { name: /notas privadas/i }),
    ).toBeInTheDocument();
    expect(screen.getByText(/todavía no tenés notas/i)).toBeInTheDocument();
  });

  it("el botón está deshabilitado sin texto y se habilita al escribir", async () => {
    const user = userEvent.setup();
    render(<App />);
    const button = screen.getByRole("button", { name: /agregar nota/i });
    expect(button).toBeDisabled();
    await user.type(screen.getByLabelText(/tu nota/i), "hola");
    expect(button).toBeEnabled();
  });

  it("agrega una nota y limpia el campo", async () => {
    const user = userEvent.setup();
    render(<App />);
    const input = screen.getByLabelText(/tu nota/i);
    await user.type(input, "comprar pan");
    await user.click(screen.getByRole("button", { name: /agregar nota/i }));
    expect(screen.getByText("comprar pan")).toBeInTheDocument();
    expect(input).toHaveValue("");
  });

  it("ignora texto en blanco (solo espacios)", async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.type(screen.getByLabelText(/tu nota/i), "   ");
    expect(
      screen.getByRole("button", { name: /agregar nota/i }),
    ).toBeDisabled();
  });

  it("expone la lista de notas con una etiqueta accesible", async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.type(screen.getByLabelText(/tu nota/i), "x");
    await user.click(screen.getByRole("button", { name: /agregar nota/i }));
    expect(
      screen.getByRole("region", { name: /tus notas/i }),
    ).toBeInTheDocument();
  });
});
