"""Gates de scripts/*.sh que antes daban verde (o bajaban otra cosa) en silencio.

SaMD §5.7: un gate que no corrió no pasa. Cada test copia el script a un repo git temporal y
ejercita SOLO la rama del fallo; no se ejecuta ninguna suite, ni Stryker, ni npm.
"""

import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
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


# --- Verdes que mentían (auditoría 2026-11-24) ----------------------------------------------

def _ejecutable(ruta: Path, cuerpo: str) -> Path:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(f"#!{BASH}\n{cuerpo}\n")
    ruta.chmod(0o755)
    return ruta


def _coverage(repo: Path, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("COV")}
    return subprocess.run(
        [sys.executable, "-m", "coverage", *args], cwd=repo, env=env,
        capture_output=True, text=True, timeout=60,
    )


def _repo_medido(tmp_path: Path, modelo: str) -> Path:
    """Repo con el `.coveragerc` REAL y datos de cobertura: global ≥ 95 %, la capa SQL según `modelo`."""
    repo = _git_repo(tmp_path, "check_coverage.sh")
    shutil.copy(ROOT / ".coveragerc", repo / ".coveragerc")
    (repo / "app" / "models").mkdir(parents=True)
    (repo / "app" / "models" / "m.py").write_text(modelo)
    (repo / "app" / "grande.py").write_text("".join(f"x{i} = {i}\n" for i in range(400)))
    (repo / "t.py").write_text("import app.grande, app.models.m\napp.models.m.f(1)\n")
    medido = _coverage(repo, "run", "t.py")
    assert medido.returncode == 0, medido.stderr
    assert _coverage(repo, "combine").returncode == 0
    (repo / ".coverage").rename(repo / "datos")
    _ejecutable(repo / "bin" / "pytest", "cp datos .coverage")
    _ejecutable(repo / "bin" / "coverage", f'exec "{sys.executable}" -m coverage "$@"')
    return repo


def _gate_cobertura(repo: Path) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("COV")}
    env |= {"PYTEST_BIN": "bin/pytest", "COVERAGE_BIN": "bin/coverage"}
    return _sh(repo, "check_coverage.sh", env=env)


def test_el_piso_sql_rojea_aunque_el_global_este_bien(tmp_path):
    repo = _repo_medido(tmp_path, "def f(x):\n    if x:\n        return 1\n    a = 2\n    return a\n")
    res = _gate_cobertura(repo)
    assert res.returncode == 1, res.stdout
    assert "capa datos/SQL por DEBAJO" in res.stdout
    assert "global por DEBAJO" not in res.stdout  # rojea por la capa, no por el total


def test_el_piso_sql_pasa_con_la_capa_cubierta(tmp_path):
    res = _gate_cobertura(_repo_medido(tmp_path, "def f(x):\n    return x\n"))
    assert res.returncode == 0, res.stdout
    assert "piso omitido" not in res.stdout


def test_un_comentario_con_puntos_suspensivos_no_esconde_la_rama(tmp_path):
    modelo = (
        "def f(x):\n"
        "    if x > 100:  # rama: ...\n"
        "        return 1\n"
        "    return 0\n"
        "\n\ndef stub(a: int) -> int: ...\n"
        "\n\nasync def stub2(\n    a: int,\n) -> int: ...\n"
        "\n\nclass E(Exception): ...\n"
        "\n\ndef stub3():\n    ...\n"
    )
    repo = _repo_medido(tmp_path, modelo)
    shutil.copy(repo / "datos", repo / ".coverage")
    salida = _coverage(repo, "report", "--include=app/models/*", "--fail-under=0").stdout
    fila = next(linea for linea in salida.splitlines() if "models/m.py" in linea)
    assert fila.split()[-1] == "3", fila  # solo la rama real; los stubs siguen excluidos


@pytest.mark.parametrize("script", ["check_placeholders.sh", "check_doc_links.sh"])
def test_desde_otro_directorio_mira_el_repo_y_no_el_vacio(tmp_path, script):
    repo = _git_repo(tmp_path / "r", script)
    marcador = "{" + "{OWNER}" + "}"
    (repo / "README.md").write_text(f"{marcador} [roto](NOPE.md)\n")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    afuera = tmp_path / "afuera"
    afuera.mkdir()
    res = subprocess.run(
        [BASH, str(repo / "scripts" / script)], cwd=afuera, capture_output=True, text=True, timeout=60
    )
    assert res.returncode == 1, res.stdout + res.stderr
    assert "README.md" in res.stdout


@pytest.mark.parametrize("script", ["check_placeholders.sh", "check_doc_links.sh"])
def test_sin_nada_que_mirar_no_da_ok(tmp_path, script):
    (tmp_path / "scripts").mkdir()  # copia sin git y sin documentos (ZIP recortado)
    shutil.copy(SCRIPTS / script, tmp_path / "scripts")
    res = _sh(tmp_path, script, env={**os.environ, "GIT_CEILING_DIRECTORIES": str(tmp_path.parent)})
    assert res.returncode == 2, res.stdout
    assert "OK:" not in res.stdout


