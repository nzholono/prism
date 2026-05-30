"""Contract tests for the Prism web client.

These run the web app in-process and assert it renders the right HTML pages.
They don't hit a real Pharos; the web client is configured to talk to our
seeded in-process Pharos through a delegating transport.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def web_client(http):
    """Build the web app with its ApiClient pointed at our in-process Pharos."""
    from prism import web

    # Patch ApiClient inside the web module so requests go to our http fixture
    # instead of trying to reach a real localhost:8000.
    original = web.ApiClient

    def make_client(*_a, **_kw):
        from prism.api_client import make_in_process_client

        return make_in_process_client(http)

    web.ApiClient = make_client  # type: ignore[assignment]
    try:
        with TestClient(web.create_app()) as c:
            yield c
    finally:
        web.ApiClient = original  # type: ignore[assignment]


def test_home_renders(web_client):
    r = web_client.get("/")
    assert r.status_code == 200
    assert "Prism" in r.text
    assert "Browse legal domains" in r.text


def test_domains_index_includes_tenant(web_client):
    r = web_client.get("/domains")
    assert r.status_code == 200
    assert "Tenant Rights" in r.text


def test_domain_detail_includes_scenarios(web_client):
    r = web_client.get("/domains/tenant")
    assert r.status_code == 200
    assert "deposit-not-returned" in r.text or "deposit" in r.text.lower()


def test_scenario_renders_walkthrough(web_client):
    r = web_client.get("/scenarios/deposit-not-returned")
    assert r.status_code == 200
    assert "765 ILCS 710" in r.text


def test_ethics_form_renders(web_client):
    r = web_client.get("/ethics")
    assert r.status_code == 200
    assert "<textarea" in r.text


def test_ethics_post_analyzes(web_client):
    r = web_client.post("/ethics", data={"situation": "Should I sue?"})
    assert r.status_code == 200
    assert "Utilitarian" in r.text
    assert "Deontological" in r.text


def test_stats_renders(web_client):
    r = web_client.get("/stats")
    assert r.status_code == 200
    assert "Domains" in r.text
