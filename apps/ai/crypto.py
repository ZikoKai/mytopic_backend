import base64
import hashlib

from django.conf import settings


def _fernet():
    try:
        from cryptography.fernet import Fernet
    except Exception as exc:
        raise RuntimeError("cryptography is required to encrypt provider API keys.") from exc

    digest = hashlib.sha256(settings.SECRET_KEY.encode("utf-8")).digest()
    return Fernet(base64.urlsafe_b64encode(digest))


def encrypt_secret(value: str) -> str:
    """Encrypt a secret before database storage."""
    cleaned = value.strip()
    if not cleaned:
        return ""
    return _fernet().encrypt(cleaned.encode("utf-8")).decode("utf-8")


def decrypt_secret(value: str) -> str:
    """Decrypt a stored secret. Empty values stay empty."""
    if not value:
        return ""
    return _fernet().decrypt(value.encode("utf-8")).decode("utf-8")
