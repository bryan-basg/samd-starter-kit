"""Punto de entrada del esqueleto de ejemplo (FastAPI).

Corré con:  TESTING=True uvicorn app.main:app --reload   (demo local; sin TESTING exige secretos reales)
Docs:       http://localhost:8000/docs

Esto es un ESQUELETO MÍNIMO de referencia que muestra las reglas duras del kit.
Borralo (o reemplazalo) cuando traigas tu aplicación real.
"""

import logging
import traceback
from collections.abc import AsyncIterator, Iterable, Mapping
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, ValidationException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.routing import Match
from starlette.types import Receive, Scope, Send

from app.core.config import settings
from app.routers import notes

logger = logging.getLogger("app")


def _assert_secure_secrets() -> None:
    """Fail-safe SaMD/ISO 14971: negarse a SERVIR con secretos no aptos.

    En TESTING (tests, CI sin secretos, tooling que solo importa la app) se
    permiten los defaults. Fuera de TESTING asumimos entorno real: si algún
    secreto sigue con el valor de dev público, está vacío o es corto, abortamos el arranque en vez de
    degradar en silencio a una postura insegura (clave de firma/cifrado conocida
    por cualquiera que lea el repo).
    """
    if settings.testing:
        return
    insecure = settings.insecure_secrets()
    if insecure:
        raise RuntimeError(
            "Arranque abortado (fail-safe SaMD): "
            + ", ".join(insecure)
            + " está(n) vacío(s), es(son) demasiado corto(s) o usa(n) el valor de"
            " DEV público. Inyectá los secretos reales "
            "desde el gestor de secretos/KMS, o poné TESTING=True solo en test."
        )


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    _assert_secure_secrets()
    yield


def _resumen_de_errores(errores: Iterable[Mapping[str, object]]) -> list[dict[str, object]]:
    """Qué campo falló y por qué (`loc` + `type`), NUNCA con el valor que mandó el usuario.

    Puerta ÚNICA de todo lo que se loguea sobre una validación fallida (GDPR Art. 5(1)(c)/32,
    HIPAA §164.312): los errores de pydantic traen `input` (el valor crudo: el texto de una
    nota de paciente), `ctx` (a veces el valor interpolado en un `ValueError`) y `msg`
    (copia el texto de los validadores propios). Ningún sitio de la app debe volver a
    loguear `exc.errors()` ni `str(exc)` de una validación: usa esta función.

    Límite conocido: en `extra_forbidden` el último segmento de `loc` ES la clave que mandó
    el cliente y se enmascara; en campos `dict[str, X]` la clave del usuario también viaja
    en `loc` y NO se detecta. Si tu modelo los tiene, recortá `loc` en esta función.
    """
    resumen: list[dict[str, object]] = []
    for error in errores:
        bruto = error.get("loc")
        loc = list(bruto) if isinstance(bruto, (tuple, list)) else []
        if error.get("type") == "extra_forbidden" and loc:
            loc[-1] = "<campo>"
        resumen.append({"type": error.get("type"), "loc": loc})
    return resumen


def _diagnostico(exc: BaseException, vistas: set[int] | None = None) -> str:
    """Qué falló y dónde: tipos de TODA la cadena + pila. NUNCA los mensajes.

    El mensaje de una excepción puede traer PHI sea del tipo que sea (`int("texto")`,
    los `parameters` de un error de base de datos, una nota con `add_note`), y también
    la excepción que la causó. Por eso no se elige qué tipos limpiar: no sale ninguno.
    """
    vistas = set() if vistas is None else vistas
    vistas.add(id(exc))
    partes: list[str] = []
    previa = exc.__cause__ or (None if exc.__suppress_context__ else exc.__context__)
    if previa is not None and id(previa) not in vistas:
        partes += [_diagnostico(previa, vistas), "--- y al manejarla ---\n"]
    partes += traceback.format_tb(exc.__traceback__)
    partes.append(f"{type(exc).__module__}.{type(exc).__qualname__}")
    if isinstance(exc, (ValidationError, ValidationException)):
        partes.append(f" {_resumen_de_errores(exc.errors())}")
    partes.append("\n")
    if isinstance(exc, BaseExceptionGroup):
        for sub in exc.exceptions:
            if id(sub) not in vistas:
                partes += ["--- dentro del grupo ---\n", _diagnostico(sub, vistas)]
    return "".join(partes)


