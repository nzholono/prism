"""Tests for recency and self-serving biases."""

from __future__ import annotations

import pytest

from prism.lenses.cognitive import biases
from prism.models import DecisionCreate


def _decision(**overrides) -> DecisionCreate:
    base = dict(
        situation="Neutral.",
        options=["A", "B"],
        chosen="A",
        reasoning="I weighed both sides. The downside is real.",
        expected_outcome="Mixed.",
        confidence=55,
    )
    base.update(overrides)
    return DecisionCreate(**base)


class TestRecency:
    def test_triggers_when_recent_events_drive_reasoning(self):
        d = _decision(
            reasoning="Yesterday they were rude. Just this morning they snapped at me again. Today I'm done."
        )
        assert biases.detect_recency(d) is not None

    def test_does_not_trigger_when_pattern_acknowledged(self):
        d = _decision(
            reasoning=(
                "Yesterday they were rude, just like usually they are. "
                "The pattern has held for months."
            )
        )
        assert biases.detect_recency(d) is None


class TestSelfServing:
    @pytest.mark.parametrize(
        "phrase",
        [
            "It's not my fault — they tricked me.",
            "I'm unlucky.",
            "I had no choice.",
            "The market was against me.",
        ],
    )
    def test_triggers_on_externalized_failure(self, phrase):
        d = _decision(reasoning=phrase)
        assert biases.detect_self_serving(d) is not None

    def test_triggers_on_unearned_success_attribution(self):
        d = _decision(
            reasoning="My hard work made this happen. I deserve this. I earned it."
        )
        assert biases.detect_self_serving(d) is not None

    def test_does_not_trigger_on_balanced_attribution(self):
        d = _decision(
            reasoning="My effort helped, but I also got lucky with the timing. The downside is real."
        )
        assert biases.detect_self_serving(d) is None


class TestAllFifteen:
    def test_full_run_returns_fifteen_or_more_biases(self):
        d = _decision(
            reasoning=(
                "I've already spent so much time. I knew this would fail. "
                "He is just lazy. She seems great — I trust her. Everyone "
                "does this. It is guaranteed to work. Yesterday they "
                "promised. Just today they confirmed. I deserve this. "
                "My hard work earned it."
            ),
            confidence=95,
        )
        flags = biases.run_all(d)
        slugs = {slug for slug, _ in flags}
        assert "sunk_cost" in slugs
        assert "hindsight_bias" in slugs
        assert "fundamental_attribution_error" in slugs
        assert "halo_effect" in slugs
        assert "bandwagon" in slugs
        assert "framing" in slugs
        assert "optimism_bias" in slugs
        assert "recency_bias" in slugs
        assert "self_serving_bias" in slugs
