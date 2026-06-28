#!/usr/bin/env bash
# sast.sh — Stack de seguridad SaMD-grade. Trivy (CVEs), Semgrep (SAST), schemathesis (fuzz OpenAPI).
# Las tres son BARATAS en CPU — el security-samd las corre sin pedir OK.
# Pentest activo contra PRODUCCIÓN siempre requiere OK explícito del dueño.
#
# Uso: bash scripts/sast.sh [trivy|semgrep|schemathesis|all]
set -uo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"

OPENAPI_URL="${OPENAPI_URL:-http://localhost:8000/openapi.json}"
rc=0

run_trivy() {
  echo "== Trivy: CVEs en deps + filesystem =="
  if command -v trivy >/dev/null 2>&1; then
    trivy fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --exit-code 1 . || rc=1
  else
    echo "  trivy no instalado — https://aquasecurity.github.io/trivy/"
  fi
}

run_semgrep() {
  echo "== Semgrep: SAST (Python + TypeScript) =="
  if command -v semgrep >/dev/null 2>&1; then
    semgrep --config auto --error --severity ERROR app/ frontend/src/ || rc=1
  else
    echo "  semgrep no instalado — pip install semgrep"
  fi
}

run_schemathesis() {
  echo "== schemathesis: fuzz de contrato contra $OPENAPI_URL =="
  echo "  (local/staging OK sin pedir; contra PRODUCCIÓN requiere OK explícito)"
  if command -v schemathesis >/dev/null 2>&1; then
    schemathesis run "$OPENAPI_URL" --checks all || rc=1
  else
    echo "  schemathesis no instalado — pip install schemathesis"
  fi
}

case "${1:-all}" in
  trivy)        run_trivy ;;
  semgrep)      run_semgrep ;;
  schemathesis) run_schemathesis ;;
  all)          run_trivy; run_semgrep; run_schemathesis ;;
  *) echo "uso: $0 [trivy|semgrep|schemathesis|all]"; exit 1 ;;
esac

exit "$rc"
