from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    """Payload sent by the frontend to generate a presentation."""

    topic: str = Field(
        ...,
        min_length=1,
        max_length=500,
        examples=["L'intelligence artificielle dans la sante"],
    )
    language: str | None = Field(
        default=None,
        description="Target language. Auto-detected from topic when omitted.",
    )


class SlideResponse(BaseModel):
    """Schema for a single slide returned by the AI."""

    slide_number: int
    slide_type: str
    title: str
    purpose: str
    content_format: str
    main_content: list[str]
    speaker_notes: str
    suggested_visual: str | None = None
    transition_to_next: str


class PresentationResponse(BaseModel):
    """Full presentation payload returned to the frontend."""

    language: str
    presentation_title: str
    presentation_subtitle: str
    target_audience: str
    presentation_goal: str
    tone: str
    slides: list[SlideResponse]
