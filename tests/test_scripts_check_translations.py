"""scripts/check_translations.py — el auditor i18n caza lo real y no aprueba por vacío.

SaMD §5.7: sin locales en ninguna de las rutas configuradas el auditor imprimía «Todas las
traducciones están sincronizadas» con rc=0 sin haber leído un archivo. Ahora falla (fail-closed);
un proyecto con una sola superficie (solo frontend o solo backend) sigue pasando.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_translations.py"


def _run(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("I18N_")}
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, timeout=120, cwd=cwd, env=env,
    )


def _json(root: Path, rel: str, data: dict) -> None:
    f = root / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def test_sin_locales_en_ninguna_ruta_da_rc1(tmp_path):
    res = _run(tmp_path)
    assert res.returncode == 1
    assert "NADA que auditar" in res.stdout
    assert "sincronizadas" not in res.stdout


def test_base_frontend_sin_namespaces_cuenta_como_nada(tmp_path):
    (tmp_path / "frontend/public/locales/en").mkdir(parents=True)
    res = _run(tmp_path)
    assert res.returncode == 1
    assert "NADA que auditar" in res.stdout


def test_solo_frontend_en_paridad_da_rc0(tmp_path):
    _json(tmp_path, "frontend/public/locales/en/common.json", {"save": "Save"})
    _json(tmp_path, "frontend/public/locales/es/common.json", {"save": "Guardar"})
    res = _run(tmp_path)
    assert res.returncode == 0, res.stdout
    assert "sincronizadas" in res.stdout


def test_solo_backend_con_clave_faltante_da_rc1(tmp_path):
    _json(tmp_path, "locales/en.json", {"a": "Alpha", "b": "Beta"})
    _json(tmp_path, "locales/es.json", {"a": "Alfa"})
    res = _run(tmp_path, "-v")
    assert res.returncode == 1
    assert "falta:        b" in res.stdout


def test_copiado_sin_traducir_en_idioma_no_latino_da_rc1(tmp_path):
    _json(tmp_path, "locales/en.json", {"greeting": "Good morning"})
    _json(tmp_path, "locales/ja.json", {"greeting": "Good morning"})
    assert _run(tmp_path).returncode == 1
