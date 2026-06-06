"""Bias-detector audit log.

Every time `service.create_decision` runs, we append a JSONL entry recording
the decision's reasoning text and which biases were flagged. The point is
exactly what Prof. Pitcher suggested in CSC299 Discord: capture the
inputs/outputs of the regex-based detectors so we can audit them later (by
hand, or by feeding the log into Claude Code) and find biases the rules
missed.

This is a *feedback loop* on the detector design, not a runtime feature
users see. The log is local-only (`~/.prism/bias_audit.jsonl`).
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

BIAS_AUDIT_LOG_PATH = Path.home() / ".prism" / "bias_audit.jsonl"


def _log_path() -> Path:
    """Indirection so tests can monkeypatch the path easily."""
    return BIAS_AUDIT_LOG_PATH


def log_bias_run(
    *,
    situation: str,
    options: list[str],
    chosen: str,
    reasoning: str,
    expected_outcome: str,
    confidence: int,
    flags_found: list[tuple[str, str]],
    log_path: Path | None = None,
) -> None:
    """Append one bias-detector run to the audit log (JSONL)."""
    path = log_path or _log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds"),
        "situation": situation,
        "options": options,
        "chosen": chosen,
        "reasoning": reasoning,
        "expected_outcome": expected_outcome,
        "confidence": confidence,
        "biases_flagged": [
            {"slug": slug, "evidence": evidence} for slug, evidence in flags_found
        ],
    }
    with path.open("a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def read_log(log_path: Path | None = None) -> list[dict]:
    """Read every entry from the audit log. Empty list if the log doesn't exist."""
    path = log_path or _log_path()
    if not path.exists():
        return []
    out: list[dict] = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out
