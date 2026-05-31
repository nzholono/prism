"""Tests for the four additional bias detectors added in the polish pass."""

from __future__ import annotations

import pytest

from prism.lenses.cognitive import biases
from prism.models import DecisionCreate


def _decision(**overrides) -> DecisionCreate:
    base = dict(
        situation="Neutral.",
        options=["A", "B"],
        chosen="A",
        reasoning="I am choosing A. The downside is real but manageable.",
        expected_outcome="It will work out.",
        confidence=50,
    )
    base.update(overrides)
    return DecisionCreate(**base)


class TestStatusQuo:
    @pytest.mark.parametrize(
        "phrase",
        [
            "I've always done it this way.",
            "Why change now?",
            "Don't fix what isn't broken.",
        ],
    )
    def test_triggers_on_phrases(self, phrase):
        d = _decision(reasoning=phrase)
        assert biases.detect_status_quo(d) is not None

    def test_triggers_on_default_no_change_with_short_reasoning(self):
        d = _decision(chosen="do nothing", reasoning="Why bother.")
        assert biases.detect_status_quo(d) is not None

    def test_does_not_trigger_on_thoughtful_no_change(self):
        d = _decision(
            chosen="do nothing",
            reasoning=(
                "I considered acting but the costs are real and the benefits "
                "marginal. The downside of inaction is small."
            ),
        )
        assert biases.detect_status_quo(d) is None


class TestBandwagon:
    @pytest.mark.parametrize(
        "phrase",
        [
            "Everyone else does it.",
            "My friends all chose this.",
            "Nobody does that anymore.",
        ],
    )
    def test_triggers(self, phrase):
        d = _decision(reasoning=phrase)
        assert biases.detect_bandwagon(d) is not None

    def test_does_not_trigger_without_social_proof(self):
        d = _decision(reasoning="This fits my situation. The downside is real.")
        assert biases.detect_bandwagon(d) is None


class TestFraming:
    def test_triggers_on_certainty_framing(self):
        d = _decision(reasoning="This is guaranteed to work.")
        assert biases.detect_framing(d) is not None

    def test_triggers_on_percentage_framing(self):
        d = _decision(reasoning="There is a 90% success rate, however I worry.")
        assert biases.detect_framing(d) is not None

    def test_does_not_trigger_on_balanced_phrasing(self):
        d = _decision(reasoning="Some chance of working, some of not. Trade-offs.")
        assert biases.detect_framing(d) is None


class TestPlanningFallacy:
    def test_triggers_on_repeated_quick_easy(self):
        d = _decision(
            reasoning="This will be quick and easy. Just a simple fix."
        )
        assert biases.detect_planning_fallacy(d) is not None

    def test_does_not_trigger_with_buffer_words(self):
        d = _decision(
            reasoning=(
                "This should be quick but it might take longer if the form "
                "gets rejected — I have buffer time."
            )
        )
        assert biases.detect_planning_fallacy(d) is None


class TestAllTen:
    def test_full_run_returns_multiple(self):
        d = _decision(
            reasoning=(
                "I've already spent so much time. Everyone does this. It is "
                "guaranteed to work. The law is on my side."
            ),
            confidence=95,
        )
        flags = biases.run_all(d)
        slugs = {slug for slug, _ in flags}
        assert "sunk_cost" in slugs
        assert "bandwagon" in slugs
        assert "framing" in slugs
        assert "optimism_bias" in slugs
        # all detectors should produce non-empty evidence
        for slug, evidence in flags:
            assert evidence
            assert len(evidence) > 10
