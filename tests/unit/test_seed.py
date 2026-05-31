"""Unit-ish tests for the seed modules.

These exercise the seed functions directly against an in-memory DB to make
sure every domain seeds idempotently with valid structure.
"""

from __future__ import annotations

import sqlite3

import pytest

from prism import db
from prism.seed import (
    campus,
    consumer,
    criminal_record,
    employment,
    ethical,
    healthcare,
    immigration,
    mental_health,
    police,
    tenant,
    traffic,
)


ALL_DOMAIN_MODULES = [
    ethical,
    tenant,
    employment,
    police,
    consumer,
    campus,
    healthcare,
    mental_health,
    immigration,
    traffic,
    criminal_record,
]


@pytest.fixture
def conn() -> sqlite3.Connection:
    c = db.connect(":memory:")
    db.init_schema(c)
    yield c
    c.close()


@pytest.mark.parametrize("module", ALL_DOMAIN_MODULES)
def test_seed_module_runs_without_error(conn, module):
    module.seed(conn)


@pytest.mark.parametrize("module", ALL_DOMAIN_MODULES)
def test_seed_module_is_idempotent(conn, module):
    """Running seed twice produces the same row counts."""
    module.seed(conn)
    counts_after_first = _counts(conn)
    module.seed(conn)
    counts_after_second = _counts(conn)
    assert counts_after_first == counts_after_second


def test_tenant_seeds_have_linked_statutes(conn):
    tenant.seed(conn)
    deposit = conn.execute(
        "SELECT id FROM scenarios WHERE slug = 'deposit-not-returned'"
    ).fetchone()
    assert deposit is not None
    linked = conn.execute(
        "SELECT COUNT(*) FROM scenario_statutes WHERE scenario_id = ?",
        (deposit["id"],),
    ).fetchone()[0]
    assert linked >= 3


def test_ethical_seeds_four_frameworks(conn):
    ethical.seed(conn)
    slugs = {
        r["slug"]
        for r in conn.execute("SELECT slug FROM ethical_frameworks").fetchall()
    }
    assert slugs == {"utilitarian", "deontological", "virtue", "care"}


def test_all_tier2_domains_present_after_full_seed(conn):
    """After seed_all, the five Tier-2 domains exist with at least 1 scenario."""
    from prism.seed import seed_all

    seed_all(conn)
    expected = {"campus", "healthcare", "immigration", "mental-health", "traffic"}
    slugs = {
        r["slug"] for r in conn.execute("SELECT slug FROM domains").fetchall()
    }
    assert expected <= slugs

    for slug in expected:
        domain_id = conn.execute(
            "SELECT id FROM domains WHERE slug = ?", (slug,)
        ).fetchone()["id"]
        scenarios = conn.execute(
            "SELECT COUNT(*) FROM scenarios WHERE domain_id = ?", (domain_id,)
        ).fetchone()[0]
        assert scenarios >= 1, f"Domain {slug} has no scenarios"


def _counts(conn: sqlite3.Connection) -> dict:
    return {
        t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        for t in (
            "domains",
            "statutes",
            "scenarios",
            "scenario_statutes",
            "ethical_frameworks",
        )
    }
