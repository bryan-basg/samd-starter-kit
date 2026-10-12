"""Punto de entrada del esqueleto de ejemplo (FastAPI).

Corré con:  uvicorn app.main:app --reload
Docs:       http://localhost:8000/docs

Esto es un ESQUELETO MÍNIMO de referencia que muestra las reglas duras del kit.
Borralo (o reemplazalo) cuando traigas tu aplicación real.
"""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.routing import Match

from app.core.config import settings
from app.routers import notes

logger = logging.getLogger("app")


def _assert_secure_secrets() -> None:
    """Fail-safe SaMD/ISO 14971: negarse a SERVIR con secretos de dev públicos.

    En TESTING (tests, CI sin secretos, tooling que solo importa la app) se
    permiten los defaults. Fuera de TESTING asumimos entorno real: si algún
    secreto sigue con el valor de dev público, abortamos el arranque en vez de
    degradar en silencio a una postura insegura (clave de firma/cifrado conocida
    por cualquiera que lea el repo).
    """
    if settings.testing:
        return
    insecure = settings.insecure_default_secrets()
    if insecure:
        raise RuntimeError(
            "Arranque abortado (fail-safe SaMD): "
            + ", ".join(insecure)
            + " usa(n) el valor de DEV público. Inyectá los secretos reales "
            "desde el gestor de secretos/KMS, o poné TESTING=True solo en test."
        )


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    _assert_secure_secrets()
    yield


app = FastAPI(
    title="SaMD Starter Kit — esqueleto de ejemplo",
    summary="Slice mínimo que demuestra identidad-por-token, cifrado en reposo y fail-safe.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    """Fail-safe global (ISO 14971 + SaMD §5.4): el usuario nunca ve un traceback.

    El detalle técnico se registra para diagnóstico; al cliente solo le llega un
    mensaje empático + el código HTTP correcto.
    """
    logger.exception("Error no manejado", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Algo salió mal de nuestro lado. Ya estamos al tanto; "
            "probá de nuevo en un momento."
        },
    )


# Mensaje único para "no pude leer lo que mandaste", en los dos caminos por los
# que el framework puede rechazar un cuerpo.
_CUERPO_ILEGIBLE = (
    "No pudimos leer los datos que enviaste. Revisá el formato y probá de nuevo."
)

# Detalles que el FRAMEWORK genera en inglés antes de que el código de la app
# llegue a correr. Se traducen; cualquier otro `HTTPException` es nuestro y pasa
# intacto (el 503 con Retry-After, el 401 de auth, etc.).
_DETALLES_DEL_FRAMEWORK = {
    "There was an error parsing the body": _CUERPO_ILEGIBLE,
}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Cuerpo inválido → mensaje empático, nunca el detalle técnico de validación.

    El default expone la ruta del campo, el tipo esperado y a veces parte del
    cuerpo enviado — jerga que §5.4 prohíbe mostrarle a un usuario. El detalle
    completo va al log, que es donde sirve.
    """
    logger.info("Petición rechazada por validación: %s", exc.errors())
    return JSONResponse(status_code=422, content={"detail": _CUERPO_ILEGIBLE})


_METODOS_HTTP = ("GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS")


def _metodos_permitidos(request: Request) -> str | None:
    """Valor del `Allow` de un 405: TODOS los métodos que el path sí atiende.

    Starlette atiende cada decorador (`@router.get`, `@router.post`) como una ruta
    aparte y, ante un método no soportado, responde con la PRIMERA coincidencia
    parcial: `/notes` anunciaba solo `POST` aunque también acepta `GET`. RFC 9110
    §15.5.6 pide que `Allow` liste lo que el recurso soporta.

    Se le pregunta al router, método por método, si hay coincidencia COMPLETA, en
    vez de leer `route.methods`: FastAPI reciente agrupa los routers incluidos en un
    objeto interno sin `methods` (y con prefijos), y esa estructura cambia entre
    versiones. `matches()` es el contrato público y estable.
    """
    permitidos = [
        metodo
        for metodo in _METODOS_HTTP
        if any(
            ruta.matches({**request.scope, "method": metodo})[0] is Match.FULL
            for ruta in request.app.router.routes
        )
    ]
    return ", ".join(permitidos) or None


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Traduce los errores que el FRAMEWORK emite en inglés, sin pisar los nuestros.

    Un cuerpo que ni siquiera se puede parsear NO llega como error de validación:
    FastAPI lo corta antes con `HTTPException(400, "There was an error parsing the
    body")` (ver `fastapi/routing.py`). Ese texto es inglés técnico y llegaba tal
    cual al usuario.

    Lo destapó el fuzz de contrato; y el primer intento de arreglo —interceptar
    solo `RequestValidationError`— quedó ESCRITO PERO MUERTO, porque ese no es el
    camino real. Lo cazó el test, no el fuzz: el fuzz se puso verde en cuanto el
    contrato declaró el 400, sin que el mensaje hubiera mejorado. De ahí que el
    test asserte el TEXTO, no solo el código.
    """
    detalle = _DETALLES_DEL_FRAMEWORK.get(str(exc.detail))
    if detalle is None:
        headers = getattr(exc, "headers", None)
        if exc.status_code == status.HTTP_405_METHOD_NOT_ALLOWED and (
            allow := _metodos_permitidos(request)
        ):
            headers = {**(headers or {}), "Allow": allow}
        # Excepción propia de la app: su mensaje ya está redactado con cuidado.
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=headers,
        )
    logger.info("Cuerpo ilegible rechazado: %s", exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": detalle})


app.include_router(notes.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
