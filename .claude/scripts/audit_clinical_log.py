#!/usr/bin/env python3
"""Bitácora de cambios en módulos clínicos/críticos (IEC 62304 §5.7, §8).

Hook `PostToolUse` de Claude Code sobre `Edit|Write|MultiEdit|NotebookEdit`: si el
archivo tocado es clínico/crítico, añade una línea (fecha ISO UTC, herramienta, ruta,
patrón) a `.claude/audit_clinical_changes.log` y le devuelve al agente un recordatorio
de trazabilidad por `additionalContext` — el canal que el agente SÍ lee; un `print` a
stderr con salida 0 solo lo ve el humano en el modo detallado.

NO bloquea ni reescribe nada, y falla ABIERTO: un error de la bitácora no puede trabar
la edición. La bitácora es local (`*.log` está en `.gitignore`): es el diario de guardia
de la máquina, no un registro del DHF — lo que va al DHF lo escribe el cierre de bloque.

Portado del proyecto de referencia (sync 2026-11-16). Contrato en
`tests/test_audit_clinical_log.py`.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

# ⚠️ Lección del proyecto de referencia: su lista era CIEGA en 4 de 10 entradas (carpetas
# renombradas o que nunca existieron) y no registró nada de lo que más importaba. Un
# detector que no encuentra nada no está limpio: está ciego. Por eso cada patrón tiene
# que casar con un archivo REAL — lo exige el test. Al adaptar el kit, poné acá los
# módulos de clase B/C de `docs/07_regulatory_and_compliance/CRITICAL_MODULES_INVENTORY.md`
# (scoring, red de crisis, auth, auditoría, modelos y migraciones) y borrá los del esqueleto.
CLINICAL_PATTERNS = [
    r"app/core/encryption",  # cifrado de PHI en reposo
    r"app/core/security",  # JWT / identidad
    r"app/core/config\.py",  # secretos y guard de claves de dev
    r"app/main\.py",  # fail-safe global y log sin PHI
    r"app/routers/notes",  # endpoint que guarda contenido del usuario (PHI)
    r"app/schemas",  # frontera de validación de los datos de entrada
]

TOOLS = frozenset({"Edit", "Write", "MultiEdit", "NotebookEdit"})

RECORDATORIO = (
    "[SaMD bitácora] Cambio en módulo clínico/crítico{estado}: {ruta}.\n"
    "Antes de declarar cerrado: docs/08_verification_and_audits/TECHNICAL_DEBT_SUMMARY.md, "
    "docs/07_regulatory_and_compliance/ISO_14971_RISK_MATRIX.md (si toca seguridad) y "
    "docs/00_master/MASTER_MAP.md; y análisis de impacto (/samd-trace)."
)


def patron_clinico(ruta_relativa: str) -> str | None:
    for patron in CLINICAL_PATTERNS:
        if re.search(patron, ruta_relativa):
            return patron
    return None


def main() -> None:
    try:
        data = json.load(sys.stdin)
        herramienta = data.get("tool_name", "")
        ruta = (data.get("tool_input") or {}).get("file_path") or (data.get("tool_input") or {}).get("notebook_path", "")
    except Exception:
        return
    if herramienta not in TOOLS or not ruta:
        return

    cwd = os.getcwd()
    relativa = os.path.relpath(ruta, cwd) if os.path.isabs(ruta) else ruta
    patron = patron_clinico(relativa.replace(os.sep, "/"))
    if patron is None:
        return

    estado = " registrado"
    try:
        bitacora = os.path.join(cwd, ".claude", "audit_clinical_changes.log")
        os.makedirs(os.path.dirname(bitacora), exist_ok=True)
        with open(bitacora, "a", encoding="utf-8") as fh:
            fh.write(f"{datetime.now(timezone.utc).isoformat()}\t{herramienta}\t{relativa}\t{patron}\n")
    except OSError as exc:  # falla abierto: la edición sigue, pero sin fingir que quedó anotada
        estado = f" — LA BITÁCORA NO SE PUDO ESCRIBIR ({type(exc).__name__}), anotalo a mano"

    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": RECORDATORIO.format(ruta=relativa, estado=estado),
    }}, ensure_ascii=False))


if __name__ == "__main__":
    main()
