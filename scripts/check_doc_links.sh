#!/usr/bin/env bash
# check_doc_links.sh — Link-checker cross-doc del DHF. Falla (exit 1) si hay enlaces rotos.
# Usado por el CI y por run_local_ci.sh. Ningún PR de reorg cierra con enlaces rotos.
set -uo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"

broken=0
while IFS= read -r line; do
  src=$(echo "$line" | cut -d: -f1)
  link=$(echo "$line" | grep -oE "\(\.{1,2}/[^)]+\.md[^)]*\)" | tr -d '()')
  for L in $link; do
    clean=$(echo "$L" | sed 's/#.*//')
    resolved=$(realpath -q --no-symlinks "$(dirname "$src")/$clean" 2>/dev/null)
    [ ! -f "$resolved" ] && { echo "BROKEN: $src -> $L"; broken=$((broken+1)); }
  done
done < <(grep -rEn "\(\.{1,2}/[^)]+\.md[^)]*\)" docs/ examples/ ./*.md 2>/dev/null)

if [ "$broken" -gt 0 ]; then
  echo "FALLO: $broken enlaces cross-doc rotos (docs/ + examples/ + raíz)"
  exit 1
fi
echo "OK: 0 enlaces cross-doc rotos"
