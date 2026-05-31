"""Seed data: LGBTQ+ rights in Illinois.

Illinois has broader protections than federal law for LGBTQ+ residents — the
Illinois Human Rights Act explicitly covers sexual orientation and gender
identity. This module focuses on practical issues: discrimination, name and
gender marker changes, healthcare access.
"""

from __future__ import annotations

import sqlite3

DOMAIN = {
    "slug": "lgbtq",
    "name": "LGBTQ+ Rights",
    "tier": 2,
    "summary": (
        "Illinois has explicit and unusually strong legal protections for "
        "LGBTQ+ residents — the Human Rights Act covers sexual orientation "
        "and gender identity in employment, housing, public accommodations, "
        "and credit. This module covers discrimination, legal name and "
        "gender marker change, healthcare access."
    ),
}

STATUTES = [
    {
        "citation": "775 ILCS 5/1-103 (sexual orientation & gender identity)",
        "title": "Illinois Human Rights Act — LGBTQ+ protections",
        "summary": (
            "Since 2005, Illinois has explicitly forbidden discrimination "
            "based on sexual orientation and gender identity in employment, "
            "housing, public accommodations, credit, and access to financial "
            "services. Coverage applies to employers of all sizes (federal "
            "law has size thresholds)."
        ),
        "body_md": (
            "**775 ILCS 5/1-103(O-1) and 5/1-103(Q)**\n\n"
            "Illinois defines 'sexual orientation' broadly: actual or "
            "perceived heterosexuality, homosexuality, bisexuality, or "
            "gender-related identity, including transgender status.\n\n"
            "**Covered areas:**\n\n"
            "- **Employment** — hiring, firing, promotion, pay, conditions. "
            "Applies to **all** Illinois employers regardless of size "
            "(federal Title VII applies only to employers with 15+).\n"
            "- **Housing** — sale, rental, financing, terms of housing.\n"
            "- **Public accommodations** — restaurants, stores, hotels, "
            "government services.\n"
            "- **Credit & financial services** — banks, lenders.\n"
            "- **Education** — schools that receive state funding.\n\n"
            "**Where to file:** Illinois Department of Human Rights (IDHR). "
            "Filing deadline: **300 days** from the discriminatory act.\n\n"
            "**Remedies:** back pay, reinstatement, front pay, emotional "
            "distress damages, attorney's fees, civil penalties.\n\n"
            "**Federal protections also exist** but are narrower: Title VII "
            "of the Civil Rights Act (after the Supreme Court's 2020 "
            "*Bostock v. Clayton County* decision), the federal Fair Housing "
            "Act, and the Affordable Care Act's Section 1557. File with the "
            "EEOC (employment) or HUD (housing). Illinois IDHR usually "
            "dual-files with the EEOC automatically."
        ),
        "source_url": "https://www2.illinois.gov/dhr/Pages/default.aspx",
    },
    {
        "citation": "750 ILCS 35 / 410 ILCS 535/17 (name & gender change)",
        "title": "Illinois name change & corrected birth certificate",
        "summary": (
            "Adults in Illinois can change their legal name by petition in "
            "circuit court (typically a short hearing). Updating the gender "
            "marker on an Illinois birth certificate no longer requires "
            "surgery — only a signed declaration from a licensed healthcare "
            "provider attesting to gender identity."
        ),
        "body_md": (
            "**Legal name change (750 ILCS 35)**\n\n"
            "1. File a petition in the circuit court of the county where you "
            "live (in Cook County, the Daley Center, Domestic Relations).\n"
            "2. Filing fee around $385 (fee waivers available).\n"
            "3. Publish notice in a newspaper for 3 weeks (Illinois "
            "**waives publication for safety reasons** if you state you "
            "fear discrimination or violence — file a motion to seal).\n"
            "4. Court hearing (often less than 5 minutes).\n"
            "5. Certified copy of order — use to update everything else.\n\n"
            "**Gender marker on Illinois birth certificate (410 ILCS 535/17)**\n\n"
            "Since 2018, Illinois eliminated the surgical requirement.\n\n"
            "Submit to Illinois Department of Public Health:\n"
            "- Form VR 396B (request for gender designation change).\n"
            "- A signed declaration from a **licensed healthcare professional** "
            "(physician, NP, psychologist, social worker — broader than most "
            "states) attesting to the gender identity.\n"
            "- Court order if your name is also changing.\n"
            "- Fee around $15.\n\n"
            "**Gender marker on driver's license** (Illinois Secretary of "
            "State): submit Form DSD A 251 with healthcare provider attestation. "
            "Non-binary 'X' marker is available."
        ),
        "source_url": "https://www.cyberdriveillinois.com/departments/drivers/drivers_license/genderdesignation.html",
    },
]

