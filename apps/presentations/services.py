from apps.ai.services import AIClientError, build_presentation


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


__all__ = ["AIClientError", "generate_topic_presentation"]
