"""Seed data: mental health rights (Illinois)."""

from __future__ import annotations

import sqlite3

DOMAIN = {
    "slug": "mental-health",
    "name": "Mental Health Rights",
    "tier": 2,
    "summary": (
        "Your rights around mental health treatment in Illinois — the strict "
        "procedural protections before someone can be involuntarily "
        "hospitalized, confidentiality of MH records, when to call 988 vs 911."
    ),
}

STATUTES = [
    {
        "citation": "405 ILCS 5/3-600",
        "title": "Illinois MH&DDC — involuntary admission requires court order",
        "summary": (
            "In Illinois, an adult cannot be involuntarily admitted to a "
            "mental health facility without specific findings: that the "
            "person poses a clear and present danger to self or others, OR is "
            "unable to provide for their basic physical needs. Court hearings, "
            "rights to counsel, and time limits all apply."
        ),
        "body_md": (
            "**405 ILCS 5/3-600 et seq. — Involuntary admission**\n\n"
            "Illinois has unusually strong procedural protections before "
            "anyone can be involuntarily committed.\n\n"
            "**Standard for involuntary admission:** the person must, because "
            "of mental illness:\n\n"
            "1. Be **reasonably expected to engage in conduct placing such "
            "person or another in physical harm**, OR\n"
            "2. Be **unable to provide for their basic physical needs** so as "
            "to guard themselves from serious harm.\n\n"
            "**Your rights when facing involuntary admission:**\n\n"
            "- **A court hearing within 5 business days** of admission.\n"
            "- **An attorney** (court-appointed if you can't afford one).\n"
            "- **An independent psychiatric examination** at your request.\n"
            "- The right to **cross-examine witnesses** at your hearing.\n"
            "- A written **statement of rights** at admission.\n"
            "- The right to **refuse psychotropic medication** in non-emergency "
            "situations (with limited exceptions following a separate court "
            "process).\n\n"
            "**Emergency admission (much shorter — up to 24 hours):**\n\n"
            "- A peace officer, qualified examiner, or doctor can take you "
            "to a facility on a 'petition for emergency admission'.\n"
            "- The facility must examine you within 24 hours.\n"
            "- If they want to continue, they must file a formal petition for "
            "involuntary admission — triggering the full process above."
        ),
        "source_url": "https://www.ilga.gov/legislation/ilcs/ilcs5.asp?ActID=1496",
    },
    {
        "citation": "740 ILCS 110 (MHDDC)",
        "title": "Illinois Mental Health & Developmental Disabilities Confidentiality Act",
        "summary": (
            "Your mental health records and the fact of your treatment are "
            "confidential under Illinois law. Mental health professionals "
            "generally cannot disclose without your written consent, except "
            "in narrow circumstances (court order, mandated reporting, "
            "immediate danger)."
        ),
        "body_md": (
            "**740 ILCS 110 — Mental Health & Developmental Disabilities "
            "Confidentiality Act**\n\n"
            "Stronger than HIPAA in important ways. Covers:\n\n"
            "- All records of mental health treatment.\n"
            "- The **fact** that you received treatment.\n"
            "- Communications between you and a mental health professional.\n\n"
            "**Disclosure requires your written consent**, with limited "
            "exceptions:\n\n"
            "- Court order (high standard — judge must balance competing "
            "interests).\n"
            "- Mandated reporting (child abuse, elder abuse).\n"
            "- Imminent danger to self or others (the 'duty to warn').\n"
            "- Other treating clinicians, with limits.\n\n"
            "**Your rights:**\n\n"
            "- Inspect your own records (with some clinical-judgment limits).\n"
            "- Authorize specific disclosures (revocable).\n"
            "- Refuse to consent to general disclosures.\n"
            "- Sue for damages if records are wrongfully disclosed.\n\n"
            "**Practical impact:**\n\n"
            "- Your employer cannot ask your therapist about your treatment "
            "without your consent.\n"
            "- Your school cannot share that you're seeing a counselor "
            "without your consent.\n"
            "- Even your spouse or parents have no right to your MH records "
            "(if you're an adult)."
        ),
        "source_url": "https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2043",
    },
]

