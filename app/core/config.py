"""Configuración del esqueleto de ejemplo.

Toda var nueva leída acá DEBE estar también en `.env.example` (regla del kit).
Los defaults son SOLO para que el ejemplo corra sin setup — en producción los
secretos se inyectan desde el gestor de secretos / KMS, nunca desde el repo.

Fail-safe SaMD/ISO 14971: los defaults de abajo son PÚBLICOS (viven en el repo).
Si la app intenta SERVIR fuera de modo test con estos valores, aborta el arranque
en vez de degradar en silencio a una postura insegura — ver `app.main.lifespan`.
"""

import base64

from pydantic_settings import BaseSettings, SettingsConfigDict

# Defaults de DEV — PÚBLICOS a propósito (para que el ejemplo corra sin setup).
# NUNCA usar en producción: cualquiera que lea el repo los conoce.
_DEV_ENCRYPTION_KEY = base64.b64encode(b"samd-starter-kit-dev-key-32bytes").decode()
_DEV_SECRET_KEY = "dev-only-insecure-secret-change-me"


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

    def insecure_default_secrets(self) -> list[str]:
        """Nombres de los secretos que siguen con el default PÚBLICO de dev.

        Lista vacía = todos los secretos fueron inyectados con valores reales.
        """
        insecure: list[str] = []
        if self.secret_key == _DEV_SECRET_KEY:
            insecure.append("SECRET_KEY")
        if self.encryption_key == _DEV_ENCRYPTION_KEY:
            insecure.append("ENCRYPTION_KEY")
        return insecure


settings = Settings()
