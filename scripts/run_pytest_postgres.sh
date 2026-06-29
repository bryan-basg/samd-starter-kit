#!/usr/bin/env bash
# run_pytest_postgres.sh — corre la suite contra PostgreSQL REAL (vs SQLite por
# defecto) para cazar lo que SQLite oculta: tipos, defaults SQL, drivers async,
# extensiones. Self-contained: levanta un contenedor con `docker run`, espera el
# health, corre pytest con DATABASE_URL apuntando ahí, y lo tira al salir.
#
# Config por env:
#   POSTGRES_IMAGE  imagen. Default: postgres:16-alpine (para pgvector: pgvector/pgvector:pg16)
#   PG_PORT         puerto host. Default: 5433
#   DATABASE_URL    override completo de la cadena de conexión.
#
# Uso:
#   bash scripts/run_pytest_postgres.sh                  # solo @pytest.mark.postgres
#   bash scripts/run_pytest_postgres.sh tests/test_x.py  # archivo específico
set -euo pipefail
cd "$(dirname "$0")/.."

command -v docker >/dev/null 2>&1 || { echo "✗ docker no encontrado. Este tier requiere Docker."; exit 1; }

IMAGE="${POSTGRES_IMAGE:-postgres:16-alpine}"
PORT="${PG_PORT:-5433}"
NAME="samd-pg-test-$$"

echo "▶ Levantando $IMAGE en :$PORT…"
docker run -d --rm --name "$NAME" \
  -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=test \
  -p "$PORT:5432" "$IMAGE" >/dev/null
trap 'docker rm -f "$NAME" >/dev/null 2>&1 || true' EXIT

echo "▶ Esperando que Postgres esté listo…"
for i in $(seq 1 30); do
  if docker exec "$NAME" pg_isready -U test -d test >/dev/null 2>&1; then
    echo "  ✓ listo (intento $i)"; break
  fi
  sleep 1
  [ "$i" = "30" ] && { echo "✗ Postgres no levantó a tiempo."; exit 1; }
done

export DATABASE_URL="${DATABASE_URL:-postgresql+asyncpg://test:test@localhost:$PORT/test}"
export TESTING=True

PYBIN="$( [ -x ./venv/bin/python ] && echo ./venv/bin/python || echo python3 )"
ARGS=("$@"); [ ${#ARGS[@]} -eq 0 ] && ARGS=("-m" "postgres" "-v")

echo "▶ pytest contra Postgres real…"
"$PYBIN" -m pytest "${ARGS[@]}"
