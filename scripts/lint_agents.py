#!/usr/bin/env python3
"""lint_agents.py — Verificación estructural del propio kit (IEC 62304 §5.7).

El SaMD Starter Kit pone reglas duras sobre el código de los proyectos que lo
usan; este script aplica el mismo rigor al kit MISMO: valida que el equipo de
agentes (`.claude/agents/*.md`), los comandos (`.claude/commands/*.md`) y las
skills (`.claude/skills/*/SKILL.md`) tengan la estructura mínima que la
documentación promete. Un agente sin `tools`, una skill sin `description` o un
comando sin frontmatter son fallos de configuración silenciosos: un agente que
se invoca y no arranca degrada de forma NO predecible. Esto es verificación
demostrable del kit como herramienta de soporte (IEC 62304 §5.7).

Contrato real (derivado de los archivos existentes, no inventado):

  - `.claude/agents/*.md`     → frontmatter YAML con `name`, `description`,
                                `tools`, los tres no vacíos.
  - `.claude/commands/*.md`   → frontmatter YAML con `description` no vacía
                                (el `name` es opcional: los comandos se nombran
                                por su archivo, p. ej. `samd-trace.md`).
  - `.claude/skills/*/SKILL.md` → frontmatter YAML con `name` y `description`
                                no vacíos + al menos una cabecera Markdown
                                (`# ...`) en el cuerpo.

Sin dependencias externas: el frontmatter se parsea a mano (subconjunto YAML
suficiente para `clave: valor` en bloque `---`). Si `pyyaml` está disponible se
usa como parser preferente, pero NO es requisito.

Salida legible (✓/✗ por archivo). Exit 1 ante cualquier fallo, 0 si todo OK.

Uso:
    python scripts/lint_agents.py
"""

from __future__ import annotations

import sys
from pathlib import Path

try:  # pyyaml es opcional — si no está, caemos al parser mínimo de abajo.
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - depende del entorno
    yaml = None  # type: ignore


REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO_ROOT / ".claude" / "agents"
COMMANDS_DIR = REPO_ROOT / ".claude" / "commands"
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"

# Claves obligatorias (no vacías) por tipo de artefacto.
AGENT_REQUIRED = ("name", "description", "tools")
COMMAND_REQUIRED = ("description",)
SKILL_REQUIRED = ("name", "description")


def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Separa el bloque frontmatter `---...---` del cuerpo.

    Devuelve `(frontmatter_crudo | None, cuerpo)`. Si no hay frontmatter al
    inicio del archivo, el primer elemento es None.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            fm = "\n".join(lines[1:idx])
            body = "\n".join(lines[idx + 1 :])
            return fm, body
    # Abrió `---` pero nunca cerró → frontmatter malformado.
    return None, text


def parse_frontmatter(fm: str) -> dict[str, str]:
    """Parsea el frontmatter a `dict[str, str]`.

    Usa pyyaml si está; si no, un parser mínimo de `clave: valor` por línea
    (suficiente para el frontmatter plano de agentes/comandos/skills). Los
    valores se normalizan a string y se les quita whitespace de los bordes.
    """
    if yaml is not None:
        try:
            data = yaml.safe_load(fm) or {}
        except yaml.YAMLError:
            return {}
        if not isinstance(data, dict):
            return {}
        return {str(k): "" if v is None else str(v).strip() for k, v in data.items()}

    result: dict[str, str] = {}
    for raw in fm.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        # Solo claves de primer nivel (sin indentación) — el frontmatter del
        # kit es plano; ignoramos sub-claves indentadas para no confundir
        # listas YAML con pares clave:valor.
        if line[0] in (" ", "\t"):
            continue
        key, _, value = line.partition(":")
        result[key.strip()] = value.strip().strip("'\"")
    return result


def check_file(path: Path, required: tuple[str, ...], *, need_heading: bool = False) -> list[str]:
    """Valida un archivo. Devuelve la lista de errores (vacía si OK)."""
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:  # pragma: no cover - I/O del entorno
        return [f"no se pudo leer: {exc}"]

    fm, body = split_frontmatter(text)
    if fm is None:
        return ["sin frontmatter YAML (`---` al inicio)"]

    data = parse_frontmatter(fm)
    for key in required:
        if key not in data:
            errors.append(f"falta la clave `{key}`")
        elif not data[key].strip():
            errors.append(f"la clave `{key}` está vacía")

    if need_heading and not any(
        line.lstrip().startswith("#") for line in body.splitlines()
    ):
        errors.append("sin cabecera Markdown (`# ...`) en el cuerpo")

    return errors


def lint_group(
    title: str,
    files: list[Path],
    required: tuple[str, ...],
    *,
    need_heading: bool = False,
    require_present: bool = True,
) -> bool:
    """Lintea un grupo de archivos. Devuelve True si el grupo pasó."""
    print(f"\n== {title} ==")
    if not files:
        if require_present:
            print("  ✗ no se encontró ningún archivo (se esperaba al menos uno)")
            return False
        print("  (sin archivos — omitido)")
        return True

    ok = True
    for path in sorted(files):
        rel = path.relative_to(REPO_ROOT)
        errors = check_file(path, required, need_heading=need_heading)
        if errors:
            ok = False
            print(f"  ✗ {rel}")
            for err in errors:
                print(f"      - {err}")
        else:
            print(f"  ✓ {rel}")
    return ok


def main() -> int:
    print("lint_agents.py — verificación estructural del kit (IEC 62304 §5.7)")
    parser = "pyyaml" if yaml is not None else "parser mínimo interno"
    print(f"Parser de frontmatter: {parser}")

    agents = list(AGENTS_DIR.glob("*.md"))
    commands = list(COMMANDS_DIR.glob("*.md"))
    skills = list(SKILLS_DIR.glob("*/SKILL.md"))

    results = [
        lint_group("Agentes (.claude/agents/*.md)", agents, AGENT_REQUIRED),
        lint_group("Comandos (.claude/commands/*.md)", commands, COMMAND_REQUIRED),
        # Las skills pueden no existir en un proyecto recién clonado → no se
        # exige presencia, pero las que existan deben cumplir el contrato.
        lint_group(
            "Skills (.claude/skills/*/SKILL.md)",
            skills,
            SKILL_REQUIRED,
            need_heading=True,
            require_present=False,
        ),
    ]

    print()
    if all(results):
        print("OK: todos los artefactos del kit cumplen la estructura mínima.")
        return 0
    print("FALLO: hay artefactos del kit con estructura inválida (ver ✗ arriba).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
