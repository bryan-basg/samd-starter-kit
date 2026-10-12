#!/usr/bin/env python3
"""Candado de la regla dura 2 (`.claude/rules/orquestacion.md`) para SUBAGENTES.

Hook `PreToolUse` sobre `Bash`: si el comando lo pide un subagente (la entrada trae
`agent_id`) y EJECUTA la suite completa o un proceso pesado, se deniega con el motivo.
La sesión principal pasa siempre: ella corre la suite con OK de {{OWNER}}. Falla ABIERTO:
un error del candado no puede bloquear todo `Bash`.
"""
import json
import re
import shlex
import sys
from collections.abc import Iterator

# `npm run <x>` que solo son «todo» si van sin ruta (adaptá los nombres a tu package.json).
_NPM_COMPLETOS_SIN_RUTA = frozenset({"test", "test:ci", "test:e2e", "test:e2e:headed",
                                     "test:e2e:chromium", "test:e2e:firefox", "test:e2e:webkit"})
_SCRIPT_PESADO = re.compile(
    r"(run_stryker|run_mutmut|run_schemathesis|run_zap_dast|run_pytest_postgres|run_local_ci)\.sh$")
# Opciones de pytest que consumen el token siguiente (no es una ruta).
_PYTEST_CON_VALOR = frozenset({"-k", "-m", "-n", "-p", "-c", "-o", "-W", "--dist", "--maxfail",
                               "--tb", "--rootdir", "--durations", "--timeout", "--cov",
                               "--cov-report", "--junitxml", "--basetemp", "--ignore",
                               "--deselect"})
_RUTAS_QUE_SON_TODO = frozenset({"tests", "tests/", "./tests", "./tests/", "."})
_PREFIJOS = frozenset({"time", "nice", "env", "exec", "command"})
_REDIRECCION = re.compile(r"(?:^|\s)\d*(?:>>?|<)&?(?:\d+\b|\s*[^\s]+)")


def _lineas_sin_heredoc(comando: str) -> Iterator[str]:
    """Descarta el cuerpo de los heredoc: es texto que se escribe, no se ejecuta."""
    fin = None
    for linea in comando.split("\n"):
        if fin is not None:
            fin = None if linea.strip() == fin else fin
            continue
        marca = re.search(r"<<-?\s*['\"]?(\w+)['\"]?", linea)
        fin = marca.group(1) if marca else None
        yield linea


def _tramos(linea: str) -> Iterator[str]:
    """Parte una línea en `&&`, `||`, `;`, `|` y `&`, respetando las comillas."""
    tramo, comilla, i = "", None, 0
    while i < len(linea):
        c = linea[i]
        if comilla:
            comilla = None if c == comilla else comilla
        elif c in "'\"":
            comilla = c
        elif linea.startswith(("&&", "||"), i):
            yield tramo
            tramo, i = "", i + 2
            continue
        elif c in ";|" or (c == "&" and linea[i - 1:i] not in "<>" and linea[i + 1:i + 2] != ">"):
            yield tramo
            tramo, i = "", i + 1
            continue
        tramo += c
        i += 1
    yield tramo


def _tokens(tramo: str) -> list[str]:
    tramo = _REDIRECCION.sub(" ", tramo)
    try:
        toks = shlex.split(tramo)
    except ValueError:
        toks = tramo.split()
    # Quita asignaciones `X=y`, `timeout [-s SIG] N` y prefijos que no cambian el comando.
    while toks:
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", toks[0]) or toks[0] in _PREFIJOS:
            toks = toks[1:]
        elif toks[0] == "timeout":
            toks = toks[1:]
            while toks and toks[0].startswith("-"):
                toks = toks[2:] if toks[0] in ("-s", "-k", "--signal", "--kill-after") else toks[1:]
            toks = toks[1:]  # la duración
        else:
            break
    return toks


def _posicionales(args: list[str], con_valor: frozenset[str] = frozenset()) -> list[str]:
    sueltos: list[str] = []
    saltar = False
    for a in args:
        if saltar:
            saltar = False
        elif a in con_valor:
            saltar = True
        elif not a.startswith("-") and a != "run":
            sueltos.append(a)
    return sueltos


def _es_pesado(toks: list[str]) -> bool:
    cabeza = toks[0].rsplit("/", 1)[-1]
    if cabeza in ("bash", "sh") and len(toks) > 1:
        toks, cabeza = toks[1:], toks[1].rsplit("/", 1)[-1]
    if _SCRIPT_PESADO.search(cabeza):
        return True
    if cabeza == "npx" and len(toks) > 1:
        toks, cabeza = toks[1:], toks[1]
    if cabeza in ("stryker", "schemathesis") or (cabeza == "mutmut" and toks[1:2] == ["run"]):
        return True
    if cabeza == "npm":
        if toks[1:2] == ["test"]:
            script, resto = "test", toks[2:]
        elif toks[1:2] == ["run"] and len(toks) > 2:
            script, resto = toks[2], toks[3:]
        else:
            return False
        return script in _NPM_COMPLETOS_SIN_RUTA and not _posicionales(resto)
    if cabeza == "vitest":
        return not _posicionales(toks[1:])
    if cabeza == "playwright" and toks[1:2] == ["test"]:
        return not _posicionales(toks[2:])
    if cabeza in ("python", "python3") and toks[1:3] == ["-m", "pytest"]:
        toks, cabeza = toks[2:], "pytest"
    if cabeza == "pytest":
        rutas = _posicionales(toks[1:], _PYTEST_CON_VALOR)
        return not rutas or all(r in _RUTAS_QUE_SON_TODO for r in rutas)
    return False


def motivo_de_bloqueo(comando: str) -> str | None:
    """Devuelve el tramo que ejecuta la suite completa o un proceso pesado, o None."""
    for linea in _lineas_sin_heredoc(comando):
        for tramo in _tramos(linea):
            toks = _tokens(tramo.strip())
            if toks and _es_pesado(toks):
                return tramo.strip()
    return None


def main() -> int:
    try:
        entrada = json.load(sys.stdin)
        if not entrada.get("agent_id"):
            return 0
        tramo = motivo_de_bloqueo(entrada.get("tool_input", {}).get("command", ""))
    except Exception:  # falla abierto: ver docstring
        return 0
    if tramo:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"⛔ Candado de la regla dura 2 (.claude/rules/orquestacion.md): un subagente corre "
                f"SOLO los tests de su directorio o archivo, nunca la suite completa ni procesos "
                f"pesados (mutación, fuzz, E2E completa, tier de BD real). Bloqueado: "
                f"`{tramo[:160]}`. La suite entera la corre el orquestador una vez, al final. "
                f"Usá tu directorio, p. ej. `pytest tests/test_<modulo>*.py -q` o "
                f"`cd frontend && npx vitest run src/<carpeta>`. Ojo: `pytest tests/ -k` y "
                f"`npm test -- <archivo>` también recorren TODO; para filtrar, pasá "
                f"la lista explícita de archivos en vez de un patrón sobre el directorio entero."),
        }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
