#!/usr/bin/env bash
# check_doc_links.sh — Link-checker cross-doc del DHF. Falla (exit 1) si hay enlaces rotos.
# Usado por el CI y por run_local_ci.sh. Ningún PR de reorg cierra con enlaces rotos.
#
# Valida TODO enlace Markdown a un `.md` con ruta relativa: con prefijo (`./X.md`, `../X.md`)
# y SIN prefijo (`X.md`, `docs/X.md`). Se ignoran http(s)/mailto/otros esquemas, anclas puras
# (`#seccion`) y rutas absolutas (`/x.md`, que dependen del hosting, no del árbol).
set -uo pipefail
# Relativo al script, no al directorio actual: desde otro lado miraba 0 archivos y daba OK.
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 2

mirados=$(find docs examples . -maxdepth 1 -name '*.md' 2>/dev/null | wc -l)
mirados=$((mirados + $(find docs examples -mindepth 2 -name '*.md' 2>/dev/null | wc -l)))
if [ "$mirados" -eq 0 ]; then
  echo "FALLO: 0 documentos .md que mirar en docs/, examples/ y la raíz." >&2
  exit 2
fi

broken=0
while IFS= read -r line; do
  src=$(echo "$line" | cut -d: -f1)
  link=$(echo "$line" | grep -oE "\]\([^)[:space:]]+\.md[^)[:space:]]*" | sed 's/^](//')
  for L in $link; do
    case "$L" in
      '#'*|/*|*://*|mailto:*) continue ;;
    esac
    clean=$(echo "$L" | sed 's/#.*//')
    resolved=$(realpath -q --no-symlinks "$(dirname "$src")/$clean" 2>/dev/null)
    [ ! -f "$resolved" ] && { echo "BROKEN: $src -> $L"; broken=$((broken+1)); }
  done
done < <(grep -rEn "\]\([^)[:space:]]+\.md[^)[:space:]]*" docs/ examples/ ./*.md 2>/dev/null)

if [ "$broken" -gt 0 ]; then
  echo "FALLO: $broken enlaces cross-doc rotos (docs/ + examples/ + raíz)"
  exit 1
fi
echo "OK: 0 enlaces cross-doc rotos"
