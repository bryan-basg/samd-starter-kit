#!/usr/bin/env bash
# sast.sh — Stubs del stack de seguridad SaMD-grade. Descomentá según tu stack.
# Trivy (CVEs), Semgrep (SAST), schemathesis (fuzz de contrato OpenAPI).
# Las tres son BARATAS en CPU — el security-samd las corre sin pedir OK.
# Pentest activo contra producción SIEMPRE requiere OK explícito del dueño.
set -euo pipefail

case "${1:-all}" in
  trivy)        echo "[SAST] Trivy — CVEs deps + Docker";  : ;; # trivy fs . ; trivy image <img>
  semgrep)      echo "[SAST] Semgrep — SAST código";       : ;; # semgrep --config auto app/ frontend/src/
  schemathesis) echo "[SAST] schemathesis — fuzz OpenAPI"; : ;; # schemathesis run <openapi-url>
  all)          bash "$0" trivy; bash "$0" semgrep; bash "$0" schemathesis ;;
  *) echo "uso: $0 [trivy|semgrep|schemathesis|all]"; exit 1 ;;
esac
