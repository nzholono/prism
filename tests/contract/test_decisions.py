"""Contract tests for the cognitive-lens (decision journal) endpoints."""

from __future__ import annotations


def _create(http, **overrides):
    body = dict(
        situation="My landlord won't return my $1200 deposit.",
        options=["Send demand letter", "Drop it"],
        chosen="Send demand letter",
        reasoning="I've already spent so much time chasing him. The law is on my side.",
        expected_outcome="He pays within 14 days.",
        confidence=90,
    )
    body.update(overrides)
    return http.post("/decisions", json=body)


def test_create_decision_returns_201_with_id(http):
    r = _create(http)
    assert r.status_code == 201
    body = r.json()
    assert "id" in body
    assert body["situation"].startswith("My landlord")


def test_create_decision_flags_biases(http):
    """The seeded reasoning should trigger sunk_cost and confirmation."""
    r = _create(http)
    body = r.json()
    slugs = {b["bias_slug"] for b in body["biases"]}
    assert "sunk_cost" in slugs
    assert "confirmation_bias" in slugs


def test_list_decisions_includes_created(http):
    _create(http)
    _create(http, situation="Different one")
    r = http.get("/decisions")
    assert r.status_code == 200
    assert len(r.json()) >= 2


def test_get_decision_includes_biases(http):
    created = _create(http).json()
    r = http.get(f"/decisions/{created['id']}")
    assert r.status_code == 200
    assert r.json()["biases"]


def test_update_decision_records_actual_outcome(http):
    created = _create(http).json()
    r = http.patch(
        f"/decisions/{created['id']}",
        json={"actual_outcome": "He paid after 8 days."},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["actual_outcome"] == "He paid after 8 days."
    assert body["reviewed_at"] is not None


def test_delete_decision_returns_204(http):
    created = _create(http).json()
    r = http.delete(f"/decisions/{created['id']}")
    assert r.status_code == 204
    r2 = http.get(f"/decisions/{created['id']}")
    assert r2.status_code == 404


def test_get_unknown_decision_returns_404(http):
    r = http.get("/decisions/99999")
    assert r.status_code == 404
