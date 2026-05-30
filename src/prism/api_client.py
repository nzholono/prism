"""ApiClient — the one HTTP wrapper every client uses.

The four UI clients (CLI, TUI, Web, GUI) and the MCP server all go through this
class. Adding a new endpoint = adding one method here, and every client gets it.
"""

from __future__ import annotations

from typing import Any

import httpx

from prism.models import (
    Decision,
    DecisionCreate,
    DecisionUpdate,
    Domain,
    DomainDetail,
    EthicalAnalysis,
    EthicalFramework,
    HealthResponse,
    Scenario,
    SearchHit,
    Stats,
    Statute,
)

DEFAULT_BASE_URL = "http://127.0.0.1:8000"


class PharosUnavailable(RuntimeError):
    """Raised when the server can't be reached. Clients should show a friendly hint."""


class ApiClient:
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        transport: httpx.BaseTransport | None = None,
        timeout: float = 5.0,
    ) -> None:
        self._client = httpx.Client(
            base_url=base_url,
            transport=transport,
            timeout=timeout,
        )

    # ── meta ────────────────────────────────────────────────────────────────
    def health(self) -> HealthResponse:
        return HealthResponse.model_validate(self._get("/health"))

    def stats(self) -> Stats:
        return Stats.model_validate(self._get("/stats"))

    # ── legal ───────────────────────────────────────────────────────────────
    def list_domains(self) -> list[Domain]:
        return [Domain.model_validate(d) for d in self._get("/domains")]

    def get_domain(self, slug: str) -> DomainDetail:
        return DomainDetail.model_validate(self._get(f"/domains/{slug}"))

    def list_scenarios(
        self, domain: str | None = None, q: str | None = None
    ) -> list[Scenario]:
        params: dict[str, Any] = {}
        if domain:
            params["domain"] = domain
        if q:
            params["q"] = q
        return [Scenario.model_validate(s) for s in self._get("/scenarios", **params)]

    def get_scenario(self, slug: str) -> Scenario:
        return Scenario.model_validate(self._get(f"/scenarios/{slug}"))

    def get_statute(self, statute_id: int) -> Statute:
        return Statute.model_validate(self._get(f"/statutes/{statute_id}"))

    def search(self, query: str, limit: int = 20) -> list[SearchHit]:
        return [SearchHit.model_validate(h) for h in self._get("/search", q=query, limit=limit)]

    # ── ethical ─────────────────────────────────────────────────────────────
    def list_ethical_frameworks(self) -> list[EthicalFramework]:
        return [EthicalFramework.model_validate(f) for f in self._get("/ethics/frameworks")]

    def analyze_ethically(self, situation: str) -> EthicalAnalysis:
        return EthicalAnalysis.model_validate(
            self._post("/ethics/analyze", {"situation": situation})
        )

    # ── cognitive (decisions) ───────────────────────────────────────────────
    def create_decision(self, d: DecisionCreate) -> Decision:
        return Decision.model_validate(self._post("/decisions", d.model_dump()))

    def list_decisions(self, limit: int = 50) -> list[Decision]:
        return [Decision.model_validate(d) for d in self._get("/decisions", limit=limit)]

    def get_decision(self, decision_id: int) -> Decision:
        return Decision.model_validate(self._get(f"/decisions/{decision_id}"))

    def update_decision(self, decision_id: int, update: DecisionUpdate) -> Decision:
        return Decision.model_validate(
            self._patch(f"/decisions/{decision_id}", update.model_dump(exclude_none=True))
        )

    def delete_decision(self, decision_id: int) -> None:
        self._delete(f"/decisions/{decision_id}")

    # ── internal ────────────────────────────────────────────────────────────
    def _get(self, path: str, **params: Any) -> Any:
        return self._request("GET", path, params=params or None)

    def _post(self, path: str, body: Any) -> Any:
        return self._request("POST", path, json=body)

    def _patch(self, path: str, body: Any) -> Any:
        return self._request("PATCH", path, json=body)

    def _delete(self, path: str) -> Any:
        return self._request("DELETE", path)

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        try:
            r = self._client.request(method, path, **kwargs)
        except httpx.HTTPError as exc:
            raise PharosUnavailable(
                f"Cannot reach Pharos at {self._client.base_url}. "
                "Did you start it with `uv run pharos`?"
            ) from exc
        r.raise_for_status()
        if r.status_code == 204 or not r.content:
            return None
        return r.json()

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "ApiClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def make_in_process_client(test_client: Any) -> ApiClient:
    """Build an ApiClient that delegates to a FastAPI TestClient.

    Pass an *entered* TestClient (its lifespan must already be running so the
    DB is seeded). Internally we delegate through httpx.MockTransport so the
    sync ApiClient code path is unchanged.
    """

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if request.url.query:
            path = f"{path}?{request.url.query.decode()}"
        response = test_client.request(
            method=request.method,
            url=path,
            content=request.content,
            headers=dict(request.headers),
        )
        return httpx.Response(
            status_code=response.status_code,
            headers=response.headers,
            content=response.content,
        )

    transport = httpx.MockTransport(handler)
    return ApiClient(base_url="http://testserver", transport=transport)
