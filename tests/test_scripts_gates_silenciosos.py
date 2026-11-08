"""Gates de scripts/*.sh que antes daban verde (o bajaban otra cosa) en silencio.

SaMD §5.7: un gate que no corrió no pasa. Cada test copia el script a un repo git temporal y
ejercita SOLO la rama del fallo; no se ejecuta ninguna suite, ni Stryker, ni npm.
"""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
BASH = shutil.which("bash")

pytestmark = pytest.mark.skipif(BASH is None, reason="requiere bash")


def _git_repo(tmp_path: Path, *scripts: str) -> Path:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "scripts").mkdir()
    for name in scripts:
        shutil.copy(SCRIPTS / name, tmp_path / "scripts" / name)
    return tmp_path


def _sh(repo: Path, script: str, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [BASH, f"scripts/{script}"], cwd=repo, capture_output=True, text=True, timeout=60,
        env=env if env is not None else os.environ.copy(),
    )


# --- check_doc_links.sh: enlaces con y sin prefijo -----------------------------------------

def test_doc_links_caza_rotos_con_y_sin_prefijo_e_ignora_externos(tmp_path):
    repo = _git_repo(tmp_path, "check_doc_links.sh")
    (repo / "docs" / "sub").mkdir(parents=True)
    (repo / "docs" / "real.md").write_text("ok\n")
    (repo / "docs" / "sub" / "a.md").write_text(
        "[ok](../real.md) [ancla](#x) [web](https://x.com/a.md) [mail](mailto:a@b.md)\n"
        "[r1](docs/NOPE.md) [r2](NOPE2.md#sec) [r3](./nope3.md) [r4](../nope4.md)\n"
    )
    res = _sh(repo, "check_doc_links.sh")
    assert res.returncode == 1
    for roto in ("docs/NOPE.md", "NOPE2.md#sec", "./nope3.md", "../nope4.md"):
        assert f"-> {roto}" in res.stdout, res.stdout
    assert "-> ../real.md" not in res.stdout
    assert "https://x.com" not in res.stdout
    assert "4 enlaces cross-doc rotos" in res.stdout


def test_doc_links_ok_cuando_todo_resuelve(tmp_path):
    repo = _git_repo(tmp_path, "check_doc_links.sh")
    (repo / "docs").mkdir()
    (repo / "docs" / "b.md").write_text("fin\n")
    (repo / "docs" / "a.md").write_text("[b](b.md) [b2](./b.md#s)\n")
    res = _sh(repo, "check_doc_links.sh")
    assert res.returncode == 0, res.stdout
    assert "OK: 0 enlaces" in res.stdout


# --- run_local_ci.sh: herramienta faltante = FALLO, no "[CI] OK" -----------------------------

def _path_solo_con_git(tmp_path: Path) -> str:
    """PATH que tiene git y nada más: ruff/mypy/pytest/npm no existen."""
    bindir = tmp_path / "solo_git"
    bindir.mkdir()
    (bindir / "git").symlink_to(shutil.which("git"))
    return str(bindir)


def test_local_ci_falla_si_faltan_ruff_mypy_pytest(tmp_path):
    repo = _git_repo(tmp_path / "r", "run_local_ci.sh")
    (repo / "tests").mkdir()
    env = {"PATH": _path_solo_con_git(tmp_path), "HOME": str(tmp_path)}
    res = _sh(repo, "run_local_ci.sh", env=env)
    assert res.returncode == 1
    for tool in ("ruff", "mypy", "pytest"):
        assert f"{tool} no instalado" in res.stdout, res.stdout
    assert "[CI] OK" not in res.stdout
    assert "1/5" not in res.stdout  # corta ANTES de gastar tiempo en el frontend


def test_local_ci_allow_missing_tools_avisa_y_sigue(tmp_path):
    repo = _git_repo(tmp_path / "r", "run_local_ci.sh")
    env = {"PATH": _path_solo_con_git(tmp_path), "HOME": str(tmp_path), "ALLOW_MISSING_TOOLS": "1"}
    res = _sh(repo, "run_local_ci.sh", env=env)
    assert "SALTEADO (ALLOW_MISSING_TOOLS=1)" in res.stdout
    assert "[CI] 1/5" in res.stdout  # no cortó en el preflight


# --- run_stryker.sh: sin @stryker-mutator NO baja el paquete legado --------------------------

@pytest.mark.skipif(shutil.which("npx") is None, reason="requiere npx")
def test_stryker_no_instalado_falla_con_mensaje_y_no_descarga(tmp_path):
    repo = _git_repo(tmp_path, "run_stryker.sh")
    (repo / "frontend").mkdir()
    (repo / "frontend" / "package.json").write_text('{"name": "x"}\n')
    res = _sh(repo, "run_stryker.sh")
    assert res.returncode == 1
    assert "@stryker-mutator/core" in res.stderr
    assert "npm install --save-dev" in res.stderr
    assert not (repo / "frontend" / "node_modules").exists()  # nada descargado


def test_stryker_usa_no_install_en_todas_las_invocaciones():
    for linea in (SCRIPTS / "run_stryker.sh").read_text().splitlines():
        if "npx" in linea and not linea.lstrip().startswith("#"):
            assert "--no-install" in linea, linea
