"""Prism CLI — Typer-based command-line client.

Run with `uv run prism-cli --help`.

Skeleton only: `health` proves the client → server round trip. Real subcommands
(`rights`, `decide`, `ethics`, `search`) land in the next phase.
"""

from __future__ import annotations

import typer
from rich.console import Console

from prism import __version__
from prism.api_client import ApiClient, PharosUnavailable

app = typer.Typer(
    name="prism-cli",
    help="Illinois legal & ethical reasoning — through three lenses.",
    no_args_is_help=True,
)

console = Console()


# A top-level callback forces Typer into multi-command mode even when only one
# subcommand exists. Without this, Typer collapses single-command apps to the
# root and `prism-cli health` becomes "unexpected extra argument".
@app.callback()
def _callback() -> None:
    """Prism — Illinois legal & ethical reasoning through three lenses."""


@app.command()
def health() -> None:
    """Check that Pharos is running."""
    try:
        with ApiClient() as client:
            r = client.health()
    except PharosUnavailable as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1)

    console.print(f"[green]OK[/green] — Pharos {r.version}")


@app.command()
def version() -> None:
    """Print the Prism client version."""
    console.print(f"prism {__version__}")


if __name__ == "__main__":
    app()
