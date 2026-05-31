"""Seed data: voter rights in Illinois.

Illinois has same-day registration, no-excuse vote-by-mail, automatic
voter registration, and one of the broader voter-rights frameworks in
the country. Most voter problems come from not knowing what's allowed.
"""

from __future__ import annotations

import sqlite3

DOMAIN = {
    "slug": "voter",
    "name": "Voter Rights",
    "tier": 2,
    "summary": (
        "Voting in Illinois — registration, ID rules, what to do if your "
        "ballot is challenged or you're turned away at the polls. Illinois "
        "has unusually voter-friendly laws: same-day registration, "
        "no-excuse mail-in voting, broad early voting."
    ),
}

STATUTES = [
    {
        "citation": "10 ILCS 5/1A-16 (election code)",
        "title": "Illinois Election Code — registration, ID, same-day registration",
        "summary": (
            "Illinois allows same-day voter registration at every early "
            "voting site and every Election Day polling place. ID is "
            "generally NOT required to vote if you're already registered — "
            "Illinois does not have a strict photo-ID requirement. Mail-in "
            "and early voting are available without excuse."
        ),
        "body_md": (
            "**10 ILCS 5/1A-16 et seq. — Illinois Election Code**\n\n"
            "**Registration:**\n\n"
            "- **Online**: ova.elections.il.gov (need Illinois driver's "
            "license or state ID).\n"
            "- **By mail**: Form NVRA, no fee.\n"
            "- **Automatic Voter Registration**: when you transact at the "
            "DMV (or other state agencies), you're registered/updated "
            "automatically unless you opt out.\n"
            "- **Same-day registration**: at any early voting site or at "
            "your polling place on Election Day. Bring two pieces of ID "
            "(one must show current address — utility bill, lease, "
            "student ID).\n\n"
            "**ID at the polls (already registered):**\n\n"
            "- **No ID required** in most cases. If you're already registered, "
            "you sign and vote.\n"
            "- Election judge **may** request ID if: (a) you registered by "
            "mail without ID and this is your first time voting, or (b) "
            "your eligibility is challenged.\n"
            "- Accepted ID: driver's license, state ID, utility bill, "
            "bank statement, paycheck, student ID, lease — many options.\n\n"
            "**Provisional ballot:**\n\n"
            "If election judges question your eligibility, you have the "
            "right to a **provisional ballot**. Cast it. Counties verify "
            "later. **Don't leave without voting.**\n\n"
            "**Vote by mail:**\n\n"
            "- **No excuse required.** Any registered voter can request a "
            "mail ballot.\n"
            "- Apply online at your county election authority's site.\n"
            "- Return by mail, drop box, or in person at the election office.\n\n"
            "**Early voting:** every Illinois county has early voting "
            "centers open weeks before Election Day.\n\n"
            "**Election Day work leave:** Illinois employers must give "
            "you up to 2 hours of paid leave to vote on Election Day if "
            "your work shift doesn't leave 2 consecutive non-work hours "
            "when the polls are open."
        ),
        "source_url": "https://www.elections.il.gov",
    },
]

