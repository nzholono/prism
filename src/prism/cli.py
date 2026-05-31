"""Prism CLI — Typer-based command-line client.

Run with `uv run prism-cli --help`.

Every command goes through ApiClient → Pharos → SQLite. The CLI never opens
the database directly.
"""

from __future__ import annotations

from typing import Optional

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

from prism import __version__
from prism.api_client import ApiClient, PharosUnavailable
from prism.models import DecisionCreate, DecisionUpdate

app = typer.Typer(
    name="prism-cli",
    help="Illinois legal & ethical reasoning — through three lenses.",
    no_args_is_help=True,
)
rights_app = typer.Typer(help="Browse legal domains and scenarios.")
decide_app = typer.Typer(help="Decision journal with bias detection.")
ethics_app = typer.Typer(help="Analyze a situation through ethical frameworks.")
app.add_typer(rights_app, name="rights")
app.add_typer(decide_app, name="decide")
app.add_typer(ethics_app, name="ethics")

console = Console()


@app.callback()
def _callback() -> None:
    """Prism — Illinois legal & ethical reasoning through three lenses."""


def _client() -> ApiClient:
    """Build an ApiClient and exit cleanly if the server is down."""
    try:
        client = ApiClient()
        client.health()  # eager check
        return client
    except PharosUnavailable as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1)


# ─── top-level commands ─────────────────────────────────────────────────────

@app.command()
def health() -> None:
    """Check that Pharos is running."""
    client = _client()
    r = client.health()
    console.print(f"[green]OK[/green] — Pharos {r.version}")


@app.command()
def version() -> None:
    """Print the Prism client version."""
    console.print(f"prism {__version__}")


@app.command()
def stats(
    calibration: bool = typer.Option(
        False, "--calibration", "-c", help="Show how well your confidence has tracked reality."
    )
) -> None:
    """Show counts of domains, statutes, scenarios, decisions. Add --calibration for accuracy report."""
    client = _client()
    s = client.stats()
    table = Table(title="Prism stats", show_header=False, box=None)
    table.add_row("Domains", str(s.domains))
    table.add_row("Statutes", str(s.statutes))
    table.add_row("Scenarios", str(s.scenarios))
    table.add_row("Decisions", str(s.decisions))
    table.add_row("Bias flags", str(s.bias_flags))
    console.print(table)

    if calibration:
        from prism.lenses.cognitive.calibration import calibrate

        decisions = client.list_decisions(limit=1000)
        report = calibrate(decisions)
        console.print()
        console.print(Panel(report.summary(), title="Calibration", border_style="cyan"))


@app.command()
def search(query: str = typer.Argument(..., help="Text to search for")) -> None:
    """Search statutes and scenarios for the given text."""
    client = _client()
    hits = client.search(query)
    if not hits:
        console.print(f"[yellow]No matches for '{query}'[/yellow]")
        return
    table = Table(title=f"Search: '{query}'")
    table.add_column("Kind")
    table.add_column("Domain")
    table.add_column("Title")
    table.add_column("Snippet", overflow="fold")
    for h in hits:
        table.add_row(h.kind, h.domain_slug, h.title, h.snippet)
    console.print(table)


# ─── rights subcommands ─────────────────────────────────────────────────────

@rights_app.callback(invoke_without_command=True)
def rights_root(ctx: typer.Context) -> None:
    """If invoked with no subcommand, list domains."""
    if ctx.invoked_subcommand is not None:
        return
    client = _client()
    domains = client.list_domains()
    table = Table(title="Legal domains")
    table.add_column("Slug", style="cyan")
    table.add_column("Name")
    table.add_column("Tier")
    table.add_column("Summary", overflow="fold")
    for d in domains:
        table.add_row(d.slug, d.name, str(d.tier), d.summary)
    console.print(table)


@rights_app.command("show")
def rights_show(domain_or_scenario: str) -> None:
    """Show a domain (e.g. `tenant`) or a scenario (e.g. `deposit-not-returned`)."""
    client = _client()

    # try scenario first, fall back to domain
    try:
        sc = client.get_scenario(domain_or_scenario)
        _render_scenario(sc)
        return
    except Exception:
        pass

    try:
        d = client.get_domain(domain_or_scenario)
    except Exception:
        console.print(f"[red]No domain or scenario named '{domain_or_scenario}'[/red]")
        raise typer.Exit(code=1)

    console.print(Panel(f"[bold]{d.name}[/bold]\n\n{d.summary}", title=d.slug))
    if d.scenarios:
        table = Table(title="Scenarios", show_header=True)
        table.add_column("Slug", style="cyan")
        table.add_column("Title")
        for sc in d.scenarios:
            table.add_row(sc.slug, sc.title)
        console.print(table)
    if d.statutes:
        table = Table(title="Statutes", show_header=True)
        table.add_column("Citation", style="cyan")
        table.add_column("Title", overflow="fold")
        for st in d.statutes:
            table.add_row(st.citation, st.title)
        console.print(table)


def _render_scenario(sc) -> None:
    console.print(Panel(f"[bold]{sc.title}[/bold]", title=sc.slug))
    console.print(Markdown(sc.description_md))
    console.print()
    console.print(Markdown(sc.walkthrough_md))
    if sc.statutes:
        console.print()
        console.print("[bold]Applicable statutes[/bold]")
        for st in sc.statutes:
            console.print(f"  • [cyan]{st.citation}[/cyan] — {st.title}")
    if sc.template_md:
        console.print()
        console.print(Markdown(sc.template_md))


