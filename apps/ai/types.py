from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Literal, Protocol


class ProviderType(StrEnum):
    """Supported LLM provider families."""

    OPENAI = "openai"
    OLLAMA = "ollama"
    OPENAI_COMPATIBLE = "openai_compatible"
    CUSTOM = "custom"


@dataclass(frozen=True)
class AIMessage:
    role: Literal["system", "user", "assistant"]
    content: str


@dataclass(frozen=True)
class GenerateOptions:
    temperature: float
    max_tokens: int
    timeout_ms: int
    response_format: dict[str, Any] | None = None


@dataclass(frozen=True)
class AIResponse:
    content: str
    raw: dict[str, Any]
    provider_name: str
    model_name: str


@dataclass(frozen=True)
class ConnectionResult:
    ok: bool
    message: str
    details: dict[str, Any] | None = None


class AIProvider(Protocol):
    """Common contract implemented by every LLM provider."""

    def test_connection(self) -> ConnectionResult:
        """Check endpoint, credentials, and model reachability where possible."""

    def chat_completion(
        self,
        messages: list[AIMessage],
        options: GenerateOptions,
    ) -> AIResponse:
        """Generate one non-streamed chat completion."""
