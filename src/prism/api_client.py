"""ApiClient — the one HTTP wrapper every client uses.

The four UI clients (CLI, TUI, Web, GUI) and the MCP server all go through this
class. Adding a new endpoint = adding one method here, and every client gets it.

For tests, `make_in_process_client()` builds an ApiClient that talks to a
FastAPI `TestClient` instead of a real socket — same surface, no network.
"""

from __future__ import annotations

from typing import Any

import httpx

from prism.models import HealthResponse


DEFAULT_BASE_URL = "http://127.0.0.1:8000"


class PharosUnavailable(RuntimeError):
    """Raised when the server can't be reached. Clients should show a friendly hint."""


class ApiClient:
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        transport: httpx.BaseTransport | None = None,
        timeout: float = 5.0,
    ) -> None:
        self._client = httpx.Client(
            base_url=base_url,
            transport=transport,
            timeout=timeout,
        )

    # ── meta ────────────────────────────────────────────────────────────────
    def health(self) -> HealthResponse:
        return HealthResponse.model_validate(self._get("/health"))

    # ── internal ────────────────────────────────────────────────────────────
    def _get(self, path: str, **params: Any) -> Any:
        try:
            r = self._client.get(path, params=params or None)
        except httpx.HTTPError as exc:
            raise PharosUnavailable(
                f"Cannot reach Pharos at {self._client.base_url}. "
                "Did you start it with `uv run pharos`?"
            ) from exc
        r.raise_for_status()
        return r.json()

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "ApiClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def make_in_process_client(app: Any) -> ApiClient:
    """Build an ApiClient that talks to a FastAPI app in-process (for tests)."""
    transport = httpx.WSGITransport(app=app) if hasattr(app, "wsgi_app") else None
    # FastAPI is ASGI — use ASGITransport
    if transport is None:
        transport = httpx.ASGITransport(app=app)
    return ApiClient(base_url="http://testserver", transport=transport)
