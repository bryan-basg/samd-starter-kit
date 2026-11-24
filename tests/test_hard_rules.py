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
    assert resp.headers["WWW-Authenticate"] == "Bearer"
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
    from cryptography.exceptions import InvalidTag

    with pytest.raises(InvalidTag):
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


@pytest.mark.security
def test_404_of_an_unknown_path_is_empathetic_and_in_spanish(client):
    """Una ruta inexistente responde 404 con mensaje empático (SaMD §5.4).

    El default de Starlette es `{"detail": "Not Found"}`: inglés y sin guía. Se
    asserta el TEXTO, no solo el código — el arreglo del 400 enseñó que el código
    HTTP puede estar bien con el mensaje todavía en crudo.
    """
    resp = client.get("/ruta-que-no-existe")
    assert resp.status_code == 404
    detail = resp.json()["detail"]
    assert "no encontramos" in detail.lower()
    assert "not found" not in detail.lower()


@pytest.mark.security
def test_405_is_empathetic_and_keeps_the_allow_header(client):
    """El 405 traducido NO pierde el `Allow`: el mensaje y la cabecera viajan juntos.

    Antes, la rama que traducía devolvía una respuesta sin cabeceras; traducir el
    405 por esa rama habría borrado el `Allow` que exige RFC 9110 §15.5.6.
    """
    resp = client.delete("/notes")
    assert resp.status_code == 405
    detail = resp.json()["detail"]
    assert "no está disponible" in detail.lower()
    assert "method not allowed" not in detail.lower()
    assert {m.strip() for m in resp.headers["Allow"].split(",")} == {"GET", "POST"}


@pytest.mark.unit
def test_app_http_exception_detail_passes_through_untouched(client):
    """Ancla de no-regresión: el detalle redactado por la app no se traduce ni pierde cabeceras."""
    resp = client.get("/demo/unavailable")
    assert resp.status_code == 503
    assert resp.json()["detail"].startswith("Estamos teniendo problemas")
    assert resp.headers["Retry-After"] == "30"


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
    assert resp.headers["WWW-Authenticate"] == "Bearer"
    assert "iniciá sesión de nuevo" in resp.json()["detail"].lower()


@pytest.mark.security
def test_token_invalid_format(client):
    resp = client.get("/notes", headers={"Authorization": "Bearer invalidtokenhere"})
    assert resp.status_code == 401
    assert resp.headers["WWW-Authenticate"] == "Bearer"
    assert "iniciá sesión de nuevo" in resp.json()["detail"].lower()


@pytest.mark.security
def test_expired_token_is_rejected(client):
    from app.core.security import create_access_token

    # Token ya vencido (exp 1 min en el pasado) => 401, no acceso.
    expired = create_access_token("alice", expires_minutes=-1)
    resp = client.get("/notes", headers={"Authorization": f"Bearer {expired}"})
    assert resp.status_code == 401
    assert resp.headers["WWW-Authenticate"] == "Bearer"
    assert "iniciá sesión de nuevo" in resp.json()["detail"].lower()


@pytest.mark.security
def test_token_without_exp_is_rejected(client):
    import jwt

    from app.core.config import settings

    # Firma válida pero SIN `exp`: un token así, filtrado, valdría para siempre.
    sin_exp = jwt.encode({"sub": "alice"}, settings.secret_key, algorithm="HS256")
    resp = client.get("/notes", headers={"Authorization": f"Bearer {sin_exp}"})
    assert resp.status_code == 401
    assert resp.headers["WWW-Authenticate"] == "Bearer"
    assert "iniciá sesión de nuevo" in resp.json()["detail"].lower()


_CLAVE_AES = "eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHg="  # 32 bytes


def _secretos(monkeypatch, secret_key: str, encryption_key: str = _CLAVE_AES) -> None:
    """Modo real con ESTOS secretos: no depende del `.env` de quien corre la suite."""
    from app.core.config import settings

    monkeypatch.setattr(settings, "testing", False)
    monkeypatch.setattr(settings, "secret_key", secret_key)
    monkeypatch.setattr(settings, "encryption_key", encryption_key)


