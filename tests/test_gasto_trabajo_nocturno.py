"""Contrato del semáforo de gasto de `/trabajo-nocturno` (`.claude/skills/trabajo-nocturno/scripts/gasto.py`).

Lo que importa no es el número exacto sino el fail-safe: sin dato NO hay verde, el semáforo
lo decide la PEOR ventana, y un modelo específico no cae en el precio de su familia.
"""
import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

_RAIZ = Path(__file__).resolve().parent.parent
_DIR = _RAIZ / ".claude/skills/trabajo-nocturno/scripts"
_spec = importlib.util.spec_from_file_location("gasto", _DIR / "gasto.py")
assert _spec is not None and _spec.loader is not None
gasto = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gasto)


def _correr(script: str, carpeta: Path, entrada: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(_DIR / script)], input=entrada, text=True, capture_output=True,
                          timeout=110, env={**os.environ, "SAMD_STATUSLINE_DIR": str(carpeta)})


def test_sin_dato_de_la_barra_no_hay_verde(tmp_path: Path) -> None:
    r = _correr("gasto.py", tmp_path)
    assert r.returncode == 2 and "SIN DATO" in r.stdout and "VERDE" not in r.stdout


def test_un_dato_de_una_ventana_ya_renovada_no_vale(tmp_path: Path) -> None:
    (tmp_path / "sesion-a.json").write_text(json.dumps(
        {"rate_limits": {"five_hour": {"used_percentage": 1, "resets_at": time.time() - 60}}}))
    r = _correr("gasto.py", tmp_path)
    assert r.returncode == 2 and "VERDE" not in r.stdout


def test_un_dato_viejo_no_da_verde_aunque_la_ventana_siga_abierta(tmp_path: Path) -> None:
    ruta = tmp_path / "sesion-a.json"
    ruta.write_text(json.dumps({"rate_limits": {"five_hour": {"used_percentage": 1, "resets_at": time.time() + 3600}}}))
    viejo = time.time() - gasto.EDAD_MAXIMA - 60
    os.utime(ruta, (viejo, viejo))
    r = _correr("gasto.py", tmp_path)
    assert r.returncode == 2 and "VERDE" not in r.stdout


@pytest.mark.parametrize(("peor", "color"), [(0, "VERDE"), (79.9, "VERDE"), (80, "AMARILLO"),
                                             (89.9, "AMARILLO"), (90, "ROJO"), (100, "ROJO")])
def test_umbrales_del_semaforo(peor: float, color: str) -> None:
    assert gasto.semaforo(peor).startswith(color)


def test_la_barra_guarda_lo_que_el_semaforo_lee(tmp_path: Path) -> None:
    """El enchufe: lo que escribe barra_estado.py es exactamente lo que gasto.py busca."""
    entrada = {"session_id": "s1", "model": {"display_name": "M"},
               "rate_limits": {"five_hour": {"used_percentage": 42, "resets_at": time.time() + 3600}}}
    r = _correr("barra_estado.py", tmp_path, json.dumps(entrada))
    assert r.returncode == 0 and "42 %" in r.stdout
    os.environ["SAMD_STATUSLINE_DIR"] = str(tmp_path)
    try:
        limites, _ = gasto.leer_limites()
    finally:
        del os.environ["SAMD_STATUSLINE_DIR"]
    assert limites is not None and limites["five_hour"]["used_percentage"] == 42


def test_la_barra_no_rompe_con_entrada_rota(tmp_path: Path) -> None:
    assert _correr("barra_estado.py", tmp_path, "no es json").returncode == 0


@pytest.mark.parametrize(("modelo", "esperado"), [
    ("claude-opus-5-5", (4, 20, 0.05)), ("claude-opus-5", (5, 25, 0.1)),
    ("claude-sonnet-5-5", (2, 10, 0.05)), ("claude-sonnet-5", (2, 10, 0.1)),
    ("claude-fable-5-2", (8, 40, 0.025)), ("claude-haiku-5-5", (0.10, 0.50, 0.1)),
])
def test_un_modelo_especifico_no_cae_en_el_precio_de_su_familia(modelo: str, esperado: tuple[float, ...]) -> None:
    assert next(v for k, v in gasto.PRECIOS.items() if k in modelo) == esperado


def test_la_cache_de_una_hora_cuesta_el_doble_de_la_entrada() -> None:
    uso = {"cache_creation": {"ephemeral_1h_input_tokens": 1_000_000}}
    assert gasto.precio(uso, "claude-opus-5-5") == pytest.approx(8.0)
