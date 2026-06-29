#!/usr/bin/env bash
# kit_upgrade.sh — Trae a la vista las mejoras del SaMD Starter Kit aguas arriba
# (upstream) para un proyecto que lo clonó hace meses, SIN aplicar nada.
#
# Flujo:
#   1. Agrega (si falta) el remote `kit-upstream` apuntando al repo del kit.
#   2. `git fetch kit-upstream`.
#   3. Muestra qué cambios del kit todavía NO tenés (log + diff resumido),
#      EXCLUYENDO las rutas que tu proyecto derivado ya personalizó
#      (app/, frontend/src/, docs/ con contenido propio, etc.).
#   4. Compara tu `.kit-version` contra el del upstream para ubicarte.
#
# IMPORTANTE — el dueño revisa antes de mergear:
#   Este script NO hace merge, NO hace cherry-pick, NO toca tu árbol de trabajo.
#   Solo INFORMA y SUGIERE. Aplicar una mejora del upstream es una decisión
#   humana: muchos archivos del kit (agentes, plantillas DHF, workflows) están
#   pensados para que los adaptes, y un merge ciego pisaría tu personalización.
#   Coherente con la regla SaMD: ningún cambio de arquitectura/algoritmo entra
#   sin revisión y trazabilidad (IEC 62304 §5.6).
#
# Uso:
#   bash scripts/kit_upgrade.sh                       # usa el upstream por defecto
#   KIT_UPSTREAM_URL=<url> bash scripts/kit_upgrade.sh  # override del repo del kit
#   KIT_UPSTREAM_BRANCH=main bash scripts/kit_upgrade.sh
set -euo pipefail

cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"

UPSTREAM_REMOTE="kit-upstream"
UPSTREAM_URL="${KIT_UPSTREAM_URL:-https://github.com/bryan-basg/samd-starter-kit.git}"
UPSTREAM_BRANCH="${KIT_UPSTREAM_BRANCH:-main}"
UPSTREAM_REF="${UPSTREAM_REMOTE}/${UPSTREAM_BRANCH}"

# Rutas que un proyecto derivado típicamente personaliza: las EXCLUIMOS del diff
# para reducir el ruido y centrar la atención en mejoras de plumbing del kit
# (scripts/, workflows, configs). Ajustá esta lista a tu proyecto.
EXCLUDE_PATHS=(
  ":(exclude)app/**"
  ":(exclude)frontend/src/**"
  ":(exclude)docs/**"
  ":(exclude)examples/**"
  ":(exclude)memory/**"
  ":(exclude).env"
  ":(exclude).kit-version"
)

echo "──────────────────────────────────────────────"
echo " kit_upgrade — mejoras del SaMD Starter Kit (solo informa)"
echo "──────────────────────────────────────────────"

# 1) Remote ---------------------------------------------------------------
if git remote get-url "$UPSTREAM_REMOTE" >/dev/null 2>&1; then
  current_url="$(git remote get-url "$UPSTREAM_REMOTE")"
  echo "[1/4] Remote '$UPSTREAM_REMOTE' ya existe → $current_url"
else
  echo "[1/4] Agregando remote '$UPSTREAM_REMOTE' → $UPSTREAM_URL"
  git remote add "$UPSTREAM_REMOTE" "$UPSTREAM_URL"
fi

# 2) Fetch ----------------------------------------------------------------
echo "[2/4] Fetch de '$UPSTREAM_REF' ..."
if ! git fetch --quiet "$UPSTREAM_REMOTE" "$UPSTREAM_BRANCH"; then
  echo "  ✗ No se pudo hacer fetch de '$UPSTREAM_REF'." >&2
  echo "    Revisá la URL (KIT_UPSTREAM_URL) y la rama (KIT_UPSTREAM_BRANCH)." >&2
  exit 1
fi

# 3) Versión --------------------------------------------------------------
echo "[3/4] Versión del kit"
local_ver="$(cat .kit-version 2>/dev/null || echo 'desconocida (sin .kit-version)')"
upstream_ver="$(git show "${UPSTREAM_REF}:.kit-version" 2>/dev/null | head -1 || echo 'desconocida')"
echo "      local     : $local_ver"
echo "      upstream  : $upstream_ver"

# 4) Qué te falta del upstream -------------------------------------------
echo "[4/4] Cambios del kit que tu proyecto aún no tiene (excluyendo lo personalizado)"
echo
ahead_count="$(git rev-list --count "HEAD..${UPSTREAM_REF}" 2>/dev/null || echo 0)"
if [[ "$ahead_count" -eq 0 ]]; then
  echo "  ✓ Estás al día con '$UPSTREAM_REF' (0 commits por delante)."
  echo
  echo "Nada que revisar. (Recordá: este script no aplica cambios — solo informa.)"
  exit 0
fi

echo "  El upstream tiene $ahead_count commit(s) que no están en tu HEAD:"
echo "  ─── git log (resumen) ───────────────────────────────────────────"
git --no-pager log --oneline --no-merges "HEAD..${UPSTREAM_REF}" | sed 's/^/    /'

echo
echo "  ─── archivos del kit con cambios (sin rutas personalizadas) ──────"
changed="$(git --no-pager diff --name-status "HEAD..${UPSTREAM_REF}" -- "${EXCLUDE_PATHS[@]}")"
if [[ -z "$changed" ]]; then
  echo "    (sin diferencias fuera de tus rutas personalizadas)"
else
  echo "$changed" | sed 's/^/    /'
fi

echo
echo "──────────────────────────────────────────────"
echo " Siguiente paso (lo decidís vos — el dueño revisa antes de mergear):"
echo "──────────────────────────────────────────────"
echo "  • Ver el diff completo de un archivo:"
echo "      git diff HEAD..${UPSTREAM_REF} -- <ruta>"
echo "  • Traer un archivo puntual del upstream (revisá antes de commitear):"
echo "      git checkout ${UPSTREAM_REF} -- <ruta>"
echo "  • Traer un commit puntual:"
echo "      git cherry-pick <sha>"
echo
echo "  NO se aplicó ningún cambio. Revisá, adaptá tu personalización y commiteá vos."
