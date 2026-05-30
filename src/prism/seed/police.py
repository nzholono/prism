"""Seed data: police & ICE encounters domain (Illinois)."""

from __future__ import annotations

import sqlite3

DOMAIN = {
    "slug": "police",
    "name": "Police & ICE Encounters",
    "tier": 1,
    "summary": (
        "Your rights when interacting with police, sheriffs, or immigration "
        "officers in Illinois. Illinois has stronger protections than most "
        "states — the TRUST Act limits local cooperation with ICE, and the "
        "SAFE-T Act reformed many police procedures."
    ),
}

STATUTES = [
    {
        "citation": "5 ILCS 805/15",
        "title": "Illinois TRUST Act — limits on local cooperation with ICE",
        "summary": (
            "Illinois law forbids local police and sheriffs from stopping, "
            "arresting, searching, or detaining anyone based on immigration "
            "status, or on the basis of an immigration detainer alone. State "
            "and local officers cannot enter into agreements that delegate "
            "civil immigration enforcement to them."
        ),
        "body_md": (
            "**5 ILCS 805/15 — Illinois TRUST Act**\n\n"
            "Illinois law enforcement agencies **shall not**:\n\n"
            "- Stop, arrest, search, or detain anyone solely based on "
            "immigration status or an immigration detainer.\n"
            "- Hold a person past their release date for ICE pickup based on a "
            "civil immigration detainer (which is not a judicial warrant).\n"
            "- Permit ICE access to non-public areas of state or local "
            "facilities without a judicial warrant.\n"
            "- Share information with ICE for purposes of civil immigration "
            "enforcement, beyond what federal law strictly requires.\n\n"
            "**What this means practically:** if you're detained by Chicago "
            "Police or Cook County Sheriff, they cannot keep you in jail past "
            "your release time just because ICE asked them to. ICE needs a "
            "**judicial warrant** (signed by a judge), not a civil 'detainer' "
            "form (signed by an ICE officer), to compel cooperation.\n\n"
            "**Federal ICE agents are not bound by the TRUST Act.** They can "
            "still conduct their own enforcement actions. The Act limits "
            "**Illinois state and local** cooperation."
        ),
        "source_url": "https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=3795",
    },
    {
        "citation": "725 ILCS 5/107-14",
        "title": "Illinois 'Stop & Identify' rules during a Terry stop",
        "summary": (
            "If a police officer in Illinois has reasonable suspicion of a "
            "crime, they may stop you briefly and ask for your name, address, "
            "and an explanation. Beyond identifying yourself if asked, you "
            "have the right to remain silent. You do not have to consent to "
            "searches; police need probable cause or a warrant."
        ),
        "body_md": (
            "**725 ILCS 5/107-14 — Temporary investigative stops**\n\n"
            "Under Illinois law, a peace officer may stop a person in a public "
            "place for a reasonable time when the officer reasonably suspects "
            "that the person is committing, is about to commit, or has "
            "committed a crime. During the stop, the officer may demand:\n\n"
            "1. The person's name.\n"
            "2. Their address.\n"
            "3. An explanation of their actions.\n\n"
            "**What you must do:** identify yourself if asked.\n\n"
            "**What you do NOT have to do:**\n\n"
            "- Answer further questions (you have the right to remain silent).\n"
            "- Consent to a search of your person, bag, car, or home.\n"
            "- Show ID if you are not driving (in Illinois — driving requires a license).\n\n"
            "**Magic words that protect you:**\n\n"
            "- *'I am exercising my right to remain silent.'*\n"
            "- *'I do not consent to any search.'*\n"
            "- *'Am I free to go?'* (if they say yes, walk away calmly)\n"
            "- *'I want a lawyer.'*\n\n"
            "**Do not physically resist** even an unlawful stop or search. "
            "Comply with orders, complain later through legal channels."
        ),
        "source_url": "https://www.ilga.gov/legislation/ilcs/documents/072500050K107-14.htm",
    },
    {
        "citation": "725 ILCS 5/103-2.1",
        "title": "Illinois recorded-interrogation requirements",
        "summary": (
            "Illinois law requires custodial interrogations for serious "
            "felonies (and many other offenses) to be electronically recorded. "
            "Unrecorded statements may be inadmissible. This is a strong "
            "protection — you should always invoke your right to silence and "
            "to a lawyer before answering questions in custody."
        ),
        "body_md": (
            "**725 ILCS 5/103-2.1 — Electronic recording of custodial interrogations**\n\n"
            "When a person is in custody at a police station or detention "
            "facility, the **entire** interrogation about certain serious "
            "offenses (including murder, sexual assault, and other Class X "
            "felonies, plus many additional offenses added in later "
            "amendments) must be electronically recorded.\n\n"
            "An unrecorded custodial statement is **presumed inadmissible** "
            "(with limited exceptions), giving you significant leverage if "
            "the police later try to use a statement against you.\n\n"
            "**The right thing to do in custody:**\n\n"
            "1. **'I am exercising my right to remain silent.'**\n"
            "2. **'I want a lawyer.'**\n"
            "3. Then say nothing else, even small talk.\n\n"
            "After you invoke your rights, police must stop questioning. You "
            "cannot waive this right by accident — but you *can* by talking. "
            "Stop talking."
        ),
        "source_url": "https://www.ilga.gov/legislation/ilcs/documents/072500050K103-2.1.htm",
    },
]

