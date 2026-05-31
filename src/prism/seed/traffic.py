"""Seed data: traffic & vehicle (Illinois)."""

from __future__ import annotations

import sqlite3

DOMAIN = {
    "slug": "traffic",
    "name": "Traffic & Vehicle",
    "tier": 2,
    "summary": (
        "Tickets, accidents, DUI basics, and the Chicago-specific quagmire "
        "of booting, towing, and red-light cameras. Most tickets are "
        "contestable if you know the process."
    ),
}

STATUTES = [
    {
        "citation": "Chi. Mun. Code 9-100-050",
        "title": "Chicago Administrative Hearings — how parking tickets are decided",
        "summary": (
            "Chicago parking and red-light camera tickets are decided through "
            "the Department of Administrative Hearings — a city agency, not "
            "a court. You can contest in person, by mail, or online. The "
            "burden is lower than criminal court, but valid defenses exist."
        ),
        "body_md": (
            "**Chicago Municipal Code 9-100-050 et seq. — Administrative "
            "Adjudication of Parking, Standing, and Compliance Violations**\n\n"
            "Parking tickets in Chicago are **not criminal** — they're civil "
            "violations handled by the Department of Administrative Hearings "
            "(DOAH). This means:\n\n"
            "- No risk of jail or criminal record.\n"
            "- No right to a jury, court-appointed lawyer, or some of the "
            "other protections of criminal proceedings.\n"
            "- Standard of proof is **'preponderance of the evidence'** "
            "(more likely than not) — not 'beyond a reasonable doubt'.\n\n"
            "**Three ways to contest:**\n\n"
            "1. **Online** at chicityclerk.com — fastest, but limited to "
            "certain defenses.\n"
            "2. **By mail** — submit a written explanation with evidence.\n"
            "3. **In person** at a DOAH hearing — best for complex defenses, "
            "requires taking time off.\n\n"
            "**Common winning defenses:**\n\n"
            "- The vehicle was stolen at the time.\n"
            "- The sign was missing, obscured, or contradictory.\n"
            "- The meter was broken (with proof — call 311 and get a ticket "
            "number when it happens).\n"
            "- The vehicle was sold and the title transferred before the "
            "ticket date.\n"
            "- You were not the registered owner (with proof).\n"
            "- A construction zone made compliance impossible.\n"
            "- For red-light camera tickets specifically: someone else was "
            "driving (sworn affidavit required) and certain technical "
            "defenses related to camera calibration.\n\n"
            "**Don't ignore the ticket.** After 25 days unpaid, fines double. "
            "After more time, your car can be **booted, towed, and the "
            "license suspended**."
        ),
        "source_url": (
            "https://codelibrary.amlegal.com/codes/chicago/latest/chicago_il/0-0-0-2615568"
        ),
    },
]

SCENARIOS = [
    {
        "slug": "parking-ticket-dispute",
        "title": "I want to fight a parking ticket in Chicago",
        "linked_statutes": ["Chi. Mun. Code 9-100-050"],
        "description_md": (
            "Chicago issues over 2 million parking tickets per year. Many "
            "of them have valid defenses — bad signage, broken meters, "
            "vehicle sold, construction zones. The process is annoying but "
            "doable, and ignoring the ticket is the worst option."
        ),
        "walkthrough_md": (
            "## What to do (in order)\n\n"
            "1. **Read the ticket carefully.** Note: ticket number, date and "
            "time, location, specific code violation cited, dollar amount, "
            "and the response deadline.\n\n"
            "2. **Photograph the scene NOW** (or as soon as possible). Get:\n"
            "   - The signs nearby (or their absence).\n"
            "   - Any obstructed sign, broken meter, construction equipment.\n"
            "   - The street layout.\n"
            "   - Time-stamped if your phone does that.\n\n"
            "3. **Pull the city's evidence.** If it's a red-light/speed camera "
            "ticket, you can view the actual video and photos on the ticket "
            "website. Sometimes the city's own evidence shows you didn't violate.\n\n"
            "4. **Pick how to contest:**\n"
            "   - **Online** (cityclerk.com): fastest, simplest. Best for "
            "clear-cut defenses (vehicle sold, no longer owned, sign down).\n"
            "   - **By mail**: include a written statement and photocopies of "
            "evidence. Keep originals. Send certified.\n"
            "   - **In person** at a DOAH hearing: best for complex cases, "
            "letter from witness, sworn affidavits. Be prepared to wait.\n\n"
            "5. **For the hearing (in-person)**:\n"
            "   - Bring three copies of everything (judge, you, city).\n"
            "   - Be brief and factual. Don't argue the law is unfair — "
            "argue you didn't violate it.\n"
            "   - Bring witnesses if relevant.\n"
            "   - Dress respectfully.\n\n"
            "6. **If you lose at first hearing:** you can request an **administrative "
            "review** within 35 days. If that fails, you can appeal to the Circuit "
            "Court of Cook County (usually requires a lawyer).\n\n"
            "## Common defenses that work\n\n"
            "- 'The sign was down/missing/obscured' (with photos).\n"
            "- 'The meter was broken — I reported it to 311, here's the "
            "service request number.'\n"
            "- 'The vehicle was sold before this date' (bill of sale, "
            "title-transfer record).\n"
            "- 'Construction made compliance impossible' (photos).\n"
            "- For street-sweeping tickets: 'the schedule was changed and not "
            "posted with required notice'.\n\n"
            "## What does NOT work\n\n"
            "- 'I only ran in for a minute.'\n"
            "- 'I didn't see the sign.'\n"
            "- 'The fine is too high.'\n"
            "- 'I was just in the wrong place.'\n\n"
            "## If your car is booted or about to be\n\n"
            "7. **Cars with 2+ tickets unpaid for 1+ year are eligible for "
            "booting** in Chicago. Once booted, fees mount fast.\n\n"
            "8. **If you're low income**, ask about the **Clear Path Relief "
            "Program** — Chicago wipes some debt for residents below certain "
            "income thresholds.\n\n"
            "9. **Don't drive a booted vehicle** — there's a separate, "
            "much-larger ticket for that.\n\n"
            "## Resources\n\n"
            "- **Chicago City Clerk** (ticket lookup, pay, contest): chicityclerk.com\n"
            "- **Department of Administrative Hearings**: chicago.gov/doah\n"
            "- **CARPLS** (free legal help): (312) 738-9200\n"
            "- **Clear Path Relief Program**: chicago.gov/clearpath\n\n"
            "---\n\n"
            "*This is reference material, not legal advice.*"
        ),
        "template_md": (
            "## Sample written defense (parking ticket contest by mail)\n\n"
            "```\n"
            "Department of Administrative Hearings\n"
            "City of Chicago\n"
            "{{Address from ticket back}}\n\n"
            "{{Your Name}}\n"
            "{{Your Address}}\n"
            "{{Date}}\n\n"
            "Re: Parking ticket #{{ticket number}}, issued {{date}} at "
            "{{location}}\n\n"
            "I respectfully request that this ticket be dismissed for the "
            "following reason(s):\n\n"
            "{{State your defense clearly. For example:}}\n"
            "On {{date}} at approximately {{time}}, the parking sign at this "
            "location was obscured by overgrown tree branches, making it "
            "impossible for me to read the parking restriction. Photographs "
            "taken on {{date}} are enclosed (Exhibits A and B).\n\n"
            "I respectfully request that this ticket be dismissed.\n\n"
            "Sincerely,\n"
            "{{Your Name}}\n\n"
            "Enclosures: Photos labeled A and B; copy of ticket.\n"
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
