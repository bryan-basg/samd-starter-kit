"""Guardián: `check_placeholders.sh` mira TAMBIÉN `CLAUDE.md` (SaMD §5.7).

`CLAUDE.md` fija la clase SaMD y el uso previsto del proyecto derivado. Estuvo eximido del
gate con el motivo «la nota de cabecera cita {{...}} en prosa», pero ese `{{...}}` no encaja
con el patrón `{{MAYÚSCULAS}}` y `init_kit.sh` reemplaza los marcadores reales en TODO el
repo: la exención no protegía nada y dejaba ciega la puerta justo sobre ese archivo.
El script se copia a un repo git temporal; no se corre ninguna suite.
"""

import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
BASH = shutil.which("bash")

pytestmark = pytest.mark.skipif(BASH is None, reason="requiere bash")


def _repo(tmp_path: Path, claude_md: str) -> Path:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "scripts").mkdir()
    shutil.copy(ROOT / "scripts" / "check_placeholders.sh", tmp_path / "scripts")
    (tmp_path / "CLAUDE.md").write_text(claude_md, encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    return tmp_path


def _gate(repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [BASH, "scripts/check_placeholders.sh"], cwd=repo, capture_output=True, text=True, timeout=60
    )


def test_marcador_sin_reemplazar_en_claude_md_rojea(tmp_path):
    repo = _repo(tmp_path, "# ONBOARDING — {{PROJECT_NAME}}\nClase {{SAMD_CLASS}}\n")
    res = _gate(repo)
    assert res.returncode == 1, res.stdout
    assert "CLAUDE.md" in res.stdout


def test_claude_md_adaptado_con_prosa_de_puntos_suspensivos_pasa(tmp_path):
    repo = _repo(tmp_path, "# ONBOARDING — Mi Proyecto\nReemplazá los marcadores `{{...}}`.\n")
    res = _gate(repo)
    assert res.returncode == 0, res.stdout