SCENARIOS = [
    {
        "slug": "988-vs-911",
        "title": "Someone is in a mental health crisis — should I call 988 or 911?",
        "linked_statutes": ["405 ILCS 5/3-600"],
        "description_md": (
            "You or someone near you is in a mental health crisis. The "
            "instinct is to call 911. But for many crises, **988 (the "
            "Suicide & Crisis Lifeline) is a better first call** — it sends "
            "trained mental health responders instead of armed police, "
            "which is safer and often more effective."
        ),
        "walkthrough_md": (
            "## Quick decision\n\n"
            "**Call 988 when:**\n"
            "- The person is in emotional distress, suicidal, or having a "
            "mental health crisis.\n"
            "- There is no immediate physical danger to anyone.\n"
            "- The person isn't actively armed or harming someone right now.\n"
            "- You want to talk to a trained crisis counselor first.\n\n"
            "**Call 911 when:**\n"
            "- Someone is actively trying to harm themselves or others **right "
            "now**.\n"
            "- There's an active weapon or violence.\n"
            "- You need an ambulance because of injury.\n"
            "- It's a medical emergency in addition to a mental health one.\n\n"
            "## What happens when you call 988\n\n"
            "1. You're connected to a trained crisis counselor — usually "
            "within 30 seconds.\n"
            "2. They listen, ask questions, work through the situation with "
            "you on the phone (or text — text 988 also works).\n"
            "3. **Most calls are resolved by phone** — fewer than 2% result "
            "in any dispatch.\n"
            "4. If dispatch is needed, **Mobile Crisis Response Teams** "
            "(available in much of Illinois) send mental health professionals "
            "— not armed police — to provide on-scene support.\n"
            "5. Hospital transport happens only when truly necessary.\n\n"
            "## What happens when you call 911 for mental health crisis\n\n"
            "1. Dispatch usually sends police, sometimes with EMTs.\n"
            "2. Police are not trained mental health responders. Their "
            "training is for criminal/violence response.\n"
            "3. Officers may take the person to a hospital under a 'petition "
            "for emergency admission' — which triggers Illinois's involuntary "
            "commitment process (see 405 ILCS 5/3-600).\n"
            "4. People in mental health crisis are **disproportionately likely "
            "to be hurt or killed during police encounters** — particularly "
            "people of color.\n\n"
            "## In Chicago specifically\n\n"
            "**CARE (Crisis Assistance Response and Engagement)** — Chicago's "
            "mobile crisis response. When you call 988 from a Chicago number "
            "during business hours and most evening hours, CARE may be "
            "dispatched. CARE responders are mental health clinicians and "
            "paramedics, no police.\n\n"
            "If you're calling for someone else and want to specifically "
            "request a mobile crisis team rather than police, say: *'This is "
            "a mental health crisis. Please send Mobile Crisis Response if "
            "available.'*\n\n"
            "## After the crisis\n\n"
            "5. If the person was hospitalized involuntarily, they have "
            "**strong rights**: court hearing within 5 business days, "
            "appointed counsel, independent evaluation, right to refuse "
            "non-emergency medication. See the involuntary-admission statute "
            "above.\n\n"
            "6. The **mental health records are confidential under Illinois "
            "law** (740 ILCS 110). Employers, schools, and family members do "
            "not automatically get to know.\n\n"
            "## Resources\n\n"
            "- **988** — Suicide & Crisis Lifeline (call or text)\n"
            "- **NAMI Chicago Helpline**: (833) NAMI-CHI\n"
            "- **Illinois CARES Line**: (800) 345-9049\n"
            "- **Trans Lifeline**: (877) 565-8860\n"
            "- **Trevor Project** (LGBTQ+ youth): (866) 488-7386\n\n"
            "---\n\n"
            "*This is reference material, not medical or legal advice.*"
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
