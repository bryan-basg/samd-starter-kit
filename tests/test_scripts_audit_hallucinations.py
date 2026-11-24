"""scripts/audit_hallucinations.py — el auditor pasa limpio sobre el kit SIN haberse apagado.

SaMD §5.7: un gate en verde solo vale si sigue cazando lo real. Estos tests anclan las dos
mitades: (1) el árbol versionado da rc=0 (el hook de pre-commit no está roto de fábrica) y
(2) el sabotaje —una alucinación real— sigue dando rc=1; la allowlist es estrecha, no un comodín.
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "audit_hallucinations.py"


@pytest.fixture(scope="module")
def auditor():
    spec = importlib.util.spec_from_file_location("audit_hallucinations", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Los literales se arman por partes: este archivo vive en el árbol que el propio auditor escanea.
FAKE_KEY = "your" + "-api-key"
DEMO_SECRET = "".join(["admin", "123"])
INC_ID = "<INC-" + "X" * 4 + ">"
LOCAL_DOCS = "http://local" + "host:8000/docs"
LOCAL_OTHER = "http://local" + "host:9999/api"


def _run(path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True, timeout=120
    )


def _write(root: Path, rel: str, text: str) -> None:
    f = root / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text, encoding="utf-8")


def test_kit_limpio_da_rc0():
    res = _run(ROOT)
    assert res.returncode == 0, res.stdout[-1500:]
    assert "Sin placeholders" in res.stdout


def test_sabotaje_alucinacion_real_da_rc1(tmp_path):
    _write(tmp_path, "app/config.py", f'API_KEY = "{FAKE_KEY}"\n')
    res = _run(tmp_path)
    assert res.returncode == 1
    assert "app/config.py:1" in res.stdout
    assert "placeholder de API key" in res.stdout


def test_credencial_demo_critica_da_rc1(tmp_path):
    _write(tmp_path, "docs/x.md", f"password = {DEMO_SECRET}\n")
    assert _run(tmp_path).returncode == 1


def test_salidas_gitignoradas_de_la_raiz_no_se_escanean(tmp_path):
    for rel in ("site/a/index.html", "reports/r.txt", "audit/g.json", "frontend/reports/x.md"):
        _write(tmp_path, rel, f"{INC_ID} {FAKE_KEY}\n")
    # Un archivo limpio que SÍ se escanea: sin él el árbol tendría 0 archivos y el gate
    # fail-closed fallaría por otra razón, enmascarando lo que este test mide.
    _write(tmp_path, "app/ok.py", "X = 1\n")
    res = _run(tmp_path)
    assert res.returncode == 0, res.stdout
    assert "(1 archivos revisados)" in res.stdout


# --- #96: las exclusiones no deben mirar los directorios POR ENCIMA de la raíz escaneada ---
@pytest.mark.parametrize("ancestro", ["build", "dist", "examples", "node_modules", ".venv"])
def test_raiz_bajo_directorio_excluido_se_escanea(tmp_path, ancestro):
    root = tmp_path / ancestro / "repo"
    _write(root, "app/config.py", f'API_KEY = "{FAKE_KEY}"\n')
    res = _run(root)
    assert res.returncode == 1, res.stdout + res.stderr
    assert "app/config.py:1" in res.stdout


def test_exclusion_por_nombre_sigue_valiendo_dentro_de_la_raiz(tmp_path):
    # La contracara: dentro del repo, `build/` y `node_modules/` siguen sin escanearse.
    _write(tmp_path, "build/x.py", f'API_KEY = "{FAKE_KEY}"\n')
    _write(tmp_path, "frontend/node_modules/p/i.js", f'k = "{FAKE_KEY}"\n')
    _write(tmp_path, "app/ok.py", "X = 1\n")
    res = _run(tmp_path)
    assert res.returncode == 0, res.stdout
    assert "(1 archivos revisados)" in res.stdout


# --- #96 (fail-closed): un gate que no revisó ningún archivo no puede declarar limpio ---
def test_cero_archivos_escaneados_da_rc1(tmp_path):
    _write(tmp_path, "build/x.py", "X = 1\n")  # todo excluido
    _write(tmp_path, "imagen.png", "binario\n")  # sufijo fuera de INCLUDE_SUFFIXES
    res = _run(tmp_path)
    assert res.returncode == 1
    assert "0 archivos escaneados" in res.stderr
    assert "Sin placeholders" not in res.stdout


@pytest.mark.parametrize("rel", ["app/site/x.py", "app/audit/x.py", "app/reports/x.py"])
def test_paquetes_versionados_homonimos_si_se_escanean(tmp_path, rel):
    _write(tmp_path, rel, f"TOKEN = '{FAKE_KEY}'\n")
    assert _run(tmp_path).returncode == 1


def test_allowlist_tolera_solo_la_linea_exacta(tmp_path):
    # La línea de plantilla autorizada pasa...
    _write(tmp_path, "docs/06_operations_and_runbooks/INCIDENT_POSTMORTEM_TEMPLATE.md",
           f"| ID de incidente | {INC_ID} |\n")
    assert _run(tmp_path).returncode == 0
    # ...pero un localhost nuevo en el MISMO archivo de código autorizado, no.
    _write(tmp_path, "app/main.py",
           f"Docs:       {LOCAL_DOCS}\nURL = '{LOCAL_OTHER}'\n")
    res = _run(tmp_path)
    assert res.returncode == 1
    assert "app/main.py:2" in res.stdout
    assert "app/main.py:1" not in res.stdout


def test_allowlist_no_es_comodin_por_etiqueta_ni_por_archivo(tmp_path):
    # Mismo fragmento autorizado en OTRO archivo: falla.
    _write(tmp_path, "otro.md", f"arranque: {LOCAL_DOCS}\n")
    assert _run(tmp_path).returncode == 1


def test_cada_entrada_de_la_allowlist_apunta_a_un_archivo_vivo(auditor):
    # Una entrada huérfana (archivo renombrado/borrado) es una excepción muerta: se poda.
    for rel, _label, frag, motivo in auditor.ALLOWLIST:
        f = ROOT / rel
        assert f.is_file(), f"allowlist huérfana: {rel}"
        assert frag in f.read_text(encoding="utf-8"), f"fragmento ausente en {rel}: {frag}"
        assert motivo.strip()


@pytest.mark.parametrize(
    "archivo",
    ["Dockerfile", "Dockerfile.prod", "Makefile", ".env", ".env.example", "app/x.conf", "db/x.sql", "infra/x.tfvars"],
)
def test_mira_archivos_sin_sufijo_de_codigo(tmp_path, archivo):
    """Antes eran invisibles: un Dockerfile con una credencial demo daba «limpio»."""
    _write(tmp_path, archivo, f"DB_PASSWORD={DEMO_SECRET}\n")
    res = _run(tmp_path)
    assert res.returncode == 1 and archivo in res.stdout, res.stdout


@pytest.mark.parametrize(
    "texto",
    ["CHANGE" + "ME", "REPLACE" + "_ME", "all" + "Users", "roles/" + "owner", "change" + "it",
     "password" + "123", "TODO" + " SECURITY", "raise NotImplemented" + "Error", LOCAL_OTHER],
)
def test_cada_patron_caza_lo_suyo(tmp_path, texto):
    _write(tmp_path, "app/x.py", f"# {texto}\n")
    assert _run(tmp_path).returncode == 1, texto
