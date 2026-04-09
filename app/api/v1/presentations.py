import logging

from fastapi import APIRouter, HTTPException

from app.schemas.presentation import GenerateRequest, PresentationResponse
from app.services.ai_client import generate_presentation, AIClientError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/presentations", tags=["Presentations"])


@router.post(
    "/generate",
    response_model=PresentationResponse,
    summary="Generate an AI presentation",
    description="Accepts a topic and optional language, returns a structured presentation.",
)
async def generate(payload: GenerateRequest):
    try:
        data = generate_presentation(
            topic=payload.topic,
            language=payload.language,
        )
    except AIClientError as exc:
        logger.error("Generation failed: %s", exc)
        raise HTTPException(status_code=502, detail=str(exc))

    return data
