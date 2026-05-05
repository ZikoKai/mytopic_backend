import json
import logging
from typing import Any
from urllib import error as urllib_error
from urllib import request as urllib_request

from apps.ai.core.language import detect_language
from apps.ai.core.prompts import SYSTEM_PROMPT, build_user_prompt
from apps.ai.core.slide_contract import (
    normalize_presentation_contract,
    validate_presentation_contract,
)

logger = logging.getLogger(__name__)


class AIClientError(Exception):
    """Raised when the AI provider returns an unusable response."""


def _get_ai_settings():
    """
    Charge la configuration IA a la demande.

    Evite de charger pydantic/pydantic_core pendant l'initialisation Django
    si l'environnement bloque les DLL natives.
    """
    try:
        from apps.ai.config import settings
    except Exception as exc:
        raise AIClientError(
            "AI settings are unavailable in this environment (blocked DLL or missing dependency)."
        ) from exc

    return settings


def _post_openai_json(endpoint: str, payload: dict[str, Any], api_key: str) -> dict[str, Any]:
    url = f"https://api.openai.com/v1/{endpoint.lstrip('/')}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib_request.Request(
        url=url,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib_request.urlopen(req, timeout=90) as response:
            body = response.read().decode("utf-8")
    except urllib_error.HTTPError as exc:
        detail = ""
        try:
            raw = exc.read().decode("utf-8")
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                err = parsed.get("error")
                if isinstance(err, dict):
                    detail = str(err.get("message", "")).strip()
        except Exception:
            detail = ""

        if not detail:
            detail = f"HTTP {exc.code}"
        raise AIClientError(f"AI provider error: {detail}") from exc
    except Exception as exc:
        raise AIClientError(f"AI provider error: {exc}") from exc

    try:
        parsed_body = json.loads(body)
    except json.JSONDecodeError as exc:
        raise AIClientError("AI provider returned invalid JSON.") from exc

    if not isinstance(parsed_body, dict):
        raise AIClientError("AI provider returned an unexpected payload.")

    return parsed_body


def generate_image(prompt: str, size: str = "1024x1024") -> dict[str, str]:
    """
    Genere une image a partir d'un prompt texte.

    @param prompt Description textuelle de l'image souhaitee.
    @param size Taille d'image OpenAI (ex: 1024x1024).
    @returns Dictionnaire contenant la data URL et le mime type.
    Securite:
    - Rejette les prompts vides.
    - Encapsule les erreurs provider.
    """
    cleaned_prompt = prompt.strip()
    if not cleaned_prompt:
        raise AIClientError("Prompt is required.")

    ai_settings = _get_ai_settings()

    if not ai_settings.OPENAI_API_KEY:
        raise AIClientError("OpenAI API key is not configured.")

    response = _post_openai_json(
        endpoint="images/generations",
        payload={
            "model": "gpt-image-1",
            "prompt": cleaned_prompt,
            "size": size,
        },
        api_key=ai_settings.OPENAI_API_KEY,
    )

    data = response.get("data")
    if not isinstance(data, list) or not data:
        raise AIClientError("AI returned no image data.")

    first_item = data[0]
    b64_json = first_item.get("b64_json") if isinstance(first_item, dict) else None
    if not isinstance(b64_json, str) or not b64_json.strip():
        raise AIClientError("AI returned invalid image payload.")

    mime_type = "image/png"
    data_url = f"data:{mime_type};base64,{b64_json.strip()}"
    return {"image_data_url": data_url, "mime_type": mime_type}


def generate_presentation(topic: str, language: str | None = None) -> dict:
    """
    Call OpenAI and return the parsed presentation dict.

    1. Detect language if not provided.
    2. Build the prompt pair.
    3. Call the Responses API without web browsing tools.
    4. Parse, validate, normalize, and enforce structure.
    """
    ai_settings = _get_ai_settings()

    if not ai_settings.OPENAI_API_KEY:
        raise AIClientError("OpenAI API key is not configured.")

    resolved_lang = language or detect_language(topic)
    logger.info(
        "Generating presentation - topic=%r lang=%s web_search=%s",
        topic,
        resolved_lang,
        False,
    )

    response = _post_openai_json(
        endpoint="chat/completions",
        payload=_build_response_request(topic, resolved_lang),
        api_key=ai_settings.OPENAI_API_KEY,
    )

    data = _parse_and_normalize_response(response, resolved_lang)

    logger.info(
        "Presentation ready - %d slides research_used=%s sources=%d",
        len(data["slides"]),
        data["research_used"],
        len(data["sources"]),
    )
    return data


def _build_response_request(topic: str, language: str) -> dict[str, Any]:
    ai_settings = _get_ai_settings()
    return {
        "model": ai_settings.OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(topic, language)},
        ],
        "temperature": ai_settings.OPENAI_TEMPERATURE,
        "max_tokens": ai_settings.OPENAI_MAX_TOKENS,
        "response_format": {"type": "json_object"},
    }


def _format_provider_error(exc: Exception) -> str:
    return f"AI provider error: {exc}"


def _extract_output_text(response: Any) -> str:
    if not isinstance(response, dict):
        return ""

    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        return ""

    message = choices[0].get("message") if isinstance(choices[0], dict) else None
    if not isinstance(message, dict):
        return ""

    content = message.get("content")
    if isinstance(content, str) and content.strip():
        return content.strip()

    if isinstance(content, list):
        chunks: list[str] = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str) and text.strip():
                    chunks.append(text.strip())
        if chunks:
            return "\n".join(chunks)

    return ""


def _parse_and_normalize_response(response: Any, language: str) -> dict:
    """
    Extrait, parse et normalise une reponse brute du provider.

    Securite:
    - Rejette les reponses vides ou JSON invalides.
    - Applique validation contractuelle avant retour applicatif.
    """
    raw = _extract_output_text(response)
    if not raw:
        raise AIClientError("AI returned an empty response.")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise AIClientError("AI returned invalid JSON.") from exc

    data["research_used"] = False
    data["sources"] = []

    _validate(data)

    try:
        normalize_presentation_contract(data, language)
        validate_presentation_contract(data)
    except ValueError as exc:
        raise AIClientError(str(exc)) from exc

    return data


def _validate(data: dict) -> None:
    for key in ("presentation_title", "slides"):
        if key not in data:
            raise AIClientError(f"Missing required field: '{key}'")

    slides = data["slides"]
    if not isinstance(slides, list) or len(slides) < 4:
        raise AIClientError(
            "Response must contain at least 4 slides: cover, agenda, body, and conclusion."
        )

    for index, slide in enumerate(slides, start=1):
        if "title" not in slide:
            raise AIClientError(f"Slide {index} missing 'title'.")
        if "main_content" not in slide or not slide["main_content"]:
            raise AIClientError(f"Slide {index} missing 'main_content'.")