def _commit(repo: Path, nombre: str) -> None:
    (repo / nombre).write_text("x\n")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@localhost", "commit", "-q", "-m", nombre],
        cwd=repo, check=True,
    )


def _kit_upgrade(tmp_path: Path, con_commit: bool) -> subprocess.CompletedProcess:
    kit = tmp_path / "kit"
    subprocess.run(["git", "init", "-q", "-b", "main", str(kit)], check=True)
    _commit(kit, "del_kit.txt")
    repo = _git_repo(tmp_path / "r", "kit_upgrade.sh")
    if con_commit:
        _commit(repo, "mio.txt")
    return _sh(repo, "kit_upgrade.sh", env={**os.environ, "KIT_UPSTREAM_URL": str(kit)})


def test_kit_upgrade_sin_commits_no_dice_al_dia(tmp_path):
    res = _kit_upgrade(tmp_path, con_commit=False)
    assert res.returncode == 1
    assert "todavía no tiene commits" in res.stderr
    assert "Estás al día" not in res.stdout


def test_kit_upgrade_avisa_si_no_hay_ancestro_comun(tmp_path):
    res = _kit_upgrade(tmp_path, con_commit=True)
    assert res.returncode == 0, res.stderr
    assert "no comparte ancestro" in res.stdout
    assert "Estás al día" not in res.stdout


@pytest.mark.parametrize(("superficial", "rc"), [(True, 3), (False, 0)])
def test_gitleaks_no_aprueba_un_clon_superficial(tmp_path, superficial, rc):
    origen = _git_repo(tmp_path / "o", "run_gitleaks.sh")
    _commit(origen, "a.txt")
    _commit(origen, "b.txt")
    clon = tmp_path / "clon"
    profundidad = ["--depth", "1"] if superficial else []
    subprocess.run(["git", "clone", "-q", *profundidad, f"file://{origen}", str(clon)], check=True)
    _ejecutable(tmp_path / "bin" / "gitleaks", "exit 0")
    res = _sh(clon, "run_gitleaks.sh", env={**os.environ, "PATH": f"{tmp_path / 'bin'}:{os.environ['PATH']}"})
    assert res.returncode == rc, res.stdout + res.stderr


@pytest.mark.parametrize(
    ("herramienta", "rc"),
    [
        ("exit 1", 1),  # la herramienta falla
        ("""echo '{"components": [{"name": "a"}]}' > "$salida"; exit 1""", 1),  # escribe y DESPUÉS falla
        ("""echo '{"components": []}' > "$salida" """, 1),  # termina bien y no encontró nada
        ("""echo '{"components": [{"name": "a"}]}' > "$salida" """, 0),
    ],
    ids=["falla", "escribe-y-falla", "vacio", "sano"],
)
def test_el_sbom_viejo_no_pasa_por_nuevo(tmp_path, herramienta, rc):
    repo = _git_repo(tmp_path, "generate_sbom.sh")
    (repo / "requirements.txt").write_text("a\n")
    venv = repo / "venv" / "bin"
    venv.mkdir(parents=True)
    (venv / "python").symlink_to(sys.executable)
    (venv / "activate").write_text(f'export PATH="{venv}:$PATH"\n')
    _ejecutable(
        venv / "cyclonedx-py",
        'while [ $# -gt 0 ]; do [ "$1" = "-o" ] && salida="$2"; shift; done\n' + herramienta,
    )
    viejo = '{"components": [{"name": "viejo"}]}'
    (repo / "sbom").mkdir()
    hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    local = datetime.now().strftime("%Y-%m-%d")
    for nombre in ("sbom-latest-backend.json", *(f"sbom-backend-cyclonedx-{d}.json" for d in {hoy, local})):
        (repo / "sbom" / nombre).write_text(viejo)
    res = subprocess.run(
        [BASH, "scripts/generate_sbom.sh", "--backend"], cwd=repo, capture_output=True, text=True, timeout=60
    )
    assert res.returncode == rc, res.stdout + res.stderr
    assert ("baseline OK" in res.stdout + res.stderr) is (rc == 0)
    assert ("viejo" in (repo / "sbom" / "sbom-latest-backend.json").read_text()) is (rc != 0)


def test_lint_agents_sin_reglas_no_aprueba(tmp_path):
    codigo = "import sys; sys.path.insert(0, 'scripts'); import lint_agents; print(lint_agents.lint_rules([]))"
    res = subprocess.run([sys.executable, "-c", codigo], cwd=ROOT, capture_output=True, text=True, timeout=60)
    assert res.stdout.strip().endswith("False"), res.stdout + res.stderr
