"""Contract test: /health returns the documented shape."""

from __future__ import annotations

from fastapi.testclient import TestClient

from prism.server import create_app


def test_health_returns_ok_with_version():
    client = TestClient(create_app())
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert isinstance(body["version"], str)
    assert body["version"].count(".") == 2  # x.y.z