@pytest.mark.security
def test_secret_guard_aborts_on_dev_defaults(monkeypatch):
    from app.core.config import _DEV_ENCRYPTION_KEY, _DEV_SECRET_KEY, settings

    # Cada default público se prueba SOLO: juntos, uno tapaba que el otro no se detectara.
    _secretos(monkeypatch, _DEV_SECRET_KEY)
    assert settings.insecure_secrets() == ["SECRET_KEY"]
    _secretos(monkeypatch, "a-real-injected-production-secret", _DEV_ENCRYPTION_KEY)
    assert settings.insecure_secrets() == ["ENCRYPTION_KEY"]


@pytest.mark.security
def test_app_startup_aborts_with_insecure_secrets(monkeypatch):
    """Flujo real: el `lifespan` (no la función suelta) se niega a arrancar."""
    from fastapi.testclient import TestClient

    from app.core.config import _DEV_SECRET_KEY
    from app.main import app

    _secretos(monkeypatch, _DEV_SECRET_KEY)
    with pytest.raises(RuntimeError, match="fail-safe SaMD.*SECRET_KEY"):
        with TestClient(app):
            pytest.fail("la app arrancó con un secreto público")


@pytest.mark.security
@pytest.mark.parametrize("margen", ["", " " * 15], ids=["sin-margen", "con-margen"])
def test_secret_guard_rejects_the_text_the_old_env_example_published(monkeypatch, margen):
    from app.core.config import settings

    _secretos(monkeypatch, margen + "# firma de sesión. Distinta de ENCRYPTION_KEY.")
    assert settings.insecure_secrets() == ["SECRET_KEY"]


@pytest.mark.security
def test_env_example_never_yields_a_usable_secret():
    """Copiar `.env.example` no puede dejar un valor en un secreto, lo lea quien lo lea.

    Se parsea a mano, como el lector más simple (todo lo que sigue al `=`): python-dotenv
    < 1.2.4 toma `VAR=   # texto` como VALOR, y el test no depende de qué versión haya.
    """
    import re
    from pathlib import Path

    from app.core.config import Settings

    texto = (Path(__file__).resolve().parents[1] / ".env.example").read_text(encoding="utf-8")
    activas = dict(
        linea.split("=", 1)
        for linea in texto.splitlines()
        if linea.strip() and not linea.lstrip().startswith("#")
    )
    assert [n for n, valor in activas.items() if "#" in valor] == []
    assert {"SECRET_KEY", "ENCRYPTION_KEY"}.isdisjoint(activas)
    # Comentadas, pero presentes: toda variable que lee `Settings` está documentada.
    documentadas = set(re.findall(r"^(?:# )?([A-Z][A-Z0-9_]*)=", texto, flags=re.M))
    assert {campo.upper() for campo in Settings.model_fields} <= documentadas


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
    assert settings.insecure_secrets() == []
    _assert_secure_secrets()  # no debe lanzar


@pytest.mark.security
@pytest.mark.parametrize(
    ("secret_key", "encryption_key", "culpable"),
    [
        ("", "eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHg=", "SECRET_KEY"),
        ("a", "eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHg=", "SECRET_KEY"),
        ("x" * 31, "eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHg=", "SECRET_KEY"),
        ("a-real-injected-production-secret", "", "ENCRYPTION_KEY"),
        ("a-real-injected-production-secret", "no-es-base64!!", "ENCRYPTION_KEY"),
        ("a-real-injected-production-secret", "eHh4eHh4eHh4eHh4eHh4eA==", "ENCRYPTION_KEY"),
        ("a-real-injected-production-secret", "eHh4" * 11, "ENCRYPTION_KEY"),
        # La MISMA clave válida en ambos roles rompe los dominios de confianza (RFC-001 §Clave).
        ("eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHg=", "eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHg=", "SECRET_KEY"),
        ("eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHg=", "eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHg=", "ENCRYPTION_KEY"),
    ],
    ids=[
        "secret-vacio", "secret-1-byte", "secret-31-bytes", "enc-vacia", "enc-no-base64",
        "enc-16-bytes", "enc-33-bytes", "misma-clave-secret", "misma-clave-enc",
    ],
)
def test_secret_guard_aborts_on_empty_short_or_malformed(
    monkeypatch, secret_key, encryption_key, culpable
):
    from app.core.config import settings
    from app.main import _assert_secure_secrets

    # El guard aborta el arranque; no deja que la app falle tarde, request por request.
    monkeypatch.setattr(settings, "testing", False)
    monkeypatch.setattr(settings, "secret_key", secret_key)
    monkeypatch.setattr(settings, "encryption_key", encryption_key)
    assert culpable in settings.insecure_secrets()
    with pytest.raises(RuntimeError, match="fail-safe SaMD"):
        _assert_secure_secrets()


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


