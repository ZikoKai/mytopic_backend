# API Contract v1

## POST `/api/v1/presentations/generate`

Request JSON:

```json
{
  "topic": "string",
  "language": "string | null"
}
```

Response JSON:

- `presentation_title`
- `slides[]` avec `slide_type`, `semantic_type`, `layout_variant`, `density`, `main_content`, etc.

## Presentation Persistence Payload

Les endpoints `POST /api/v1/presentations` et `PUT /api/v1/presentations/{id}`
acceptent un `content` JSON qui contient des slides enrichies avec une scene
editable persistee.

Extrait de structure recommandee:

```json
{
  "schema_version": "2026-04",
  "theme": "editorial-light",
  "slides": [
    {
      "slide_number": 1,
      "title": "Titre",
      "purpose": "Objectif",
      "main_content": ["Point A", "Point B"],
      "editor_scene": {
        "version": "1.0",
        "width": 1600,
        "height": 900,
        "background": "#f8fafc",
        "elements": [
          {
            "id": "text-1",
            "type": "text",
            "x": 120,
            "y": 90,
            "width": 1000,
            "height": 100,
            "rotation": 0,
            "zIndex": 1,
            "locked": false,
            "visible": true,
            "opacity": 1,
            "text": "Titre de slide",
            "color": "#0f172a",
            "fontSize": 56,
            "fontFamily": "Geist Variable, sans-serif",
            "fontWeight": 800,
            "fontStyle": "normal",
            "align": "left",
            "lineHeight": 1.2
          },
          {
            "id": "shape-1",
            "type": "shape",
            "x": 80,
            "y": 70,
            "width": 1440,
            "height": 760,
            "rotation": 0,
            "zIndex": 0,
            "locked": false,
            "visible": true,
            "opacity": 1,
            "shape": "rect",
            "fill": "#ffffff",
            "stroke": "#e2e8f0",
            "strokeWidth": 1,
            "cornerRadius": 24
          }
        ]
      }
    }
  ]
}
```
