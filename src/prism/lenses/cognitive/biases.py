"""Bias detectors — keyword/heuristic rules over decision-journal entries.

Each detector takes a `DecisionCreate` and returns either None (no flag)
or a tuple `(bias_slug, evidence)`.

These are deliberately simple. They will catch obvious cases and miss subtle
ones — they're a *prompt* for the user to reflect, not an oracle.
"""

from __future__ import annotations

import re
from typing import Callable

from prism.models import DecisionCreate


BiasResult = tuple[str, str] | None
Detector = Callable[[DecisionCreate], BiasResult]


def _haystack(d: DecisionCreate) -> str:
    """Combined lowercased text we scan across."""
    parts = [d.situation, d.reasoning, d.expected_outcome, *d.options, d.chosen]
    return " ".join(parts).lower()


# ──────────────────────────────────────────────────────────────────────────────
# Detectors
# ──────────────────────────────────────────────────────────────────────────────

SUNK_COST_PATTERNS = [
    r"already (spent|invested|put in|paid)",
    r"can'?t waste",
    r"too much (time|money|effort) (in|invested)",
    r"come this far",
    r"give up now",
    r"after all (i'?ve|i have) put",
]


def detect_sunk_cost(d: DecisionCreate) -> BiasResult:
    text = _haystack(d)
    for pattern in SUNK_COST_PATTERNS:
        m = re.search(pattern, text)
        if m:
            return (
                "sunk_cost",
                f"Phrase '{m.group(0)}' suggests reasoning from past spending — "
                "past costs should not drive future decisions.",
            )
    return None


def detect_anchoring(d: DecisionCreate) -> BiasResult:
    """Single dollar/number reference dominating reasoning."""
    text = d.reasoning.lower()
    # one prominent dollar figure mentioned repeatedly
    dollars = re.findall(r"\$\d[\d,]*(?:\.\d+)?", text)
    if dollars and len(set(dollars)) == 1 and len(dollars) >= 2:
        return (
            "anchoring",
            f"Reasoning anchors on a single number ({dollars[0]}) without "
            "comparing alternatives.",
        )
    return None


CONFIRMATION_NEGATIVES = ["but", "however", "on the other hand", "downside", "risk"]


def detect_confirmation(d: DecisionCreate) -> BiasResult:
    """Reasoning that lists only supporting evidence with no counter-consideration."""
    text = d.reasoning.lower()
    if len(text) < 40:
        return None
    if not any(neg in text for neg in CONFIRMATION_NEGATIVES):
        return (
            "confirmation_bias",
            "Reasoning mentions no counter-considerations (no 'but', 'however', "
            "'downside', etc.). Consider what would change your mind.",
        )
    return None


def detect_availability(d: DecisionCreate) -> BiasResult:
    """Recent vivid example driving the choice."""
    text = _haystack(d)
    triggers = [
        r"(last week|yesterday|recently) .{0,40}(happened|saw|heard)",
        r"my (friend|cousin|roommate) .{0,40}(told me|said|got)",
        r"i (just|recently) read",
    ]
    for pattern in triggers:
        m = re.search(pattern, text)
        if m:
            return (
                "availability_bias",
                f"Phrase '{m.group(0)}' suggests one vivid recent example is "
                "shaping the decision. Is it representative of typical outcomes?",
            )
    return None


def detect_loss_aversion(d: DecisionCreate) -> BiasResult:
    text = _haystack(d)
    loss_words = ["lose", "losing", "loss", "give up", "let go"]
    gain_words = ["gain", "win", "earn", "get"]
    losses = sum(text.count(w) for w in loss_words)
    gains = sum(text.count(w) for w in gain_words)
    if losses >= 3 and losses >= 2 * max(gains, 1):
        return (
            "loss_aversion",
            f"Reasoning mentions losses {losses}x vs gains {gains}x. "
            "You may be weighting potential loss more heavily than potential gain.",
        )
    return None


def detect_optimism(d: DecisionCreate) -> BiasResult:
    if d.confidence < 85:
        return None
    text = _haystack(d)
    contingency_words = ["if it doesn't work", "backup", "fallback", "worst case", "plan b"]
    if not any(w in text for w in contingency_words):
        return (
            "optimism_bias",
            f"Confidence is {d.confidence}/100 but no contingency mentioned. "
            "High confidence without a fallback plan is a common failure mode.",
        )
    return None


ALL_DETECTORS: list[Detector] = [
    detect_sunk_cost,
    detect_anchoring,
    detect_confirmation,
    detect_availability,
    detect_loss_aversion,
    detect_optimism,
]


def run_all(d: DecisionCreate) -> list[tuple[str, str]]:
    """Run every detector and return the list of (slug, evidence) flags."""
    results: list[tuple[str, str]] = []
    for detector in ALL_DETECTORS:
        flag = detector(d)
        if flag is not None:
            results.append(flag)
    return results
