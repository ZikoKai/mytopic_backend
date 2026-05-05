from apps.ai.core.ai_client import AIClientError, generate_image, generate_presentation


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


def build_image_from_prompt(prompt: str, size: str = "1024x1024") -> dict[str, str]:
    """
    Facade AI pour la generation d'image texte -> image.

    @param prompt Prompt texte.
    @param size Taille OpenAI demandee.
    @returns image_data_url + mime_type.
    """
    return generate_image(prompt=prompt, size=size)


__all__ = ["AIClientError", "build_presentation", "build_image_from_prompt"]