SCENARIOS = [
    {
        "slug": "workplace-discrimination-lgbtq",
        "title": "I'm being discriminated against at work for being LGBTQ+",
        "linked_statutes": ["775 ILCS 5/1-103 (sexual orientation & gender identity)"],
        "description_md": (
            "You came out (or were outed) and now your hours are cut, your "
            "boss makes comments, your coworkers harass you, or you've been "
            "fired. In Illinois — unlike most states — this is illegal at "
            "every workplace regardless of size, with strong remedies."
        ),
        "walkthrough_md": (
            "## What to do\n\n"
            "1. **Document everything.** Comments (date, who said what, "
            "witnesses), schedule changes, performance criticism that started "
            "after coming out, written warnings. Save in personal email/cloud, "
            "not work account.\n\n"
            "2. **Compare your treatment to others'.** Are similarly-situated "
            "straight or cisgender coworkers treated the same way? Different "
            "treatment is evidence.\n\n"
            "3. **Internal complaint** (recommended, not required). File "
            "with HR or your manager's manager in writing. This creates a "
            "paper trail and gives the employer a chance to fix it. **Save "
            "your complaint.** Retaliation for complaining is a **separate** "
            "violation.\n\n"
            "4. **File an IDHR charge within 300 days.** Free, no lawyer "
            "needed. Online at illinois.gov/dhr. The Illinois IDHR will "
            "investigate, attempt mediation, and (if appropriate) refer to "
            "litigation.\n\n"
            "5. **Dual-file with the EEOC** (usually automatic). Federal "
            "Title VII also protects LGBTQ+ workers after *Bostock v. Clayton "
            "County* (2020), but the Illinois Human Rights Act is broader "
            "(covers smaller employers and has additional protections).\n\n"
            "6. **Get a lawyer.** Many employment lawyers take strong cases "
            "on contingency. Don't sign a severance agreement or "
            "general-release form without one reading it first.\n\n"
            "## Possible remedies\n\n"
            "- Back pay (wages you lost).\n"
            "- Reinstatement (your job back).\n"
            "- Front pay (if reinstatement isn't feasible).\n"
            "- Emotional-distress damages.\n"
            "- Attorney's fees (which is why lawyers take these).\n"
            "- Punitive damages in egregious cases.\n\n"
            "## Free help\n\n"
            "- **Illinois Department of Human Rights**: (312) 814-6200\n"
            "- **EEOC Chicago District Office**: (800) 669-4000\n"
            "- **Lambda Legal Help Desk** (LGBTQ+ specialty): (312) 663-4413\n"
            "- **ACLU of Illinois**: (312) 201-9740\n"
            "- **Equality Illinois**: equalityillinois.us\n\n"
            "---\n\n"
            "*This is reference material, not legal advice. The 300-day IDHR "
            "filing deadline is strict.*"
        ),
        "template_md": None,
    },
    {
        "slug": "name-and-gender-change",
        "title": "I want to change my legal name and/or gender marker",
        "linked_statutes": ["750 ILCS 35 / 410 ILCS 535/17 (name & gender change)"],
        "description_md": (
            "You want your legal documents to reflect who you are. Illinois "
            "process is relatively friendly — no surgical requirement for "
            "gender markers, and publication can be waived for safety. "
            "But the paperwork is in pieces (court for name, IDPH for "
            "birth certificate, Secretary of State for license), so the "
            "order of operations matters."
        ),
        "walkthrough_md": (
            "## Recommended order\n\n"
            "1. **Court name change first.** Most other updates need the "
            "court order.\n"
            "2. **Driver's license** (gender marker + name).\n"
            "3. **Social Security card** (name + SSA gender marker).\n"
            "4. **Birth certificate** (if Illinois-born).\n"
            "5. **Passport** (US passports use 'X' gender option as of 2022).\n"
            "6. **Bank accounts, utilities, employer records, leases.**\n\n"
            "## Step-by-step\n\n"
            "**Name change (court):**\n\n"
            "1. **Pick up forms** at the circuit court in your county or "
            "download from illinoiscourts.gov.\n"
            "2. **Complete the Petition for Change of Name.** State current "
            "name, desired name, your address, prior names (if any), "
            "criminal history (some convictions create barriers).\n"
            "3. **File at the clerk's office.** ~$385 filing fee in Cook "
            "County (waiver available — request a fee waiver application).\n"
            "4. **Publication:** Illinois requires 3 weeks of newspaper "
            "publication. **You can waive this for safety reasons** — file "
            "a 'Motion to Waive Publication' citing fear of discrimination "
            "or violence. Granted routinely for LGBTQ+ applicants.\n"
            "5. **Court hearing.** Often 5 minutes. The judge confirms your "
            "identity and grants the order.\n"
            "6. **Certified copies** ($9 each — get several; you'll need "
            "them for every update).\n\n"
            "**Driver's license (Illinois Secretary of State):**\n\n"
            "1. Visit any Driver Services facility.\n"
            "2. Bring: certified court order (for name), Form DSD A 251 "
            "(gender marker; signed by healthcare provider — physician, NP, "
            "psychologist, etc.).\n"
            "3. The 'X' non-binary marker is available; check the box on "
            "DSD A 251.\n"
            "4. New license issued same day.\n\n"
            "**Social Security:**\n\n"
            "1. SSA Form SS-5 (name change).\n"
            "2. SSA gender marker: as of 2022, **self-attestation only** — "
            "no medical documentation required. Just request the change.\n"
            "3. Mail or in-person at any SSA office.\n\n"
            "**Birth certificate** (Illinois Department of Public Health, "
            "for IL-born only):\n\n"
            "1. Form VR 396B.\n"
            "2. Certified court order (for name).\n"
            "3. Healthcare-provider attestation (for gender marker — no "
            "surgery required since 2018).\n"
            "4. Fee ~$15.\n"
            "5. Processing time can be 4-12 weeks.\n\n"
            "**Passport:**\n\n"
            "1. Form DS-82 (renewal) or DS-11 (new).\n"
            "2. Self-attestation of gender marker (no medical proof since "
            "2021); 'X' marker available since 2022.\n\n"
            "## Free help\n\n"
            "- **Transformative Justice Law Project of Illinois**: tjlp.org "
            "(free name-change clinics for trans Illinoisans)\n"
            "- **Lambda Legal**: lambdalegal.org\n"
            "- **Howard Brown Health legal navigation**: howardbrown.org\n"
            "- **ACLU of Illinois**: (312) 201-9740\n\n"
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
