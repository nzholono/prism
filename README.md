# Prism

[![tests](https://github.com/nzholono/prism/actions/workflows/test.yml/badge.svg)](https://github.com/nzholono/prism/actions/workflows/test.yml)
[![python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A framework for reasoning about **legal and ethical decisions in Illinois** — through three lenses.

When you face a difficult situation (your landlord keeps the deposit, a cop pulls you over, your employer underpays you), Prism shows you:

1. **What the law says** — actual Illinois statutes and Chicago ordinances, with templates and walkthroughs.
2. **What ethics says** — how four ethical frameworks (utilitarian, deontological, virtue, care) frame the same choice.
3. **What your mind says** — a decision journal that flags ten cognitive biases (sunk cost, anchoring, confirmation, availability, loss aversion, optimism, status quo, bandwagon, framing, planning fallacy) before you commit.

Named after a **prism** because it refracts one situation into three useful perspectives. The REST server is named **Pharos** (the Lighthouse of Alexandria) because it's the central hub all clients connect to.

Built for CSC299 — Sophomore Lab in AI-Assisted Software Development, DePaul University, Spring 2026.

## Architecture

```
                   ┌────────────────────────────────────────┐
                   │   Pharos — FastAPI REST server :8000   │
                   │   owns the SQLite database             │
                   └────────────────────┬───────────────────┘
                                        │  HTTP JSON
            ┌──────────────┬────────────┼────────────┬──────────────┐
            │              │            │            │              │
        ┌───┴───┐     ┌────┴────┐  ┌────┴─────┐ ┌────┴────┐    ┌────┴────┐
        │  CLI  │     │   TUI   │  │   Web    │ │   GUI   │    │   MCP   │
        │ typer │     │ textual │  │ fastapi  │ │ tkinter │    │  server │
        │       │     │         │  │  :8001   │ │         │    │  stdio  │
        └───────┘     └─────────┘  └──────────┘ └─────────┘    └─────────┘
```

All five clients import `ApiClient` from `prism/api_client.py` — one shared Python wrapper around the REST endpoints. Add an endpoint = add one method here, every client gets it.

## Quickstart

```bash
uv sync                    # install dependencies
uv run pytest              # run the test suite (~80 tests)

# Pharos server first — every other client needs it running
uv run pharos              # FastAPI REST server on http://localhost:8000

# Then any client (each in its own terminal)
uv run prism-cli --help    # Typer command-line client
uv run prism-tui           # Textual TUI
uv run prism-web           # FastAPI web UI on http://localhost:8001
uv run prism-gui           # Tkinter desktop client

# MCP server runs the service layer directly (stdio)
uv run prism-mcp
```

## Features

### Legal lens — 10 Illinois domains

**Tier 1 (deep coverage with multiple scenarios + walkthroughs):**
- **Tenant rights** — security deposits, eviction notices, repairs, Chicago RLTO
- **Employment** — wage theft, discrimination, paid leave, Illinois Human Rights Act
- **Police & ICE encounters** — Illinois TRUST Act, your rights during a stop, what to say (and not say)
- **Consumer rights & debt** — FDCPA, Illinois Consumer Fraud Act, BIPA (biometric privacy)

**Tier 2 (real content, extensible via the `add-scenario` skill):**
- Campus / student rights (Title IX, FERPA, ADA)
- Healthcare & medical bills (Hospital Uninsured Patient Discount Act)
- Immigration / international students (F-1, OPT)
- Mental health rights (involuntary commitment, MH&DDC Act)
- Traffic & vehicle (tickets, accidents, towing)
- Criminal records & expungement (Illinois Criminal Identification Act)

### Ethical lens — 4 frameworks

For any situation, Prism frames the choice through:

- **Utilitarian** — maximize wellbeing across everyone affected
- **Deontological** — duties, rights, rules that hold regardless of outcomes
- **Virtue ethics** — what would a person of good character do
- **Care ethics** — preserve relationships, attend to specific others

Each framework comes with key questions to ask yourself.

### Cognitive lens — decision journal + 15 bias detectors

Log a decision *before* you know the outcome. Prism stores:
- the situation, your options, what you chose
- your reasoning, what you expect, confidence (0–100)

…and runs thirteen bias detectors against your reasoning, flagging anything suspicious:

| Bias | What it catches |
| --- | --- |
| Sunk cost | "I've already spent so much on this" |
| Anchoring | A single number dominating your reasoning |
| Confirmation | Reasoning that lists only supporting evidence |
| Availability | A recent vivid example driving the choice |
| Loss aversion | Disproportionate focus on what's being lost |
| Optimism | High confidence with no contingency plan |
| Status quo | Defaulting to "no change" without examination |
| Bandwagon | "Everyone does it" reasoning |
| Framing | Heavy use of one frame (certainty / percentage / loss) |
| Planning fallacy | "Quick and easy" with no buffer time |
| Hindsight | Treating outcome as if it was knowable in advance |
| Fundamental attribution | Explaining behavior by character, not situation |
| Halo effect | One positive trait coloring overall judgment |
| Recency | A single recent event overshadowing the longer pattern |
| Self-serving | Externalizing failure / claiming all credit for success |

**Calibration over time:** `prism-cli stats --calibration` shows whether your confidence has tracked reality. Are you overconfident? Underconfident? Do certain biases correlate with bad outcomes?

## MCP server — Prism inside Claude Code

`uv run prism-mcp` exposes the legal/ethical/cognitive layers over MCP so Claude Code (or any MCP-aware tool) can query Prism's curated database. Tools:

- `list_domains`, `get_domain`, `get_scenario`, `search` — legal queries
- `analyze_ethically` — four-lens ethical analysis
- `log_decision`, `recent_decisions`, `review_decision` — cognitive journal
- `stats` — overall counts

Plus a `scenario://` resource type and a `bias_audit` prompt template.

To register with Claude Code, add to your MCP config:

```json
{
  "mcpServers": {
    "prism": {
      "command": "uv",
      "args": ["run", "prism-mcp"],
      "cwd": "/path/to/prism"
    }
  }
}
```

## Project skills

Two skills under `.claude/skills/`:

- **`add-scenario`** — guides Claude through researching Illinois statutes and adding a new scenario to the database (the supported way to grow the legal content).
- **`bias-audit`** — produces a deep written audit of a single decision-journal entry, walking through ~12 biases beyond what the automated detectors catch.

## Testing

Three-layer test pyramid, organized by folder:

```
tests/unit/        — pure logic (bias detectors, calibration, seed modules)
tests/contract/    — REST API shape via FastAPI TestClient
tests/integration/ — full stack through real clients (Typer CliRunner, web)
```

Run a slice:

```bash
uv run pytest -m unit
uv run pytest -m contract
uv run pytest -m integration
```

See `docs/testing.md` for the full strategy.

## Documentation

| File | What it covers |
| --- | --- |
| [`docs/spec.md`](docs/spec.md) | Full specification: scope, data model, REST endpoints, MVP plan |
| [`docs/architecture.md`](docs/architecture.md) | Architecture explained, with Mermaid diagrams |
| [`docs/testing.md`](docs/testing.md) | Test strategy: unit / contract / integration |
| [`docs/demo.md`](docs/demo.md) | Walkthrough scenario for live demo |
| [`CHANGELOG.md`](CHANGELOG.md) | Day-by-day build log |

## Disclaimer

This is reference material, not legal advice. For your specific situation, contact a licensed Illinois attorney or one of the free legal aid resources listed in each scenario:

- **CARPLS** (Cook County legal help line): (312) 738-9200
- **Illinois Legal Aid Online**: illinoislegalaid.org
- **National Immigrant Justice Center**: (312) 660-1370
- **First Defense Legal Aid** (24-hour Chicago hotline): (800) LAW-REP-4

## Course

CSC299 — Sophomore Lab in AI-Assisted Software Development, DePaul University, Spring 2026. Instructor: Prof. Corin Pitcher.
