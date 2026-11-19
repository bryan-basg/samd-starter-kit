#!/usr/bin/env python3
"""Veredicto de `npm audit` al umbral `high`, con tolerados nombrados y con fecha.

Rojo si queda un aviso high/critical sin tolerar, si un tolerado caducó o ya no
aparece, o si el informe no se puede leer. Corre `npm audit` él mismo para
juzgar su exit code sin `|| true` en el workflow (`security-audit.yml`, job
`npm-audit`).

Por qué un guion y no `npm audit --audit-level=high` a secas: a secas, la única
salida ante un aviso SIN parche es apagar el paso entero (`|| true`), y el
escaneo deja de poder rojear para siempre. Acá la excepción es por aviso, con
motivo escrito y fecha de caducidad: vencida, vuelve a rojear sola.

Portado del proyecto de referencia (sync 2026-11-16). Contrato en
`tests/test_ci_npm_audit_veredicto.py`.
"""

from __future__ import annotations

import argparse
import json
import os
# `subprocess` corre solo `npm audit` con argumentos literales, sin shell ni entrada externa.
import subprocess  # nosec B404
import sys
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

UMBRAL = "high"
SEVERIDADES_QUE_FRENAN = frozenset({"high", "critical"})


@dataclass(frozen=True)
class Tolerado:
    paquete: str
    caduca: date
    motivo: str


# Clave: id GHSA del aviso. Cada uno lleva fecha de caducidad: vencida, rojea.
# Al tolerar uno, escribí el porqué (por qué no hay parche y por qué el fallo no
# alcanza a tu producto) y una fecha a ≤ 90 días — el test lo exige. Ejemplo:
#
#     "<id GHSA del aviso>": Tolerado(
#         paquete="<paquete>",
#         caduca=date(AAAA, MM, DD),
#         motivo="El parche solo existe en la major siguiente y migrar cambia ...",
#     ),
# Vacío desde el 2026-11-19: GHSA-fc5q-39xc-vjpf (picomatch) dejó de informarse en `npm audit`.
TOLERADOS: Dict[str, Tolerado] = {}


def avisos_que_frenan(informe: object) -> Dict[str, str]:
    """GHSA → paquete de cada aviso raíz high/critical del informe."""
    if not isinstance(informe, dict) or not isinstance(informe.get("vulnerabilities"), dict):
        raise ValueError("el informe no tiene la forma de `npm audit --json` (falta `vulnerabilities`)")
    avisos: Dict[str, str] = {}
    for nodo in informe["vulnerabilities"].values():
        for via in nodo.get("via", []):
            if isinstance(via, dict) and via.get("severity") in SEVERIDADES_QUE_FRENAN:
                avisos[str(via["url"]).rsplit("/", 1)[-1]] = str(via["name"])
    return avisos


def juzgar(
    informe: object,
    exit_npm: int,
    hoy: date,
    tolerados: Dict[str, Tolerado],
) -> Tuple[List[str], List[str]]:
    """Devuelve (fallos, tolerados_aplicados). Sin fallos = verde."""
    avisos = avisos_que_frenan(informe)
    # Anti-ciego: npm y este parser tienen que coincidir en si hay algo que frena.
    if (exit_npm != 0) != bool(avisos):
        return [
            f"`npm audit` salió {exit_npm} y el informe trae {len(avisos)} aviso(s) "
            f"high/critical: no coinciden, el veredicto no puede fiarse del informe."
        ], []
    fallos: List[str] = []
    aplicados: List[str] = []
    for ghsa, tolerado in sorted(tolerados.items()):
        if hoy > tolerado.caduca:
            fallos.append(
                f"El tolerado {ghsa} ({tolerado.paquete}) caducó el {tolerado.caduca}: "
                "revisá si ya hay parche y renová o borrá la excepción."
            )
        elif ghsa not in avisos:
            fallos.append(f"El tolerado {ghsa} ({tolerado.paquete}) ya no aparece: borralo de TOLERADOS.")
        else:
            aplicados.append(f"{ghsa} ({tolerado.paquete}) tolerado hasta el {tolerado.caduca}")
    vigentes = {ghsa for ghsa, t in tolerados.items() if hoy <= t.caduca}
    for ghsa, paquete in sorted(avisos.items()):
        if ghsa not in vigentes:
            fallos.append(f"{ghsa} ({paquete}): aviso high/critical sin tolerar.")
    return fallos, aplicados


def ejecutar_npm_audit() -> Tuple[str, int]:
    # `npm` lo pone `setup-node` en el PATH del runner; el argv es fijo.
    proceso = subprocess.run(  # nosec B603 B607
        ["npm", "audit", "--json", f"--audit-level={UMBRAL}"],
        capture_output=True,
        text=True,
        check=False,
    )
    return proceso.stdout, proceso.returncode


def _resumen(lineas: List[str]) -> None:
    texto = "\n".join(lineas)
    print(texto)
    destino = os.environ.get("GITHUB_STEP_SUMMARY")
    if destino:
        with open(destino, "a", encoding="utf-8") as fh:
            fh.write(texto + "\n")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--informe", required=True, help="Dónde guardar el JSON de npm audit (artefacto).")
    args = parser.parse_args(argv)

    salida, exit_npm = ejecutar_npm_audit()
    Path(args.informe).write_text(salida, encoding="utf-8")
    try:
        informe = json.loads(salida)
        fallos, aplicados = juzgar(informe, exit_npm, datetime.now(timezone.utc).date(), TOLERADOS)
    except (json.JSONDecodeError, ValueError, KeyError) as exc:
        _resumen([f"❌ npm audit: el informe no se puede juzgar ({type(exc).__name__}: {exc})."])
        return 1

    lineas = ["### npm audit — veredicto", ""]
    lineas += [f"* ⚠️ {a}" for a in aplicados]
    if fallos:
        _resumen(lineas + [f"* ❌ {f}" for f in fallos])
        return 1
    _resumen(lineas + [f"* ✅ 0 avisos {'/'.join(sorted(SEVERIDADES_QUE_FRENAN))} sin tolerar."])
    return 0


if __name__ == "__main__":
    sys.exit(main())
