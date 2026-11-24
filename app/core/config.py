"""Configuración del esqueleto de ejemplo.

Toda var nueva leída acá DEBE estar también en `.env.example` (regla del kit).
Los defaults son SOLO para que el ejemplo corra sin setup — en producción los
secretos se inyectan desde el gestor de secretos / KMS, nunca desde el repo.

Fail-safe SaMD/ISO 14971: los defaults de abajo son PÚBLICOS (viven en el repo).
Si la app intenta SERVIR fuera de modo test con estos valores, aborta el arranque
en vez de degradar en silencio a una postura insegura — ver `app.main.lifespan`.
"""

import base64
import hmac
import binascii

from pydantic_settings import BaseSettings, SettingsConfigDict

# Defaults de DEV — PÚBLICOS a propósito (para que el ejemplo corra sin setup).
# NUNCA usar en producción: cualquiera que lea el repo los conoce.
_DEV_ENCRYPTION_KEY = base64.b64encode(b"samd-starter-kit-dev-key-32bytes").decode()
# Mínimo 32 bytes: HS256 lo exige (RFC 7518 §3.2) y PyJWT avisa por debajo.
_DEV_SECRET_KEY = "dev-only-insecure-public-secret-key"
# Todo texto que ESTE repo publicó y que algún despliegue pudo tomar como SECRET_KEY. El
# segundo era el comentario en línea del `.env.example` viejo: python-dotenv < 1.2.4 lo
# leía como valor y pasaba el piso de longitud. Quien copió ese archivo lo sigue teniendo.
_SECRET_KEYS_PUBLICAS = frozenset(
    {_DEV_SECRET_KEY, "# firma de sesión. Distinta de ENCRYPTION_KEY."}
)

# Pisos de longitud. SECRET_KEY: ≥32 bytes (HS256, RFC 7518 §3.2) — una clave
# HMAC corta se rompe por fuerza bruta offline a partir de cualquier token.
# ENCRYPTION_KEY: base64 que decodifica a EXACTAMENTE 32 bytes (AES-256).
MIN_SECRET_KEY_BYTES = 32
ENCRYPTION_KEY_BYTES = 32


def decode_encryption_key(value: str) -> bytes | None:
    """Puerta única del formato de ENCRYPTION_KEY. `None` = clave inválida.

    La usan el guard de arranque (`Settings.insecure_secrets`) y el cifrado
    (`app.core.encryption._key`), para que la regla de los 32 bytes viva en un
    solo lugar.
    """
    try:
        raw = base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError):
        return None
    return raw if len(raw) == ENCRYPTION_KEY_BYTES else None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # AES-256-GCM para PII/PHI en reposo (REQ-SEC-01). 32 bytes en base64.
    # DEV ONLY: clave derivada de una frase fija. NUNCA usar en producción.
    encryption_key: str = _DEV_ENCRYPTION_KEY

    # Firma del token de sesión. Distinta de encryption_key. DEV ONLY.
    secret_key: str = _DEV_SECRET_KEY

    # Vida del token de sesión. Sin `exp` un token robado vale para siempre.
    access_token_expire_minutes: int = 30

    # TESTING=True habilita los defaults de dev (tests/CI/tooling local). En
    # producción DEBE ser false: es lo que distingue "importo la app" de "sirvo
    # la app con secretos reales" en el guard fail-safe de `app.main`.
    testing: bool = False

    def insecure_secrets(self) -> list[str]:
        """Nombres de los secretos que NO sirven para producción.

        Inseguro = sigue con el default PÚBLICO de dev, está vacío, es demasiado
        corto / mal formado, o `SECRET_KEY` y `ENCRYPTION_KEY` son la misma clave. Lista vacía = todos los secretos son aptos.
        """
        insecure: list[str] = []
        if (
            self.secret_key.strip() in _SECRET_KEYS_PUBLICAS
            or len(self.secret_key.encode("utf-8")) < MIN_SECRET_KEY_BYTES
        ):
            insecure.append("SECRET_KEY")
        if (
            self.encryption_key == _DEV_ENCRYPTION_KEY
            or decode_encryption_key(self.encryption_key) is None
        ):
            insecure.append("ENCRYPTION_KEY")
        # Dominios de confianza separados (RFC-001 §Clave): firmar JWT y cifrar PHI con la
        # MISMA clave deja que quien roba una rompa la otra. Detecta el copiar-y-pegar de
        # la misma clave; una variante casi igual (clave + sufijo) no se detecta.
        if hmac.compare_digest(self.secret_key.encode("utf-8"), self.encryption_key.encode("utf-8")):
            insecure.extend(n for n in ("SECRET_KEY", "ENCRYPTION_KEY") if n not in insecure)
        return insecure


settings = Settings()
