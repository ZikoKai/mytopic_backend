# MyTopic Backend (Django REST)

Backend Django REST qui genere des presentations dynamiques a partir d'un sujet.

## Stack

- Django
- Django REST Framework
- OpenAI SDK
- Pydantic settings (configuration AI)
- langdetect

## Structure principale

```text
mytopic_backend/
├── manage.py
├── config/
│   ├── urls.py
│   └── settings/
│       ├── base.py
│       ├── dev.py
│       └── prod.py
├── api/
│   └── v1/urls.py
├── apps/
│   ├── ai/services.py
│   ├── common/
│   └── presentations/
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
├── apps/ai/core/  # moteur AI (prompts, contrat slides, client OpenAI)
└── requirements/
    ├── base.txt
    ├── dev.txt
    └── prod.txt
```

## Installation

```powershell
cd mytopic_backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuration `.env`

```env
DEBUG=True
DJANGO_SECRET_KEY=change-me
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ORIGINS=http://localhost:5173

OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini
OPENAI_TEMPERATURE=0.85
OPENAI_MAX_TOKENS=5000
```

## Lancer le backend

```powershell
cd mytopic_backend
.\venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## Endpoints

- `GET /health`
- `POST /api/v1/presentations/generate`

Exemple payload:

```json
{
  "topic": "Intelligence artificielle",
  "language": "French"
}
```

## Notes migration

- FastAPI a ete retire du runtime.
- L'endpoint frontend reste identique (`/api/v1/presentations/generate`).
- Le pipeline AI conserve la logique de normalisation/validation dynamique des slides.
