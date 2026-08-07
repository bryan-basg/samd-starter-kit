#!/usr/bin/env bash
# DAST — OWASP ZAP baseline scan contra la app CORRIENDO.
#
# Complementa el stack estático/contrato (SAST + SCA + fuzz de contrato): ZAP ataca
# la app VIVA buscando XSS, inyección, headers de seguridad faltantes, cookies
# inseguras y fugas. Crítico en un SaMD que maneja datos sensibles (HIPAA/GDPR Art. 32).
#
# Por defecto ARRANCA un backend LOCAL (uvicorn app.main:app con env de test) y lo
# escanea. NUNCA apunta a producción por defecto: un scan ACTIVO contra prod
# requiere OK explícito.
#
# Config por env:
#   PORT           puerto del backend local. Default: 8089
#   TARGET         URL a escanear.           Default: http://localhost:PORT/docs
#                  OJO: tiene que ser una ruta que devuelva 200. La raíz `/` de una
#                  API suele NO existir, y ZAP la spiderea igual y da verde sin
#                  haber escaneado nada (ver el guard más abajo). Si tu app sirve
#                  una UI web, apuntá ahí; para una API sola, /docs es lo útil.
#   ZAP_IMAGE      imagen de ZAP.            Default: zaproxy/zap-stable
#   START_BACKEND  1 = arranca backend local; 0 = ya tengo uno en TARGET. Default: 1
#
# Salida: reports/dast/zap_dast_report.{html,json}. Exit !=0 si ZAP reporta FAIL.
set -uo pipefail
cd "$(dirname "$0")/.."

PORT="${PORT:-8089}"
TARGET="${TARGET:-http://localhost:${PORT}/docs}"
REPORT_DIR="$(pwd)/reports/dast"
ZAP_IMAGE="${ZAP_IMAGE:-zaproxy/zap-stable}"
START_BACKEND="${START_BACKEND:-1}"
mkdir -p "$REPORT_DIR"

BACK_PID=""
cleanup() {
  # uvicorn deja un worker hijo: matamos hijos + master para no dejar huérfanos.
  if [ -n "$BACK_PID" ]; then
    pkill -P "$BACK_PID" 2>/dev/null
    kill "$BACK_PID" 2>/dev/null
  fi
}
trap cleanup EXIT

if [ "$START_BACKEND" = "1" ]; then
  if [ -x ./venv/bin/uvicorn ]; then UVI=(./venv/bin/uvicorn); else UVI=(python -m uvicorn); fi
  echo "▶ Arrancando backend local en :$PORT (env de test)…"
  TESTING=True \
  SECRET_KEY="dast_scan_local_only_not_for_production_0123456789ab" \
    "${UVI[@]}" app.main:app --host 0.0.0.0 --port "$PORT" --workers 1 \
    > "$REPORT_DIR/dast_backend.log" 2>&1 &
  BACK_PID=$!
  echo "  esperando /health…"
  for i in $(seq 1 40); do
    if curl -fsS "http://localhost:${PORT}/health" >/dev/null 2>&1; then
      echo "  ✓ backend arriba"; break
    fi
    sleep 1
    [ "$i" = "40" ] && { echo "✗ el backend no levantó — ver $REPORT_DIR/dast_backend.log"; exit 3; }
  done
fi

command -v docker >/dev/null 2>&1 || { echo "✗ docker no encontrado (ZAP corre en contenedor)."; exit 1; }

# ─────────────────────────────────────────────────────────────────────────────
# GUARD: el objetivo tiene que EXISTIR antes de escanearlo.
#
# Sin esto el gate daba un verde que mentía: ZAP spidereaba la raíz `/`, la app
# no tiene ruta raíz (sus rutas son /health, /notes, /docs…), las 3 URLs de
# arranque devolvían 404 y ZAP terminaba con "PASS: 66" habiendo escaneado NADA.
# Un gate que aprueba porque su objetivo no existe es peor que no tener gate:
# firma una verificación que nunca ocurrió (IEC 62304 §5.7).
# ─────────────────────────────────────────────────────────────────────────────
echo "▶ Verificando que el objetivo responde…"
TARGET_CODE="$(curl -s -o /dev/null -w '%{http_code}' "$TARGET" 2>/dev/null || echo 000)"
if [ "$TARGET_CODE" != "200" ]; then
  echo "✗ $TARGET devolvió HTTP $TARGET_CODE (se esperaba 200)."
  echo "  ZAP no puede spiderear un objetivo que no responde: el scan pasaria en"
  echo "  verde sin haber mirado nada. Ajustá TARGET a una ruta que exista."
  echo "  Rutas del esqueleto: /docs (UI del contrato), /health, /openapi.json."
  exit 3
fi
echo "  ✓ $TARGET responde 200"

# El contenedor de ZAP corre con su propio usuario y necesita escribir los
# reportes en el volumen montado. Sin permisos de escritura, ZAP falla con
# AccessDeniedException y el artifact que sube el CI queda VACÍO (se midió: 404
# bytes) — evidencia perdida en un gate regulatorio (§5.7).
chmod 777 "$REPORT_DIR" 2>/dev/null || true

echo "▶ ZAP baseline scan contra $TARGET…"
# --network host: el contenedor alcanza el localhost del host (Linux).
# -m 5: 5 min de spider; -J/-r: reportes.
# -I: gate suave — los WARN (endurecimiento opcional) se REPORTAN pero NO bloquean;
#     SOLO un FAIL (vuln real) → exit !=0. Para endurecer un WARN, moverlo a FAIL
#     vía rules file de ZAP.
docker run --rm --network host \
  -v "$REPORT_DIR:/zap/wrk/:rw" \
  "$ZAP_IMAGE" zap-baseline.py \
  -t "$TARGET" \
  -J zap_dast_report.json \
  -r zap_dast_report.html \
  -m 5 \
  -I
ZAP_EXIT=$?

echo ""
echo "==================== RESUMEN DAST ===================="
echo "Reportes: $REPORT_DIR/zap_dast_report.{html,json}"
echo "ZAP exit: $ZAP_EXIT  (0=limpio · 1=FAIL · 2=solo WARN · 3=error)"

# Segundo guard, del lado de la EVIDENCIA: un scan sin reporte no es verificable.
# Si ZAP salió 0 pero no dejó reporte, el gate no puede aprobar — es el mismo
# fallo que el anterior visto desde la salida en vez de la entrada.
if [ ! -s "$REPORT_DIR/zap_dast_report.json" ]; then
  echo "✗ No se generó el reporte JSON (o quedó vacío)."
  echo "  Sin evidencia no hay verificación demostrable: el gate NO aprueba."
  echo "====================================================="
  exit 3
fi
echo "Evidencia: $(wc -c < "$REPORT_DIR/zap_dast_report.json") bytes de reporte JSON"
echo "====================================================="
exit "$ZAP_EXIT"
