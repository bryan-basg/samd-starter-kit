#!/usr/bin/env bash
# run_local_ci.sh — CI local pre-push (stack de referencia: React+TS / Python+FastAPI).
# Falla rápido: si un paso falla, aborta (no se pushea con CI roto).
# Adaptá los comandos a tu stack; el paso de trazabilidad (5/5) es agnóstico y obligatorio.
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"

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

echo "[CI] 5/5 Trazabilidad documental (enlaces cross-doc — obligatorio)"
bash scripts/check_doc_links.sh

echo "[CI] OK"
