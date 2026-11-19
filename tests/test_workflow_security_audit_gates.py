"""Guardián: los gates de Trivy y Semgrep de `security-audit.yml` pueden ponerse en rojo.

SaMD §5.7: un gate que se puede apagar sin que nada rojee es un verde que miente. Para npm
audit ya existe el anclaje (`test_ci_npm_audit_veredicto.py`); acá se fija lo mismo para
los otros dos: umbral HIGH/CRITICAL con `exit-code: '1'` en Trivy y `--error` sin `|| true` en
Semgrep. Borrar cualquiera de esas piezas tiene que romper este test.
"""

from pathlib import Path

import yaml

WORKFLOW = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "security-audit.yml"
JOBS = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))["jobs"]


def _pasos(job: str) -> list[dict]:
    return JOBS[job]["steps"]


def test_trivy_frena_en_high_y_critical():
    trivy = next(p for p in _pasos("trivy") if "trivy-action" in p.get("uses", ""))
    with_ = trivy["with"]
    assert str(with_["exit-code"]) == "1"
    assert set(with_["severity"].split(",")) == {"HIGH", "CRITICAL"}
    assert "vuln" in with_["scanners"].split(",")


def test_semgrep_falla_con_hallazgos_y_no_se_tapa():
    comandos = [p["run"] for p in _pasos("semgrep") if "run" in p]
    semgrep = next(c for c in comandos if "semgrep" in c)
    assert "--error" in semgrep
    assert "|| true" not in semgrep
    assert "app/" in semgrep and "frontend/src/" in semgrep


def test_pip_audit_audita_el_backend_y_no_se_tapa():
    comandos = [p["run"] for p in _pasos("pip-audit") if "run" in p]
    auditoria = next(c for c in comandos if c.startswith("pip-audit"))
    assert "-r requirements.txt" in auditoria
    assert "|| true" not in auditoria
    assert any(c.startswith("pip install pip-audit==") for c in comandos), "versión sin pinear"


def test_ningun_job_de_seguridad_puede_fallar_en_silencio():
    for nombre, job in JOBS.items():
        assert not job.get("continue-on-error"), nombre
        for paso in job["steps"]:
            assert not paso.get("continue-on-error"), (nombre, paso.get("name"))
            assert "|| true" not in paso.get("run", ""), (nombre, paso.get("name"))
