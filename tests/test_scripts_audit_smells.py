"""scripts/audit_smells.py — el gate de smells caza lo real y no aprueba por vacío.

SaMD §5.7: un gate en verde solo vale si miró algo. Mismo defecto que el issue #96 en
`audit_hallucinations.py`: las exclusiones miraban la ruta ABSOLUTA, así que un BASE_DIR bajo
`/build/` o `/work/dist/` se excluía entero y el gate daba rc=0 sin escanear un archivo.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "audit_smells.py"

SMELL = "import time\n\n\nasync def f():\n    time." + "sleep(1)\n"
CLEAN = "async def f():\n    return 1\n"


def _run(base_dir: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, "BASE_DIR": str(base_dir)}
    return subprocess.run(
        [sys.executable, str(SCRIPT)], capture_output=True, text=True, timeout=120, env=env
    )


def _write(root: Path, rel: str, text: str) -> None:
    f = root / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text, encoding="utf-8")


def test_backend_del_kit_limpio_da_rc0():
    res = _run(ROOT / "app")
    assert res.returncode == 0, res.stdout + res.stderr
    assert "archivos revisados" in res.stdout


def test_sabotaje_io_bloqueante_en_async_da_rc1(tmp_path):
    _write(tmp_path, "svc.py", SMELL)
    res = _run(tmp_path)
    assert res.returncode == 1
    assert "svc.py:5" in res.stdout


@pytest.mark.parametrize("ancestro", ["build", "dist", "tests", "node_modules", ".venv"])
def test_base_dir_bajo_directorio_excluido_se_escanea(tmp_path, ancestro):
    base = tmp_path / ancestro / "app"
    _write(base, "svc.py", SMELL)
    res = _run(base)
    assert res.returncode == 1, res.stdout + res.stderr
    assert "svc.py:5" in res.stdout


def test_exclusion_por_nombre_sigue_valiendo_dentro_de_base_dir(tmp_path):
    _write(tmp_path, "tests/test_x.py", SMELL)
    _write(tmp_path, "build/gen.py", SMELL)
    _write(tmp_path, "svc.py", CLEAN)
    res = _run(tmp_path)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "(1 archivos revisados)" in res.stdout


def test_cero_archivos_escaneados_da_rc1(tmp_path):
    _write(tmp_path, "tests/test_x.py", CLEAN)  # todo excluido
    res = _run(tmp_path)
    assert res.returncode == 1
    assert "0 archivos .py escaneados" in res.stderr
    assert "Sin smells" not in res.stdout


def test_base_dir_inexistente_da_rc1(tmp_path):
    assert _run(tmp_path / "no-existe").returncode == 1