# --- A-1: la PHI no se loguea cuando la validación falla (GDPR Art. 5(1)(c)/32, HIPAA §164.312) ---

_PHI = "PACIENTE-DIAGNOSTICO-SECRETO"


@pytest.mark.security
def test_validation_failure_does_not_log_the_submitted_text(client, caplog):
    """Flujo real: POST autenticado con texto > máximo → 422, y el texto NO llega al log."""
    import logging

    caplog.set_level(logging.INFO, logger="app")
    caplog.clear()
    resp = client.post("/notes", json={"text": _PHI + "x" * 2001}, headers=auth("alice"))
    assert resp.status_code == 422
    assert _PHI not in caplog.text
    # El diagnóstico sigue sirviendo (campo + motivo); si alguien borra la llamada al
    # helper o el log entero, esta aserción rojea.
    assert "string_too_long" in caplog.text
    assert "text" in caplog.text


def _validacion_fallida() -> None:
    from pydantic import BaseModel, Field

    class _Modelo(BaseModel):
        texto: str = Field(max_length=5)

    _Modelo(texto=_PHI)


def _fallo_directo(_token: str) -> str:
    _validacion_fallida()
    return ""


def _fallo_encadenado(_token: str) -> str:
    try:
        _validacion_fallida()
    except ValueError as exc:
        raise RuntimeError("no pude leer la nota") from exc
    return ""


def _fallo_con_contexto(_token: str) -> str:
    try:
        _validacion_fallida()
    except ValueError:
        raise RuntimeError("no pude leer la nota")
    return ""


def _fallo_agrupado(_token: str) -> str:
    try:
        _validacion_fallida()
    except ValueError as exc:
        raise ExceptionGroup("lote", [exc]) from None
    return ""


def _fallo_con_nota(_token: str) -> str:
    exc = RuntimeError("no pude leer la nota")
    exc.add_note(_PHI)
    raise exc


def _fallo_de_otro_tipo(_token: str) -> str:
    return str(int(_PHI))  # no es una validación, y su mensaje copia el valor igual


_FALLOS = [
    _fallo_directo, _fallo_encadenado, _fallo_con_contexto,
    _fallo_agrupado, _fallo_con_nota, _fallo_de_otro_tipo,
]


@pytest.mark.security
@pytest.mark.parametrize("fallo", _FALLOS)
def test_unhandled_validation_error_does_not_log_the_value(monkeypatch, caplog, fallo):
    """Ruta real (`GET /notes`): ni nuestro log ni lo que ESCAPA hacia el servidor llevan PHI.

    Lo que sale de la app es lo que cualquier servidor ASGI loguea, así que se formatea
    igual que lo haría él (con causa, contexto, grupo y notas).
    """
    import logging
    import traceback

    from fastapi.testclient import TestClient

    from app.main import ErrorInterno, app

    _STORE["alice"] = [{"id": 1, "ciphertext": "x"}]
    monkeypatch.setattr(encryption, "decrypt", fallo)
    caplog.set_level(logging.INFO, logger="app")
    caplog.clear()
    with pytest.raises(ErrorInterno) as escapa:
        TestClient(app).get("/notes", headers=auth("alice"))
    assert _PHI not in "".join(traceback.format_exception(escapa.value))
    assert escapa.value.__context__ is None and escapa.value.__cause__ is None
    assert _PHI not in caplog.text
    # El diagnóstico sigue sirviendo: dónde falló y de qué tipo, en TODA la cadena.
    assert fallo.__name__ in caplog.text
    if fallo not in (_fallo_con_nota, _fallo_de_otro_tipo):
        assert "ValidationError" in caplog.text
        assert "string_too_long" in caplog.text


