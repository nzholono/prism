# Testing Strategy

Three-layer test pyramid, organized by folder. `tests/conftest.py` auto-applies the right pytest marker based on which folder a test lives in, so you can run a slice with `uv run pytest -m unit`.

## tests/unit/ — pure logic

What's tested here:
- Bias detector rules (does "I already spent 20 hours on this" trigger sunk-cost?)
- Pydantic model validation
- Ethical framework prompt generation
- Pure helpers (slug normalization, citation parsing)

What's NOT here: anything that opens an HTTP connection or hits a real SQLite file. Unit tests should be fast (whole folder <1s).

## tests/contract/ — REST API shape

What's tested here:
- Every endpoint returns the expected status code for the happy path
- Response schema matches the documented contract (Pydantic validation passes)
- Error cases return the right 4xx codes with structured error bodies
- Pagination, filtering, sorting work as documented

Uses FastAPI's `TestClient` against the in-memory app. No real network. No client code involved — these test the *server's* contract.

## tests/integration/ — full stack

What's tested here:
- CLI commands produce the right output (via Typer's `CliRunner`)
- TUI navigation works end-to-end (via Textual's `Pilot`)
- Web client renders pages with real data
- A user scenario like "log a decision, check biases were flagged, mark outcome, query later" runs through CLI → ApiClient → server → DB and back

Each integration test gets a fresh SQLite DB (in-memory) via a fixture, so they don't pollute each other.

## conftest.py highlights

```python
# auto-mark by folder
def pytest_collection_modifyitems(config, items):
    for item in items:
        if "tests/unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "tests/contract" in str(item.fspath):
            item.add_marker(pytest.mark.contract)
        elif "tests/integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
```

```python
# in-process client for fast integration tests
@pytest.fixture
def in_process_client():
    from fastapi.testclient import TestClient
    from prism.server import create_app
    from prism.api_client import ApiClient

    app = create_app(db_url="sqlite:///:memory:")
    test_client = TestClient(app)
    return ApiClient(transport=test_client)
```

## What "good coverage" looks like for this project

Not chasing 100%. Aim:
- Every bias detector has at least 3 positive cases (triggers) and 3 negative cases (correctly does not trigger)
- Every REST endpoint has a happy-path contract test
- Every CLI subcommand has at least one integration test
- The decision-journal end-to-end flow is covered by at least one integration test
