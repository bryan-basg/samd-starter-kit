#!/usr/bin/env bash
# scripts/generate_sbom.sh — genera el Software Bill of Materials (SBOM) en
# formato CycloneDX 1.5 JSON para el backend Python y el frontend Node de un
# SaMD genérico.
#
#   Proyecto:    {{PROJECT_NAME}}
#   Clase SaMD:  {{SAMD_CLASS}}
#   Stacks:      {{BACKEND_STACK}} (Python) + {{FRONTEND_STACK}} (Node)
#
# Marco regulatorio:
#   - IEC 81001-5-1 §4.1.5 (Software bill of materials).
#   - IEC 62304 §5.1.4 (configuration items / SOUP) y §5.7 (mantenibilidad).
#   - FDA Cybersecurity in Medical Devices (Sep 2023) §V.B.
#   - US Executive Order 14028 (Improving the Nation's Cybersecurity).
#   - EU Cyber Resilience Act (CRA) — SBOM como entregable de cadena de suministro.
#   - NTIA Minimum Elements for an SBOM (2021).
#
# Uso:
#   bash scripts/generate_sbom.sh             # genera baseline completo
#   bash scripts/generate_sbom.sh --backend   # solo backend Python
#   bash scripts/generate_sbom.sh --frontend  # solo frontend Node
#   bash scripts/generate_sbom.sh --help
#
# Variables de entorno (parametrización de paths):
#   SBOM_DIR        — directorio de salida (default: <repo>/sbom)
#   BACKEND_REQS    — requirements.txt del backend (default: <repo>/requirements.txt)
#   FRONTEND_DIR    — carpeta del frontend (default: <repo>/frontend)
#   VENV_DIR        — virtualenv del backend (default: <repo>/venv)
#
# Exit codes:
#   0  OK
#   1  Error de ejecución (CLI rota, archivo faltante, SBOM vacío, etc).
#   2  Herramientas requeridas no instaladas — imprime instrucciones y sale
#      sin generar nada.
#
# Idempotencia: cada corrida produce archivos con timestamp (YYYY-MM-DD) y
# actualiza punteros estables `sbom-latest-backend.json` /
# `sbom-latest-frontend.json` por copia (no symlink; los runners Windows/Mac
# no lo manejan igual).
set -euo pipefail

# ------------------------------------------------------------------ paths
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SBOM_DIR="${SBOM_DIR:-$ROOT_DIR/sbom}"
DATE_TAG="$(date +%Y-%m-%d)"
TS_TAG="$(date +%Y-%m-%dT%H:%M:%S%z)"

BACKEND_REQS="${BACKEND_REQS:-$ROOT_DIR/requirements.txt}"
FRONTEND_DIR="${FRONTEND_DIR:-$ROOT_DIR/frontend}"
FRONTEND_LOCK="$FRONTEND_DIR/package-lock.json"
VENV_DIR="${VENV_DIR:-$ROOT_DIR/venv}"

# ------------------------------------------------------------------ helpers
log()  { printf '[sbom] %s\n' "$*"; }
warn() { printf '[sbom][WARN] %s\n' "$*" >&2; }
err()  { printf '[sbom][ERR] %s\n' "$*" >&2; }

ensure_dir() { mkdir -p "$SBOM_DIR"; }

# Detección estricta del venv. El script NO improvisa instalaciones globales:
# exige un entorno aislado como manda el setup del proyecto.
detect_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        err "venv no encontrado en $VENV_DIR"
        err "Crear con: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
        exit 1
    fi
    if [ ! -x "$VENV_DIR/bin/python" ]; then
        err "$VENV_DIR/bin/python no es ejecutable. Revisa tu venv."
        exit 1
    fi
    # shellcheck source=/dev/null
    source "$VENV_DIR/bin/activate"
    log "venv activado: $(python -c 'import sys; print(sys.executable)')"
}

# ------------------------------------------------------------------ backend
generate_backend() {
    detect_venv
    log "Generando SBOM del backend (Python)..."

    if ! command -v cyclonedx-py >/dev/null 2>&1; then
        err "cyclonedx-py NO esta instalado en el venv."
        cat >&2 <<'EOF'

  Instalacion manual requerida (no se instala silenciosamente):

      source venv/bin/activate
      pip install cyclonedx-bom

  El paquete pip se llama 'cyclonedx-bom'; el binario instalado es
  'cyclonedx-py'. Despues relanza este script.

EOF
        return 2
    fi

    local out_file="$SBOM_DIR/sbom-backend-cyclonedx-${DATE_TAG}.json"
    local latest_file="$SBOM_DIR/sbom-latest-backend.json"

    if [ ! -f "$BACKEND_REQS" ]; then
        err "requirements.txt no encontrado en $BACKEND_REQS"
        return 1
    fi

    log "Inspeccionando el venv para enumerar deps transitivas..."
    # Se prefiere `environment` (instalacion real con sub-dependencias
    # transitivas resueltas) sobre `requirements` (solo top-level): el SBOM
    # regulatorio necesita el grafo completo.
    cyclonedx-py environment \
        --sv 1.5 \
        --of JSON \
        --mc-type application \
        --output-reproducible \
        --validate \
        -o "$out_file" \
        "$VENV_DIR/bin/python"

    # Guard: el SBOM NO puede salir vacío (sin componentes => evidencia inútil).
    if [ ! -s "$out_file" ]; then
        err "SBOM backend vacio. Revisa el venv."
        return 1
    fi

    cp -f "$out_file" "$latest_file"
    log "Backend SBOM -> $out_file"
    log "Pointer estable -> $latest_file"
}

