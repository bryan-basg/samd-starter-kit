#!/usr/bin/env bash
# run_stryker.sh — mutation testing del frontend (Stryker). Pesado: pedir OK antes.
#
# `npx --no-install`: sin esa bandera, si @stryker-mutator/core no está instalado npx baja
# en silencio el paquete LEGADO y deprecado `stryker` (otro motor, otra versión: un score que
# no es el del proyecto). Mejor fallar con un mensaje claro (IEC 62304 §8, control de SOUP).
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)/frontend"

if ! npx --no-install stryker --version >/dev/null 2>&1; then
  echo "✗ Stryker no está instalado en frontend/ (@stryker-mutator/core)." >&2
  echo "  Instalalo con: cd frontend && npm install --save-dev @stryker-mutator/core" >&2
  echo "  (más el runner/checker que use stryker.config: p. ej. @stryker-mutator/vitest-runner)" >&2
  echo "  y volvé a correr: bash scripts/run_stryker.sh" >&2
  exit 1
fi
npx --no-install stryker run "$@"
