class ApplicationError(Exception):
    """
    Base application exception.

    Securite:
    - Utilisee pour controler les erreurs metier sans exposer des traces internes.
    """
