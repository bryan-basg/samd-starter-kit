"""Verificación del candado de la regla dura 2 (`.claude/scripts/candado_suite_completa.py`).

Cubre la función pura de decisión (`motivo_de_bloqueo`) y el `main` real vía subprocess con el
JSON que manda el hook `PreToolUse`: un subagente (entrada con `agent_id`) no puede correr la
suite completa ni los procesos pesados; la sesión principal (sin `agent_id`) pasa siempre.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / ".claude" / "scripts" / "candado_suite_completa.py"

_spec = importlib.util.spec_from_file_location("candado_suite_completa", SCRIPT)
assert _spec is not None and _spec.loader is not None
candado = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(candado)

# Comandos que un subagente NO puede correr (suite completa o proceso pesado).
BLOQUEADOS = [
    "pytest -q",
    "pytest tests/",
    "pytest tests/ -k foo",
    "python -m pytest -q",
    "venv/bin/pytest -q tests/",
    "bash scripts/run_local_ci.sh",
    "bash scripts/run_stryker.sh",
    "bash scripts/run_mutmut.sh",
    "bash scripts/run_schemathesis.sh",
    "bash scripts/run_zap_dast.sh",
    "bash scripts/run_pytest_postgres.sh",
    "cd frontend && npm test",
    "npm run test:e2e",
    "npx vitest run",
    "cd x && pytest tests/test_a.py && pytest -q",
]

# Comandos que un subagente SÍ puede correr (sus propios tests / escaneos cortos).
PERMITIDOS = [
    "pytest -q tests/test_a.py",
    "venv/bin/pytest -q tests/test_a.py tests/test_b.py",
    "pytest tests/test_a.py -k foo",
    "npm test -- src/a.test.ts",
    "npx vitest run src/carpeta",
    "bash scripts/run_trivy.sh",
    "bash scripts/run_semgrep.sh",
    "git status --short",
    "cat <<'EOF'\npytest -q\nEOF",
]


def _correr_hook(comando: str, con_agente: bool) -> subprocess.CompletedProcess[str]:
    entrada: dict[str, object] = {"tool_name": "Bash", "tool_input": {"command": comando}}
    if con_agente:
        entrada["agent_id"] = "agente-1"
    return subprocess.run(
        [sys.executable, str(SCRIPT)], input=json.dumps(entrada),
        capture_output=True, text=True, timeout=30, check=False)


@pytest.mark.parametrize("comando", BLOQUEADOS)
def test_motivo_de_bloqueo_detecta_suite_completa_y_pesados(comando: str) -> None:
    motivo = candado.motivo_de_bloqueo(comando)
    assert motivo is not None and motivo != ""


@pytest.mark.parametrize("comando", PERMITIDOS)
def test_motivo_de_bloqueo_deja_pasar_tests_propios_y_escaneos_cortos(comando: str) -> None:
    assert candado.motivo_de_bloqueo(comando) is None


def test_motivo_devuelve_el_tramo_ofensor() -> None:
    assert candado.motivo_de_bloqueo("cd x && pytest tests/ -k foo") == "pytest tests/ -k foo"


@pytest.mark.parametrize("comando", BLOQUEADOS)
def test_main_deniega_a_un_subagente(comando: str) -> None:
    res = _correr_hook(comando, con_agente=True)
    assert res.returncode == 0
    salida = json.loads(res.stdout)["hookSpecificOutput"]
    assert salida["hookEventName"] == "PreToolUse"
    assert salida["permissionDecision"] == "deny"
    assert "regla dura 2" in salida["permissionDecisionReason"]


@pytest.mark.parametrize("comando", PERMITIDOS)
def test_main_permite_a_un_subagente_sus_tests_propios(comando: str) -> None:
    res = _correr_hook(comando, con_agente=True)
    assert res.returncode == 0
    assert res.stdout == ""


@pytest.mark.parametrize("comando", BLOQUEADOS + PERMITIDOS)
def test_main_sesion_principal_sin_agent_id_pasa_todo(comando: str) -> None:
    res = _correr_hook(comando, con_agente=False)
    assert res.returncode == 0
    assert res.stdout == ""


def test_main_falla_abierto_ante_entrada_corrupta() -> None:
    res = subprocess.run([sys.executable, str(SCRIPT)], input="no es json",
                         capture_output=True, text=True, timeout=30, check=False)
    assert res.returncode == 0
    assert res.stdout == ""


def test_el_texto_del_motivo_no_afirma_que_npm_test_con_archivo_se_deniega() -> None:
    """El mensaje debe decir la verdad: `npm test -- <archivo>` corre solo ese archivo y pasa."""
    res = _correr_hook("pytest tests/ -k foo", con_agente=True)
    razon = json.loads(res.stdout)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "npm test --" not in razon
    assert "pytest tests/ -k" in razon
