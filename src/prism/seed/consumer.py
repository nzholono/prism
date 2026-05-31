"""Seed data: consumer rights & debt collection (Illinois)."""

from __future__ import annotations

import sqlite3

DOMAIN = {
    "slug": "consumer",
    "name": "Consumer Rights & Debt",
    "tier": 1,
    "summary": (
        "Your rights as a consumer in Illinois — protections against debt "
        "collectors, identity theft, deceptive sales practices, and the "
        "powerful Illinois Consumer Fraud Act."
    ),
}

STATUTES = [
    {
        "citation": "15 U.S.C. § 1692 (FDCPA)",
        "title": "Fair Debt Collection Practices Act — what debt collectors cannot do",
        "summary": (
            "The federal Fair Debt Collection Practices Act forbids debt "
            "collectors from harassing you, lying to you, calling at "
            "unreasonable hours, contacting you at work after you tell them "
            "not to, or threatening actions they can't legally take. "
            "Violations entitle you to statutory damages up to $1,000 plus "
            "actual damages plus attorney's fees."
        ),
        "body_md": (
            "**Fair Debt Collection Practices Act (15 U.S.C. § 1692)**\n\n"
            "Applies to **third-party debt collectors** (not the original "
            "creditor in most cases). Forbidden conduct includes:\n\n"
            "- Calling **before 8am or after 9pm** in your local time.\n"
            "- Calling you **at work** after you tell them your employer "
            "doesn't allow it.\n"
            "- Calling you after you send a **written cease-and-desist** "
            "letter (they may only contact you to acknowledge the letter or "
            "say they're suing).\n"
            "- **Misrepresenting** the amount, the legal status, or who they are.\n"
            "- **Threatening arrest, garnishment, lawsuit, or seizure of "
            "property they can't or don't intend to take.**\n"
            "- Talking to third parties (family, employer, neighbors) about "
            "your debt, beyond asking for your location.\n"
            "- Using obscene language or harassing repeated calls.\n\n"
            "**Verification:** Within 30 days of first contact you may demand "
            "**written verification of the debt**. The collector must stop "
            "collection until they provide it.\n\n"
            "**Damages:** Up to **$1,000 statutory damages**, plus actual "
            "damages (lost wages, emotional distress documented), plus "
            "**attorney's fees** (which is why lawyers take these on contingency)."
        ),
        "source_url": "https://www.consumerfinance.gov/rules-policy/regulations/1006/",
    },
    {
        "citation": "815 ILCS 505/2",
        "title": "Illinois Consumer Fraud and Deceptive Business Practices Act",
        "summary": (
            "One of the strongest consumer-protection statutes in the country. "
            "Forbids any deception, fraud, or unfair practice in trade or "
            "commerce — broader than common-law fraud (you don't have to prove "
            "the business intended to deceive). Damages include actual loss, "
            "punitive damages, attorney's fees, and court costs."
        ),
        "body_md": (
            "**Illinois Consumer Fraud and Deceptive Business Practices Act "
            "(815 ILCS 505)**\n\n"
            "Forbids any **deceptive act or practice**, including fraud, false "
            "promise, misrepresentation, or concealment of any material fact, "
            "in connection with the sale of any service or good in Illinois.\n\n"
            "**Why it's powerful:**\n\n"
            "- You **do not have to prove intent** — unlike common-law fraud, "
            "the business doesn't have to have meant to deceive you.\n"
            "- Covers a **huge range** of commerce: car sales, home repairs, "
            "rental scams, fake websites, deceptive billing, predatory loans, "
            "almost anything.\n"
            "- **Damages:** actual loss, plus optional **punitive damages**, "
            "plus **attorney's fees**, plus costs.\n"
            "- The **Illinois Attorney General** can also sue on behalf of "
            "consumers — and often does, recovering money back for victims.\n\n"
            "**Statute of limitations:** 3 years from when you discovered (or "
            "reasonably should have discovered) the fraud."
        ),
        "source_url": "https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2356",
    },
    {
        "citation": "740 ILCS 14 (BIPA)",
        "title": "Illinois Biometric Information Privacy Act",
        "summary": (
            "BIPA is one of the strongest biometric privacy laws in the United "
            "States. Companies that collect biometric data (fingerprints, "
            "face scans, voice prints, retinal scans) from Illinois residents "
            "must obtain WRITTEN informed consent, disclose retention "
            "schedules, and never sell the data. Violations entitle each "
            "individual to $1,000–$5,000 per violation."
        ),
        "body_md": (
            "**Illinois Biometric Information Privacy Act (740 ILCS 14)**\n\n"
            "Often overlooked by Illinois residents, BIPA is a remarkably "
            "strong privacy statute. It applies to **any private entity** "
            "(employer, app, retailer) collecting biometric identifiers from "
            "Illinois residents, including:\n\n"
            "- Fingerprints\n"
            "- Face scans (e.g., facial-recognition photo apps)\n"
            "- Voice prints\n"
            "- Retina or iris scans\n"
            "- Hand or face geometry\n\n"
            "Before collecting, the entity must:\n\n"
            "1. **Inform you in writing** what data is being collected and why.\n"
            "2. **Inform you in writing** of the specific retention schedule and "
            "destruction guidelines.\n"
            "3. **Obtain written consent** from you.\n"
            "4. **Never sell, lease, or trade** your biometric data.\n"
            "5. **Protect** the data with reasonable care.\n\n"
            "**Damages — per violation, per person:**\n\n"
            "- **$1,000** for negligent violations.\n"
            "- **$5,000** for intentional or reckless violations.\n"
            "- Plus actual damages, attorney's fees, costs.\n\n"
            "**Class actions** under BIPA have produced settlements in the "
            "hundreds of millions of dollars (Facebook paid $650M for tagging "
            "Illinois users with face-recognition without consent). This is a "
            "right you may not have known you have."
        ),
        "source_url": "https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=3004",
    },
]

