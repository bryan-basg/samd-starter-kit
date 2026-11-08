"""Guardián de la cadena de suministro del CI (IEC 62304 §8 — SOUP, §5.7).

Una acción escrita como `actions/checkout@v4` no apunta a un código concreto: apunta a
una ETIQUETA, y una etiqueta la mueve su dueño cuando quiere. Quien controle ese
repositorio —o quien le robe la cuenta— puede reapuntar `v4` a otro commit y el CI de
este proyecto ejecuta ese código en la siguiente corrida, sin que nadie apruebe nada y
sin rastro en el diff. Es el vector que se cobró `tj-actions/changed-files` en marzo
de 2025. Un SHA de 40 caracteres no se puede mover: nombra un commit y solo ese.

La regla vive en prosa en `.claude/rules/github-actions.md`; una regla en prosa que
nada vigila se erosiona en silencio. Este archivo es el guardián que la hace cumplir.

El conjunto se DERIVA de los workflows en disco, no de una lista escrita a mano: un
workflow nuevo entra en la comprobación por existir, sin que nadie tenga que acordarse
de apuntarlo.
"""

import re
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"

# El kit trae 46 referencias remotas. Piso del detector: ajustalo hacia abajo SOLO si tu
# proyecto adaptado realmente usa menos acciones; su único trabajo es no aprobar por vacío.
MINIMO_DE_REFERENCIAS = 5

# `uses: <owner>/<repo>[/<subpath>]@<ref>` — se captura acción y referencia.
_USES = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)\s*(?:#.*)?$", re.MULTILINE)
_SHA = re.compile(r"^[0-9a-f]{40}$")
_PIN_SIN_COMENTARIO = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+@[0-9a-f]{40})\s*$")


def _archivos() -> list[Path]:
    return sorted(WORKFLOWS.glob("*.yml")) + sorted(WORKFLOWS.glob("*.yaml"))


def _referencias() -> list[tuple[Path, str, str]]:
    """(archivo, acción, referencia) de cada `uses:` de un repositorio REMOTO.

    Se ignoran las acciones locales (`./.github/...`) y las de contenedor
    (`docker://`), que no se resuelven por etiqueta de git.
    """
    salida: list[tuple[Path, str, str]] = []
    for wf in _archivos():
        for bruto in _USES.findall(wf.read_text(encoding="utf-8")):
            valor = bruto.strip().strip("\"'")
            if valor.startswith(("./", "docker://")) or "@" not in valor:
                continue
            accion, _, ref = valor.rpartition("@")
            salida.append((wf, accion, ref))
    return salida


def test_hay_workflows_que_examinar():
    """Integridad del detector: no puede aprobar por no haber mirado nada.

    Todo lo que afirma este archivo tiene forma de «ninguna acción incumple», y eso es
    trivialmente cierto sobre una lista vacía. Si el glob deja de encontrar workflows
    (carpeta renombrada, patrón que no casa), los demás tests pasarían en verde sin
    haber leído una línea.
    """
    refs = _referencias()
    assert len(refs) >= MINIMO_DE_REFERENCIAS, (
        f"Solo se encontraron {len(refs)} referencias `uses:` en {WORKFLOWS}. "
        "El detector no está leyendo los workflows y los demás tests de este archivo "
        "estarían midiendo el vacío."
    )


def test_toda_accion_esta_pineada_a_un_sha_completo():
    """Ninguna referencia por etiqueta (`@v4`) ni por rama (`@main`)."""
    sueltas = [
        f"{wf.name}: {accion}@{ref}"
        for wf, accion, ref in _referencias()
        if not _SHA.match(ref)
    ]
    assert not sueltas, (
        "Estas acciones se referencian por una etiqueta o rama, que su dueño puede mover "
        "a otro commit en cualquier momento — y el CI de este proyecto lo ejecutaría en "
        "la siguiente corrida sin aprobación ni rastro en el diff:\n  - "
        + "\n  - ".join(sorted(sueltas))
        + "\n\nPinealas al SHA de 40 caracteres del commit, dejando la versión legible "
        "en un comentario: `uses: actions/checkout@<sha> # v4.2.2`."
    )


