import re
import unicodedata
from typing import Any

ALLOWED_SLIDE_TYPES = {
    "cover",
    "agenda",
    "section",
    "introduction",
    "content",
    "synthesis",
    "conclusion",
    "closing",
    "optional",
}

ALLOWED_CONTENT_FORMATS = {
    "paragraph",
    "bullets",
    "definition",
    "comparison",
    "table",
    "timeline",
    "mixed",
    "quote",
    "kpi",
    "process",
    "workflow",
}

ALLOWED_SEMANTIC_TYPES = {
    "cover.title",
    "section.agenda",
    "section.transition",
    "content.paragraph",
    "content.definition",
    "content.definition_list",
    "content.multi_paragraph",
    "content.quote",
    "content.info_box",
    "list.bullets",
    "list.numbered",
    "list.takeaways",
    "list.pros_cons",
    "comparison.two_column",
    "comparison.before_after",
    "comparison.concepts",
    "comparison.solutions",
    "data.table",
    "data.comparative_table",
    "data.matrix",
    "data.kpi",
    "data.cards",
    "visual.image_text",
    "visual.overlay",
    "visual.illustration",
    "visual.gallery",
    "diagram.timeline",
    "diagram.process",
    "diagram.workflow",
    "diagram.orgchart",
    "diagram.cause_effect",
    "business.problem_solution",
    "business.objectives_results",
    "business.use_case",
    "business.roadmap",
    "business.architecture",
    "business.product_feature",
    "academic.definition",
    "academic.explanation",
    "academic.case_study",
    "academic.summary",
    "academic.qa",
    "closure.conclusion",
    "closure.thank_you",
}

ALLOWED_LAYOUT_VARIANTS = {
    "hero-center",
    "hero-split",
    "agenda-grid",
    "section-band",
    "text-left-accent",
    "text-two-column",
    "quote-focus",
    "info-highlight",
    "list-grid",
    "list-numbered",
    "comparison-dual",
    "comparison-before-after",
    "table-clean",
    "matrix-grid",
    "stats-strip",
    "cards-grid",
    "visual-split",
    "visual-overlay",
    "visual-mosaic",
    "timeline-horizontal",
    "timeline-vertical",
    "process-steps",
    "workflow-flow",
    "architecture-map",
    "problem-solution",
    "objective-results",
    "roadmap-track",
    "qa-focus",
    "closing-minimal",
}

ALLOWED_DENSITIES = {"compact", "balanced", "expanded"}

DEFAULT_THEME = "editorial-light"
DEFAULT_SCHEMA_VERSION = "2026-04"
MAX_AGENDA_ITEMS = 12
MAX_AGENDA_WORDS = 4
MIN_CONCLUSION_SENTENCES = 2
MAX_CONCLUSION_SENTENCES = 4

AGENDA_TITLE_BY_LANGUAGE = {
    "French": "Plan",
    "English": "Agenda",
    "Spanish": "Plan",
    "Portuguese": "Plano",
    "Italian": "Piano",
    "German": "Gliederung",
    "Dutch": "Plan",
    "Arabic": "Agenda",
}

CONCLUSION_TITLE_BY_LANGUAGE = {
    "French": "Conclusion",
    "English": "Conclusion",
    "Spanish": "Conclusion",
    "Portuguese": "Conclusao",
    "Italian": "Conclusione",
    "German": "Fazit",
    "Dutch": "Conclusie",
    "Arabic": "Conclusion",
}

THANK_YOU_TITLE_BY_LANGUAGE = {
    "French": "Merci",
    "English": "Thank you",
    "Spanish": "Gracias",
    "Portuguese": "Obrigado",
    "Italian": "Grazie",
    "German": "Danke",
    "Dutch": "Bedankt",
    "Arabic": "Thank you",
}

