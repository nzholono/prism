"""Integration tests: ApiClient → Pharos round trip through an in-process app.

These prove the shared ApiClient really does work against the real server
the way every UI client uses it.
"""

from __future__ import annotations

from prism.models import DecisionCreate, DecisionUpdate


def test_health_through_apiclient(in_process_client):
    r = in_process_client.health()
    assert r.status == "ok"
    assert r.version


def test_browse_tenant_domain(in_process_client):
    d = in_process_client.get_domain("tenant")
    assert d.slug == "tenant"
    assert any(sc.slug == "deposit-not-returned" for sc in d.scenarios)
    assert any("765 ILCS 710/1" in s.citation for s in d.statutes)


def test_scenario_has_linked_statutes(in_process_client):
    sc = in_process_client.get_scenario("deposit-not-returned")
    citations = [st.citation for st in sc.statutes]
    assert "765 ILCS 710/1" in citations


def test_search_across_kinds(in_process_client):
    hits = in_process_client.search("deposit")
    kinds = {h.kind for h in hits}
    assert "scenario" in kinds or "statute" in kinds


def test_ethical_analysis_returns_all_four_lenses(in_process_client):
    analysis = in_process_client.analyze_ethically("Should I sue?")
    assert {p.framework_slug for p in analysis.perspectives} == {
        "utilitarian",
        "deontological",
        "virtue",
        "care",
    }


def test_decision_flow_log_review_delete(in_process_client):
    """End-to-end: create a decision, see biases, record outcome, delete."""
    created = in_process_client.create_decision(
        DecisionCreate(
            situation="My landlord won't return my $1200 deposit.",
            options=["Sue in small claims", "Drop it"],
            chosen="Sue in small claims",
            reasoning=(
                "I've already spent 10 hours on this. The law is clearly on my side. "
                "It will definitely work out."
            ),
            expected_outcome="I get the deposit back doubled.",
            confidence=92,
        )
    )
    assert created.id
    bias_slugs = {b.bias_slug for b in created.biases}
    assert "sunk_cost" in bias_slugs

    listed = in_process_client.list_decisions()
    assert any(d.id == created.id for d in listed)

    reviewed = in_process_client.update_decision(
        created.id, DecisionUpdate(actual_outcome="Settled for the original deposit.")
    )
    assert reviewed.actual_outcome == "Settled for the original deposit."
    assert reviewed.reviewed_at is not None

    in_process_client.delete_decision(created.id)
    listed_after = in_process_client.list_decisions()
    assert not any(d.id == created.id for d in listed_after)
