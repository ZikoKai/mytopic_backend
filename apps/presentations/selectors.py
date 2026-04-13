from apps.presentations.models import PresentationRequestLog


def get_recent_requests(limit: int = 20):
    """
    Retourne les dernieres requetes de generation.

    @param limit Nombre maximal de lignes.
    @returns Queryset ordonne.
    Securite:
    - Expose un acces lecture borne.
    """
    return PresentationRequestLog.objects.order_by("-created_at")[:limit]
