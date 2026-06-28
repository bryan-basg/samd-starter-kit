#!/usr/bin/env python3
"""Auditor de smells de robustez backend — {{PROJECT_NAME}} (SaMD {{SAMD_CLASS}}).

IEC 62304 §5.5 — implementación robusta. Dos smells que ni el linter ni los
tests cazan de forma fiable y que en un backend asíncrono son bugs reales:

  1. I/O BLOQUEANTE dentro de funciones `async`:
       `open(...)`, `time.sleep(...)`, `requests.<verbo>(...)`
     Bloquean el event loop → degradan TODO el servicio bajo carga.

  2. `except:` / `except Exception:` DEMASIADO AMPLIOS sin re-raise:
     tragan errores (incluidos los de salud del sistema) en silencio →
     viola el fail-safe explícito (ISO 14971): el fallo debe degradar de
     forma predecible, nunca callar.

Camina el AST de cada `.py` bajo BASE_DIR (env `BASE_DIR`, default `app/`).
Reporta `archivo:línea`. Exit 1 si encuentra algo.

Uso:
    python scripts/audit_smells.py
    BASE_DIR=src/server python scripts/audit_smells.py

Exit codes:
    0 → limpio.
    1 → al menos un smell (o error de parseo).
"""

from __future__ import annotations

import ast
import os
import sys
from pathlib import Path

BASE_DIR = Path(os.environ.get("BASE_DIR", "app"))

EXCLUDE_DIRS = {
    "__pycache__", "venv", ".venv", "tests", "alembic",
    "node_modules", "build", "dist",
}

# Llamadas bloqueantes prohibidas dentro de `async def`.
#   - func simple:   open(...)            → nombre "open"
#   - func atributo: time.sleep(...)      → ("time", "sleep")
#                    requests.get/post... → ("requests", "<cualquiera>")
BLOCKING_SIMPLE_CALLS = {"open"}
BLOCKING_ATTR_CALLS = {
    ("time", "sleep"),
    ("requests", "*"),  # cualquier requests.<verbo>
    ("urllib", "*"),
    ("socket", "*"),
    ("subprocess", "*"),
}


def _attr_root(node: ast.AST) -> str | None:
    """Nombre raíz de un atributo encadenado: `a.b.c` → 'a'."""
    while isinstance(node, ast.Attribute):
        node = node.value
    return node.id if isinstance(node, ast.Name) else None


class SmellVisitor(ast.NodeVisitor):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.findings: list[tuple[int, str]] = []
        self._async_depth = 0

    # --- Rastreo de contexto async ------------------------------------------
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._async_depth += 1
        self.generic_visit(node)
        self._async_depth -= 1

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        # Una def síncrona anidada corta el contexto async (su I/O es legítimo).
        saved = self._async_depth
        self._async_depth = 0
        self.generic_visit(node)
        self._async_depth = saved

    # --- Smell 1: I/O bloqueante en async -----------------------------------
    def visit_Call(self, node: ast.Call) -> None:
        if self._async_depth > 0:
            self._check_blocking(node)
        self.generic_visit(node)

    def _check_blocking(self, node: ast.Call) -> None:
        func = node.func
        if isinstance(func, ast.Name) and func.id in BLOCKING_SIMPLE_CALLS:
            self.findings.append(
                (node.lineno, f"I/O bloqueante en async: `{func.id}(...)`")
            )
        elif isinstance(func, ast.Attribute):
            root = _attr_root(func)
            attr = func.attr
            for mod, verb in BLOCKING_ATTR_CALLS:
                if root == mod and (verb == "*" or verb == attr):
                    self.findings.append(
                        (node.lineno, f"I/O bloqueante en async: `{root}.{attr}(...)`")
                    )
                    break

    # --- Smell 2: except demasiado amplio sin re-raise ----------------------
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        bare = node.type is None
        broad = isinstance(node.type, ast.Name) and node.type.id in {
            "Exception", "BaseException"
        }
        if bare or broad:
            if not self._reraises(node.body):
                kind = "bare `except:`" if bare else f"`except {node.type.id}:`"  # type: ignore[union-attr]
                self.findings.append(
                    (node.lineno, f"{kind} demasiado amplio sin re-raise")
                )
        self.generic_visit(node)

    @staticmethod
    def _reraises(body: list[ast.stmt]) -> bool:
        """True si el bloque re-lanza (raise) en algún punto de su nivel."""
        for stmt in body:
            if isinstance(stmt, ast.Raise):
                return True
            # `raise` dentro de un if/with cuenta como manejo explícito.
            for child in ast.walk(stmt):
                if isinstance(child, ast.Raise):
                    return True
        return False


def _iter_py_files(root: Path):
    for path in root.rglob("*.py"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        yield path


def main() -> int:
    if not BASE_DIR.exists():
        print(f"❌ BASE_DIR inexistente: {BASE_DIR.resolve()}", file=sys.stderr)
        print("   Ajustá la env var BASE_DIR (ej. BASE_DIR=src/server).", file=sys.stderr)
        return 1

    total = 0
    for path in _iter_py_files(BASE_DIR):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (SyntaxError, OSError) as exc:
            print(f"❌ No se pudo parsear {path}: {exc}", file=sys.stderr)
            return 1
        visitor = SmellVisitor(str(path))
        visitor.visit(tree)
        for lineno, msg in sorted(visitor.findings):
            print(f"🔴 {path}:{lineno}  {msg}")
            total += 1

    if total == 0:
        print(f"✅ Sin smells de robustez en {BASE_DIR}/.")
        return 0
    print(f"\n❌ {total} smell(s) detectados — resolver antes de commitear.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
