"""scripts/init_kit.sh — el primer comando del adoptante (auditoría 2026-11-24).

Moría por SIGPIPE sin mostrar los «Próximos pasos», no se podía re-correr y escribía valores que
rompían YAML, JSON o Python. Se copia el script a un repo mínimo: no toca el kit.
"""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
BASH = shutil.which("bash")
NOMBRES = [
    "PROJECT_NAME", "SAMD_CLASS", "INTENDED_USE", "OWNER", "FRONTEND_STACK",
    "BACKEND_STACK", "DB_STACK", "CLOUD_STACK", "CHAT_LANG",
]

pytestmark = pytest.mark.skipif(BASH is None, reason="requiere bash")


def _m(nombre: str) -> str:
    return "{" + "{" + nombre + "}" + "}"  # literal, `init_kit.sh` lo reemplazaría acá mismo


def _repo(tmp_path: Path) -> Path:
    (tmp_path / "scripts").mkdir()
    shutil.copy(ROOT / "scripts" / "init_kit.sh", tmp_path / "scripts")
    (tmp_path / "doc.md").write_text(" ".join(_m(n) for n in NOMBRES) + "\n")
    (tmp_path / "pendientes.md").write_text((_m("TODO") + " " + "x" * 200 + "\n") * 3000)
    return tmp_path


def _init(repo: Path, **valores: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if k not in NOMBRES} | valores
    return subprocess.run(
        [BASH, "scripts/init_kit.sh", "--yes"], cwd=repo, env=env,
        capture_output=True, text=True, timeout=60,
    )


def test_termina_bien_y_muestra_los_proximos_pasos(tmp_path):
    repo = _repo(tmp_path)
    valores = {n: "v" for n in NOMBRES} | {"SAMD_CLASS": "c"}
    res = _init(repo, **valores)
    assert res.returncode == 0, res.stderr
    assert "Próximos pasos" in res.stdout and "Tu clase: C" in res.stdout
    assert ".kit-adapted" in res.stdout and "CODEOWNERS" in res.stdout
    assert (repo / "doc.md").read_text() == "v C v v v v v v v\n"


def test_se_puede_re_correr_y_completa_lo_que_faltaba(tmp_path):
    repo = _repo(tmp_path)
    assert _init(repo, PROJECT_NAME="Uno").returncode == 0
    res = _init(repo, PROJECT_NAME="Uno", OWNER="yo")
    assert res.returncode == 0, res.stderr
    texto = (repo / "doc.md").read_text()
    assert "Uno" in texto and "yo" in texto and _m("DB_STACK") in texto


@pytest.mark.parametrize(
    "valor",
    ['Mi "Salud"', "D'Angelo", "C:\\Uno", "a`id`", "a$HOME", "Uno: dos", "a #b", "dos\nlíneas", _m("OWNER")],
)
def test_un_valor_que_rompe_archivos_se_rechaza_sin_cambiar_nada(tmp_path, valor):
    repo = _repo(tmp_path)
    antes = (repo / "doc.md").read_text()
    res = _init(repo, PROJECT_NAME="Bien", OWNER=valor)
    assert res.returncode == 1 and "OWNER" in res.stderr
    assert (repo / "doc.md").read_text() == antes


@pytest.mark.parametrize("valor", ["Niño & Cía/2", "D’Angelo", "a|b", "[x] (y) *z*", "C++ 50%", "a:b"])
def test_un_valor_normal_se_escribe_tal_cual(tmp_path, valor):
    repo = _repo(tmp_path)
    assert _init(repo, PROJECT_NAME=valor).returncode == 0
    assert valor in (repo / "doc.md").read_text()
