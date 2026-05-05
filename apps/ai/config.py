import os
from dataclasses import dataclass


def _load_env_file() -> None:
    """Best-effort .env loading without hard dependency at import time."""
    try:
        from dotenv import load_dotenv
    except Exception:
        return

    load_dotenv()


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _as_float(value: str | None, default: float) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _as_int(value: str | None, default: int) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _as_list(value: str | None, default: list[str]) -> list[str]:
    if value is None:
        return default
    parts = [item.strip() for item in value.split(",")]
    return [item for item in parts if item] or default


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables / .env file."""

    APP_NAME: str = "MyTopic API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    CORS_ORIGINS: list[str] | tuple[str, ...] = ("*",)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4.1"
    OPENAI_TEMPERATURE: float = 0.85
    OPENAI_MAX_TOKENS: int = 5000
    OPENAI_ENABLE_WEB_SEARCH: bool = False


def _build_settings() -> Settings:
    _load_env_file()
    return Settings(
        APP_NAME=os.getenv("APP_NAME", "MyTopic API"),
        APP_VERSION=os.getenv("APP_VERSION", "1.0.0"),
        DEBUG=_as_bool(os.getenv("DEBUG"), default=False),
        CORS_ORIGINS=_as_list(os.getenv("CORS_ORIGINS"), default=["*"]),
        OPENAI_API_KEY=os.getenv("OPENAI_API_KEY", "").strip(),
        OPENAI_MODEL=os.getenv("OPENAI_MODEL", "gpt-4.1").strip() or "gpt-4.1",
        OPENAI_TEMPERATURE=_as_float(os.getenv("OPENAI_TEMPERATURE"), default=0.85),
        OPENAI_MAX_TOKENS=_as_int(os.getenv("OPENAI_MAX_TOKENS"), default=5000),
        OPENAI_ENABLE_WEB_SEARCH=_as_bool(
            os.getenv("OPENAI_ENABLE_WEB_SEARCH"),
            default=False,
        ),
    )


settings = _build_settings()
