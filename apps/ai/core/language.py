from langdetect import detect, LangDetectException

_LANGUAGE_MAP = {
    "fr": "French",
    "en": "English",
    "es": "Spanish",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "nl": "Dutch",
    "ar": "Arabic",
    "zh-cn": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ru": "Russian",
}


def detect_language(text: str) -> str:
    """Return the full language name for *text*. Falls back to English."""
    try:
        code = detect(text)
        return _LANGUAGE_MAP.get(code, "English")
    except LangDetectException:
        return "English"
