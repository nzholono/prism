"""Tests for the bias-detector audit log.

The log captures every regex-detector run so the design can be evaluated
(by hand or by feeding to Claude Code) for missed biases — the feedback
loop suggested by Prof. Pitcher in CSC299 Discord on 2026-06-04.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from prism.lenses.cognitive import audit


@pytest.fixture
def tmp_log_path(tmp_path: Path) -> Path:
    return tmp_path / "bias_audit.jsonl"


def test_log_creates_file(tmp_log_path):
    audit.log_bias_run(
        situation="A",
        options=["x", "y"],
        chosen="x",
        reasoning="reasoning",
        expected_outcome="ok",
        confidence=50,
        flags_found=[],
        log_path=tmp_log_path,
    )
    assert tmp_log_path.exists()


def test_log_appends_one_jsonl_line_per_call(tmp_log_path):
    for i in range(3):
        audit.log_bias_run(
            situation=f"situation {i}",
            options=["a", "b"],
            chosen="a",
            reasoning="reasoning",
            expected_outcome="ok",
            confidence=50,
            flags_found=[],
            log_path=tmp_log_path,
        )
    lines = tmp_log_path.read_text().strip().split("\n")
    assert len(lines) == 3
    for line in lines:
        json.loads(line)  # each line is valid JSON


def test_log_records_situation_and_flags(tmp_log_path):
    audit.log_bias_run(
        situation="My landlord won't return my deposit.",
        options=["sue", "drop"],
        chosen="sue",
        reasoning="I've already spent so much time.",
        expected_outcome="I win.",
        confidence=95,
        flags_found=[("sunk_cost", "Phrase 'already spent' suggests …")],
        log_path=tmp_log_path,
    )
    entry = json.loads(tmp_log_path.read_text().strip())
    assert entry["situation"].startswith("My landlord")
    assert entry["reasoning"] == "I've already spent so much time."
    assert entry["confidence"] == 95
    assert entry["biases_flagged"][0]["slug"] == "sunk_cost"


def test_read_log_returns_empty_when_no_file(tmp_log_path):
    assert audit.read_log(tmp_log_path) == []


def test_read_log_roundtrip(tmp_log_path):
    for i in range(2):
        audit.log_bias_run(
            situation=f"s{i}",
            options=["a", "b"],
            chosen="a",
            reasoning=f"r{i}",
            expected_outcome="ok",
            confidence=50 + i,
            flags_found=[("sunk_cost", "evidence")] if i == 0 else [],
            log_path=tmp_log_path,
        )
    entries = audit.read_log(tmp_log_path)
    assert len(entries) == 2
    assert entries[0]["situation"] == "s0"
    assert entries[0]["biases_flagged"][0]["slug"] == "sunk_cost"
    assert entries[1]["biases_flagged"] == []
