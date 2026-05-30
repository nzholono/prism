"""Scaffolded Tier-2 domains: structure + 1 sample scenario each.

These prove the architecture is extensible — designed to be grown via the
`add-scenario` skill rather than hand-coded all at once.
"""

from __future__ import annotations

import sqlite3

DOMAINS = [
    {
        "slug": "campus",
        "name": "Campus / Student Rights",
        "tier": 2,
        "summary": (
            "Title IX, FERPA, ADA accommodations, academic appeals. Specifically "
            "relevant to DePaul and other Illinois colleges."
        ),
        "scaffold_statutes": [
            {
                "citation": "20 U.S.C. § 1232g (FERPA)",
                "title": "Family Educational Rights and Privacy Act",
                "summary": (
                    "Your school cannot share your education records (grades, "
                    "transcripts, disciplinary records) with most third parties "
                    "without your written consent."
                ),
                "body_md": "Add full FERPA text via `add-scenario` skill.",
                "source_url": "https://www2.ed.gov/policy/gen/guid/fpco/ferpa/index.html",
            },
        ],
        "scaffold_scenarios": [
            {
                "slug": "grade-dispute",
                "title": "I want to dispute a grade I think is unfair",
                "linked_citations": [],
                "description_md": "Most colleges have a formal academic-appeal process.",
                "walkthrough_md": "Scaffolded — extend via `add-scenario` skill.",
                "template_md": None,
            },
        ],
    },
    {
        "slug": "healthcare",
        "name": "Healthcare & Medical Bills",
        "tier": 2,
        "summary": (
            "Hospital Uninsured Patient Discount Act, surprise billing, mental "
            "health parity, EMTALA emergency-care rights."
        ),
        "scaffold_statutes": [
            {
                "citation": "210 ILCS 89/10",
                "title": "Illinois Hospital Uninsured Patient Discount Act",
                "summary": (
                    "Hospitals must offer discounts to uninsured Illinois "
                    "patients whose income is at or below certain thresholds."
                ),
                "body_md": "Add full statute via `add-scenario` skill.",
                "source_url": "https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2988",
            },
        ],
        "scaffold_scenarios": [
            {
                "slug": "shocking-medical-bill",
                "title": "I received a shockingly high medical bill",
                "linked_citations": ["210 ILCS 89/10"],
                "description_md": "Most hospital bills are negotiable.",
                "walkthrough_md": "Scaffolded — extend via `add-scenario` skill.",
                "template_md": None,
            },
        ],
    },
    {
        "slug": "immigration",
        "name": "Immigration / International Students",
        "tier": 2,
        "summary": (
            "F-1 visa rules, OPT, DACA, ICE encounters specific to status. "
            "Particularly relevant to DePaul's international student population."
        ),
        "scaffold_statutes": [],
        "scaffold_scenarios": [
            {
                "slug": "f1-employment-rules",
                "title": "What can I do with an F-1 visa during my studies?",
                "linked_citations": [],
                "description_md": (
                    "F-1 students have limited on-campus employment rights and "
                    "specific OPT/CPT options."
                ),
                "walkthrough_md": "Scaffolded — extend via `add-scenario` skill.",
                "template_md": None,
            },
        ],
    },
    {
        "slug": "mental-health",
        "name": "Mental Health Rights",
        "tier": 2,
        "summary": (
            "Involuntary commitment law, mental health confidentiality, "
            "988 vs 911, your right to refuse treatment."
        ),
        "scaffold_statutes": [
            {
                "citation": "405 ILCS 5/3-600",
                "title": "Illinois Mental Health & Developmental Disabilities Code — involuntary admission",
                "summary": (
                    "Strict procedural protections before someone can be "
                    "involuntarily hospitalized in Illinois."
                ),
                "body_md": "Add full statute via `add-scenario` skill.",
                "source_url": "https://www.ilga.gov/legislation/ilcs/ilcs5.asp?ActID=1496",
            },
        ],
        "scaffold_scenarios": [
            {
                "slug": "988-vs-911",
                "title": "When should I call 988 vs 911 in a mental health crisis?",
                "linked_citations": [],
                "description_md": "988 is the mental health crisis line — different response than police.",
                "walkthrough_md": "Scaffolded — extend via `add-scenario` skill.",
                "template_md": None,
            },
        ],
    },
    {
        "slug": "traffic",
        "name": "Traffic & Vehicle",
        "tier": 2,
        "summary": (
            "Tickets, accidents, DUI basics, booting and towing in Chicago."
        ),
        "scaffold_statutes": [],
        "scaffold_scenarios": [
            {
                "slug": "parking-ticket-dispute",
                "title": "I want to fight a parking ticket in Chicago",
                "linked_citations": [],
                "description_md": "Chicago tickets can be contested via the Department of Administrative Hearings.",
                "walkthrough_md": "Scaffolded — extend via `add-scenario` skill.",
                "template_md": None,
            },
        ],
    },
]


def seed(conn: sqlite3.Connection) -> None:
    for d in DOMAINS:
        conn.execute(
            "INSERT OR IGNORE INTO domains (slug, name, tier, summary) VALUES (?, ?, ?, ?)",
            (d["slug"], d["name"], d["tier"], d["summary"]),
        )
        domain_id = conn.execute(
            "SELECT id FROM domains WHERE slug = ?", (d["slug"],)
        ).fetchone()["id"]

        cite_to_id: dict[str, int] = {}
        for s in d["scaffold_statutes"]:
            existing = conn.execute(
                "SELECT id FROM statutes WHERE citation = ? AND domain_id = ?",
                (s["citation"], domain_id),
            ).fetchone()
            if existing:
                cite_to_id[s["citation"]] = existing["id"]
                continue
            cur = conn.execute(
                "INSERT INTO statutes (domain_id, citation, title, summary, body_md, source_url) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    domain_id,
                    s["citation"],
                    s["title"],
                    s["summary"],
                    s["body_md"],
                    s["source_url"],
                ),
            )
            cite_to_id[s["citation"]] = cur.lastrowid

        for sc in d["scaffold_scenarios"]:
            existing = conn.execute(
                "SELECT id FROM scenarios WHERE slug = ?", (sc["slug"],)
            ).fetchone()
            if existing:
                scenario_id = existing["id"]
            else:
                cur = conn.execute(
                    "INSERT INTO scenarios (domain_id, slug, title, description_md, "
                    "walkthrough_md, template_md) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        domain_id,
                        sc["slug"],
                        sc["title"],
                        sc["description_md"],
                        sc["walkthrough_md"],
                        sc["template_md"],
                    ),
                )
                scenario_id = cur.lastrowid
            for citation in sc["linked_citations"]:
                if (sid := cite_to_id.get(citation)) is not None:
                    conn.execute(
                        "INSERT OR IGNORE INTO scenario_statutes (scenario_id, statute_id) VALUES (?, ?)",
                        (scenario_id, sid),
                    )
    conn.commit()
