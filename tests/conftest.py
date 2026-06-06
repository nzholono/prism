"""Test configuration.

Auto-marks tests by which folder they live in, so you can run a slice:

    uv run pytest -m unit
    uv run pytest -m contract
    uv run pytest -m integration

Provides three fixtures:

- `app`   — a fresh FastAPI app with an in-memory SQLite DB (no lifespan yet).
- `http`  — a TestClient bound to that app, with lifespan entered (DB seeded).
- `in_process_client` — an ApiClient that delegates to `http`, so integration
  tests share the same seeded DB.
"""

from __future__ import annotations

import pytest


def pytest_collection_modifyitems(config, items):
    for item in items:
        path = str(item.fspath)
        if "/tests/unit/" in path:
            item.add_marker(pytest.mark.unit)
        elif "/tests/contract/" in path:
            item.add_marker(pytest.mark.contract)
        elif "/tests/integration/" in path:
            item.add_marker(pytest.mark.integration)


@pytest.fixture(autouse=True)
def _redirect_bias_audit_log(tmp_path, monkeypatch):
    """Send the bias audit log to a temp file during every test so the
    user's real ~/.prism/bias_audit.jsonl isn't polluted."""
    from prism.lenses.cognitive import audit

    log_file = tmp_path / "bias_audit.jsonl"
    monkeypatch.setattr(audit, "BIAS_AUDIT_LOG_PATH", log_file)
    yield log_file


@pytest.fixture
def app():
    """Bare FastAPI app with an in-memory DB. Use `http` if you need lifespan."""
    from prism.server import create_app

    return create_app(db_path=":memory:")


@pytest.fixture
def http(app):
    """A FastAPI TestClient with lifespan entered (DB created and seeded)."""
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        yield client


@pytest.fixture
def in_process_client(http):
    """An ApiClient that delegates to the seeded TestClient. No real network."""
    from prism.api_client import make_in_process_client

    return make_in_process_client(http)
