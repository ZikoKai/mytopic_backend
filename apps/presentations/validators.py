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
