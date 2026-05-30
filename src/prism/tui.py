"""Prism TUI — Textual app.

Run with `uv run prism-tui`. Requires Pharos to be running.

Layout:
    ┌─────────────────┬───────────────────────────────────────┐
    │ Domains         │ Scenario / statute reader             │
    │ (left pane)     │ (center)                              │
    │                 │                                       │
    │ Scenarios for   │                                       │
    │ selected domain │                                       │
    └─────────────────┴───────────────────────────────────────┘
    │ status bar                                              │

Keys:
    /  — focus search
    n  — new decision
    j  — list decisions
    e  — ethics analyze prompt
    q  — quit
"""

from __future__ import annotations

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen, Screen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    Markdown,
    Static,
    TextArea,
)

from prism.api_client import ApiClient, PharosUnavailable
from prism.models import DecisionCreate


# ──────────────────────────────────────────────────────────────────────────────
# Modals
# ──────────────────────────────────────────────────────────────────────────────


class SearchModal(ModalScreen[str]):
    """A small overlay to type a search query."""

    BINDINGS = [Binding("escape", "dismiss", "Cancel")]

    def compose(self) -> ComposeResult:
        with Vertical(classes="modal"):
            yield Label("Search statutes and scenarios:")
            yield Input(placeholder="e.g. deposit", id="search-input")

    @on(Input.Submitted)
    def on_submit(self, event: Input.Submitted) -> None:
        self.dismiss(event.value)


class EthicsModal(ModalScreen[str]):
    """Prompt for an ethical-analysis situation."""

    BINDINGS = [Binding("escape", "dismiss", "Cancel")]

    def compose(self) -> ComposeResult:
        with Vertical(classes="modal"):
            yield Label("Describe the situation in one sentence:")
            yield Input(placeholder="e.g. Should I sue my landlord?", id="ethics-input")

    @on(Input.Submitted)
    def on_submit(self, event: Input.Submitted) -> None:
        self.dismiss(event.value)


class NewDecisionScreen(Screen):
    """Full-screen form to log a new decision."""

    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def __init__(self, client: ApiClient) -> None:
        super().__init__()
        self.client = client

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with VerticalScroll(id="decision-form"):
            yield Label("[bold]New decision[/bold]")
            yield Label("What's happening?")
            yield Input(id="d-situation")
            yield Label("Options (comma-separated)")
            yield Input(id="d-options", placeholder="Option A, Option B, Option C")
            yield Label("Which are you leaning toward?")
            yield Input(id="d-chosen")
            yield Label("Why? (be honest)")
            yield TextArea(id="d-reasoning")
            yield Label("What do you expect to happen?")
            yield Input(id="d-expected")
            yield Label("Confidence (0–100)")
            yield Input(id="d-confidence", value="60")
            with Horizontal(id="decision-buttons"):
                yield Button("Save", id="save", variant="primary")
                yield Button("Cancel", id="cancel")
        yield Footer()

    @on(Button.Pressed, "#save")
    def save(self) -> None:
        try:
            options_raw = self.query_one("#d-options", Input).value
            options = [o.strip() for o in options_raw.split(",") if o.strip()]
            if len(options) < 2:
                self.app.bell()
                self.notify("Need at least 2 options", severity="error")
                return
            d = DecisionCreate(
                situation=self.query_one("#d-situation", Input).value,
                options=options,
                chosen=self.query_one("#d-chosen", Input).value,
                reasoning=self.query_one("#d-reasoning", TextArea).text,
                expected_outcome=self.query_one("#d-expected", Input).value,
                confidence=int(self.query_one("#d-confidence", Input).value or "60"),
            )
            decision = self.client.create_decision(d)
            self.dismiss(decision)
        except Exception as exc:  # noqa: BLE001
            self.notify(f"Error: {exc}", severity="error")

    @on(Button.Pressed, "#cancel")
    def cancel(self) -> None:
        self.action_cancel()

    def action_cancel(self) -> None:
        self.dismiss(None)


# ──────────────────────────────────────────────────────────────────────────────
# Main app
# ──────────────────────────────────────────────────────────────────────────────


