"""Seed data: tenant rights domain (Illinois).

Coverage: security deposits, eviction notice, repairs / warranty of habitability.
Focus is on the things DePaul students actually encounter.

Citations checked against ilga.gov and the Chicago Municipal Code as of 2026.
This is reference material, not legal advice — every scenario ends with the
free-legal-aid disclaimer.
"""

from __future__ import annotations

import sqlite3

DOMAIN = {
    "slug": "tenant",
    "name": "Tenant Rights",
    "tier": 1,
    "summary": (
        "Your rights as a renter in Illinois and (where applicable) the City of "
        "Chicago — what your landlord can and cannot do, the deadlines they must "
        "meet, and what to do when they don't."
    ),
}

STATUTES = [
    {
        "citation": "765 ILCS 710/1",
        "title": "Illinois Security Deposit Return Act — return deadlines",
        "summary": (
            "If your landlord owns five or more rental units in any combination of "
            "buildings, they must return your security deposit within 45 days of "
            "you vacating. If they keep any portion for damages, they must give you "
            "an itemized written statement of damages within 30 days, with paid "
            "receipts, or pay you the full deposit back."
        ),
        "body_md": (
            "**765 ILCS 710/1 — Security Deposit Return Act**\n\n"
            "Applies to landlords of buildings containing 5 or more rental units.\n\n"
            "Key deadlines:\n\n"
            "- **30 days** after the tenant vacates: landlord must mail itemized "
            "statement of damages with paid receipts if they intend to withhold any "
            "portion of the deposit.\n"
            "- **45 days** after the tenant vacates: landlord must return the deposit "
            "(minus documented damages).\n\n"
            "If the landlord misses the 30-day itemization deadline, they forfeit "
            "their right to deduct anything and must return the full deposit by the "
            "45-day deadline.\n\n"
            "**Penalty for violation:** Under 765 ILCS 710/2, a tenant suing "
            "successfully under the Act is entitled to **twice the amount of the "
            "deposit wrongfully withheld**, plus court costs and reasonable attorney's "
            "fees."
        ),
        "source_url": "https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2153",
    },
    {
        "citation": "765 ILCS 710/2",
        "title": "Illinois Security Deposit Return Act — penalty for wrongful retention",
        "summary": (
            "A tenant who wins a security-deposit lawsuit under the Act is entitled "
            "to twice the amount wrongfully withheld, plus court costs and attorney's "
            "fees. This is one of the strongest tenant remedies in Illinois law."
        ),
        "body_md": (
            "**765 ILCS 710/2 — Penalty provision**\n\n"
            "If the landlord fails to comply with the itemization or return deadlines "
            "of 765 ILCS 710/1, the tenant may recover:\n\n"
            "1. **Twice the amount wrongfully withheld** (double damages).\n"
            "2. **Court costs.**\n"
            "3. **Reasonable attorney's fees.**\n\n"
            "Small-claims court in Illinois can hear cases up to $10,000, and these "
            "deposit cases fit comfortably within that limit. You do not need a lawyer "
            "to file in small claims."
        ),
        "source_url": "https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2153",
    },
    {
        "citation": "Chi. Mun. Code 5-12-080",
        "title": "Chicago Residential Landlord and Tenant Ordinance (RLTO) — security deposits",
        "summary": (
            "Chicago's RLTO covers most rentals in the city (with some exceptions for "
            "owner-occupied buildings of 6 or fewer units). It requires landlords to "
            "hold deposits in a separate interest-bearing account in an Illinois bank, "
            "and to return the deposit within 45 days. Violations can trigger damages "
            "of two times the deposit plus attorney's fees."
        ),
        "body_md": (
            "**Chicago Municipal Code 5-12-080 — Security deposits under the RLTO**\n\n"
            "The Chicago RLTO applies to most rental units within the city. It does "
            "**not** apply to:\n\n"
            "- Owner-occupied buildings with 6 or fewer units.\n"
            "- Dormitories, hotels, hospitals.\n"
            "- Units in cooperative housing.\n\n"
            "Key requirements:\n\n"
            "- Deposit must be held in a federally-insured Illinois bank, in a "
            "separate account from the landlord's own funds.\n"
            "- Landlord must give a receipt naming the bank.\n"
            "- **Interest** must be paid on deposits held more than 6 months (the "
            "Chicago City Comptroller publishes the rate annually).\n"
            "- Itemized statement of damages within 30 days.\n"
            "- Deposit returned within 45 days.\n\n"
            "**Penalty:** Two times the deposit, plus attorney's fees, for violations "
            "of the deposit rules. This is on top of any state-law remedies."
        ),
        "source_url": (
            "https://codelibrary.amlegal.com/codes/chicago/latest/chicago_il/0-0-0-2607797"
        ),
    },
    {
        "citation": "735 ILCS 5/9-209",
        "title": "Forcible Entry and Detainer — five-day notice for non-payment of rent",
        "summary": (
            "Before a landlord can file an eviction case for unpaid rent in Illinois, "
            "they must serve you with a written 'five-day notice' demanding payment. "
            "If you pay within five days, the landlord must accept the rent and "
            "cannot proceed with eviction on that ground."
        ),
        "body_md": (
            "**735 ILCS 5/9-209 — Five-day notice for non-payment of rent**\n\n"
            "Before filing an eviction action for unpaid rent, the landlord must:\n\n"
            "1. Serve a written notice demanding the amount due.\n"
            "2. Give you **at least 5 days** to pay.\n"
            "3. Properly serve the notice (in person, by certified mail, or by "
            "posting if you are absent from the premises).\n\n"
            "If you tender the full amount demanded within the 5 days, the landlord "
            "**must** accept it and cannot evict you for that non-payment.\n\n"
            "If you pay only part of what's demanded, the landlord can refuse and "
            "proceed. Get the landlord's agreement in writing if you negotiate a "
            "partial payment."
        ),
        "source_url": "https://www.ilga.gov/legislation/ilcs/documents/073500050K9-209.htm",
    },
    {
        "citation": "Jack Spring, Inc. v. Little (1972)",
        "title": "Illinois implied warranty of habitability",
        "summary": (
            "Under Illinois case law, every residential lease carries an implied "
            "warranty that the unit is fit to live in. If your landlord fails to keep "
            "the unit habitable (heat, water, freedom from infestation, structural "
            "safety), you may have rights to withhold rent, repair-and-deduct, or "
            "terminate the lease — but only if you follow the right notice procedures."
        ),
        "body_md": (
            "**Jack Spring, Inc. v. Little, 50 Ill.2d 351 (1972)**\n\n"
            "The Illinois Supreme Court held that every written and oral residential "
            "lease in Illinois includes an **implied warranty of habitability**. The "
            "warranty requires the landlord to deliver and maintain premises that are "
            "fit for residential use.\n\n"
            "What counts as a breach of habitability:\n\n"
            "- No heat in winter\n"
            "- No running water or hot water\n"
            "- Severe pest infestation (roaches, rats, bedbugs)\n"
            "- Structural problems making the unit unsafe\n"
            "- No working electricity\n"
            "- Conditions that violate the local building code\n\n"
            "**Important:** to invoke remedies, you generally must give the landlord "
            "written notice and a reasonable time to fix the problem. The exact "
            "procedure depends on whether Chicago's RLTO applies or only the common "
            "law. Document everything (photos, dates, written notices)."
        ),
        "source_url": "https://law.justia.com/cases/illinois/supreme-court/1972/44537-7.html",
    },
]

