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
# Se captura en una variable antes de recortar: con `pipefail`, `grep | head` falla por SIGPIPE
# cuando hay más líneas que el tope, y el `|| echo` imprimía "(sin deuda)" justo con MUCHA deuda.
debt=$(grep -n "Abierta\|Abierto" docs/08_verification_and_audits/TECHNICAL_DEBT_SUMMARY.md 2>/dev/null || true)
if [ -n "$debt" ]; then
  echo "$debt" | head -40
  n=$(echo "$debt" | wc -l)
  [ "$n" -gt 40 ] && echo "  … $n filas en total (se muestran 40)"
else
  echo "  (sin TECHNICAL_DEBT_SUMMARY o sin deuda abierta)"
fi
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
# Mismo patrón que la deuda: contar ANTES de recortar, para no decir "(ninguno)" con 100+ archivos.
# Solo archivos versionados (`git grep`): un `grep -r` sobre el disco contaba también lo ignorado
# (venv/, site/ de mkdocs, __pycache__), que no es parte del kit a adaptar.
if git rev-parse --git-dir >/dev/null 2>&1; then
  markers=$(git grep -lI "{{[A-Z_]*}}" 2>/dev/null || true)
else
  markers=$(grep -rlI "{{[A-Z_]*}}" . --exclude-dir=node_modules 2>/dev/null || true)
fi
if [ -n "$markers" ]; then
  echo "$markers" | head -20
  n=$(echo "$markers" | wc -l)
  [ "$n" -gt 20 ] && echo "  … $n archivos en total (se muestran 20)"
else
  echo "  (ninguno)"
fi
echo
echo "===== FIN — resolvé/anotá lo vivo antes de cerrar. Borrar/archivar lo decide el dueño. ====="
