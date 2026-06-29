"""Esquemas de entrada/salida (validación estricta, Pydantic v2)."""

from pydantic import BaseModel, Field


class NoteIn(BaseModel):
    # OJO: no hay campo `user_id`/`owner`. La identidad viene del token, nunca
    # del cliente. Un `user_id` en el body se ignora (se demuestra en los tests).
    text: str = Field(min_length=1, max_length=2000)


class NoteOut(BaseModel):
    id: int
    text: str
