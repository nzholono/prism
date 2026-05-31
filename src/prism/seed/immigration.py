"""Seed data: immigration & international students (Illinois)."""

from __future__ import annotations

import sqlite3

DOMAIN = {
    "slug": "immigration",
    "name": "Immigration / International Students",
    "tier": 2,
    "summary": (
        "F-1 visa rules, OPT, on-campus and off-campus employment, "
        "interactions with ICE specific to immigration status. Critical for "
        "DePaul's large international student population."
    ),
}

STATUTES = [
    {
        "citation": "8 CFR § 214.2(f)",
        "title": "F-1 visa employment rules",
        "summary": (
            "F-1 students may work on-campus up to 20 hours/week during the "
            "academic year and full-time during breaks. Off-campus work "
            "requires specific authorization: CPT (Curricular Practical "
            "Training, tied to a class), OPT (Optional Practical Training, "
            "post-completion), or severe economic hardship authorization."
        ),
        "body_md": (
            "**8 CFR § 214.2(f) — F-1 student employment**\n\n"
            "**On-campus employment:**\n\n"
            "- Authorized as part of your F-1 status — no separate paperwork.\n"
            "- **Up to 20 hours per week** during the academic year.\n"
            "- **Full-time** during official breaks (summer, winter break).\n"
            "- Must be performed on school premises or at an off-campus "
            "location 'educationally affiliated' with the school.\n\n"
            "**CPT (Curricular Practical Training):**\n\n"
            "- For employment that is integral to your curriculum (an "
            "internship for academic credit).\n"
            "- Authorized by your DSO (designated school official) — not USCIS.\n"
            "- **12+ months of full-time CPT will eliminate your OPT eligibility**.\n\n"
            "**OPT (Optional Practical Training):**\n\n"
            "- **12 months** of work authorization after completing your "
            "program (Pre-completion OPT also exists but is uncommon).\n"
            "- **STEM extension:** 24 additional months for qualifying STEM "
            "degree holders — total 36 months.\n"
            "- Apply via Form I-765, with USCIS, typically 90 days before "
            "program completion. **Filing deadlines are strict.**\n"
            "- During OPT you must be employed in a job related to your "
            "field of study.\n"
            "- **Unemployment limit:** 90 days during initial OPT, 150 days "
            "total with STEM extension. Exceeding triggers status loss.\n\n"
            "**Severe economic hardship authorization:** rare, requires "
            "demonstrating unforeseen economic circumstances. Apply through USCIS.\n\n"
            "**Unauthorized employment is a status violation** — can result "
            "in deportation. When in doubt, talk to your DSO before working."
        ),
        "source_url": "https://studyinthestates.dhs.gov/students",
    },
]

SCENARIOS = [
    {
        "slug": "f1-employment-rules",
        "title": "What can I do (and not do) for work on an F-1 visa?",
        "linked_statutes": ["8 CFR § 214.2(f)"],
        "description_md": (
            "You're an international student on F-1 and you want to know "
            "what work you can legally do — on campus, off campus, freelance "
            "gigs, summer jobs, internships, post-graduation. The wrong move "
            "here can cost you your status and your degree."
        ),
        "walkthrough_md": (
            "## Quick reference — what's allowed by default\n\n"
            "**Allowed without extra paperwork:**\n"
            "- On-campus jobs (cafeteria, library, lab, RA position) up to "
            "20 hrs/week during semester, full-time during breaks.\n\n"
            "**Requires authorization first:**\n"
            "- Any off-campus paid work (internship, side hustle, freelance, "
            "tutoring, food delivery, Uber, Instacart, dog-walking apps — yes, "
            "all of those count as employment).\n"
            "- Sale of self-created content (selling art online, monetized "
            "YouTube channels — talk to your DSO).\n\n"
            "**Never allowed:**\n"
            "- Working for a U.S. employer while in F-1 status without "
            "authorization, even unpaid in some cases.\n"
            "- More than 20 hrs/week on-campus during the semester.\n"
            "- Any work after status expiration.\n\n"
            "## What to do\n\n"
            "1. **Talk to your DSO first**, every time. DePaul's "
            "international student office is the gatekeeper for everything "
            "in this area. It's their job — they're a resource, not a threat.\n\n"
            "2. **For paid internships during your program:** apply for **CPT** "
            "with your DSO. The internship must be integral to your degree "
            "(typically required for academic credit or required for the "
            "program). Get the authorization **before starting**.\n\n"
            "3. **For post-graduation work:** apply for **OPT** via Form "
            "I-765, ideally 90 days before your program ends. Don't miss "
            "deadlines — once your program ends without OPT in hand, you "
            "have a 60-day grace period and that's it.\n\n"
            "4. **Track your unemployment days during OPT.** 90 days cap on "
            "initial OPT, 150 total with STEM. Going over triggers status "
            "loss. The SEVP Portal tracks this — make sure it shows your "
            "employer.\n\n"
            "5. **STEM OPT extension** requires:\n"
            "   - Degree in DHS-designated STEM field.\n"
            "   - Employer enrolled in E-Verify.\n"
            "   - Training plan (Form I-983) signed by you and employer.\n"
            "   - Apply before initial OPT ends.\n\n"
            "6. **Side gigs are risky.** Driving for Uber, Instacart deliveries, "
            "freelance projects on Upwork — all count as work. Most are "
            "unauthorized for F-1 unless tied to OPT/CPT with a registered "
            "employer. Don't do them without DSO sign-off.\n\n"
            "7. **Travel during OPT** is allowed but tricky. Have:\n"
            "   - Valid passport (6+ months validity).\n"
            "   - Valid F-1 visa.\n"
            "   - Valid I-20 with travel signature (within 6 months).\n"
            "   - Valid EAD card (OPT authorization).\n"
            "   - Letter from employer confirming employment.\n\n"
            "## If you violated status accidentally\n\n"
            "8. **Don't panic — but talk to an immigration lawyer immediately.** "
            "Status violations don't always end your time here, but how you "
            "respond matters a lot. Options include reinstatement, "
            "departure-and-reentry, or change of status. **Don't try to fix it "
            "yourself.**\n\n"
            "## Resources\n\n"
            "- **DePaul Office of International Student & Scholar Services**: "
            "go.depaul.edu/oiss (or your school's equivalent)\n"
            "- **National Immigrant Justice Center**: (312) 660-1370\n"
            "- **AILA Immigration Lawyer Search**: ailalawyer.com\n"
            "- **USCIS hotline**: (800) 375-5283\n\n"
            "---\n\n"
            "*This is reference material, not legal advice. Immigration law is "
            "complicated and consequential — talk to your DSO and, for serious "
            "questions, an immigration attorney.*"
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
