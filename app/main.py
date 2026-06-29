"""Punto de entrada del esqueleto de ejemplo (FastAPI).

Corré con:  uvicorn app.main:app --reload
Docs:       http://localhost:8000/docs

Esto es un ESQUELETO MÍNIMO de referencia que muestra las reglas duras del kit.
Borralo (o reemplazalo) cuando traigas tu aplicación real.
"""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers import notes

logger = logging.getLogger("app")

app = FastAPI(
    title="SaMD Starter Kit — esqueleto de ejemplo",
    summary="Slice mínimo que demuestra identidad-por-token, cifrado en reposo y fail-safe.",
    version="0.1.0",
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
