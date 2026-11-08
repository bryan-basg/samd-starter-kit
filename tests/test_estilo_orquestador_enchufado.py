"""Guardián del estilo de salida de la sesión principal (SaMD §5.7 — gobernanza verificable).

Las reglas que solo necesita la sesión principal (preferencias del dueño,
orquestación, sesiones paralelas) viven en `.claude/output-styles/orquestador.md`
para que los subagentes no las relean en cada turno (SCMP §2.1). Ese traslado
tiene dos modos de fallo silenciosos que este test caza:

1. **Enchufe roto**: `outputStyle` en `.claude/settings.json` no coincide EXACTO
   con el `name:` del frontmatter → Claude Code cae al estilo por defecto sin
   avisar, y la sesión principal pierde esas reglas.
2. **Duplicado**: la misma sección queda en el estilo Y en `CLAUDE.md` o en
   `.claude/rules/` → el ahorro desaparece y, peor, dos copias derivan una de otra.
"""

import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
ESTILO = ROOT / ".claude" / "output-styles" / "orquestador.md"
SETTINGS = ROOT / ".claude" / "settings.json"
CLAUDE_MD = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
ORQUESTACION = (ROOT / ".claude" / "rules" / "orquestacion.md").read_text(encoding="utf-8")


def _frontmatter() -> dict:
    texto = ESTILO.read_text(encoding="utf-8")
    assert texto.startswith("---\n"), "el estilo no abre con frontmatter YAML"
    return yaml.safe_load(texto.split("---")[1])


def test_settings_activa_el_estilo_por_su_nombre_exacto():
    settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
    assert settings.get("outputStyle") == _frontmatter()["name"]
    # El candado de la suite completa sigue enchufado al lado del estilo.
    assert "PreToolUse" in settings.get("hooks", {})


def test_el_estilo_conserva_las_instrucciones_de_ingenieria():
    assert _frontmatter().get("keep-coding-instructions") is True


@pytest.mark.parametrize(
    "seccion",
    [
        "### Idioma y registro",
        "### Modo tutor",
        "### Antes de actuar",
        "### Delegar en el especialista",
        "### Diseño de equipo — reglas A-F",
        "### Reglas duras de convivencia",
    ],
)
def test_el_estilo_trae_sus_secciones(seccion):
    assert seccion in ESTILO.read_text(encoding="utf-8")


def test_claude_md_remite_al_estilo_con_red_de_seguridad():
    assert ".claude/output-styles/orquestador.md" in CLAUDE_MD
    assert "NO está entre tus instrucciones" in CLAUDE_MD


@pytest.mark.parametrize(
    ("texto", "donde", "contenido"),
    [
        ("### Modo tutor", "CLAUDE.md", CLAUDE_MD),
        ("### Idioma y registro", "CLAUDE.md", CLAUDE_MD),
        ("Diseño de equipo — reglas A-F", "orquestacion.md", ORQUESTACION),
        ("Protocolo anti-drift", "orquestacion.md", ORQUESTACION),
    ],
)
def test_lo_movido_no_quedo_duplicado(texto, donde, contenido):
    assert texto not in contenido, f"«{texto}» sigue en {donde}: está duplicado con el estilo"


def test_lo_que_obedecen_todos_sigue_en_las_reglas_que_cargan_los_agentes():
    assert "## Reglas duras que un modelo mejor NO anula" in ORQUESTACION
    assert "## Higiene de contexto" in ORQUESTACION
    assert "## Antes de cantar verde" in ORQUESTACION
    assert "### Git y commits" in CLAUDE_MD
