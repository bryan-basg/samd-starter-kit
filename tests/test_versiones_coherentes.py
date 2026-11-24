"""Guardián: una sola versión X.Y de Python y un solo major de Node en todo el kit (SOUP §8).

Un PR que subía SOLO el `FROM` del Dockerfile (3.12 → 3.15) salía verde sin haber probado nada:
el CI corre con la versión de `setup-python` y ningún job construye la imagen. Ahora la
versión se sube en todos los sitios a la vez, y entonces el verde del CI sí la probó.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _uno(ruta: str, patron: str) -> str:
    hallado = re.search(patron, (ROOT / ruta).read_text(encoding="utf-8"), flags=re.M)
    assert hallado, f"{ruta}: no encuentro la versión con {patron!r}"
    return hallado.group(1)


def _en_workflows(clave: str) -> dict[str, str]:
    patron = re.compile(rf"""{clave}:\s*['"]?([\d.]+)""")
    return {
        f"{wf.name}#{i}": version
        for wf in sorted((ROOT / ".github" / "workflows").glob("*.yml"))
        for i, version in enumerate(patron.findall(wf.read_text(encoding="utf-8")))
    }


def test_una_sola_version_de_python() -> None:
    sitios = _en_workflows("python-version")
    assert len(sitios) >= 5, sitios  # el detector no aprueba por vacío
    sitios["Dockerfile"] = _uno("Dockerfile", r"^FROM python:(\d+\.\d+)")
    sitios[".mypy.ini"] = _uno(".mypy.ini", r"^python_version\s*=\s*([\d.]+)")
    mayor, menor = re.match(r"(\d)(\d+)", _uno("pyproject.toml", r"target-version\s*=\s*\"py(\d+)\"")).groups()
    sitios["pyproject.toml"] = f"{mayor}.{menor}"
    sitios[".devcontainer"] = _uno(
        ".devcontainer/devcontainer.json", r"devcontainers/python:[\d.]*-(\d+\.\d+)"
    )
    assert len(set(sitios.values())) == 1, sitios


def test_un_solo_major_de_node() -> None:
    sitios = _en_workflows("node-version")
    assert len(sitios) >= 3, sitios
    sitios["docker-compose.yml"] = _uno("docker-compose.yml", r"image:\s*node:(\d+)")
    sitios[".devcontainer"] = _uno(
        ".devcontainer/devcontainer.json", r"features/node:\d+\"\s*:\s*\{\s*\"version\":\s*\"(\d+)"
    )
    paquete = json.loads((ROOT / "frontend" / "package.json").read_text(encoding="utf-8"))
    sitios["engines"] = re.sub(r"\D*(\d+).*", r"\1", paquete["engines"]["node"])
    sitios["@types/node"] = re.sub(r"\D*(\d+).*", r"\1", paquete["devDependencies"]["@types/node"])
    assert len({v.split(".")[0] for v in sitios.values()}) == 1, sitios
