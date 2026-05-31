"""Seed data: campus / student rights (Title IX, FERPA, ADA).

Specifically targeted at DePaul and other Illinois colleges.
"""

from __future__ import annotations

import sqlite3

DOMAIN = {
    "slug": "campus",
    "name": "Campus / Student Rights",
    "tier": 2,
    "summary": (
        "Your rights at DePaul and other Illinois colleges. Title IX (sex "
        "discrimination and harassment), FERPA (your education records), ADA "
        "(disability accommodations), and how to appeal an academic decision."
    ),
}

STATUTES = [
    {
        "citation": "20 U.S.C. § 1232g (FERPA)",
        "title": "Family Educational Rights and Privacy Act",
        "summary": (
            "Your school cannot share your education records (grades, "
            "transcripts, disciplinary records, attendance) with most third "
            "parties without your written consent. You also have the right to "
            "inspect your own records and request corrections."
        ),
        "body_md": (
            "**20 U.S.C. § 1232g — FERPA**\n\n"
            "Applies to every school that receives federal funding (which is "
            "almost all of them, including DePaul).\n\n"
            "**Your rights:**\n\n"
            "- Inspect your own education records.\n"
            "- Request corrections to inaccurate or misleading entries.\n"
            "- Control whom the school shares your records with (with limited "
            "exceptions like accreditation auditors, court orders, health "
            "emergencies).\n"
            "- Once you turn 18 or enter college (whichever first), rights "
            "transfer from your parents to you. **Your school cannot share "
            "your grades or status with your parents without your consent.**\n\n"
            "**Directory information exception:** schools may publish "
            "'directory information' (name, address, major, dates of "
            "attendance) unless you opt out in writing. At DePaul you opt out "
            "through Campus Connection.\n\n"
            "**To file a complaint:** Family Policy Compliance Office, "
            "U.S. Department of Education — studentprivacy.ed.gov."
        ),
        "source_url": "https://studentprivacy.ed.gov/ferpa",
    },
    {
        "citation": "20 U.S.C. § 1681 (Title IX)",
        "title": "Title IX — sex discrimination & sexual harassment in education",
        "summary": (
            "Federal law forbids sex discrimination in any educational program "
            "receiving federal funds — including DePaul. Covers sexual "
            "harassment, sexual assault, pregnancy discrimination, gender "
            "identity discrimination, and retaliation for reporting any of these."
        ),
        "body_md": (
            "**20 U.S.C. § 1681 — Title IX**\n\n"
            "Title IX requires every school to have a designated **Title IX "
            "Coordinator**. At DePaul: see depaul.edu/title-ix for current "
            "contact information.\n\n"
            "**What's covered:**\n\n"
            "- Sex- or gender-based discrimination in admissions, grades, "
            "scholarships, athletics, housing.\n"
            "- Sexual harassment by students, faculty, or staff.\n"
            "- Sexual assault.\n"
            "- Pregnancy and parenting discrimination (you may not be penalized "
            "for pregnancy-related absences).\n"
            "- **Retaliation** against anyone who reports a Title IX violation.\n\n"
            "**Your options as a complainant:**\n\n"
            "- **Supportive measures** — academic accommodations, no-contact "
            "orders, schedule changes — available even if you don't file a "
            "formal complaint.\n"
            "- **Formal grievance process** — investigation, live hearing with "
            "cross-examination (under current regs), written outcome.\n"
            "- **Confidential resources** — campus counseling, victim "
            "advocates (typically don't trigger investigation).\n"
            "- **Outside complaint** — U.S. Department of Education Office for "
            "Civil Rights, ocr@ed.gov."
        ),
        "source_url": "https://www.ed.gov/laws-and-policy/civil-rights-laws/title-ix-and-sex-discrimination",
    },
    {
        "citation": "42 U.S.C. § 12182 (ADA Title III)",
        "title": "ADA — academic accommodations for disabilities",
        "summary": (
            "Public and private colleges must provide reasonable accommodations "
            "for students with disabilities — extended test time, note-takers, "
            "accessible housing, sign language interpreters, course "
            "substitutions in limited cases. The student must register with the "
            "disability services office and provide documentation."
        ),
        "body_md": (
            "**Americans with Disabilities Act — Title III + Section 504 of the "
            "Rehabilitation Act**\n\n"
            "At DePaul, accommodations go through the **Center for Students "
            "with Disabilities (CSD)**: csd.depaul.edu.\n\n"
            "**Eligible disabilities include:**\n\n"
            "- Learning disabilities (dyslexia, ADHD).\n"
            "- Mental health conditions (depression, anxiety, bipolar, PTSD).\n"
            "- Physical disabilities.\n"
            "- Chronic illness (diabetes, autoimmune, long COVID).\n"
            "- Temporary disabilities (broken arm during exam season).\n\n"
            "**Common accommodations:**\n\n"
            "- Extended time on exams (1.5x or 2x).\n"
            "- Quiet/distraction-reduced testing room.\n"
            "- Note-taking assistance or recording lectures.\n"
            "- Flexibility with attendance for medical reasons.\n"
            "- Extended deadlines (case-by-case).\n"
            "- Accessible classroom location.\n\n"
            "**You generally need documentation** (recent psych eval, doctor's "
            "letter). DePaul's CSD can help you understand what's needed.\n\n"
            "**Retaliation is illegal.** A professor cannot grade you down for "
            "using your approved accommodations.\n\n"
            "**Complaint route:** U.S. Department of Education OCR, ocr@ed.gov."
        ),
        "source_url": "https://www.ada.gov/topics/postsecondary/",
    },
]

