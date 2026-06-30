#!/usr/bin/env bash
# run_mutmut.sh — mutation testing del backend (mutmut) + gate de score.
#
# mutmut prueba si tus tests MATAN mutantes (rompe el código a propósito y verifica
# que algún test lo cace) — no solo si cubren líneas. PESADO y CPU-intensivo: pedí
# OK antes de correrlo sobre una suite grande, y NO lo corras en paralelo con
# agentes/tareas que escriben tests (congela la lista en el dry-run).
#
# Config por env:
#   MUTMUT_PATHS              qué mutar. Default: app/
#   MUTMUT_SCORE_THRESHOLD    piso del score (%). Default: 80  (ver check_mutmut_score.py)
#   PYTHON_BIN                intérprete. Default: ./venv/bin/python si existe, si no python3
#
# Uso:
#   bash scripts/run_mutmut.sh                 # muta app/ y evalúa el score
set -uo pipefail
cd "$(dirname "$0")/.."

PYBIN="${PYTHON_BIN:-$( [ -x ./venv/bin/python ] && echo ./venv/bin/python || echo python3 )}"

if ! "$PYBIN" -c "import mutmut" >/dev/null 2>&1; then
  echo "✗ mutmut no está instalado. Instalá:  pip install mutmut"
  exit 1
fi

PATHS="${MUTMUT_PATHS:-app/}"
echo "▶ mutmut run --paths-to-mutate $PATHS  (esto puede tardar bastante)…"

# Exportar MUTMUT_BIN para que check_mutmut_score.py use el binario correcto del venv
MUTMUT_LOCAL_BIN="$(dirname "$PYBIN")/mutmut"
if [ -x "$MUTMUT_LOCAL_BIN" ]; then
  export MUTMUT_BIN="${MUTMUT_BIN:-$MUTMUT_LOCAL_BIN}"
else
  export MUTMUT_BIN="${MUTMUT_BIN:-mutmut}"
fi

# mutmut sale !=0 cuando hay mutantes vivos; el gate de abajo decide si rompe el build.
"$PYBIN" -m mutmut run --paths-to-mutate "$PATHS" "$@" || true

echo ""
echo "▶ Evaluando el score contra el piso…"
exec "$PYBIN" scripts/check_mutmut_score.py