@pytest.mark.security
def test_real_server_log_never_carries_the_value(monkeypatch, caplog):
    """Uvicorn de verdad: responde el 500 empático y su logger `uvicorn.error` no lleva PHI."""
    import logging
    import socket
    import threading
    import time

    import httpx
    import uvicorn

    from app.main import app

    _STORE["alice"] = [{"id": 1, "ciphertext": "x"}]
    monkeypatch.setattr(encryption, "decrypt", _fallo_encadenado)
    caplog.set_level(logging.INFO)
    sock = socket.create_server(("127.0.0.1", 0))  # puerto libre: aislado entre corridas
    servidor = uvicorn.Server(uvicorn.Config(app, log_config=None, lifespan="off", ws="none"))
    hilo = threading.Thread(target=servidor.run, kwargs={"sockets": [sock]}, daemon=True)
    hilo.start()
    try:
        limite = time.monotonic() + 10
        while not servidor.started and hilo.is_alive() and time.monotonic() < limite:
            time.sleep(0.01)
        resp = httpx.get(
            f"http://127.0.0.1:{sock.getsockname()[1]}/notes", headers=auth("alice")
        )
    finally:
        servidor.should_exit = True
        hilo.join(10)
        sock.close()
    assert resp.status_code == 500
    assert "salió mal" in resp.json()["detail"].lower()
    del_servidor = [r for r in caplog.records if r.name == "uvicorn.error" and r.exc_info]
    assert del_servidor, "uvicorn no logueó el fallo: este test no está mirando nada"
    assert _PHI not in caplog.text


@pytest.mark.security
@pytest.mark.parametrize("donde", ["middleware", "websocket"])
def test_exit_gate_covers_outer_middleware_and_websockets(caplog, donde):
    import asyncio
    import traceback

    from fastapi import WebSocket
    from fastapi.testclient import TestClient

    from app.main import AppSinDatosEnElLog, ErrorInterno

    local = AppSinDatosEnElLog()

    class _MiddlewareDeAfuera:
        def __init__(self, app):
            self.app = app

        async def __call__(self, scope, receive, send):
            if scope["type"] == "http":
                _validacion_fallida()
            await self.app(scope, receive, send)

    @local.websocket("/ws")
    async def _ws(ws: WebSocket) -> None:
        await ws.accept()
        _validacion_fallida()

    async def _conectar() -> None:
        scope = {"type": "websocket", "path": "/ws", "headers": [], "query_string": b""}

        async def _recibir():
            return {"type": "websocket.connect"}

        async def _enviar(_mensaje):
            return None

        await local(scope, _recibir, _enviar)

    local.add_middleware(_MiddlewareDeAfuera)
    with pytest.raises(ErrorInterno) as escapa:
        if donde == "middleware":
            TestClient(local).get("/")
        else:
            asyncio.run(_conectar())
    assert _PHI not in "".join(traceback.format_exception(escapa.value))
    assert _PHI not in caplog.text
    assert "string_too_long" in caplog.text


@pytest.mark.security
def test_resumen_de_errores_never_carries_value_ctx_or_user_keys():
    from app.main import _resumen_de_errores

    errores = [
        {"type": "string_too_long", "loc": ("body", "text"), "input": _PHI, "ctx": {"max_length": 2000}},
        {"type": "extra_forbidden", "loc": ("body", "PHI-COMO-CLAVE"), "input": _PHI, "msg": _PHI},
    ]
    resumen = _resumen_de_errores(errores)
    assert resumen == [
        {"type": "string_too_long", "loc": ["body", "text"]},
        {"type": "extra_forbidden", "loc": ["body", "<campo>"]},
    ]
    assert _PHI not in repr(resumen) and "PHI-COMO-CLAVE" not in repr(resumen)


def test_every_endpoint_is_async():
    """«100 % async» (`app/README.md`): un `def` corre en hilos y dos notas compartían id."""
    import inspect

    from app.main import app
    from app.routers import notes

    handlers = [r.endpoint for r in notes.router.routes if hasattr(r, "endpoint")]
    handlers += [r.endpoint for r in app.routes if getattr(r, "path", "") == "/health"]
    assert len(handlers) >= 5
    assert [h.__name__ for h in handlers if not inspect.iscoroutinefunction(h)] == []


@pytest.mark.security
def test_empty_sub_is_rejected(client):
    """Un token bien firmado con `sub` vacío no es nadie: `require` solo exige que exista."""
    resp = client.get("/notes", headers=auth(""))
    assert resp.status_code == 401
    assert resp.headers["WWW-Authenticate"] == "Bearer"
