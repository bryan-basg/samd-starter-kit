#!/usr/bin/env bash
# run_act.sh — corre los workflows de GitHub Actions localmente con nektos/act,
# para iterar el CI sin pushear. Por defecto corre el workflow de CI principal.
#
# Config por env:
#   ACT_WORKFLOW   workflow a correr. Default: .github/workflows/ci.yml
#   ACT_JOB        job específico (vacío = todos los del workflow).
#   Si existe un archivo `.secrets` en la raíz, se pasa con --secret-file.
#
# Requiere `act` (https://github.com/nektos/act) + Docker.
set -euo pipefail
cd "$(dirname "$0")/.."

command -v act >/dev/null 2>&1 || {
  echo "✗ 'act' no está instalado. Ver https://github.com/nektos/act"
  echo "  (brew install act · o descargá el binario de releases)"
  exit 1
}
docker info >/dev/null 2>&1 || { echo "✗ Docker no está corriendo o sin permisos."; exit 1; }

WF="${ACT_WORKFLOW:-.github/workflows/ci.yml}"
JOB="${ACT_JOB:-}"

ARGS=(-W "$WF" --container-architecture linux/amd64)
[ -n "$JOB" ] && ARGS=(-j "$JOB" "${ARGS[@]}")
[ -f .secrets ] && ARGS+=(--secret-file .secrets)

echo "▶ act $WF ${JOB:+(job: $JOB)}…"
act "${ARGS[@]}"
echo "✓ Simulación completada."
