"""Pharos — the REST server.

Owns the SQLite database. Every other process is a client that talks to Pharos
over HTTP. Run with `uv run pharos`.

This is a *minimal* skeleton — `/health` works so we can prove the architecture
end-to-end. Real endpoints land in the next phase.
"""

from __future__ import annotations

from fastapi import FastAPI

from prism import __version__
from prism.models import HealthResponse


def create_app() -> FastAPI:
    """Build the FastAPI app. Kept as a factory so tests can pass overrides."""
    app = FastAPI(
        title="Pharos",
        description="REST server for Prism — Illinois legal & ethical reasoning framework.",
        version=__version__,
    )

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(status="ok", version=__version__)

    return app


app = create_app()


def main() -> None:
    """Entry point for `uv run pharos`."""
    import uvicorn

    uvicorn.run("prism.server:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()