AGENDA_ITEM_SPLIT_PATTERN = re.compile(r"\s*(?:\u2014|\u2013|:|-)\s*", re.UNICODE)
AGENDA_NUMBERING_PATTERN = re.compile(r"^\s*(?:\d+[\).:-]?\s*|[-*]\s*)")

SEMANTIC_ALIASES = {
    "cover": "cover.title",
    "agenda": "section.agenda",
    "transition": "section.transition",
    "paragraph": "content.paragraph",
    "definition": "content.definition",
    "definitions": "content.definition_list",
    "multi_paragraph": "content.multi_paragraph",
    "quote": "content.quote",
    "info_box": "content.info_box",
    "bullets": "list.bullets",
    "numbered": "list.numbered",
    "takeaways": "list.takeaways",
    "pros_cons": "list.pros_cons",
    "comparison": "comparison.two_column",
    "before_after": "comparison.before_after",
    "matrix": "data.matrix",
    "table": "data.table",
    "kpi": "data.kpi",
    "cards": "data.cards",
    "image_text": "visual.image_text",
    "overlay": "visual.overlay",
    "illustration": "visual.illustration",
    "gallery": "visual.gallery",
    "timeline": "diagram.timeline",
    "process": "diagram.process",
    "workflow": "diagram.workflow",
    "orgchart": "diagram.orgchart",
    "cause_effect": "diagram.cause_effect",
    "problem_solution": "business.problem_solution",
    "objective_results": "business.objectives_results",
    "use_case": "business.use_case",
    "roadmap": "business.roadmap",
    "architecture": "business.architecture",
    "product_feature": "business.product_feature",
    "summary": "academic.summary",
    "qa": "academic.qa",
    "conclusion": "closure.conclusion",
    "thank_you": "closure.thank_you",
}

LAYOUT_ALIASES = {
    "hero": "hero-center",
    "cover": "hero-center",
    "split": "visual-split",
    "grid": "cards-grid",
    "table": "table-clean",
    "timeline": "timeline-horizontal",
    "workflow": "workflow-flow",
    "architecture": "architecture-map",
    "closing": "closing-minimal",
}

SEMANTIC_BY_SLIDE_TYPE = {
    "cover": "cover.title",
    "agenda": "section.agenda",
    "section": "section.transition",
    "introduction": "content.paragraph",
    "synthesis": "academic.summary",
    "conclusion": "closure.conclusion",
    "closing": "closure.thank_you",
    "optional": "data.cards",
}

SEMANTIC_BY_CONTENT_FORMAT = {
    "paragraph": "content.paragraph",
    "bullets": "list.bullets",
    "definition": "content.definition_list",
    "comparison": "comparison.two_column",
    "table": "data.table",
    "timeline": "diagram.timeline",
    "mixed": "content.info_box",
    "quote": "content.quote",
    "kpi": "data.kpi",
    "process": "diagram.process",
    "workflow": "diagram.workflow",
}

LAYOUT_BY_SEMANTIC = {
    "cover.title": "hero-center",
    "section.agenda": "agenda-grid",
    "section.transition": "section-band",
    "content.paragraph": "text-left-accent",
    "content.definition": "text-two-column",
    "content.definition_list": "cards-grid",
    "content.multi_paragraph": "text-two-column",
    "content.quote": "quote-focus",
    "content.info_box": "info-highlight",
    "list.bullets": "list-grid",
    "list.numbered": "list-numbered",
    "list.takeaways": "cards-grid",
    "list.pros_cons": "comparison-dual",
    "comparison.two_column": "comparison-dual",
    "comparison.before_after": "comparison-before-after",
    "comparison.concepts": "comparison-dual",
    "comparison.solutions": "comparison-dual",
    "data.table": "table-clean",
    "data.comparative_table": "table-clean",
    "data.matrix": "matrix-grid",
    "data.kpi": "stats-strip",
    "data.cards": "cards-grid",
    "visual.image_text": "visual-split",
    "visual.overlay": "visual-overlay",
    "visual.illustration": "visual-split",
    "visual.gallery": "visual-mosaic",
    "diagram.timeline": "timeline-horizontal",
    "diagram.process": "process-steps",
    "diagram.workflow": "workflow-flow",
    "diagram.orgchart": "workflow-flow",
    "diagram.cause_effect": "workflow-flow",
    "business.problem_solution": "problem-solution",
    "business.objectives_results": "objective-results",
    "business.use_case": "cards-grid",
    "business.roadmap": "roadmap-track",
    "business.architecture": "architecture-map",
    "business.product_feature": "visual-split",
    "academic.definition": "text-two-column",
    "academic.explanation": "text-left-accent",
    "academic.case_study": "cards-grid",
    "academic.summary": "cards-grid",
    "academic.qa": "qa-focus",
    "closure.conclusion": "closing-minimal",
    "closure.thank_you": "closing-minimal",
}

