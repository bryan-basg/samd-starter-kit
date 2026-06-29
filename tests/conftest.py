"""Fixtures compartidas + aislamiento de estado global (regla dura del kit)."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers.notes import _STORE


@pytest.fixture(autouse=True)
def _reset_store():
    """Cada test arranca con el store vacío y lo limpia al salir (sin fugas)."""
    _STORE.clear()
    yield
    _STORE.clear()


@pytest.fixture
def client():
    # raise_server_exceptions=False para que el handler global responda (en vez de
    # re-lanzar) y podamos verificar que NO se filtra el traceback.
    return TestClient(app, raise_server_exceptions=False)


def auth(user_id: str) -> dict[str, str]:
    from app.core.security import create_access_token

    return {"Authorization": f"Bearer {create_access_token(user_id)}"}
