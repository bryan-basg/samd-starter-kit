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
    "bash scripts/check_coverage.sh",
    "bash scripts/run_flaky_check.sh",
    "cd frontend && npm test",
    "npm run test:e2e",
    "npx vitest run",
    "cd x && pytest tests/test_a.py && pytest -q",
    # Envoltorios corrientes (auditoría 2026-11-24: pasaban todos).
    "uv run pytest",
    "poetry run pytest -q",
    "bash -c 'pytest -q'",
    'sh -c "cd x && pytest"',
    "bash -lc 'pytest'",
    "eval pytest",
    "(pytest -q)",
    "nohup pytest &",
    "nice -n 10 pytest",
    "sudo pytest",
    "timeout 60 pytest -q",
    "FOO=1 pytest",
    "python3.12 -m pytest -q",
    "python -mpytest",
    "coverage run -m pytest",
    "python -m coverage run -m pytest",
    "pytest ./",
    "pytest tests/./",
    "pytest -q tests/../tests",
    "pytest /repo/tests",
    "pytest -q tests/test_a.py tests/",
    "pytest -q --cov-config .coveragerc",
    "pytest --numprocesses auto",
    "pnpm test",
    "yarn test",
    "npm --prefix frontend test",
    "npm test --prefix frontend",
    "npm exec vitest",
    "npx -y vitest run",
    "npx playwright test",
    "mutmut run",
    "bash -x scripts/check_coverage.sh",
    "source scripts/check_coverage.sh",
    "bash <<'X'\npytest -q\nX",
    "cat <<< hola\npytest",
    "echo $((1 << 2))\npytest",
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
    "cat > f.sh <<EOF\npytest\nEOF",
    "pytest --version",
    "pytest --collect-only -q",
    "pytest tests/ --co",
    "vitest --version",
    "uv run pytest tests/test_a.py",
    "bash -c 'pytest tests/test_a.py'",
    "python3.12 -m pytest tests/test_a.py",
    "npm --prefix frontend test -- src/a.test.ts",
    "pnpm test src/a.test.ts",
    "npm ci",
    "npm run lint",
    "bash scripts/sast.sh",
    "make test",
    "echo pytest",
    "pip install pytest",
    "git commit -m 'x; pytest'",
    "pytest tests/unit/",
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


def test_el_hook_esta_enchufado_a_bash_y_apunta_al_script() -> None:
    """El enchufe, no solo la pieza: matcher `Bash` y una ruta que existe."""
    raiz = SCRIPT.parents[2]
    hooks = json.loads((raiz / ".claude" / "settings.json").read_text(encoding="utf-8"))["hooks"]
    comandos = [
        h["command"]
        for grupo in hooks["PreToolUse"] if grupo["matcher"] == "Bash"
        for h in grupo["hooks"]
    ]
    assert any(SCRIPT.relative_to(raiz).as_posix() in c for c in comandos), hooks["PreToolUse"]
