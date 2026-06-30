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

# Ejemplo orientativo por campo (se muestra en el prompt, no se guarda).
declare -A HINTS=(
  [PROJECT_NAME]="ej. AuraLog"
  [SAMD_CLASS]="A, B o C — la clase de seguridad IEC 62304 §4.3"
  [INTENDED_USE]="ej. registro y seguimiento de síntomas para una condición crónica"
  [OWNER]="tu nombre o handle de GitHub (dueño del repo)"
  [FRONTEND_STACK]="ej. React + TypeScript"
  [BACKEND_STACK]="ej. Python + FastAPI"
  [DB_STACK]="ej. PostgreSQL"
  [CLOUD_STACK]="ej. Google Cloud Platform"
  [CHAT_LANG]="ej. español — idioma del chat con el agente"
)

PROMPTS=(PROJECT_NAME SAMD_CLASS INTENDED_USE OWNER FRONTEND_STACK BACKEND_STACK DB_STACK CLOUD_STACK CHAT_LANG)

# Normaliza y valida la clase de seguridad: debe ser A, B o C (o vacío para omitir).
validate_class() {
  local v="${1^^}"   # a -> A
  case "$v" in
    A|B|C|"") printf '%s' "$v"; return 0 ;;
    *) return 1 ;;
  esac
}

if [[ "${1:-}" != "--yes" ]]; then
  echo "Completá los valores del proyecto (Enter para dejar el marcador sin reemplazar):"
  for k in "${PROMPTS[@]}"; do
    [[ -n "${VARS[$k]}" ]] && continue
    while true; do
      read -rp "  {{$k}}  (${HINTS[$k]}) = " val
      if [[ "$k" == "SAMD_CLASS" ]]; then
        if val="$(validate_class "$val")"; then
          VARS[$k]="$val"; break
        else
          echo "    ↳ La clase debe ser A, B o C. Probá de nuevo (o Enter para decidirla luego)."
        fi
      else
        VARS[$k]="$val"; break
      fi
    done
  done
else
  # Modo no interactivo: validar la clase si vino por variable de entorno.
  if [[ -n "${VARS[SAMD_CLASS]}" ]]; then
    if ! VARS[SAMD_CLASS]="$(validate_class "${VARS[SAMD_CLASS]}")"; then
      echo "ERROR: SAMD_CLASS='${SAMD_CLASS}' inválida. Debe ser A, B o C." >&2
      exit 1
    fi
  fi
fi

echo
echo "Reemplazando marcadores en $ROOT ..."
for k in "${PROMPTS[@]}"; do
  val="${VARS[$k]}"
  [[ -z "$val" ]] && continue
  # Escapar caracteres especiales de sed en el valor
  esc=$(printf '%s' "$val" | sed -e 's/[\/&]/\\&/g')
  grep -rlZ --binary-files=without-match "{{$k}}" "$ROOT" \
    --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=venv --exclude-dir=.venv \
    --exclude-dir=.mypy_cache --exclude-dir=.pytest_cache --exclude-dir=.ruff_cache --exclude-dir=dist \
    --exclude="init_kit.sh" 2>/dev/null \
    | xargs -0 -r sed -i "s/{{$k}}/$esc/g"
  echo "  {{$k}} -> $val"
done

echo
remaining="$(grep -rl "{{[A-Z_]*}}" "$ROOT" --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=venv --exclude-dir=.venv --exclude-dir=.mypy_cache --exclude-dir=.pytest_cache --exclude-dir=.ruff_cache --exclude-dir=dist --exclude="init_kit.sh" 2>/dev/null || true)"
if [[ -n "$remaining" ]]; then
  echo "Marcadores sin reemplazar (los podés completar luego o re-correr este script):"
  grep -rn "{{[A-Z_]*}}" "$ROOT" --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=venv --exclude-dir=.venv --exclude-dir=.mypy_cache --exclude-dir=.pytest_cache --exclude-dir=.ruff_cache --exclude-dir=dist --exclude="init_kit.sh" 2>/dev/null \
    | sed 's/^/  /' | head -20
  total="$(grep -rho "{{[A-Z_]*}}" "$ROOT" --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=venv --exclude-dir=.venv --exclude-dir=.mypy_cache --exclude-dir=.pytest_cache --exclude-dir=.ruff_cache --exclude-dir=dist --exclude="init_kit.sh" 2>/dev/null | wc -l | tr -d ' ')"
  [[ "$total" -gt 20 ]] && echo "  ... y más (total $total ocurrencias)"
else
  echo "✓ No quedan marcadores sin reemplazar."
fi

# Próximos pasos.
cls="${VARS[SAMD_CLASS]}"
echo
echo "──────────────────────────────────────────────"
echo " Próximos pasos"
echo "──────────────────────────────────────────────"
echo " 1. Leé la guía de arranque:  GETTING_STARTED.md"
echo " 2. Clasificá tu software (A/B/C) y registralo en:"
echo "      docs/07_regulatory_and_compliance/SOFTWARE_SAFETY_CLASSIFICATION.md"
echo " 3. Completá los 4 documentos base, en orden:"
echo "      clasificación → Master Map → matriz de riesgo ISO 14971 → matriz de trazabilidad"
echo "    (mirá examples/auralog/ para verlos rellenos en un dispositivo Clase B ficticio)"
if [[ -n "$cls" ]]; then
  echo
  echo " Tu clase: $cls"
  case "$cls" in
    A) echo "   Clase A: igual necesitás los básicos — una afirmación de 'sin daño' debe quedar documentada y ser defendible." ;;
    B) echo "   Clase B: sumá arquitectura + segregación de ítems, plan de desarrollo, evaluación clínica y vigilancia post-mercado." ;;
    C) echo "   Clase C: rigor máximo — diseño detallado, verificación independiente de cada control, usabilidad sumativa (IEC 62366) y QMS ISO 13485." ;;
  esac
fi
echo "──────────────────────────────────────────────"
