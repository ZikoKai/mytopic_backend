from dataclasses import dataclass

from apps.ai.core.ai_client import AIClientError
from apps.ai.providers.http import join_url, post_json
from apps.ai.types import AIMessage, AIResponse, ConnectionResult, GenerateOptions


@dataclass(frozen=True)
class OpenAICompatibleProvider:
    provider_name: str
    base_url: str
    model_name: str
    api_key: str = ""

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            return {}
        return {"Authorization": f"Bearer {self.api_key}"}

    def test_connection(self) -> ConnectionResult:
        try:
            self.chat_completion(
                messages=[AIMessage(role="user", content="Reply with OK.")],
                options=GenerateOptions(
                    temperature=0,
                    max_tokens=8,
                    timeout_ms=10000,
                    response_format=None,
                ),
            )
        except AIClientError as exc:
            return ConnectionResult(ok=False, message=str(exc), details=None)
        return ConnectionResult(ok=True, message="Connection successful.", details=None)

    def chat_completion(
        self,
        messages: list[AIMessage],
        options: GenerateOptions,
    ) -> AIResponse:
        payload = {
            "model": self.model_name,
            "messages": [message.__dict__ for message in messages],
            "temperature": options.temperature,
            "max_tokens": options.max_tokens,
        }
        if options.response_format:
            payload["response_format"] = options.response_format

        raw = post_json(
            url=join_url(self.base_url, "/v1/chat/completions"),
            payload=payload,
            timeout_seconds=options.timeout_ms / 1000,
            headers=self._headers(),
        )
        content = _extract_chat_content(raw)
        if not content:
            raise AIClientError("Provider returned an empty response.")
        return AIResponse(
            content=content,
            raw=raw,
            provider_name=self.provider_name,
            model_name=self.model_name,
        )


class OpenAIProvider(OpenAICompatibleProvider):
    def __init__(self, provider_name: str, model_name: str, api_key: str, base_url: str = ""):
        super().__init__(
            provider_name=provider_name,
            base_url=base_url or "https://api.openai.com",
            model_name=model_name,
            api_key=api_key,
        )


def _extract_chat_content(raw: dict) -> str:
    choices = raw.get("choices")
    if not isinstance(choices, list) or not choices:
        return ""
    first = choices[0]
    if not isinstance(first, dict):
        return ""
    message = first.get("message")
    if not isinstance(message, dict):
        return ""
    content = message.get("content")
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"].strip())
        return "\n".join(part for part in parts if part)
    return ""
