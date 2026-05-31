# Demo Walkthrough

A 5-minute live demo of Prism. Designed for the CSC299 final-project presentation.

## Setup before you start

In three separate terminal tabs:

**Tab 1 — Pharos REST server:**
```bash
cd ~/PROJECTS/prism
rm -rf ~/.prism      # start with a clean DB so the demo is reproducible
uv run pharos
```
Leave running. You should see `Uvicorn running on http://127.0.0.1:8000`.

**Tab 2 — Web client:**
```bash
cd ~/PROJECTS/prism
uv run prism-web
```
Leave running. Open `http://localhost:8001` in your browser.

**Tab 3 — CLI / TUI scratchpad:**
```bash
cd ~/PROJECTS/prism
```
Use this for interactive commands during the demo.

## The story

> *"I built Prism because students at DePaul lose their security deposits, get unfair tickets, and make life-changing decisions under emotional pressure with no good resource to lean on. Prism gives them three lenses on the same situation: what the law says, what ethics says, and what their own mind might be hiding from them."*

## Step 1 — The architecture (30 seconds)

Show the README. Point at the architecture diagram.

> *"One REST server owns the SQLite database. Four clients — CLI, TUI, web, GUI — and an MCP server all talk to it through the same Python `ApiClient` class. Adding an endpoint means one method here, every client gets it for free."*

## Step 2 — The legal lens (60 seconds)

Switch to the browser at `http://localhost:8001`.

1. Click **Rights**. Show the 9 domains.
2. Click **Tenant Rights**.
3. Click **Landlord didn't return my security deposit**.

> *"Real Illinois statutes — 765 ILCS 710/1, the Chicago RLTO. A step-by-step walkthrough. A demand letter template. Free legal aid contacts."*

Scroll through the walkthrough briefly. Point out the citation tag and template.

## Step 3 — The ethical lens (45 seconds)

Click **Ethics** in the nav. Type:

> "My roommate keeps using my food without asking. I know they're broke and stressed about their dad's illness."

Click **Analyze**.

> *"Four ethical frameworks frame the same choice differently. Utilitarian asks about wellbeing across everyone. Deontological asks about duties and rights. Virtue ethics asks what kind of person you want to be. Care ethics asks whose voice is missing."*

Read one or two of the framings out loud.

## Step 4 — The cognitive lens (90 seconds)

This is the killer feature. Switch to **Tab 3** (CLI).

```bash
uv run prism-cli decide new
```

Type, deliberately, the following:

- **What's happening?** `My landlord won't return my $1200 deposit`
- **Options (comma-separated):** `Sue in small claims, Drop it, Try to negotiate`
- **Which are you leaning toward?** `Sue in small claims`
- **Why? (be honest):** `I've already spent so much time on this. The law is clearly on my side. It will definitely work.`
- **What do you expect to happen?** `I get the money back doubled`
- **Confidence (0–100):** `95`

Hit Enter.

> *"Three bias flags. Sunk cost — 'I've already spent so much'. Confirmation — I gave only supporting evidence, no counter-considerations. Optimism — confidence 95 with no fallback plan."*

> *"None of this means I shouldn't sue. It means I should make the decision aware of how my own mind is trying to push me there."*

## Step 5 — The MCP integration (30 seconds)

In any terminal:

```bash
uv run prism-cli stats --calibration
```

> *"After you've logged and reviewed a few decisions, Prism shows you patterns. Are you systematically overconfident? Do your bias-flagged decisions go worse than your clean ones? This is the meta-feature — Prism doesn't tell you what to do, it shows you how you think."*

Show `.claude/skills/`:

```bash
cat .claude/skills/add-scenario/SKILL.md | head -30
```

> *"Two project skills installed for Claude Code. `add-scenario` knows the conventions for adding a new Illinois statute. `bias-audit` runs a deep cognitive audit of a journal entry. Prism is designed to grow over time."*

## Step 6 — The architecture proof (30 seconds)

Show the **TUI** quickly:

```bash
uv run prism-tui
```

Press `/`, search `deposit`, navigate one scenario. Press `q` to quit.

Then the **GUI**:

```bash
uv run prism-gui
```

Show the tree on the left, click a scenario.

> *"Same data, four different interfaces. None of them touches the SQLite file directly — they all go through Pharos."*

## Step 7 — Tests (15 seconds)

```bash
uv run pytest --tb=no -q
```

Should print `80 passed` or so.

> *"Three test layers. Unit tests for the bias detectors and calibration. Contract tests that pin the REST API shape. Integration tests that drive the CLI and web client end-to-end against an in-process Pharos."*

## Closing line

> *"Prism is open-source on GitHub at github.com/nzholono/prism. The Tier-2 domains are scaffolded so the legal content grows over time through the `add-scenario` skill. Built with Claude Code in 12 days."*

## If something breaks during the demo

| Problem | Fix |
| --- | --- |
| Pharos won't start | Check port 8000 is free: `lsof -i :8000` |
| Web shows "server unavailable" | Pharos isn't running in Tab 1 |
| TUI looks weird | Make terminal at least 100 cols × 35 rows |
| `prism-cli` says command not found | `uv sync` first |
| Tests fail | `rm -rf ~/.prism` then re-run |

## Backup: pre-seeded demo data

If demo is for a tight time slot, pre-seed three decisions so the calibration command has something to show:

```bash
uv run prism-cli decide new   # decision 1: high confidence, becomes "bad" outcome
uv run prism-cli decide review 1     # mark "didn't work"
uv run prism-cli decide new   # decision 2: lower confidence, "good" outcome
uv run prism-cli decide review 2     # mark "worked out fine"
uv run prism-cli decide new   # decision 3: medium confidence, no review yet
```

Then `uv run prism-cli stats --calibration` will produce a meaningful report.