KEYWORD_SEMANTIC_RULES = (
    (("plan", "agenda", "outline"), "section.agenda"),
    (("transition", "section", "partie"), "section.transition"),
    (("citation", "quote", "message cle", "key message"), "content.quote"),
    (("definition", "concept", "notion"), "content.definition"),
    (("avantages", "inconvenients", "advantages", "disadvantages"), "list.pros_cons"),
    (("takeaway", "points cles", "key points"), "list.takeaways"),
    (("avant", "apres", "before", "after"), "comparison.before_after"),
    (("comparaison", "compare", "comparison"), "comparison.two_column"),
    (("tableau", "table"), "data.table"),
    (("matrice", "matrix"), "data.matrix"),
    (("kpi", "statistiques", "metrics", "indicateurs"), "data.kpi"),
    (("timeline", "chronologie"), "diagram.timeline"),
    (("process", "processus", "etapes"), "diagram.process"),
    (("workflow", "flux", "pipeline"), "diagram.workflow"),
    (("architecture", "systeme", "system", "stack"), "business.architecture"),
    (("roadmap", "feuille de route"), "business.roadmap"),
    (("probleme", "solution", "problem", "solution"), "business.problem_solution"),
    (("cas d'usage", "use case", "etude de cas", "case study"), "business.use_case"),
    (("q&a", "questions", "reponses", "faq"), "academic.qa"),
    (("conclusion", "synthese", "summary"), "closure.conclusion"),
    (("merci", "thank"), "closure.thank_you"),
)

GENERIC_AGENDA_SIGNATURES = {
    (
        "introduction",
        "definition",
        "advantages",
        "disadvantages",
        "conclusion",
    ),
    (
        "introduction",
        "definitions",
        "advantages",
        "disadvantages",
        "conclusion",
    ),
}


def build_slide_catalog_summary() -> str:
    return """
SLIDE CONTRACT
- slide_type: cover | agenda | section | introduction | content | synthesis | conclusion | closing | optional
- semantic_type: cover.title | section.agenda | section.transition | content.paragraph | content.definition | content.definition_list | content.multi_paragraph | content.quote | content.info_box | list.bullets | list.numbered | list.takeaways | list.pros_cons | comparison.two_column | comparison.before_after | comparison.concepts | comparison.solutions | data.table | data.comparative_table | data.matrix | data.kpi | data.cards | visual.image_text | visual.overlay | visual.illustration | visual.gallery | diagram.timeline | diagram.process | diagram.workflow | diagram.orgchart | diagram.cause_effect | business.problem_solution | business.objectives_results | business.use_case | business.roadmap | business.architecture | business.product_feature | academic.definition | academic.explanation | academic.case_study | academic.summary | academic.qa | closure.conclusion | closure.thank_you
- layout_variant: hero-center | hero-split | agenda-grid | section-band | text-left-accent | text-two-column | quote-focus | info-highlight | list-grid | list-numbered | comparison-dual | comparison-before-after | table-clean | matrix-grid | stats-strip | cards-grid | visual-split | visual-overlay | visual-mosaic | timeline-horizontal | timeline-vertical | process-steps | workflow-flow | architecture-map | problem-solution | objective-results | roadmap-track | qa-focus | closing-minimal
- density: compact | balanced | expanded

Choose the semantic_type that best describes the real communicative role of the slide.
Choose a layout_variant that matches the slide structure and remains consistent with a modern light presentation theme.
""".strip()


