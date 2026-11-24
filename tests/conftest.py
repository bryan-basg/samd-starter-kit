"""Fixtures compartidas + aislamiento de estado global (regla dura del kit).

`app/` se importa DENTRO de las fixtures: los guardianes del kit no la usan y tienen que seguir
corriendo cuando borrás el ejemplo. Solo se tolera que el módulo NO EXISTA; si existe y está
roto, el import falla y los tests rojean.
"""

from importlib.util import find_spec

import pytest


def _existe(modulo: str) -> bool:
    try:
        return find_spec(modulo) is not None
    except ModuleNotFoundError:  # falta un paquete padre
        return False


@pytest.fixture(autouse=True)
def _reset_store():
    """Cada test arranca con el store vacío y lo limpia al salir (sin fugas)."""
    if not _existe("app.routers.notes"):
        yield
        return
    from app.routers.notes import _STORE

    _STORE.clear()
    yield
    _STORE.clear()


@pytest.fixture
def client():
    from fastapi.testclient import TestClient

    from app.main import app

    # raise_server_exceptions=False para que el handler global responda (en vez de
    # re-lanzar) y podamos verificar que NO se filtra el traceback.
    return TestClient(app, raise_server_exceptions=False)


def auth(user_id: str) -> dict[str, str]:
    from app.core.security import create_access_token

    return {"Authorization": f"Bearer {create_access_token(user_id)}"}
