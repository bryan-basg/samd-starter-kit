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

import pytest

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


# --- Verdes que mentían (auditoría 2026-11-24): cada uno daba «completo» con rc=0 -----------

@pytest.mark.parametrize("idioma", ["zh-CN", "ja_JP", "zh", "RU"])
def test_la_region_no_saca_al_idioma_del_gate_duro(tmp_path, idioma):
    _json(tmp_path, "locales/en.json", {"g": "Good morning friend"})
    _json(tmp_path, f"locales/{idioma}.json", {"g": "Good morning friend"})
    res = _run(tmp_path)
    assert res.returncode == 1 and "SIN TRADUCIR" in res.stdout, res.stdout


@pytest.mark.parametrize("texto", ["Buenos días", "Good morning to you"])
def test_texto_latino_de_otro_idioma_en_locale_no_latino_da_rc1(tmp_path, texto):
    _json(tmp_path, "locales/en.json", {"g": "Good morning"})
    _json(tmp_path, "locales/ru.json", {"g": texto})
    assert _run(tmp_path).returncode == 1


@pytest.mark.parametrize("texto", ["Доброе утро", "Отправить email", "PDF", "{{name}}", "12 %"])
def test_traduccion_legitima_no_latina_pasa(tmp_path, texto):
    _json(tmp_path, "locales/en.json", {"g": "Good morning"})
    _json(tmp_path, "locales/ru.json", {"g": texto})
    res = _run(tmp_path)
    assert res.returncode == 0, res.stdout


@pytest.mark.parametrize("valor", ["", "   ", None, 3, ["x"], {}])
def test_valor_vacio_o_de_otro_tipo_da_rc1(tmp_path, valor):
    _json(tmp_path, "locales/en.json", {"a": "Alpha beta"})
    _json(tmp_path, "locales/es.json", {"a": valor})
    assert _run(tmp_path).returncode == 1


def test_base_vacia_admite_traduccion_vacia(tmp_path):
    _json(tmp_path, "locales/en.json", {"a": "", "b": "Beta"})
    _json(tmp_path, "locales/es.json", {"a": "", "b": "Be"})
    assert _run(tmp_path).returncode == 0


def test_lista_mas_corta_da_rc1(tmp_path):
    _json(tmp_path, "locales/en.json", {"pasos": ["One", "Two"]})
    _json(tmp_path, "locales/es.json", {"pasos": ["Uno"]})
    res = _run(tmp_path, "-v")
    assert res.returncode == 1 and "pasos.1" in res.stdout


def test_namespace_huerfano_da_rc1(tmp_path):
    for idioma, texto in (("en", "Save"), ("es", "Guardar")):
        _json(tmp_path, f"frontend/public/locales/{idioma}/common.json", {"s": texto})
    _json(tmp_path, "frontend/public/locales/es/viejo.json", {"s": "x"})
    res = _run(tmp_path)
    assert res.returncode == 1 and "viejo.json" in res.stdout


@pytest.mark.parametrize("superficie", ["frontend", "backend"])
def test_idiomas_sin_su_base_no_se_omiten(tmp_path, superficie):
    """Una superficie sana no tapa a la otra, que tiene idiomas pero no el base."""
    sana = {"frontend": "locales/{}.json", "backend": "frontend/public/locales/{}/c.json"}[superficie]
    rota = {"backend": "locales/{}.json", "frontend": "frontend/public/locales/{}/c.json"}[superficie]
    for idioma, texto in (("en", "Save"), ("es", "Guardar")):
        _json(tmp_path, sana.format(idioma), {"s": texto})
    _json(tmp_path, rota.format("en-US"), {"s": "Save"})
    res = _run(tmp_path)
    assert res.returncode == 1 and "pero no la base" in res.stdout, res.stdout
