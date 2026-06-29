import { useState, type FormEvent } from "react";

/**
 * Esqueleto de ejemplo del cliente. Demuestra las reglas neuro-UX del kit:
 * diseño plano (sin glassmorphism), `prefers-reduced-motion` respetado y
 * etiquetas accesibles. Borralo cuando traigas tu cliente real.
 *
 * En la app real, esta lista guardaría offline-first y sincronizaría con el
 * backend (`POST /notes`), que cifra el texto en reposo.
 */
export default function App() {
  const [text, setText] = useState("");
  const [notes, setNotes] = useState<string[]>([]);

  const trimmed = text.trim();

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!trimmed) return;
    setNotes((prev) => [trimmed, ...prev]);
    setText("");
  }

  return (
    <main className="app">
      <h1>Notas privadas</h1>
      <p className="hint">
        Esqueleto de ejemplo del SaMD Starter Kit. En tu app real, esto guarda
        offline-first y sincroniza con el backend.
      </p>

      <form onSubmit={handleSubmit} className="note-form">
        <label htmlFor="note-input">Tu nota</label>
        <textarea
          id="note-input"
          value={text}
          onChange={(event) => setText(event.target.value)}
          placeholder="Escribí algo…"
          rows={3}
        />
        <button type="submit" disabled={!trimmed}>
          Agregar nota
        </button>
      </form>

      <section aria-live="polite" aria-label="Tus notas">
        {notes.length === 0 ? (
          <p className="empty">Todavía no tenés notas.</p>
        ) : (
          <ul className="note-list">
            {notes.map((note, index) => (
              <li key={index}>{note}</li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
