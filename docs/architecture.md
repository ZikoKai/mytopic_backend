# Architecture Django REST

- `config/` contient la configuration Django (settings, urls, asgi, wsgi).
- `api/v1/` expose les routes versionnees.
- `apps/presentations/` contient l'endpoint de generation.
- `apps/ai/` encapsule l'appel au moteur AI existant.
- `apps/ai/core/` contient le moteur de prompt + contrat slides + client OpenAI.
