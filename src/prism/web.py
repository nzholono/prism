"""Prism Web — FastAPI web UI on port 8001.

Separate process from Pharos. Every page renders by calling Pharos via the
shared ApiClient — proving the client/server split is real.

Run with `uv run prism-web` (Pharos must already be running on 8000).
"""

from __future__ import annotations

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from prism.api_client import ApiClient, PharosUnavailable
from prism.models import DecisionCreate, DecisionUpdate

# Templates are inlined below as constants so we don't need a templates/ folder.
# This keeps the project a single Python package while still using Jinja.


_BASE_CSS = """
<style>
  :root {
    --primary: #2c3e50;
    --primary-light: #34495e;
    --accent: #16a085;
    --warn: #f39c12;
    --danger: #c0392b;
    --text: #1d1d1f;
    --text-dim: #6e6e73;
    --bg: #fafafa;
    --card-bg: #ffffff;
    --border: #e4e4e7;
  }
  * { box-sizing: border-box; }
  body {
    font: 16px/1.6 -apple-system, BlinkMacSystemFont, "SF Pro Text",
          system-ui, sans-serif;
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem 1.2rem 4rem;
    color: var(--text);
    background: var(--bg);
  }
  h1 { font-size: 2.2rem; font-weight: 700; margin-top: 0;
       letter-spacing: -0.02em; color: var(--primary); }
  h2 { font-size: 1.5rem; font-weight: 600; margin-top: 2rem;
       color: var(--primary); }
  h3 { font-size: 1.15rem; font-weight: 600; color: var(--primary); }
  p { margin: 0.6rem 0; }
  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }

  nav {
    display: flex; gap: 0.4rem; align-items: center;
    background: var(--primary);
    padding: 0.7rem 1.2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    box-shadow: 0 2px 8px rgba(44, 62, 80, 0.15);
  }
  nav .brand {
    color: white; font-weight: 700; font-size: 1.1rem;
    margin-right: auto; letter-spacing: 0.02em;
  }
  nav a {
    color: rgba(255,255,255,0.85);
    padding: 0.3rem 0.8rem;
    border-radius: 6px;
    font-weight: 500;
    transition: background 0.15s;
  }
  nav a:hover {
    background: rgba(255,255,255,0.12);
    color: white;
    text-decoration: none;
  }

  .card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: box-shadow 0.15s, transform 0.05s;
  }
  .card:hover { box-shadow: 0 4px 14px rgba(0,0,0,0.08); }
  .card h3 { margin-top: 0; }
  .card h3 a { color: var(--primary); }
  .card h3 a:hover { color: var(--accent); text-decoration: none; }

  .tag {
    display: inline-block;
    padding: 0.15rem 0.55rem;
    background: #ecf0f1;
    color: var(--text-dim);
    border-radius: 4px;
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-right: 0.4rem;
  }
  .tag.tier1 { background: #d4efdf; color: #196f3d; }
  .tag.tier2 { background: #fdebd0; color: #9c6310; }

  .bias {
    background: linear-gradient(to right, #fff8dc, #fffbe6);
    border-left: 4px solid var(--warn);
    padding: 0.7rem 1.1rem;
    margin: 0.7rem 0;
    border-radius: 0 6px 6px 0;
  }
  .bias strong { color: #9c6310; text-transform: uppercase;
                 font-size: 0.78rem; letter-spacing: 0.05em; }

  .scenario-body, .scenario-body pre { white-space: pre-wrap;
                                       line-height: 1.7; }
  pre {
    background: #f5f5f7;
    border-radius: 6px;
    padding: 0.9rem 1.1rem;
    overflow-x: auto;
    font: 13px/1.5 ui-monospace, "SF Mono", Menlo, monospace;
  }

  form label {
    display: block;
    margin-top: 1rem;
    font-weight: 600;
    color: var(--primary);
    font-size: 0.92rem;
  }
  form input, form textarea {
    width: 100%;
    padding: 0.55rem 0.7rem;
    border: 1px solid var(--border);
    border-radius: 6px;
    font-size: 1rem;
    font-family: inherit;
    background: white;
    transition: border-color 0.15s;
  }
  form input:focus, form textarea:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(22, 160, 133, 0.15);
  }
  form textarea { min-height: 5rem; resize: vertical; }

  button {
    background: var(--primary);
    color: white;
    border: none;
    padding: 0.65rem 1.4rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.95rem;
    font-weight: 600;
    margin-top: 1.2rem;
    transition: background 0.15s, transform 0.05s;
  }
  button:hover { background: var(--primary-light); }
  button:active { transform: translateY(1px); }

  .error {
    color: var(--danger);
    background: #fadbd8;
    padding: 0.8rem 1.2rem;
    border-radius: 6px;
    border-left: 4px solid var(--danger);
  }
  .stat-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 1rem; margin: 1rem 0;
  }
  .stat-card {
    background: white; padding: 1rem; border-radius: 8px;
    border: 1px solid var(--border); text-align: center;
  }
  .stat-card .num { font-size: 2.2rem; font-weight: 700;
                    color: var(--primary); line-height: 1; }
  .stat-card .lbl { font-size: 0.85rem; color: var(--text-dim);
                    text-transform: uppercase; letter-spacing: 0.04em;
                    margin-top: 0.4rem; }

  footer {
    margin-top: 4rem;
    color: var(--text-dim);
    font-size: 0.85rem;
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
  }
  .citation {
    color: var(--accent);
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 0.92em;
    background: rgba(22, 160, 133, 0.08);
    padding: 0.1rem 0.4rem;
    border-radius: 3px;
  }
  .disclaimer {
    background: #fff3cd; color: #856404; padding: 0.7rem 1rem;
    border-radius: 6px; font-size: 0.9rem; margin: 1rem 0;
    border-left: 3px solid #ffe57f;
  }
</style>
"""

