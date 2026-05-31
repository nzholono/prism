"""Seed data: employment rights domain (Illinois).

Coverage: wage theft, discrimination, wrongful termination.
"""

from __future__ import annotations

import sqlite3

DOMAIN = {
    "slug": "employment",
    "name": "Employment",
    "tier": 1,
    "summary": (
        "Your rights as an employee in Illinois — minimum wage, overtime, paid "
        "sick leave, protection from discrimination, what to do when you're "
        "underpaid or fired in retaliation."
    ),
}

STATUTES = [
    {
        "citation": "820 ILCS 105/4",
        "title": "Illinois Minimum Wage Law — current minimum wage",
        "summary": (
            "The Illinois minimum wage is $15.00/hour as of January 1, 2025. "
            "Chicago and Cook County have higher minimums. Tipped employees have "
            "a separate (lower) tipped wage but the employer must make up the "
            "difference if tips don't reach the standard minimum."
        ),
        "body_md": (
            "**820 ILCS 105/4 — Illinois Minimum Wage Law**\n\n"
            "Statewide minimum wage (as of Jan 1, 2025): **$15.00 per hour**.\n\n"
            "Workers under 18 with fewer than 650 hours of work in a calendar "
            "year may be paid a lower training wage.\n\n"
            "**Tipped employees:** the tipped wage is 60% of the standard minimum "
            "(currently $9.00/hour). The employer must make up the difference if "
            "the tipped employee's total pay (tips + tipped wage) does not reach "
            "the full minimum wage for hours worked.\n\n"
            "**Local minimums (override the state floor where higher):**\n\n"
            "- City of Chicago: ~$16.20/hour for employers with 4+ employees (2024 figure; check current).\n"
            "- Cook County (outside Chicago): generally $14.05/hour (2024 figure).\n\n"
            "**Recovery:** Under the Wage Payment and Collection Act (820 ILCS 115), "
            "an employee who recovers unpaid wages is entitled to **damages of 5% "
            "of the underpayment per month**, plus attorney's fees and costs."
        ),
        "source_url": "https://labor.illinois.gov/laws-rules/fls/minimum-wage.html",
    },
    {
        "citation": "820 ILCS 115/14",
        "title": "Illinois Wage Payment and Collection Act — penalty for unpaid wages",
        "summary": (
            "If your employer doesn't pay you wages you've earned, you can recover "
            "the underpayment plus 5% per month in damages, plus attorney's fees. "
            "You can file a complaint with the Illinois Department of Labor "
            "(no lawyer needed) or sue directly."
        ),
        "body_md": (
            "**820 ILCS 115/14 — Penalty for unpaid wages**\n\n"
            "An employee whose wages are not paid when due may file:\n\n"
            "1. **A complaint with the Illinois Department of Labor** at "
            "labor.illinois.gov — free, no lawyer required. The Department "
            "investigates and can order the employer to pay.\n\n"
            "2. **A lawsuit** in state court. Recoverable amounts:\n"
            "   - The unpaid wages.\n"
            "   - **5% per month** of the underpayment as damages.\n"
            "   - Court costs.\n"
            "   - Reasonable attorney's fees.\n\n"
            "**Statute of limitations:** 10 years for written contracts, 5 years "
            "for oral contracts.\n\n"
            "**Final paycheck rule:** When you leave a job (quit or fired), your "
            "final paycheck is due on or before the next regular payday. Late "
            "final paychecks are wage theft under this statute."
        ),
        "source_url": "https://www.ilga.gov/legislation/ilcs/ilcs3.asp?ActID=2402",
    },
    {
        "citation": "775 ILCS 5/1-103",
        "title": "Illinois Human Rights Act — protected classes",
        "summary": (
            "Illinois law forbids employment discrimination based on race, color, "
            "religion, sex, national origin, ancestry, age (40+), order of "
            "protection status, marital status, sexual orientation, gender "
            "identity, pregnancy, disability, military status, unfavorable "
            "discharge, citizenship status, work authorization status, arrest "
            "record, and conviction record (with limits). The Illinois list is "
            "broader than federal law."
        ),
        "body_md": (
            "**775 ILCS 5/1-103 — Illinois Human Rights Act protected categories**\n\n"
            "Discrimination is illegal in Illinois employment based on:\n\n"
            "- Race, color, national origin, ancestry\n"
            "- Religion\n"
            "- Sex (including pregnancy)\n"
            "- Sexual orientation, gender identity, gender expression\n"
            "- Age (40 and over)\n"
            "- Disability\n"
            "- Marital status\n"
            "- Citizenship status, work-authorization status\n"
            "- Military status, unfavorable military discharge\n"
            "- Order of protection status\n"
            "- Arrest record (limited use), conviction record (limited use)\n"
            "- Source of income (housing, also covered)\n\n"
            "**Where to file:** Illinois Department of Human Rights (IDHR). "
            "Filing deadline: **300 days** from the discriminatory act. Free, "
            "no lawyer required (though one helps).\n\n"
            "**Possible remedies:** back pay, reinstatement, front pay, emotional "
            "distress damages, attorney's fees, and (in some cases) civil "
            "penalties."
        ),
        "source_url": "https://www2.illinois.gov/dhr/Pages/default.aspx",
    },
    {
        "citation": "820 ILCS 192/15",
        "title": "Illinois Paid Leave for All Workers Act",
        "summary": (
            "As of January 1, 2024, most Illinois employees earn at least 40 "
            "hours of paid leave per year, accrued at one hour per 40 hours "
            "worked. The leave can be used for any reason, with notice if "
            "foreseeable. Chicago and Cook County have separate, more generous "
            "paid sick leave ordinances."
        ),
        "body_md": (
            "**820 ILCS 192/15 — Paid Leave for All Workers Act**\n\n"
            "Effective January 1, 2024:\n\n"
            "- Almost all Illinois employees accrue paid leave at **1 hour per 40 "
            "hours worked**, up to at least **40 hours per year**.\n"
            "- Employees may use the leave for **any reason** — vacation, illness, "
            "caregiving, mental health, voting, anything.\n"
            "- Employers may require up to **7 calendar days advance notice** if "
            "the need is foreseeable. For unforeseeable needs (e.g., sudden "
            "illness), notice must be given as soon as practicable.\n"
            "- Employees can start using leave after **90 days** of employment.\n\n"
            "**Local stronger laws apply.** Chicago and Cook County paid sick "
            "leave ordinances are more generous and continue to apply for "
            "workers covered by them.\n\n"
            "**Retaliation prohibited.** An employer cannot fire, demote, or "
            "punish you for using or requesting paid leave."
        ),
        "source_url": "https://labor.illinois.gov/laws-rules/paidleave.html",
    },
]

