"""Guardián del verificador de anclas (SaMD §5.7 — la documentación es verificable).

`check_doc_links.sh` comprueba que el ARCHIVO destino exista pero descarta el
`#ancla`: un título renombrado deja el enlace "sano" para él y roto para quien lo pulsa.
`scripts/check_doc_anchors.py` cierra ese hueco. Este archivo ancla tres cosas:

1. La lógica: el slug es el de GitHub (acentos conservados, duplicados con sufijo) y un
   ancla rota se detecta. Se prueba con documentos sintéticos, porque el kit trae pocas
   anclas reales y un verde sobre pocas anclas no prueba que el detector vea.
2. Los documentos reales del kit no traen anclas rotas (0 rotas, y un mínimo de anclas
   miradas: un detector ciego también da "0 rotas").
3. El enchufe: el CI y el CI local tienen que LLAMAR al script. Escrito y sin llamar, no
   protege nada.
"""

import importlib.util
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_doc_anchors.py"

# Anclas reales que el verificador mira hoy en el kit. Si baja de acá, el detector
# dejó de ver enlaces (regex rota, ruta equivocada) aunque diga "0 rotas".
MINIMO_DE_ANCLAS = 5


@pytest.fixture
def anchors(monkeypatch):
    spec = importlib.util.spec_from_file_location("check_doc_anchors", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    return module


def _doc(tmp_path: Path, name: str, text: str) -> Path:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


# ---- 1. La lógica ---------------------------------------------------------------


def test_el_slug_conserva_acentos_como_github(anchors):
    assert anchors.github_slug("Refutación: ¿qué pasó?") == "refutación-qué-pasó"


def test_un_ancla_sin_acento_contra_un_titulo_con_acento_esta_rota(anchors, tmp_path):
    doc = _doc(tmp_path, "a.md", "# Refutación\n\nVer [aquí](#refutacion).\n")
    assert len(anchors.check_file(doc, tmp_path)) == 1


def test_un_ancla_bien_escrita_pasa(anchors, tmp_path):
    doc = _doc(tmp_path, "a.md", "# Refutación\n\nVer [aquí](#refutación).\n")
    assert anchors.check_file(doc, tmp_path) == []


def test_los_titulos_repetidos_se_desambiguan_con_sufijo(anchors):
    slugs = anchors.build_slug_index("# Notas\n\n# Notas\n\n# Notas\n")
    assert slugs == {"notas", "notas-1", "notas-2"}


def test_una_ancla_explicita_cuenta(anchors, tmp_path):
    doc = _doc(tmp_path, "a.md", '<a id="mi-ancla"></a>\n\nVer [x](#mi-ancla).\n')
    assert anchors.check_file(doc, tmp_path) == []


def test_ancla_a_otro_archivo_se_resuelve_contra_ese_archivo(anchors, tmp_path):
    _doc(tmp_path, "b.md", "# Destino real\n")
    ok = _doc(tmp_path, "ok.md", "[x](b.md#destino-real)\n")
    mal = _doc(tmp_path, "mal.md", "[x](b.md#destino-falso)\n")
    assert anchors.check_file(ok, tmp_path) == []
    assert len(anchors.check_file(mal, tmp_path)) == 1


def test_lo_que_esta_en_un_bloque_o_span_de_codigo_no_es_un_enlace(anchors, tmp_path):
    texto = "# T\n\n```\n[x](#no-existe)\n```\n\nTexto con `[y](#tampoco)` citado.\n"
    assert anchors.check_file(_doc(tmp_path, "a.md", texto), tmp_path) == []


def test_una_ruta_de_la_app_no_es_un_ancla(anchors, tmp_path):
    doc = _doc(tmp_path, "a.md", "# T\n\n[privacidad](#/privacy)\n")
    assert anchors.check_file(doc, tmp_path) == []


def test_un_titulo_dentro_de_un_bloque_de_codigo_no_genera_ancla(anchors, tmp_path):
    texto = "# T\n\n```\n# Falso titulo\n```\n\n[x](#falso-titulo)\n"
    assert len(anchors.check_file(_doc(tmp_path, "a.md", texto), tmp_path)) == 1


# ---- 2. Los documentos reales del kit -------------------------------------------


def test_los_documentos_del_kit_no_tienen_anclas_rotas(anchors):
    rotas = []
    for doc in anchors.default_files(ROOT):
        rotas.extend(anchors.check_file(doc, ROOT))
    assert rotas == [], "\n".join(rotas)


def test_el_detector_ve_las_anclas_reales_del_kit(anchors):
    total = sum(
        len(anchors.find_anchor_links(doc.read_text(encoding="utf-8")))
        for doc in anchors.default_files(ROOT)
    )
    assert total >= MINIMO_DE_ANCLAS, (
        f"el verificador solo ve {total} anclas (mínimo {MINIMO_DE_ANCLAS}): "
        "un detector ciego da '0 rotas' igual"
    )


# ---- 3. El enchufe --------------------------------------------------------------


@pytest.mark.parametrize(
    "ruta",
    [
        ".github/workflows/ci.yml",
        ".github/workflows/kit-quality.yml",
        "scripts/run_local_ci.sh",
    ],
)
def test_el_ci_llama_al_verificador_de_anclas(ruta):
    lineas = (ROOT / ruta).read_text(encoding="utf-8").splitlines()
    # Un `#` (inicio de línea o precedido de espacio) abre un comentario tanto en
    # YAML como en shell: `run: echo # python scripts/check_doc_anchors.py` NO llama
    # al script. Se descarta de cada línea todo lo que va desde ese `#`.
    sin_comentarios = [re.sub(r"(^|\s)#.*$", "", ln) for ln in lineas]
    activas = [ln for ln in sin_comentarios if "check_doc_anchors.py" in ln]
    assert activas, f"{ruta} no llama a scripts/check_doc_anchors.py"
