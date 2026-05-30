"""Pydantic models shared between server and clients.

These define the wire format for the REST API. If you change a model here,
both Pharos and every client see the change consistently.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


# ──────────────────────────────────────────────────────────────────────────────
# Legal lens
# ──────────────────────────────────────────────────────────────────────────────

class Domain(BaseModel):
    id: int
    slug: str
    name: str
    tier: Literal[1, 2]
    summary: str


class Statute(BaseModel):
    id: int
    domain_id: int
    citation: str
    title: str
    summary: str
    body_md: str
    source_url: str | None = None


class Scenario(BaseModel):
    id: int
    domain_id: int
    slug: str
    title: str
    description_md: str
    walkthrough_md: str
    template_md: str | None = None
    statutes: list[Statute] = Field(default_factory=list)


class DomainDetail(Domain):
    statutes: list[Statute] = Field(default_factory=list)
    scenarios: list[Scenario] = Field(default_factory=list)


# ──────────────────────────────────────────────────────────────────────────────
# Ethical lens
# ──────────────────────────────────────────────────────────────────────────────

class EthicalFramework(BaseModel):
    id: int
    slug: str
    name: str
    description_md: str
    key_questions: list[str]


class EthicalAnalysisRequest(BaseModel):
    situation: str


class EthicalPerspective(BaseModel):
    framework_slug: str
    framework_name: str
    questions: list[str]
    framing: str  # how this framework would frame the choice


class EthicalAnalysis(BaseModel):
    situation: str
    perspectives: list[EthicalPerspective]


# ──────────────────────────────────────────────────────────────────────────────
# Cognitive lens — decision journal + bias flags
# ──────────────────────────────────────────────────────────────────────────────

class DecisionCreate(BaseModel):
    situation: str
    options: list[str]
    chosen: str
    reasoning: str
    expected_outcome: str
    confidence: int = Field(ge=0, le=100)
    linked_scenario_id: int | None = None


class DecisionUpdate(BaseModel):
    actual_outcome: str | None = None


class BiasFlag(BaseModel):
    id: int
    bias_slug: str
    evidence: str


class Decision(BaseModel):
    id: int
    created_at: datetime
    situation: str
    options: list[str]
    chosen: str
    reasoning: str
    expected_outcome: str
    confidence: int
    linked_scenario_id: int | None = None
    actual_outcome: str | None = None
    reviewed_at: datetime | None = None
    biases: list[BiasFlag] = Field(default_factory=list)


# ──────────────────────────────────────────────────────────────────────────────
# Meta
# ──────────────────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: Literal["ok"]
    version: str


class Stats(BaseModel):
    domains: int
    statutes: int
    scenarios: int
    decisions: int
    bias_flags: int


class SearchHit(BaseModel):
    kind: Literal["statute", "scenario"]
    id: int
    title: str
    snippet: str
    domain_slug: str
