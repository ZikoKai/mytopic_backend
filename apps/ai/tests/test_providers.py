from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.ai.models import AIProviderConfig
from apps.ai.providers.factory import AIProviderFactory
from apps.ai.providers.ollama import OllamaProvider
from apps.ai.providers.openai_compatible import OpenAICompatibleProvider, OpenAIProvider


class AIProviderFactoryTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="provider-user",
            email="provider@example.com",
            password="pass",
        )

    def make_config(self, provider_type: str, base_url: str = "http://localhost:11434"):
        config = AIProviderConfig(
            owner=self.user,
            provider_name="Test provider",
            provider_type=provider_type,
            base_url=base_url,
            model_name="test-model",
        )
        config.set_api_key("secret-key")
        return config

    def test_factory_creates_openai_provider(self) -> None:
        provider = AIProviderFactory.from_config(
            self.make_config("openai", base_url=""),
        )
        self.assertIsInstance(provider, OpenAIProvider)

    def test_factory_creates_ollama_provider(self) -> None:
        provider = AIProviderFactory.from_config(self.make_config("ollama"))
        self.assertIsInstance(provider, OllamaProvider)

    def test_factory_creates_openai_compatible_provider(self) -> None:
        provider = AIProviderFactory.from_config(
            self.make_config("openai_compatible", base_url="http://llm.internal"),
        )
        self.assertIsInstance(provider, OpenAICompatibleProvider)

    def test_api_key_is_encrypted_at_rest(self) -> None:
        config = self.make_config("openai_compatible")
        config.save()
        self.assertNotIn("secret-key", config.encrypted_api_key)
        self.assertEqual(config.get_api_key(), "secret-key")
