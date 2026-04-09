from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file."""

    # --- Application ---
    APP_NAME: str = "MyTopic API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # --- CORS ---
    CORS_ORIGINS: list[str] = ["*"]

    # --- OpenAI ---
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API secret key")
    OPENAI_MODEL: str = "gpt-4.1-mini"
    OPENAI_TEMPERATURE: float = 0.85
    OPENAI_MAX_TOKENS: int = 5000

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


settings = Settings()
