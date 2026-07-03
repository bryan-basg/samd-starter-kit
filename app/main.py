"""Punto de entrada del esqueleto de ejemplo (FastAPI).

Corré con:  uvicorn app.main:app --reload
Docs:       http://localhost:8000/docs

Esto es un ESQUELETO MÍNIMO de referencia que muestra las reglas duras del kit.
Borralo (o reemplazalo) cuando traigas tu aplicación real.
"""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

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


app.include_router(notes.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
