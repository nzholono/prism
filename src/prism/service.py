"""Service layer: business logic shared by the REST server and the MCP server.

Every read and write against the database goes through a function here. Both
`server.py` (HTTP) and `mcp_server.py` (MCP/stdio) call into this module so
they stay consistent.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime

from prism.lenses.cognitive import audit, biases
from prism.models import (
    BiasFlag,
    Decision,
    DecisionCreate,
    DecisionUpdate,
    Domain,
    DomainDetail,
    EthicalAnalysis,
    EthicalFramework,
    EthicalPerspective,
    Scenario,
    SearchHit,
    Stats,
    Statute,
)

# ──────────────────────────────────────────────────────────────────────────────
# Domains
# ──────────────────────────────────────────────────────────────────────────────


def list_domains(conn: sqlite3.Connection) -> list[Domain]:
    rows = conn.execute(
        "SELECT id, slug, name, tier, summary FROM domains ORDER BY tier, name"
    ).fetchall()
    return [Domain(**dict(r)) for r in rows]


def get_domain(conn: sqlite3.Connection, slug: str) -> DomainDetail | None:
    row = conn.execute(
        "SELECT id, slug, name, tier, summary FROM domains WHERE slug = ?", (slug,)
    ).fetchone()
    if row is None:
        return None

    domain_id = row["id"]
    statutes = [
        Statute(**dict(s))
        for s in conn.execute(
            "SELECT id, domain_id, citation, title, summary, body_md, source_url "
            "FROM statutes WHERE domain_id = ? ORDER BY citation",
            (domain_id,),
        ).fetchall()
    ]
    scenarios = [
        Scenario(**dict(sc))
        for sc in conn.execute(
            "SELECT id, domain_id, slug, title, description_md, walkthrough_md, template_md "
            "FROM scenarios WHERE domain_id = ? ORDER BY title",
            (domain_id,),
        ).fetchall()
    ]
    return DomainDetail(**dict(row), statutes=statutes, scenarios=scenarios)


# ──────────────────────────────────────────────────────────────────────────────
# Statutes
# ──────────────────────────────────────────────────────────────────────────────


def get_statute(conn: sqlite3.Connection, statute_id: int) -> Statute | None:
    row = conn.execute(
        "SELECT id, domain_id, citation, title, summary, body_md, source_url "
        "FROM statutes WHERE id = ?",
        (statute_id,),
    ).fetchone()
    return Statute(**dict(row)) if row else None


# ──────────────────────────────────────────────────────────────────────────────
# Scenarios
# ──────────────────────────────────────────────────────────────────────────────


def list_scenarios(
    conn: sqlite3.Connection,
    domain_slug: str | None = None,
    query: str | None = None,
) -> list[Scenario]:
    sql = (
        "SELECT s.id, s.domain_id, s.slug, s.title, s.description_md, "
        "s.walkthrough_md, s.template_md "
        "FROM scenarios s JOIN domains d ON d.id = s.domain_id WHERE 1=1"
    )
    params: list[object] = []
    if domain_slug:
        sql += " AND d.slug = ?"
        params.append(domain_slug)
    if query:
        sql += " AND (s.title LIKE ? OR s.description_md LIKE ?)"
        like = f"%{query}%"
        params.extend([like, like])
    sql += " ORDER BY s.title"

    rows = conn.execute(sql, params).fetchall()
    return [Scenario(**dict(r)) for r in rows]


def get_scenario(conn: sqlite3.Connection, slug: str) -> Scenario | None:
    row = conn.execute(
        "SELECT id, domain_id, slug, title, description_md, walkthrough_md, template_md "
        "FROM scenarios WHERE slug = ?",
        (slug,),
    ).fetchone()
    if row is None:
        return None
    statutes = [
        Statute(**dict(s))
        for s in conn.execute(
            "SELECT st.id, st.domain_id, st.citation, st.title, st.summary, "
            "st.body_md, st.source_url FROM statutes st "
            "JOIN scenario_statutes ss ON ss.statute_id = st.id "
            "WHERE ss.scenario_id = ? ORDER BY st.citation",
            (row["id"],),
        ).fetchall()
    ]
    return Scenario(**dict(row), statutes=statutes)


# ──────────────────────────────────────────────────────────────────────────────
# Search (cross-domain)
# ──────────────────────────────────────────────────────────────────────────────


def search(conn: sqlite3.Connection, query: str, limit: int = 20) -> list[SearchHit]:
    """Cross-domain text search ranked by simple relevance.

    Matches in title weight more heavily than matches in body. Scenarios
    rank above statutes when scores tie (more user-actionable).
    """
    if not query.strip():
        return []
    like = f"%{query}%"
    q_lower = query.lower()

    scored: list[tuple[float, SearchHit]] = []

    for r in conn.execute(
        "SELECT st.id, st.title, st.summary, st.body_md, d.slug AS domain_slug "
        "FROM statutes st JOIN domains d ON d.id = st.domain_id "
        "WHERE st.title LIKE ? OR st.summary LIKE ? OR st.body_md LIKE ?",
        (like, like, like),
    ).fetchall():
        score = _relevance(q_lower, title=r["title"], body=(r["summary"] or "") + " " + (r["body_md"] or ""))
        # statutes get a slight penalty so scenarios float up
        score -= 0.5
        scored.append((
            score,
            SearchHit(
                kind="statute",
                id=r["id"],
                title=r["title"],
                snippet=_excerpt(r["summary"], query),
                domain_slug=r["domain_slug"],
            ),
        ))

    for r in conn.execute(
        "SELECT s.id, s.title, s.description_md, s.walkthrough_md, d.slug AS domain_slug "
        "FROM scenarios s JOIN domains d ON d.id = s.domain_id "
        "WHERE s.title LIKE ? OR s.description_md LIKE ? OR s.walkthrough_md LIKE ?",
        (like, like, like),
    ).fetchall():
        score = _relevance(q_lower, title=r["title"], body=(r["description_md"] or "") + " " + (r["walkthrough_md"] or ""))
        scored.append((
            score,
            SearchHit(
                kind="scenario",
                id=r["id"],
                title=r["title"],
                snippet=_excerpt(r["description_md"], query),
                domain_slug=r["domain_slug"],
            ),
        ))

    # Sort descending by score, then return top N
    scored.sort(key=lambda t: -t[0])
    return [hit for _, hit in scored[:limit]]


def _relevance(query: str, *, title: str, body: str) -> float:
    """Simple relevance score: title matches weight more, repeated matches add up."""
    title_l = title.lower()
    body_l = body.lower()
    score = 0.0
    # exact title match is gold
    if query in title_l:
        score += 5.0
        # whole-word match in title even better
        if f" {query} " in f" {title_l} ":
            score += 2.0
    # body matches scale with frequency, capped
    body_hits = body_l.count(query)
    score += min(body_hits, 5) * 0.5
    return score


def _excerpt(text: str, query: str, width: int = 80) -> str:
    """Return a short snippet centered around the first match of `query`."""
    idx = text.lower().find(query.lower())
    if idx == -1:
        return text[:width].rstrip() + ("…" if len(text) > width else "")
    start = max(0, idx - width // 2)
    end = min(len(text), start + width)
    snippet = text[start:end].strip()
    if start > 0:
        snippet = "…" + snippet
    if end < len(text):
        snippet = snippet + "…"
    return snippet


# ──────────────────────────────────────────────────────────────────────────────
# Ethical frameworks
# ──────────────────────────────────────────────────────────────────────────────


def list_ethical_frameworks(conn: sqlite3.Connection) -> list[EthicalFramework]:
    rows = conn.execute(
        "SELECT id, slug, name, description_md, key_questions FROM ethical_frameworks "
        "ORDER BY name"
    ).fetchall()
    return [
        EthicalFramework(
            id=r["id"],
            slug=r["slug"],
            name=r["name"],
            description_md=r["description_md"],
            key_questions=json.loads(r["key_questions"]),
        )
        for r in rows
    ]


# templated framing — deterministic, no AI required
_FRAMING_TEMPLATES = {
    "utilitarian": (
        "From a utilitarian perspective, the right choice is the one that maximizes "
        "total wellbeing across everyone affected. For this situation, list every "
        "person impacted and try to estimate the net change in their wellbeing under "
        "each option."
    ),
    "deontological": (
        "From a deontological perspective, the right choice respects duties and "
        "rights regardless of outcomes. Ask: which option, if everyone in your "
        "position took it, would lead to a world you can stand behind? Are you "
        "treating anyone merely as a means to your goal?"
    ),
    "virtue": (
        "From a virtue-ethics perspective, the question is not 'what should I do' "
        "but 'who am I becoming'. Which option reflects the character you want — "
        "courage, honesty, fairness, prudence? Which option would you respect in "
        "someone else?"
    ),
    "care": (
        "From a care-ethics perspective, what matters is the concrete relationships "
        "at stake. Whose voice has been heard so far in your reasoning, and whose "
        "is missing? Which option preserves trust and meets the needs of the "
        "specific people involved?"
    ),
}


def analyze_ethically(conn: sqlite3.Connection, situation: str) -> EthicalAnalysis:
    frameworks = list_ethical_frameworks(conn)
    perspectives = [
        EthicalPerspective(
            framework_slug=fw.slug,
            framework_name=fw.name,
            questions=fw.key_questions,
            framing=_FRAMING_TEMPLATES.get(fw.slug, fw.description_md),
        )
        for fw in frameworks
    ]
    return EthicalAnalysis(situation=situation, perspectives=perspectives)


# ──────────────────────────────────────────────────────────────────────────────
# Decisions (cognitive lens)
# ──────────────────────────────────────────────────────────────────────────────


def create_decision(conn: sqlite3.Connection, d: DecisionCreate) -> Decision:
    cur = conn.execute(
        "INSERT INTO decisions (situation, options, chosen, reasoning, "
        "expected_outcome, confidence, linked_scenario_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            d.situation,
            json.dumps(d.options),
            d.chosen,
            d.reasoning,
            d.expected_outcome,
            d.confidence,
            d.linked_scenario_id,
        ),
    )
    decision_id = cur.lastrowid

    flags = biases.run_all(d)
    for slug, evidence in flags:
        conn.execute(
            "INSERT INTO bias_flags (decision_id, bias_slug, evidence) VALUES (?, ?, ?)",
            (decision_id, slug, evidence),
        )
    conn.commit()

    # Audit-log every detector run so we can later inspect (by hand or by feeding
    # to Claude Code) what biases the regex rules might be missing. Suggestion
    # from Prof. Pitcher in CSC299 Discord.
    try:
        audit.log_bias_run(
            situation=d.situation,
            options=d.options,
            chosen=d.chosen,
            reasoning=d.reasoning,
            expected_outcome=d.expected_outcome,
            confidence=d.confidence,
            flags_found=flags,
        )
    except OSError:
        # don't let a logging failure break decision creation
        pass

    return get_decision(conn, decision_id)  # type: ignore[return-value]


def list_decisions(conn: sqlite3.Connection, limit: int = 50) -> list[Decision]:
    rows = conn.execute(
        "SELECT id FROM decisions ORDER BY created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    return [get_decision(conn, r["id"]) for r in rows if get_decision(conn, r["id"])]  # type: ignore[misc]


def get_decision(conn: sqlite3.Connection, decision_id: int) -> Decision | None:
    row = conn.execute(
        "SELECT id, created_at, situation, options, chosen, reasoning, "
        "expected_outcome, confidence, linked_scenario_id, actual_outcome, reviewed_at "
        "FROM decisions WHERE id = ?",
        (decision_id,),
    ).fetchone()
    if row is None:
        return None
    flag_rows = conn.execute(
        "SELECT id, bias_slug, evidence FROM bias_flags WHERE decision_id = ?",
        (decision_id,),
    ).fetchall()
    return Decision(
        id=row["id"],
        created_at=_parse_dt(row["created_at"]),
        situation=row["situation"],
        options=json.loads(row["options"]),
        chosen=row["chosen"],
        reasoning=row["reasoning"],
        expected_outcome=row["expected_outcome"],
        confidence=row["confidence"],
        linked_scenario_id=row["linked_scenario_id"],
        actual_outcome=row["actual_outcome"],
        reviewed_at=_parse_dt(row["reviewed_at"]) if row["reviewed_at"] else None,
        biases=[BiasFlag(**dict(f)) for f in flag_rows],
    )


def update_decision(
    conn: sqlite3.Connection, decision_id: int, update: DecisionUpdate
) -> Decision | None:
    if update.actual_outcome is None:
        return get_decision(conn, decision_id)
    conn.execute(
        "UPDATE decisions SET actual_outcome = ?, reviewed_at = ? WHERE id = ?",
        (update.actual_outcome, datetime.utcnow().isoformat(timespec="seconds"), decision_id),
    )
    conn.commit()
    return get_decision(conn, decision_id)


def delete_decision(conn: sqlite3.Connection, decision_id: int) -> bool:
    cur = conn.execute("DELETE FROM decisions WHERE id = ?", (decision_id,))
    conn.commit()
    return cur.rowcount > 0


def _parse_dt(value: str | None) -> datetime:
    if value is None:
        return datetime.utcnow()
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


# ──────────────────────────────────────────────────────────────────────────────
# Stats
# ──────────────────────────────────────────────────────────────────────────────


def get_stats(conn: sqlite3.Connection) -> Stats:
    def one(sql: str) -> int:
        return int(conn.execute(sql).fetchone()[0])

    return Stats(
        domains=one("SELECT COUNT(*) FROM domains"),
        statutes=one("SELECT COUNT(*) FROM statutes"),
        scenarios=one("SELECT COUNT(*) FROM scenarios"),
        decisions=one("SELECT COUNT(*) FROM decisions"),
        bias_flags=one("SELECT COUNT(*) FROM bias_flags"),
    )
