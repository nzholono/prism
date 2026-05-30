"""Seed data entry point.

`seed_all(conn)` runs every seeder. All seeders are idempotent — safe to run
on every startup.

Layers:
  - ethical: 4 frameworks (utilitarian, deontological, virtue, care)
  - tenant, employment, police, consumer: Tier-1 (deep) domains
  - scaffolded: Tier-2 domains with structure and one sample scenario each,
    designed to be grown via the `add-scenario` skill
"""

from __future__ import annotations

import sqlite3

from prism.seed import consumer, employment, ethical, police, scaffolded, tenant


def seed_all(conn: sqlite3.Connection) -> None:
    ethical.seed(conn)
    tenant.seed(conn)
    employment.seed(conn)
    police.seed(conn)
    consumer.seed(conn)
    scaffolded.seed(conn)
