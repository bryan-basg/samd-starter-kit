"""Contrato de `.claude/scripts/audit_clinical_log.py` (bitácora de cambios clínicos).

Tres cosas que un verde de la pieza sola no demuestra: que cada patrón casa con un archivo
REAL (un detector que no encuentra nada está ciego), que el hook está ENCHUFADO en
`.claude/settings.json`, y que el recordatorio apunta a documentos que existen.
"""

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".claude" / "scripts" / "audit_clinical_log.py"


def _correr(entrada: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPT)], input=entrada, cwd=cwd,
                          capture_output=True, text=True, check=False, timeout=10)


def _patrones() -> list[str]:
    # Se carga el módulo: leer el texto hasta el primer `]` dejaba ciegos los patrones de atrás.
    spec = importlib.util.spec_from_file_location("audit_clinical_log", SCRIPT)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return list(modulo.CLINICAL_PATTERNS)


def _archivos_del_repo() -> list[str]:
    salida = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True)
    return salida.stdout.splitlines()


def test_hay_patrones() -> None:
    assert len(_patrones()) >= 1


@pytest.mark.parametrize("patron", _patrones())
def test_cada_patron_casa_con_un_archivo_real(patron: str) -> None:
    assert any(re.search(patron, f) for f in _archivos_del_repo()), (
        f"`{patron}` no casa con ningún archivo versionado: el detector está ciego ahí."
    )


def test_editar_un_modulo_clinico_deja_linea_y_recordatorio(tmp_path: Path) -> None:
    entrada = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": str(tmp_path / "app/core/encryption.py")}})
    r = _correr(entrada, tmp_path)
    assert r.returncode == 0
    linea = (tmp_path / ".claude" / "audit_clinical_changes.log").read_text(encoding="utf-8")
    assert linea.endswith("\tEdit\tapp/core/encryption.py\tapp/core/encryption\n")
    salida = json.loads(r.stdout)["hookSpecificOutput"]
    assert salida["hookEventName"] == "PostToolUse"
    assert "app/core/encryption.py" in salida["additionalContext"]


@pytest.mark.parametrize("entrada", [
    json.dumps({"tool_name": "Edit", "tool_input": {"file_path": "frontend/src/App.tsx"}}),
    json.dumps({"tool_name": "Read", "tool_input": {"file_path": "app/core/encryption.py"}}),
    json.dumps({"tool_name": "Edit", "tool_input": {}}),
    "esto no es json",
], ids=["no-clinico", "no-es-edicion", "sin-ruta", "entrada-rota"])
def test_lo_demas_no_deja_rastro_y_no_falla(tmp_path: Path, entrada: str) -> None:
    r = _correr(entrada, tmp_path)
    assert r.returncode == 0 and r.stdout == ""
    assert not (tmp_path / ".claude" / "audit_clinical_changes.log").exists()


def test_el_recordatorio_apunta_a_documentos_que_existen() -> None:
    texto = SCRIPT.read_text(encoding="utf-8")
    citados = set(re.findall(r"docs/[\w/.-]+\.md", texto))
    assert citados
    assert all((ROOT / d).is_file() for d in citados), [d for d in citados if not (ROOT / d).is_file()]


def test_el_hook_esta_enchufado_en_settings() -> None:
    settings = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    entradas = settings["hooks"]["PostToolUse"]
    enchufadas = [e for e in entradas
                  if any("audit_clinical_log.py" in h.get("command", "") for h in e["hooks"])]
    assert enchufadas, "el script existe pero ningún hook PostToolUse lo llama"
    assert {"Edit", "Write"} <= set(enchufadas[0]["matcher"].split("|"))


def test_la_bitacora_no_se_versiona() -> None:
    r = subprocess.run(["git", "check-ignore", "-q", ".claude/audit_clinical_changes.log"], cwd=ROOT, check=False)
    assert r.returncode == 0, "la bitácora es local: tiene que estar en .gitignore"


def test_si_la_bitacora_no_se_puede_escribir_avisa_igual(tmp_path: Path) -> None:
    """Callar es lo peor: la edición sigue, pero quien edita se entera de que no quedó anotada."""
    (tmp_path / ".claude").write_text("no es una carpeta")
    entrada = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": str(tmp_path / "app/core/encryption.py")}})
    r = _correr(entrada, tmp_path)
    assert r.returncode == 0
    aviso = json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]
    assert "NO SE PUDO ESCRIBIR" in aviso and " registrado" not in aviso