class PrismApp(App):
    CSS = """
    Screen { layout: vertical; }
    #main { height: 1fr; }
    #left-pane { width: 35; border-right: solid $primary; }
    #right-pane { padding: 1 2; }
    .modal {
        align: center middle;
        background: $boost;
        border: round $primary;
        padding: 1 2;
        width: 60;
        height: auto;
    }
    #decision-form { padding: 1 2; }
    #decision-form Input, #decision-form TextArea { margin-bottom: 1; }
    #decision-buttons { margin-top: 1; height: 3; }
    Button { margin-right: 2; }
    .bias-flag {
        border: solid yellow;
        padding: 0 1;
        margin: 0 0 1 0;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("slash", "search", "Search"),
        Binding("n", "new_decision", "New decision"),
        Binding("j", "list_decisions", "Decisions"),
        Binding("e", "ethics", "Ethics"),
        Binding("s", "stats", "Stats"),
        Binding("h", "home", "Home"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.client: ApiClient | None = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Horizontal(id="main"):
            with Vertical(id="left-pane"):
                yield Label("[bold]Domains[/bold]", id="domains-header")
                yield ListView(id="domain-list")
                yield Label("[bold]Scenarios[/bold]", id="scenarios-header")
                yield ListView(id="scenario-list")
            with VerticalScroll(id="right-pane"):
                yield Static("Loading…", id="content")
        yield Footer()

    async def on_mount(self) -> None:
        self.title = "Prism"
        self.sub_title = "Illinois legal & ethical reasoning"
        try:
            self.client = ApiClient()
            self.client.health()
        except PharosUnavailable:
            self.query_one("#content", Static).update(
                "[red]Cannot reach Pharos.[/red]\n\n"
                "Start the server in another terminal:\n\n"
                "    uv run pharos\n\n"
                "then quit this app and start it again."
            )
            return
        await self._load_domains()
        await self._show_home()

    async def _load_domains(self) -> None:
        if self.client is None:
            return
        list_view = self.query_one("#domain-list", ListView)
        await list_view.clear()
        for d in self.client.list_domains():
            item = ListItem(Label(f"{d.name}"))
            item.data = d.slug  # type: ignore[attr-defined]
            await list_view.append(item)

    async def _show_home(self) -> None:
        if self.client is None:
            return
        stats = self.client.stats()
        self.query_one("#content", Static).update(
            f"[bold]Welcome to Prism[/bold]\n\n"
            f"  Domains:   {stats.domains}\n"
            f"  Statutes:  {stats.statutes}\n"
            f"  Scenarios: {stats.scenarios}\n"
            f"  Decisions: {stats.decisions}\n"
            f"  Biases:    {stats.bias_flags}\n\n"
            f"[dim]Pick a domain on the left, or press / to search, "
            f"n for new decision, j for journal, e for ethics, q to quit.[/dim]"
        )

    @on(ListView.Selected, "#domain-list")
    async def on_domain_selected(self, event: ListView.Selected) -> None:
        if self.client is None or event.item is None:
            return
        slug = getattr(event.item, "data", None)
        if slug is None:
            return
        d = self.client.get_domain(slug)
        body = f"# {d.name}\n\n{d.summary}\n\n"
        if d.statutes:
            body += "## Statutes\n\n"
            for s in d.statutes:
                body += f"- **{s.citation}** — {s.title}\n"
        self.query_one("#content", Static).update(body)
        scenarios_view = self.query_one("#scenario-list", ListView)
        await scenarios_view.clear()
        for sc in d.scenarios:
            item = ListItem(Label(sc.title))
            item.data = sc.slug  # type: ignore[attr-defined]
            await scenarios_view.append(item)

    @on(ListView.Selected, "#scenario-list")
    async def on_scenario_selected(self, event: ListView.Selected) -> None:
        if self.client is None or event.item is None:
            return
        slug = getattr(event.item, "data", None)
        if slug is None:
            return
        sc = self.client.get_scenario(slug)
        body = f"# {sc.title}\n\n{sc.description_md}\n\n{sc.walkthrough_md}\n\n"
        if sc.statutes:
            body += "## Applicable statutes\n\n"
            for s in sc.statutes:
                body += f"- **{s.citation}** — {s.title}\n  {s.summary}\n\n"
        if sc.template_md:
            body += "\n" + sc.template_md
        self.query_one("#content", Static).update(body)

    async def action_search(self) -> None:
        if self.client is None:
            return
        query = await self.push_screen_wait(SearchModal())
        if not query:
            return
        hits = self.client.search(query)
        if not hits:
            self.query_one("#content", Static).update(f"No matches for '{query}'.")
            return
        body = f"# Search results for '{query}'\n\n"
        for h in hits:
            body += f"- [{h.kind}] **{h.title}** ({h.domain_slug})\n  {h.snippet}\n\n"
        self.query_one("#content", Static).update(body)

    async def action_ethics(self) -> None:
        if self.client is None:
            return
        situation = await self.push_screen_wait(EthicsModal())
        if not situation:
            return
        analysis = self.client.analyze_ethically(situation)
        body = f"# Ethical analysis\n\n*{analysis.situation}*\n\n"
        for p in analysis.perspectives:
            body += f"## {p.framework_name}\n\n{p.framing}\n\n**Key questions:**\n\n"
            for q in p.questions:
                body += f"- {q}\n"
            body += "\n"
        self.query_one("#content", Static).update(body)

    async def action_new_decision(self) -> None:
        if self.client is None:
            return
        decision = await self.push_screen_wait(NewDecisionScreen(self.client))
        if decision is None:
            return
        body = f"# Decision #{decision.id} logged\n\n"
        body += f"**Chose:** {decision.chosen}\n\n"
        body += f"**Confidence:** {decision.confidence}\n\n"
        if decision.biases:
            body += "## Bias flags\n\n"
            for b in decision.biases:
                body += f"- **{b.bias_slug}** — {b.evidence}\n\n"
        else:
            body += "_No bias flags raised._\n"
        self.query_one("#content", Static).update(body)

    async def action_list_decisions(self) -> None:
        if self.client is None:
            return
        decisions = self.client.list_decisions()
        if not decisions:
            self.query_one("#content", Static).update(
                "No decisions logged yet. Press [bold]n[/bold] to log one."
            )
            return
        body = "# Decision journal\n\n"
        for d in decisions:
            biases = ", ".join(b.bias_slug for b in d.biases) or "—"
            outcome = "✓" if d.actual_outcome else "—"
            body += (
                f"## #{d.id} — {d.created_at.strftime('%Y-%m-%d')}\n\n"
                f"*{d.situation}*\n\n"
                f"Chose: **{d.chosen}** (confidence {d.confidence}) — outcome: {outcome}\n\n"
                f"Biases: {biases}\n\n---\n\n"
            )
        self.query_one("#content", Static).update(body)

    async def action_stats(self) -> None:
        await self._show_home()

    async def action_home(self) -> None:
        await self._show_home()


def main() -> None:
    PrismApp().run()


if __name__ == "__main__":
    main()