SCENARIOS = [
    {
        "slug": "turned-away-at-polls",
        "title": "I was turned away at my polling place",
        "linked_statutes": ["10 ILCS 5/1A-16 (election code)"],
        "description_md": (
            "You showed up to vote and were told you're not on the rolls, "
            "you're at the wrong location, you don't have the right ID, or "
            "someone challenged your right to vote. **Do not leave without "
            "casting a ballot.** Illinois law gives you several ways to "
            "vote even when something is wrong."
        ),
        "walkthrough_md": (
            "## In the moment\n\n"
            "1. **Stay calm. Do not leave.** If you leave without voting, "
            "you've lost the chance for this election.\n\n"
            "2. **'I'd like to register and vote today, please.'** Illinois "
            "allows **same-day registration** at every polling place. Bring "
            "two pieces of ID — one showing current address (utility bill, "
            "lease, student ID, bank statement). The polling place is "
            "required to accommodate same-day registration.\n\n"
            "3. **If they say you're at the wrong location**, ask them to "
            "look up where you should be. Many Illinois jurisdictions allow "
            "you to vote a **provisional ballot** even at the wrong location, "
            "but it's better to drive to the right one if there's time.\n\n"
            "4. **If they challenge your eligibility**, you have the right "
            "to a **provisional ballot** under Illinois law. Cast it. The "
            "county will verify and count it later if eligible.\n\n"
            "5. **If they refuse a provisional ballot**, call the **Election "
            "Protection hotline immediately: 1-866-OUR-VOTE (1-866-687-8683)**. "
            "Volunteer attorneys are standing by, and they will intervene.\n\n"
            "6. **Other live numbers to call:**\n"
            "   - **Spanish**: 1-888-VE-Y-VOTA (1-888-839-8682)\n"
            "   - **Asian language hotline**: 1-888-API-VOTE (1-888-274-8683)\n"
            "   - **Arabic**: 1-844-YALLA-US (1-844-925-5287)\n\n"
            "7. **Document.** Write down: polling place address, time, "
            "name(s) of election judge(s) who turned you away, exactly what "
            "was said.\n\n"
            "## After the election\n\n"
            "8. **File a complaint** with the Illinois State Board of "
            "Elections (elections.il.gov) and the Illinois Attorney General "
            "if you believe rules were violated. Patterns of voter "
            "suppression are taken seriously.\n\n"
            "## To avoid being turned away\n\n"
            "- **Check your registration** at ova.elections.il.gov "
            "before Election Day.\n"
            "- **Vote early** — fewer lines, more time to resolve issues.\n"
            "- **Vote by mail** — apply by mail or online, no excuse needed.\n\n"
            "## Free help\n\n"
            "- **Election Protection hotline**: 1-866-OUR-VOTE\n"
            "- **Illinois State Board of Elections**: (217) 782-4141 or "
            "elections.il.gov\n"
            "- **ACLU of Illinois**: (312) 201-9740\n"
            "- **League of Women Voters of Illinois**: lwvil.org\n\n"
            "---\n\n"
            "*This is reference material, not legal advice.*"
        ),
        "template_md": None,
    },
]


def seed(conn: sqlite3.Connection) -> None:
    conn.execute(
        "INSERT OR IGNORE INTO domains (slug, name, tier, summary) VALUES (?, ?, ?, ?)",
        (DOMAIN["slug"], DOMAIN["name"], DOMAIN["tier"], DOMAIN["summary"]),
    )
    domain_id = conn.execute(
        "SELECT id FROM domains WHERE slug = ?", (DOMAIN["slug"],)
    ).fetchone()["id"]

    statute_ids: dict[str, int] = {}
    for s in STATUTES:
        existing = conn.execute(
            "SELECT id FROM statutes WHERE citation = ? AND domain_id = ?",
            (s["citation"], domain_id),
        ).fetchone()
        if existing:
            statute_ids[s["citation"]] = existing["id"]
            continue
        cur = conn.execute(
            "INSERT INTO statutes (domain_id, citation, title, summary, body_md, source_url) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (domain_id, s["citation"], s["title"], s["summary"], s["body_md"], s["source_url"]),
        )
        statute_ids[s["citation"]] = cur.lastrowid

    for sc in SCENARIOS:
        existing = conn.execute("SELECT id FROM scenarios WHERE slug = ?", (sc["slug"],)).fetchone()
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
        for citation in sc["linked_statutes"]:
            sid = statute_ids.get(citation)
            if sid:
                conn.execute(
                    "INSERT OR IGNORE INTO scenario_statutes (scenario_id, statute_id) VALUES (?, ?)",
                    (scenario_id, sid),
                )
    conn.commit()
