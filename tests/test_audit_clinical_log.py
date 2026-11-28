"""Contrato del vigía `.claude/scripts/audit_clinical_log.py`: ve el cambio venga de la herramienta que venga.

En el proyecto de referencia el vigía solo escuchaba Edit/Write y estuvo mudo varios días
cuando el trabajo pasó a la terminal (SCMP v1.20). Estas pruebas corren el script REAL
sobre un repositorio de juguete, y además anclan lo que un verde de la pieza sola no
demuestra: que cada patrón casa con un archivo real, que el hook está ENCHUFADO también a
la terminal y que el recordatorio apunta a documentos que existen.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest

_RAIZ = Path(__file__).resolve().parent.parent
_SCRIPT = _RAIZ / ".claude/scripts/audit_clinical_log.py"
_spec = importlib.util.spec_from_file_location("audit_clinical_log", _SCRIPT)
assert _spec is not None and _spec.loader is not None
_vigia = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_vigia)

_CLINICO = "app/core/encryption.py"
_OTRO = "app/schemas/notas.py"


def _git(raiz: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(raiz), "-c", "user.email=a@b.c", "-c", "user.name=x", *args],
                   check=True, capture_output=True)


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    for rel in (".claude/rules/backend.md", ".claude/rules/github-actions.md"):
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(_RAIZ / rel, tmp_path / rel)
    (tmp_path / _CLINICO).parent.mkdir(parents=True)
    (tmp_path / _CLINICO).write_text("A = 1\n")
    (tmp_path / _OTRO).parent.mkdir(parents=True)
    (tmp_path / _OTRO).write_text("B = 1\n")
    (tmp_path / ".gitignore").write_text("*.log\n.claude/worktrees/\n")
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "base")
    return tmp_path


def _correr_crudo(repo: Path, entrada: str, proyecto: Path | None = None) -> str:
    res = subprocess.run([sys.executable, str(_SCRIPT)], input=entrada, text=True,
                         capture_output=True, timeout=20,
                         env={**os.environ, "CLAUDE_PROJECT_DIR": str(proyecto or repo)})
    assert res.returncode == 0, res.stderr
    if not res.stdout:
        return ""
    salida = json.loads(res.stdout)["hookSpecificOutput"]
    assert salida["hookEventName"] == "PostToolUse"
    contexto: str = salida["additionalContext"]
    return contexto


def _correr(repo: Path, herramienta: str = "Bash", sesion: str = "s1",
            proyecto: Path | None = None, **extra: Any) -> str:
    entrada = {"tool_name": herramienta, "session_id": sesion, "cwd": str(repo),
               "tool_input": {"command": "x"}, "duration_ms": 5, **extra}
    return _correr_crudo(repo, json.dumps(entrada), proyecto)


def _registro(repo: Path) -> list[str]:
    log = repo / ".claude/audit_clinical_changes.log"
    return log.read_text().splitlines() if log.exists() else []


# ── Conducta: lo que cambia en el disco, venga de donde venga ──────────────────────────

def test_un_cambio_hecho_por_terminal_queda_registrado(repo: Path) -> None:
    (repo / _CLINICO).write_text("A = 2\n")
    contexto = _correr(repo)
    (linea,) = _registro(repo)
    assert linea.split("\t")[1:] == ["Bash", _CLINICO, r"app/core/encryption"]
    assert "[SaMD vigía]" in contexto and " registrado" in contexto


def test_un_cambio_hecho_con_edit_tambien(repo: Path) -> None:
    (repo / _CLINICO).write_text("A = 2\n")
    _correr(repo, herramienta="Edit", tool_input={"file_path": str(repo / _CLINICO)})
    (linea,) = _registro(repo)
    assert linea.split("\t")[1:3] == ["Edit", _CLINICO]


def test_mover_un_archivo_viejo_encima_tambien_cuenta(repo: Path) -> None:
    """`mv` conserva la fecha de contenido: con mtime este cambio era invisible."""
    _correr(repo)
    nuevo = repo.parent / f"{repo.name}-nuevo.py"
    nuevo.write_text("A = 3\n")
    os.utime(nuevo, (1, 1))
    os.replace(nuevo, repo / _CLINICO)
    _correr(repo)
    assert len(_registro(repo)) == 1


def test_borrar_un_archivo_clinico_queda_registrado(repo: Path) -> None:
    (repo / _CLINICO).unlink()
    _correr(repo)
    assert len(_registro(repo)) == 1


def test_borrar_la_carpeta_entera_queda_registrado_una_vez(repo: Path) -> None:
    """Sin carpeta padre no hay fecha que mirar: el borrado cuenta como «ahora» la primera vez."""
    shutil.rmtree(repo / "app/core")
    assert "app/core/encryption.py" in _correr(repo)
    _correr(repo)
    assert len(_registro(repo)) == 1


def test_un_borrado_no_se_vuelve_a_registrar_cuando_cambia_otro_archivo_de_su_carpeta(repo: Path) -> None:
    (repo / _CLINICO).unlink()
    _correr(repo)
    (repo / "app/core/otro.py").write_text("x = 1\n")
    _correr(repo)
    assert len(_registro(repo)) == 1


def test_el_mismo_cambio_no_se_registra_dos_veces(repo: Path) -> None:
    (repo / _CLINICO).write_text("A = 2\n")
    _correr(repo)
    _correr(repo)
    _correr(repo, sesion="otra")
    assert len(_registro(repo)) == 1


def test_lo_que_no_es_clinico_no_deja_rastro(repo: Path) -> None:
    (repo / "README.md").write_text("hola")
    assert _correr(repo) == ""
    assert _registro(repo) == []


@pytest.mark.parametrize("entrada", ["esto no es json", "{}"], ids=["entrada-rota", "entrada-vacia"])
def test_una_entrada_rara_no_frena_nunca(repo: Path, entrada: str) -> None:
    _correr_crudo(repo, entrada)  # returncode 0 lo exige _correr_crudo


def test_una_copia_de_trabajo_se_ve_y_se_registra_en_el_principal(repo: Path) -> None:
    copia = repo / ".claude/worktrees/w1"
    _git(repo, "worktree", "add", "-q", str(copia))
    (copia / _CLINICO).write_text("A = 9\n")
    _correr(repo, tool_input={"command": f"cd '{copia}' && sed -i x y"})
    (linea,) = _registro(repo)
    assert linea.split("\t")[2] == f".claude/worktrees/w1/{_CLINICO}"


def test_un_edit_en_una_copia_de_trabajo_fuera_del_repo_se_ve(repo: Path) -> None:
    copia = repo.parent / f"{repo.name}-wt"
    _git(repo, "worktree", "add", "-q", str(copia))
    (copia / _CLINICO).write_text("A = 9\n")
    _correr(repo, herramienta="Edit", tool_input={"file_path": str(copia / _CLINICO)})
    (linea,) = _registro(repo)
    assert linea.split("\t")[2].endswith(f"-wt/{_CLINICO}")


def test_una_sesion_abierta_en_la_copia_escribe_en_el_mismo_registro(repo: Path) -> None:
    copia = repo / ".claude/worktrees/w2"
    _git(repo, "worktree", "add", "-q", str(copia))
    (copia / _CLINICO).write_text("A = 9\n")
    _correr(copia, proyecto=copia)
    assert len(_registro(repo)) == 1 and _registro(copia) == []


# ── La regla de la capa tocada por terminal ────────────────────────────────────────────

def test_el_recordatorio_nombra_el_archivo_y_vuelve_con_cada_archivo_clinico_nuevo(repo: Path) -> None:
    (repo / _CLINICO).write_text("A = 2\n")
    assert _CLINICO in _correr(repo, herramienta="Edit")
    (repo / _CLINICO).write_text("A = 3\n")
    assert "[SaMD vigía]" not in _correr(repo, herramienta="Edit")  # mismo archivo: ya avisado
    (repo / _OTRO).write_text("B = 2\n")
    aviso = _correr(repo, herramienta="Edit")
    assert _OTRO in aviso and _CLINICO not in aviso


def test_la_regla_de_la_capa_llega_una_vez_por_agente(repo: Path) -> None:
    (repo / _CLINICO).write_text("A = 2\n")
    primera = _correr(repo)
    assert "# ESTÁNDARES DEL BACKEND" in primera and "[SaMD vigía]" in primera
    (repo / _CLINICO).write_text("A = 3\n")
    assert _correr(repo) == ""
    (repo / _CLINICO).write_text("A = 4\n")
    assert "# ESTÁNDARES DEL BACKEND" in _correr(repo, agent_id="a7")


def test_lo_que_otro_toco_antes_de_mi_comando_se_registra_pero_no_me_da_la_regla(repo: Path) -> None:
    (repo / _CLINICO).write_text("A = 2\n")
    time.sleep(2.2)
    assert _correr(repo) == ""
    assert len(_registro(repo)) == 1


def test_con_edit_no_se_repite_la_regla_que_ya_cargo_claude_code(repo: Path) -> None:
    (repo / _CLINICO).write_text("A = 2\n")
    contexto = _correr(repo, herramienta="Edit")
    assert "ESTÁNDARES" not in contexto and len(_registro(repo)) == 1


def test_una_regla_que_no_entra_en_el_tope_se_manda_a_leer(repo: Path) -> None:
    flujo = repo / ".github/workflows/x.yml"
    flujo.parent.mkdir(parents=True)
    flujo.write_text("on: push")
    contexto = _correr(repo)
    assert len(contexto) < 10_000
    entregada = "Regla de la capa que tocaste por terminal (.claude/rules/github-actions.md)" in contexto
    assert entregada or "leé AHORA .claude/rules/github-actions.md" in contexto


# ── No calla: si falla, lo dice ────────────────────────────────────────────────────────

def test_si_la_bitacora_no_se_puede_escribir_avisa_igual(repo: Path) -> None:
    """La edición sigue, pero quien edita se entera de que no quedó anotada."""
    (repo / ".claude/audit_clinical_changes.log").mkdir(parents=True)  # una carpeta: no se puede abrir
    (repo / _CLINICO).write_text("A = 2\n")
    aviso = _correr(repo)
    assert "NO SE PUDO ESCRIBIR" in aviso and " registrado" not in aviso


def test_si_la_bitacora_fallo_el_cambio_se_registra_cuando_vuelve(repo: Path) -> None:
    """La marca no avanza sobre lo que no se pudo escribir: repetir antes que perder."""
    bloqueo = repo / ".claude/audit_clinical_changes.log"
    bloqueo.mkdir(parents=True)
    (repo / _CLINICO).write_text("A = 2\n")
    _correr(repo)
    bloqueo.rmdir()
    _correr(repo)
    assert len(_registro(repo)) == 1


def test_un_fallo_antes_de_registrar_dice_que_no_quedo_registrado(repo: Path) -> None:
    (repo / ".git/samd-vigia").write_text("no es una carpeta")
    (repo / _CLINICO).write_text("A = 2\n")
    aviso = _correr(repo)
    assert "falló" in aviso and "NO quedó registrado" in aviso
    assert [x.split("\t")[1] for x in _registro(repo)] == ["ERROR"]


def test_un_fallo_despues_de_registrar_no_miente_sobre_la_bitacora(repo: Path) -> None:
    (repo / ".claude/rules/backend.md").write_bytes(b"\xff\xfe no es utf-8")
    (repo / _CLINICO).write_text("A = 2\n")
    aviso = _correr(repo)
    assert "falló" in aviso and "SÍ quedó en la bitácora" in aviso and "NO quedó" not in aviso
    assert [x.split("\t")[1] for x in _registro(repo)] == ["Bash", "ERROR"]


def test_fuera_de_un_repositorio_git_no_frena(tmp_path: Path) -> None:
    assert _correr(tmp_path) == ""


# ── Anclas: patrones reales, hook enchufado, documentos que existen ────────────────────

def test_cada_patron_escrito_a_mano_casa_con_un_archivo_real() -> None:
    reales = subprocess.run(["git", "ls-files"], cwd=_RAIZ, capture_output=True, text=True,
                            check=True).stdout.splitlines()
    assert _vigia.CLINICAL_PATTERNS
    ciegos = [p for p in _vigia.CLINICAL_PATTERNS if not any(re.search(p, r) for r in reales)]
    assert ciegos == [], f"{ciegos} no casan con ningún archivo versionado: el detector está ciego ahí."


def test_toda_regla_con_paths_se_puede_entregar() -> None:
    con_paths = {f.name for f in (_RAIZ / ".claude/rules").glob("*.md")
                 if f.read_text("utf-8").startswith("---\npaths:")}
    reglas = _vigia.reglas_por_capa(_RAIZ)
    assert con_paths and set(reglas) == con_paths and all(regexes for regexes, _ in reglas.values())


def test_el_vigia_esta_enchufado_tambien_a_la_terminal() -> None:
    ajustes = json.loads((_RAIZ / ".claude/settings.json").read_text("utf-8"))
    grupos = [g for g in ajustes["hooks"]["PostToolUse"]
              if any("audit_clinical_log.py" in h["command"] for h in g["hooks"])]
    assert grupos, "el script existe pero ningún hook PostToolUse lo llama"
    herramientas = {h for g in grupos for h in g["matcher"].split("|")}
    assert {"Bash", "Edit", "Write"} <= herramientas


def test_el_recordatorio_apunta_a_documentos_que_existen() -> None:
    citados = set(re.findall(r"docs/[\w/.-]+\.md", _SCRIPT.read_text(encoding="utf-8")))
    assert citados
    assert [d for d in citados if not (_RAIZ / d).is_file()] == []


def test_la_bitacora_no_se_versiona() -> None:
    r = subprocess.run(["git", "check-ignore", "-q", ".claude/audit_clinical_changes.log"], cwd=_RAIZ, check=False)
    assert r.returncode == 0, "la bitácora es local: tiene que estar en .gitignore"
