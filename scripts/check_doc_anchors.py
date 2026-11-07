#!/usr/bin/env python3
"""Verifica que los enlaces ``](#ancla)`` y ``](archivo.md#ancla)`` de la
documentación apunten a un título que existe de verdad.

Por qué existe (IEC 62304 §5.7 — la documentación del DHF es un entregable
verificable): ``scripts/check_doc_links.sh`` comprueba que el ARCHIVO destino
exista, pero descarta el fragmento ``#ancla``. Un título renombrado deja el
enlace "sano" para el link-checker y roto para quien lo pulsa. El caso típico
es escribir el ancla a mano SIN acentos mientras el slug real de GitHub los
conserva: ``#refutacion`` contra un título «Refutación».

Usa el mismo algoritmo de slug que GitHub (github-slugger): minúsculas, se
conservan letras (también acentuadas), números, ``-`` y ``_``, se elimina el
resto de la puntuación, cada espacio literal pasa a ``-`` (sin colapsar los
consecutivos) y los títulos repetidos se desambiguan con sufijo ``-1``, ``-2``.
También acepta las anclas explícitas ``<a id="...">`` / ``<a name="...">``.

Uso:
    python3 scripts/check_doc_anchors.py             # docs/ + *.md de la raíz
    python3 scripts/check_doc_anchors.py --paths X   # rutas puntuales

Exit code 1 si hay anclas rotas (lo corre el CI).
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
# ](#ancla)  o  ](archivo.md#ancla). No engancha URLs http(s).
ANCHOR_LINK_RE = re.compile(r"\]\(([^)\s]*?\.md)?#([^)\s]+)\)")
EXPLICIT_ANCHOR_RE = re.compile(r'<a\s+(?:id|name)="([^"]+)"')

# Sintaxis markdown que se limpia de un título antes de sluggificarlo, igual
# que hace el renderizador antes de pasarle el texto a github-slugger.
CODE_RE = re.compile(r"`([^`]*)`")
LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
EMPHASIS_RE = re.compile(r"(\*\*|\*|__|_)")


def clean_heading_text(raw: str) -> str:
    text = CODE_RE.sub(r"\1", raw)
    text = LINK_RE.sub(r"\1", text)
    return EMPHASIS_RE.sub("", text)


def github_slug(text: str) -> str:
    """Réplica de github-slugger para un título ya limpio."""
    out: list[str] = []
    for ch in text.strip().lower():
        if ch == " ":
            out.append("-")
        elif ch in ("-", "_") or ch.isalnum():
            out.append(ch)
        elif unicodedata.category(ch).startswith("M"):
            out.append(ch)  # marca combinante (acento descompuesto)
        # el resto de la puntuación/símbolos se descarta
    return "".join(out)


def build_slug_index(text: str) -> set[str]:
    """Slugs reales del documento (con desambiguación de duplicados) más las
    anclas explícitas ``<a id>``. Ignora lo que está dentro de bloques de código."""
    seen: dict[str, int] = {}
    slugs: set[str] = set()
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if match:
            base = github_slug(clean_heading_text(match.group(2)))
            if base in seen:
                seen[base] += 1
                slugs.add(f"{base}-{seen[base]}")
            else:
                seen[base] = 0
                slugs.add(base)
        for explicit in EXPLICIT_ANCHOR_RE.finditer(line):
            slugs.add(explicit.group(1))
    return slugs


def find_anchor_links(text: str) -> list[tuple[str | None, str]]:
    """(archivo_destino_o_None, ancla) de cada enlace con fragmento, sin mirar
    bloques de código ni spans de código inline (un enlace escrito COMO TEXTO
    dentro de backticks no es un enlace real)."""
    found: list[tuple[str | None, str]] = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in ANCHOR_LINK_RE.finditer(CODE_RE.sub("", line)):
            anchor = match.group(2)
            # `#/ruta` no es el ancla de un título: es una ruta de la app
            # (router por fragmento). Tratarla como ancla daría falsos rojos.
            if anchor.startswith("/"):
                continue
            found.append((match.group(1), anchor))
    return found


def check_file(path: Path, root: Path) -> list[str]:
    """Anclas rotas de ``path`` (contra sí mismo o contra su archivo destino)."""
    text = path.read_text(encoding="utf-8")
    cache: dict[Path, set[str]] = {path: build_slug_index(text)}
    broken: list[str] = []
    for target_file, anchor in find_anchor_links(text):
        target = path if target_file is None else (path.parent / target_file).resolve()
        if target not in cache:
            cache[target] = (
                build_slug_index(target.read_text(encoding="utf-8"))
                if target.exists()
                else set()
            )
        if anchor not in cache[target]:
            destino = target_file or "(mismo archivo)"
            broken.append(f"{path.relative_to(root)}: ancla rota #{anchor} -> {destino}")
    return broken


def default_files(root: Path) -> list[Path]:
    return sorted((root / "docs").rglob("*.md")) + sorted(root.glob("*.md"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verifica que los enlaces con #ancla apunten a un título real."
    )
    parser.add_argument("--paths", nargs="*", default=None, help="Rutas puntuales a escanear")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    files = [Path(p).resolve() for p in args.paths] if args.paths else default_files(root)

    broken: list[str] = []
    for f in files:
        broken.extend(check_file(f, root))

    if broken:
        print(f"ANCLAS ROTAS: {len(broken)}")
        for line in broken:
            print(f"  BROKEN: {line}")
        return 1
    print(f"Anclas internas OK (0 rotas, {len(files)} archivos).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