def normalize_presentation_contract(data: dict[str, Any], language: str) -> None:
    """
    Normalize la presentation complete selon le contrat de slides.

    Securite:
    - Nettoie et borne les valeurs texte pour reduire les sorties mal formees.
    - Force une structure minimale fiable (cover, agenda, conclusion).
    """
    data.setdefault("schema_version", DEFAULT_SCHEMA_VERSION)
    data.setdefault("theme", DEFAULT_THEME)
    data.setdefault("language", language)
    data.setdefault("presentation_subtitle", "")
    data.setdefault("target_audience", "General")
    data.setdefault("presentation_goal", "inform")
    data.setdefault("tone", "academic")
    data["research_used"] = bool(data.get("research_used"))
    data["sources"] = _normalize_sources(data.get("sources", []))

    for index, slide in enumerate(data["slides"], start=1):
        slide_number = slide.get("slide_number")
        slide["slide_number"] = (
            slide_number if isinstance(slide_number, int) and slide_number > 0 else index
        )

        slide_type = str(slide.get("slide_type", "content")).strip().lower()
        slide["slide_type"] = slide_type if slide_type in ALLOWED_SLIDE_TYPES else "content"

        content_format = str(slide.get("content_format", "paragraph")).strip().lower()
        slide["content_format"] = (
            content_format if content_format in ALLOWED_CONTENT_FORMATS else "paragraph"
        )

        slide["title"] = str(slide.get("title", "")).strip()
        slide["purpose"] = str(slide.get("purpose", "")).strip()
        slide["speaker_notes"] = str(slide.get("speaker_notes", "")).strip()
        slide["transition_to_next"] = str(slide.get("transition_to_next", "")).strip()

        suggested_visual = slide.get("suggested_visual")
        slide["suggested_visual"] = (
            str(suggested_visual).strip() if suggested_visual not in (None, "") else None
        )

        raw_main_content = slide.get("main_content", [])
        if not isinstance(raw_main_content, list):
            raw_main_content = [raw_main_content]

        slide["main_content"] = [
            str(item).strip() for item in raw_main_content if str(item).strip()
        ] or [slide["purpose"] or slide["title"]]

        semantic_type = normalize_semantic_type(
            slide.get("semantic_type"),
            slide_type=slide["slide_type"],
            content_format=slide["content_format"],
            title=slide["title"],
            purpose=slide["purpose"],
            main_content=slide["main_content"],
        )
        slide["semantic_type"] = semantic_type
        slide["layout_variant"] = normalize_layout_variant(slide.get("layout_variant"), semantic_type)
        slide["density"] = normalize_density(slide.get("density"), slide["main_content"])

    enforce_required_slide_order(data["slides"])
    normalize_cover_slide(data)
    normalize_agenda_slide(data["slides"], data["language"])
    normalize_conclusion_slide(data["slides"], data["language"])


def validate_presentation_contract(data: dict[str, Any]) -> None:
    """
    Verifie les contraintes structurelles majeures de la presentation.

    Securite:
    - Bloque les structures invalides avant retour API.
    """
    slides = data["slides"]

    if slides[0]["slide_type"] != "cover":
        raise ValueError("The first slide must be a cover slide.")
    if slides[1]["slide_type"] != "agenda":
        raise ValueError("The second slide must be an agenda slide.")
    if slides[-1]["slide_type"] not in {"conclusion", "closing"}:
        raise ValueError("The final slide must be a conclusion or closing slide.")

    agenda_items = slides[1]["main_content"]
    if len(agenda_items) < 3:
        raise ValueError("The agenda slide must contain at least 3 short section titles.")

    for item in agenda_items:
        plain_item = strip_agenda_prefix(item)
        if not plain_item:
            raise ValueError("Agenda items must be non-empty section titles.")
        if len(plain_item.split()) > MAX_AGENDA_WORDS:
            raise ValueError(
                "Agenda items must be short titles rather than full explanatory sentences."
            )


