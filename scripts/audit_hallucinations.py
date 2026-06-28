#!/usr/bin/env python3
"""Auditor anti-alucinaciones de IA — {{PROJECT_NAME}} (SaMD {{SAMD_CLASS}}).

IEC 62304 §5.5/§5.7 — el código generado por asistentes de IA suele dejar
placeholders, credenciales de ejemplo o claims sin resolver que NUNCA deben
llegar a un repo de dispositivo médico. Este script barre el árbol y FALLA
(exit 1) si encuentra alguno.

Patrones en una lista editable (`PATTERNS`). Cada entrada:
    (regex, etiqueta, severidad)
Severidad "critical" o "warning"; ambas hacen fallar por default (modo SaMD
es fail-closed). Para tolerar warnings, correr con `--allow-warnings`.

Uso:
    python scripts/audit_hallucinations.py [ruta]    # default: cwd
    python scripts/audit_hallucinations.py --allow-warnings

Exit codes:
    0 → limpio (o solo warnings con --allow-warnings).
    1 → se encontró al menos un patrón bloqueante.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ----------------------------------------------------------------------------
# Patrones editables. Añadí/quitá según el stack del proyecto.
# Las regex se compilan con IGNORECASE.
# ----------------------------------------------------------------------------
PATTERNS: list[tuple[str, str, str]] = [
    # --- Placeholders de infraestructura ------------------------------------
    (r"\byour[-_]project[-_]id\b", "placeholder de project id", "critical"),
    (r"\byour[-_]api[-_]key\b", "placeholder de API key", "critical"),
    (r"\bAPI_KEY_HERE\b", "placeholder de API key", "critical"),
    (r"\b(?:xxxx+|XXXX+)\b", "placeholder XXXX", "warning"),
    (r"<your[-_ ][^>]+>", "placeholder <your ...>", "warning"),
    (r"\bCHANGE[-_]?ME\b", "marcador CHANGEME", "critical"),
    (r"\bREPLACE[-_]?ME\b", "marcador REPLACEME", "critical"),

    # --- Dominios / emails de ejemplo ---------------------------------------
    (r"\b[\w.+-]+@example\.com\b", "email de ejemplo (example.com)", "warning"),
    (r"\bexample\.(?:com|org|net)\b", "dominio de ejemplo", "warning"),
    (r"\bfoo\.bar\b", "dominio foo.bar", "warning"),
    (r"\blocalhost:\d+\b", "localhost hardcodeado", "warning"),

    # --- Credenciales demo / débiles ----------------------------------------
    (r"\badmin123\b", "credencial demo admin123", "critical"),
    (r"\bpassword123\b", "credencial demo password123", "critical"),
    (r"\bchangeit\b", "credencial demo changeit", "critical"),
    (r"(?:password|passwd|pwd)\s*[:=]\s*['\"]?(?:admin|root|test|demo|secret)['\"]?",
     "password demo en asignación", "critical"),

    # --- Roles / permisos peligrosos sembrados por IA ------------------------
    (r"\broles/owner\b", "rol IAM owner hardcodeado", "critical"),
    (r"\ballUsers\b", "binding IAM público (allUsers)", "critical"),

    # --- Marcadores de trabajo sin terminar (críticos) ----------------------
    (r"\b(?:TODO|FIXME)[_ ]?(?:CRITICAL|SECURITY|SAMD)\b", "TODO crítico sin resolver", "critical"),
    (r"\bHACK\b.*\b(?:remove|temporary|before[-_ ]?prod)\b", "HACK temporal sin resolver", "warning"),
    (r"\braise NotImplementedError\b", "función sin implementar", "warning"),
]

# Directorios/archivos que NO se escanean.
EXCLUDE_DIRS = {
    ".git", "node_modules", "venv", ".venv", "build", "dist",
    "__pycache__", ".stryker-tmp", ".mypy_cache", ".pytest_cache",
    "coverage", "htmlcov",
    # Las plantillas/ejemplos del kit usan valores de muestra a propósito.
    # En tu proyecto real, quitá estas exclusiones para auditar tus docs.
    "examples",
}
# El propio auditor contiene los patrones como literales → se auto-excluye.
EXCLUDE_FILES = {"audit_hallucinations.py"}

# Solo archivos de texto/código relevantes.
INCLUDE_SUFFIXES = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".env", ".sh", ".tf", ".md", ".txt",
    ".html", ".cjs", ".mjs",
}

_COMPILED = [(re.compile(rx, re.IGNORECASE), label, sev) for rx, label, sev in PATTERNS]


def _iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        if path.name in EXCLUDE_FILES:
            continue
        if path.suffix.lower() not in INCLUDE_SUFFIXES:
            continue
        yield path


def scan(root: Path) -> list[tuple[Path, int, str, str, str]]:
    """Devuelve hallazgos: (archivo, línea, etiqueta, severidad, fragmento)."""
    findings: list[tuple[Path, int, str, str, str]] = []
    for path in _iter_files(root):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for regex, label, sev in _COMPILED:
                if regex.search(line):
                    findings.append((path, lineno, label, sev, line.strip()[:120]))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Auditor anti-alucinaciones de IA.")
    parser.add_argument("path", nargs="?", default=".", help="Raíz a escanear (default: cwd).")
    parser.add_argument("--allow-warnings", action="store_true",
                        help="No fallar por severidad 'warning' (solo 'critical' bloquea).")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"❌ Ruta inexistente: {root}", file=sys.stderr)
        return 1

    findings = scan(root)
    if not findings:
        print("✅ Sin placeholders ni alucinaciones de IA detectadas.")
        return 0

    criticals = [f for f in findings if f[3] == "critical"]
    warnings = [f for f in findings if f[3] == "warning"]

    for path, lineno, label, sev, frag in findings:
        icon = "🔴" if sev == "critical" else "🟡"
        rel = path.relative_to(root) if path.is_relative_to(root) else path
        print(f"{icon} {rel}:{lineno}  [{label}]  {frag}")

    print()
    print(f"Resumen: {len(criticals)} críticos, {len(warnings)} warnings.")

    blocking = len(criticals) > 0 or (warnings and not args.allow_warnings)
    if blocking:
        print("❌ Auditoría FALLIDA — resolver los hallazgos antes de commitear.")
        return 1
    print("✅ Solo warnings (tolerados por --allow-warnings).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
