#!/usr/bin/env python3
"""Verifica que las citas al código de la documentación apunten a algo que existe.

Forma canónica de citar código en el DHF (IEC 62304 §5.1 / §5.7):

    ruta/archivo.py::símbolo              función, clase o constante
    ruta/archivo.py::Clase::metodo        también con ``.`` (Clase.metodo)
    tests/test_x.py::test_algo[caso]      id de test estilo pytest

Por qué por NOMBRE y no por número de línea: el número envejece con cada commit
que agrega o borra una línea más arriba; el nombre sobrevive hasta que alguien lo
renombra, y ESE caso sí lo caza este script (rojo en el CI). Una cita que no se
puede comprobar no es trazabilidad.

Qué comprueba (solo las citas con ``::``):
  1. el archivo existe;
  2. en ``.py`` el símbolo está definido de verdad (AST: def/class/asignación);
  3. en cualquier otro tipo de archivo (TS/JS/SH/YML…) el nombre aparece como
     palabra completa. Es una comprobación más floja: lo dice el reporte.

Qué NO comprueba (y lo dice): las citas viejas ``archivo.py:123`` sin ``::`` se
cuentan y se informan, pero no se verifican ni se reescriben en masa.

Se ignoran los bloques de código, las plantillas (``<…>``, ``{{…}}``) y los
marcadores literales (``ruta/archivo.py::símbolo``).

Uso:
    python3 scripts/check_doc_citations.py             # docs/ + *.md de la raíz
    python3 scripts/check_doc_citations.py --paths X   # rutas puntuales

Exit code 1 si hay citas rotas (lo corre el CI).
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

CODE_EXTENSIONS = r"py|tsx|ts|jsx|js|mjs|cjs|sh|yml|yaml|sql|toml|json"
# Delante de la cita no puede haber nada que la haga parte de otra ruta o de una
# plantilla (``{{X}}/a.py::b``, ``<dir>/a.py::b``): ahí no hay ruta real.
_NOT_BEFORE = r"(?<![\w./{}<>$~-])"
_PATH = rf"[\w.-]+(?:/[\w.-]+)*\.(?:{CODE_EXTENSIONS})"
_SYMBOL = r"[^\W\d]\w*(?:(?:::|\.)[^\W\d]\w*)*"
CITATION_RE = re.compile(
    rf"{_NOT_BEFORE}(?P<path>{_PATH})(?::\d+)?::(?P<symbol>{_SYMBOL})(?:\[[^\]\n]*\])?"
)
# Cita vieja: ``archivo.py:123`` (sin ``::`` a continuación). Solo se cuenta.
LEGACY_RE = re.compile(rf"{_NOT_BEFORE}{_PATH}:\d+(?!\d|::)")

# Ejemplos literales de la propia documentación: no son rutas reales.
_PLACEHOLDER_FIRST_SEGMENTS = {"ruta", "path"}
_PLACEHOLDER_STEMS = {"archivo", "file"}

FENCE_RE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE_RE = re.compile(r"`([^`\n]*)`")


@dataclass(frozen=True)
class Citation:
    path: str
    symbol: str
    line: int


def is_placeholder(path: str) -> bool:
    parts = path.split("/")
    return parts[0] in _PLACEHOLDER_FIRST_SEGMENTS or (
        parts[-1].rsplit(".", 1)[0] in _PLACEHOLDER_STEMS
    )


def _prose_lines(text: str) -> Iterable[tuple[int, str]]:
    """(nº de línea, texto) de las líneas que NO están dentro de un bloque de
    código cercado."""
    in_fence = False
    for number, line in enumerate(text.splitlines(), start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield number, line


def find_citations(text: str) -> tuple[list[Citation], int]:
    """(citas por nombre, cantidad de citas viejas por número de línea)."""
    found: list[Citation] = []
    legacy = 0
    for number, line in _prose_lines(text):
        for match in CITATION_RE.finditer(line):
            if not is_placeholder(match.group("path")):
                found.append(
                    Citation(match.group("path"), match.group("symbol"), number)
                )
        legacy += sum(
            1
            for m in LEGACY_RE.finditer(line)
            if not is_placeholder(m.group(0).rsplit(":", 1)[0])
        )
    return found, legacy


def _collect_names(body: list[ast.stmt], prefix: str, out: set[str]) -> None:
    for node in body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            qualified = prefix + node.name
            out.add(qualified)
            if isinstance(node, ast.ClassDef):
                _collect_names(node.body, qualified + ".", out)
        elif isinstance(node, ast.Assign):
            out.update(
                prefix + t.id for t in node.targets if isinstance(t, ast.Name)
            )
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name):
                out.add(prefix + node.target.id)
        else:  # if/try/with/for a nivel de módulo o de clase
            for field in ("body", "orelse", "finalbody"):
                _collect_names(getattr(node, field, []), prefix, out)
            for handler in getattr(node, "handlers", []):
                _collect_names(handler.body, prefix, out)


def python_symbols(source: str) -> set[str]:
    """Nombres calificados definidos en un módulo Python (``Clase.metodo``)."""
    names: set[str] = set()
    _collect_names(ast.parse(source).body, "", names)
    return names


def check_citation(citation: Citation, root: Path) -> str | None:
    """Motivo por el que la cita está rota, o ``None`` si es válida."""
    target = root / citation.path
    if not target.is_file():
        return f"el archivo {citation.path} no existe"
    source = target.read_text(encoding="utf-8", errors="replace")
    wanted = citation.symbol.replace("::", ".")
    if citation.path.endswith(".py"):
        try:
            defined = python_symbols(source)
        except SyntaxError:
            return f"{citation.path} no se pudo parsear"
        if wanted not in defined:
            return f"{citation.path} no define «{citation.symbol}»"
        return None
    last = wanted.rsplit(".", 1)[-1]
    if not re.search(rf"(?<![\w$]){re.escape(last)}(?![\w$])", source):
        return f"«{last}» no aparece en {citation.path}"
    return None


@dataclass
class Report:
    broken: list[str]
    verified: int
    legacy: int


def check_file(path: Path, root: Path) -> Report:
    text = path.read_text(encoding="utf-8")
    citations, legacy = find_citations(text)
    broken: list[str] = []
    for citation in citations:
        reason = check_citation(citation, root)
        if reason:
            where = f"{path.relative_to(root)}:{citation.line}"
            broken.append(f"{where}: {citation.path}::{citation.symbol} -> {reason}")
    return Report(broken, len(citations) - len(broken), legacy)


def default_files(root: Path) -> list[Path]:
    return sorted((root / "docs").rglob("*.md")) + sorted(root.glob("*.md"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verifica que las citas ruta/archivo.py::símbolo existan."
    )
    parser.add_argument(
        "--paths", nargs="*", default=None, help="Rutas puntuales a escanear"
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    files = (
        [Path(p).resolve() for p in args.paths] if args.paths else default_files(root)
    )

    broken: list[str] = []
    verified = legacy = 0
    for f in files:
        report = check_file(f, root)
        broken.extend(report.broken)
        verified += report.verified
        legacy += report.legacy

    if broken:
        print(f"CITAS ROTAS: {len(broken)}")
        for line in broken:
            print(f"  BROKEN: {line}")
        return 1
    print(
        f"Citas por nombre OK ({verified} verificadas, 0 rotas, {len(files)} "
        f"archivos). Citas viejas por número de línea sin verificar: {legacy}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
