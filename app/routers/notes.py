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
from app.schemas import NoteIn, NoteOut

router = APIRouter()


class _StoredNote(TypedDict):
    id: int
    ciphertext: str


# user_id -> lista de notas cifradas. El texto NUNCA se guarda en claro.
_STORE: dict[str, list[_StoredNote]] = {}


@router.post("/notes", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteIn, user_id: str = Depends(get_current_user_id)) -> NoteOut:
    bucket = _STORE.setdefault(user_id, [])
    item: _StoredNote = {"id": len(bucket) + 1, "ciphertext": encryption.encrypt(note.text)}
    bucket.append(item)
    return NoteOut(id=item["id"], text=note.text)


@router.get("/notes", response_model=list[NoteOut])
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
