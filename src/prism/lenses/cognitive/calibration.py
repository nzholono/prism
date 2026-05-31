"""Calibration: analyze the user's reviewed decisions to spot patterns.

The point isn't to grade the user, it's to show them how their *confidence*
tracks (or doesn't track) reality. Are you overconfident? Underconfident?
Do certain biases correlate with bad outcomes?

This is the most impressive feature of the cognitive lens — it lets users
see their own thinking from outside.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from prism.models import Decision


@dataclass
class CalibrationReport:
    total: int = 0
    reviewed: int = 0
    avg_confidence: float = 0.0
    avg_confidence_when_outcome_good: float = 0.0
    avg_confidence_when_outcome_bad: float = 0.0
    most_common_biases: list[tuple[str, int]] = field(default_factory=list)
    bias_decisions_reviewed: int = 0
    bias_decisions_bad_outcome: int = 0
    pattern_notes: list[str] = field(default_factory=list)

    def summary(self) -> str:
        if self.total == 0:
            return "No decisions logged yet."
        if self.reviewed == 0:
            return (
                f"{self.total} decisions logged, none reviewed yet. "
                f"Use `prism-cli decide review <id>` to record actual outcomes "
                f"— calibration needs reviewed entries to work."
            )
        lines = [
            f"Decisions logged: {self.total}",
            f"Decisions reviewed: {self.reviewed} ({100*self.reviewed//max(self.total,1)}%)",
            f"Average confidence: {self.avg_confidence:.0f}/100",
        ]
        if self.avg_confidence_when_outcome_good or self.avg_confidence_when_outcome_bad:
            lines.append(
                f"Avg confidence when outcome went well: "
                f"{self.avg_confidence_when_outcome_good:.0f}"
            )
            lines.append(
                f"Avg confidence when outcome went poorly: "
                f"{self.avg_confidence_when_outcome_bad:.0f}"
            )
        if self.most_common_biases:
            lines.append("\nMost frequently flagged biases:")
            for slug, count in self.most_common_biases:
                lines.append(f"  - {slug}: {count} time(s)")
        if self.pattern_notes:
            lines.append("\nPatterns:")
            for note in self.pattern_notes:
                lines.append(f"  - {note}")
        return "\n".join(lines)


# Heuristic: an outcome is "bad" if the actual outcome text contains certain
# negative cues. This is crude but deterministic — keeps the project test-able
# without bringing in sentiment analysis.
_NEGATIVE_OUTCOME_CUES = [
    "didn't work",
    "did not work",
    "regret",
    "wish i hadn't",
    "wish i had",
    "lost",
    "failed",
    "denied",
    "rejected",
    "fired",
    "no",
    "worse",
    "mistake",
    "should have",
    "would have",
    "won't pay",
    "wouldn't",
    "couldn't",
    "backfired",
]


def _outcome_is_bad(text: str) -> bool:
    low = text.lower()
    return any(cue in low for cue in _NEGATIVE_OUTCOME_CUES)


def calibrate(decisions: list[Decision]) -> CalibrationReport:
    """Build a CalibrationReport from a list of decisions."""
    report = CalibrationReport(total=len(decisions))
    if not decisions:
        return report

    reviewed = [d for d in decisions if d.actual_outcome]
    report.reviewed = len(reviewed)
    report.avg_confidence = sum(d.confidence for d in decisions) / len(decisions)

    good_confs: list[int] = []
    bad_confs: list[int] = []
    for d in reviewed:
        if _outcome_is_bad(d.actual_outcome or ""):
            bad_confs.append(d.confidence)
        else:
            good_confs.append(d.confidence)
    if good_confs:
        report.avg_confidence_when_outcome_good = sum(good_confs) / len(good_confs)
    if bad_confs:
        report.avg_confidence_when_outcome_bad = sum(bad_confs) / len(bad_confs)

    counter: Counter[str] = Counter()
    bias_reviewed = 0
    bias_bad = 0
    for d in decisions:
        slugs = {b.bias_slug for b in d.biases}
        for slug in slugs:
            counter[slug] += 1
        if slugs and d.actual_outcome:
            bias_reviewed += 1
            if _outcome_is_bad(d.actual_outcome):
                bias_bad += 1
    report.most_common_biases = counter.most_common(5)
    report.bias_decisions_reviewed = bias_reviewed
    report.bias_decisions_bad_outcome = bias_bad

    # Pattern notes
    if good_confs and bad_confs:
        gap = report.avg_confidence_when_outcome_bad - report.avg_confidence_when_outcome_good
        if gap > 10:
            report.pattern_notes.append(
                "When outcomes went poorly, you were on average "
                f"{gap:.0f} points MORE confident — classic overconfidence pattern."
            )
        elif gap < -10:
            report.pattern_notes.append(
                "You were less confident on decisions that went well — "
                "you may underestimate your own judgment."
            )
    if bias_reviewed >= 3:
        rate = 100 * bias_bad // bias_reviewed
        if rate >= 60:
            report.pattern_notes.append(
                f"{rate}% of decisions with flagged biases ended badly. "
                "The bias flags are predictive — take them seriously."
            )
    if report.avg_confidence >= 80 and report.reviewed >= 5:
        report.pattern_notes.append(
            "Your average confidence is high (≥80). Real-world calibration "
            "research suggests confidence above 80 is rarely justified outside "
            "narrow domains."
        )
    return report
