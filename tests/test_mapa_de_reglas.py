"""Guardián del MAPA de reglas (SaMD §5.7 — el reglamento es verificable).

`CLAUDE.md` §MAPA DE ESTE CEREBRO es el índice de qué regla carga cuándo. Una regla
nueva en `.claude/rules/` que no figura ahí existe en disco pero nadie sabe que hay
que abrirla: es una regla invisible, el mismo "escrita pero sin enchufar" que el
resto del kit combate. `scripts/lint_agents.py` valida la ESTRUCTURA de cada archivo
de regla; esto valida que el mapa los nombre a todos.

También ancla que `docs.md` cargue de verdad al tocar `docs/`: sin `paths:` correcto
sería una regla que cree ser path-scoped y no lo es.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RULES = sorted((ROOT / ".claude" / "rules").glob("*.md"))
CLAUDE_MD = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")


def test_hay_reglas_que_mirar():
    # Un glob que no encuentra nada haría pasar la parametrización en vacío.
    # 5 path-scoped + 2 transversales; lo que solo usa la sesión principal vive en
    # el estilo `.claude/output-styles/orquestador.md` (ver
    # tests/test_estilo_orquestador_enchufado.py).
    assert len(RULES) >= 7, f"solo {len(RULES)} reglas en .claude/rules/"


def test_el_mapa_nombra_el_estilo_de_la_sesion_principal():
    assert ".claude/output-styles/orquestador.md" in CLAUDE_MD


@pytest.mark.parametrize("regla", RULES, ids=lambda p: p.name)
def test_cada_regla_figura_en_el_mapa_de_claude_md(regla):
    assert f".claude/rules/{regla.name}" in CLAUDE_MD, (
        f"{regla.name} existe pero CLAUDE.md §MAPA DE ESTE CEREBRO no la nombra"
    )


def test_docs_md_carga_al_tocar_la_documentacion():
    texto = (ROOT / ".claude" / "rules" / "docs.md").read_text(encoding="utf-8")
    cabecera = texto.split("---")[1]
    assert "paths:" in cabecera
    assert '"docs/**/*.md"' in cabecera