class ErrorInterno(Exception):
    """Lo único que sale de la app hacia el servidor: el tipo del fallo, sin datos."""


class AppSinDatosEnElLog(FastAPI):
    """Puerta ÚNICA de salida de errores no manejados (GDPR Art. 32, HIPAA §164.312).

    Starlette responde el 500 y RELANZA la excepción original; uvicorn, hypercorn y
    gunicorn la loguean con `str(exc)`. `__call__` es el último punto nuestro antes
    del servidor: por fuera de cualquier middleware, también para WebSocket, streaming
    y tareas de fondo. Se relanza (no se traga) para que el servidor corte una
    respuesta a medias en vez de darla por completa.

    Fuera de su alcance: `asyncio.create_task` sin `await`, un `logger.exception()`
    propio y los exportadores (Sentry, OpenTelemetry) que observan desde adentro.
    """

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            await super().__call__(scope, receive, send)
            return
        except Exception as exc:
            if scope["type"] == "lifespan":
                # El arranque no lleva datos de pacientes, y el mensaje del guard de
                # secretos tiene que llegar entero a quien despliega.
                raise
            fallo = exc
        # Fuera del `except` a propósito: adentro, Python le colgaría la excepción
        # original como `__context__` a lo que se lance acá.
        logger.error("Error no manejado\n%s", _diagnostico(fallo))
        tipo = type(fallo).__qualname__
        del fallo
        raise ErrorInterno(f"{tipo} (detalle en el logger 'app')")


app = AppSinDatosEnElLog(
    title="SaMD Starter Kit — esqueleto de ejemplo",
    summary="Slice mínimo que demuestra identidad-por-token, cifrado en reposo y fail-safe.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
    """Fail-safe global (ISO 14971 + SaMD §5.4): el usuario nunca ve un traceback.

    Solo arma la respuesta empática. El diagnóstico lo registra la salida de la app
    (`AppSinDatosEnElLog`): después de este handler el framework RELANZA la excepción
    y el servidor la escribe entera, así que limpiar el log acá no alcanzaba.
    """
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
#
# "Not Found" y "Method Not Allowed" son el texto que Starlette pone por defecto
# (la frase estándar del código HTTP) cuando una ruta no existe o no acepta el
# método. Un `HTTPException(404)` propio SIN detalle cae en el mismo texto, y
# también se traduce: sigue sin estar redactado para el usuario.
_DETALLES_DEL_FRAMEWORK = {
    "There was an error parsing the body": _CUERPO_ILEGIBLE,
    "Not Found": "No encontramos lo que buscás. Revisá la dirección y probá de nuevo.",
    "Method Not Allowed": "Esa acción no está disponible en esta dirección.",
}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Cuerpo inválido → mensaje empático, nunca el detalle técnico de validación.

    El default expone la ruta del campo, el tipo esperado y a veces parte del
    cuerpo enviado — jerga que §5.4 prohíbe mostrarle a un usuario. Al log va el
    campo y el motivo (`_resumen_de_errores`), nunca el valor: ese puede ser PHI.
    """
    logger.info("Petición rechazada por validación: %s", _resumen_de_errores(exc.errors()))
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
    headers = getattr(exc, "headers", None)
    if exc.status_code == status.HTTP_405_METHOD_NOT_ALLOWED and (
        allow := _metodos_permitidos(request)
    ):
        headers = {**(headers or {}), "Allow": allow}
    detalle = _DETALLES_DEL_FRAMEWORK.get(str(exc.detail))
    if detalle is None:
        # Excepción propia de la app: su mensaje ya está redactado con cuidado.
        detalle = exc.detail
    else:
        logger.info(
            "Detalle del framework traducido (%s): %s", exc.status_code, exc.detail
        )
    return JSONResponse(
        status_code=exc.status_code, content={"detail": detalle}, headers=headers
    )


app.include_router(notes.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
