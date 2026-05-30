---
name: add-scenario
description: Add a new legal scenario to the Prism database. Use when the user wants to extend Prism with coverage of a new everyday legal situation (e.g., "add a scenario for getting your car booted in Chicago"). Gathers Illinois-specific statutes, drafts the walkthrough, generates a template letter if appropriate, and links everything via the REST API or directly in the seed module.
---

# Add Scenario to Prism

You are helping the user grow Prism's curated knowledge base. The goal is **one well-researched scenario**, not a sprawl of half-built ones.

## Process

1. **Clarify the situation.** Ask the user to describe the scenario in one or two sentences. Examples:
   - "Roommate refuses to pay their share of rent."
   - "Got a parking ticket that I think is wrong."
   - "Employer is requiring fingerprint scans without consent."

2. **Identify the domain.** Match the scenario to an existing domain (`tenant`, `employment`, `consumer`, `police`, `traffic`, `bipa`, etc.). If none fits, propose creating a new domain and confirm with the user before proceeding.

3. **Find applicable Illinois statutes.** Search for the specific Illinois Compiled Statutes (ILCS) or Chicago Municipal Code sections that apply. For each statute capture:
   - Citation in standard form (e.g., `765 ILCS 710/1`)
   - Title
   - Plain-English summary (1–3 sentences a non-lawyer can read)
   - Source URL (ilga.gov for state, codelibrary.amlegal.com for Chicago)

4. **Draft the walkthrough.** A numbered, step-by-step action list. Be concrete. Each step should be doable in one sitting. Include:
   - Deadlines (statutes of limitations, response windows)
   - Documents to gather
   - Whom to contact (and free legal aid resources)
   - When to escalate (small claims, complaint to AG, etc.)

5. **Optional: template letter.** If the scenario benefits from a written demand or complaint (most tenant/consumer/employment cases do), draft a template letter in markdown. Use `{{placeholder}}` syntax for fields the user fills in.

6. **Persist it.** Either:
   - **Via API** (preferred if the user has Pharos running): `POST /domains/{slug}/scenarios` with the structured payload, then `POST /scenarios/{slug}/statutes` to link.
   - **Via seed module**: add a Python module under `src/prism/seed/` that re-inserts the data on first run.

7. **Verify.** Run `uv run prism-cli rights <domain> <new-scenario-slug>` and confirm the output reads well.

## Conventions

- Slugs are lowercase-hyphenated (`deposit-not-returned`, not `Deposit Not Returned`).
- Citations follow Bluebook-lite: `<title> <code> <chapter>/<section>` for ILCS, `Chi. Mun. Code <chapter>-<section>` for Chicago.
- Walkthroughs assume the reader has no legal background. Define every term the first time you use it.
- Always end with a disclaimer line: *"This is not legal advice. For your specific situation, contact a licensed Illinois attorney or one of the free legal aid resources listed."*

## Free legal aid resources to recommend

- **CARPLS** — Cook County legal help line, (312) 738-9200
- **Illinois Legal Aid Online** — illinoislegalaid.org
- **Chicago Volunteer Legal Services** — cvls.org
- **Illinois Attorney General Consumer Fraud Hotline** — (800) 386-5438
- **CAIR Chicago** — for immigration / civil rights, cairchicago.org

## Anti-patterns

- Don't invent statutes. If you can't find one, say so and stop.
- Don't generalize across states. Prism is Illinois-only by design.
- Don't promise legal outcomes. Use hedged language ("you may be entitled to...", "Illinois law typically requires...").
