"""Runner de pytest para mutmut: toda salida distinta de 0 cuenta como mutante muerto.

mutmut 2.5.1 (`tests_pass`) solo mata con exit 1: un mutante que rompe la importación
(conftest → exit 4) o una lista de tests vacía (exit 5) quedaban como SUPERVIVIENTES,
inflando el número de mutantes vivos con ruido que no es un hueco real de los tests.

pytest corre en ESTE proceso (no en un `bash -c '… || exit 1'`) para que el kill por
timeout de mutmut no deje un pytest huérfano.

Lo invoca `scripts/run_mutmut.sh` vía `--runner`; no se usa a mano.
"""

import os
import sys

# Igual que `python -m pytest`: el primer lugar del path es el repo, no scripts/.
sys.path[0] = os.getcwd()

import pytest  # noqa: E402

if __name__ == "__main__":
    sys.exit(0 if pytest.main(sys.argv[1:]) == 0 else 1)
