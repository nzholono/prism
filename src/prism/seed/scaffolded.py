"""DEPRECATED — Tier-2 domains are now in their own modules (campus.py,
healthcare.py, mental_health.py, immigration.py, traffic.py).

This module is kept for backward compatibility but is a no-op.
"""

from __future__ import annotations

import sqlite3


def seed(conn: sqlite3.Connection) -> None:  # pragma: no cover
    """No-op. Real Tier-2 content is now in individual modules."""
