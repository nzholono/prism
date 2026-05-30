# Prism — Specification

## Goal

Build a personal reasoning tool that helps Illinois residents (especially DePaul students) navigate everyday legal and ethical situations. Combines three independent perspectives — legal, ethical, cognitive — and lets the user explore each before committing to a decision.

## Three Lenses

### 1. Legal Lens

A curated, Illinois-specific knowledge base of laws, rights, and procedures. Organized by domain. Each domain has:

- **Statutes / rules** — relevant Illinois state law, Chicago municipal code, and federal law where it matters.
- **Scenarios** — common real-world situations (e.g., "landlord won't return my deposit"), each linked to applicable statutes.
- **Walkthroughs** — step-by-step actions (e.g., "how to file a small-claims case in Cook County").
- **Templates** — document drafts (demand letters, complaints).
- **Resources** — free legal aid organizations relevant to that domain.

### 2. Ethical Lens

Four ethical frameworks. For any decision, the user can ask Prism to explain how each framework would frame the choice.

- **Utilitarian** — maximizing overall wellbeing across affected parties
- **Deontological** — duties, rules, and rights regardless of outcomes
- **Virtue ethics** — what a person of good character would do
- **Care ethics** — preserving relationships and attending to specific others

For each framework, the system stores:
- Short description
- Key questions it asks ("Who is affected? What's the net wellbeing?")
- Example application to a sample dilemma

### 3. Cognitive Lens

A decision journal. The user logs decisions *before* knowing the outcome:

- What am I deciding?
- What are my options?
- What do I expect to happen?
- What's my reasoning?
- Confidence (0–100)?

The system then runs **bias detectors** against the entry — heuristic rules that flag possible cognitive biases:

- **Sunk cost** — keywords like "already spent / invested / put in"
- **Anchoring** — single reference price/number drives reasoning
- **Confirmation bias** — only evidence supporting one side mentioned
- **Availability** — recent vivid example dominates reasoning
- **Loss aversion** — disproportionate focus on what's being lost vs. gained
- **Optimism bias** — confidence > 80 with no contingency plan

Later, the user reviews the entry against actual outcome — building a personal "calibration" history.

## Legal Domains

### Tier 1 — Deeply Built (with multiple scenarios + walkthroughs)

1. **Tenant rights** — security deposits, eviction, repairs, lease terms, Chicago RLTO
2. **Employment** — wage theft, discrimination, wrongful termination, IL Human Rights Act
3. **Police / ICE encounters** — what to say and not say, IL TRUST Act, Stop Act
4. **Consumer rights & debt** — debt collection (FDCPA), refunds, scams, identity theft

### Tier 2 — Scaffolded (structure + 1–2 scenarios, designed for skill-based expansion)

5. **Campus / student rights** — Title IX, FERPA, ADA accommodations, academic appeals
6. **Healthcare & medical bills** — Hospital Uninsured Patient Discount Act, surprise billing, mental health parity
7. **Immigration / international students** — F-1, OPT, ICE encounters specific to status
8. **Mental health rights** — involuntary commitment, MH&DDC Act, 988 vs 911
9. **Traffic / vehicle** — tickets, accidents, DUI basics, booting in Chicago
10. **BIPA (Biometric Information Privacy Act)** — unique Illinois biometric protections; showcase domain

## Data Model

SQLite database, six core tables:

### `domains`
| col | type | notes |
| --- | --- | --- |
| `id` | INTEGER PRIMARY KEY | |
| `slug` | TEXT UNIQUE | e.g. `tenant`, `employment` |
| `name` | TEXT | e.g. `Tenant Rights` |
| `tier` | INTEGER | 1 or 2 |
| `summary` | TEXT | one-paragraph overview |

### `statutes`
| col | type | notes |
| --- | --- | --- |
| `id` | INTEGER PRIMARY KEY | |
| `domain_id` | FK → domains | |
| `citation` | TEXT | e.g. `765 ILCS 710/1` |
| `title` | TEXT | human-readable name |
| `summary` | TEXT | plain-English explanation |
| `body_md` | TEXT | markdown — full text or key excerpts |
| `source_url` | TEXT | link to official source |

### `scenarios`
| col | type | notes |
| --- | --- | --- |
| `id` | INTEGER PRIMARY KEY | |
| `domain_id` | FK → domains | |
| `slug` | TEXT UNIQUE | e.g. `deposit-not-returned` |
| `title` | TEXT | e.g. `Landlord won't return my deposit` |
| `description_md` | TEXT | what this situation looks like |
| `walkthrough_md` | TEXT | step-by-step what to do |
| `template_md` | TEXT | optional document draft |

### `scenario_statutes` (many-to-many)
| col | type | notes |
| --- | --- | --- |
| `scenario_id` | FK → scenarios | |
| `statute_id` | FK → statutes | |

### `ethical_frameworks`
| col | type | notes |
| --- | --- | --- |
| `id` | INTEGER PRIMARY KEY | |
| `slug` | TEXT UNIQUE | `utilitarian`, `deontological`, `virtue`, `care` |
| `name` | TEXT | |
| `description_md` | TEXT | |
| `key_questions` | TEXT (JSON array) | |

### `decisions` (the journal)
| col | type | notes |
| --- | --- | --- |
| `id` | INTEGER PRIMARY KEY | |
| `created_at` | DATETIME | |
| `situation` | TEXT | what's happening |
| `options` | TEXT (JSON array) | options considered |
| `chosen` | TEXT | option selected |
| `reasoning` | TEXT | why |
| `expected_outcome` | TEXT | what user expects |
| `confidence` | INTEGER | 0–100 |
| `linked_scenario_id` | FK → scenarios | nullable |
| `actual_outcome` | TEXT | filled in later |
| `reviewed_at` | DATETIME | when user reviewed |