SCENARIOS = [
    {
        "slug": "subscription-wont-cancel",
        "title": "A company won't let me cancel my subscription",
        "linked_statutes": ["815 ILCS 505/2"],
        "description_md": (
            "You signed up for a gym, streaming service, or 'free trial' "
            "that turned into a monthly charge. Now you're trying to cancel "
            "and the company has hidden the cancellation button, demands a "
            "phone call during business hours, or just charges you again. "
            "Illinois has laws against this — it's often a violation of the "
            "Consumer Fraud Act."
        ),
        "walkthrough_md": (
            "## What to do (in order)\n\n"
            "1. **Try to cancel through the normal channels first**, but "
            "**document every step** with screenshots. Date, time, what you "
            "clicked, what page you got to.\n\n"
            "2. **Send a written cancellation request** by email (saves the "
            "trail). Include:\n"
            "   - Your account info.\n"
            "   - Clear request: 'I am cancelling effective immediately.'\n"
            "   - Demand they stop charging and confirm in writing.\n\n"
            "3. **Dispute the charge with your credit card or bank.** This "
            "is the most effective tool:\n"
            "   - Call the number on the back of your card.\n"
            "   - Tell them you cancelled and the company keeps charging.\n"
            "   - File a chargeback for unauthorized recurring charges.\n"
            "   - Ask them to **block future charges from that merchant**.\n\n"
            "4. **If the company used 'dark patterns'** (hidden cancellation, "
            "misleading 'free trial' that auto-renews, repeated upsells in "
            "the cancel flow), it likely violates Illinois Consumer Fraud "
            "Act (815 ILCS 505/2) and the federal FTC 'click-to-cancel' "
            "rules.\n\n"
            "5. **File complaints:**\n"
            "   - **Illinois Attorney General Consumer Fraud Bureau**: "
            "(800) 386-5438 or illinoisattorneygeneral.gov/consumers.\n"
            "   - **Federal Trade Commission**: reportfraud.ftc.gov.\n"
            "   - **Better Business Bureau**: bbb.org (less powerful, but "
            "free and public, and companies often respond to BBB faster "
            "than to consumers).\n\n"
            "6. **For ongoing fraud**, consider:\n"
            "   - Closing the card and getting a new number (last resort — "
            "may break other auto-pays).\n"
            "   - **Small claims court** for refund of unauthorized charges. "
            "Under the Consumer Fraud Act you can recover the charges plus "
            "attorney's fees — making lawyers willing to take strong cases.\n\n"
            "## Free help\n\n"
            "- **Illinois AG Consumer Fraud**: (800) 386-5438\n"
            "- **FTC Consumer Protection**: (877) FTC-HELP\n"
            "- **CARPLS**: (312) 738-9200\n\n"
            "---\n\n"
            "*This is reference material, not legal advice.*"
        ),
        "template_md": (
            "## Email cancellation script\n\n"
            "```\n"
            "Subject: Cancellation of account #{{account}} — written notice\n\n"
            "To {{company billing@}}:\n\n"
            "I am writing to cancel my subscription effective immediately.\n\n"
            "Account holder: {{your name}}\n"
            "Account number / email: {{account}}\n"
            "Date of this request: {{date}}\n\n"
            "I have attempted to cancel through your website but was unable "
            "to complete the process because {{reason: 'no cancel button found' / "
            "'site looped to upsell pages' / etc.}}\n\n"
            "Please:\n"
            "1. Confirm cancellation in writing within 5 business days.\n"
            "2. Process no further charges to my account.\n"
            "3. Refund any charges made after this notice.\n\n"
            "If charges continue, I will pursue all available remedies "
            "including dispute through my card issuer, a complaint with the "
            "Illinois Attorney General's Consumer Fraud Bureau, and an action "
            "under the Illinois Consumer Fraud and Deceptive Business Practices "
            "Act (815 ILCS 505).\n\n"
            "Sincerely,\n"
            "{{your name}}\n"
            "```\n"
        ),
    },
    {
        "slug": "debt-collector-harassment",
        "title": "A debt collector is harassing me",
        "linked_statutes": ["15 U.S.C. § 1692 (FDCPA)"],
        "description_md": (
            "A collection agency is calling repeatedly, calling at night or "
            "early morning, talking to your family, threatening arrest or "
            "lawsuit, or refusing to give details about the alleged debt. "
            "Most of this is illegal — and you may be entitled to money."
        ),
        "walkthrough_md": (
            "## What to do\n\n"
            "1. **Log every contact.** Date, time, phone number, what was "
            "said, who else heard it. This log is evidence.\n\n"
            "2. **Within 30 days of first contact, demand written "
            "verification.** Send a letter (certified mail) asking for proof "
            "of the debt: original creditor name, amount, date opened, the "
            "agency's authority to collect it. They **must stop collection** "
            "until they provide verification.\n\n"
            "3. **Send a cease-and-desist letter** if you want them to stop "
            "contacting you. After receipt they may only contact you to (a) "
            "acknowledge the letter, (b) confirm specific actions like "
            "lawsuit, or (c) actually sue. **Send certified mail with return "
            "receipt.**\n\n"
            "4. **Do not acknowledge the debt or make any payment** until "
            "you've verified it's legitimate and within the statute of "
            "limitations. In Illinois the SOL on most consumer debt is **5 "
            "years for oral, 10 years for written**, but partial payment can "
            "restart the clock.\n\n"
            "5. **File complaints — the system actually works.**\n"
            "   - **Consumer Financial Protection Bureau**: consumerfinance.gov/complaint\n"
            "   - **Illinois Attorney General Consumer Fraud**: (800) 386-5438\n"
            "   - **Federal Trade Commission**: reportfraud.ftc.gov\n\n"
            "6. **Sue if violations are clear.** You can recover up to "
            "**$1,000 statutory damages** plus actual damages plus "
            "**attorney's fees**. The fee-shifting makes lawyers take these "
            "on contingency.\n\n"
            "## Free legal help\n\n"
            "- **CARPLS**: (312) 738-9200\n"
            "- **Legal Action Chicago**: legalactionchicago.org\n"
            "- **Illinois Legal Aid Online**: illinoislegalaid.org/debt\n"
            "- **CFPB complaint portal**: consumerfinance.gov/complaint\n\n"
            "---\n\n"
            "*This is reference material, not legal advice.*"
        ),
        "template_md": (
            "## Cease-and-desist / verification request\n\n"
            "```\n"
            "{{Your Name}}\n"
            "{{Your Address}}\n"
            "{{Date}}\n\n"
            "{{Collector Name}}\n"
            "{{Collector Address}}\n\n"
            "SENT CERTIFIED MAIL, RETURN RECEIPT REQUESTED\n\n"
            "Re: Account #{{account}} (alleged)\n\n"
            "To whom it may concern,\n\n"
            "Pursuant to the Fair Debt Collection Practices Act, 15 U.S.C. § "
            "1692g, I dispute the validity of the alleged debt referenced "
            "above and request that you provide written verification, "
            "including:\n\n"
            "  1. The name of the original creditor.\n"
            "  2. The original amount owed and date of last activity.\n"
            "  3. Documentation that your agency has the authority to collect.\n\n"
            "Until I receive this verification, you must cease collection "
            "activity pursuant to 15 U.S.C. § 1692g(b).\n\n"
            "Further, pursuant to 15 U.S.C. § 1692c(c), I notify you that I "
            "**refuse to pay** the alleged debt and request that you cease "
            "all further communication with me, except as permitted by that "
            "section.\n\n"
            "I am keeping a log of every communication and will pursue all "
            "available remedies, including statutory damages of up to $1,000 "
            "plus actual damages and attorney's fees, for any violations of "
            "the FDCPA.\n\n"
            "Sincerely,\n"
            "{{Your Name}}\n"
            "```\n"
        ),
    },
    {
        "slug": "biometric-collected-without-consent",
        "title": "A company collected my fingerprint or face scan without consent",
        "linked_statutes": ["740 ILCS 14 (BIPA)"],
        "description_md": (
            "Your employer is using a fingerprint scanner to clock you in/out. "
            "An app you used asked for face scans without explaining why. A "
            "retail store has a face-recognition system. If you're an Illinois "
            "resident and you did not give written informed consent, you may "
            "be entitled to $1,000–$5,000 per violation under BIPA."
        ),
        "walkthrough_md": (
            "## What to do\n\n"
            "1. **Confirm the basics.** Are you an Illinois resident? Did a "
            "private entity (employer, app, retailer) collect a biometric "
            "identifier (fingerprint, face scan, voice print, retina/iris, "
            "hand geometry)? Did they obtain your **written informed consent** "
            "first, disclosing retention and destruction?\n\n"
            "2. **Save evidence.** Screenshots of consent screens (or the "
            "absence of one). Pay stubs showing fingerprint clock-ins. Apps' "
            "privacy policies. Photos of the biometric device.\n\n"
            "3. **Do not delete the app** if you're considering action — that "
            "may erase evidence of how the data was collected and described.\n\n"
            "4. **Contact a BIPA-experienced lawyer.** This is one of the "
            "hottest class-action areas in Illinois law. Many firms take "
            "these cases on contingency. A few worth contacting:\n"
            "   - Edelson PC (Chicago)\n"
            "   - Stephan Zouras\n"
            "   - Loevy & Loevy\n"
            "(Not endorsements — just firms with BIPA experience.)\n\n"
            "5. **Don't sign anything from the company** without showing it "
            "to a lawyer first. Companies sometimes try to get retroactive "
            "consent or arbitration agreements.\n\n"
            "6. **Damages can be substantial.** Each negligent violation: "
            "$1,000. Each intentional violation: $5,000. Class actions have "
            "produced settlements in the **hundreds of millions** (Facebook "
            "paid $650M to Illinois users for face-tagging photos without "
            "consent).\n\n"
            "## Free legal help\n\n"
            "- **Illinois Attorney General Consumer Protection**: (800) 386-5438\n"
            "- **CARPLS**: (312) 738-9200\n"
            "- **Electronic Frontier Foundation** (general resources): eff.org\n\n"
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
            statute_id = statute_ids.get(citation)
            if statute_id:
                conn.execute(
                    "INSERT OR IGNORE INTO scenario_statutes (scenario_id, statute_id) VALUES (?, ?)",
                    (scenario_id, statute_id),
                )
    conn.commit()
