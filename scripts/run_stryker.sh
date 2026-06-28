#!/usr/bin/env bash
# run_stryker.sh — mutation testing del frontend (Stryker). Pesado: pedir OK antes.
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)/frontend"
npx stryker run "$@"
