"""Contrato de `scripts/ci_npm_audit_veredicto.py` (veredicto de `npm audit` en CI).

Todo aviso high/critical rojea salvo los tolerados por nombre, y cada tolerado
rojea a su vez cuando caduca o cuando ya no hace falta.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, Tuple

import pytest

_RUTA = Path(__file__).resolve().parents[1] / "scripts" / "ci_npm_audit_veredicto.py"
_SPEC = importlib.util.spec_from_file_location("ci_npm_audit_veredicto", _RUTA)
assert _SPEC and _SPEC.loader
v = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = v  # `@dataclass` resuelve su módulo por nombre
_SPEC.loader.exec_module(v)

HOY = date(2026, 10, 8)
TOLERADO = "GHSA-tolerado-0001"
TOLERADOS = {TOLERADO: v.Tolerado(paquete="braces", caduca=date(2026, 11, 8), motivo="sin parche")}


def _informe(*avisos: Tuple[str, str, str]) -> Dict[str, object]:
    """Forma de `npm audit --json`: el nodo con el aviso y un nodo que lo arrastra."""
    vulnerabilidades: Dict[str, object] = {}
    for ghsa, paquete, severidad in avisos:
        vulnerabilidades[paquete] = {
            "severity": severidad,
            "via": [{"name": paquete, "severity": severidad, "url": f"https://github.com/advisories/{ghsa}"}],
        }
        vulnerabilidades[f"arrastra-{paquete}"] = {"severity": severidad, "via": [paquete]}
    return {"vulnerabilities": vulnerabilidades, "metadata": {}}


def test_sin_avisos_que_frenan_es_verde() -> None:
    assert v.juzgar(_informe(("GHSA-mod", "uuid", "moderate")), 0, HOY, {}) == ([], [])


@pytest.mark.parametrize("severidad", ["high", "critical"])
def test_un_aviso_sin_tolerar_rojea(severidad: str) -> None:
    fallos, _ = v.juzgar(_informe(("GHSA-nuevo", "axios", severidad)), 1, HOY, {})
    assert fallos == ["GHSA-nuevo (axios): aviso high/critical sin tolerar."]


def test_el_tolerado_vigente_no_rojea_y_se_anuncia() -> None:
    fallos, aplicados = v.juzgar(_informe((TOLERADO, "braces", "high")), 1, HOY, TOLERADOS)
    assert fallos == []
    assert aplicados == [f"{TOLERADO} (braces) tolerado hasta el 2026-11-08"]


def test_el_tolerado_vale_hasta_su_fecha_inclusive_y_rojea_al_dia_siguiente() -> None:
    informe = _informe((TOLERADO, "braces", "high"))
    assert v.juzgar(informe, 1, date(2026, 11, 8), TOLERADOS)[0] == []
    fallos, aplicados = v.juzgar(informe, 1, date(2026, 11, 9), TOLERADOS)
    assert aplicados == []
    assert any("caducó el 2026-11-08" in f for f in fallos), fallos
    assert any("sin tolerar" in f for f in fallos), fallos


def test_el_tolerado_que_ya_no_aparece_rojea() -> None:
    fallos, _ = v.juzgar(_informe(), 0, HOY, TOLERADOS)
    assert fallos == [f"El tolerado {TOLERADO} (braces) ya no aparece: borralo de TOLERADOS."]


def test_tolerar_un_aviso_no_tolera_otro_del_mismo_paquete() -> None:
    informe = {
        "vulnerabilities": {
            "braces": {
                "severity": "high",
                "via": [
                    {"name": "braces", "severity": "high", "url": f"https://github.com/advisories/{TOLERADO}"},
                    {"name": "braces", "severity": "high", "url": "https://github.com/advisories/GHSA-otro"},
                ],
            }
        }
    }
    fallos, _ = v.juzgar(informe, 1, HOY, TOLERADOS)
    assert fallos == ["GHSA-otro (braces): aviso high/critical sin tolerar."]


@pytest.mark.parametrize(
    "exit_npm,avisos",
    [(1, ()), (0, (("GHSA-nuevo", "axios", "high"),))],
    ids=["npm-rojo-informe-vacio", "npm-verde-informe-con-high"],
)
def test_npm_y_el_informe_tienen_que_coincidir(exit_npm: int, avisos: Tuple[Tuple[str, str, str], ...]) -> None:
    fallos, _ = v.juzgar(_informe(*avisos), exit_npm, HOY, {})
    assert len(fallos) == 1 and "no coinciden" in fallos[0], fallos


@pytest.mark.parametrize("informe", [{"error": {"code": "ENOAUDIT"}}, [], {"vulnerabilities": []}])
def test_un_informe_sin_forma_no_se_aprueba(informe: object) -> None:
    with pytest.raises(ValueError):
        v.juzgar(informe, 1, HOY, {})


def test_el_workflow_corre_el_veredicto_sin_tapar_su_exit() -> None:
    """El enchufe: el job existe, llama a ESTE guion y nada le pone `|| true`."""
    import yaml

    flujo = yaml.safe_load((_RUTA.parents[1] / ".github" / "workflows" / "security-audit.yml").read_text(encoding="utf-8"))
    pasos = flujo["jobs"]["npm-audit"]["steps"]
    comandos = [p["run"] for p in pasos if "run" in p]
    assert any("ci_npm_audit_veredicto.py" in c for c in comandos), comandos
    assert not any("|| true" in c for c in comandos), comandos


def test_el_umbral_sigue_siendo_high() -> None:
    """Bajarlo a `critical` sería maquillar el medidor, no calibrarlo."""
    assert v.UMBRAL == "high"
    assert v.SEVERIDADES_QUE_FRENAN == frozenset({"high", "critical"})


def test_cada_tolerado_real_tiene_motivo_y_caduca_en_menos_de_90_dias() -> None:
    hoy = date.today()
    for ghsa, tolerado in v.TOLERADOS.items():
        assert ghsa.startswith("GHSA-"), ghsa
        assert tolerado.motivo.strip(), ghsa
        assert tolerado.caduca <= hoy + timedelta(days=90), (
            f"{ghsa} se tolera hasta {tolerado.caduca}: más de 90 días es un perdón, no una excepción."
        )


# --- El enchufe: `main` corre npm, guarda el informe y devuelve el veredicto ---


@pytest.mark.parametrize(
    "salida,exit_npm,esperado",
    [
        (json.dumps(_informe(("GHSA-nuevo", "axios", "high"))), 1, 1),
        (json.dumps(_informe(("GHSA-mod", "uuid", "moderate"))), 0, 0),
        ("npm ERR! sin red", 1, 1),
    ],
    ids=["high-sin-tolerar", "solo-moderate", "salida-que-no-es-json"],
)
def test_main_guarda_el_informe_y_juzga(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, salida: str, exit_npm: int, esperado: int
) -> None:
    monkeypatch.setattr(v, "ejecutar_npm_audit", lambda: (salida, exit_npm))
    monkeypatch.setattr(v, "TOLERADOS", {})
    destino = tmp_path / "npm-audit.json"
    assert v.main(["--informe", str(destino)]) == esperado
    assert destino.read_text(encoding="utf-8") == salida
