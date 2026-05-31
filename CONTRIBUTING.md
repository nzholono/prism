# Contributing to Prism

Prism is a small but extensible legal-reasoning framework focused on Illinois law.
Contributions of any size welcome.

## Easiest contribution: add a scenario

Use the `add-scenario` skill in Claude Code, or by hand:

1. Pick an existing domain (`tenant`, `employment`, `consumer`, …) or create a new module under `src/prism/seed/`.
2. Add a scenario dict with `slug`, `title`, `description_md`, `walkthrough_md`, optional `template_md`, and `linked_statutes` (list of citation strings).
3. Add any new statutes the scenario references.
4. Run `uv run pytest tests/unit/test_seed.py -v` to confirm idempotent seeding works.
5. Test in the CLI: `uv run prism-cli rights show <new-scenario-slug>`.

## Setup

```bash
git clone https://github.com/nzholono/prism.git
cd prism
uv sync --all-groups
uv run pytest
```

## Project layout

```
src/prism/         # library code
src/prism/seed/    # one module per Illinois legal domain
src/prism/lenses/  # legal / ethical / cognitive logic
tests/unit/        # pure logic
tests/contract/    # REST API shape
tests/integration/ # full stack through real clients
docs/              # spec, architecture, testing, demo, this file
.claude/skills/    # extension skills for Claude Code
```

See `docs/architecture.md` for the system shape and `docs/spec.md` for the data model.

## Conventions

- **Citations** follow Bluebook-lite: `<title> <code> <chapter>/<section>` for ILCS, `Chi. Mun. Code <chapter>-<section>` for Chicago.
- **Slugs** are lowercase-hyphenated (`deposit-not-returned`, not `Deposit Not Returned`).
- **Walkthroughs** assume the reader has no legal background. Define every term the first time you use it.
- **Always end** scenarios with the free-legal-aid disclaimer.

## Anti-patterns

- ❌ Inventing statutes. If you can't find the source URL, don't add the statute.
- ❌ Generalizing across states. Prism is Illinois-only by design.
- ❌ Promising legal outcomes. Use hedged language ("you may be entitled to…").
- ❌ Skipping tests for new content.

## Tests

Three layers — run independently:

```bash
uv run pytest -m unit         # fast, pure logic
uv run pytest -m contract     # REST API shape
uv run pytest -m integration  # full stack through real clients
uv run pytest                 # all of the above
```

CI runs all three on every push to `main` (see `.github/workflows/test.yml`).

## Questions?

Open an issue or DM @nzholono on GitHub.
