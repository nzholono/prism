"""Seed data: family law basics in Illinois.

Focused on the situations most common to DePaul students: orders of
protection (domestic violence, stalking, sexual abuse), emancipation, and
the basics of how custody/divorce work in Illinois.
"""

from __future__ import annotations

import sqlite3

DOMAIN = {
    "slug": "family",
    "name": "Family Law Basics",
    "tier": 2,
    "summary": (
        "Orders of protection (domestic violence, stalking, sexual abuse), "
        "emancipation of minors, and the basics of divorce and custody in "
        "Illinois. Most of these processes are doable without a lawyer, "
        "with free help available."
    ),
}

STATUTES = [
    {
        "citation": "750 ILCS 60 (IDVA)",
        "title": "Illinois Domestic Violence Act — orders of protection",
        "summary": (
            "Illinois lets you petition for an emergency order of protection "
            "against a family member, household member, or dating partner "
            "in 24 hours or less, with a court hearing the same day in many "
            "Illinois counties. No filing fee. Cover yourself, your children, "
            "and your address from disclosure."
        ),
        "body_md": (
            "**750 ILCS 60 — Illinois Domestic Violence Act**\n\n"
            "**Who can petition:** anyone who has been abused by a:\n\n"
            "- Family or household member (current/former spouse, parent, "
            "child, sibling, roommate, person who shares or shared a home).\n"
            "- Current or former dating partner.\n"
            "- Person you have a child with.\n\n"
            "**What counts as abuse:**\n\n"
            "- Physical abuse (hitting, restraining, sexual assault).\n"
            "- Harassment (repeated unwanted contact).\n"
            "- Intimidation.\n"
            "- Interference with personal liberty.\n"
            "- Willful deprivation.\n\n"
            "**Three types of orders:**\n\n"
            "1. **Emergency Order of Protection (EOP)** — issued ex parte "
            "(without the other party present) on the same day you file. "
            "Lasts 14–21 days.\n"
            "2. **Interim Order** — issued after a brief hearing if the "
            "respondent was served but the full hearing is delayed.\n"
            "3. **Plenary Order** — full hearing with both sides. Can last "
            "up to 2 years and be renewed.\n\n"
            "**An order of protection can:**\n\n"
            "- Prohibit further abuse or contact.\n"
            "- Order the abuser to stay away from you, your home, your "
            "workplace, your school, your children's school.\n"
            "- Give you exclusive possession of the shared home.\n"
            "- Award temporary custody of children.\n"
            "- Order surrender of firearms.\n"
            "- Prohibit publishing your address.\n\n"
            "**No filing fee.** Cook County has dedicated Domestic Violence "
            "Court at 555 W. Harrison; suburban courts have similar processes.\n\n"
            "**Violating an order of protection is a criminal offense** — "
            "the abuser faces immediate arrest.\n\n"
            "**Stalking** and **civil no-contact** orders are available "
            "under separate but similar statutes (740 ILCS 21 and 740 ILCS 22) "
            "when the relationship doesn't qualify under IDVA."
        ),
        "source_url": "https://www.ilga.gov/legislation/ilcs/ilcs5.asp?ActID=2100",
    },
    {
        "citation": "750 ILCS 30 (Emancipation of Minors Act)",
        "title": "Illinois Emancipation of Mature Minors Act",
        "summary": (
            "Illinois minors **16 or 17 years old** can petition the court "
            "for partial or complete emancipation if they can demonstrate "
            "they're mature, can manage their own affairs, and have a stable "
            "source of income. Emancipation lets a minor enter contracts, "
            "consent to medical care, sue and be sued, and decide where to live."
        ),
        "body_md": (
            "**750 ILCS 30 — Emancipation of Mature Minors Act**\n\n"
            "**Eligibility:** minors **16 or 17** years old who:\n\n"
            "- Are Illinois residents.\n"
            "- Are mature enough to handle their own affairs.\n"
            "- Can support themselves with a stable, lawful income.\n"
            "- Are seeking partial or complete emancipation for a legitimate "
            "reason.\n\n"
            "**Process:**\n\n"
            "1. **File a petition** in the circuit court of the county where "
            "you live.\n"
            "2. **Notify parents/guardians** (with limited exceptions for "
            "abuse situations — the court can excuse notice).\n"
            "3. **Attend the hearing.** The judge evaluates maturity, "
            "self-sufficiency, and the reason for the request. A guardian "
            "ad litem may be appointed.\n"
            "4. **If granted**, the order specifies whether emancipation "
            "is **partial** (specific rights, like the right to consent to "
            "medical care) or **complete** (all rights of adulthood).\n\n"
            "**Effects of complete emancipation:**\n\n"
            "- Right to enter contracts.\n"
            "- Right to consent to medical care.\n"
            "- Right to live where you choose.\n"
            "- Right to sue and be sued.\n"
            "- Right to keep your own earnings.\n"
            "- Parents are released from support obligations.\n\n"
            "**Free legal help is essential** — emancipation petitions are "
            "complex and the standard for granting them is strict."
        ),
        "source_url": "https://www.ilga.gov/legislation/ilcs/ilcs5.asp?ActID=2098",
    },
]

