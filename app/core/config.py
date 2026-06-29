"""Configuración del esqueleto de ejemplo.

Toda var nueva leída acá DEBE estar también en `.env.example` (regla del kit).
Los defaults son SOLO para que el ejemplo corra sin setup — en producción los
secretos se inyectan desde el gestor de secretos / KMS, nunca desde el repo.
"""

import base64

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # AES-256-GCM para PII/PHI en reposo (REQ-SEC-01). 32 bytes en base64.
    # DEV ONLY: clave derivada de una frase fija. NUNCA usar en producción.
    encryption_key: str = base64.b64encode(b"samd-starter-kit-dev-key-32bytes").decode()

    # Firma del token de sesión. Distinta de encryption_key. DEV ONLY.
    secret_key: str = "dev-only-insecure-secret-change-me"


settings = Settings()
