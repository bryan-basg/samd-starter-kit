#!/usr/bin/env bash
# run_mutmut.sh — mutation testing del backend (mutmut 2.x) + gate de score.
#
# mutmut prueba si tus tests MATAN mutantes (rompe el código a propósito y verifica
# que algún test lo cace) — no solo si cubren líneas. PESADO y CPU-intensivo: pedí
# OK antes de correrlo sobre una suite grande, y NO lo corras en paralelo con
# agentes/tareas que escriben tests (congela la lista en el dry-run).
#
# Config por env:
#   MUTMUT_PATHS              qué mutar. Default: app/
#   MUTMUT_TESTS              qué tests corre CADA mutante. Default: tests/
#   MUTMUT_SCORE_THRESHOLD    piso del score (%). Default: 80  (ver check_mutmut_score.py)
#   PYTHON_BIN                intérprete. Default: ./venv/bin/python si existe, si no python3
#
# Uso:
#   bash scripts/run_mutmut.sh                 # muta app/ y evalúa el score
#
# Por qué dos detalles que parecen caprichos (los dos nacieron de un fallo real):
#   * mutmut está FIJADO a 2.x. mutmut 3 (lo que instala un `pip install mutmut` pelado)
#     eliminó --paths-to-mutate y --runner: el script se rompía recién al correr.
#   * Los tests de cada mutante corren con scripts/mutmut_pytest_runner.py, no con pytest
#     directo: mutmut 2.5.1 solo da por muerto un mutante si pytest sale con exit 1. Un
#     mutante que rompe el import (exit 4) o una lista de tests vacía (exit 5) contaban
#     como SUPERVIVIENTES. El runner convierte cualquier exit != 0 en 1.
set -uo pipefail
cd "$(dirname "$0")/.."

# Espejo de requirements-dev.txt (tests/test_mutmut_gate.py verifica que coincidan).
MUTMUT_PIN="2.5.1"

PYBIN="${PYTHON_BIN:-$( [ -x ./venv/bin/python ] && echo ./venv/bin/python || echo python3 )}"

if ! "$PYBIN" -c "import mutmut" >/dev/null 2>&1; then
  echo "✗ mutmut no está instalado. Instalá la versión fijada:  pip install mutmut==${MUTMUT_PIN}"
  echo "  (o todo el entorno de desarrollo:  pip install -r requirements-dev.txt)"
  exit 1
fi

MUTMUT_VERSION="$("$PYBIN" -c "from importlib.metadata import version; print(version('mutmut'))" 2>/dev/null || echo "?")"
case "$MUTMUT_VERSION" in
  2.*) ;;
  *)
    echo "✗ Hay mutmut ${MUTMUT_VERSION} instalado; este script usa la CLI de mutmut 2.x"
    echo "  (--paths-to-mutate, --runner), que mutmut 3 eliminó. Instalá:  pip install mutmut==${MUTMUT_PIN}"
    exit 1
    ;;
esac

PATHS="${MUTMUT_PATHS:-app/}"
TESTS="${MUTMUT_TESTS:-tests/}"
RUNNER="${PYBIN} scripts/mutmut_pytest_runner.py ${TESTS} -x -q --no-cov"
echo "▶ mutmut ${MUTMUT_VERSION} run --paths-to-mutate $PATHS  (tests por mutante: $TESTS)"
echo "  Esto puede tardar bastante…"

# --CI: el exit code de mutmut pasa a ser 1 SOLO ante un error fatal (suite roja sin
# mutaciones, path inexistente, crash) y 0 en cualquier otro caso, incluso con
# sobrevivientes. Sobrevivir es un RESULTADO normal que juzga el gate de abajo; un error
# fatal NO se puede tragar con un `|| true` (la corrida "terminaba" y el gate leía un
# cache viejo o vacío).
"$PYBIN" -m mutmut run --CI --paths-to-mutate "$PATHS" --runner "$RUNNER" "$@"
MUTMUT_RC=$?
if [ "$MUTMUT_RC" -ne 0 ]; then
  echo "✗ mutmut terminó con un ERROR (exit ${MUTMUT_RC}), no con un resultado de mutación."
  echo "  Causas típicas: la suite no pasa SIN mutaciones, o MUTMUT_PATHS no existe."
  exit "$MUTMUT_RC"
fi

echo ""
echo "▶ Evaluando el score contra el piso…"
exec "$PYBIN" scripts/check_mutmut_score.py
