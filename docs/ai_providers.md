# AI Providers

MyTopic routes presentation generation through `apps.ai.orchestrator.AIService`.
Application code should call `build_presentation(..., user=request.user)` and never call
a concrete LLM SDK directly.

## Flow

Frontend settings call `/api/v1/ai/providers`.
Generation calls `/api/v1/presentations/generate`.

At runtime:

`AIService -> AIProviderFactory -> OpenAIProvider | OllamaProvider | OpenAICompatibleProvider`

If the user has an active default provider, it is used. Otherwise the legacy
OpenAI environment variables remain the fallback, so existing generation keeps
working.

## Secrets

Provider API keys are accepted only as write-only `apiKey` input. They are
encrypted with Fernet before being stored in `ai_provider_configs.encrypted_api_key`.
Responses expose only `hasApiKey`.

Server logs must not include prompts or API keys. Current provider logs include
only provider id/name/type/model and operation status.

## Adding A Provider

1. Add a new value to `ProviderType` in `apps/ai/types.py`.
2. Implement the `AIProvider` protocol: `test_connection()` and `chat_completion()`.
3. Register it in `AIProviderFactory.from_config`.
4. Add validation rules in `AIProviderConfigSerializer` if the provider needs
   special fields.
5. Add a focused unit test in `apps/ai/tests`.

## Ollama Notes

Ollama uses:

- `GET /api/tags` for connection/model checks.
- `POST /api/chat` for non-streamed chat generation.

When the app is hosted on Vercel or another remote server, `localhost` means the
server itself, not the user's laptop. Users must provide a server-reachable
network URL such as `http://10.0.0.45:11434`, deploy MyTopic inside the customer
network, or use a future local agent/private tunnel.
