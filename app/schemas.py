"""Esquemas de entrada/salida (validación estricta, Pydantic v2)."""

from pydantic import BaseModel, Field


class NoteIn(BaseModel):
    # OJO: no hay campo `user_id`/`owner`. La identidad viene del token, nunca
    # del cliente. Un `user_id` en el body se ignora (se demuestra en los tests).
    text: str = Field(min_length=1, max_length=2000)


class NoteOut(BaseModel):
    id: int
    text: str


class ErrorOut(BaseModel):
    """Forma ÚNICA de todo error que sale de la API.

    El default del framework para un 422 es `detail: [ {loc, msg, type}, … ]` —
    una lista de errores de validación con rutas de campo y nombres de tipo, o
    sea jerga técnica que §5.4 prohíbe mostrarle a un usuario. Los handlers de
    `app/main.py` devuelven en su lugar UNA frase empática, así que el contrato
    tiene que declarar esa forma: si el contrato promete una lista y la app manda
    texto, el cliente generado rompe.

    Lo cazó el fuzz de contrato al validar la respuesta contra su propio esquema.
    """

    detail: str = Field(examples=["No pudimos leer los datos que enviaste."])