# ─── ethics subcommands ─────────────────────────────────────────────────────

@ethics_app.command("frameworks")
def ethics_frameworks() -> None:
    """List the four ethical frameworks."""
    client = _client()
    for fw in client.list_ethical_frameworks():
        console.print(Panel(Markdown(fw.description_md), title=f"{fw.name} ({fw.slug})"))


@ethics_app.command("analyze")
def ethics_analyze(situation: str = typer.Argument(..., help="The situation in one sentence")) -> None:
    """Frame a situation through each ethical lens."""
    client = _client()
    analysis = client.analyze_ethically(situation)
    console.print(Panel(f"[italic]{analysis.situation}[/italic]", title="Situation"))
    for p in analysis.perspectives:
        body = p.framing + "\n\n**Key questions:**\n" + "\n".join(f"- {q}" for q in p.questions)
        console.print(Panel(Markdown(body), title=p.framework_name))


# ─── decide subcommands ─────────────────────────────────────────────────────

@decide_app.command("new")
def decide_new() -> None:
    """Interactively log a new decision and see flagged biases."""
    client = _client()
    console.print("[bold]New decision[/bold] — describe what you're deciding.\n")
    situation = Prompt.ask("What's happening?")
    raw_options = Prompt.ask("Your options (comma-separated)")
    options = [o.strip() for o in raw_options.split(",") if o.strip()]
    if len(options) < 2:
        console.print("[red]Need at least 2 options.[/red]")
        raise typer.Exit(code=1)
    chosen = Prompt.ask("Which are you leaning toward?", default=options[0])
    reasoning = Prompt.ask("Why? (be honest)")
    expected_outcome = Prompt.ask("What do you expect to happen?")
    confidence = IntPrompt.ask("Confidence (0–100)", default=60)

    d = DecisionCreate(
        situation=situation,
        options=options,
        chosen=chosen,
        reasoning=reasoning,
        expected_outcome=expected_outcome,
        confidence=confidence,
    )
    decision = client.create_decision(d)

    console.print()
    console.print(f"[green]Logged as decision #{decision.id}[/green]")
    if decision.biases:
        console.print("\n[bold yellow]Bias flags:[/bold yellow]")
        for b in decision.biases:
            console.print(Panel(b.evidence, title=b.bias_slug, border_style="yellow"))
    else:
        console.print("[dim]No bias flags raised by the automated detectors.[/dim]")


@decide_app.command("list")
def decide_list(limit: int = typer.Option(20, help="Max entries to show")) -> None:
    """List your most recent decisions."""
    client = _client()
    decisions = client.list_decisions(limit=limit)
    if not decisions:
        console.print("[dim]No decisions logged yet. Try `prism-cli decide new`.[/dim]")
        return
    table = Table(title="Recent decisions")
    table.add_column("#", style="cyan", justify="right")
    table.add_column("Date")
    table.add_column("Situation", overflow="fold")
    table.add_column("Chose")
    table.add_column("Conf.")
    table.add_column("Biases")
    table.add_column("Outcome")
    for d in decisions:
        table.add_row(
            str(d.id),
            d.created_at.strftime("%Y-%m-%d"),
            d.situation,
            d.chosen,
            str(d.confidence),
            str(len(d.biases)),
            "✓" if d.actual_outcome else "—",
        )
    console.print(table)


@decide_app.command("show")
def decide_show(decision_id: int) -> None:
    """Show the full text of a decision and its bias flags."""
    client = _client()
    d = client.get_decision(decision_id)
    console.print(Panel(d.situation, title=f"Decision #{d.id}"))
    table = Table(show_header=False, box=None)
    table.add_row("Options", ", ".join(d.options))
    table.add_row("Chose", d.chosen)
    table.add_row("Confidence", str(d.confidence))
    table.add_row("Expected", d.expected_outcome)
    table.add_row("Reasoning", d.reasoning)
    if d.actual_outcome:
        table.add_row("[green]Actual[/green]", d.actual_outcome)
    console.print(table)
    if d.biases:
        console.print("\n[bold yellow]Bias flags:[/bold yellow]")
        for b in d.biases:
            console.print(Panel(b.evidence, title=b.bias_slug, border_style="yellow"))


@decide_app.command("review")
def decide_review(decision_id: int) -> None:
    """Record what actually happened for a past decision."""
    client = _client()
    d = client.get_decision(decision_id)
    console.print(Panel(d.situation, title=f"Reviewing decision #{d.id}"))
    console.print(f"You expected: [italic]{d.expected_outcome}[/italic]\n")
    actual = Prompt.ask("What actually happened?")
    updated = client.update_decision(decision_id, DecisionUpdate(actual_outcome=actual))
    console.print(f"[green]Saved.[/green] Decision #{updated.id} now has a recorded outcome.")


@decide_app.command("delete")
def decide_delete(decision_id: int) -> None:
    """Delete a decision."""
    client = _client()
    if not Confirm.ask(f"Delete decision #{decision_id}?"):
        return
    client.delete_decision(decision_id)
    console.print(f"[green]Deleted decision #{decision_id}.[/green]")


if __name__ == "__main__":
    app()
