def validate_topic(topic: str) -> str:
    """
    Valide et nettoie le sujet de presentation.

    @param topic Sujet brut en entree.
    @returns Sujet nettoye.
    Securite:
    - Limite les entrees vides et trop longues.
    """
    cleaned = topic.strip()
    if not cleaned:
        raise ValueError("Topic is required.")
    if len(cleaned) > 500:
        raise ValueError("Topic exceeds max length.")
    return cleaned


def validate_presentation_content(content: object) -> dict:
    """Valide la structure minimale d'une presentation persistable."""

    if not isinstance(content, dict):
        raise ValueError("Content must be a JSON object.")

    slides = content.get("slides")
    if not isinstance(slides, list) or not slides:
        raise ValueError("Content.slides must be a non-empty array.")

    for index, slide in enumerate(slides):
        if not isinstance(slide, dict):
            raise ValueError(f"Slide #{index + 1} must be an object.")

        title = str(slide.get("title", "")).strip()
        if not title:
            raise ValueError(f"Slide #{index + 1} title is required.")

        scene = slide.get("editor_scene")
        if scene is None:
            continue

        if not isinstance(scene, dict):
            raise ValueError(f"Slide #{index + 1} editor_scene must be an object.")

        elements = scene.get("elements")
        if not isinstance(elements, list):
            raise ValueError(f"Slide #{index + 1} editor_scene.elements must be an array.")

        for element_index, element in enumerate(elements):
            if not isinstance(element, dict):
                raise ValueError(
                    f"Slide #{index + 1} element #{element_index + 1} must be an object."
                )

            element_id = str(element.get("id", "")).strip()
            if not element_id:
                raise ValueError(
                    f"Slide #{index + 1} element #{element_index + 1} id is required."
                )

            element_type = str(element.get("type", "")).strip()
            if element_type not in {
                "text",
                "shape",
                "list",
                "table",
                "media",
                "icon",
                "chart",
                "columns",
                "group",
                "background",
            }:
                raise ValueError(
                    f"Slide #{index + 1} element #{element_index + 1} has invalid type."
                )

    return content