SCENARIOS = [
    {
        "slug": "police-stop",
        "title": "I was stopped by the police in Illinois",
        "linked_statutes": ["725 ILCS 5/107-14", "725 ILCS 5/103-2.1"],
        "description_md": (
            "An officer is asking you questions on the street, has pulled you "
            "over, or has knocked on your door. You're not sure if you're free "
            "to go, what you have to answer, or whether you should consent to "
            "a search. Knowing your rights in the moment is the difference "
            "between a brief inconvenience and a criminal case."
        ),
        "walkthrough_md": (
            "## In the moment\n\n"
            "1. **Stay calm. Keep your hands visible.** Don't run. Don't argue "
            "physically. Don't make sudden moves toward pockets or compartments.\n\n"
            "2. **Ask: 'Am I being detained, or am I free to go?'** If the "
            "officer says you're free to go, calmly walk away. If you're "
            "detained, the rights below apply.\n\n"
            "3. **Identify yourself if asked.** Under Illinois law you can be "
            "asked for your name, address, and an explanation during a "
            "lawful stop. Identify yourself. If you're driving, hand over "
            "license, registration, insurance.\n\n"
            "4. **'I am exercising my right to remain silent.'** Say it once, "
            "clearly. After that, do not answer questions about where you've "
            "been, what you've been doing, where you live (beyond ID), etc.\n\n"
            "5. **'I do not consent to any search.'** Say this even if the "
            "officer asks to 'just take a look'. Your verbal non-consent is "
            "critical even if they search anyway — it preserves your ability "
            "to challenge the search later.\n\n"
            "6. **'I want a lawyer.'** Say this the moment you are taken into "
            "custody or formally questioned. Police must stop questioning you "
            "after you ask for a lawyer.\n\n"
            "7. **Do not lie. Do not consent. Do not resist physically.** Those "
            "three rules together are the safest path.\n\n"
            "## After the encounter\n\n"
            "8. **Write everything down within 24 hours.** Officer names and "
            "badge numbers (visible on uniforms), time, location, witnesses, "
            "what was said.\n\n"
            "9. **Get medical attention if you were injured**, even if the "
            "injuries seem minor. Get the records.\n\n"
            "10. **If you believe your rights were violated**, contact "
            "**Civilian Office of Police Accountability (COPA)** for Chicago "
            "complaints: copa.chicago.gov. For other Illinois departments, "
            "the **Illinois ACLU** can help: aclu-il.org.\n\n"
            "## Free legal help\n\n"
            "- **First Defense Legal Aid (24-hour Chicago hotline)**: (800) LAW-REP-4\n"
            "- **Illinois ACLU**: aclu-il.org\n"
            "- **CARPLS** for general advice: (312) 738-9200\n\n"
            "---\n\n"
            "*This is reference material, not legal advice. For your specific "
            "situation, contact a criminal-defense attorney immediately.*"
        ),
        "template_md": None,
    },
    {
        "slug": "ice-encounter",
        "title": "ICE is at my door or has detained me",
        "linked_statutes": ["5 ILCS 805/15"],
        "description_md": (
            "Immigration agents are at your home, your workplace, or have "
            "stopped you. Illinois has stronger protections than most states "
            "(the TRUST Act), but federal ICE agents still have broad powers. "
            "Knowing what to do — and what NOT to sign — matters more than "
            "almost anything else in this situation."
        ),
        "walkthrough_md": (
            "## If ICE is at your door\n\n"
            "1. **Do not open the door.** ICE agents often come without a "
            "judicial warrant. You have the right to keep the door closed.\n\n"
            "2. **Ask them to slide any paperwork under the door.** A valid "
            "**judicial warrant** is signed by a **judge**, names a specific "
            "address, and says 'U.S. District Court' or similar. A 'Warrant "
            "of Removal/Deportation' (Form I-205) or 'Warrant for Arrest of "
            "Alien' (Form I-200) is signed by an ICE officer, **not a judge** — "
            "this is not enough to enter your home without consent.\n\n"
            "3. **Say through the door: 'I do not consent to your entry.'**\n\n"
            "4. **You have the right to remain silent.** Do not answer "
            "questions about where you were born, your status, how you came to "
            "the U.S., or anything else. This applies even if they come in.\n\n"
            "5. **Do not lie. Do not produce false documents.** This makes "
            "things much worse. Silence is your right; lying is a crime.\n\n"
            "## If ICE stops you in public or at work\n\n"
            "6. **Ask if you are free to go.** If yes, leave calmly.\n\n"
            "7. **You have the right to remain silent.** *'I am exercising my "
            "right to remain silent.'*\n\n"
            "8. **You have the right to refuse to sign anything without a "
            "lawyer.** Many people are deported because they signed a "
            "voluntary-departure form they didn't understand. **Do not sign.**\n\n"
            "9. **Ask for a lawyer.** *'I want to speak with an immigration "
            "lawyer.'* Note: the right to a *court-appointed* lawyer in "
            "immigration proceedings does not exist as it does in criminal "
            "cases — but you have the right to a lawyer at your own expense, "
            "and many nonprofits provide free representation.\n\n"
            "10. **Memorize a phone number of someone who can help.** A family "
            "member, a lawyer, a friend. Phones can be taken. Memorize it.\n\n"
            "## Illinois-specific protections (TRUST Act)\n\n"
            "Local Illinois police and sheriffs **cannot**:\n\n"
            "- Hold you past your release date based on an ICE detainer alone.\n"
            "- Ask about your immigration status.\n"
            "- Help ICE with civil enforcement.\n\n"
            "Federal ICE agents are not bound by the TRUST Act but "
            "**Illinois jails and county sheriffs are**.\n\n"
            "## Make a family preparedness plan NOW (before anything happens)\n\n"
            "- Designate guardians for your children in writing.\n"
            "- Memorize a lawyer's number and a trusted person's number.\n"
            "- Keep important documents (passports, birth certificates) in a "
            "secure location accessible to a trusted person.\n"
            "- Know your A-number (alien registration) if you have one.\n\n"
            "## Free legal help in Illinois\n\n"
            "- **National Immigrant Justice Center (Chicago)**: (312) 660-1370\n"
            "- **CAIR Coalition Illinois**: cairchicago.org\n"
            "- **Resurrection Project**: resurrectionproject.org\n"
            "- **ICIRR Family Support Hotline**: (855) HELP-MY-FAMILY (435-7693)\n\n"
            "---\n\n"
            "*This is reference material, not legal advice. For your specific "
            "situation, contact an immigration attorney immediately. Do not "
            "sign anything until you do.*"
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
            statute_id = statute_ids.get(citation)
            if statute_id:
                conn.execute(
                    "INSERT OR IGNORE INTO scenario_statutes (scenario_id, statute_id) VALUES (?, ?)",
                    (scenario_id, statute_id),
                )
    conn.commit()
