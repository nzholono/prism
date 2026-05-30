"""Integration test: ApiClient → Pharos round trip through an in-process app."""

from __future__ import annotations


def test_health_through_apiclient(in_process_client):
    r = in_process_client.health()
    assert r.status == "ok"
    assert r.version
