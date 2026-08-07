"""Recurso de ejemplo: notas privadas por usuario.

Demuestra, en un slice mínimo, cuatro reglas duras del kit:
  1. Identidad solo del token (el dueño de la nota es `get_current_user_id`).
  2. Cifrado en reposo (el texto se guarda cifrado, se descifra al leer).
  3. Aislamiento por dueño (un usuario no ve las notas de otro).
  4. Fail-safe explícito (degradación 503 + Retry-After, mensaje empático).

Store EN MEMORIA a propósito: el esqueleto corre sin base de datos. En tu app
real, esto es un repositorio sobre tu `{{DB_STACK}}` con cifrado a nivel de columna.
"""

from typing import TypedDict

from fastapi import APIRouter, Depends, HTTPException, status

from app.core import encryption
from app.core.security import get_current_user_id
from app.schemas import ErrorOut, NoteIn, NoteOut

router = APIRouter()

# Respuestas de error que el contrato DEBE declarar. Un endpoint autenticado que
# solo documenta el 200 le miente al contrato: el cliente generado a partir de
# `openapi.json` no sabe que existe el 401 y lo trata como una respuesta
# inesperada. El fuzz de contrato (schemathesis) lo levanta como "Undocumented
# HTTP status code" — fue exactamente el hallazgo que destapó encender ese gate.
_AUTH_RESPONSES: dict[int | str, dict[str, object]] = {
    401: {"description": "Falta el token o no es válido.", "model": ErrorOut},
}

# Mismo criterio para el cuerpo: si la app puede devolver 400 o 422, el contrato los
# declara — y con el modelo REAL (`ErrorOut`, una frase), no con el default del
# framework (una lista de errores de validación). Los emite `app/main.py`.
_BODY_RESPONSES: dict[int | str, dict[str, object]] = {
    **_AUTH_RESPONSES,
    400: {"description": "El cuerpo enviado no es JSON válido.", "model": ErrorOut},
    422: {"description": "Los datos enviados no son válidos.", "model": ErrorOut},
}


class _StoredNote(TypedDict):
    id: int
    ciphertext: str


# user_id -> lista de notas cifradas. El texto NUNCA se guarda en claro.
_STORE: dict[str, list[_StoredNote]] = {}


@router.post(
    "/notes",
    response_model=NoteOut,
    status_code=status.HTTP_201_CREATED,
    responses=_BODY_RESPONSES,
)
def create_note(note: NoteIn, user_id: str = Depends(get_current_user_id)) -> NoteOut:
    bucket = _STORE.setdefault(user_id, [])
    item: _StoredNote = {"id": len(bucket) + 1, "ciphertext": encryption.encrypt(note.text)}
    bucket.append(item)
    return NoteOut(id=item["id"], text=note.text)


@router.get("/notes", response_model=list[NoteOut], responses=_AUTH_RESPONSES)
def list_notes(user_id: str = Depends(get_current_user_id)) -> list[NoteOut]:
    return [
        NoteOut(id=i["id"], text=encryption.decrypt(i["ciphertext"]))
        for i in _STORE.get(user_id, [])
    ]


@router.get("/demo/unavailable")
def demo_unavailable() -> None:
    """Ilustra el fusible: cuando una dependencia cae, degradamos así (no 500 seco)."""
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Estamos teniendo problemas para conectar. Probá de nuevo en un momento.",
        headers={"Retry-After": "30"},
    )


@router.get("/demo/internal-error")
def demo_internal_error() -> None:
    """Ilustra el handler global: un error inesperado NO filtra traceback al usuario."""
    raise RuntimeError("fallo interno simulado con detalle sensible que no debe filtrarse")