SCENARIOS = [
    {
        "slug": "get-order-of-protection",
        "title": "I need an order of protection from a partner or family member",
        "linked_statutes": ["750 ILCS 60 (IDVA)"],
        "description_md": (
            "Someone who is — or was — in your life is abusing you. A "
            "partner, ex, family member, roommate. You can get an "
            "**Emergency Order of Protection** in Illinois in 24 hours or "
            "less, free, without a lawyer. The hardest part is just walking "
            "into the courthouse the first time."
        ),
        "walkthrough_md": (
            "## If you're in danger right now\n\n"
            "**Call 911**, or get to a safe location and call the 24-hour "
            "Illinois Domestic Violence Helpline: **1-877-863-6338**.\n\n"
            "## Getting an Emergency Order of Protection (EOP)\n\n"
            "1. **Go to the courthouse with jurisdiction.**\n"
            "   - **Chicago / Cook County**: Domestic Violence Courthouse at "
            "**555 W. Harrison St.** Open daily including weekends and "
            "holidays.\n"
            "   - **Suburban Cook County**: branch courthouses — call (312) "
            "325-9000 for the nearest.\n"
            "   - **Other Illinois counties**: circuit court clerk's office.\n\n"
            "2. **Walk in. You don't need an appointment.** Tell the clerk "
            "you want an Emergency Order of Protection. There is **no "
            "filing fee** and you don't need ID.\n\n"
            "3. **Free advocates are at the courthouse.** Ask for a domestic "
            "violence advocate before you fill out paperwork. They are "
            "trained and free. In Chicago: **Connections for Abused Women "
            "and their Children (CAWC)** has advocates onsite at 555 W. "
            "Harrison.\n\n"
            "4. **Fill out the Petition.** The advocate will help. You will "
            "describe:\n"
            "   - What happened (dates, what was said/done, injuries).\n"
            "   - The other person's address (for service).\n"
            "   - Specific protections you want (no contact, stay-away, "
            "exclusive home possession, child custody, firearm surrender).\n\n"
            "5. **Same-day hearing.** A judge reviews your petition the same "
            "day (sometimes within hours). If you show **good cause** (any "
            "credible threat or pattern of abuse), the judge issues an "
            "Emergency Order valid for 14-21 days.\n\n"
            "6. **The sheriff serves the order** on the other person at "
            "their home or work.\n\n"
            "7. **Plenary hearing within 14-21 days.** Both sides appear. If "
            "you prove the case by a preponderance of evidence, you get a "
            "**Plenary Order of Protection** lasting up to 2 years, "
            "renewable.\n\n"
            "## What to bring (helpful but not required)\n\n"
            "- Photo ID (helpful, not required).\n"
            "- Photos of injuries or damage.\n"
            "- Threatening texts / voicemails / emails (printed).\n"
            "- Names and phone numbers of witnesses.\n"
            "- Police reports if any.\n"
            "- Medical records if any.\n\n"
            "## Confidential address program\n\n"
            "The Illinois **Address Confidentiality Program** lets domestic "
            "violence survivors use a state-supplied substitute address on "
            "all public records (driver's license, voter rolls, school "
            "records). illinoisattorneygeneral.gov.\n\n"
            "## Free help\n\n"
            "- **Illinois Domestic Violence Helpline (24/7)**: 1-877-863-6338\n"
            "- **CAWC (Chicago)**: cawc.org, (773) 278-4566\n"
            "- **Apna Ghar** (South Asian focus, Chicago): (773) 334-4663\n"
            "- **Mujeres Latinas en Acción** (Spanish-speaking): "
            "(312) 738-5358\n"
            "- **ICAVI legal advocacy**: (217) 753-4117\n\n"
            "---\n\n"
            "*This is reference material, not legal advice. The advocates at "
            "the courthouse are free and know the process — use them.*"
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
