#!/usr/bin/env python3
"""Vigía SaMD (IEC 62304 §5.7, §8): registra cambios en módulos clínicos y entrega la regla de la capa.

Hook `PostToolUse` sobre `Bash|Edit|Write|MultiEdit|NotebookEdit`. Mira QUÉ CAMBIÓ EN EL
DISCO (`git status` + fecha de cada archivo), no qué herramienta lo escribió. La versión
anterior solo escuchaba Edit/Write: en el proyecto de referencia quedó MUDA varios días
cuando el trabajo pasó a la terminal (`sed`, `python`, heredocs), y nadie lo notó porque
un vigía que no ve nada parece un vigía sin novedades (SCMP v1.20).

De los mismos cambios salen dos cosas:

1. una línea en `.claude/audit_clinical_changes.log` (fecha ISO UTC, herramienta, ruta,
   patrón) por cada archivo clínico/crítico cambiado — local, `*.log` está en `.gitignore`:
   es el diario de guardia de la máquina, no un registro del DHF;
2. un recordatorio de trazabilidad por `additionalContext` (el canal que el agente SÍ lee;
   un `print` a stderr con salida 0 solo lo ve el humano en modo detallado) y, si el cambio
   vino por TERMINAL, el texto de la regla por capa (`.claude/rules/*.md` con `paths:`),
   una vez por conversación y agente. Las de Read/Edit ya las carga Claude Code solo.

NO bloquea nada y no calla: si el propio vigía falla, lo anota en la bitácora Y se lo dice
al agente. Contrato: `tests/test_audit_clinical_log.py` (corre el script real sobre un
repositorio de juguete).
"""
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ⚠️ Lección del proyecto de referencia: su lista era CIEGA en 4 de 10 entradas (carpetas
# renombradas o que nunca existieron) y no registró nada de lo que más importaba. Un
# detector que no encuentra nada no está limpio: está ciego. Por eso cada patrón tiene
# que casar con un archivo REAL — lo exige el test. Al adaptar el kit, poné acá los
# módulos de clase B/C de `docs/07_regulatory_and_compliance/CRITICAL_MODULES_INVENTORY.md`
# (scoring, red de crisis, auth, auditoría, modelos y migraciones) y borrá los del esqueleto.
# Si tu proyecto declara la lista de mutación crítica en un archivo (JSON de mutmut, `mutate`
# de una config de Stryker), derivá los patrones de ahí en `patrones_clinicos()`: copiarla
# a mano es la receta para que las dos listas se separen.
CLINICAL_PATTERNS = [
    r"app/core/encryption",  # cifrado de PHI en reposo
    r"app/core/security",  # JWT / identidad
    r"app/core/config\.py",  # secretos y guard de claves de dev
    r"app/main\.py",  # fail-safe global y log sin PHI
    r"app/routers/notes",  # endpoint que guarda contenido del usuario (PHI)
    r"app/schemas",  # frontera de validación de los datos de entrada
]

RECORDATORIO = (
    "[SaMD vigía] Cambio en módulo clínico/crítico{estado}. Antes de declarar cerrado: "
    "docs/08_verification_and_audits/TECHNICAL_DEBT_SUMMARY.md, "
    "docs/07_regulatory_and_compliance/ISO_14971_RISK_MATRIX.md (si toca seguridad) y "
    "docs/00_master/MASTER_MAP.md; y análisis de impacto (/samd-trace)."
)

_TOPE_CONTEXTO = 9_500  # Claude Code recorta `additionalContext` en 10.000 caracteres.
_MARGEN_PRIMERA_VEZ = 120.0  # segundos hacia atrás la primera vez que se mira un árbol
_HOLGURA = 2.0  # segundos entre el fin del comando y el arranque del hook
_COPIA = re.compile(r"\.claude/worktrees/[\w.-]+")


def _git(raiz: Path, *args: str) -> str:
    return subprocess.run(["git", "--no-optional-locks", "-C", str(raiz), *args], capture_output=True,
                          text=True, errors="replace", timeout=4, check=True).stdout  # varias llamadas dentro del tope del hook


def _glob_a_regex(glob: str) -> str:
    """Traduce el subconjunto de globs que usan las reglas: `**`, `*` y `{a,b}`."""
    partes = re.split(r"(\*\*/|\*\*|\*|\{[^}]*\})", glob)
    traduccion = {"**/": "(?:.*/)?", "**": ".*", "*": "[^/]*"}
    salida = ""
    for parte in partes:
        if parte.startswith("{"):
            salida += "(?:" + "|".join(re.escape(x) for x in parte[1:-1].split(",")) + ")"
        else:
            salida += traduccion.get(parte, re.escape(parte))
    return f"^{salida}$"


def patrones_clinicos(principal: Path) -> list[str]:
    """Hoy, la lista escrita a mano. Punto único para sumarle listas derivadas (ver arriba)."""
    del principal  # se usa al derivar de los archivos de mutación del proyecto adoptante
    return list(CLINICAL_PATTERNS)


def patron_clinico(rel: str, patrones: list[str]) -> str | None:
    return next((p for p in patrones if re.search(p, rel)), None)


def reglas_por_capa(principal: Path) -> dict[str, tuple[list[str], str]]:
    """{nombre: (regex de sus `paths:`, texto)} leídas del frontmatter: no se copian acá."""
    reglas: dict[str, tuple[list[str], str]] = {}
    for archivo in sorted((principal / ".claude/rules").glob("*.md")):
        partes = archivo.read_text("utf-8").split("---\n", 2)
        if len(partes) < 3 or partes[0].strip() or "paths:" not in partes[1]:
            continue
        globs = re.findall(r'^\s*-\s*"([^"]+)"', partes[1], re.M)
        reglas[archivo.name] = ([_glob_a_regex(g) for g in globs], partes[2].strip())
    return reglas


def _carpeta_git(raiz: Path) -> Path:
    """La carpeta `.git` común: la comparten el árbol principal y sus copias de trabajo."""
    return (raiz / _git(raiz, "rev-parse", "--git-common-dir").strip()).resolve()


def _existente(ruta: Path) -> Path:
    """La carpeta existente más cercana (un archivo o carpeta borrados no tienen `git -C`)."""
    for candidata in (ruta, *ruta.parents):
        if candidata.is_dir():
            return candidata
    return Path(".")


def _raices(entrada: dict[str, Any], principal: Path) -> list[Path]:
    """El árbol donde corrió la herramienta, el del archivo editado y las copias de trabajo que nombra."""
    datos = entrada.get("tool_input") or {}
    editados = [str(datos[k]) for k in ("file_path", "notebook_path") if datos.get(k)]
    texto = " ".join([str(datos.get("command", "")), *editados])
    cwd = Path(entrada.get("cwd") or ".")
    candidatas = [cwd, principal]
    candidatas += [_existente((cwd / e).parent) for e in editados]  # Edit en una copia de trabajo de afuera
    candidatas += [principal / c for c in _COPIA.findall(texto)]
    comun = _carpeta_git(principal)
    raices: list[Path] = []
    for c in candidatas:
        try:
            raiz = Path(_git(c, "rev-parse", "--show-toplevel").strip())
        except (subprocess.SubprocessError, OSError):
            continue  # una carpeta fuera de git (p. ej. /tmp) no es un árbol que vigilar
        if raiz not in raices and _carpeta_git(raiz) == comun:
            raices.append(raiz)
    return raices


def cambios_sin_commit(raiz: Path, borrados_vistos: set[str], ahora: float) -> tuple[list[tuple[str, float]], set[str]]:
    """(archivo, instante del último cambio) de todo lo que está sin commit, y los borrados actuales.

    Un borrado no tiene fecha propia: la de su carpeta cambia cada vez que se toca OTRO archivo
    de ahí, y si se borró la carpeta entera no hay nada que mirar. Por eso un borrado cuenta
    como «ahora» la primera vez que se ve y nunca más, mientras siga borrado.
    """
    crudo = _git(raiz, "status", "--porcelain", "-uall", "--no-renames", "-z", "--", ".",
                 ":(exclude).claude/worktrees")
    cambios: list[tuple[str, float]] = []
    borrados: set[str] = set()
    for item in filter(None, crudo.split("\0")):
        rel = item[3:]
        ruta = raiz / rel
        if ruta.exists() or ruta.is_symlink():
            # ctime y no mtime: `mv` y `cp -p` conservan la fecha de contenido.
            cambios.append((rel, ruta.lstat().st_ctime))
        else:
            borrados.add(rel)
            cambios.append((rel, 0.0 if rel in borrados_vistos else ahora))
    return cambios, borrados


_REGISTRADOS: list[str] = []  # lo que esta corrida ya dejó en la bitácora (para no mentir si algo falla después)


def _registrar(principal: Path, herramienta: str, rel: str, motivo: str) -> None:
    bitacora = principal / ".claude/audit_clinical_changes.log"
    bitacora.parent.mkdir(parents=True, exist_ok=True)
    with open(bitacora, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()}\t{herramienta}\t{rel}\t{motivo}\n")
    _REGISTRADOS.append(rel)


def _contexto(principal: Path, estado: Path, entrada: dict[str, Any], quien: str,
              cambios: set[str], clinicos: set[str], fallo_bitacora: str) -> str:
    vistas = estado / f"vistas-{quien}"
    ya = set(vistas.read_text("utf-8").split()) if vistas.exists() else set()
    avisos: list[str] = []
    textos: list[str] = []
    nuevos = sorted(c for c in clinicos if f"clinico:{c}" not in ya)  # uno por archivo, no uno por sesión
    nombres = ", ".join(nuevos[:5]) + (f" y {len(nuevos) - 5} más" if len(nuevos) > 5 else "")
    if fallo_bitacora:  # nunca se calla, aunque ya se haya avisado antes
        avisos.append(RECORDATORIO.format(estado=f" ({nombres or 'ver git status'}) — LA BITÁCORA NO SE PUDO "
                                                 f"ESCRIBIR ({fallo_bitacora}), anotalo a mano"))
    elif nuevos:
        ya.update(f"clinico:{c}" for c in nuevos)
        avisos.append(RECORDATORIO.format(estado=f" registrado ({nombres})"))
    for nombre, (regexes, texto) in reglas_por_capa(principal).items():
        if nombre in ya or not any(re.match(r, c) for r in regexes for c in cambios):
            continue
        ya.add(nombre)
        if entrada.get("tool_name") != "Bash":
            continue  # Read/Edit ya hicieron que Claude Code cargara la regla
        if sum(map(len, textos)) + len(texto) < _TOPE_CONTEXTO - 700:
            textos.append(f"Regla de la capa que tocaste por terminal (.claude/rules/{nombre}):\n{texto}")
        else:
            avisos.append(f"Tocaste una capa con reglas duras: leé AHORA .claude/rules/{nombre}.")
    vistas.write_text("\n".join(sorted(ya)), "utf-8")
    return "\n\n".join(avisos + textos)


def _limpiar(estado: Path) -> None:
    """Borra el estado de más de 7 días. Dos hooks a la vez pueden pisarse: no es un fallo."""
    for vieja in estado.iterdir():
        try:
            if vieja.stat().st_mtime < time.time() - 7 * 86_400:
                vieja.unlink(missing_ok=True)
        except FileNotFoundError:
            pass


def revisar(entrada: dict[str, Any], principal: Path) -> str:
    """Registra lo clínico que cambió y devuelve el contexto a entregar ('' si nada)."""
    estado = _carpeta_git(principal) / "samd-vigia"
    estado.mkdir(exist_ok=True)
    _limpiar(estado)
    quien = re.sub(r"[^\w-]", "", f"{entrada.get('session_id')}-{entrada.get('agent_id', 'main')}")
    patrones = patrones_clinicos(principal)
    ahora = time.time()  # se toma ANTES de mirar: lo que cambie mientras miro entra en la próxima
    inicio = ahora - float(entrada.get("duration_ms") or 0) / 1000 - _HOLGURA
    propios: set[str] = set()
    clinicos: set[str] = set()
    fallo_bitacora = ""
    for raiz in _raices(entrada, principal):
        arbol = re.sub(r"\W+", "_", str(raiz))
        marca, lista_borrados = estado / f"marca-{arbol}", estado / f"borrados-{arbol}"
        # La bitácora es de todos: cada cambio, una línea. La regla es solo para quien escribía
        # en ese momento: lo que otra ventana tocó antes no cuenta.
        desde = marca.stat().st_mtime if marca.exists() else inicio - _MARGEN_PRIMERA_VEZ
        vistos = set(lista_borrados.read_text("utf-8").splitlines()) if lista_borrados.exists() else set()
        cambios, borrados = cambios_sin_commit(raiz, vistos, ahora)
        fallo_aca = ""
        for rel, instante in cambios:
            motivo = patron_clinico(rel, patrones)
            if motivo and instante > desde:
                try:
                    _registrar(principal, str(entrada.get("tool_name", "?")),
                               os.path.relpath(raiz / rel, principal), motivo)
                except OSError as exc:  # la edición sigue, pero sin fingir que quedó anotada
                    fallo_aca = fallo_bitacora = type(exc).__name__
            if instante > inicio:
                propios.add(rel)
                if motivo:
                    clinicos.add(rel)
        if not fallo_aca:  # la marca avanza solo si todo quedó escrito: repetir antes que perder
            lista_borrados.write_text("\n".join(sorted(borrados)), "utf-8")
            marca.touch()
            os.utime(marca, (ahora, ahora))
    if not propios and not fallo_bitacora:
        return ""
    return _contexto(principal, estado, entrada, quien, propios, clinicos, fallo_bitacora)


def _emitir(contexto: str) -> None:
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                             "additionalContext": contexto}}, ensure_ascii=False))


def main() -> int:
    aqui = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
    principal = aqui
    try:
        principal = _carpeta_git(aqui).parent  # desde una copia de trabajo, la bitácora es la misma
    except (subprocess.SubprocessError, OSError):
        return 0  # sin repositorio git no hay `git status` que mirar: el kit se adopta con git
    try:
        contexto = revisar(json.load(sys.stdin), principal)
    except Exception as e:  # no frena el trabajo, pero deja rastro y avisa: callar es lo peor
        detalle = f"{type(e).__name__}: {str(e)[:200]}".replace("\n", " ")
        try:
            _registrar(principal, "ERROR", type(e).__name__, detalle)
        except OSError:
            pass
        if any(r != type(e).__name__ for r in _REGISTRADOS):
            estado = ("lo clínico SÍ quedó en la bitácora, pero no pudo entregarse el recordatorio ni la regla "
                      "de la capa: revisá la trazabilidad a mano")
        else:
            estado = "este cambio NO quedó registrado. Revisá la trazabilidad a mano y avisá al dueño"
        _emitir(f"[SaMD vigía] El vigía de cambios clínicos falló ({detalle}): {estado}.")
        return 0
    if contexto:
        _emitir(contexto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
