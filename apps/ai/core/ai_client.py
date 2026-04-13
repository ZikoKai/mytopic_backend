import json
import logging
from typing import Any

from openai import OpenAI

from apps.ai.config import settings
from apps.ai.core.language import detect_language
from apps.ai.core.prompts import SYSTEM_PROMPT, build_user_prompt
from apps.ai.core.slide_contract import (
    normalize_presentation_contract,
    validate_presentation_contract,
)

logger = logging.getLogger(__name__)


class AIClientError(Exception):
    """Raised when the AI provider returns an unusable response."""


def generate_presentation(topic: str, language: str | None = None) -> dict:
    """
    Call OpenAI and return the parsed presentation dict.

    1. Detect language if not provided.
    2. Build the prompt pair.
    3. Call the Responses API without web browsing tools.
    4. Parse, validate, normalize, and enforce structure.
    """
    if not settings.OPENAI_API_KEY:
        raise AIClientError("OpenAI API key is not configured.")

    resolved_lang = language or detect_language(topic)
    logger.info(
        "Generating presentation - topic=%r lang=%s web_search=%s",
        topic,
        resolved_lang,
        False,
    )

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    try:
        response = client.responses.create(**_build_response_request(topic, resolved_lang))
    except Exception as exc:
        logger.exception("OpenAI API call failed")
        raise AIClientError(_format_provider_error(exc)) from exc

    data = _parse_and_normalize_response(response, resolved_lang)

    logger.info(
        "Presentation ready - %d slides research_used=%s sources=%d",
        len(data["slides"]),
        data["research_used"],
        len(data["sources"]),
    )
    return data


def _build_response_request(topic: str, language: str) -> dict[str, Any]:
    return {
        "model": settings.OPENAI_MODEL,
        "instructions": SYSTEM_PROMPT,
        "input": build_user_prompt(topic, language),
        "temperature": settings.OPENAI_TEMPERATURE,
        "max_output_tokens": settings.OPENAI_MAX_TOKENS,
    }


def _format_provider_error(exc: Exception) -> str:
    return f"AI provider error: {exc}"


def _extract_output_text(response: Any) -> str:
    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

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
