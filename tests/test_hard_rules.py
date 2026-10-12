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


@pytest.mark.security
def test_malformed_body_gets_an_empathetic_message_not_the_framework_default(client):
    """Cuerpo ilegible → 400 con mensaje humano, nunca el texto del framework.

    Lo destapó el fuzz de contrato (schemathesis), no una revisión a ojo: sin el
    handler, la librería respondía `"There was an error parsing the body"` — en
    inglés y en jerga técnica, justo lo que §5.4 prohíbe mostrarle a un usuario.
    """
    resp = client.post(
        "/notes",
        content=b"\x80\x81 esto no es json",
        headers={**auth("alice"), "Content-Type": "application/json"},
    )
    assert resp.status_code == 400
    detail = resp.json()["detail"]
    # Mensaje empático y en español...
    assert "no pudimos leer" in detail.lower()
    # ...y NADA del default técnico del framework.
    for leak in ("parsing", "body", "JSON decode", "Traceback"):
        assert leak.lower() not in detail.lower()


@pytest.mark.security
def test_invalid_payload_shape_is_422_and_still_empathetic(client):
    """Un cuerpo JSON válido pero con forma inválida sigue siendo 422, no 400.

    Ancla que el handler distingue "no pude parsear" (400) de "parseé pero no
    valida" (422): colapsar ambos en un solo código le mentiría al contrato.
    """
    resp = client.post("/notes", json={"text": 12345678}, headers=auth("alice"))
    assert resp.status_code == 422
    assert "no pudimos leer" in resp.json()["detail"].lower()


@pytest.mark.unit
def test_405_allow_header_lists_every_method_of_the_path(client):
    """Un 405 declara en `Allow` TODOS los métodos que la ruta sí acepta.

    Lo destapó el fuzz de contrato (schemathesis 4.30): `/notes` tiene un GET y un
    POST, y Starlette las atiende como rutas separadas — responde con la primera
    que encuentra, así que `Allow` decía solo `POST` y le mentía al cliente sobre
    el `GET` (RFC 9110 §15.5.6). Se asserta el CONJUNTO, no un texto: el orden de
    los métodos no es contrato.
    """
    resp = client.options("/notes")
    assert resp.status_code == 405
    allow = {m.strip() for m in resp.headers["Allow"].split(",")}
    assert allow == {"GET", "POST"}


@pytest.mark.unit
def test_405_allow_header_survives_a_router_prefix():
    """El caso real de una app: routers incluidos con prefijo, no rutas sueltas.

    FastAPI reciente agrupa un router incluido en un objeto interno; leer
    `route.methods` del nivel de arriba no veía nada. Se arma una app aparte con
    prefijo para anclar que el arreglo no depende de esa estructura.
    """
    from fastapi import APIRouter, FastAPI
    from fastapi.testclient import TestClient
    from starlette.exceptions import HTTPException as StarletteHTTPException

    from app.main import http_exception_handler

    router = APIRouter(prefix="/v1")

    @router.get("/recurso")
    def _leer() -> dict[str, str]:
        return {}

    @router.put("/recurso")
    def _reemplazar() -> dict[str, str]:
        return {}

    local = FastAPI()
    local.add_exception_handler(StarletteHTTPException, http_exception_handler)
    local.include_router(router)

    resp = TestClient(local).post("/v1/recurso")
    assert resp.status_code == 405
    assert {m.strip() for m in resp.headers["Allow"].split(",")} == {"GET", "PUT"}


@pytest.mark.unit
def test_405_allow_header_on_a_single_method_path_is_unchanged(client):
    """Ancla de no-regresión: una ruta de un solo método sigue anunciando solo ese."""
    resp = client.options("/health")
    assert resp.status_code == 405
    assert resp.headers["Allow"] == "GET"


@pytest.mark.unit
def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


@pytest.mark.unit
def test_encryption_key_length_validation(monkeypatch):
    import base64
    from app.core import encryption
    # Cambiar temporalmente la key configurada por una corta (inválida)
    monkeypatch.setattr(
        encryption.settings,
        "encryption_key",
        base64.b64encode(b"short-key").decode(),
    )
    with pytest.raises(ValueError, match="ENCRYPTION_KEY debe decodificar a 32 bytes"):
        encryption.encrypt("test")


@pytest.mark.security
def test_token_missing_sub_claim(client):
    import jwt
    from app.core.config import settings
    # Generar un token firmado pero sin el claim 'sub'
    bad_token = jwt.encode({}, settings.secret_key, algorithm="HS256")
    resp = client.get("/notes", headers={"Authorization": f"Bearer {bad_token}"})
    assert resp.status_code == 401
    assert "iniciá sesión de nuevo" in resp.json()["detail"].lower()


@pytest.mark.security
def test_token_invalid_format(client):
    resp = client.get("/notes", headers={"Authorization": "Bearer invalidtokenhere"})
    assert resp.status_code == 401
    assert "iniciá sesión de nuevo" in resp.json()["detail"].lower()


@pytest.mark.security
def test_expired_token_is_rejected(client):
    from app.core.security import create_access_token

    # Token ya vencido (exp 1 min en el pasado) => 401, no acceso.
    expired = create_access_token("alice", expires_minutes=-1)
    resp = client.get("/notes", headers={"Authorization": f"Bearer {expired}"})
    assert resp.status_code == 401
    assert "iniciá sesión de nuevo" in resp.json()["detail"].lower()


@pytest.mark.security
def test_secret_guard_aborts_on_dev_defaults(monkeypatch):
    from app.core.config import settings
    from app.main import _assert_secure_secrets

    # Simular producción (TESTING off) con los defaults de dev todavía puestos.
    monkeypatch.setattr(settings, "testing", False)
    with pytest.raises(RuntimeError, match="fail-safe SaMD"):
        _assert_secure_secrets()


@pytest.mark.security
def test_secret_guard_passes_with_real_secrets(monkeypatch):
    import base64

    from app.core.config import settings
    from app.main import _assert_secure_secrets

    # Producción con secretos reales inyectados => NO aborta.
    monkeypatch.setattr(settings, "testing", False)
    monkeypatch.setattr(settings, "secret_key", "a-real-injected-production-secret")
    monkeypatch.setattr(
        settings, "encryption_key", base64.b64encode(b"x" * 32).decode()
    )
    assert settings.insecure_default_secrets() == []
    _assert_secure_secrets()  # no debe lanzar


@pytest.mark.security
def test_lifespan_boots_in_testing_mode(monkeypatch):
    from fastapi.testclient import TestClient

    from app.core.config import settings
    from app.main import app

    # En modo TESTING el guard se salta aunque haya defaults de dev: el lifespan
    # arranca y la app sirve. (with => dispara startup/shutdown del lifespan.)
    monkeypatch.setattr(settings, "testing", True)
    with TestClient(app) as c:
        assert c.get("/health").status_code == 200