def normalize_semantic_type(
    raw_value: Any,
    *,
    slide_type: str,
    content_format: str,
    title: str,
    purpose: str,
    main_content: list[str],
) -> str:
    value = str(raw_value or "").strip().lower()
    value = value.replace(" ", "_")
    value = SEMANTIC_ALIASES.get(value, value)
    if value in ALLOWED_SEMANTIC_TYPES:
        return value

    hint = " ".join([title, purpose, *main_content[:3]])
    hint_ascii = _slugify(hint)
    for keywords, semantic_type in KEYWORD_SEMANTIC_RULES:
        if any(keyword in hint_ascii for keyword in keywords):
            return semantic_type

    if slide_type in SEMANTIC_BY_SLIDE_TYPE:
        return SEMANTIC_BY_SLIDE_TYPE[slide_type]
    return SEMANTIC_BY_CONTENT_FORMAT.get(content_format, "content.paragraph")


def normalize_layout_variant(raw_value: Any, semantic_type: str) -> str:
    value = str(raw_value or "").strip().lower()
    value = value.replace("_", "-").replace(" ", "-")
    value = LAYOUT_ALIASES.get(value, value)
    if value in ALLOWED_LAYOUT_VARIANTS:
        return value
    return LAYOUT_BY_SEMANTIC.get(semantic_type, "text-left-accent")


def normalize_density(raw_value: Any, main_content: list[str]) -> str:
    value = str(raw_value or "").strip().lower()
    if value in ALLOWED_DENSITIES:
        return value

    char_count = sum(len(item) for item in main_content)
    item_count = len(main_content)

    if item_count <= 3 and char_count <= 220:
        return "compact"
    if item_count >= 7 or char_count >= 580:
        return "expanded"
    return "balanced"


def normalize_cover_slide(data: dict[str, Any]) -> None:
    """
    Force les attributs obligatoires de la slide de couverture.

    Securite:
    - Evite une ouverture de presentation incoherente ou vide.
    """
    cover = data["slides"][0]

    if not data["presentation_title"]:
        data["presentation_title"] = cover["title"] or "Presentation"

    if not cover["title"]:
        cover["title"] = data["presentation_title"]

    cover["semantic_type"] = "cover.title"
    cover["layout_variant"] = "hero-center"
    cover["density"] = "compact"

    if data["presentation_subtitle"] and data["presentation_subtitle"] not in cover["main_content"]:
        cover["main_content"] = [data["presentation_subtitle"], *cover["main_content"]][:4]


def normalize_agenda_slide(slides: list[dict[str, Any]], language: str) -> None:
    """
    Nettoie et reconstruit l'agenda de facon concise et non repetitive.

    Securite:
    - Limite la taille des items et supprime les duplications.
    """
    agenda = slides[1]
    derived_items = derive_agenda_items(slides, language)
    source_items = agenda["main_content"] or derived_items

    cleaned_items: list[str] = []
    seen: set[str] = set()

    for raw_item in [*source_items, *derived_items]:
        cleaned = clean_agenda_item(raw_item)
        if not cleaned:
            continue
        key = cleaned.casefold()
        if key in seen:
            continue
        seen.add(key)
        cleaned_items.append(cleaned)
        if len(cleaned_items) >= MAX_AGENDA_ITEMS:
            break

    agenda["slide_type"] = "agenda"
    agenda["semantic_type"] = "section.agenda"
    agenda["layout_variant"] = "agenda-grid"
    agenda["title"] = agenda["title"] or AGENDA_TITLE_BY_LANGUAGE.get(language, "Agenda")
    agenda["content_format"] = "bullets"
    agenda["density"] = "compact"
    agenda_items = [
        f"{index}. {item}" for index, item in enumerate(cleaned_items[:MAX_AGENDA_ITEMS], start=1)
    ]
    if _is_generic_agenda_sequence(agenda_items):
        rebuilt_items = derive_agenda_items(slides, language, force_topic_specific=True)
        agenda_items = [
            f"{index}. {item}"
            for index, item in enumerate(rebuilt_items[:MAX_AGENDA_ITEMS], start=1)
        ]

    agenda["main_content"] = agenda_items


