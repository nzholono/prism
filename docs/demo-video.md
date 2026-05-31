# YouTube Demo Video Script — Prism

Target length: **3 minutes**. Designed for the CSC299 final-project YouTube submission.

## Before recording

- Run `rm -rf ~/.prism` and `uv run pharos` so the DB seeds fresh
- Open two terminal tabs:
  - **Tab A** — Pharos server running (visible briefly at the start)
  - **Tab B** — empty prompt in `~/PROJECTS/prism`
- Open Chrome to `http://localhost:8001`
- Have `docs/demo-video.md` open in a separate window for reference
- Close all other apps for clean recording (use QuickTime or Loom)

---

## Shot list

### Shot 1 — Intro (0:00 – 0:15)

**On screen:** README on GitHub, scroll past badges and architecture diagram.

**Voiceover:**
> "I'm Dana, and this is Prism — a framework for reasoning about legal and ethical decisions in Illinois. Built for CSC299 over 5 days using Claude Code."

### Shot 2 — The three lenses (0:15 – 0:30)

**On screen:** Switch to Tab B. Type and run:
```bash
uv run prism-cli rights
```

**Voiceover:**
> "Nine Illinois legal domains — tenant rights, employment, police encounters, consumer protection, plus campus, healthcare, immigration, mental health, and traffic. Each one is real Illinois law with sources."

### Shot 3 — A real walkthrough (0:30 – 0:55)

**On screen:** In Tab B run:
```bash
uv run prism-cli rights show deposit-not-returned
```
Let it scroll, then **switch to Chrome** at `http://localhost:8001/scenarios/deposit-not-returned`. Show the rendered web version.

**Voiceover:**
> "When your landlord doesn't return your deposit, Prism shows you the actual Illinois statutes — 765 ILCS 710 — gives you a step-by-step walkthrough, and generates a demand letter template. The same data renders identically in the CLI, the web client, and the desktop GUI."

### Shot 4 — Ethical lens (0:55 – 1:15)

**On screen:** In Chrome, click **Ethics** in nav. Type:
> "My roommate keeps using my food without asking. I know they're broke and stressed."

Click Analyze. Briefly show all four framework cards.

**Voiceover:**
> "The same situation through four ethical frameworks — utilitarian, deontological, virtue ethics, care ethics. Each one frames the choice differently. The point isn't to tell you what to do — it's to show you that what looks like one question is really several."

### Shot 5 — Cognitive lens (the killer feature) (1:15 – 2:00)

**On screen:** Switch to Tab B. Run:
```bash
uv run prism-cli decide new
```

Type, deliberately, as you go:
- **What's happening?** `My landlord won't return my $1200 deposit`
- **Options:** `Sue in small claims, Drop it, Try to negotiate`
- **Which leaning toward?** `Sue in small claims`
- **Why?** `I've already spent so much time on this. The law is clearly on my side. It will definitely work.`
- **Expected outcome?** `I get the money back doubled`
- **Confidence?** `95`

Hit Enter. **Pause** for the bias flags to render.

**Voiceover (over the typing):**
> "The cognitive lens is the most important one. You log a decision before you know how it turns out — your reasoning, your confidence, what you expect. Then Prism runs ten cognitive bias detectors against what you wrote."

**Voiceover (after flags appear):**
> "Three flags. Sunk cost — 'I've already spent so much.' Confirmation bias — I gave only supporting evidence. Optimism — confidence 95 with no fallback. None of this means I shouldn't sue. It means I should make the decision aware of what my own mind is doing."

### Shot 6 — Calibration (2:00 – 2:25)

**On screen:** In Tab B, run:
```bash
uv run prism-cli stats --calibration
```

**Voiceover:**
> "Over time, Prism tracks whether your confidence has matched reality. Were the decisions with bias flags worse than the ones without? Are you systematically overconfident? This is the meta-feature — Prism doesn't tell you what to do, it shows you how you think."

### Shot 7 — Architecture (2:25 – 2:50)

**On screen:** Briefly show TUI:
```bash
uv run prism-tui
```
Navigate one scenario with arrow keys, then `q` to quit.

Then show GUI:
```bash
uv run prism-gui
```
Click one domain, then close the window.

Then back to Chrome, scroll briefly.

**Voiceover:**
> "Four interfaces — CLI, TUI, Web, desktop GUI — plus an MCP server so Claude Code can query Prism directly. None of them touches the database; they all go through one REST server. Add an endpoint, every client gets it for free. Ninety tests across three layers. Open source, MIT licensed, on GitHub at github dot com slash nzholono slash prism."

### Shot 8 — Close (2:50 – 3:00)

**On screen:** GitHub repo page.

**Voiceover:**
> "Prism. Three lenses on one situation. Thanks for watching."

---

## Recording tips

- **Pause between shots.** Easier to edit later than to re-record.
- **Type slowly** during the decision-journal shot — it's the most important visual.
- **Don't apologize on screen** if you make a typo. Just keep going; edit out in post.
- **Volume:** test mic levels in QuickTime before the real take.
- **Terminal font size:** at least 16pt. Make sure viewers can read it.
- **Hide your dock and notifications** (Do Not Disturb on Mac).

## After recording

1. Trim dead space at start and end.
2. Add a title card if you want (Prism — Illinois Legal & Ethical Reasoning).
3. Upload to YouTube as **Unlisted** first to test, then **Public**.
4. Title: `Prism — Illinois Legal & Ethical Reasoning Framework (CSC299 final project)`
5. Description: include the GitHub link.
6. Add the YouTube URL to your Discord post / project submission.
