# Prism

A framework for reasoning about legal and ethical decisions in Illinois — through three lenses: **legal**, **ethical**, and **cognitive**.

When you face a difficult situation (your landlord keeps the deposit, a cop pulls you over, your employer underpays you), Prism shows you:

1. **What the law says** — actual Illinois statutes and Chicago ordinances, with templates and walkthroughs.
2. **What ethics says** — how different ethical frameworks (utilitarian, deontological, virtue, care) frame the same choice.
3. **What your mind says** — a decision journal that flags cognitive biases (sunk cost, anchoring, confirmation, etc.) before you commit.

The system is named after a **prism** because it refracts one situation into three useful perspectives. The REST server is named **Pharos** (the Lighthouse of Alexandria) because it's the central hub all clients connect to.

## Architecture

```
                   ┌────────────────────────────────────────┐
                   │   Pharos — FastAPI REST server         │
                   │   owns the SQLite DB                   │
                   └────────────────────┬───────────────────┘
                                        │  HTTP JSON
            ┌──────────────┬────────────┼────────────┬──────────────┐
            │              │            │            │              │
        ┌───┴───┐     ┌────┴────┐  ┌────┴─────┐ ┌────┴────┐    ┌────┴────┐
        │  CLI  │     │   TUI   │  │   Web    │ │   GUI   │    │   MCP   │
        │ typer │     │ textual │  │ fastapi  │ │ tkinter │    │  server │
        └───────┘     └─────────┘  └──────────┘ └─────────┘    └─────────┘
```

All clients import `ApiClient` from `prism/api_client.py` — one shared Python wrapper around Pharos endpoints.

## Quickstart

```bash
uv sync                          # install dependencies
uv run pytest                    # run the test suite

# Pharos server first — every client needs it running
uv run pharos                    # FastAPI on http://localhost:8000

# Then any client (each in its own terminal)
uv run prism-cli --help          # Typer command-line client
uv run prism-tui                 # Textual TUI client
uv run prism-web                 # FastAPI web UI on http://localhost:8001
uv run prism-gui                 # Tkinter desktop client

# MCP server (stdio)
uv run prism-mcp
```

## Status

In development. See `docs/spec.md` for the full specification and `docs/architecture.md` for architectural details.

## Course

CSC299 Sophomore Lab — AI-Assisted Software Development, DePaul University, Spring 2026.
