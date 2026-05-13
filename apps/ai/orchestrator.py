import json
import logging
from typing import Any

from django.contrib.auth.models import AnonymousUser

from apps.ai.config import settings as ai_settings
from apps.ai.core.ai_client import AIClientError
from apps.ai.core.language import detect_language
from apps.ai.core.prompts import SYSTEM_PROMPT, build_user_prompt
from apps.ai.core.slide_contract import (
    normalize_presentation_contract,
    validate_presentation_contract,
)
from apps.ai.models import AIProviderConfig
from apps.ai.providers.factory import AIProviderFactory
from apps.ai.types import AIMessage, GenerateOptions

logger = logging.getLogger(__name__)


class AIService:
    """Single application entry point for LLM-backed features."""

    def __init__(self, user: object | None = None):
        self.user = user

    def generate_presentation(self, topic: str, language: str | None = None) -> dict:
        resolved_lang = language or detect_language(topic)
        config = self._resolve_provider_config()
        provider = AIProviderFactory.from_config(config)

        logger.info(
            "Generating presentation with provider=%s type=%s model=%s",
            config.provider_name,
            config.provider_type,
            config.model_name,
        )
        response = provider.chat_completion(
            messages=[
                AIMessage(role="system", content=SYSTEM_PROMPT),
                AIMessage(role="user", content=build_user_prompt(topic, resolved_lang)),
            ],
            options=GenerateOptions(
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                timeout_ms=config.timeout_ms,
                response_format={"type": "json_object"},
            ),
        )
        data = self._parse_and_normalize_response(response.content, resolved_lang)
        logger.info(
            "Presentation ready with provider=%s slides=%d",
            response.provider_name,
            len(data["slides"]),
        )
        return data

    def test_provider(self, config: AIProviderConfig):
        provider = AIProviderFactory.from_config(config)
        return provider.test_connection()

    def _resolve_provider_config(self) -> AIProviderConfig:
        if self.user and not isinstance(self.user, AnonymousUser) and getattr(self.user, "is_authenticated", False):
            config = (
                AIProviderConfig.objects.filter(
                    owner=self.user,
                    is_active=True,
                    is_default=True,
                )
                .order_by("-updated_at")
                .first()
            )
            if config:
                return config

        env_config = AIProviderFactory.default_openai_from_env()
        if not env_config.api_key:
            raise AIClientError("No active AI provider is configured.")

        return _EnvConfigAdapter(
            provider_name=env_config.provider_name,
            provider_type=env_config.provider_type,
            base_url=env_config.base_url,
            api_key=env_config.api_key,
            model_name=env_config.model_name,
            temperature=ai_settings.OPENAI_TEMPERATURE,
            max_tokens=ai_settings.OPENAI_MAX_TOKENS,
            timeout_ms=90000,
        )

    def _parse_and_normalize_response(self, raw: str, language: str) -> dict:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise AIClientError("AI returned invalid JSON.") from exc

        if not isinstance(data, dict):
            raise AIClientError("AI returned an unexpected payload.")
        data["research_used"] = False
        data["sources"] = []

        for key in ("presentation_title", "slides"):
            if key not in data:
                raise AIClientError(f"Missing required field: '{key}'")

        slides = data["slides"]
        if not isinstance(slides, list) or len(slides) < 4:
            raise AIClientError(
                "Response must contain at least 4 slides: cover, agenda, body, and conclusion."
            )

        try:
            normalize_presentation_contract(data, language)
            validate_presentation_contract(data)
        except ValueError as exc:
            raise AIClientError(str(exc)) from exc

        return data


class _EnvConfigAdapter:
    """Looks like AIProviderConfig, but keeps env fallback out of the database."""

    def __init__(
        self,
        provider_name: str,
        provider_type: str,
        base_url: str,
        api_key: str,
        model_name: str,
        temperature: float,
        max_tokens: int,
        timeout_ms: int,
    ):
        self.provider_name = provider_name
        self.provider_type = provider_type
        self.base_url = base_url
        self._api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout_ms = timeout_ms

    def get_api_key(self) -> str:
        return self._api_key