def normalize_conclusion_slide(slides: list[dict[str, Any]], language: str) -> None:
    """
    Garantit une conclusion complete (resume + synthese + ouverture).

    Securite:
    - Evite les conclusions vides ou trop courtes degradeant la qualite finale.
    """
    conclusion = slides[-1]
    if conclusion["slide_type"] == "closing":
        conclusion["semantic_type"] = "closure.thank_you"
        conclusion["title"] = conclusion["title"] or THANK_YOU_TITLE_BY_LANGUAGE.get(language, "Thank you")
    else:
        conclusion["slide_type"] = "conclusion"
        conclusion["semantic_type"] = "closure.conclusion"
        conclusion["title"] = conclusion["title"] or CONCLUSION_TITLE_BY_LANGUAGE.get(language, "Conclusion")

    conclusion["layout_variant"] = "closing-minimal"
    conclusion["density"] = "compact"

    # Evite le doublon visuel "Conclusion" repete dans le corps de la meme slide.
    conclusion_title_slug = _slugify(conclusion.get("title", ""))
    filtered_main_content: list[str] = []
    for item in conclusion.get("main_content", []):
        cleaned_item = str(item).strip()
        if not cleaned_item:
            continue
        if _slugify(cleaned_item) == conclusion_title_slug:
            continue
        filtered_main_content.append(cleaned_item)
    conclusion["main_content"] = filtered_main_content

    if conclusion["slide_type"] == "conclusion":
        sentence_count = _count_sentences(" ".join(conclusion.get("main_content", [])))
        if sentence_count < MIN_CONCLUSION_SENTENCES:
            conclusion["main_content"] = _build_conclusion_fallback(slides, language)

    if not conclusion.get("speaker_notes", "").strip():
        conclusion["speaker_notes"] = (
            "Recap briefly the key ideas, confirm the practical takeaway, and open to next steps."
        )


def derive_agenda_items(
    slides: list[dict[str, Any]],
    language: str,
    *,
    force_topic_specific: bool = False,
) -> list[str]:
    """
    Derive un agenda depuis les slides de corps en privilegiant la specificite sujet.

    Securite:
    - Evite un plan statique quand le contenu offre de meilleurs intitulés.
    """
    body_titles: list[str] = []
    for slide in slides[2:-1]:
        cleaned = clean_agenda_item(slide.get("title", ""))
        if cleaned:
            body_titles.append(cleaned)

    if not body_titles:
        body_titles = [
            clean_agenda_item(item)
            for item in ("Introduction", "Definitions", "Methodology", "Results")
            if clean_agenda_item(item)
        ]
    elif force_topic_specific:
        body_titles = [item for item in body_titles if _slugify(item) not in {"introduction"}] or body_titles

    items = body_titles[:MAX_AGENDA_ITEMS]
    return items


def clean_agenda_item(value: str) -> str:
    """
    Nettoie un item d'agenda et limite sa longueur.

    Securite:
    - Retire les prefixes et separateurs pour eviter des intitulés bruyants.
    """
    item = strip_agenda_prefix(str(value).strip())
    if not item:
        return ""

    parts = [part.strip() for part in AGENDA_ITEM_SPLIT_PATTERN.split(item) if part.strip()]
    if parts:
        item = parts[0]

    words = item.split()
    if len(words) > MAX_AGENDA_WORDS:
        item = " ".join(words[:MAX_AGENDA_WORDS])

    return item.strip(" .;,:")