def test_cada_accion_usa_una_sola_version_en_todo_el_repo():
    """Dos pines distintos de la misma acción es drift, no seguridad.

    Pinear protege de que muevan la etiqueta; no protege de que el repo acabe ejecutando
    tres versiones distintas de `setup-python` según el workflow que toque.
    """
    por_accion: dict[str, set[str]] = defaultdict(set)
    for _, accion, ref in _referencias():
        if _SHA.match(ref):
            por_accion[accion].add(ref)

    divergentes = {a: sorted(s) for a, s in por_accion.items() if len(s) > 1}

    # Divergencias toleradas HOY, cada una con su motivo. Vacío en el kit: o se unifica,
    # o se declara acá por escrito (así lo que falta unificar no vive solo en una cabeza).
    toleradas: set[str] = set()

    nuevas = {a: v for a, v in divergentes.items() if a not in toleradas}
    assert not nuevas, (
        "Estas acciones aparecen pineadas a SHA DISTINTOS en distintos workflows, y eso "
        "no estaba declarado:\n  - "
        + "\n  - ".join(f"{a}: {v}" for a, v in sorted(nuevas.items()))
        + "\n\nUnificá al mismo pin, o añadila a `toleradas` con su motivo."
    )

    # Y que las toleradas sigan siéndolo: una excepción que sobrevive a su motivo es la
    # que nadie vuelve a revisar.
    ya_unificadas = [a for a in toleradas if a in por_accion and a not in divergentes]
    assert not ya_unificadas, f"{ya_unificadas} ya no divergen: quitalas de `toleradas`."


def test_el_pin_lleva_la_version_legible_al_lado():
    """Un SHA a secas es incorruptible pero ilegible.

    Sin el comentario nadie sabe si el SHA es la v4 o la v2, y actualizarlo exige salir a
    internet a resolverlo. La convención es `@<sha> # <version>`; esto la mantiene.
    """
    sin_comentario = [
        f"{wf.name}:{numero}: {m.group(1)}"
        for wf in _archivos()
        for numero, linea in enumerate(wf.read_text(encoding="utf-8").splitlines(), 1)
        if (m := _PIN_SIN_COMENTARIO.match(linea))
    ]
    assert not sin_comentario, (
        "Estos pines no dicen a qué versión corresponden:\n  - "
        + "\n  - ".join(sin_comentario)
        + "\n\nAñadí ` # vX.Y.Z` al final de la línea."
    )


# `FROM [--platform=...] <imagen> [AS <etapa>]`; se ignora `FROM scratch`. Un `FROM <etapa previa>` de un build multi-etapa saldría como suelto: ajustá el patrón si lo adoptás.
_FROM = re.compile(r"^FROM\s+(?:--\S+\s+)*(?!scratch\b)(\S+)", re.MULTILINE)


def _imagenes_de_contenedor() -> list[tuple[str, str]]:
    """(origen, imagen) de `container:`/`services.*.image` de cada job y del `FROM` de cada Dockerfile."""
    salida: list[tuple[str, str]] = []
    for wf in _archivos():
        jobs = (yaml.safe_load(wf.read_text(encoding="utf-8")) or {}).get("jobs") or {}
        for nombre, job in jobs.items():
            cont = job.get("container")
            if cont:
                imagen = cont if isinstance(cont, str) else cont.get("image")
                salida.append((f"{wf.name}:{nombre}:container", imagen))
            for svc, datos in (job.get("services") or {}).items():
                salida.append((f"{wf.name}:{nombre}:services.{svc}", datos["image"]))
    # La imagen base de cada Dockerfile del repo: es la que se construye y despliega.
    for df in sorted(ROOT.glob("Dockerfile*")):
        for imagen in _FROM.findall(df.read_text(encoding="utf-8")):
            salida.append((f"{df.name}:FROM", imagen))
    return salida


def test_hay_imagenes_de_contenedor_que_examinar():
    """El detector de imágenes no puede aprobar por vacío (el kit trae semgrep, pgvector y el Dockerfile)."""
    assert len(_imagenes_de_contenedor()) >= 3
    assert any(donde.startswith("Dockerfile") for donde, _ in _imagenes_de_contenedor())


def test_toda_imagen_de_contenedor_esta_pineada_a_digest():
    """`semgrep/semgrep` o `pgvector:pg16` son etiquetas mutables: mismo vector que `@v4`.

    Su dueño reapunta la etiqueta y el CI ejecuta otra imagen sin que cambie el diff. Se
    exige `@sha256:<64 hex>`; la etiqueta legible puede quedar al lado (`imagen:tag@sha256:...`).
    """
    sueltas = [
        f"{donde}: {imagen}"
        for donde, imagen in _imagenes_de_contenedor()
        if not re.search(r"@sha256:[0-9a-f]{64}$", imagen)
    ]
    assert not sueltas, (
        "Imágenes de contenedor sin digest:\n  - "
        + "\n  - ".join(sueltas)
        + "\n\nPinealas con `imagen:tag@sha256:<digest>` (digest del índice multi-arquitectura)."
    )
