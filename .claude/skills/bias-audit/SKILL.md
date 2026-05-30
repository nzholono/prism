---
name: bias-audit
description: Deep cognitive-bias audit of an entry in the Prism decision journal. Use when the user wants a thorough, structured review of their reasoning beyond what the automated detectors caught — going through each bias systematically and producing a written report. Reads the decision via the Prism API, runs through ~12 common biases, and writes a markdown audit.
---

# Bias Audit on a Prism Decision

You are reviewing a single decision-journal entry and producing a careful, written cognitive-bias audit. This complements the automated detectors that already ran when the entry was saved — your job is to catch the things heuristic rules miss.

## Process

1. **Fetch the entry.** Ask the user for the decision ID. Call `GET /decisions/{id}` via the Prism API (or read it from `~/.prism/prism.db` directly if the user prefers).

2. **Review the existing automated flags.** They appear in `entry.biases`. Do not duplicate them — instead, treat them as the floor, not the ceiling.

3. **Walk through this checklist.** For each, note whether the bias appears to be present, possibly present, or not present. Be honest — most decisions will have only 1–3 real biases. Inventing them dilutes the audit.

   - **Sunk cost** — past spending influencing the current choice
   - **Anchoring** — first number/option disproportionately shaping reasoning
   - **Confirmation bias** — only supporting evidence considered
   - **Availability heuristic** — recent or vivid example over-weighted
   - **Loss aversion** — losses weighted more than equivalent gains
   - **Optimism bias** — high confidence with no contingency plan
   - **Status quo bias** — defaulting to "no change" without examining alternatives
   - **Bandwagon / social proof** — choosing because others did
   - **Framing effect** — the way the situation is described biasing the choice
   - **Hindsight feel** — reasoning that assumes the outcome is already known
   - **Planning fallacy** — underestimating time/cost/risk of chosen path
   - **Self-serving bias** — attributing success to self, failure to circumstances

4. **Look for what's missing.** Some biases hide in *absence*:
   - No fallback plan mentioned (optimism + planning fallacy)
   - No mention of the second-best option (status quo)
   - No mention of how this might fail (confirmation)
   - No mention of whose interests are at stake (myopic framing)

5. **Write the audit.** Markdown, 200–500 words. Structure:

   ```markdown
   # Bias Audit — Decision #{id}

   ## What you decided
   <one-sentence restatement>

   ## Likely biases
   - **<bias>** — <evidence from the entry>, <one-line reframe>
   - ...

   ## Possible biases (less certain)
   - **<bias>** — <evidence>, <what to check>

   ## What's missing
   - <thing that wasn't considered>
   - ...

   ## A different framing
   <one paragraph: how would you describe this situation from a perspective
   that doesn't share your current emotional stake?>

   ## Recommended next step
   <one concrete thing the user could do before committing>
   ```

6. **Offer to save it.** Ask whether the user wants the audit appended to the decision as a note, or saved as a separate markdown file under `~/.prism/audits/`.

## Tone

- Direct but kind. The user already wrote down their reasoning honestly — meet that with honest analysis.
- Avoid hedging-for-hedging's-sake. If you don't see a bias, say so.
- Don't lecture. The bias names are enough; the user knows what sunk cost is by the third entry.

## Anti-patterns

- Listing every bias in the checklist as "possibly present". That's not useful.
- Recommending specific outcomes ("you should not sue"). Recommend better thinking, not different choices.
- Treating high confidence as automatically suspect. Sometimes high confidence is correct.