SCENARIOS = [
    {
        "slug": "title-ix-incident",
        "title": "I experienced sexual harassment or assault on campus",
        "linked_statutes": ["20 U.S.C. § 1681 (Title IX)"],
        "description_md": (
            "Something happened on campus — by a student, professor, staff "
            "member, or even at an off-campus event tied to school activities. "
            "You have options. None of them require you to make decisions all "
            "at once. The single most important first step is talking to "
            "someone confidential before you talk to anyone official."
        ),
        "walkthrough_md": (
            "## First — your safety\n\n"
            "1. **If you're in immediate danger, call 911.** If you're hurt, "
            "go to an ER. **Don't shower, change clothes, or wash anything** "
            "if there's any chance you might want to preserve evidence — but "
            "do whatever helps you feel safe right now. The investigation can "
            "happen later.\n\n"
            "## Talk to someone confidential FIRST\n\n"
            "2. **Confidential resources** at DePaul (and most colleges) don't "
            "trigger a mandatory report:\n"
            "   - Campus counseling (University Counseling Services).\n"
            "   - On-campus victim advocates if available.\n"
            "   - Chaplains and religious counselors.\n"
            "   - Off-campus: **RAINN** (1-800-656-HOPE) or **Resilience** "
            "(Chicago, resiliencechicago.org).\n\n"
            "   These let you process what happened **and** learn your "
            "options without committing to anything.\n\n"
            "## Get supportive measures (no investigation needed)\n\n"
            "3. **The Title IX Coordinator can put supportive measures in "
            "place without a formal complaint:**\n"
            "   - No-contact order between you and the other person.\n"
            "   - Schedule changes so you don't share classes.\n"
            "   - Housing reassignment.\n"
            "   - Academic accommodations (deadline extensions, exam re-takes).\n"
            "   - Counseling referrals.\n\n"
            "## Decide about a formal complaint at your pace\n\n"
            "4. **A formal Title IX complaint** triggers an investigation, "
            "interviews, and a hearing. The process is exhausting. You don't "
            "have to make this decision quickly. You can:\n"
            "   - File now.\n"
            "   - File later (no firm deadline, though earlier is generally "
            "easier evidence-wise).\n"
            "   - Decide not to file and just use supportive measures.\n\n"
            "## If you file\n\n"
            "5. **You have the right to:**\n"
            "   - An advisor of your choice (can be a lawyer, friend, "
            "advocate). Free advisors are available at many schools.\n"
            "   - See evidence collected.\n"
            "   - Cross-examination at the live hearing (through your advisor).\n"
            "   - Written notice of the outcome.\n"
            "   - Appeal.\n\n"
            "## You can also report outside the school\n\n"
            "6. **Criminal charges** are separate from the Title IX process. "
            "You can pursue either, both, or neither. Chicago Police, the "
            "Cook County State's Attorney, and federal authorities each have "
            "jurisdiction depending on the incident.\n\n"
            "7. **Federal complaint** if you think your school mishandled the "
            "Title IX process: U.S. Department of Education Office for Civil "
            "Rights, ocr@ed.gov.\n\n"
            "## Resources\n\n"
            "- **RAINN** (24/7 confidential): 1-800-656-HOPE (4673)\n"
            "- **Resilience** (Chicago): resiliencechicago.org\n"
            "- **DePaul Title IX office**: depaul.edu/title-ix\n"
            "- **DePaul University Counseling Services**: studentaffairs.depaul.edu/ucs\n"
            "- **Know Your IX** (national advocacy): knowyourix.org\n\n"
            "---\n\n"
            "*This is reference material, not legal advice. Talk to a confidential "
            "advocate before talking to anyone official.*"
        ),
        "template_md": None,
    },
    {
        "slug": "academic-integrity-charge",
        "title": "I'm accused of cheating or plagiarism",
        "linked_statutes": ["20 U.S.C. § 1232g (FERPA)"],
        "description_md": (
            "You got an email or letter saying you've been accused of an "
            "academic integrity violation. Maybe it's a Turnitin match you "
            "can explain. Maybe it's a misunderstanding about collaboration "
            "rules. Maybe it's a wrong accusation. The hearing process "
            "matters — failure to engage well at this stage can result in "
            "suspension, expulsion, or a transcript notation that follows "
            "you for years."
        ),
        "walkthrough_md": (
            "## What to do — in order\n\n"
            "1. **Don't reply with an emotional first message.** Don't "
            "admit, deny, or explain in detail until you've read the policy "
            "and gathered evidence.\n\n"
            "2. **Acknowledge receipt** within whatever deadline they give "
            "(usually short — 3-5 business days). Something like: *'I "
            "acknowledge receipt of this notice and will be responding by "
            "[date]. Please send me a copy of the academic integrity policy "
            "and the specific evidence the charge is based on.'*\n\n"
            "3. **Read the academic integrity policy carefully.** At DePaul: "
            "go.depaul.edu/academicintegrity. Note:\n"
            "   - The specific rule you're alleged to have violated.\n"
            "   - The process (informal resolution, formal hearing, appeal).\n"
            "   - Possible sanctions.\n"
            "   - Your right to bring an advisor.\n"
            "   - Deadlines at each stage.\n\n"
            "4. **Get an advisor.** Almost every college process allows you "
            "an advisor, sometimes including a lawyer. Free options:\n"
            "   - Student government legal advisor (if your school has one).\n"
            "   - Trusted faculty member outside the course.\n"
            "   - Ombudsperson (confidential informal resolution).\n"
            "   - Local pro bono legal clinic.\n\n"
            "5. **Gather evidence.** Drafts with metadata, your search "
            "history during the assignment, communications with the "
            "professor about expectations, sources you used, your "
            "interpretation of what was permitted vs not.\n\n"
            "6. **Understand what they're actually alleging.** Plagiarism? "
            "Improper collaboration? Unauthorized resources? Each has "
            "different defenses.\n\n"
            "7. **Informal resolution first** (if available). Often a "
            "conversation with the professor and a department chair, where "
            "you can explain context. Many cases end here with a learning "
            "agreement or warning. If you accept this resolution, **get the "
            "exact terms in writing** — including whether it goes on your "
            "permanent record.\n\n"
            "8. **Formal hearing** (if it goes there). You'll typically:\n"
            "   - Receive a copy of all evidence in advance.\n"
            "   - Submit a written response.\n"
            "   - Appear at a hearing with the panel and the professor.\n"
            "   - Have your advisor present (often silent — they advise you, "
            "you speak).\n"
            "   - Receive a written outcome with appeal rights.\n\n"
            "9. **Tone matters.** Be respectful, factual, organized. Don't "
            "attack the professor or the process — make your case on the "
            "merits.\n\n"
            "10. **Appeal if needed.** Grounds usually include: procedural "
            "error, new evidence, sanction inconsistent with policy. "
            "Deadlines are short (often 5-10 days).\n\n"
            "11. **Consequences depend on outcome.** A finding of "
            "responsibility can affect: GPA, graduation, professional "
            "school admissions (law/med schools ask), scholarships, "
            "professional licensing, immigration status (for F-1 students "
            "especially — talk to OISS).\n\n"
            "## What rarely works\n\n"
            "- 'I didn't know it was against the rules.' (Sometimes "
            "mitigating, rarely exonerating.)\n"
            "- 'Everyone does it.'\n"
            "- 'My grade should be lowered to a [X] instead.' (Penalty "
            "negotiation works better after responsibility is determined.)\n"
            "- Lying. If discovered, this is its own violation and far worse.\n\n"
            "## Free help\n\n"
            "- **DePaul Office of the Ombudsperson**: depaul.edu/ombuds\n"
            "- **DePaul Student Conduct office**: depaul.edu/dean-of-students\n"
            "- **CARPLS general legal advice**: (312) 738-9200\n"
            "- For F-1 students with possible immigration impact: "
            "**DePaul OISS** + immigration attorney consultation immediately.\n\n"
            "---\n\n"
            "*This is reference material, not legal advice.*"
        ),
        "template_md": None,
    },
    {
        "slug": "grade-dispute",
        "title": "I want to dispute a grade I think is unfair",
        "linked_statutes": [],
        "description_md": (
            "You got a grade you believe is wrong — calculation error, "
            "professor missed a submission, biased grading, didn't follow the "
            "syllabus. Most Illinois colleges have a formal academic-appeal "
            "process. Knowing the right order to escalate matters."
        ),
        "walkthrough_md": (
            "## What to do\n\n"
            "1. **Re-read the syllabus.** Does the grade match the stated "
            "grading policy? If the professor didn't follow their own "
            "published policy, that's the strongest type of appeal.\n\n"
            "2. **Email the professor first — politely.** Calm, factual: 'I "
            "received [grade]. Per the syllabus [section], I expected "
            "[different grade] because [reason]. Can we discuss?' Often this "
            "resolves at this step.\n\n"
            "3. **Make office hours.** Show your work. Bring the assignment "
            "and the syllabus. Ask the professor to walk you through the "
            "specific points lost.\n\n"
            "4. **Escalate to the department chair.** If the professor won't "
            "discuss or won't change, write a formal email to the chair. "
            "Include: the syllabus excerpt, your work, the professor's "
            "explanation (if any), and what outcome you're requesting.\n\n"
            "5. **File a formal academic appeal.** Each DePaul college has a "
            "documented process — find it on the college's website ('academic "
            "appeals' or 'grade appeals'). Common requirements:\n"
            "   - Specific basis: calculation error, syllabus violation, "
            "discrimination, accommodation not honored.\n"
            "   - Deadline (often within 30 days of the grade posting).\n"
            "   - Written statement of what happened and what you want.\n"
            "   - Supporting documentation.\n\n"
            "6. **If the issue is discrimination or accommodation-related**, "
            "loop in:\n"
            "   - Title IX office (if sex/gender-based).\n"
            "   - Office of Diversity, Equity & Inclusion.\n"
            "   - Center for Students with Disabilities (if accommodation "
            "wasn't honored).\n\n"
            "7. **Document everything.** Save the syllabus, all emails, the "
            "graded work, any witnesses. Date and time matter — keep a log.\n\n"
            "## What rarely works\n\n"
            "- 'I worked really hard on this' (effort isn't graded; output is).\n"
            "- 'I need this grade for [scholarship / GPA / parent expectation]'.\n"
            "- Going around the professor to the dean without giving them a chance to fix it first.\n\n"
            "## Resources\n\n"
            "- Your college's academic appeals office (search your college's website).\n"
            "- DePaul Ombudsperson — confidential informal resolution.\n"
            "- **Student Legal Services** if available at your school.\n\n"
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
