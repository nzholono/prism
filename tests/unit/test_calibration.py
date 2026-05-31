"""Unit tests for the calibration analyzer."""

from __future__ import annotations

from datetime import datetime

from prism.lenses.cognitive.calibration import _outcome_is_bad, calibrate
from prism.models import BiasFlag, Decision


def _decision(
    id: int = 1,
    confidence: int = 60,
    actual_outcome: str | None = None,
    biases: list[str] | None = None,
) -> Decision:
    return Decision(
        id=id,
        created_at=datetime.utcnow(),
        situation=f"situation {id}",
        options=["A", "B"],
        chosen="A",
        reasoning="reasoning",
        expected_outcome="expected",
        confidence=confidence,
        actual_outcome=actual_outcome,
        biases=[BiasFlag(id=i, bias_slug=slug, evidence="ev") for i, slug in enumerate(biases or [])],
    )


def test_empty_report():
    r = calibrate([])
    assert r.total == 0
    assert "No decisions" in r.summary()


def test_unreviewed_only_report():
    r = calibrate([_decision(id=1), _decision(id=2)])
    assert r.total == 2
    assert r.reviewed == 0
    assert "none reviewed" in r.summary()


def test_outcome_is_bad():
    assert _outcome_is_bad("It didn't work")
    assert _outcome_is_bad("I regret it")
    assert _outcome_is_bad("Landlord won't pay")
    assert not _outcome_is_bad("Worked out great")
    assert not _outcome_is_bad("Settled in my favor")


def test_overconfidence_pattern_detected():
    decisions = [
        # high confidence, bad outcomes
        _decision(id=1, confidence=90, actual_outcome="didn't work"),
        _decision(id=2, confidence=90, actual_outcome="regret it"),
        _decision(id=3, confidence=85, actual_outcome="failed"),
        # lower confidence, good outcomes
        _decision(id=4, confidence=55, actual_outcome="went well"),
        _decision(id=5, confidence=55, actual_outcome="great result"),
    ]
    r = calibrate(decisions)
    assert r.reviewed == 5
    assert any("overconfidence" in note.lower() for note in r.pattern_notes)


def test_bias_flags_counted():
    decisions = [
        _decision(id=1, biases=["sunk_cost"], actual_outcome="ok"),
        _decision(id=2, biases=["sunk_cost", "optimism_bias"], actual_outcome="ok"),
    ]
    r = calibrate(decisions)
    slugs = dict(r.most_common_biases)
    assert slugs["sunk_cost"] == 2
    assert slugs["optimism_bias"] == 1


def test_summary_contains_all_sections_when_data_is_rich():
    decisions = [
        _decision(id=i, confidence=80 + i, actual_outcome="went well", biases=["sunk_cost"])
        for i in range(5)
    ]
    summary = calibrate(decisions).summary()
    assert "Decisions logged: 5" in summary
    assert "reviewed" in summary.lower()
    assert "Average confidence" in summary
