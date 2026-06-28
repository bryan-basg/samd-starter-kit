#!/usr/bin/env bash
# run_local_ci.sh — CI local pre-push. Adaptá los comandos a tu stack real.
# Falla rápido: si un paso falla, el script aborta (no se pushea con CI roto).
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"

echo "[CI] 1/5 Lint frontend"
# (cd frontend && npm run lint)

echo "[CI] 2/5 Type-check (frontend tsc + backend type-checker estricto)"
# (cd frontend && npm run typecheck)
# <type-checker backend>

echo "[CI] 3/5 Tests frontend"
# (cd frontend && npm run test)

echo "[CI] 4/5 Tests backend (con entorno activo)"
# npm run backend:test

echo "[CI] 5/5 Auditoría de trazabilidad documental (enlaces cross-doc)"
broken=0
while IFS= read -r line; do
  src=$(echo "$line" | cut -d: -f1)
  link=$(echo "$line" | grep -oE "\(\.{1,2}/[^)]+\.md[^)]*\)" | tr -d '()')
  for L in $link; do
    clean=$(echo "$L" | sed 's/#.*//')
    resolved=$(realpath -q --no-symlinks "$(dirname "$src")/$clean" 2>/dev/null)
    [ ! -f "$resolved" ] && { echo "  BROKEN: $src -> $L"; broken=$((broken+1)); }
  done
done < <(grep -rEn "\(\.{1,2}/[^)]+\.md[^)]*\)" docs/ 2>/dev/null)
[ "$broken" -gt 0 ] && { echo "[CI] FALLO: $broken enlaces cross-doc rotos"; exit 1; }

echo "[CI] OK — descomentá los pasos de tu stack antes de confiar en el verde."
