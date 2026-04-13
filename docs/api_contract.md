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
