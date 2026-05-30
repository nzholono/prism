"""Test configuration.

Auto-marks tests by which folder they live in, so you can run a slice:

    uv run pytest -m unit
    uv run pytest -m contract
    uv run pytest -m integration
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


@pytest.fixture
def in_process_client():
    """An ApiClient that talks to a fresh in-process Pharos app (no network)."""
    from prism.api_client import make_in_process_client
    from prism.server import create_app

    app = create_app()
    return make_in_process_client(app)
