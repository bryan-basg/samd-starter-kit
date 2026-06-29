"""Cifrado en reposo AES-256-GCM (REQ-SEC-01).

Demuestra el patrón "PII/PHI cifrada a nivel de campo": el texto se guarda
cifrado y solo se descifra al leerlo. La clave vive en config (en prod: KMS).
NO es SQLCipher; es cifrado autenticado a nivel de valor.
"""

import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.core.config import settings

_NONCE_BYTES = 12


def _key() -> bytes:
    raw = base64.b64decode(settings.encryption_key)
    if len(raw) != 32:
        # Fail-safe explícito: una clave mal configurada NO debe degradar a
        # "sin cifrado" en silencio — rompe ruidosamente.
        raise ValueError("ENCRYPTION_KEY debe decodificar a 32 bytes (AES-256).")
    return raw


def encrypt(plaintext: str) -> str:
    """Cifra y devuelve `base64(nonce || ciphertext)`."""
    aes = AESGCM(_key())
    nonce = os.urandom(_NONCE_BYTES)
    ciphertext = aes.encrypt(nonce, plaintext.encode("utf-8"), None)
    return base64.b64encode(nonce + ciphertext).decode("ascii")


def decrypt(token: str) -> str:
    """Inverso de `encrypt`. Lanza si el dato fue manipulado (GCM autentica)."""
    blob = base64.b64decode(token)
    nonce, ciphertext = blob[:_NONCE_BYTES], blob[_NONCE_BYTES:]
    aes = AESGCM(_key())
    return aes.decrypt(nonce, ciphertext, None).decode("utf-8")
