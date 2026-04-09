import json
import logging

from openai import OpenAI

from app.config import settings
from app.services.prompts import SYSTEM_PROMPT, build_user_prompt
from app.services.language import detect_language

logger = logging.getLogger(__name__)

ALLOWED_SLIDE_TYPES = {
    "cover",
    "agenda",
    "introduction",
    "content",
    "synthesis",
    "conclusion",
    "optional",
}

ALLOWED_CONTENT_FORMATS = {
    "paragraph",
    "bullets",
    "definition",
    "comparison",
    "table",
    "timeline",
    "mixed",
}


class AIClientError(Exception):
    """Raised when the AI provider returns an unusable response."""


def generate_presentation(topic: str, language: str | None = None) -> dict:
    """
    Call OpenAI and return the parsed presentation dict.

    1. Detect language if not provided.
    2. Build the prompt pair.
    3. Call the API with JSON mode.
    4. Parse, validate, and normalize the response.
    """
    if not settings.OPENAI_API_KEY:
        raise AIClientError("OpenAI API key is not configured.")

    resolved_lang = language or detect_language(topic)
    logger.info("Generating presentation — topic=%r  lang=%s", topic, resolved_lang)

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(topic, resolved_lang)},
            ],
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS,
            response_format={"type": "json_object"},
        )
    except Exception as exc:
        logger.exception("OpenAI API call failed")
        raise AIClientError(f"AI provider error: {exc}") from exc

    raw = response.choices[0].message.content

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise AIClientError("AI returned invalid JSON.") from exc

    _validate(data)
    _normalize(data, resolved_lang)

    logger.info("Presentation ready — %d slides", len(data["slides"]))
    return data


def _validate(data: dict) -> None:
    for key in ("presentation_title", "slides"):
        if key not in data:
            raise AIClientError(f"Missing required field: '{key}'")

    slides = data["slides"]
    if not isinstance(slides, list) or len(slides) < 1:
        raise AIClientError("Response must contain at least one slide.")

    for i, slide in enumerate(slides, start=1):
        if "title" not in slide:
            raise AIClientError(f"Slide {i} missing 'title'.")
        if "main_content" not in slide or not slide["main_content"]:
            raise AIClientError(f"Slide {i} missing 'main_content'.")


def _normalize(data: dict, language: str) -> None:
    data.setdefault("language", language)
    data.setdefault("presentation_subtitle", "")
    data.setdefault("target_audience", "General")
    data.setdefault("presentation_goal", "inform")
    data.setdefault("tone", "professional")

    for index, slide in enumerate(data["slides"], start=1):
        slide_number = slide.get("slide_number")
        slide["slide_number"] = slide_number if isinstance(slide_number, int) and slide_number > 0 else index

        slide_type = str(slide.get("slide_type", "content")).strip().lower()
        slide["slide_type"] = slide_type if slide_type in ALLOWED_SLIDE_TYPES else "content"

        content_format = str(slide.get("content_format", "paragraph")).strip().lower()
        slide["content_format"] = (
            content_format if content_format in ALLOWED_CONTENT_FORMATS else "paragraph"
        )

        slide["title"] = str(slide.get("title", "")).strip()
        slide["purpose"] = str(slide.get("purpose", "")).strip()
        slide["speaker_notes"] = str(slide.get("speaker_notes", "")).strip()
        slide["transition_to_next"] = str(slide.get("transition_to_next", "")).strip()

        suggested_visual = slide.get("suggested_visual")
        slide["suggested_visual"] = (
            str(suggested_visual).strip() if suggested_visual not in (None, "") else None
        )

        raw_main_content = slide.get("main_content", [])
        if not isinstance(raw_main_content, list):
            raw_main_content = [raw_main_content]

        slide["main_content"] = [
            str(item).strip() for item in raw_main_content if str(item).strip()
        ] or [slide["purpose"] or slide["title"]]
