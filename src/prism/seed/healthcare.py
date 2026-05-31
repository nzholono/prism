"""Seed data: healthcare & medical bills (Illinois)."""

from __future__ import annotations

import sqlite3

DOMAIN = {
    "slug": "healthcare",
    "name": "Healthcare & Medical Bills",
    "tier": 2,
    "summary": (
        "Your rights as a patient in Illinois: hospital charity care, "
        "protection from surprise billing, mental health parity, EMTALA "
        "emergency-care rights, and how to negotiate a medical bill down."
    ),
}

STATUTES = [
    {
        "citation": "210 ILCS 89/10",
        "title": "Illinois Hospital Uninsured Patient Discount Act",
        "summary": (
            "Illinois hospitals must offer discounts to uninsured patients "
            "with family income below 600% of the federal poverty level. "
            "Rural and critical-access hospitals: discounts down to actual "
            "Medicare reimbursement rates. Urban hospitals: 135% of cost."
        ),
        "body_md": (
            "**210 ILCS 89/10 — Illinois Hospital Uninsured Patient Discount Act**\n\n"
            "Applies to most non-profit Illinois hospitals (small rural "
            "hospitals have a separate, even more generous formula).\n\n"
            "**Who qualifies:**\n\n"
            "- Uninsured (no health insurance or Medicare/Medicaid).\n"
            "- Illinois resident.\n"
            "- Family income at or below **600% of the federal poverty level** "
            "(FPL). For 2025: roughly $90,000/year for an individual, "
            "$183,000/year for a family of four.\n\n"
            "**The discount:**\n\n"
            "- Urban hospitals can charge at most **135% of cost** (which is "
            "typically a small fraction of the 'sticker price' on your bill).\n"
            "- Rural/critical-access hospitals: capped at actual Medicare "
            "reimbursement rates.\n\n"
            "**Maximum collection in any 12-month period:** capped at 25% of "
            "your annual family income (more strict caps at lower incomes).\n\n"
            "**The hospital must:**\n\n"
            "- Tell you about this discount.\n"
            "- Provide an application.\n"
            "- Decide within 60 days of receiving your application.\n\n"
            "**Most hospitals also have charity care policies** that go even "
            "further — full forgiveness for very-low-income patients. Always "
            "apply for both."
        ),
        "source_url": "https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2988",
    },
    {
        "citation": "No Surprises Act (federal)",
        "title": "Federal No Surprises Act — protection from surprise billing",
        "summary": (
            "Since 2022, federal law forbids 'balance billing' for "
            "out-of-network emergency care, out-of-network providers at "
            "in-network facilities, and air ambulance services. If you receive "
            "a surprise bill, you can dispute it through the federal IDR process."
        ),
        "body_md": (
            "**The No Surprises Act (effective January 1, 2022)**\n\n"
            "Protects you from being 'balance billed' (the practice of an "
            "out-of-network provider billing you for the difference between "
            "what they charge and what your insurance paid).\n\n"
            "**Covered situations:**\n\n"
            "- **Emergency services** at any hospital — you pay only your "
            "in-network cost-share.\n"
            "- **Non-emergency services at an in-network facility** when an "
            "out-of-network provider treats you (e.g., the anesthesiologist "
            "is out-of-network at an in-network hospital).\n"
            "- **Air ambulance** — protected.\n\n"
            "**Not covered (you can still be balance billed):**\n\n"
            "- Ground ambulance (a major gap — Illinois lawmakers are "
            "working on this).\n"
            "- Some elective procedures where you signed a written waiver.\n\n"
            "**If you get a surprise bill anyway:**\n\n"
            "1. **Don't pay it.** First confirm whether the No Surprises Act applies.\n"
            "2. **Call the No Surprises Help Desk:** 1-800-985-3059.\n"
            "3. **File a complaint** at cms.gov/nosurprises.\n"
            "4. Initiate **Independent Dispute Resolution (IDR)** if needed."
        ),
        "source_url": "https://www.cms.gov/nosurprises",
    },
]

