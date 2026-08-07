#!/usr/bin/env bash
# sast.sh — Stack de seguridad SaMD-grade. Trivy (CVEs), Semgrep (SAST), schemathesis (fuzz OpenAPI).
# Las tres son BARATAS en CPU — el security-samd las corre sin pedir OK.
# Pentest activo contra PRODUCCIÓN siempre requiere OK explícito del dueño.
#
# Uso: bash scripts/sast.sh [trivy|semgrep|schemathesis|all]
#
# Variables:
#   OPENAPI_URL          contrato a fuzzear.   Default: http://localhost:8000/openapi.json
#   PORT                 puerto del backend.   Default: 8000
#   START_BACKEND        1 = arranca el backend si no responde; 0 = ya tengo uno. Default: 1
#   ALLOW_MISSING_TOOLS  1 = avisar y seguir si falta una herramienta (exploración local).
#                        Default 0 = FALLAR. Ver "gate vacío" abajo.
#
# REGLA DURA — un gate que no escaneó NO pasa (IEC 62304 §5.7):
#   La versión anterior de este script imprimía "herramienta no instalada" y salía 0.
#   Eso es un verde que miente: en CI, un `pip install` que falle en silencio dejaba
#   el gate de seguridad en verde sin haber mirado una sola línea. Por defecto ahora
#   falla; `ALLOW_MISSING_TOOLS=1` recupera el comportamiento viejo para uso local.
set -uo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"

PORT="${PORT:-8000}"
OPENAPI_URL="${OPENAPI_URL:-http://localhost:${PORT}/openapi.json}"
START_BACKEND="${START_BACKEND:-1}"
ALLOW_MISSING_TOOLS="${ALLOW_MISSING_TOOLS:-0}"
rc=0

BACK_PID=""
cleanup() {
  # uvicorn deja un worker hijo: matamos hijos + master para no dejar huérfanos.
  if [ -n "$BACK_PID" ]; then
    pkill -P "$BACK_PID" 2>/dev/null
    kill "$BACK_PID" 2>/dev/null
  fi
}
trap cleanup EXIT

# Falta una herramienta: por defecto es FALLO, no un aviso simpático.
missing_tool() {
  local tool="$1" install_hint="$2"
  if [ "$ALLOW_MISSING_TOOLS" = "1" ]; then
    echo "  ⚠ $tool no instalado — SALTEADO (ALLOW_MISSING_TOOLS=1). Esto NO es un gate aprobado."
    return 0
  fi
  echo "  ✗ $tool no instalado y el gate no puede aprobar sin escanear."
  echo "    Instalá con: $install_hint"
  echo "    (Si estás explorando en local y querés saltearlo: ALLOW_MISSING_TOOLS=1)"
  rc=1
}

run_trivy() {
  echo "== Trivy: CVEs en deps + filesystem =="
  if command -v trivy >/dev/null 2>&1; then
    trivy fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --exit-code 1 . || rc=1
  else
    missing_tool trivy "https://aquasecurity.github.io/trivy/"
  fi
}

run_semgrep() {
  echo "== Semgrep: SAST (Python + TypeScript) =="
  if command -v semgrep >/dev/null 2>&1; then
    semgrep --config auto --error --severity ERROR app/ frontend/src/ || rc=1
  else
    missing_tool semgrep "pip install semgrep"
  fi
}

# Levanta el backend local si el contrato no responde todavía. Sin esto, el fuzz
# moría con "Connection refused": ni el workflow ni este script arrancaban la app,
# y el gate fallaba por harness en vez de por un hallazgo real.
ensure_backend() {
  curl -fsS "$OPENAPI_URL" >/dev/null 2>&1 && { echo "  ✓ contrato ya disponible en $OPENAPI_URL"; return 0; }

  if [ "$START_BACKEND" != "1" ]; then
    echo "  ✗ $OPENAPI_URL no responde y START_BACKEND=0."
    return 1
  fi

  if [ -x ./venv/bin/uvicorn ]; then UVI=(./venv/bin/uvicorn); else UVI=(python -m uvicorn); fi
  echo "  ▶ arrancando backend local en :$PORT (env de test)…"
  mkdir -p reports/schemathesis
  TESTING=True \
  SECRET_KEY="schemathesis_local_only_not_for_production_0123456789ab" \
    "${UVI[@]}" app.main:app --host 127.0.0.1 --port "$PORT" --workers 1 \
    > reports/schemathesis/backend.log 2>&1 &
  BACK_PID=$!

  for i in $(seq 1 40); do
    if curl -fsS "http://127.0.0.1:${PORT}/health" >/dev/null 2>&1; then
      echo "  ✓ backend arriba"; return 0
    fi
    sleep 1
  done
  echo "  ✗ el backend no levantó en 40s — ver reports/schemathesis/backend.log"
  tail -20 reports/schemathesis/backend.log 2>/dev/null
  return 1
}

run_schemathesis() {
  echo "== schemathesis: fuzz de contrato contra $OPENAPI_URL =="
  echo "  (local/staging OK sin pedir; contra PRODUCCIÓN requiere OK explícito)"
  if ! command -v schemathesis >/dev/null 2>&1; then
    missing_tool schemathesis "pip install schemathesis"
    return
  fi
  if ! ensure_backend; then
    rc=1
    return
  fi
  # Los endpoints de demostración del esqueleto (`/demo/*`) devuelven 500 y 503 A
  # PROPÓSITO: existen para ilustrar el handler global sin traceback y el fusible
  # con Retry-After. Fuzzearlos reporta "Server error" en algo que está haciendo
  # justo lo que debe. Se excluyen del fuzz, NO se "arreglan".
  # Si tu proyecto no tiene endpoints así, borrá el --exclude-path.
  schemathesis run "$OPENAPI_URL" \
    --checks all \
    --exclude-path-regex '^/demo/' \
    ${SCHEMATHESIS_EXAMPLES:+--max-examples "$SCHEMATHESIS_EXAMPLES"} || rc=1
}

case "${1:-all}" in
  trivy)        run_trivy ;;
  semgrep)      run_semgrep ;;
  schemathesis) run_schemathesis ;;
  all)          run_trivy; run_semgrep; run_schemathesis ;;
  *) echo "uso: $0 [trivy|semgrep|schemathesis|all]"; exit 1 ;;
esac

exit "$rc"
