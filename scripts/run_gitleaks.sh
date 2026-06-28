#!/usr/bin/env bash
# scripts/run_gitleaks.sh — escanea TODO el historial git en busca de secretos
# filtrados (API keys, tokens, passwords, claves privadas).
#
#   Proyecto:   {{PROJECT_NAME}}
#   Clase SaMD: {{SAMD_CLASS}}
#
# Un hook pre-commit solo revisa archivos en stage; este script audita el repo
# COMPLETO incluyendo commits viejos (un secreto rotado pero aún en el historial
# sigue siendo un secreto comprometido — GDPR Art.32 / HIPAA Security Rule).
#
# Wrapper fino sobre gitleaks: usa la allowlist auditada en `.gitleaks.toml`.
#
# Uso:
#   bash scripts/run_gitleaks.sh
#
# Variables de entorno:
#   GITLEAKS_CONFIG  — ruta a la config (default: <repo>/.gitleaks.toml)
#   GITLEAKS_REPORT  — ruta del reporte JSON (default: <repo>/audit/gitleaks_report.json)
#
# Exit codes:
#   0  sin secretos
#   1  secretos detectados (revisar el reporte)
#   2  gitleaks no esta instalado
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

CONFIG="${GITLEAKS_CONFIG:-$ROOT_DIR/.gitleaks.toml}"
REPORT="${GITLEAKS_REPORT:-$ROOT_DIR/audit/gitleaks_report.json}"

# Aviso claro si la herramienta no esta instalada (no asumir que esta en PATH).
if ! command -v gitleaks >/dev/null 2>&1; then
    echo "[gitleaks][ERR] gitleaks no esta instalado o no esta en PATH." >&2
    cat >&2 <<'EOF'

  Instalacion:
      # Go:        go install github.com/gitleaks/gitleaks/v8@latest
      # macOS:     brew install gitleaks
      # Binario:   https://github.com/gitleaks/gitleaks/releases
      # Docker:    docker run -v "$PWD:/repo" zricethezav/gitleaks:latest detect --source=/repo

EOF
    exit 2
fi

mkdir -p "$(dirname "$REPORT")"

echo "[gitleaks] Escaneando historial completo (config: $CONFIG)..."
# --redact: nunca imprime el valor del secreto en logs (los logs de CI son
#           públicos en muchos setups).
# detect (sin --no-git): recorre TODO el historial, no solo el working tree.
gitleaks detect --redact --source . --config "$CONFIG" \
    --report-format json --report-path "$REPORT" || {
    echo "[gitleaks][ERR] Secretos detectados. Revisa $REPORT" >&2
    echo "[gitleaks] Si es un falso positivo auditado, anadilo a .gitleaks.toml (ver comentarios)." >&2
    exit 1
}

echo "[gitleaks] OK — sin secretos detectados en el historial."
