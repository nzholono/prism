"""Integration tests for the CLI through Typer's CliRunner.

Uses monkeypatching to point `ApiClient()` (the default constructor used by
the CLI) at our in-process seeded app.
"""

from __future__ import annotations

import pytest
from typer.testing import CliRunner


@pytest.fixture
def cli_runner(in_process_client, monkeypatch):
    """A Typer CliRunner whose ApiClient calls land in the in-process app."""
    from prism import cli

    monkeypatch.setattr(cli, "ApiClient", lambda *_a, **_kw: in_process_client)
    return CliRunner(), cli.app


def test_health_command(cli_runner):
    runner, app = cli_runner
    result = runner.invoke(app, ["health"])
    assert result.exit_code == 0
    assert "OK" in result.stdout


def test_stats_command(cli_runner):
    runner, app = cli_runner
    result = runner.invoke(app, ["stats"])
    assert result.exit_code == 0
    assert "Domains" in result.stdout


def test_rights_list_includes_tenant(cli_runner):
    runner, app = cli_runner
    result = runner.invoke(app, ["rights"])
    assert result.exit_code == 0
    assert "tenant" in result.stdout.lower()


def test_rights_show_scenario(cli_runner):
    runner, app = cli_runner
    result = runner.invoke(app, ["rights", "show", "deposit-not-returned"])
    assert result.exit_code == 0
    assert "deposit" in result.stdout.lower()
    assert "765 ILCS" in result.stdout


def test_search_command_finds_deposit(cli_runner):
    runner, app = cli_runner
    result = runner.invoke(app, ["search", "deposit"])
    assert result.exit_code == 0
    assert "deposit" in result.stdout.lower()


def test_ethics_frameworks_command(cli_runner):
    runner, app = cli_runner
    result = runner.invoke(app, ["ethics", "frameworks"])
    assert result.exit_code == 0
    assert "Utilitarian" in result.stdout
