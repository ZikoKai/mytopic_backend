import json
from typing import Any
from urllib import error as urllib_error
from urllib import request as urllib_request

from apps.ai.core.ai_client import AIClientError


def join_url(base_url: str, path: str) -> str:
    return f"{base_url.rstrip('/')}/{path.lstrip('/')}"


def read_json(url: str, timeout_seconds: float) -> dict[str, Any]:
    req = urllib_request.Request(url=url, method="GET")
    try:
        with urllib_request.urlopen(req, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8")
    except urllib_error.HTTPError as exc:
        raise AIClientError(f"Provider endpoint returned HTTP {exc.code}.") from exc
    except TimeoutError as exc:
        raise AIClientError("Provider request timed out.") from exc
    except Exception as exc:
        raise AIClientError(f"Provider endpoint is unreachable: {exc}") from exc

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise AIClientError("Provider returned invalid JSON.") from exc
    if not isinstance(parsed, dict):
        raise AIClientError("Provider returned an unexpected payload.")
    return parsed


def post_json(
    url: str,
    payload: dict[str, Any],
    timeout_seconds: float,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib_request.Request(
        url=url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json", **(headers or {})},
    )

    try:
        with urllib_request.urlopen(req, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8")
    except urllib_error.HTTPError as exc:
        detail = ""
        try:
            parsed = json.loads(exc.read().decode("utf-8"))
            if isinstance(parsed, dict):
                error = parsed.get("error")
                if isinstance(error, dict):
                    detail = str(error.get("message") or "").strip()
                elif isinstance(error, str):
                    detail = error.strip()
        except Exception:
            detail = ""

        raise AIClientError(detail or f"Provider endpoint returned HTTP {exc.code}.") from exc
    except TimeoutError as exc:
        raise AIClientError("Provider request timed out.") from exc
    except Exception as exc:
        raise AIClientError(f"Provider endpoint is unreachable: {exc}") from exc

    try:
        parsed_body = json.loads(body)
    except json.JSONDecodeError as exc:
        raise AIClientError("Provider returned invalid JSON.") from exc
    if not isinstance(parsed_body, dict):
        raise AIClientError("Provider returned an unexpected payload.")
    return parsed_body
