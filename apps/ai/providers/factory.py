from dataclasses import dataclass

from apps.ai.config import settings as ai_settings
from apps.ai.models import AIProviderConfig
from apps.ai.providers.ollama import OllamaProvider
from apps.ai.providers.openai_compatible import OpenAICompatibleProvider, OpenAIProvider
from apps.ai.types import ProviderType


@dataclass(frozen=True)
class RuntimeProviderConfig:
    provider_name: str
    provider_type: str
    base_url: str
    api_key: str
    model_name: str


class AIProviderFactory:
    """Creates concrete LLM providers from persisted or env configuration."""

    @staticmethod
    def from_config(config: AIProviderConfig | RuntimeProviderConfig):
        provider_type = ProviderType(config.provider_type)
        api_key = (
            config.get_api_key()
            if hasattr(config, "get_api_key")
            else getattr(config, "api_key", "")
        )

        if provider_type == ProviderType.OPENAI:
            return OpenAIProvider(
                provider_name=config.provider_name,
                model_name=config.model_name,
                api_key=api_key,
                base_url=config.base_url,
            )
        if provider_type == ProviderType.OLLAMA:
            return OllamaProvider(
                provider_name=config.provider_name,
                base_url=config.base_url,
                model_name=config.model_name,
            )
        if provider_type in {ProviderType.OPENAI_COMPATIBLE, ProviderType.CUSTOM}:
            return OpenAICompatibleProvider(
                provider_name=config.provider_name,
                base_url=config.base_url,
                model_name=config.model_name,
                api_key=api_key,
            )

        raise ValueError(f"Unsupported provider type: {config.provider_type}")

    @staticmethod
    def default_openai_from_env() -> RuntimeProviderConfig:
        return RuntimeProviderConfig(
            provider_name="OpenAI default",
            provider_type=ProviderType.OPENAI.value,
            base_url="https://api.openai.com",
            api_key=ai_settings.OPENAI_API_KEY,
            model_name=ai_settings.OPENAI_MODEL,
        )
