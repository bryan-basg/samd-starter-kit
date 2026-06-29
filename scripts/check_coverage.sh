#!/usr/bin/env bash
# ============================================================================
# Cobertura backend CANÓNICA y reproducible — {{PROJECT_NAME}} (SaMD {{SAMD_CLASS}} §5.7).
#
# POR QUÉ ESTE SCRIPT (no `pytest --cov` a secas):
#   En modo secuencial monoproceso, el data-file de coverage.py se corrompe
#   ("no such table: context") al escribirse desde múltiples greenlets+threads
#   (.coveragerc: concurrency=greenlet,thread) → cientos de falsos "errors" y un
#   TOTAL distinto cada corrida (no reproducible). Fix: xdist + --dist loadscope
#   (reparto determinista) + parallel=True (.coveragerc, cada worker su data-file,
#   `coverage combine` implícito de pytest-cov al final).
#
# DOS PISOS (ambos sobre el MISMO data-file, sin re-correr la suite):
#   1. GLOBAL backend   ≥ COVERAGE_FLOOR     (default 95)
#   2. Capa DATOS/SQL   ≥ SQL_FLOOR          (default 95) — coverage.py no tiene
#      gate por-path nativo: se re-reporta con --include sobre COVERAGE_SQL_INCLUDE.
#
# Config por env (defaults sensatos):
#   COVERAGE_FLOOR        piso global.            Default: 95
#   SQL_FLOOR             piso capa datos/SQL.    Default: 95
#   COVERAGE_SQL_INCLUDE  globs de la capa datos. Default: app/database/*,app/crud/*,app/models/*,app/schemas/*
#   PYTEST_BIN            binario de pytest.      Default: ./venv/bin/pytest (o pytest si no hay venv)
#   COVERAGE_BIN          binario de coverage.    Default: ./venv/bin/coverage (o coverage si no hay venv)
# ============================================================================
set -uo pipefail
# El script vive en scripts/, así que la raíz del repo es el directorio padre.
cd "$(dirname "$0")/.."

export TESTING=True
GLOBAL_FLOOR="${COVERAGE_FLOOR:-95}"
SQL_FLOOR="${SQL_FLOOR:-95}"
SQL_INCLUDE="${COVERAGE_SQL_INCLUDE:-app/database/*,app/crud/*,app/models/*,app/schemas/*}"
PYTEST="${PYTEST_BIN:-$( [ -x ./venv/bin/pytest ] && echo ./venv/bin/pytest || echo pytest )}"
COVERAGE="${COVERAGE_BIN:-$( [ -x ./venv/bin/coverage ] && echo ./venv/bin/coverage || echo coverage )}"

rm -f .coverage .coverage.* 2>/dev/null || true

# 1) Corre la suite con cobertura. Sin gate aquí (--cov-fail-under=0): los pisos se
#    evalúan abajo para poder reportar AMBOS aunque uno falle.
"$PYTEST" tests/ -n auto --dist loadscope \
  --cov=app --cov-report=term-missing --cov-fail-under=0
PYTEST_RC=$?
if [ $PYTEST_RC -ne 0 ]; then
  echo "✗ La suite de tests falló (rc=$PYTEST_RC). Cobertura NO evaluada."
  exit $PYTEST_RC
fi

FAIL=0

echo ""
echo "════════ Piso GLOBAL backend (≥ ${GLOBAL_FLOOR}%) ════════"
if ! "$COVERAGE" report --fail-under="$GLOBAL_FLOOR" >/dev/null 2>&1; then
  echo "✗ Cobertura global por DEBAJO de ${GLOBAL_FLOOR}%"; FAIL=1
fi
"$COVERAGE" report | tail -1

echo ""
echo "════════ Piso capa DATOS/SQL (≥ ${SQL_FLOOR}%) ════════"
if "$COVERAGE" report --include="$SQL_INCLUDE" >/dev/null 2>&1; then
  # La capa existe y tiene archivos cubiertos → el piso se exige.
  if ! "$COVERAGE" report --include="$SQL_INCLUDE" --fail-under="$SQL_FLOOR" >/dev/null 2>&1; then
    echo "✗ Cobertura de la capa datos/SQL por DEBAJO de ${SQL_FLOOR}%"; FAIL=1
  fi
  "$COVERAGE" report --include="$SQL_INCLUDE" | tail -1
else
  echo "  (capa datos/SQL sin archivos cubiertos — piso omitido; existirá cuando agregues $SQL_INCLUDE)"
fi

echo ""
if [ $FAIL -eq 0 ]; then
  echo "✓ Ambos pisos OK (global ≥${GLOBAL_FLOOR}% y datos/SQL ≥${SQL_FLOOR}%)"
else
  echo "✗ Algún piso no se cumple — ver detalle arriba."
fi
exit $FAIL