### `bias_flags`
| col | type | notes |
| --- | --- | --- |
| `id` | INTEGER PRIMARY KEY | |
| `decision_id` | FK → decisions | |
| `bias_slug` | TEXT | `sunk_cost`, `anchoring`, etc. |
| `evidence` | TEXT | what triggered the flag |

## REST API (Pharos)

Base: `http://localhost:8000`

### Health & meta
- `GET /health` → `{"status":"ok"}`
- `GET /stats` → counts (domains, statutes, scenarios, decisions)

### Legal
- `GET /domains` → list
- `GET /domains/{slug}` → domain with nested statutes + scenarios
- `GET /scenarios` → list (optional `?domain=tenant&q=deposit`)
- `GET /scenarios/{slug}` → scenario with linked statutes
- `GET /statutes/{id}` → one statute

### Ethical
- `GET /ethics/frameworks` → list of all four
- `POST /ethics/analyze` → body `{"situation": "..."}` → returns analysis from each lens

### Cognitive (decisions)
- `POST /decisions` → create entry, returns entry + flagged biases
- `GET /decisions` → list (newest first, optional filter)
- `GET /decisions/{id}` → one entry with bias flags
- `PATCH /decisions/{id}` → update with actual_outcome / review notes
- `DELETE /decisions/{id}`
- `POST /decisions/{id}/biases/recheck` → re-run detectors

### Search
- `GET /search?q=...` → cross-domain search across statutes + scenarios

## Clients

All clients use a shared `ApiClient` in `prism/api_client.py`.

### CLI (`prism-cli`)

```
prism-cli rights tenant deposit
prism-cli scenario list --domain employment
prism-cli decide new
prism-cli decide list
prism-cli decide review <id>
prism-cli ethics analyze "should I report my roommate to the landlord?"
prism-cli search "deposit"
prism-cli stats
```

### TUI (`prism-tui`)

Textual app. Left pane: domain list. Center: scenarios / statute reader. Right: decision journal. Keyboard-driven. Quick search with `/`.

### Web (`prism-web`)

FastAPI app on port 8001. Renders pages with Jinja2 (or simple HTMX). Routes:
- `/` — domains overview
- `/domain/{slug}` — domain page
- `/scenario/{slug}` — scenario walkthrough
- `/decide/new` — decision form
- `/decide/{id}` — decision review

### GUI (`prism-gui`)

Tkinter desktop app. Two-pane layout: tree of domains/scenarios on left, content + decision form on right. Native macOS/Windows/Linux.

## MCP Server (`prism-mcp`)

Exposes Prism over MCP so Claude Code (or other MCP-aware tools) can query the legal/ethical knowledge base directly. Tools:

- `list_domains()`
- `get_scenario(slug)`
- `search(query)`
- `analyze_decision(situation, options, reasoning)` — returns ethical + cognitive lens output
- `log_decision(...)` — write to journal
- `recent_decisions(limit=5)`

## Project Skills

`.claude/skills/`:

### `add-scenario/SKILL.md`
Helps the user (with Claude Code) add a new scenario to the database: gather facts, find applicable statutes, draft walkthrough, write template letter, link everything.

### `bias-audit/SKILL.md`
Deep analysis of a decision-journal entry. Claude reads the entry, runs through each bias systematically, and produces a structured audit report.

## Testing Strategy

Three folders (auto-marked via `conftest.py`):

- `tests/unit/` — pure logic. Bias detectors, ethical framework prompts, data-model validation. No HTTP, no DB I/O beyond in-memory.
- `tests/contract/` — REST API shape. Uses FastAPI `TestClient`. Asserts response schemas, status codes, error handling.
- `tests/integration/` — full stack. Spins up real server in a fixture, runs real clients (CLI via Typer's `CliRunner`) against it.

Run subsets:
```
uv run pytest -m unit
uv run pytest -m contract
uv run pytest -m integration
```

## 12-Day MVP Plan

Today: May 29 (Friday). Deadline: June 10 at 11:30 AM.

| Day | Date | Goal |
| --- | ---- | ---- |
| 1 | May 30 | Spec + scaffolding (uv init, structure, README, docs) ← *we are here* |
| 2 | May 31 | DB schema + service layer + initial seed data |
| 3 | Jun 1 | Pharos REST server + contract tests |
| 4 | Jun 2 | ApiClient + CLI (Typer) |
| 5 | Jun 3 | Content: tenant + employment domains deep |
| 6 | Jun 4 | Content: police + consumer domains deep |
| 7 | Jun 5 | TUI (Textual) |
| 8 | Jun 6 | Web client (FastAPI on 8001) + GUI (Tkinter, basic) |
| 9 | Jun 7 | Ethical frameworks + bias detectors + decision endpoints |
| 10 | Jun 8 | MCP server + 2 skills |
| 11 | Jun 9 | Integration tests, docs polish, demo scenario walkthrough |
| 12 | Jun 10 | Buffer + final push to GitHub by 11:30 AM |

Scope discipline: if behind by Day 7, drop GUI (keep CLI/TUI/Web), drop Tier-2 scenario depth (keep structure).

## Out of Scope (Explicit)

- "All laws everywhere" — only curated Illinois content
- Actual legal advice — every screen shows a disclaimer pointing to free legal aid
- Real-time law updates — manual updates via the `add-scenario` skill
- User accounts / multi-user — local single-user only
- Mobile app — desktop and terminal only
