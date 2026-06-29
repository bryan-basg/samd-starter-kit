#!/usr/bin/env bash
# check_placeholders.sh — gate del PROYECTO DERIVADO (después de correr init_kit.sh).
# Escanea los archivos VERSIONADOS y reporta marcadores de plantilla {{ALGO}} que
# quedaron sin reemplazar. Sale con código 1 si encuentra alguno fuera de la allowlist.
#
# IMPORTANTE: en el KIT SIN ADAPTAR este script DEBE fallar — la plantilla está llena
# de {{PROJECT_NAME}}, {{SAMD_CLASS}}, etc. a propósito. Solo tiene sentido como gate
# DESPUÉS de personalizar tu copia con:  bash scripts/init_kit.sh
# (Por eso el workflow placeholder-guard.yml solo lo activa si existe el flag .kit-adapted.)
#
# Los marcadores son los 9 de init_kit.sh: PROJECT_NAME, SAMD_CLASS, INTENDED_USE,
# OWNER, FRONTEND_STACK, BACKEND_STACK, DB_STACK, CLOUD_STACK, CHAT_LANG (y afines).
set -uo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"

# Patrón de marcador del kit: {{ALGO_EN_MAYUS}}.
PATTERN='\{\{[A-Z_]+\}\}'

# Allowlist: archivos que LEGÍTIMAMENTE conservan marcadores como plantilla.
# (case glob: '*' matchea también las barras, así que matchea rutas completas.)
is_allowlisted() {
  case "$1" in
    CLAUDE.md)                    return 0 ;;  # la nota de cabecera cita {{...}} en prosa
    scripts/init_kit.sh)          return 0 ;;  # el reemplazador (contiene el patrón)
    scripts/check_placeholders.sh) return 0 ;; # este propio gate (patrón + ejemplos)
    *TEMPLATE.md)                 return 0 ;;  # RFC-TEMPLATE.md, *_TEMPLATE.md: blanks por uso
  esac
  return 1
}

found=0
while IFS= read -r f; do
  is_allowlisted "$f" && continue
  # -I salta binarios; -q solo testea si hay match.
  if grep -IqE "$PATTERN" "$f" 2>/dev/null; then
    echo "MARCADOR sin reemplazar: $f"
    grep -noE "$PATTERN" "$f" 2>/dev/null | sort -u | sed 's/^/    /'
    found=$((found + 1))
  fi
done < <(git ls-files)

echo
if [ "$found" -gt 0 ]; then
  echo "FALLO: $found archivo(s) con marcadores {{...}} sin reemplazar."
  echo "  -> Corré 'bash scripts/init_kit.sh' para completarlos,"
  echo "     o agregá el archivo a la allowlist de este script si es una plantilla legítima."
  exit 1
fi
echo "OK: 0 marcadores {{...}} sin reemplazar (fuera de la allowlist)."
