#!/usr/bin/env python3
"""Candado de la regla dura 2 (`.claude/rules/orquestacion.md`) para SUBAGENTES.

Hook `PreToolUse` sobre `Bash`: si el comando lo pide un subagente (la entrada trae
`agent_id`) y EJECUTA la suite completa o un proceso pesado, se deniega con el motivo.
La sesión principal pasa siempre: ella corre la suite con OK de {{OWNER}}. Falla ABIERTO:
un error del candado no puede bloquear todo `Bash`.

Límite honesto: lee el TEXTO del comando. Cubre los envoltorios corrientes (`uv run`, `bash -c`,
`npm --prefix`, rutas sin normalizar, heredoc hacia un shell), no a quien quiera esquivarlo
(un alias, un script propio, `make test`, variables).
"""
import json
import posixpath
import re
import shlex
import sys
from collections.abc import Iterator

# `npm run <x>` que solo son «todo» si van sin ruta (adaptá los nombres a tu package.json).
_NPM_COMPLETOS_SIN_RUTA = frozenset({"test", "test:ci", "test:e2e", "test:e2e:headed",
                                     "test:e2e:chromium", "test:e2e:firefox", "test:e2e:webkit"})
_SCRIPT_PESADO = re.compile(
    r"(run_stryker|run_mutmut|run_schemathesis|run_zap_dast|run_pytest_postgres|run_local_ci|check_coverage|run_flaky_check)\.sh$")
# Opciones de pytest que consumen el token siguiente (no es una ruta).
_PYTEST_CON_VALOR = frozenset({"-k", "-m", "-n", "-p", "-c", "-o", "-W", "--dist", "--maxfail",
                               "--tb", "--rootdir", "--durations", "--timeout", "--cov",
                               "--cov-report", "--cov-config", "--junitxml", "--basetemp",
                               "--ignore", "--deselect", "--numprocesses"})
# Con estas, pytest informa y no ejecuta ningún test.
_PYTEST_SOLO_INFORMA = frozenset({"--version", "-V", "--help", "-h", "--collect-only", "--co",
                                  "--fixtures", "--markers"})
_PREFIJOS = frozenset({"time", "env", "exec", "command", "nohup", "sudo", "xargs", "then", "do"})
_CORREDORES = frozenset({"uv", "poetry", "pipenv", "pdm", "hatch"})  # `uv run <comando>`
_SHELLS = frozenset({"bash", "sh", "zsh", "dash"})
_GESTORES_JS = frozenset({"npm", "pnpm", "yarn", "bun"})
_REDIRECCION = re.compile(r"(?:^|\s)\d*(?:>>?|<)&?(?:\d+\b|\s*[^\s]+)")


def _lineas_que_se_ejecutan(comando: str) -> Iterator[str]:
    """Descarta el cuerpo de un heredoc (texto que se escribe), salvo si lo recibe un shell."""
    fin, ejecuta = None, False
    for linea in comando.split("\n"):
        if fin is not None:
            if linea.strip() == fin:
                fin = None
            elif ejecuta:
                yield linea
            continue
        # `<<<` (here-string) y `$((1 << 2))` no abren un heredoc.
        marca = re.search(r"(?<!<)<<(?!<)-?\s*(['\"]?)([A-Za-z_]\w*)\1", linea)
        fin = marca.group(2) if marca else None
        if marca:
            toks = _tokens(re.split(r"[;&|]", linea[: marca.start()])[-1])
            ejecuta = bool(toks) and posixpath.basename(toks[0]) in _SHELLS
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
    tramo = _REDIRECCION.sub(" ", tramo.strip().lstrip("({ ").rstrip(")} "))
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
        elif toks[0] == "nice":
            toks = toks[3:] if toks[1:2] == ["-n"] else toks[1:]
        elif toks[0] in _CORREDORES and toks[1:2] == ["run"]:
            toks = toks[2:]
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


