"""Unit tests for the cognitive bias detectors.

These are the first real tests in the project — they prove that the
detector logic works on representative positive and negative cases.
"""

from __future__ import annotations

import pytest

from prism.lenses.cognitive import biases
from prism.models import DecisionCreate


def _decision(**overrides) -> DecisionCreate:
    """Helper: build a baseline decision and override specific fields."""
    base = dict(
        situation="A neutral situation.",
        options=["A", "B"],
        chosen="A",
        reasoning="I am choosing A because it seems reasonable.",
        expected_outcome="It will work out fine.",
        confidence=50,
    )
    base.update(overrides)
    return DecisionCreate(**base)


# ──────────────────────────────────────────────────────────────────────────────
# sunk_cost
# ──────────────────────────────────────────────────────────────────────────────

class TestSunkCost:
    @pytest.mark.parametrize(
        "phrase",
        [
            "I've already spent 20 hours on this.",
            "I can't waste the money I put in.",
            "Too much time invested to back out.",
            "I've come this far, I should finish.",
        ],
    )
    def test_triggers(self, phrase):
        d = _decision(reasoning=phrase)
        assert biases.detect_sunk_cost(d) is not None

    @pytest.mark.parametrize(
        "phrase",
        [
            "I am weighing the options carefully.",
            "The benefits look slightly better than the costs.",
            "This is a fresh decision.",
        ],
    )
    def test_does_not_trigger(self, phrase):
        d = _decision(reasoning=phrase)
        assert biases.detect_sunk_cost(d) is None


# ──────────────────────────────────────────────────────────────────────────────
# anchoring
# ──────────────────────────────────────────────────────────────────────────────

class TestAnchoring:
    def test_triggers_on_repeated_dollar_amount(self):
        d = _decision(
            reasoning="The landlord owes me $1200. I want my $1200 back. The $1200 is the principle."
        )
        assert biases.detect_anchoring(d) is not None

    def test_does_not_trigger_on_varied_numbers(self):
        d = _decision(
            reasoning="I could lose $1200 in deposit but spend $400 on filing. Net $800."
        )
        assert biases.detect_anchoring(d) is None


# ──────────────────────────────────────────────────────────────────────────────
# confirmation
# ──────────────────────────────────────────────────────────────────────────────

class TestConfirmation:
    def test_triggers_on_one_sided_reasoning(self):
        d = _decision(
            reasoning=(
                "Going to court is great. I will win. The law is on my side. "
                "It will set a good precedent and feel satisfying."
            )
        )
        assert biases.detect_confirmation(d) is not None

    def test_does_not_trigger_when_counter_mentioned(self):
        d = _decision(
            reasoning=(
                "Going to court could work but it will take months. "
                "The downside is significant time investment."
            )
        )
        assert biases.detect_confirmation(d) is None


# ──────────────────────────────────────────────────────────────────────────────
# optimism
# ──────────────────────────────────────────────────────────────────────────────

class TestOptimism:
    def test_triggers_on_high_confidence_no_fallback(self):
        d = _decision(
            confidence=95,
            reasoning="This will definitely work. I'm sure of it.",
        )
        assert biases.detect_optimism(d) is not None

    def test_does_not_trigger_with_contingency(self):
        d = _decision(
            confidence=95,
            reasoning="I'm very confident, but if it doesn't work I have a backup plan.",
        )
        assert biases.detect_optimism(d) is None

    def test_does_not_trigger_on_modest_confidence(self):
        d = _decision(confidence=70, reasoning="Pretty sure but not certain.")
        assert biases.detect_optimism(d) is None


# ──────────────────────────────────────────────────────────────────────────────
# run_all
# ──────────────────────────────────────────────────────────────────────────────

class TestRunAll:
    def test_returns_empty_list_for_clean_decision(self):
        d = _decision(
            reasoning="I'm weighing both sides carefully. The downside is real but manageable.",
            confidence=60,
        )
        flags = biases.run_all(d)
        assert flags == []

    def test_returns_multiple_flags(self):
        d = _decision(
            reasoning=(
                "I've already spent so much time on this. It will definitely work. "
                "The law is on my side."
            ),
            confidence=95,
        )
        flags = biases.run_all(d)
        slugs = {slug for slug, _ in flags}
        assert "sunk_cost" in slugs
        assert "optimism_bias" in slugs

    def test_each_flag_has_evidence(self):
        d = _decision(reasoning="I've already spent so much time on this.")
        flags = biases.run_all(d)
        for slug, evidence in flags:
            assert slug
            assert evidence
            assert len(evidence) > 10
