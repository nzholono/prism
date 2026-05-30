"""Prism MCP server — exposes the legal/ethical/cognitive layers over MCP.

Runs over stdio. Lets Claude Code (or any MCP-aware client) query Prism's
curated Illinois legal knowledge, run ethical analyses, and log decisions.

Run with `uv run prism-mcp` (no Pharos required — talks to the DB directly
through the service layer, so it works even if the user hasn't started Pharos).
"""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from prism import db, service
from prism.models import DecisionCreate, DecisionUpdate
from prism.seed import seed_all

mcp = FastMCP("prism")


def _conn():
    """Open a fresh connection and ensure schema + seed. SQLite is thread-safe enough for this."""
    conn = db.connect()
    db.init_schema(conn)
    seed_all(conn)
    return conn


# ──────────────────────────────────────────────────────────────────────────────
# Legal tools
# ──────────────────────────────────────────────────────────────────────────────


@mcp.tool()
def list_domains() -> str:
    """List every Illinois legal domain covered by Prism."""
    with _conn() as conn:
        domains = service.list_domains(conn)
    return "\n".join(f"- {d.slug}: {d.name} (tier {d.tier}) — {d.summary}" for d in domains)


@mcp.tool()
def get_domain(slug: str) -> str:
    """Fetch a domain with its statutes and scenarios. Pass the slug, e.g. 'tenant'."""
    with _conn() as conn:
        d = service.get_domain(conn, slug)
    if d is None:
        return f"No domain named '{slug}'."
    out = [f"# {d.name}", "", d.summary, "", "## Statutes"]
    for s in d.statutes:
        out.append(f"- **{s.citation}** — {s.title}")
    out.extend(["", "## Scenarios"])
    for sc in d.scenarios:
        out.append(f"- **{sc.slug}** — {sc.title}")
    return "\n".join(out)


@mcp.tool()
def get_scenario(slug: str) -> str:
    """Fetch a full scenario walkthrough with linked statutes. E.g. 'deposit-not-returned'."""
    with _conn() as conn:
        sc = service.get_scenario(conn, slug)
    if sc is None:
        return f"No scenario named '{slug}'."
    body = f"# {sc.title}\n\n{sc.description_md}\n\n{sc.walkthrough_md}\n"
    if sc.statutes:
        body += "\n## Applicable statutes\n"
        for s in sc.statutes:
            body += f"\n- **{s.citation}** — {s.title}\n  {s.summary}\n"
    if sc.template_md:
        body += f"\n{sc.template_md}\n"
    return body


@mcp.tool()
def search(query: str, limit: int = 10) -> str:
    """Cross-domain text search across statutes and scenarios."""
    with _conn() as conn:
        hits = service.search(conn, query, limit=limit)
    if not hits:
        return f"No matches for '{query}'."
    return "\n".join(
        f"- [{h.kind}] **{h.title}** ({h.domain_slug}) — {h.snippet}" for h in hits
    )


# ──────────────────────────────────────────────────────────────────────────────
# Ethical tool
# ──────────────────────────────────────────────────────────────────────────────


@mcp.tool()
def analyze_ethically(situation: str) -> str:
    """Frame a situation through utilitarian, deontological, virtue, and care ethics."""
    with _conn() as conn:
        analysis = service.analyze_ethically(conn, situation)
    out = [f"# Ethical analysis", f"_{analysis.situation}_", ""]
    for p in analysis.perspectives:
        out.append(f"## {p.framework_name}")
        out.append(p.framing)
        out.append("\n**Key questions:**")
        for q in p.questions:
            out.append(f"- {q}")
        out.append("")
    return "\n".join(out)


# ──────────────────────────────────────────────────────────────────────────────
# Cognitive tools (decision journal)
# ──────────────────────────────────────────────────────────────────────────────


@mcp.tool()
def log_decision(
    situation: str,
    options: list[str],
    chosen: str,
    reasoning: str,
    expected_outcome: str,
    confidence: int,
) -> str:
    """Log a decision in Prism's journal. Returns the created entry with any bias flags."""
    d = DecisionCreate(
        situation=situation,
        options=options,
        chosen=chosen,
        reasoning=reasoning,
        expected_outcome=expected_outcome,
        confidence=confidence,
    )
    with _conn() as conn:
        decision = service.create_decision(conn, d)
    out = [
        f"Decision #{decision.id} logged.",
        f"Chose: {decision.chosen} (confidence {decision.confidence})",
    ]
    if decision.biases:
        out.append("\nBias flags raised:")
        for b in decision.biases:
            out.append(f"- **{b.bias_slug}**: {b.evidence}")
    else:
        out.append("\nNo bias flags raised by the automated detectors.")
    return "\n".join(out)


@mcp.tool()
def recent_decisions(limit: int = 5) -> str:
    """List the user's most recent decisions."""
    with _conn() as conn:
        decisions = service.list_decisions(conn, limit=limit)
    if not decisions:
        return "No decisions logged yet."
    out = []
    for d in decisions:
        biases = ", ".join(b.bias_slug for b in d.biases) or "—"
        outcome = d.actual_outcome or "(not yet reviewed)"
        out.append(
            f"#{d.id} ({d.created_at.strftime('%Y-%m-%d')}): {d.situation}\n"
            f"  Chose {d.chosen} at confidence {d.confidence}.\n"
            f"  Biases: {biases}\n  Outcome: {outcome}\n"
        )
    return "\n".join(out)


@mcp.tool()
def review_decision(decision_id: int, actual_outcome: str) -> str:
    """Record what actually happened for a past decision."""
    with _conn() as conn:
        d = service.update_decision(
            conn, decision_id, DecisionUpdate(actual_outcome=actual_outcome)
        )
    if d is None:
        return f"No decision #{decision_id}."
    return f"Decision #{d.id} updated. Actual outcome recorded."


@mcp.tool()
def stats() -> str:
    """Return overall counts (domains, statutes, scenarios, decisions, bias flags)."""
    with _conn() as conn:
        s = service.get_stats(conn)
    return json.dumps(s.model_dump(), indent=2)


# ──────────────────────────────────────────────────────────────────────────────
# Resources & prompts
# ──────────────────────────────────────────────────────────────────────────────


@mcp.resource("scenario://{slug}")
def scenario_resource(slug: str) -> str:
    """Read a scenario as a resource (useful for citing the source in Claude's context)."""
    with _conn() as conn:
        sc = service.get_scenario(conn, slug)
    if sc is None:
        return f"No scenario named '{slug}'."
    return f"# {sc.title}\n\n{sc.walkthrough_md}"


@mcp.prompt()
def bias_audit_prompt(decision_id: int) -> str:
    """Prompt template for running a deep bias audit on a journal entry."""
    return (
        f"Please run a bias-audit pass over Prism decision #{decision_id}. "
        f"Use the `recent_decisions` tool to find it, then walk through the "
        f"checklist in the `.claude/skills/bias-audit/SKILL.md` skill. Output "
        f"a markdown report. Be honest — don't invent biases."
    )


def main() -> None:
    """Entry point for `uv run prism-mcp`."""
    mcp.run()


if __name__ == "__main__":
    main()
