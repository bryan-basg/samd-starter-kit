"""Identidad SOLO del token (REQ-SEC-02, RFC-002).

El `user_id` se deriva EXCLUSIVAMENTE del token decodificado. NUNCA se acepta
desde el body, query ni headers custom — eso es un vector de escalada garantizado.
"""

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings

_ALGORITHM = "HS256"

# auto_error=False: manejamos el 401 nosotros para dar un mensaje empático
# (un usuario nunca debe ver un error técnico crudo — SaMD §5.4).
_bearer = HTTPBearer(auto_error=False)

_UNAUTHENTICATED = "Necesitás iniciar sesión para continuar."
_INVALID = "Tu sesión expiró o no es válida. Iniciá sesión de nuevo."


def create_access_token(user_id: str) -> str:
    """Helper de DEV/test para emitir un token. En prod lo emite tu proveedor de auth."""
    return jwt.encode({"sub": user_id}, settings.secret_key, algorithm=_ALGORITHM)


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> str:
    if credentials is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, _UNAUTHENTICATED)
    try:
        payload = jwt.decode(
            credentials.credentials, settings.secret_key, algorithms=[_ALGORITHM]
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, _INVALID) from None
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, _INVALID)
    return str(user_id)