def strip_agenda_prefix(value: str) -> str:
    """
    Supprime numerotation/puce initiale d'un item d'agenda.

    Securite:
    - Standardise les entrées pour validation fiable.
    """
    return AGENDA_NUMBERING_PATTERN.sub("", value).strip()


def enforce_required_slide_order(slides: list[dict[str, Any]]) -> None:
    """
    Impose l'ordre minimal cover -> agenda -> ... -> conclusion/closing.

    Securite:
    - Previent une structure invalide avant normalisation finale.
    """
    slides[0]["slide_type"] = "cover"
    slides[1]["slide_type"] = "agenda"
    if slides[-1]["slide_type"] not in {"conclusion", "closing"}:
        slides[-1]["slide_type"] = "conclusion"


def _normalize_sources(raw_sources: Any) -> list[str]:
    """
    Nettoie et deduplique les sources.

    Securite:
    - Evite les doublons et valeurs vides dans la sortie.
    """
    if not isinstance(raw_sources, list):
        return []

    sources: list[str] = []
    seen: set[str] = set()

    for source in raw_sources:
        url = str(source).strip()
        if not url or url in seen:
            continue
        seen.add(url)
        sources.append(url)

    return sources


def _slugify(value: str) -> str:
    """
    Convertit une chaine en version ASCII lowercase pour matching robuste.

    Securite:
    - Reduit les ambiguities de comparaison en supprimant les diacritiques.
    """
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    return ascii_value.casefold()


def _is_generic_agenda_sequence(items: list[str]) -> bool:
    """
    Detecte un plan d'agenda generique a eviter.

    Securite:
    - Empêche les structures statiques repetitives en sortie.
    """
    normalized_items = [clean_agenda_item(item) for item in items if clean_agenda_item(item)]
    signature = tuple(_slugify(item) for item in normalized_items)
    return signature in GENERIC_AGENDA_SIGNATURES


def _count_sentences(text: str) -> int:
    """
    Compte approximativement le nombre de phrases d'un texte.

    Securite:
    - Sert de garde-fou pour imposer une conclusion minimale.
    """
    fragments = [chunk.strip() for chunk in re.split(r"[.!?]+", text) if chunk.strip()]
    return len(fragments)


def _build_conclusion_fallback(slides: list[dict[str, Any]], language: str) -> list[str]:
    """
    Construit une conclusion de secours structurée (2 a 4 phrases).

    Securite:
    - Evite une conclusion vide/mecanique en cas de generation incomplete.
    """
    body_titles = [slide.get("title", "").strip() for slide in slides[2:-1] if slide.get("title", "").strip()]
    top_titles = body_titles[:3]

    if language.casefold().startswith("french"):
        first_sentence = (
            "Cette presentation a explore les axes majeurs du sujet avec une progression claire et "
            "orientee vers la comprehension."
        )
        if top_titles:
            second_sentence = f"Les points cles abordes incluent notamment {', '.join(top_titles)}."
        else:
            second_sentence = "Les idees principales ont ete reliees de facon coherente pour soutenir l'objectif."
        third_sentence = (
            "En perspective, la suite repose sur une mise en pratique rigoureuse et un ajustement continu "
            "selon le contexte."
        )
    else:
        first_sentence = (
            "This presentation explored the topic through a clear and structured progression."
        )
        if top_titles:
            second_sentence = f"Key points included {', '.join(top_titles)}."
        else:
            second_sentence = (
                "The core ideas were connected to support a coherent understanding of the subject."
            )
        third_sentence = (
            "As a forward-looking perspective, practical implementation and continuous adaptation remain essential."
        )

    return [first_sentence, second_sentence, third_sentence][:MAX_CONCLUSION_SENTENCES]
