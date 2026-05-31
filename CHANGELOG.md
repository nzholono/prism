# Changelog

All notable changes to Prism. Most recent first.

## Day 6 — May 30 (late) — Expansion & professional polish

### Added
- **5 Tier-2 domains expanded** to real content (no longer stubs):
  - **Campus** — FERPA, Title IX, ADA (3 statutes, 2 scenarios incl. Title IX walkthrough and grade-dispute appeal)
  - **Healthcare** — Hospital Uninsured Patient Discount Act, No Surprises Act (2 statutes, 1 detailed walkthrough + negotiation template)
  - **Mental health** — 405 ILCS 5/3-600 (involuntary admission), MHDDC confidentiality (2 statutes, 988-vs-911 walkthrough)
  - **Immigration** — F-1 visa employment rules (1 statute, full F-1 work walkthrough)
  - **Traffic** — Chicago administrative hearings (1 statute, parking ticket dispute walkthrough + template)
- **`prism-cli decide audit <id>`** — structured 12-bias audit report (Markdown)
- **`prism-cli decide export <id> [-o path]`** — export decision as standalone Markdown file
- **`prism-cli decide new --scenario <slug>`** — link a decision to a legal scenario at creation time
- **LICENSE** (MIT, with explicit legal-advice disclaimer)
- **`.github/workflows/test.yml`** — CI runs all three test layers on Python 3.10/3.11/3.12 every push
- **`CONTRIBUTING.md`** — explains how to add scenarios via the skill or by hand
- **README badges** — tests status, Python version, license
- **`docs/demo-video.md`** — shot-by-shot 3-minute script for YouTube submission

### Changed
- `seed/__init__.py` now imports all 9 domain modules; `scaffolded.py` is a no-op stub kept for backwards compatibility

## Day 5 — May 30 — Polish & calibration

### Added
- **4 more bias detectors:** status quo, bandwagon, framing, planning fallacy. Total: 10.
- **Calibration analysis** (`prism.lenses.cognitive.calibration`) — tracks
  overconfidence patterns across reviewed decisions.
- **`prism-cli stats --calibration`** — surfaces calibration in the CLI.
- **Polished web UI** — proper card design, stat grid on home page, tier badges,
  consistent color system.
- **CHANGELOG.md** — this file.
- **`docs/demo.md`** — full live-demo walkthrough script.
- **README rewrite** — covers everything that's built.
- **More unit tests** — `test_more_biases.py`, `test_calibration.py`.

## Day 3–4 — May 30 — Clients & content

### Added
- **TUI** (Textual) — full keyboard-driven terminal UI with domain navigation,
  search modal, ethics analyzer, decision-journal screens.
- **Web client** (FastAPI on port 8001) — proper pages for rights, scenarios,
  ethics form, decision journal, search, stats.
- **GUI** (Tkinter) — desktop app with domain tree and content pane.
- **MCP server** (`prism-mcp`) — exposes 9 tools, 1 resource, 1 prompt template
  over MCP/stdio for Claude Code integration.
- **Employment domain** — minimum wage, wage theft, discrimination
  (820 ILCS 105/4, 820 ILCS 115/14, 775 ILCS 5/1-103, 820 ILCS 192/15).
- **Police & ICE domain** — TRUST Act, Terry stops, recorded interrogations
  (5 ILCS 805/15, 725 ILCS 5/107-14, 725 ILCS 5/103-2.1).
- **Consumer domain** — FDCPA, Illinois Consumer Fraud Act, BIPA
  (15 USC § 1692, 815 ILCS 505/2, 740 ILCS 14).
- **Scaffolded domains** — campus, healthcare, immigration, mental health,
  traffic (1 sample scenario each, extensible via `add-scenario` skill).
- **Seed tests** — every domain seeded idempotently.
- **Web contract tests** — every page renders the right shape.

### Fixed
- TUI: `Static.update()` is synchronous in current Textual, not awaitable.

## Day 2 — May 29 (evening) — Service layer, real API, decision journal

### Added
- **Service layer** (`prism/service.py`) — every read/write goes through here.
  Both Pharos and the MCP server share this code.
- **REST endpoints** for domains, scenarios, statutes, search, ethics,
  decisions (create / list / show / patch / delete).
- **ApiClient methods** for every endpoint — the single source of truth.
- **CLI commands:** `rights`, `rights show`, `decide new / list / show /
  review / delete`, `ethics frameworks / analyze`, `search`, `stats`.
- **Tenant domain seed** — 5 statutes (765 ILCS 710/1, /2; Chi. Mun. Code
  5-12-080; 735 ILCS 5/9-209; Jack Spring v. Little), 3 scenarios
  (deposit-not-returned, five-day-notice, repairs-not-made) with demand-letter
  template.
- **Ethical-frameworks seed** — utilitarian, deontological, virtue, care.
- **Contract tests** for legal, ethics, and decisions endpoints.
- **Integration tests** for the CLI end-to-end and for the ApiClient round trip.

### Fixed
- `httpx.ASGITransport` is async-only — switched to a `MockTransport` that
  delegates to FastAPI's `TestClient`, keeping the ApiClient code path sync.

## Day 1 — May 29 — Scaffolding

### Added
- Project initialized with `uv init`. `pyproject.toml` lists all dependencies.
- Directory structure: `src/prism/`, `tests/{unit,contract,integration}/`,
  `.claude/skills/`, `docs/`.
- **Cognitive bias detectors** — 6 (sunk cost, anchoring, confirmation,
  availability, loss aversion, optimism) with parametrized unit tests.
- **`/health` endpoint** in Pharos — minimal proof of architecture.
- **CLI skeleton** with `health` command via Typer.
- **Test fixtures** — `app`, `http`, `in_process_client` (later refactored).
- **Skills**: `add-scenario`, `bias-audit`.
- **Docs**: `spec.md`, `architecture.md` (with Mermaid), `testing.md`,
  `README.md`.
- Pushed to GitHub.
