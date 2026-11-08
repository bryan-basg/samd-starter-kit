#!/usr/bin/env bash
# run_local_ci.sh — CI local pre-push (stack de referencia: React+TS / Python+FastAPI).
# Falla rápido: si un paso falla, aborta (no se pushea con CI roto).
# Adaptá los comandos a tu stack; el paso de trazabilidad (5/5) es agnóstico y obligatorio.
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"

# Preflight — un gate que no corrió NO pasa (IEC 62304 §5.7; mismo patrón que scripts/sast.sh).
# Antes ruff/mypy/pytest ausentes se salteaban en silencio y el script cerraba "[CI] OK" sin
# haber mirado el backend. Se chequea ANTES de gastar minutos en el frontend.
# ALLOW_MISSING_TOOLS=1 recupera el salteo, solo para exploración local (NO es un gate aprobado).
ALLOW_MISSING_TOOLS="${ALLOW_MISSING_TOOLS:-0}"
missing=0
need_tool() {
  local tool="$1" hint="$2"
  command -v "$tool" >/dev/null 2>&1 && return 0
  if [ "$ALLOW_MISSING_TOOLS" = "1" ]; then
    echo "  ⚠ $tool no instalado — SALTEADO (ALLOW_MISSING_TOOLS=1). Esto NO es un gate aprobado."
    return 0
  fi
  echo "  ✗ $tool no instalado: el CI local no puede aprobar sin correrlo."
  echo "    Instalá con: $hint  (¿activaste el entorno virtual?)"
  missing=1
}
need_tool ruff "pip install ruff"
need_tool mypy "pip install mypy"
if [ -d tests ]; then need_tool pytest "pip install -r requirements.txt"; fi
if [ "$missing" -ne 0 ]; then
  echo "[CI] FALLO: faltan herramientas del backend (si solo explorás en local: ALLOW_MISSING_TOOLS=1)"
  exit 1
fi

echo "[CI] 1/5 Frontend: lint + types"
if [ -f frontend/package.json ]; then
  (cd frontend && npm run lint && npm run typecheck)
else
  echo "  (sin frontend/package.json — omitido)"
fi

echo "[CI] 2/5 Frontend: tests"
if [ -f frontend/package.json ]; then
  (cd frontend && npm run test -- --run)
else
  echo "  (omitido)"
fi

echo "[CI] 3/5 Backend: imports muertos + type-check estricto"
if command -v ruff >/dev/null 2>&1; then ruff check app/ --select F401,F841,F811; fi
if command -v mypy >/dev/null 2>&1; then mypy .; fi

echo "[CI] 4/5 Backend: tests (activá el entorno virtual antes)"
if command -v pytest >/dev/null 2>&1 && [ -d tests ]; then
  TESTING=True DATABASE_URL="sqlite+aiosqlite:///:memory:" pytest -q
else
  echo "  (sin pytest o sin carpeta tests/ — omitido)"
fi

echo "[CI] 5/5 Trazabilidad documental (enlaces cross-doc + anclas + citas al código — obligatorio)"
bash scripts/check_doc_links.sh
python3 scripts/check_doc_anchors.py
python3 scripts/check_doc_citations.py

echo "[CI] OK"
