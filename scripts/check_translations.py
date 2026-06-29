#!/usr/bin/env python3
"""Auditor de cobertura i18n — frontend + backend ({{PROJECT_NAME}}, SaMD {{SAMD_CLASS}} §5.4).

Detecta DINÁMICAMENTE los idiomas y los namespaces (NO hardcodea listas: una lista
hardcodeada se queda ciega cuando agregás un idioma o movés una carpeta, y el
problema se acumula en silencio). Hace DOS chequeos contra el idioma base:

1. PARIDAD DE CLAVES — claves que faltan o sobran. Gate duro (rompe CI).

2. SIN TRADUCIR — valores IDÉNTICOS a la base (texto "copiado" como placeholder y
   nunca traducido). Históricamente invisible: la clave existe, así que la paridad
   da verde mientras la app muestra el idioma base en otro idioma.
   · En idiomas de alfabeto NO latino (zh, ja, ko, ru…) un valor idéntico a la base
     es, casi sin excepción, traducción faltante real → gate duro.
   · En idiomas latinos (en, pt, it, fr, de, nl, sv…) hay coincidencias legítimas
     ("Total", "Error"…), así que sólo se INFORMA; no rompe el gate.
   Marca, siglas y nombres propios se descartan vía ALLOW_TOKENS + IGNORE_KEY_PATTERNS
   (ambos extensibles por env — sumá los términos de TU producto, no los hardcodees acá).

Config por env (con defaults sensatos):
    I18N_BASE_LANG           idioma base. Default: en
    I18N_FRONTEND_DIR        carpeta de locales frontend. Default: frontend/public/locales
    I18N_BACKEND_DIR         carpeta de locales backend.  Default: locales
    I18N_NONLATIN_STRICT     idiomas con gate duro de sin-traducir. Default: zh,ja,ko,ru
    I18N_ALLOW_TOKENS        términos extra legítimos de dejar igual (coma-separados; tu marca).
    I18N_IGNORE_KEY_PATTERNS patrones de clave extra a ignorar (coma-separados; regex).

Uso:
    python scripts/check_translations.py              # resumen (conteos + %)
    python scripts/check_translations.py -v           # además lista las claves
    python scripts/check_translations.py --no-untranslated   # sólo paridad de claves
"""
import json
import os
import re
import sys
from typing import Any

BASE_LANG = os.environ.get("I18N_BASE_LANG", "en")
FRONTEND_DIR = os.environ.get("I18N_FRONTEND_DIR", "frontend/public/locales")
BACKEND_DIR = os.environ.get("I18N_BACKEND_DIR", "locales")
VERBOSE = "-v" in sys.argv or "--verbose" in sys.argv
CHECK_UNTRANSLATED = "--no-untranslated" not in sys.argv

# Idiomas de alfabeto no latino: un valor idéntico a la base = traducción faltante
# real (no hay coincidencias legítimas). Estos rompen el gate.
NONLATIN_STRICT = {
    s.strip() for s in (os.environ.get("I18N_NONLATIN_STRICT") or "zh,ja,ko,ru").split(",") if s.strip()
}

# Términos GENÉRICOS legítimos de dejar igual que la base (técnicos, siglas,
# nombres nativos de idioma). Sumá los TUYOS (marca, productos, librerías) por env
# I18N_ALLOW_TOKENS="acme,widgetpro,...". Comparación en minúsculas.
_DEFAULT_ALLOW = {
    "email", "id", "url", "api", "pdf", "csv", "json", "xml", "html", "http",
    "https", "sla", "tbd", "ai", "ok", "css", "sdk", "ui", "ux", "faq", "sms",
    "utc", "tz", "iso", "uuid",
    # nombres nativos de idioma (viajan igual en todos los idiomas)
    "deutsch", "english", "español", "francais", "français", "italiano",
    "nederlands", "portugues", "português", "svenska",
}
_EXTRA_ALLOW = {
    t.strip().lower() for t in (os.environ.get("I18N_ALLOW_TOKENS") or "").split(",") if t.strip()
}
ALLOW_TOKENS = _DEFAULT_ALLOW | _EXTRA_ALLOW

# Patrones de clave cuyo valor es legítimamente idéntico a la base (marca, versión,
# nombres nativos de idioma, copyrights de librerías). Sumá los tuyos por env
# I18N_IGNORE_KEY_PATTERNS="^legal\\.,\\.brand_name$".
_DEFAULT_IGNORE = (
    r"^legal\.",
    r"\.brand_name$",
    r"\.app_version$",
    r"^settings\.lang_",
    r"\.export_filename$",
    r"\.server_tz_value$",
)
_EXTRA_IGNORE = tuple(
    p.strip() for p in (os.environ.get("I18N_IGNORE_KEY_PATTERNS") or "").split(",") if p.strip()
)
IGNORE_KEY_PATTERNS = [re.compile(p) for p in (_DEFAULT_IGNORE + _EXTRA_IGNORE)]

_PLACEHOLDER_RE = re.compile(r"\{\{.*?\}\}|%\w|<[^>]+>")
_LATIN_LETTERS_RE = re.compile(r"[^A-Za-zÀ-ÿ]+")


