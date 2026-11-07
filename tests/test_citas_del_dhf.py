"""Guardián de las citas al código del DHF (SaMD §5.1 / §5.7 — trazabilidad verificable).

La regla del DHF es que cada REQ apunte a código y a un test que existen HOY. Con
`archivo:línea` esa promesa caduca en el siguiente commit que mueva una línea; la forma
canónica `ruta/archivo.py::símbolo` la hace comprobable. `scripts/check_doc_citations.py`
la comprueba. Este archivo ancla tres cosas:

1. La lógica, con un repo sintético: una cita buena pasa y una rota (símbolo renombrado,
   archivo borrado) se detecta. Un verde sobre las pocas citas reales del kit no
   prueba que el detector vea.
2. Los documentos reales del kit no traen citas rotas, y el verificador VE un mínimo
   de citas reales: un detector ciego también da "0 rotas".
3. El enchufe: el CI y el CI local tienen que LLAMAR al script.
"""

import importlib.util
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_doc_citations.py"

# Citas por nombre reales que el verificador comprueba hoy en el kit (las filas de
# ejemplo de la matriz de trazabilidad). Si baja de acá, el detector dejó de ver
# citas aunque diga "0 rotas".
MINIMO_DE_CITAS = 4

CODIGO = '''\
"""Módulo de ejemplo."""

LIMITE = 3
ETIQUETA: str = "x"


def cifrar(valor):
    return valor


async def sincronizar():
    return 1


class Servicio:
    def evaluar(self):
        return 2


if LIMITE:
    def condicional():
        return 3
'''


@pytest.fixture
def citas(monkeypatch):
    spec = importlib.util.spec_from_file_location("check_doc_citations", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "app").mkdir()
    (tmp_path / "app" / "mod.py").write_text(CODIGO, encoding="utf-8")
    (tmp_path / "app" / "ui.ts").write_text(
        "export function calcularRiesgo(x) { return x }\n", encoding="utf-8"
    )
    return tmp_path


def _revisar(citas, repo: Path, texto: str):
    doc = repo / "doc.md"
    doc.write_text(texto, encoding="utf-8")
    return citas.check_file(doc, repo)


# ---- 1. La lógica ---------------------------------------------------------------


@pytest.mark.parametrize(
    "cita",
    [
        "app/mod.py::cifrar",
        "app/mod.py::sincronizar",
        "app/mod.py::Servicio",
        "app/mod.py::Servicio::evaluar",
        "app/mod.py::Servicio.evaluar",
        "app/mod.py::LIMITE",
        "app/mod.py::ETIQUETA",
        "app/mod.py::condicional",
        "app/mod.py::cifrar[caso-1]",
        "app/mod.py:7::cifrar",  # forma vieja con línea + nombre: se tolera
        "app/ui.ts::calcularRiesgo",
    ],
)
def test_una_cita_buena_pasa(citas, repo, cita):
    informe = _revisar(citas, repo, f"Ver `{cita}` para el detalle.\n")
    assert informe.broken == []
    assert informe.verified == 1


def test_un_simbolo_renombrado_es_una_cita_rota(citas, repo):
    informe = _revisar(citas, repo, "Ver `app/mod.py::descifrar`.\n")
    assert len(informe.broken) == 1
    assert "no define" in informe.broken[0]


def test_un_archivo_borrado_es_una_cita_rota(citas, repo):
    informe = _revisar(citas, repo, "Ver `app/otro.py::cifrar`.\n")
    assert len(informe.broken) == 1
    assert "no existe" in informe.broken[0]


def test_un_metodo_sin_su_clase_no_cuenta(citas, repo):
    # `evaluar` es un método de Servicio, no una función del módulo.
    informe = _revisar(citas, repo, "Ver `app/mod.py::evaluar`.\n")
    assert len(informe.broken) == 1


def test_el_reporte_dice_en_que_linea_del_documento_esta(citas, repo):
    informe = _revisar(citas, repo, "uno\ndos\nVer `app/mod.py::nada`.\n")
    assert "doc.md:3" in informe.broken[0]


def test_en_ts_el_nombre_tiene_que_ser_palabra_completa(citas, repo):
    mal = _revisar(citas, repo, "Ver `app/ui.ts::calcular`.\n")
    assert len(mal.broken) == 1


def test_lo_que_esta_en_un_bloque_de_codigo_no_es_una_cita(citas, repo):
    texto = "```\napp/mod.py::no_existe\n```\n"
    informe = _revisar(citas, repo, texto)
    assert informe.broken == [] and informe.verified == 0


@pytest.mark.parametrize(
    "plantilla",
    [
        "`ruta/archivo.py::símbolo`",
        "`archivo.py::símbolo`",
        "`<app/modulo>.py::nombre`",
        "`{{BACKEND_DIR}}/servicio.py::nombre`",
        "`app/<servicio>/mod.py::nombre`",
    ],
)
def test_las_plantillas_y_marcadores_no_son_citas(citas, repo, plantilla):
    informe = _revisar(citas, repo, f"Formato: {plantilla}.\n")
    assert informe.broken == [] and informe.verified == 0


def test_un_punto_al_final_de_la_frase_no_es_parte_del_simbolo(citas, repo):
    informe = _revisar(citas, repo, "Está en app/mod.py::cifrar.\n")
    assert informe.broken == [] and informe.verified == 1


def test_las_citas_viejas_por_numero_se_cuentan_pero_no_se_verifican(citas, repo):
    informe = _revisar(citas, repo, "Antes: `app/no_existe.py:42`.\n")
    assert informe.broken == []
    assert informe.legacy == 1


def test_el_marcador_NN_de_las_plantillas_no_cuenta_como_cita_vieja(citas, repo):
    informe = _revisar(citas, repo, "Plantilla: `app/dependencies.py:NN`.\n")
    assert informe.legacy == 0


# ---- 2. Los documentos reales del kit -------------------------------------------


def test_los_documentos_del_kit_no_tienen_citas_rotas(citas):
    rotas = []
    for doc in citas.default_files(ROOT):
        rotas.extend(citas.check_file(doc, ROOT).broken)
    assert rotas == [], "\n".join(rotas)


def test_el_detector_ve_las_citas_reales_del_kit(citas):
    total = sum(citas.check_file(doc, ROOT).verified for doc in citas.default_files(ROOT))
    assert total >= MINIMO_DE_CITAS, (
        f"el verificador solo comprueba {total} citas (mínimo {MINIMO_DE_CITAS}): "
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
def test_el_ci_llama_al_verificador_de_citas(ruta):
    lineas = (ROOT / ruta).read_text(encoding="utf-8").splitlines()
    # Un `#` (inicio de línea o precedido de espacio) abre un comentario tanto en
    # YAML como en shell: `run: echo # python scripts/check_doc_citations.py` NO
    # llama al script. Se descarta de cada línea todo lo que va desde ese `#`.
    sin_comentarios = [re.sub(r"(^|\s)#.*$", "", ln) for ln in lineas]
    activas = [ln for ln in sin_comentarios if "check_doc_citations.py" in ln]
    assert activas, f"{ruta} no llama a scripts/check_doc_citations.py"
