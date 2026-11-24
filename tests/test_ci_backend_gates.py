"""Guardián: los workflows de PR corren los gates que dicen correr (SaMD §5.7).

Cada script tiene tests propios de su lógica, pero un test de la pieza no prueba que alguien la
llame: cambiar `bash scripts/check_coverage.sh` por `true` dejaba toda la suite en verde. Borrar
o tapar cualquiera de estas llamadas tiene que romper este test (el enchufe, no solo la lógica).
"""

from pathlib import Path

import pytest
import yaml

WORKFLOWS = Path(__file__).resolve().parent.parent / ".github" / "workflows"

# (workflow, job) → líneas que tienen que estar TAL CUAL en algún `run:` de sus pasos.
EXIGIDOS = {
    ("ci.yml", "trace-integrity"): [
        "bash scripts/check_doc_links.sh",
        "python3 scripts/check_doc_anchors.py",
        "python3 scripts/check_doc_citations.py",
    ],
    ("ci.yml", "frontend"): [
        "npm ci",
        "npm run lint",
        "npm run typecheck",
        "npm run test -- --run",
        "npm run build",
    ],
    ("ci.yml", "backend"): [
        "ruff check app/ --select F401,F841,F811",
        "mypy .",
        "python scripts/audit_hallucinations.py",
        "python scripts/audit_smells.py",
        "bash scripts/check_coverage.sh",
    ],
    ("ci.yml", "imagen"): [
        "docker build -t kit-ci .",
        "docker run -d --name kit -e TESTING=True -p 8000:8000 kit-ci",
    ],
    ("ci.yml", "contract-sync"): [
        "python scripts/export_openapi.py --out /tmp/openapi.json",
        "git diff --no-index --exit-code frontend/src/api/openapi.json /tmp/openapi.json \\",
    ],
    ("kit-quality.yml", "kit-quality"): [
        "python scripts/lint_agents.py",
        "bash scripts/check_doc_links.sh",
        "python scripts/check_doc_anchors.py",
        "python scripts/check_doc_citations.py",
    ],
}


def _job(workflow: str, job: str) -> dict:
    return yaml.safe_load((WORKFLOWS / workflow).read_text(encoding="utf-8"))["jobs"][job]


@pytest.mark.parametrize(
    ("donde", "linea"),
    [(donde, linea) for donde, lineas in EXIGIDOS.items() for linea in lineas],
    ids=lambda v: v if isinstance(v, str) else v[1],
)
def test_el_workflow_corre_el_gate(donde: tuple[str, str], linea: str) -> None:
    lineas = [
        renglon.strip()
        for paso in _job(*donde)["steps"]
        for renglon in paso.get("run", "").splitlines()
    ]
    assert linea in lineas, f"{donde}: falta `{linea}` (o está tapado)"


@pytest.mark.parametrize("donde", EXIGIDOS, ids=lambda d: "/".join(d))
def test_ningun_gate_se_tapa(donde: tuple[str, str]) -> None:
    job = _job(*donde)
    assert not job.get("continue-on-error")
    for paso in job["steps"]:
        assert not paso.get("continue-on-error"), paso
        if "run" in paso:
            assert "if" not in paso, paso
            assert "|| true" not in paso["run"] and "set +e" not in paso["run"], paso
