"""Guardián: el CI del backend se dispara con TODO lo que leen sus tests (IEC 62304 §5.7).

Varios tests de `tests/` no prueban código: abren `CLAUDE.md`, `.claude/**` o `docs/**` y
comprueban que el reglamento y el DHF digan lo correcto. Si el filtro `backend` de
`.github/workflows/ci.yml` no incluye esas rutas, un PR que edita SOLO un `.md` no dispara el
job y esos guardianes NO CORREN: no aparece un rojo, aparece un verde de un CI que no miró.

El conjunto se DERIVA del disco: un test nuevo que lea `docs/` entra solo por existir, y el
filtro tiene que cubrirlo (portado del proyecto de referencia, donde el agujero se midió).
"""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / ".github" / "workflows" / "ci.yml"

# Qué texto en un test delata que lee una zona → qué glob tiene que estar en el filtro.
ZONAS = {
    "CLAUDE.md": "CLAUDE.md",
    '".claude"': ".claude/**",
    ".claude/": ".claude/**",
    '"docs"': "docs/**",
    "docs/": "docs/**",
    # Dockerfile: `test_workflows_pineados_a_sha` hace `ROOT.glob("Dockerfile*")`.
    "Dockerfile*": "Dockerfile*",
    # scripts/*.sh: los tests copian y EJECUTAN los gates (`_sh`, `check_coverage.sh`...).
    ".sh": "scripts/**/*.sh",
    # `test_hard_rules` comprueba el formato de la plantilla de entorno.
    ".env.example": ".env.example",
    # `test_versiones_coherentes` y el test del piso de cobertura.
    "docker-compose.yml": "docker-compose.yml",
    ".devcontainer": ".devcontainer/**",
    "package.json": "frontend/package.json",
    ".coveragerc": ".coveragerc",
}

# Piso del detector: si el grep deja de encontrar lectores, el test no aprueba por vacío.
MINIMO_DE_TESTS_LECTORES = 3


def _filtro_backend() -> list[str]:
    flujo = yaml.safe_load(CI.read_text(encoding="utf-8"))
    for paso in flujo["jobs"]["changes"]["steps"]:
        filtros = (paso.get("with") or {}).get("filters")
        if filtros:
            return list(yaml.safe_load(filtros)["backend"])
    raise AssertionError("ci.yml no tiene el paso de paths-filter del job `changes`")


def _globs_exigidos() -> dict[str, list[str]]:
    exigidos: dict[str, list[str]] = {}
    for test in sorted((ROOT / "tests").glob("*.py")):
        if test.name == Path(__file__).name:
            continue
        texto = test.read_text(encoding="utf-8")
        for marca, glob in ZONAS.items():
            if marca in texto:
                exigidos.setdefault(glob, [])
                if test.name not in exigidos[glob]:
                    exigidos[glob].append(test.name)
    return exigidos


def test_el_detector_encuentra_lectores() -> None:
    lectores = {t for tests in _globs_exigidos().values() for t in tests}
    assert len(lectores) >= MINIMO_DE_TESTS_LECTORES, lectores


def test_el_filtro_backend_cubre_todo_lo_que_leen_los_tests() -> None:
    filtro = set(_filtro_backend())
    faltan = {g: t for g, t in _globs_exigidos().items() if g not in filtro}
    assert not faltan, (
        "Estos tests leen rutas que NO disparan el job backend de ci.yml "
        f"(un PR que solo las toque no los corre): {faltan}"
    )
