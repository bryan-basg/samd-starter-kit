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
echo "--- Ramas remotas sin mergear a origin/main ---"
# En CI el checkout es de UNA sola rama: la sección local de arriba queda ciega. Esta mira el remoto.
# Ojo: con squash-merge git NO reconoce la rama como integrada, así que pueden aparecer ramas cuyo
# PR ya se mergeó. Verificá cada una (p. ej. `gh pr list --state merged --head <rama>`) antes de
# darla por trabajo vivo; borrarlas lo decide el dueño.
if git rev-parse --verify -q origin/main >/dev/null 2>&1; then
  remote_unmerged=$(git branch -r --no-merged origin/main 2>/dev/null \
    | sed 's/^[* ]*//' | grep '^origin/' | grep -v -e '^origin/HEAD' -e '^origin/main$' || true)
  if [ -n "$remote_unmerged" ]; then
    echo "$remote_unmerged"
    echo "  ($(echo "$remote_unmerged" | wc -l) ramas; con squash-merge pueden ser ramas ya integradas)"
  else
    echo "  (ninguna)"
  fi
else
  echo "  (sin origin/main — no se puede comparar; ¿falta 'git fetch'?)"
fi
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
# La fila plantilla `D-XXX-01` (scope XXX) no es deuda real: se ignora toda fila con `XXX`.
debt=$(grep -n "Abierta\|Abierto" docs/08_verification_and_audits/TECHNICAL_DEBT_SUMMARY.md 2>/dev/null | grep -v "XXX" || true)
if [ -n "$debt" ]; then
  echo "$debt" | head -40
  n=$(echo "$debt" | wc -l)
  [ "$n" -gt 40 ] && echo "  … $n filas en total (se muestran 40)"
else
  echo "  (sin TECHNICAL_DEBT_SUMMARY o sin deuda abierta)"
fi
echo
echo "--- Enlaces cross-doc rotos ---"
# Una sola fuente de verdad: el mismo link-checker del CI (cubre rutas con y sin prefijo ./ ../).
bash scripts/check_doc_links.sh 2>&1 | sed 's/^/  /' || true
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
