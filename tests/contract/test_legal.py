"""Contract tests for the legal-lens endpoints: domains, scenarios, statutes, search."""

from __future__ import annotations


def test_list_domains_returns_tenant(http):
    r = http.get("/domains")
    assert r.status_code == 200
    slugs = [d["slug"] for d in r.json()]
    assert "tenant" in slugs


def test_get_domain_returns_nested_statutes_and_scenarios(http):
    r = http.get("/domains/tenant")
    assert r.status_code == 200
    body = r.json()
    assert body["slug"] == "tenant"
    assert len(body["statutes"]) >= 3
    assert len(body["scenarios"]) >= 1


def test_get_unknown_domain_returns_404(http):
    r = http.get("/domains/does-not-exist")
    assert r.status_code == 404


def test_get_scenario_includes_linked_statutes(http):
    r = http.get("/scenarios/deposit-not-returned")
    assert r.status_code == 200
    body = r.json()
    assert body["slug"] == "deposit-not-returned"
    assert any("765 ILCS 710/1" in st["citation"] for st in body["statutes"])


def test_list_scenarios_filter_by_domain(http):
    r = http.get("/scenarios", params={"domain": "tenant"})
    assert r.status_code == 200
    body = r.json()
    assert all(isinstance(s["title"], str) for s in body)
    assert len(body) >= 1


def test_search_finds_deposit_scenario(http):
    r = http.get("/search", params={"q": "deposit"})
    assert r.status_code == 200
    hits = r.json()
    titles = [h["title"] for h in hits]
    assert any("deposit" in t.lower() for t in titles)


def test_search_empty_query_returns_empty(http):
    r = http.get("/search", params={"q": ""})
    assert r.status_code == 200
    assert r.json() == []
