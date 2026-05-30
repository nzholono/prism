"""Contract tests for the ethical-lens endpoints."""

from __future__ import annotations


def test_list_frameworks_returns_four(http):
    r = http.get("/ethics/frameworks")
    assert r.status_code == 200
    body = r.json()
    slugs = {fw["slug"] for fw in body}
    assert slugs == {"utilitarian", "deontological", "virtue", "care"}


def test_analyze_returns_perspective_per_framework(http):
    r = http.post("/ethics/analyze", json={"situation": "Should I sue my landlord?"})
    assert r.status_code == 200
    body = r.json()
    assert body["situation"] == "Should I sue my landlord?"
    assert len(body["perspectives"]) == 4
    for p in body["perspectives"]:
        assert p["framework_slug"]
        assert p["framework_name"]
        assert p["framing"]
        assert p["questions"]
        assert isinstance(p["questions"], list)