_NAV = """
<nav>
  <a href="/" class="brand">◇ Prism</a>
  <a href="/domains">Rights</a>
  <a href="/decisions">Decisions</a>
  <a href="/ethics">Ethics</a>
  <a href="/search">Search</a>
  <a href="/stats">Stats</a>
</nav>
"""


def _page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{title} — Prism</title>{_BASE_CSS}</head>
<body>
{_NAV}
{body}
<footer>Prism — Illinois legal &amp; ethical reasoning. Not legal advice.</footer>
</body></html>"""


def _markdown_to_html(md: str) -> str:
    """Convert markdown to HTML using the `markdown` library.

    Supports headings, lists, bold/italic, links, fenced code blocks, and
    tables — much better than the hand-rolled version that came before.
    """
    import markdown as md_lib

    return md_lib.markdown(
        md,
        extensions=["extra", "sane_lists", "tables", "fenced_code", "nl2br"],
    )


def create_app(pharos_url: str = "http://127.0.0.1:8000") -> FastAPI:
    app = FastAPI(title="Prism Web")

    def get_client() -> ApiClient:
        return ApiClient(base_url=pharos_url)

    def _unavailable() -> HTMLResponse:
        return HTMLResponse(
            _page(
                "Server unavailable",
                f"<div class='error'>Cannot reach Pharos at {pharos_url}. "
                f"Start it in another terminal with <code>uv run pharos</code>.</div>",
            ),
            status_code=503,
        )

    @app.get("/", response_class=HTMLResponse)
    def home(client: ApiClient = Depends(get_client)) -> HTMLResponse:
        try:
            stats = client.stats()
        except PharosUnavailable:
            return _unavailable()
        body = (
            "<h1>Prism</h1>"
            "<p style='font-size: 1.15rem; color: var(--text-dim); margin-bottom: 2rem;'>"
            "Illinois legal &amp; ethical reasoning — through three lenses."
            "</p>"
            "<div class='stat-grid'>"
            f"<div class='stat-card'><div class='num'>{stats.domains}</div>"
            f"<div class='lbl'>Domains</div></div>"
            f"<div class='stat-card'><div class='num'>{stats.statutes}</div>"
            f"<div class='lbl'>Statutes</div></div>"
            f"<div class='stat-card'><div class='num'>{stats.scenarios}</div>"
            f"<div class='lbl'>Scenarios</div></div>"
            f"<div class='stat-card'><div class='num'>{stats.decisions}</div>"
            f"<div class='lbl'>Decisions</div></div>"
            "</div>"
            "<div class='card'><h3>The three lenses</h3>"
            "<p><strong>Legal lens</strong> — What Illinois &amp; Chicago law actually "
            "says, with walkthroughs and templates.</p>"
            "<p><strong>Ethical lens</strong> — Four frameworks (utilitarian, "
            "deontological, virtue, care) framing the same choice differently.</p>"
            "<p><strong>Cognitive lens</strong> — A decision journal that flags "
            "ten cognitive biases before you commit.</p>"
            "</div>"
            "<div class='card'><h3>Start here</h3>"
            "<ul>"
            "<li><a href='/domains'>Browse legal rights</a> — by domain</li>"
            "<li><a href='/decisions/new'>Log a decision</a> — get automatic bias detection</li>"
            "<li><a href='/ethics'>Analyze a situation ethically</a></li>"
            "<li><a href='/search'>Search</a> across all statutes and scenarios</li>"
            "</ul></div>"
            "<div class='disclaimer'>This is reference material, not legal advice. "
            "For your specific situation, contact a licensed Illinois attorney or one of "
            "the free legal aid resources listed in each scenario.</div>"
        )
        return HTMLResponse(_page("Home", body))

    @app.get("/domains", response_class=HTMLResponse)
    def list_domains(client: ApiClient = Depends(get_client)) -> HTMLResponse:
        try:
            domains = client.list_domains()
        except PharosUnavailable:
            return _unavailable()
        body = "<h1>Legal domains</h1>"
        body += (
            "<p style='color: var(--text-dim);'>"
            "Tier 1 domains have multiple scenarios with deep walkthroughs. "
            "Tier 2 are scaffolded — extend them via the <code>add-scenario</code> "
            "Claude skill.</p>"
        )
        for d in domains:
            tier_cls = "tier1" if d.tier == 1 else "tier2"
            body += (
                f"<div class='card'>"
                f"<h3><a href='/domains/{d.slug}'>{d.name}</a> "
                f"<span class='tag {tier_cls}'>Tier {d.tier}</span></h3>"
                f"<p>{d.summary}</p></div>"
            )
        return HTMLResponse(_page("Domains", body))

    @app.get("/domains/{slug}", response_class=HTMLResponse)
    def domain_detail(slug: str, client: ApiClient = Depends(get_client)) -> HTMLResponse:
        try:
            d = client.get_domain(slug)
        except PharosUnavailable:
            return _unavailable()
        body = f"<h1>{d.name}</h1><p>{d.summary}</p>"
        if d.scenarios:
            body += "<h2>Scenarios</h2>"
            for sc in d.scenarios:
                body += (
                    f"<div class='card'>"
                    f"<h3><a href='/scenarios/{sc.slug}'>{sc.title}</a></h3>"
                    f"</div>"
                )
        if d.statutes:
            body += "<h2>Statutes</h2>"
            for st in d.statutes:
                body += (
                    f"<div class='card'>"
                    f"<h4><span class='citation'>{st.citation}</span> — {st.title}</h4>"
                    f"<p>{st.summary}</p>"
                    + (
                        f"<p><a href='{st.source_url}' target='_blank'>Source</a></p>"
                        if st.source_url
                        else ""
                    )
                    + "</div>"
                )
        return HTMLResponse(_page(d.name, body))

    @app.get("/scenarios/{slug}", response_class=HTMLResponse)
    def scenario_detail(slug: str, client: ApiClient = Depends(get_client)) -> HTMLResponse:
        try:
            sc = client.get_scenario(slug)
        except PharosUnavailable:
            return _unavailable()
        body = (
            f"<h1>{sc.title}</h1>"
            f"<div class='card'><h3>What's going on</h3>{_markdown_to_html(sc.description_md)}</div>"
            f"<div class='card scenario-body'><h3>What to do</h3>"
            f"{_markdown_to_html(sc.walkthrough_md)}</div>"
        )
        if sc.statutes:
            body += "<div class='card'><h3>Applicable statutes</h3>"
            for st in sc.statutes:
                body += (
                    f"<p><span class='citation'>{st.citation}</span> — "
                    f"<strong>{st.title}</strong><br>{st.summary}</p>"
                )
            body += "</div>"
        if sc.template_md:
            body += (
                f"<div class='card scenario-body'><h3>Template</h3>"
                f"{_markdown_to_html(sc.template_md)}</div>"
            )
        return HTMLResponse(_page(sc.title, body))

    @app.get("/search", response_class=HTMLResponse)
    def search_form(q: str = "", client: ApiClient = Depends(get_client)) -> HTMLResponse:
        body = (
            "<h1>Search</h1>"
            f"<form method='get'><input name='q' value='{q}' placeholder='deposit'>"
            "<button type='submit'>Search</button></form>"
        )
        if q:
            try:
                hits = client.search(q)
            except PharosUnavailable:
                return _unavailable()
            if not hits:
                body += f"<p>No matches for '{q}'.</p>"
            for h in hits:
                link = f"/scenarios/{h.title}" if h.kind == "scenario" else f"/domains/{h.domain_slug}"
                body += (
                    f"<div class='card'><span class='tag'>{h.kind}</span> "
                    f"<a href='/domains/{h.domain_slug}'>{h.title}</a><br>"
                    f"<small>{h.snippet}</small></div>"
                )
        return HTMLResponse(_page("Search", body))

    @app.get("/ethics", response_class=HTMLResponse)
    def ethics_form() -> HTMLResponse:
        body = (
            "<h1>Ethical analysis</h1>"
            "<p>Describe a situation. Prism will frame it through four ethical lenses.</p>"
            "<form method='post' action='/ethics'>"
            "<label>Situation</label>"
            "<textarea name='situation' placeholder='Should I sue my landlord?'></textarea>"
            "<button type='submit'>Analyze</button></form>"
        )
        return HTMLResponse(_page("Ethics", body))

    @app.post("/ethics", response_class=HTMLResponse)
    def ethics_submit(
        situation: str = Form(...), client: ApiClient = Depends(get_client)
    ) -> HTMLResponse:
        try:
            analysis = client.analyze_ethically(situation)
        except PharosUnavailable:
            return _unavailable()
        body = (
            f"<h1>Ethical analysis</h1>"
            f"<p><em>{analysis.situation}</em></p>"
        )
        for p in analysis.perspectives:
            qs = "".join(f"<li>{q}</li>" for q in p.questions)
            body += (
                f"<div class='card'><h3>{p.framework_name}</h3>"
                f"<p>{p.framing}</p>"
                f"<p><strong>Key questions:</strong></p><ul>{qs}</ul></div>"
            )
        return HTMLResponse(_page("Ethics", body))

    @app.get("/decisions", response_class=HTMLResponse)
    def decisions_list(client: ApiClient = Depends(get_client)) -> HTMLResponse:
        try:
            decisions = client.list_decisions()
        except PharosUnavailable:
            return _unavailable()
        body = (
            "<h1>Decision journal</h1>"
            "<p><a href='/decisions/new'>+ New decision</a></p>"
        )
        if not decisions:
            body += "<p>No decisions logged yet.</p>"
        for d in decisions:
            biases = ", ".join(b.bias_slug for b in d.biases) or "—"
            outcome = d.actual_outcome or "<em>not yet reviewed</em>"
            body += (
                f"<div class='card'>"
                f"<h3><a href='/decisions/{d.id}'>#{d.id}: {d.situation[:60]}</a></h3>"
                f"<p>Chose: <strong>{d.chosen}</strong> · Confidence: {d.confidence} · "
                f"Date: {d.created_at.strftime('%Y-%m-%d')}</p>"
                f"<p><span class='tag'>biases</span> {biases}</p>"
                f"<p><span class='tag'>outcome</span> {outcome}</p>"
                f"</div>"
            )
        return HTMLResponse(_page("Decisions", body))

    @app.get("/decisions/new", response_class=HTMLResponse)
    def decision_new_form() -> HTMLResponse:
        body = (
            "<h1>New decision</h1>"
            "<form method='post' action='/decisions/new'>"
            "<label>Situation</label><input name='situation'>"
            "<label>Options (comma-separated)</label><input name='options' placeholder='A, B, C'>"
            "<label>Chosen</label><input name='chosen'>"
            "<label>Reasoning (be honest)</label><textarea name='reasoning'></textarea>"
            "<label>Expected outcome</label><input name='expected_outcome'>"
            "<label>Confidence (0–100)</label><input name='confidence' value='60'>"
            "<button type='submit'>Save</button></form>"
        )
        return HTMLResponse(_page("New decision", body))

    @app.post("/decisions/new", response_class=HTMLResponse)
    def decision_new_submit(
        situation: str = Form(...),
        options: str = Form(...),
        chosen: str = Form(...),
        reasoning: str = Form(...),
        expected_outcome: str = Form(...),
        confidence: int = Form(60),
        client: ApiClient = Depends(get_client),
    ) -> HTMLResponse:
        opts = [o.strip() for o in options.split(",") if o.strip()]
        d = DecisionCreate(
            situation=situation,
            options=opts,
            chosen=chosen,
            reasoning=reasoning,
            expected_outcome=expected_outcome,
            confidence=confidence,
        )
        try:
            decision = client.create_decision(d)
        except PharosUnavailable:
            return _unavailable()
        return RedirectResponse(f"/decisions/{decision.id}", status_code=303)

    @app.get("/decisions/{decision_id}", response_class=HTMLResponse)
    def decision_show(
        decision_id: int, client: ApiClient = Depends(get_client)
    ) -> HTMLResponse:
        try:
            d = client.get_decision(decision_id)
        except PharosUnavailable:
            return _unavailable()
        body = (
            f"<h1>Decision #{d.id}</h1>"
            f"<div class='card'>"
            f"<p><strong>Situation:</strong> {d.situation}</p>"
            f"<p><strong>Options:</strong> {', '.join(d.options)}</p>"
            f"<p><strong>Chose:</strong> {d.chosen} (confidence {d.confidence})</p>"
            f"<p><strong>Expected:</strong> {d.expected_outcome}</p>"
            f"<p><strong>Reasoning:</strong><br>{d.reasoning}</p>"
            f"</div>"
        )
        if d.biases:
            body += "<h3>Bias flags</h3>"
            for b in d.biases:
                body += (
                    f"<div class='bias'><strong>{b.bias_slug}</strong><br>{b.evidence}</div>"
                )
        if d.actual_outcome:
            body += (
                f"<div class='card'><h3>Actual outcome</h3>"
                f"<p>{d.actual_outcome}</p></div>"
            )
        else:
            body += (
                f"<div class='card'><h3>Record what happened</h3>"
                f"<form method='post' action='/decisions/{d.id}/review'>"
                f"<textarea name='actual_outcome'></textarea>"
                f"<button type='submit'>Save outcome</button></form></div>"
            )
        return HTMLResponse(_page(f"Decision #{d.id}", body))

    @app.post("/decisions/{decision_id}/review", response_class=HTMLResponse)
    def decision_review(
        decision_id: int,
        actual_outcome: str = Form(...),
        client: ApiClient = Depends(get_client),
    ) -> RedirectResponse:
        try:
            client.update_decision(decision_id, DecisionUpdate(actual_outcome=actual_outcome))
        except PharosUnavailable:
            pass
        return RedirectResponse(f"/decisions/{decision_id}", status_code=303)

    @app.get("/stats", response_class=HTMLResponse)
    def stats_page(client: ApiClient = Depends(get_client)) -> HTMLResponse:
        try:
            stats = client.stats()
        except PharosUnavailable:
            return _unavailable()
        body = (
            "<h1>Stats</h1>"
            f"<div class='card'>"
            f"<ul>"
            f"<li>Domains: {stats.domains}</li>"
            f"<li>Statutes: {stats.statutes}</li>"
            f"<li>Scenarios: {stats.scenarios}</li>"
            f"<li>Decisions: {stats.decisions}</li>"
            f"<li>Bias flags raised: {stats.bias_flags}</li>"
            f"</ul></div>"
        )
        return HTMLResponse(_page("Stats", body))

    return app


app = create_app()


def main() -> None:
    """Entry point for `uv run prism-web`."""
    import uvicorn

    uvicorn.run("prism.web:app", host="127.0.0.1", port=8001, reload=False)


if __name__ == "__main__":
    main()
