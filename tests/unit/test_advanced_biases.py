"""Tests for hindsight, fundamental attribution, and halo biases."""

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


class TestHindsight:
    @pytest.mark.parametrize(
        "phrase",
        [
            "I knew this would happen.",
            "Obviously it was going to fail.",
            "In retrospect, the signs were everywhere.",
            "Of course they backed out.",
            "I should have known he was lying.",
        ],
    )
    def test_triggers(self, phrase):
        d = _decision(reasoning=phrase)
        assert biases.detect_hindsight(d) is not None

    def test_does_not_trigger_when_uncertainty_acknowledged(self):
        d = _decision(reasoning="It was a coin flip. The downside might have been worse.")
        assert biases.detect_hindsight(d) is None


class TestFundamentalAttribution:
    @pytest.mark.parametrize(
        "phrase",
        [
            "He is just lazy.",
            "Typical of her to bail at the last minute.",
            "That's who they are — selfish people.",
            "She always does this.",
        ],
    )
    def test_triggers(self, phrase):
        d = _decision(reasoning=phrase)
        assert biases.detect_fundamental_attribution(d) is not None

    def test_does_not_trigger_on_situational_framing(self):
        d = _decision(
            reasoning="He was probably overwhelmed at work that week. The downside is real."
        )
        assert biases.detect_fundamental_attribution(d) is None


class TestHalo:
    @pytest.mark.parametrize(
        "phrase",
        [
            "She seems great. I trust her.",
            "He came highly recommended.",
            "I like him.",
            "Good vibes.",
            "He looks the part.",
        ],
    )
    def test_triggers(self, phrase):
        d = _decision(reasoning=phrase)
        assert biases.detect_halo(d) is not None

    def test_does_not_trigger_on_specific_evidence(self):
        d = _decision(
            reasoning=(
                "She has 5 years experience with this exact problem and "
                "two references confirmed the prior outcomes. The downside is real."
            )
        )
        assert biases.detect_halo(d) is None


class TestAllThirteen:
    def test_full_run_returns_many_biases(self):
        d = _decision(
            reasoning=(
                "I've already spent so much time. I knew this would happen. "
                "He is just lazy. She seems great so I trust her. Everyone "
                "does this. It is guaranteed to work."
            ),
            confidence=95,
        )
        flags = biases.run_all(d)
        slugs = {slug for slug, _ in flags}
        # at least these should appear:
        assert "sunk_cost" in slugs
        assert "hindsight_bias" in slugs
        assert "fundamental_attribution_error" in slugs
        assert "halo_effect" in slugs
        assert "bandwagon" in slugs
        assert "framing" in slugs
        assert "optimism_bias" in slugs
