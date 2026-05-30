"""Contract test: /health returns the documented shape."""

from __future__ import annotations


def test_health_returns_ok_with_version(http):
    r = http.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert isinstance(body["version"], str)
    assert body["version"].count(".") == 2  # x.y.z


def test_stats_returns_counts(http):
    r = http.get("/stats")
    assert r.status_code == 200
    body = r.json()
    for key in ("domains", "statutes", "scenarios", "decisions", "bias_flags"):
        assert key in body
        assert isinstance(body[key], int)
