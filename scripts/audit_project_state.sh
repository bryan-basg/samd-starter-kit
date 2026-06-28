#!/usr/bin/env bash
# audit_project_state.sh — Foto del estado del proyecto antes de cerrar un bloque grande.
# Barre los rincones donde se esconden trabajo y deuda. Solo INFORMA; no borra nada.
set -uo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"

echo "===== FOTO DEL ESTADO DEL PROYECTO ====="
echo
echo "--- Ramas sin mergear a la principal ---"
git branch --no-merged 2>/dev/null || true
echo
echo "--- Ramas solo en disco (no en remoto) ---"
git for-each-ref --format='%(refname:short) %(upstream)' refs/heads 2>/dev/null | awk '$2=="" {print $1}'
echo
echo "--- Stashes ---"
git stash list 2>/dev/null || true
echo
echo "--- Worktrees ---"
git worktree list 2>/dev/null || true
echo
echo "--- Cambios sin commitear ---"
git status --short 2>/dev/null || true
echo
echo "--- Deuda técnica abierta (DHF) ---"
grep -rn "Abierta\|Abierto" docs/08_verification_and_audits/TECHNICAL_DEBT_SUMMARY.md 2>/dev/null | head -40 || echo "  (sin TECHNICAL_DEBT_SUMMARY o sin deuda abierta)"
echo
echo "--- Enlaces cross-doc rotos ---"
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
echo "  Enlaces rotos: $broken"
echo
echo "--- Marcadores del kit sin reemplazar ---"
grep -rln "{{[A-Z_]*}}" . --exclude-dir=.git 2>/dev/null | head -20 || echo "  (ninguno)"
echo
echo "===== FIN — resolvé/anotá lo vivo antes de cerrar. Borrar/archivar lo decide el dueño. ====="
