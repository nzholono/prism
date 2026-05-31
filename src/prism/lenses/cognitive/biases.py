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


STATUS_QUO_PATTERNS = [
    r"i've always",
    r"this is how (it'?s |i'?ve )always",
    r"why change now",
    r"don'?t fix what isn'?t broken",
    r"keep things (the same|as they are)",
]


def detect_status_quo(d: DecisionCreate) -> BiasResult:
    """Defaulting to no-change without examining alternatives."""
    text = _haystack(d)
    for pattern in STATUS_QUO_PATTERNS:
        m = re.search(pattern, text)
        if m:
            return (
                "status_quo",
                f"Phrase '{m.group(0)}' suggests defaulting to no-change. "
                "Examine the alternatives as if you had to pick fresh.",
            )
    # also flag when "do nothing" / "keep" is chosen with minimal reasoning
    if (
        d.chosen.lower() in {"do nothing", "stay", "wait", "no change"}
        and len(d.reasoning) < 60
    ):
        return (
            "status_quo",
            f"Chose '{d.chosen}' with very short reasoning. The 'no change' "
            "option deserves the same scrutiny as the active ones.",
        )
    return None


BANDWAGON_PATTERNS = [
    r"everyone (else )?(is|does|says)",
    r"my (friends?|family|coworkers?|classmates?) (all |are )",
    r"(everybody|nobody) does",
    r"that'?s what people do",
]


def detect_bandwagon(d: DecisionCreate) -> BiasResult:
    """Choosing because others chose, not because the choice fits the situation."""
    text = _haystack(d)
    for pattern in BANDWAGON_PATTERNS:
        m = re.search(pattern, text)
        if m:
            return (
                "bandwagon",
                f"Phrase '{m.group(0)}' suggests social proof is driving the "
                "choice. Would you still pick this if others weren't?",
            )
    return None


FRAMING_PATTERNS = [
    (r"\bonly\b.*(lose|cost|risk)", "downside framing"),
    (r"\bguaranteed\b", "certainty framing"),
    (r"\b\d+% (success|chance|likely)", "positive percentage framing"),
    (r"\b\d+% (fail|risk|likely to)", "negative percentage framing"),
]


def detect_framing(d: DecisionCreate) -> BiasResult:
    """Reasoning leans heavily on one frame (gain vs loss, certainty vs probability)."""
    text = _haystack(d)
    for pattern, label in FRAMING_PATTERNS:
        m = re.search(pattern, text)
        if m:
            return (
                "framing",
                f"Phrase '{m.group(0)}' uses {label}. Try flipping the frame — "
                "if the same fact were described the opposite way, would you choose differently?",
            )
    return None


def detect_planning_fallacy(d: DecisionCreate) -> BiasResult:
    """Underestimating time/cost — common when chosen path involves work."""
    text = _haystack(d)
    quick_words = ["quick", "easy", "simple", "fast", "shouldn't take", "just a"]
    risk_words = ["might take longer", "could take", "if it drags", "buffer", "delay"]
    quick = sum(text.count(w) for w in quick_words)
    risk = sum(text.count(w) for w in risk_words)
    if quick >= 2 and risk == 0:
        return (
            "planning_fallacy",
            f"Reasoning uses 'quick/easy/simple' {quick}x with no mention of "
            "delays or longer-than-expected scenarios. Most plans take longer "
            "than expected — what if this one does?",
        )
    return None


ALL_DETECTORS: list[Detector] = [
    detect_sunk_cost,
    detect_anchoring,
    detect_confirmation,
    detect_availability,
    detect_loss_aversion,
    detect_optimism,
    detect_status_quo,
    detect_bandwagon,
    detect_framing,
    detect_planning_fallacy,
]


def run_all(d: DecisionCreate) -> list[tuple[str, str]]:
    """Run every detector and return the list of (slug, evidence) flags."""
    results: list[tuple[str, str]] = []
    for detector in ALL_DETECTORS:
        flag = detector(d)
        if flag is not None:
            results.append(flag)
    return results
