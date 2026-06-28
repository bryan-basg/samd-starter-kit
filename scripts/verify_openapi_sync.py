#!/usr/bin/env python3
"""Candado de drift del contrato OpenAPI — {{PROJECT_NAME}} (SaMD {{SAMD_CLASS}}).

IEC 62304 §5.1/§5.7 — el contrato publicado debe reflejar la API real. Compara
el `openapi.json` VERSIONADO en el repo contra el que genera el código en
runtime (`app.openapi()`). Si difieren, el contrato dejó de reflejar la API →
exit 1 para abortar el PR.

IMPORTANTE — este script es READ-ONLY sobre el repo. NUNCA sobreescribe el
`openapi.json`. La regeneración es responsabilidad EXPLÍCITA del autor del PR
vía `scripts/export_openapi.py` (script complementario que SÍ escribe). Si este
verificador pisara el archivo antes de comparar, el drift sería indetectable.

Determinismo — ambos lados se serializan con
`json.dumps(..., indent=2, sort_keys=True, ensure_ascii=False)`. `sort_keys`
neutraliza diferencias de ORDEN de claves (ruido entre versiones de libs) →
solo falla por drift semántico real.

Config por env (con defaults sensatos):
    OPENAPI_PATH  → contrato versionado.  Default: frontend/src/api/openapi.json
    APP_IMPORT    → ruta de import de la app ASGI.  Default: app.main:app

Uso:
    # activar el venv del backend primero
    python scripts/verify_openapi_sync.py

Exit codes:
    0 → en sync.
    1 → drift detectado o error de entorno (falla cerrada, apta para CI).
"""

from __future__ import annotations

import difflib
import importlib
import json
import os
import sys
from pathlib import Path

# El backend vive en la raíz del repo (no en una carpeta `backend/`).
sys.path.insert(0, os.getcwd())

OPENAPI_PATH = Path(os.environ.get("OPENAPI_PATH", "frontend/src/api/openapi.json"))
APP_IMPORT = os.environ.get("APP_IMPORT", "app.main:app")
REGEN_CMD = "python scripts/export_openapi.py"


def _canonical(schema: object) -> str:
    """Serialización canónica determinista (orden de claves estable)."""
    return json.dumps(schema, indent=2, sort_keys=True, ensure_ascii=False)


def _load_app_schema() -> object | None:
    """Importa la app ASGI y devuelve su esquema OpenAPI en runtime."""
    module_path, _, attr = APP_IMPORT.partition(":")
    if not module_path or not attr:
        print(f"❌ APP_IMPORT mal formado: '{APP_IMPORT}' (esperado 'modulo:atributo').")
        return None
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        print(f"❌ No se pudo importar '{module_path}': {exc}")
        print("   Pistas:")
        print("   - ¿Activaste el venv del backend?")
        print(f"   - ¿La app vive en otro módulo? Ajustá APP_IMPORT (ej. "
              f"APP_IMPORT=src.server.main:app).")
        return None
    app = getattr(module, attr, None)
    if app is None:
        print(f"❌ El módulo '{module_path}' no expone '{attr}'.")
        return None
    openapi = getattr(app, "openapi", None)
    if not callable(openapi):
        print(f"❌ '{APP_IMPORT}' no parece una app con método .openapi() (FastAPI).")
        return None
    return openapi()


def verify_sync() -> int:
    print("🔍 Verificando sincronización del contrato OpenAPI (repo vs runtime)...")

    # 1. Cargar el contrato VERSIONADO en el repo (sin tocarlo).
    if not OPENAPI_PATH.exists():
        print(f"❌ {OPENAPI_PATH} no existe en el repo.")
        print(f"   Generalo y commiteálo:  {REGEN_CMD}")
        return 1
    try:
        repo_schema = json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"❌ No se pudo leer/parsear {OPENAPI_PATH}: {exc}")
        return 1

    # 2. Generar el contrato que produce el código en runtime.
    runtime_schema = _load_app_schema()
    if runtime_schema is None:
        return 1

    # 3. Comparar en forma canónica.
    repo_canon = _canonical(repo_schema)
    runtime_canon = _canonical(runtime_schema)

    if repo_canon == runtime_canon:
        print("✅ Contrato OpenAPI en sync (repo == runtime).")
        return 0

    print("❌ DRIFT detectado entre el contrato versionado y la API real.\n")
    diff = difflib.unified_diff(
        repo_canon.splitlines(),
        runtime_canon.splitlines(),
        fromfile=f"{OPENAPI_PATH} (repo)",
        tofile="app.openapi() (runtime)",
        lineterm="",
        n=2,
    )
    # Mostrar solo las primeras ~60 líneas del diff para no inundar el log.
    for i, line in enumerate(diff):
        if i >= 60:
            print("   ... (diff truncado)")
            break
        print(f"   {line}")

    print(f"\n   Regenerá y commiteá el contrato:  {REGEN_CMD}")
    return 1


if __name__ == "__main__":
    sys.exit(verify_sync())
