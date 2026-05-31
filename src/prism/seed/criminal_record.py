"""Seed data: criminal record / expungement (Illinois).

A surprising number of Illinois residents — including DePaul students —
have arrests or convictions they don't realize they can clear. Illinois has
some of the broader expungement and sealing laws in the country.
"""

from __future__ import annotations

import sqlite3

DOMAIN = {
    "slug": "criminal-record",
    "name": "Criminal Records & Expungement",
    "tier": 2,
    "summary": (
        "Illinois lets many people clear arrests and convictions from their "
        "record through expungement or sealing — including arrests that "
        "didn't result in conviction, juvenile records, and many Class 3 "
        "and 4 felonies. The process is doable without a lawyer."
    ),
}

STATUTES = [
    {
        "citation": "20 ILCS 2630/5.2",
        "title": "Illinois Criminal Identification Act — expungement & sealing",
        "summary": (
            "Illinois law allows expungement (records physically destroyed or "
            "returned) for most arrests not resulting in conviction, and "
            "sealing (records hidden from most employers and the public) for "
            "many convictions including most Class 3 and 4 felonies and most "
            "misdemeanors. The 2017 Cannabis Regulation and Tax Act added "
            "automatic expungement for many cannabis-related records."
        ),
        "body_md": (
            "**20 ILCS 2630/5.2 — Illinois expungement and sealing**\n\n"
            "**Expungement** (full erasure) is available for:\n\n"
            "- **Arrests that did not lead to conviction** — dismissed, "
            "acquitted, no charges filed, supervision successfully completed "
            "(for certain misdemeanors).\n"
            "- **Juvenile records** in most cases.\n"
            "- **Many cannabis-related convictions** under the 2019 Cannabis "
            "Regulation and Tax Act — some processed automatically by the "
            "state.\n\n"
            "**Sealing** (records remain but hidden from public and most "
            "employers) is available for:\n\n"
            "- Most **misdemeanors** after a waiting period (typically 3 years "
            "after sentence completion).\n"
            "- Most **Class 3 and Class 4 felonies** after a waiting period.\n"
            "- **NOT available** for:\n"
            "  - Most violent felonies.\n"
            "  - Sex offenses requiring registration.\n"
            "  - DUI convictions.\n"
            "  - Domestic violence convictions.\n\n"
            "**Process:**\n\n"
            "1. Get your **RAP sheet** (record) from the Illinois State Police.\n"
            "2. Determine eligibility (this is the hard part — eligibility "
            "rules are intricate).\n"
            "3. File a petition in the county where the case was heard.\n"
            "4. Serve the State's Attorney, who has 60 days to object.\n"
            "5. Court hearing if there's objection or if the judge wants one.\n"
            "6. If granted, the order is sent to law enforcement agencies.\n\n"
            "**Cost:** filing fees vary by county (often $120–$200, waivable "
            "based on income).\n\n"
            "**Why bother:** sealed/expunged records don't show up on most "
            "background checks. Major impact on jobs, housing, professional "
            "licenses, college admissions."
        ),
        "source_url": "https://www.ilga.gov/legislation/ilcs/documents/002026300K5.2.htm",
    },
]

SCENARIOS = [
    {
        "slug": "expunge-old-arrest",
        "title": "I have an old arrest or conviction I want off my record",
        "linked_statutes": ["20 ILCS 2630/5.2"],
        "description_md": (
            "An arrest from years ago keeps showing up on background checks. "
            "Or a conviction is blocking you from a job, a license, an "
            "apartment. Illinois has unusually broad expungement and sealing "
            "laws — many people don't realize they're eligible."
        ),
        "walkthrough_md": (
            "## What to do\n\n"
            "1. **Get your RAP sheet first.** Visit the Illinois State Police "
            "website (isp.illinois.gov) or call (815) 740-5160. There's a "
            "small fee. You need this to know exactly what's on your record.\n\n"
            "2. **Figure out your eligibility.** This is the hardest step. "
            "General rules:\n"
            "   - **Arrests that didn't result in conviction**: expungement "
            "is usually available immediately.\n"
            "   - **Court supervision** (a sentence that isn't a conviction "
            "if you finish it successfully): expungement is often available "
            "5 years after termination for most offenses, 2 years for some "
            "minor ones.\n"
            "   - **Misdemeanor conviction**: sealing usually available 3 "
            "years after sentence completion.\n"
            "   - **Class 3 or 4 felony conviction**: sealing usually "
            "available 3 years after sentence completion if eligible.\n"
            "   - **Cannabis convictions**: many automatically expunged "
            "under the 2019 law. Check first; you may already be clean.\n\n"
            "3. **Get free help with eligibility analysis.** This step is "
            "where most people give up. Don't. These organizations help "
            "FREE:\n"
            "   - **Cabrini Green Legal Aid expungement clinic** (Chicago): "
            "(312) 332-5537. Walk-in clinics most weeks.\n"
            "   - **Illinois Legal Aid Online expungement guide**: "
            "illinoislegalaid.org/expungement (interactive tool that helps "
            "determine eligibility).\n"
            "   - **Chicago Legal Clinic**: clclaw.org.\n"
            "   - **Local public defender's office** — some run expungement "
            "clinics.\n\n"
            "4. **File the petition.** The clinic will help you complete "
            "the right form for your situation. Filed in the county where "
            "your case was heard.\n\n"
            "5. **Pay or waive the filing fee.** $120–$200 typically. "
            "Income-based waivers available (fill out a fee waiver "
            "application with the petition).\n\n"
            "6. **Serve the State's Attorney**, who has 60 days to object. "
            "Most don't object to clearly-eligible petitions.\n\n"
            "7. **Court hearing**, if needed. The judge reviews. You may "
            "or may not need to be present (depends on county).\n\n"
            "8. **If granted, your records are sealed or expunged.** Make "
            "sure to:\n"
            "   - Get a copy of the order.\n"
            "   - Wait 6 months, then pull your RAP sheet again to "
            "confirm the records were actually removed by all agencies.\n"
            "   - Update any background-check services (some private ones "
            "keep old records; you may need to dispute with each).\n\n"
            "## Common myths\n\n"
            "- ❌ 'Old records fall off automatically after 7 years.' False. "
            "Criminal records last forever unless you expunge or seal them.\n"
            "- ❌ 'I have to pay a lawyer thousands of dollars.' False. "
            "Free legal aid handles most of these.\n"
            "- ❌ 'A conviction means it can never be cleared.' False. Many "
            "convictions can be sealed in Illinois.\n"
            "- ❌ 'If I never went to court, there's no record.' False. The "
            "arrest itself can show up. Always pull your RAP sheet to know.\n\n"
            "## Free help\n\n"
            "- **Cabrini Green Legal Aid expungement clinic**: (312) 332-5537\n"
            "- **Illinois Legal Aid Online**: illinoislegalaid.org/expungement\n"
            "- **CARPLS**: (312) 738-9200\n"
            "- **State Appellate Defender (juvenile records)**: "
            "(312) 814-5472\n\n"
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
