#!/usr/bin/env bash
# init_kit.sh — Reemplaza los marcadores {{...}} del SaMD Starter Kit con los
# valores de tu proyecto, en todos los archivos de texto del repo.
#
# Uso interactivo:   bash scripts/init_kit.sh
# Uso no interactivo: PROJECT_NAME="Mi App" SAMD_CLASS="B" ... bash scripts/init_kit.sh --yes
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

declare -A VARS=(
  [PROJECT_NAME]="${PROJECT_NAME:-}"
  [SAMD_CLASS]="${SAMD_CLASS:-}"
  [INTENDED_USE]="${INTENDED_USE:-}"
  [OWNER]="${OWNER:-}"
  [FRONTEND_STACK]="${FRONTEND_STACK:-}"
  [BACKEND_STACK]="${BACKEND_STACK:-}"
  [DB_STACK]="${DB_STACK:-}"
  [CLOUD_STACK]="${CLOUD_STACK:-}"
  [CHAT_LANG]="${CHAT_LANG:-}"
)

PROMPTS=(PROJECT_NAME SAMD_CLASS INTENDED_USE OWNER FRONTEND_STACK BACKEND_STACK DB_STACK CLOUD_STACK CHAT_LANG)

if [[ "${1:-}" != "--yes" ]]; then
  echo "Completá los valores del proyecto (Enter para dejar el marcador sin reemplazar):"
  for k in "${PROMPTS[@]}"; do
    if [[ -z "${VARS[$k]}" ]]; then
      read -rp "  {{$k}} = " val
      VARS[$k]="$val"
    fi
  done
fi

echo "Reemplazando marcadores en $ROOT ..."
for k in "${PROMPTS[@]}"; do
  val="${VARS[$k]}"
  [[ -z "$val" ]] && continue
  # Escapar caracteres especiales de sed en el valor
  esc=$(printf '%s' "$val" | sed -e 's/[\/&]/\\&/g')
  grep -rlZ --binary-files=without-match "{{$k}}" "$ROOT" \
    --exclude-dir=.git --exclude="init_kit.sh" 2>/dev/null \
    | xargs -0 -r sed -i "s/{{$k}}/$esc/g"
  echo "  {{$k}} -> $val"
done

echo "Listo. Marcadores restantes sin reemplazar:"
grep -rn "{{[A-Z_]*}}" "$ROOT" --exclude-dir=.git --exclude="init_kit.sh" || echo "  (ninguno)"
echo
echo "Próximo paso: clasificá tu software en docs/07_regulatory_and_compliance/SOFTWARE_SAFETY_CLASSIFICATION.md"
