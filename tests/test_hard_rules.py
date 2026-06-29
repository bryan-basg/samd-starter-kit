"""Verificación de las reglas duras del kit sobre el esqueleto de ejemplo.

Tests RIGUROSOS (SaMD §5.7): aserciones específicas sobre valores, side effects
y comportamiento de seguridad — NO "responde 200 sin crashear".
"""

import pytest

from app.core import encryption
from app.routers.notes import _STORE
from tests.conftest import auth


@pytest.mark.security
def test_unauthenticated_request_is_rejected(client):
    resp = client.post("/notes", json={"text": "hola"})
    assert resp.status_code == 401
    # Mensaje empático, no técnico.
    assert "iniciar sesión" in resp.json()["detail"].lower()


@pytest.mark.security
def test_identity_comes_from_token_not_from_body(client):
    # Alice manda una nota e INTENTA hacerse pasar por otro vía el body.
    resp = client.post(
        "/notes",
        json={"text": "secreto de alice", "user_id": "attacker", "owner": "attacker"},
        headers=auth("alice"),
    )
    assert resp.status_code == 201

    # El body fue ignorado: la nota es de alice, no de "attacker".
    assert list(_STORE.keys()) == ["alice"]
    assert "attacker" not in _STORE


@pytest.mark.security
def test_owner_isolation_between_users(client):
    client.post("/notes", json={"text": "nota de alice"}, headers=auth("alice"))

    # Bob no ve nada de Alice.
    bob = client.get("/notes", headers=auth("bob"))
    assert bob.status_code == 200
    assert bob.json() == []

    # Alice sí ve la suya, en claro.
    alice = client.get("/notes", headers=auth("alice"))
    assert [n["text"] for n in alice.json()] == ["nota de alice"]


@pytest.mark.security
def test_text_is_encrypted_at_rest(client):
    plaintext = "dato clínico sensible"
    client.post("/notes", json={"text": plaintext}, headers=auth("alice"))

    stored = _STORE["alice"][0]["ciphertext"]
    # Lo guardado NO es el texto en claro...
    assert plaintext not in stored
    assert stored != plaintext
    # ...pero descifra de vuelta exacto.
    assert encryption.decrypt(stored) == plaintext


@pytest.mark.unit
def test_encryption_roundtrip_and_nonce_uniqueness():
    a = encryption.encrypt("mismo texto")
    b = encryption.encrypt("mismo texto")
    # Nonce aleatorio => dos cifrados del mismo texto difieren (no determinista).
    assert a != b
    assert encryption.decrypt(a) == "mismo texto"
    assert encryption.decrypt(b) == "mismo texto"


@pytest.mark.unit
def test_tampered_ciphertext_is_rejected():
    import base64

    token = encryption.encrypt("intacto")
    raw = bytearray(base64.b64decode(token))
    raw[-1] ^= 0x01  # corrompe un byte del tag GCM
    tampered = base64.b64encode(bytes(raw)).decode()
    with pytest.raises(Exception):
        encryption.decrypt(tampered)


@pytest.mark.security
def test_internal_error_never_leaks_a_traceback(client):
    resp = client.get("/demo/internal-error", headers=auth("alice"))
    assert resp.status_code == 500
    body = resp.text
    # Mensaje empático presente...
    assert "salió mal" in resp.json()["detail"].lower()
    # ...y CERO filtración técnica.
    for leak in ("Traceback", "RuntimeError", "sensible", "app/routers"):
        assert leak not in body


@pytest.mark.security
def test_failsafe_returns_503_with_retry_after(client):
    resp = client.get("/demo/unavailable", headers=auth("alice"))
    assert resp.status_code == 503
    assert resp.headers.get("Retry-After") == "30"
    assert "momento" in resp.json()["detail"].lower()