def flatten_items(d: dict[str, Any], parent: str = "") -> dict[str, Any]:
    """Aplana un dict anidado a {clave.con.puntos: valor}."""
    out: dict[str, Any] = {}
    for k, v in d.items():
        nk = f"{parent}.{k}" if parent else k
        if isinstance(v, dict):
            out.update(flatten_items(v, nk))
        else:
            out[nk] = v
    return out


def load_items(path: str) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return flatten_items(json.load(f))


def _key_ignored(key: str) -> bool:
    return any(p.search(key) for p in IGNORE_KEY_PATTERNS)


def is_untranslated(key: str, base_val: Any, val: Any) -> bool:
    """True si `val` quedó como copia textual de la base (sin traducir)."""
    if not isinstance(val, str) or not isinstance(base_val, str):
        return False
    if val != base_val:
        return False
    if _key_ignored(key):
        return False
    # Quita placeholders/tags y deja sólo palabras con letras latinas.
    text = _PLACEHOLDER_RE.sub(" ", val)
    words = [w for w in _LATIN_LETTERS_RE.split(text) if len(w) >= 2]
    if not words:  # sólo símbolos/números/emojis → no es traducible
        return False
    # Si TODAS las palabras son marca/sigla/nombre propio → legítimo.
    real = [w for w in words if w.lower() not in ALLOW_TOKENS]
    return bool(real)


def _report(label: str, base_items: dict[str, Any], path: str) -> bool:
    """Compara un archivo de idioma contra la base. True si pasa el gate."""
    if not os.path.exists(path):
        print(f"    ❌ {label}: FALTA EL ARCHIVO")
        return False
    items = load_items(path)
    base_keys, keys = set(base_items), set(items)
    missing = base_keys - keys
    extra = keys - base_keys

    untranslated: list[str] = []
    if CHECK_UNTRANSLATED:
        untranslated = [
            k for k in base_keys & keys
            if is_untranslated(k, base_items[k], items[k])
        ]

    strict = label in NONLATIN_STRICT
    # El gate sólo lo rompen: claves faltantes/sobrantes, o sin-traducir en
    # idiomas no latinos (donde no hay falsos positivos).
    gate_ok = not missing and not extra and not (strict and untranslated)

    if not missing and not extra and not untranslated:
        print(f"    ✅ {label}: completo")
        return gate_ok

    pct = 100 * (len(base_keys) - len(missing)) / len(base_keys) if base_keys else 100.0
    bits = []
    if missing:
        bits.append(f"{len(missing)} faltan")
    if extra:
        bits.append(f"{len(extra)} sobran")
    if untranslated:
        tag = "SIN TRADUCIR" if strict else "posibles sin traducir (revisar)"
        bits.append(f"{len(untranslated)} {tag}")
    icon = "❌" if not gate_ok else "⚠️ "
    print(f"    {icon} {label}: {', '.join(bits)} ({pct:.1f}% claves)")

    if VERBOSE:
        for key in sorted(missing):
            print(f"         · falta:        {key}")
        for key in sorted(extra):
            print(f"         · sobra:        {key}")
        for key in sorted(untranslated):
            print(f"         · sin traducir: {key} = {base_items[key]!r}")
    return gate_ok


def audit_frontend() -> bool:
    base_dir = os.path.join(FRONTEND_DIR, BASE_LANG)
    if not os.path.isdir(base_dir):
        print(f"=== FRONTEND: no existe {base_dir}, omitido ===")
        return True
    namespaces = sorted(f for f in os.listdir(base_dir) if f.endswith(".json"))
    langs = sorted(
        d for d in os.listdir(FRONTEND_DIR)
        if os.path.isdir(os.path.join(FRONTEND_DIR, d)) and d != BASE_LANG
    )
    print(f"=== FRONTEND ({FRONTEND_DIR}) — base '{BASE_LANG}', "
          f"{len(langs)} idiomas, namespaces: {namespaces} ===")
    ok = True
    for ns in namespaces:
        base_items = load_items(os.path.join(base_dir, ns))
        print(f"\n  [{ns}] base = {len(base_items)} claves")
        for lng in langs:
            ok &= _report(lng, base_items, os.path.join(FRONTEND_DIR, lng, ns))
    return ok


def audit_backend() -> bool:
    base = os.path.join(BACKEND_DIR, f"{BASE_LANG}.json")
    if not os.path.exists(base):
        print(f"\n=== BACKEND: no existe {base}, omitido ===")
        return True
    base_items = load_items(base)
    langs = sorted(
        f[:-5] for f in os.listdir(BACKEND_DIR)
        if f.endswith(".json") and f != f"{BASE_LANG}.json"
    )
    print(f"\n=== BACKEND ({BACKEND_DIR}) — base '{BASE_LANG}' = "
          f"{len(base_items)} claves, {len(langs)} idiomas ===")
    ok = True
    for lng in langs:
        ok &= _report(lng, base_items, os.path.join(BACKEND_DIR, f"{lng}.json"))
    return ok


if __name__ == "__main__":
    fe = audit_frontend()
    be = audit_backend()
    if fe and be:
        print("\n✨ Todas las traducciones están sincronizadas y traducidas.")
        sys.exit(0)
    print("\n❌ Hay traducciones faltantes, sobrantes o sin traducir (ver arriba).")
    print("   Detalle por clave:  python scripts/check_translations.py -v")
    sys.exit(1)