# ------------------------------------------------------------------ frontend
generate_frontend() {
    log "Generando SBOM del frontend (Node)..."

    if [ ! -f "$FRONTEND_LOCK" ]; then
        err "package-lock.json no existe en $FRONTEND_LOCK. Corre 'npm install' en $FRONTEND_DIR."
        return 1
    fi

    if ! ( cd "$FRONTEND_DIR" && npx --yes @cyclonedx/cyclonedx-npm --version >/dev/null 2>&1 ); then
        err "@cyclonedx/cyclonedx-npm no disponible via npx."
        cat >&2 <<'EOF'

  Instalacion manual requerida (sin sudo):

      # Opcion A: cache global de usuario (requiere prefix custom)
      npm config set prefix "$HOME/.npm-global"
      export PATH="$HOME/.npm-global/bin:$PATH"
      npm install -g @cyclonedx/cyclonedx-npm

      # Opcion B: ejecutar siempre via npx (lo que hace este script)
      cd frontend && npx --yes @cyclonedx/cyclonedx-npm --version

  El script usa npx por defecto. Si npx falla, revisa el cache npm.

EOF
        return 2
    fi

    local out_file="$SBOM_DIR/sbom-frontend-cyclonedx-${DATE_TAG}.json"
    local latest_file="$SBOM_DIR/sbom-latest-frontend.json"

    # --omit dev: SOUP de runtime unicamente. Si se necesita auditar dev
    # (mutation/E2E tooling), agregar un segundo run con sufijo `-with-dev.json`.
    ( cd "$FRONTEND_DIR" && npx --yes @cyclonedx/cyclonedx-npm \
        --spec-version 1.5 \
        --output-format JSON \
        --output-reproducible \
        --omit dev \
        --output-file "$out_file" )

    # Guard: lockfile íntegro => SBOM con componentes; vacío => abortar.
    if [ ! -s "$out_file" ]; then
        err "SBOM frontend vacio. Revisa que el lockfile este integro."
        return 1
    fi

    cp -f "$out_file" "$latest_file"
    log "Frontend SBOM -> $out_file"
    log "Pointer estable -> $latest_file"
}

# ------------------------------------------------------------------ summary
generate_summary() {
    log "Generando resumen markdown legible..."

    local summary_file="$SBOM_DIR/sbom-summary-${DATE_TAG}.md"
    local be_file="$SBOM_DIR/sbom-backend-cyclonedx-${DATE_TAG}.json"
    local fe_file="$SBOM_DIR/sbom-frontend-cyclonedx-${DATE_TAG}.json"
    local be_count="N/A"
    local fe_count="N/A"

    if command -v python >/dev/null 2>&1; then
        [ -f "$be_file" ] && be_count="$(python -c "
import json
print(len(json.load(open(r'''$be_file''')).get('components',[])))
" 2>/dev/null || echo "ERR")"
        [ -f "$fe_file" ] && fe_count="$(python -c "
import json
print(len(json.load(open(r'''$fe_file''')).get('components',[])))
" 2>/dev/null || echo "ERR")"
    fi

    cat > "$summary_file" <<SUMMARY
# SBOM Summary — ${DATE_TAG}

> Generado por \`scripts/generate_sbom.sh\` el ${TS_TAG}.
> Proyecto: {{PROJECT_NAME}} · Clase SaMD: {{SAMD_CLASS}}.
> Formato fuente: CycloneDX 1.5 JSON.
> Marco regulatorio: IEC 81001-5-1 §4.1.5 + FDA Cybersecurity 2023 + EO 14028 + EU CRA.

## Totales

| Ecosistema | Archivo CycloneDX | Componentes |
|------------|-------------------|-------------|
| Backend (Python) | sbom-backend-cyclonedx-${DATE_TAG}.json | ${be_count} |
| Frontend (Node)  | sbom-frontend-cyclonedx-${DATE_TAG}.json | ${fe_count} |

## Proximos pasos

1. Cruzar con feeds de CVE (Trivy + npm audit + pip-audit + Dependabot).
2. Registrar HIGH/CRITICAL en \`ISO_14971_RISK_MATRIX.md\` con plazo de remediacion.
3. Versionar este SBOM en Git para trazabilidad SaMD §5.7.

Ver \`docs/07_regulatory_and_compliance/SBOM_MANAGEMENT_PLAN.md\` para la politica completa.
SUMMARY
    log "Summary -> $summary_file"
}

# ------------------------------------------------------------------ main
main() {
    local target="${1:-all}"
    local rc_be=0
    local rc_fe=0

    ensure_dir

    case "$target" in
        --backend)
            generate_backend || rc_be=$?
            ;;
        --frontend)
            generate_frontend || rc_fe=$?
            ;;
        all|--all|"")
            generate_backend || rc_be=$?
            generate_frontend || rc_fe=$?
            ;;
        -h|--help)
            sed -n '1,40p' "$0"
            exit 0
            ;;
        *)
            err "Argumento desconocido: $target"
            err "Uso: bash scripts/generate_sbom.sh [--backend|--frontend|--all]"
            exit 1
            ;;
    esac

    generate_summary || true

    if [ "$rc_be" -eq 2 ] || [ "$rc_fe" -eq 2 ]; then
        err "Una o mas herramientas SBOM no estan instaladas. Revisa los mensajes arriba."
        exit 2
    fi
    if [ "$rc_be" -ne 0 ] || [ "$rc_fe" -ne 0 ]; then
        err "Generacion parcial con errores (backend=$rc_be frontend=$rc_fe)."
        exit 1
    fi

    log "SBOM baseline OK."
    log "Directorio: $SBOM_DIR"
}

main "$@"
