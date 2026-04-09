# MyTopic Backend

API FastAPI qui genere des presentations structurees a partir d'un sujet en s'appuyant sur OpenAI.

## Vue d'ensemble

Le backend recoit un sujet depuis le frontend, detecte la langue si besoin, construit un prompt complet, appelle OpenAI, puis retourne une presentation JSON prete a etre affichee en slides.

Fonctionnalites principales :

- generation de presentations entre 8 et 14 slides
- detection automatique de la langue du sujet
- sortie JSON normalisee pour le frontend
- documentation interactive avec Swagger
- endpoint de sante pour verifier que l'API tourne

## Stack technique

- Python
- FastAPI
- Pydantic / Pydantic Settings
- OpenAI Python SDK
- langdetect
- Uvicorn

## Structure du projet

```text
mytopic_backend/
├── app/
│   ├── api/
│   │   ├── router.py
│   │   └── v1/presentations.py
│   ├── schemas/presentation.py
│   ├── services/
│   │   ├── ai_client.py
│   │   ├── language.py
│   │   └── prompts.py
│   ├── config.py
│   └── main.py
├── requirements.txt
├── run.py
└── README.md
```

## Flux de fonctionnement

1. Le frontend envoie un `topic` et eventuellement une `language`.
2. Le backend valide la requete avec `GenerateRequest`.
3. Si la langue est absente, elle est detectee automatiquement.
4. Le service `ai_client.py` construit les prompts et appelle OpenAI.
5. La reponse JSON est validee, normalisee, puis retournee au frontend.

## Installation

```powershell
cd mytopic_backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuration

Creez un fichier `.env` a la racine de `mytopic_backend` :

```env
APP_NAME=MyTopic API
APP_VERSION=1.0.0
DEBUG=True
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini
OPENAI_TEMPERATURE=0.85
OPENAI_MAX_TOKENS=5000
```

Variables importantes :

- `OPENAI_API_KEY` : cle API OpenAI obligatoire
- `OPENAI_MODEL` : modele utilise pour la generation
- `OPENAI_TEMPERATURE` : niveau de creativite de la reponse
- `OPENAI_MAX_TOKENS` : limite de tokens retournee par le modele
- `CORS_ORIGINS` : origines autorisees pour le frontend

## Lancer le serveur

```powershell
cd mytopic_backend
.\venv\Scripts\Activate.ps1
python run.py
```

Le serveur demarre par defaut sur :

- API : `http://localhost:8000`
- Swagger UI : `http://localhost:8000/docs`
- ReDoc : `http://localhost:8000/redoc`
- Health check : `http://localhost:8000/health`

## Endpoints principaux

### `POST /api/v1/presentations/generate`

Genere une presentation a partir d'un sujet.

Exemple de requete :

```json
{
  "topic": "L'intelligence artificielle dans la sante",
  "language": "French"
}
```

Le champ `language` est optionnel. S'il est omis, la langue est detectee a partir du sujet.

Exemple de reponse :

```json
{
  "language": "French",
  "presentation_title": "L'intelligence artificielle dans la sante",
  "presentation_subtitle": "Usages, opportunites et limites",
  "target_audience": "General",
  "presentation_goal": "inform",
  "tone": "professional",
  "slides": [
    {
      "slide_number": 1,
      "slide_type": "cover",
      "title": "Pourquoi l'IA transforme deja la sante",
      "purpose": "Introduire le sujet",
      "content_format": "paragraph",
      "main_content": ["Une vue d'ensemble du sujet."],
      "speaker_notes": "Notes du presentateur",
      "suggested_visual": "Illustration d'un hopital numerique",
      "transition_to_next": "Passer au plan"
    }
  ]
}
```

### `GET /health`

Retourne l'etat du service et la version de l'application.

## Points techniques utiles

- `app/main.py` cree l'application FastAPI et configure le CORS.
- `app/api/v1/presentations.py` expose l'endpoint de generation.
- `app/services/prompts.py` contient le prompt systeme et le prompt utilisateur.
- `app/services/language.py` gere la detection de langue.
- `app/services/ai_client.py` centralise l'appel OpenAI, la validation et la normalisation de la reponse.

## Integration avec le frontend

Le frontend appelle l'endpoint :

```text
http://localhost:8000/api/v1/presentations/generate
```

Assurez-vous que le backend tourne sur le port `8000`, sinon il faudra ajuster l'URL dans le frontend.

## Erreurs possibles

- absence de `OPENAI_API_KEY`
- erreur de connexion a OpenAI
- JSON invalide retourne par le modele
- structure incomplete dans la reponse generee

Dans ces cas, l'API retourne une erreur HTTP `502`.