def _es_todo(ruta: str) -> bool:
    """`.`, `tests`, `./tests/`, `tests/../tests` o `/abs/…/tests`: recorre la suite entera."""
    normal = posixpath.normpath(ruta.split("::")[0])
    return normal == "." or posixpath.basename(normal) == "tests"


def _es_pesado(toks: list[str]) -> bool:
    cabeza = posixpath.basename(toks[0])
    if cabeza in _SHELLS | {"source", "."}:
        resto = toks[1:]
        while resto and resto[0].startswith("-"):
            if resto[0].endswith("c") and not resto[0].startswith("--") and len(resto) > 1:
                return motivo_de_bloqueo(resto[1]) is not None  # bash -c "<comando>"
            resto = resto[1:]
        if not resto:
            return False
        toks, cabeza = resto, posixpath.basename(resto[0])
    if cabeza == "eval":
        return motivo_de_bloqueo(" ".join(toks[1:])) is not None
    if _SCRIPT_PESADO.search(cabeza):
        return True
    if cabeza in ("npx", "bunx"):
        toks = [x for i, x in enumerate(toks[1:]) if i or not x.startswith("-")]
        while toks and toks[0].startswith("-"):
            toks = toks[1:]
        if not toks:
            return False
        cabeza = toks[0]
    if cabeza in _GESTORES_JS:
        args = toks[1:]
        while args and args[0].startswith("-"):  # `npm --prefix frontend test`
            args = args[2:] if args[0] in ("--prefix", "-C", "--dir", "--cwd") else args[1:]
        if args[:1] == ["exec"] or (args[:1] and args[0] in ("vitest", "playwright", "stryker")):
            args = [a for a in (args[1:] if args[0] == "exec" else args) if a != "--"]
            return bool(args) and _es_pesado(args)
        if args[:1] == ["run"]:
            args = args[1:]
        elif args[:1] not in (["test"], ["t"]):
            return False
        if not args:
            return False
        script = "test" if args[0] == "t" else args[0]
        return script in _NPM_COMPLETOS_SIN_RUTA and not _posicionales(args[1:], frozenset({"--prefix"}))
    if cabeza in ("stryker", "schemathesis") or (cabeza == "mutmut" and toks[1:2] == ["run"]):
        return True
    if cabeza == "vitest":
        if "--version" in toks or "--help" in toks:
            return False
        return not _posicionales(toks[1:])
    if cabeza == "playwright" and toks[1:2] == ["test"]:
        return not _posicionales(toks[2:])
    if cabeza == "coverage" and toks[1:2] == ["run"]:
        return "pytest" in toks and _es_pesado(toks[toks.index("pytest"):])
    if re.fullmatch(r"python(\d+(\.\d+)?)?", cabeza):
        if toks[1:2] == ["-mpytest"]:
            toks, cabeza = ["pytest", *toks[2:]], "pytest"
        elif toks[1:3] == ["-m", "pytest"]:
            toks, cabeza = toks[2:], "pytest"
        elif toks[1:3] == ["-m", "coverage"]:
            return _es_pesado(toks[2:])
    if cabeza in ("pytest", "py.test"):
        if _PYTEST_SOLO_INFORMA & set(toks[1:]):
            return False
        rutas = _posicionales(toks[1:], _PYTEST_CON_VALOR)
        return not rutas or any(_es_todo(r) for r in rutas)
    return False


def motivo_de_bloqueo(comando: str) -> str | None:
    """Devuelve el tramo que ejecuta la suite completa o un proceso pesado, o None."""
    for linea in _lineas_que_se_ejecutan(comando):
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
                f"`cd frontend && npx vitest run src/<carpeta>`. Ojo: `pytest tests/ -k <patrón>` "
                f"también recorre TODO (un patrón sobre el directorio entero no es una ruta); "
                f"para filtrar, pasá la lista explícita de archivos."),
        }}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