SCENARIOS = [
    {
        "slug": "non-compete-agreement",
        "title": "My employer wants me to sign a non-compete agreement",
        "linked_statutes": [],
        "description_md": (
            "You've been offered a job (or are already in one) and the "
            "employer is asking you to sign a non-compete agreement — a "
            "promise not to work for competitors for some period after you "
            "leave. Illinois passed strong limits on these in 2022. Most "
            "non-competes in Illinois are now invalid by law."
        ),
        "walkthrough_md": (
            "## Quick answer\n\n"
            "As of January 1, 2022, the **Illinois Freedom to Work Act** "
            "(820 ILCS 90) makes most non-compete agreements unenforceable. "
            "Specifically:\n\n"
            "- **Non-competes** are void if you earn **less than $75,000/year** "
            "(threshold rises with inflation — currently around $80K+).\n"
            "- **Non-solicitation agreements** are void if you earn less "
            "than $45,000/year.\n"
            "- For higher earners, the employer must give you at least "
            "**14 calendar days to review** the agreement and **advise you "
            "in writing** to consult a lawyer.\n"
            "- The agreement must be supported by **adequate consideration** — "
            "usually at least 2 years of continued employment OR a "
            "meaningful bonus/raise.\n\n"
            "## What to do\n\n"
            "1. **Don't sign it on the spot.** Even if the employer pressures "
            "you, the law requires they give you 14 days to review for "
            "high-earner agreements.\n\n"
            "2. **Check the income threshold.** If you'll earn under "
            "$75K/year and they hand you a non-compete, the entire "
            "non-compete is void. Sign or don't sign — they can't enforce it.\n\n"
            "3. **Read the geographic scope.** Even valid non-competes must "
            "be 'reasonable' in scope. 'You can't work for any tech "
            "company anywhere in the world for 5 years' is not enforceable.\n\n"
            "4. **Read the time period.** Most Illinois courts won't enforce "
            "more than 1-2 years.\n\n"
            "5. **Note the activities restricted.** A non-compete for the "
            "exact role you do is more enforceable than one that bars all "
            "industry employment.\n\n"
            "6. **Negotiate** if the agreement seems overbroad. Most "
            "employers will modify scope, time, geography, or activities. "
            "Ask for:\n"
            "   - Shorter duration (6-12 months).\n"
            "   - Narrower geography (city/state, not nationwide).\n"
            "   - Activities limited to your specific role.\n"
            "   - Pay during the restricted period (sometimes called "
            "'garden leave').\n\n"
            "7. **For technical employees**, ask about which side projects, "
            "consulting, open-source work are covered. Get carveouts in writing.\n\n"
            "8. **If you're being asked to sign as a condition of getting an "
            "offer you already negotiated**, push back. The change in terms is "
            "negotiable.\n\n"
            "9. **If you've already left a job under a non-compete and you're "
            "facing enforcement**, talk to an employment lawyer immediately. "
            "Illinois courts often refuse to enforce these even when valid "
            "on paper.\n\n"
            "## Free legal help\n\n"
            "- **Illinois Attorney General Workplace Rights Bureau**: (844) 740-5076\n"
            "- **Chicago Bar Association referral service**: (312) 554-2001\n"
            "- **Illinois State Bar Association lawyer referral**: (800) 922-8757\n\n"
            "---\n\n"
            "*This is reference material, not legal advice.*"
        ),
        "template_md": None,
    },
    {
        "slug": "unpaid-wages",
        "title": "My employer didn't pay me for hours I worked",
        "linked_statutes": ["820 ILCS 105/4", "820 ILCS 115/14"],
        "description_md": (
            "You worked hours your employer hasn't paid you for — final paycheck "
            "missing, off-the-clock work demanded, paid below minimum wage, "
            "overtime not paid, or hours 'shaved' from your timesheet. This is "
            "wage theft, and Illinois law has strong remedies."
        ),
        "walkthrough_md": (
            "## What to do\n\n"
            "1. **Document the hours.** Pull your own records: timesheets, "
            "schedules, pay stubs, photos of clock-in screens, text messages "
            "from your boss telling you to come in. Calendar entries help.\n\n"
            "2. **Calculate what you're owed.** Hours × rate, plus overtime "
            "(1.5x for hours over 40 in a workweek under federal FLSA). Use the "
            "**higher** of the federal, state, or local minimum wage.\n\n"
            "3. **Ask the employer in writing first.** A written request creates "
            "a paper trail. Be calm and specific: \"On [dates] I worked [hours] "
            "at [rate]. Pay shows [amount]. Please correct by [date].\"\n\n"
            "4. **File a complaint with the Illinois Department of Labor (IDOL).** "
            "Online at labor.illinois.gov. **Free, no lawyer needed.** IDOL "
            "investigates and can order payment.\n\n"
            "5. **For overtime claims**, you can also file with the federal "
            "Department of Labor Wage and Hour Division. Federal claims have a "
            "**2-year statute of limitations** (3 if willful).\n\n"
            "6. **You can sue directly** in state court. Under 820 ILCS 115/14, "
            "you recover the unpaid wages **plus 5% per month** in damages, "
            "**plus attorney's fees**. The fee-shifting makes lawyers willing to "
            "take these cases on contingency.\n\n"
            "7. **Retaliation is illegal.** If your employer fires or demotes "
            "you for raising a wage claim, that's a separate violation with its "
            "own damages.\n\n"
            "## Free legal help\n\n"
            "- **Illinois Department of Labor**: (312) 793-2800 or labor.illinois.gov\n"
            "- **Raise the Floor Alliance** (worker-center coalition): raisetheflooralliance.org\n"
            "- **Chicago Workers' Collaborative**: chicagoworkers.org\n"
            "- **CARPLS** for general legal advice: (312) 738-9200\n\n"
            "---\n\n"
            "*This is reference material, not legal advice. For your specific "
            "situation, contact a licensed Illinois attorney or one of the free "
            "resources above.*"
        ),
        "template_md": (
            "## Wage demand letter template\n\n"
            "```\n"
            "{{Your Name}}\n"
            "{{Your Address}}\n"
            "{{City, IL ZIP}}\n"
            "{{Date}}\n\n"
            "{{Employer Name}}\n"
            "{{Address}}\n\n"
            "Re: Unpaid wages\n\n"
            "Dear {{Manager / HR}},\n\n"
            "I am writing to request payment of wages owed to me for work "
            "performed between {{start date}} and {{end date}}.\n\n"
            "Hours worked: {{total hours}}\n"
            "Rate of pay: ${{rate}}/hour\n"
            "Amount owed: ${{amount}}\n"
            "Amount paid: ${{amount paid, if any}}\n"
            "**Balance due: ${{balance}}**\n\n"
            "Please remit the balance by {{date — 14 days out}}. If I do not "
            "receive payment, I will file a complaint with the Illinois "
            "Department of Labor and may pursue a claim under 820 ILCS 115/14, "
            "which provides for the unpaid wages plus damages of 5% per month "
            "and attorney's fees.\n\n"
            "Sincerely,\n"
            "{{Your Name}}\n"
            "```\n"
        ),
    },
    {
        "slug": "fired-for-discrimination",
        "title": "I was fired (or demoted) and I think it was discrimination",
        "linked_statutes": ["775 ILCS 5/1-103"],
        "description_md": (
            "You were fired, demoted, denied a promotion, or harassed at work, "
            "and you believe it was because of your race, sex, age, disability, "
            "national origin, sexual orientation, gender identity, religion, "
            "pregnancy, or another protected characteristic. Illinois has a "
            "broader list of protected classes than federal law, and a free "
            "agency to investigate."
        ),
        "walkthrough_md": (
            "## What to do\n\n"
            "1. **Write down what happened — now, while it's fresh.** Dates, "
            "specific words said, who was present, what your performance was "
            "like, who replaced you (if you were fired). Save it somewhere your "
            "employer cannot access (personal email, cloud).\n\n"
            "2. **Mind the deadline.** In Illinois, you have **300 days** from "
            "the discriminatory act to file with the Illinois Department of "
            "Human Rights (IDHR). Federal EEOC filings have the same deadline "
            "in Illinois. **Do not wait.**\n\n"
            "3. **Preserve evidence.** Emails, performance reviews, written "
            "warnings or commendations, comparison data (how were similar "
            "employees treated?), texts, the company handbook. Forward "
            "work-account emails to your personal email **only if your handbook "
            "doesn't forbid it** — check first.\n\n"
            "4. **File a charge with IDHR.** Online at illinois.gov/dhr. "
            "**Free, no lawyer required** (though a lawyer often helps). IDHR "
            "investigates and can attempt mediation. After investigation you "
            "may get a 'right to sue' letter allowing court action.\n\n"
            "5. **For Title VII (federal) claims**, you can also file with the "
            "EEOC at eeoc.gov. In Illinois, filing with IDHR usually triggers "
            "dual-filing automatically.\n\n"
            "6. **Consult an employment lawyer** before you do anything that "
            "could be characterized as quitting. Many take strong cases on "
            "contingency — no upfront cost. Resignation in protest is sometimes "
            "treated as 'constructive discharge' but the bar is high.\n\n"
            "7. **Do not sign a separation agreement without a lawyer reading "
            "it first.** Severance offers often include a release of all claims. "
            "Once signed, your discrimination case may be gone.\n\n"
            "## Free legal help\n\n"
            "- **Illinois Department of Human Rights**: (312) 814-6200 or "
            "illinois.gov/dhr — free intake, free investigation.\n"
            "- **EEOC Chicago District Office**: (800) 669-4000.\n"
            "- **Chicago Lawyers' Committee for Civil Rights**: clccrul.org.\n"
            "- **Equip for Equality** (disability discrimination): equipforequality.org.\n\n"
            "---\n\n"
            "*This is reference material, not legal advice. For your specific "
            "situation, contact a licensed Illinois attorney or one of the free "
            "resources above. The deadlines are strict — don't delay.*"
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
