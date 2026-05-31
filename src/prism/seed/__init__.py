"""Seed data entry point.

`seed_all(conn)` runs every seeder. All seeders are idempotent — safe to run
on every startup.

Layers:
  - ethical: 4 frameworks (utilitarian, deontological, virtue, care)
  - tenant, employment, police, consumer: Tier-1 domains (deep)
  - campus, healthcare, mental_health, immigration, traffic: Tier-2 domains
    (at least one full walkthrough each; designed to be grown via the
    `add-scenario` skill)
"""

from __future__ import annotations

import sqlite3

from prism.seed import (
    campus,
    consumer,
    employment,
    ethical,
    healthcare,
    immigration,
    mental_health,
    police,
    tenant,
    traffic,
)


def seed_all(conn: sqlite3.Connection) -> None:
    ethical.seed(conn)
    # Tier 1
    tenant.seed(conn)
    employment.seed(conn)
    police.seed(conn)
    consumer.seed(conn)
    # Tier 2 (real content, not stubs)
    campus.seed(conn)
    healthcare.seed(conn)
    mental_health.seed(conn)
    immigration.seed(conn)
    traffic.seed(conn)
