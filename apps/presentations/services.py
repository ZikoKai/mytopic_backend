from apps.ai.services import AIClientError, build_image_from_prompt, build_presentation


def generate_topic_presentation(topic: str, language: str | None) -> dict:
    """
    Service metier presentations.

    @param topic Sujet a transformer en deck.
    @param language Langue cible optionnelle.
    @returns Presentation JSON complete.
    Securite:
    - Point d'orchestration unique pour encapsuler les erreurs AI.
    """
    return build_presentation(topic=topic, language=language)


def generate_image_for_presentation(prompt: str, size: str = "1024x1024") -> dict[str, str]:
    """
    Service metier texte -> image pour l'editeur de presentation.

    @param prompt Description textuelle de l'image.
    @param size Format cible.
    @returns image_data_url + mime_type.
    """
    return build_image_from_prompt(prompt=prompt, size=size)


__all__ = [
    "AIClientError",
    "generate_topic_presentation",
    "generate_image_for_presentation",
]
