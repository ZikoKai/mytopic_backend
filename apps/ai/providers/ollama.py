from dataclasses import dataclass

from apps.ai.core.ai_client import AIClientError
from apps.ai.providers.http import join_url, post_json, read_json
from apps.ai.types import AIMessage, AIResponse, ConnectionResult, GenerateOptions


@dataclass(frozen=True)
class OllamaProvider:
    provider_name: str
    base_url: str
    model_name: str

    def test_connection(self) -> ConnectionResult:
        try:
            raw = read_json(join_url(self.base_url, "/api/tags"), timeout_seconds=10)
        except AIClientError as exc:
            return ConnectionResult(ok=False, message=str(exc), details=None)

        models = raw.get("models")
        model_names = [
            str(item.get("name", "")).split(":")[0]
            for item in models
            if isinstance(item, dict)
        ] if isinstance(models, list) else []
        requested = self.model_name.split(":")[0]
        if model_names and requested not in model_names:
            return ConnectionResult(
                ok=False,
                message=f"Model '{self.model_name}' was not found on this Ollama server.",
                details={"availableModels": model_names[:20]},
            )
        return ConnectionResult(ok=True, message="Connection successful.", details=None)

    def chat_completion(
        self,
        messages: list[AIMessage],
        options: GenerateOptions,
    ) -> AIResponse:
        raw = post_json(
            url=join_url(self.base_url, "/api/chat"),
            payload={
                "model": self.model_name,
                "messages": [message.__dict__ for message in messages],
                "stream": False,
                "format": "json" if options.response_format else "",
                "options": {
                    "temperature": options.temperature,
                    "num_predict": options.max_tokens,
                },
            },
            timeout_seconds=options.timeout_ms / 1000,
        )
        message = raw.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, str) or not content.strip():
            raise AIClientError("Ollama returned an empty response.")
        return AIResponse(
            content=content.strip(),
            raw=raw,
            provider_name=self.provider_name,
            model_name=self.model_name,
        )
