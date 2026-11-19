"""Guardián: el job backend de `ci.yml` corre los auditores del pre-commit (SaMD §5.7).

`scripts/audit_hallucinations.py` y `scripts/audit_smells.py` tienen tests propios de su
lógica (incluido el fail-closed con 0 archivos), pero un test de la pieza no prueba que alguien
la llame: sin estos pasos en el CI solo corrían con el hook instalado. Borrar cualquiera de las
dos llamadas del flujo tiene que romper este test (el enchufe, no solo la lógica).
"""

from pathlib import Path

import yaml

CI = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "ci.yml"
BACKEND = yaml.safe_load(CI.read_text(encoding="utf-8"))["jobs"]["backend"]["steps"]


def _comandos() -> str:
    return "\n".join(p["run"] for p in BACKEND if "run" in p)


def test_el_job_backend_corre_los_dos_auditores_del_pre_commit():
    comandos = _comandos()
    assert "python scripts/audit_hallucinations.py" in comandos
    assert "python scripts/audit_smells.py" in comandos


def test_los_auditores_no_se_tapan():
    for paso in BACKEND:
        if "audit_" in paso.get("run", ""):
            assert "|| true" not in paso["run"], paso.get("name")
            assert not paso.get("continue-on-error"), paso.get("name")
