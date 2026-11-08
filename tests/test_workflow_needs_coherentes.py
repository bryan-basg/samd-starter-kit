"""Guardián de coherencia `needs` ↔ contexto `needs.*` en los workflows (IEC 62304 §5.7).

En GitHub Actions el contexto `needs` contiene SOLO las dependencias DIRECTAS del job. Un
`if: needs.guard.outputs.enabled == 'true'` en un job que declara `needs: migrate` (y no
`guard`) se evalúa contra un contexto sin `guard`: el valor es vacío, la condición es falsa
y el job se SALTEA en silencio, sin error y con el workflow en verde. Eso era `deploy-backend`
en `deploy.yml`: el deploy no se ejecutaba y nada lo avisaba.

El conjunto se DERIVA de los workflows en disco: un workflow o job nuevo entra por existir.
"""

import json
import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"

# Piso del detector: no puede aprobar por vacío si el glob deja de encontrar workflows/jobs.
MINIMO_DE_JOBS_CON_NEEDS = 3

_REF_NEEDS = re.compile(r"\bneeds\.([A-Za-z_][A-Za-z0-9_-]*)|\bneeds\[\s*['\"]([^'\"]+)['\"]\s*\]")


def _archivos() -> list[Path]:
    return sorted(WORKFLOWS.glob("*.yml")) + sorted(WORKFLOWS.glob("*.yaml"))


def _needs_declarado(job: dict) -> set[str]:
    needs = job.get("needs", [])
    return {needs} if isinstance(needs, str) else set(needs or [])


def _needs_usado(job: dict) -> set[str]:
    """Jobs referenciados como `needs.X` en CUALQUIER parte del job salvo su propio `needs:`."""
    cuerpo = {k: v for k, v in job.items() if k != "needs"}
    texto = json.dumps(cuerpo, ensure_ascii=False)
    return {a or b for a, b in _REF_NEEDS.findall(texto)}


def incoherencias(workflow: dict) -> list[str]:
    """Problemas de `needs` de un workflow ya parseado (puro: se puede alimentar con un sabotaje)."""
    jobs = workflow.get("jobs") or {}
    problemas: list[str] = []
    for nombre, job in jobs.items():
        declarado = _needs_declarado(job)
        for dep in sorted(declarado - jobs.keys()):
            problemas.append(f"{nombre}: `needs` apunta a un job inexistente `{dep}`")
        for dep in sorted(_needs_usado(job) - declarado):
            problemas.append(
                f"{nombre}: usa `needs.{dep}` pero `{dep}` no está en su `needs` "
                f"(declarado: {sorted(declarado) or 'nada'}); el contexto no lo incluye "
                "y la expresión se evalúa vacía"
            )
    return problemas


def _workflows() -> list[tuple[Path, dict]]:
    return [(wf, yaml.safe_load(wf.read_text(encoding="utf-8"))) for wf in _archivos()]


def test_hay_jobs_con_needs_que_examinar():
    """El detector no puede aprobar midiendo el vacío."""
    con_needs = [
        nombre
        for _, wf in _workflows()
        for nombre, job in (wf.get("jobs") or {}).items()
        if _needs_declarado(job)
    ]
    assert len(con_needs) >= MINIMO_DE_JOBS_CON_NEEDS, (
        f"Solo {len(con_needs)} jobs con `needs` en {WORKFLOWS}: el detector no está leyendo."
    )


@pytest.mark.parametrize("wf,datos", _workflows(), ids=lambda x: x.name if isinstance(x, Path) else "")
def test_todo_needs_referenciado_esta_declarado(wf: Path, datos: dict):
    assert not incoherencias(datos), f"{wf.name}:\n  - " + "\n  - ".join(incoherencias(datos))


def test_deploy_publica_backend_antes_que_frontend():
    """Productor del contrato antes que el consumidor (regla de orden de deploy)."""
    jobs = yaml.safe_load((WORKFLOWS / "deploy.yml").read_text(encoding="utf-8"))["jobs"]
    assert "deploy-backend" in _needs_declarado(jobs["deploy-frontend"])
    assert "migrate" in _needs_declarado(jobs["deploy-backend"])


def test_sabotaje_el_detector_caza_el_bug_original_de_deploy():
    """Anclaje del propio guardián: el `deploy.yml` previo al arreglo DEBE dar rojo.

    Reconstruye en memoria el estado roto (`deploy-backend` con `needs: migrate` y un `if:`
    que lee `needs.guard`). Si el detector dejara de verlo, los tests de arriba pasarían
    en verde sin proteger nada.
    """
    datos = yaml.safe_load((WORKFLOWS / "deploy.yml").read_text(encoding="utf-8"))
    assert incoherencias(datos) == []  # estado real: coherente
    datos["jobs"]["deploy-backend"]["needs"] = "migrate"  # el bug original
    problemas = incoherencias(datos)
    assert any("deploy-backend" in p and "needs.guard" in p for p in problemas), problemas