SCENARIOS = [
    {
        "slug": "shocking-medical-bill",
        "title": "I received a shockingly high medical bill",
        "linked_statutes": ["210 ILCS 89/10", "No Surprises Act (federal)"],
        "description_md": (
            "An ER visit, an ambulance ride, a 'routine' scan — and the bill "
            "is in the thousands or tens of thousands. Don't panic and don't "
            "pay yet. Most medical bills are negotiable, often dramatically, "
            "and Illinois has unusually strong patient protections."
        ),
        "walkthrough_md": (
            "## What to do (in order)\n\n"
            "1. **Don't pay immediately.** Hospitals routinely offer 30-60% "
            "discounts to patients who ask. Paying upfront forfeits all "
            "leverage.\n\n"
            "2. **Get an itemized bill.** Call the billing office and "
            "request it in writing. The summary bill is often vague; the "
            "itemized one lets you spot errors and overcharges.\n\n"
            "3. **Look for errors.** Medical billing errors are "
            "extraordinarily common — duplicates, services not rendered, "
            "wrong insurance applied. Highlight anything you don't recognize.\n\n"
            "4. **Check if the No Surprises Act applies.** If this was an "
            "emergency or you saw an out-of-network provider at an in-network "
            "facility, **call 1-800-985-3059** to dispute. Don't pay anything "
            "the No Surprises Act doesn't permit.\n\n"
            "5. **Apply for charity care.** Every Illinois hospital has a "
            "charity care policy. Ask billing for the application. If your "
            "family income is below 200% of FPL, you may qualify for full "
            "forgiveness. Apply even if you think you don't qualify.\n\n"
            "6. **Apply under the Illinois Hospital Uninsured Patient Discount "
            "Act.** Income below 600% of FPL (around $90K for a single person) "
            "and uninsured? You're entitled to substantial discounts by law. "
            "Hospitals must process your application within 60 days.\n\n"
            "7. **Negotiate.** If charity care doesn't fully apply, call "
            "billing and ask:\n"
            "   - 'Will you accept the Medicare reimbursement rate?' (often "
            "30-40% of the sticker price.)\n"
            "   - 'Can I set up a 0% interest payment plan?'\n"
            "   - 'Will you accept [amount] in full settlement?' (start at "
            "30% of the bill.)\n"
            "   Get any agreement **in writing** before paying anything.\n\n"
            "8. **Don't let them send you to collections without responding.** "
            "Once a bill goes to a third-party collector, you have additional "
            "rights under the FDCPA. But it's also harder to negotiate "
            "directly with the hospital after that.\n\n"
            "9. **For ambulance bills**, ask the ambulance company about "
            "hardship/membership programs. Many Illinois municipalities have "
            "no-fee policies for residents.\n\n"
            "10. **If you have insurance and they denied a claim**, file an "
            "internal appeal first (deadlines apply — usually 180 days). "
            "Then an external appeal through the Illinois Department of "
            "Insurance: insurance.illinois.gov.\n\n"
            "## Free help\n\n"
            "- **AGE Options** (medical billing help for any age in IL): ageoptions.org\n"
            "- **Triage Cancer** (specific to cancer bills): triagecancer.org\n"
            "- **CARPLS** (general legal help): (312) 738-9200\n"
            "- **Illinois Department of Insurance**: (877) 527-9431\n"
            "- **No Surprises Help Desk**: 1-800-985-3059\n\n"
            "---\n\n"
            "*This is reference material, not legal advice.*"
        ),
        "template_md": (
            "## Hospital negotiation script\n\n"
            "```\n"
            "Hello, I'm calling about account #{{account number}}.\n"
            "I received a bill for ${{amount}}.\n\n"
            "1. Can you send me an itemized statement of services?\n"
            "2. I'd like to apply for charity care — please send the application.\n"
            "3. I'd also like to apply under the Illinois Hospital Uninsured "
            "Patient Discount Act, 210 ILCS 89/10.\n"
            "4. While my application is processed, please put a hold on "
            "collections activity and confirm in writing.\n"
            "5. If I'm not eligible for full charity, what's the lowest "
            "amount you can accept as payment in full?\n\n"
            "Thank you. Please confirm everything in writing to "
            "{{your address}}.\n"
            "```\n"
        ),
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
