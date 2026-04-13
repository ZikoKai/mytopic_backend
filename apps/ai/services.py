from apps.ai.core.ai_client import AIClientError, generate_presentation


def build_presentation(topic: str, language: str | None = None) -> dict:
    """
    Facade AI pour la generation de presentation.

    @param topic Sujet principal de generation.
    @param language Langue cible optionnelle.
    @returns Presentation JSON normalisee.
    Securite:
    - Delègue a un service valide qui applique parse + validation du contrat.
    """
    return generate_presentation(topic=topic, language=language)


__all__ = ["AIClientError", "build_presentation"]
