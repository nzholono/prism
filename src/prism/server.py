"""Pharos — the REST server.

Owns the SQLite database. Every other process is a client that talks to Pharos
over HTTP. Run with `uv run pharos`.
"""

from __future__ import annotations

import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Iterator

from fastapi import Depends, FastAPI, HTTPException

from prism import __version__, db, service
from prism.models import (
    Decision,
    DecisionCreate,
    DecisionUpdate,
    Domain,
    DomainDetail,
    EthicalAnalysis,
    EthicalAnalysisRequest,
    EthicalFramework,
    HealthResponse,
    Scenario,
    SearchHit,
    Stats,
    Statute,
)
from prism.seed import seed_all


def create_app(db_path: str | Path | None = None) -> FastAPI:
    """Build the FastAPI app. `db_path` overrides the default for tests."""

    # Hold one shared connection per app — sqlite3 is fine for this with
    # check_same_thread=False (set in db.connect).
    state: dict[str, sqlite3.Connection] = {}

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        conn = db.connect(db_path)
        db.init_schema(conn)
        seed_all(conn)
        state["conn"] = conn
        try:
            yield
        finally:
            conn.close()
            state.pop("conn", None)

    app = FastAPI(
        title="Pharos",
        description="REST server for Prism — Illinois legal & ethical reasoning framework.",
        version=__version__,
        lifespan=lifespan,
    )

    def get_conn() -> Iterator[sqlite3.Connection]:
        yield state["conn"]

    # ── meta ────────────────────────────────────────────────────────────────

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(status="ok", version=__version__)

    @app.get("/stats", response_model=Stats)
    def stats(conn: sqlite3.Connection = Depends(get_conn)) -> Stats:
        return service.get_stats(conn)

    # ── legal ───────────────────────────────────────────────────────────────

    @app.get("/domains", response_model=list[Domain])
    def list_domains(conn: sqlite3.Connection = Depends(get_conn)) -> list[Domain]:
        return service.list_domains(conn)

    @app.get("/domains/{slug}", response_model=DomainDetail)
    def get_domain(slug: str, conn: sqlite3.Connection = Depends(get_conn)) -> DomainDetail:
        domain = service.get_domain(conn, slug)
        if domain is None:
            raise HTTPException(status_code=404, detail=f"Domain not found: {slug}")
        return domain

    @app.get("/scenarios", response_model=list[Scenario])
    def list_scenarios(
        domain: str | None = None,
        q: str | None = None,
        conn: sqlite3.Connection = Depends(get_conn),
    ) -> list[Scenario]:
        return service.list_scenarios(conn, domain_slug=domain, query=q)

    @app.get("/scenarios/{slug}", response_model=Scenario)
    def get_scenario(slug: str, conn: sqlite3.Connection = Depends(get_conn)) -> Scenario:
        sc = service.get_scenario(conn, slug)
        if sc is None:
            raise HTTPException(status_code=404, detail=f"Scenario not found: {slug}")
        return sc

    @app.get("/statutes/{statute_id}", response_model=Statute)
    def get_statute(statute_id: int, conn: sqlite3.Connection = Depends(get_conn)) -> Statute:
        st = service.get_statute(conn, statute_id)
        if st is None:
            raise HTTPException(status_code=404, detail=f"Statute not found: {statute_id}")
        return st

    @app.get("/search", response_model=list[SearchHit])
    def search(q: str, limit: int = 20, conn: sqlite3.Connection = Depends(get_conn)) -> list[SearchHit]:
        return service.search(conn, q, limit=limit)

    # ── ethical ─────────────────────────────────────────────────────────────

    @app.get("/ethics/frameworks", response_model=list[EthicalFramework])
    def list_frameworks(conn: sqlite3.Connection = Depends(get_conn)) -> list[EthicalFramework]:
        return service.list_ethical_frameworks(conn)

    @app.post("/ethics/analyze", response_model=EthicalAnalysis)
    def ethics_analyze(
        req: EthicalAnalysisRequest, conn: sqlite3.Connection = Depends(get_conn)
    ) -> EthicalAnalysis:
        return service.analyze_ethically(conn, req.situation)

    # ── cognitive ───────────────────────────────────────────────────────────

    @app.post("/decisions", response_model=Decision, status_code=201)
    def create_decision(
        d: DecisionCreate, conn: sqlite3.Connection = Depends(get_conn)
    ) -> Decision:
        return service.create_decision(conn, d)

    @app.get("/decisions", response_model=list[Decision])
    def list_decisions(
        limit: int = 50, conn: sqlite3.Connection = Depends(get_conn)
    ) -> list[Decision]:
        return service.list_decisions(conn, limit=limit)

    @app.get("/decisions/{decision_id}", response_model=Decision)
    def get_decision(
        decision_id: int, conn: sqlite3.Connection = Depends(get_conn)
    ) -> Decision:
        d = service.get_decision(conn, decision_id)
        if d is None:
            raise HTTPException(status_code=404, detail=f"Decision not found: {decision_id}")
        return d

    @app.patch("/decisions/{decision_id}", response_model=Decision)
    def update_decision(
        decision_id: int,
        update: DecisionUpdate,
        conn: sqlite3.Connection = Depends(get_conn),
    ) -> Decision:
        d = service.update_decision(conn, decision_id, update)
        if d is None:
            raise HTTPException(status_code=404, detail=f"Decision not found: {decision_id}")
        return d

    @app.delete("/decisions/{decision_id}", status_code=204)
    def delete_decision(
        decision_id: int, conn: sqlite3.Connection = Depends(get_conn)
    ) -> None:
        ok = service.delete_decision(conn, decision_id)
        if not ok:
            raise HTTPException(status_code=404, detail=f"Decision not found: {decision_id}")

    return app


# Module-level app for `uvicorn prism.server:app`
app = create_app()


def main() -> None:
    """Entry point for `uv run pharos`."""
    import uvicorn

    uvicorn.run("prism.server:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()