SCENARIOS = [
    {
        "slug": "breaking-lease-early",
        "title": "I need to break my lease early",
        "linked_statutes": ["Chi. Mun. Code 5-12-080"],
        "description_md": (
            "Job in another city, medical situation, abusive household, "
            "domestic violence — you need out of your lease before it ends. "
            "Illinois protects renters in some specific situations, and the "
            "Chicago RLTO has stronger rules. The penalty for just walking "
            "away can be steep, so know your options first."
        ),
        "walkthrough_md": (
            "## What to do\n\n"
            "1. **Re-read your lease for early-termination clauses.** Some "
            "leases let you pay a fixed buyout (typically 2 months rent). "
            "If yours does, that's usually the cleanest path.\n\n"
            "2. **Identify whether a legal protection applies:**\n"
            "   - **Active military service** — federal SCRA lets you "
            "terminate without penalty when called to active duty.\n"
            "   - **Domestic violence** — Illinois VESSA (Victims' Economic "
            "Security and Safety Act) lets you terminate after written notice "
            "plus documentation (police report, order of protection, "
            "court record).\n"
            "   - **Uninhabitable conditions** — if landlord won't fix major "
            "issues, see the 'repairs not made' scenario; you may have a "
            "right to terminate.\n"
            "   - **Constructive eviction** — landlord's actions made the "
            "unit unusable. High bar; talk to a lawyer.\n\n"
            "3. **Otherwise, negotiate.** Most landlords prefer a paying "
            "replacement tenant over an empty unit. Offer to:\n"
            "   - Find a qualified replacement tenant who will sign a new lease.\n"
            "   - Pay 1-2 months as a buyout.\n"
            "   - Forfeit your security deposit.\n"
            "   Get any agreement in writing.\n\n"
            "4. **Know about the duty to mitigate damages.** Illinois "
            "landlords **must make reasonable efforts to re-rent** the unit. "
            "If they leave it empty out of spite, that's not your problem. "
            "Document any evidence they aren't trying (no listings, no showings).\n\n"
            "5. **If you just walk away**, the landlord can sue for the "
            "remaining rent owed (minus any rent they collected from a new "
            "tenant after reasonable mitigation), keep your deposit, and "
            "report you to a tenant-screening service. This will hurt future "
            "rental applications for years.\n\n"
            "6. **Send written notice** before vacating. Include your "
            "forwarding address. Take dated photos of the empty, clean unit. "
            "Return all keys. Document everything via certified mail.\n\n"
            "## Free legal help\n\n"
            "- **CARPLS**: (312) 738-9200\n"
            "- **Lawyers' Committee for Better Housing**: lcbh.org\n"
            "- **Illinois Coalition Against Domestic Violence**: ilcadv.org "
            "(VESSA help)\n\n"
            "---\n\n"
            "*This is reference material, not legal advice.*"
        ),
        "template_md": (
            "## Termination notice template (negotiated)\n\n"
            "```\n"
            "{{Your Name}}\n"
            "{{Address}}\n"
            "{{Date}}\n\n"
            "{{Landlord Name}}\n"
            "{{Address}}\n\n"
            "SENT CERTIFIED MAIL\n\n"
            "Re: Lease at {{unit address}}, dated {{lease date}}\n\n"
            "Dear {{Landlord Name}},\n\n"
            "I am writing to provide notice that I will be vacating the above "
            "unit on {{vacate date}}, prior to the lease end date of "
            "{{lease end date}}.\n\n"
            "I propose the following terms:\n\n"
            "1. I will pay {{X months}} of rent as a buyout (${{amount}}).\n"
            "2. I forfeit my security deposit of ${{amount}}.\n"
            "3. I will return all keys and leave the unit broom-clean.\n"
            "4. The lease will be considered fully terminated as of "
            "{{vacate date}}, with no further obligations on either side.\n\n"
            "Please respond in writing by {{date}} to confirm these terms or "
            "propose alternatives. I am also willing to help find a "
            "replacement tenant.\n\n"
            "My forwarding address will be: {{address}}.\n\n"
            "Sincerely,\n"
            "{{Your Name}}\n"
            "```\n"
        ),
    },
    {
        "slug": "deposit-not-returned",
        "title": "Landlord didn't return my security deposit",
        "linked_statutes": [
            "765 ILCS 710/1",
            "765 ILCS 710/2",
            "Chi. Mun. Code 5-12-080",
        ],
        "description_md": (
            "You moved out, you left the unit clean, and now it's been more than 45 "
            "days and your landlord hasn't returned your deposit — or they returned "
            "only part of it with no itemized statement, or with vague claims of "
            "'damages' that don't add up. This is one of the most common landlord "
            "violations in Illinois, and the law is on your side."
        ),
        "walkthrough_md": (
            "## What to do\n\n"
            "1. **Confirm the deadline has passed.** Illinois law (765 ILCS 710/1) "
            "and the Chicago RLTO both require the deposit to be returned within "
            "**45 days** of you vacating. If the landlord intends to deduct anything, "
            "they must give you an **itemized written statement with paid receipts "
            "within 30 days**.\n\n"
            "2. **Gather your evidence.** Move-in and move-out photos, your lease, "
            "the cancelled check or receipt showing you paid the deposit, copies of "
            "any text messages or emails with the landlord, and your forwarding "
            "address that you gave the landlord.\n\n"
            "3. **Send a demand letter.** Use the template below. Send it by "
            "**certified mail with return receipt** (about $9 at any USPS) to the "
            "landlord's last known address. Keep a copy. Give them 14 days to respond.\n\n"
            "4. **If they don't respond or refuse, file in small claims court.** "
            "In Cook County, small-claims jurisdiction goes up to $10,000. The "
            "filing fee is around $50–$120 depending on the amount, and there is "
            "no jury — you present your case to a judge. You do not need a lawyer.\n\n"
            "5. **Know what you can recover.** Under 765 ILCS 710/2 and the Chicago "
            "RLTO, you can ask for:\n"
            "    - **Twice** the amount of the deposit wrongfully withheld.\n"
            "    - Your **court costs**.\n"
            "    - **Reasonable attorney's fees** (if you used one).\n\n"
            "6. **Bring your evidence to court.** Print three copies of everything: "
            "one for the judge, one for the landlord, one for you.\n\n"
            "7. **If you win, collecting is a separate step.** A judgment is paper "
            "until you act on it. Options include wage garnishment, bank levy, or "
            "negotiating a settlement. Free legal aid can help.\n\n"
            "## Free legal aid in Illinois\n\n"
            "- **CARPLS** (Cook County legal help line): (312) 738-9200\n"
            "- **Illinois Legal Aid Online**: illinoislegalaid.org (has small-claims guides)\n"
            "- **Lawyers' Committee for Better Housing**: lcbh.org (focuses on tenant cases)\n\n"
            "---\n\n"
            "*This is reference material, not legal advice. For your specific "
            "situation, contact a licensed Illinois attorney or one of the free "
            "legal aid resources above.*"
        ),
        "template_md": (
            "## Demand letter template\n\n"
            "```\n"
            "{{Your Name}}\n"
            "{{Your New Address}}\n"
            "{{City, IL ZIP}}\n"
            "{{Date}}\n\n"
            "{{Landlord Name}}\n"
            "{{Landlord Address}}\n"
            "{{City, IL ZIP}}\n\n"
            "SENT VIA CERTIFIED MAIL, RETURN RECEIPT REQUESTED\n\n"
            "Re: Security deposit for {{rental unit address}}\n\n"
            "Dear {{Landlord Name}},\n\n"
            "I vacated the above rental unit on {{move-out date}}. Pursuant to the "
            "Illinois Security Deposit Return Act (765 ILCS 710/1) {{and the "
            "Chicago Residential Landlord and Tenant Ordinance (5-12-080), if Chicago}}, "
            "you were required to return my security deposit of ${{amount}} within 45 "
            "days, and to provide any itemized statement of deductions within 30 days.\n\n"
            "As of today, more than {{number}} days have passed, and I have not "
            "received {{the deposit / a proper itemized statement / the full deposit}}. \n\n"
            "I hereby demand the return of the full $${{amount}} within 14 days of your "
            "receipt of this letter. If I do not receive payment, I will file a small-"
            "claims action seeking twice the deposit wrongfully withheld, plus court "
            "costs and attorney's fees, as provided by 765 ILCS 710/2.\n\n"
            "My forwarding address is at the top of this letter.\n\n"
            "Sincerely,\n"
            "{{Your Name}}\n"
            "```\n"
        ),
    },
    {
        "slug": "five-day-notice",
        "title": "I got a five-day notice for unpaid rent",
        "linked_statutes": ["735 ILCS 5/9-209"],
        "description_md": (
            "Your landlord gave you a 'five-day notice' demanding overdue rent. "
            "This is the required first step before they can file an eviction case. "
            "You still have options, but the clock is running."
        ),
        "walkthrough_md": (
            "## What to do\n\n"
            "1. **Read the notice carefully.** Confirm the amount demanded is "
            "correct (compare to your records of rent paid). Note the exact date "
            "the notice was served — your five days run from then.\n\n"
            "2. **If the amount is right and you can pay, pay the full amount within "
            "5 days.** Get a written receipt. Under 735 ILCS 5/9-209, the landlord "
            "**must** accept full payment within the 5-day window and cannot proceed "
            "with eviction for that non-payment.\n\n"
            "3. **If the amount is wrong**, send a written response within the 5 "
            "days explaining the discrepancy with evidence (cancelled checks, "
            "receipts). This doesn't stop the clock, but it documents your position.\n\n"
            "4. **If you cannot pay everything**, call free legal aid immediately. "
            "CARPLS at (312) 738-9200 or Chicago Volunteer Legal Services. There "
            "are rental-assistance programs that can sometimes pay your back rent "
            "directly to the landlord.\n\n"
            "5. **Do not move out just because of the notice.** A five-day notice "
            "is not an eviction. The landlord still has to go to court, win a "
            "judgment, and have the sheriff (not the landlord) physically remove "
            "you. You have time to negotiate or to find help.\n\n"
            "6. **If the landlord files in court**, you will be served with a "
            "summons. **Show up to every court date.** Failing to appear is the "
            "single biggest reason tenants lose evictions they could have won.\n\n"
            "## Free legal aid in Illinois\n\n"
            "- **CARPLS**: (312) 738-9200\n"
            "- **Lawyers' Committee for Better Housing**: lcbh.org\n"
            "- **Chicago Volunteer Legal Services**: cvls.org\n"
            "- **Illinois Department of Human Services rental assistance**: dhs.state.il.us\n\n"
            "---\n\n"
            "*This is reference material, not legal advice. For your specific "
            "situation, contact a licensed Illinois attorney or one of the free "
            "legal aid resources above.*"
        ),
        "template_md": None,
    },
    {
        "slug": "repairs-not-made",
        "title": "Landlord won't fix essential conditions (heat, water, pests)",
        "linked_statutes": [
            "Jack Spring, Inc. v. Little (1972)",
            "Chi. Mun. Code 5-12-080",
        ],
        "description_md": (
            "Your landlord is refusing to fix something that makes the unit unsafe "
            "or unsanitary — no heat in winter, no hot water, severe pest "
            "infestation, broken locks, exposed wiring. Under the Illinois implied "
            "warranty of habitability, you may have powerful remedies. But you have "
            "to follow the right procedure — withholding rent without notice can "
            "backfire."
        ),
        "walkthrough_md": (
            "## What to do\n\n"
            "1. **Document the problem.** Photos and videos with dates. If it's "
            "ongoing (no heat for days), log dates and temperatures.\n\n"
            "2. **Give the landlord written notice.** Email or text counts but "
            "certified mail is strongest. Describe the problem specifically. Ask "
            "for repair within a **reasonable time** — usually 14 days for "
            "non-emergencies, much sooner for things like no heat or no water in "
            "winter.\n\n"
            "3. **If it's a Chicago rental covered by the RLTO**, you have specific "
            "options after waiting the notice period:\n"
            "    - **Repair and deduct**: hire someone to fix it (up to $500 or "
            "half the monthly rent, whichever is more) and deduct the cost from "
            "your next rent — but only after following the exact RLTO procedure.\n"
            "    - **Withhold rent in proportion** to the reduced value of the unit.\n"
            "    - **Terminate the lease** if the problem is serious and not fixed "
            "within 14 days after notice.\n"
            "    - Sue for damages.\n\n"
            "4. **Outside Chicago**, your remedies come from the common law "
            "implied warranty of habitability (*Jack Spring v. Little*) plus any "
            "local ordinances. You generally need written notice and a reasonable "
            "chance to fix before withholding rent. **Get legal advice before "
            "withholding rent** — doing it wrong can lead to eviction.\n\n"
            "5. **Call the city.** In Chicago, call **311** to report building "
            "code violations. An inspector will visit and can issue citations. "
            "This creates an official paper trail.\n\n"
            "6. **Don't move out without legal advice unless you must for safety.** "
            "If conditions are dangerous (no heat in January, sewage backup), "
            "your safety comes first — leave and call CARPLS.\n\n"
            "## Free legal aid in Illinois\n\n"
            "- **CARPLS**: (312) 738-9200\n"
            "- **Lawyers' Committee for Better Housing**: lcbh.org\n"
            "- **Chicago 311** (building violations): dial 311 in Chicago\n"
            "- **Illinois Legal Aid Online**: illinoislegalaid.org\n\n"
            "---\n\n"
            "*This is reference material, not legal advice. For your specific "
            "situation, contact a licensed Illinois attorney or one of the free "
            "legal aid resources above.*"
        ),
        "template_md": None,
    },
]


def seed(conn: sqlite3.Connection) -> None:
    """Seed the tenant domain. Idempotent: existing rows are left untouched."""
    cur = conn.execute(
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
            (
                domain_id,
                s["citation"],
                s["title"],
                s["summary"],
                s["body_md"],
                s["source_url"],
            ),
        )
        statute_ids[s["citation"]] = cur.lastrowid

    for sc in SCENARIOS:
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

        for citation in sc["linked_statutes"]:
            statute_id = statute_ids.get(citation)
            if statute_id is None:
                continue
            conn.execute(
                "INSERT OR IGNORE INTO scenario_statutes (scenario_id, statute_id) "
                "VALUES (?, ?)",
                (scenario_id, statute_id),
            )

    conn.commit()
