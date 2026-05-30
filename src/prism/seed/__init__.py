"""Seed data entry point.

`seed_all(conn)` runs every domain + ethical-framework seeder. All seeders are
idempotent — safe to run on every startup.
"""

from __future__ import annotations

import sqlite3

from prism.seed import ethical, tenant


def seed_all(conn: sqlite3.Connection) -> None:
    ethical.seed(conn)
    tenant.seed(conn)
    # add new domain seeders here as they're built
