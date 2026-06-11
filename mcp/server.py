#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp>=1.2"]
# ///
"""MCP server for best-of-Agent-Harnesses.

Serves the curated list (harnesses.json) as tools so agents can recommend
agent harnesses: pick_harness, search_harnesses, get_harness, list_categories.

Run directly from GitHub (no clone needed):
    uv run https://raw.githubusercontent.com/RyanAlberts/best-of-Agent-Harnesses/main/mcp/server.py
"""

import json
import re
import urllib.request
from pathlib import Path

from mcp.server.fastmcp import FastMCP

DATA_URL = "https://raw.githubusercontent.com/RyanAlberts/best-of-Agent-Harnesses/main/harnesses.json"

mcp = FastMCP("agent-harnesses")

_data: dict | None = None


def data() -> dict:
    global _data
    if _data is None:
        local = Path(__file__).resolve().parent.parent / "harnesses.json"
        if local.exists():
            _data = json.loads(local.read_text())
        else:
            with urllib.request.urlopen(DATA_URL, timeout=15) as r:
                _data = json.loads(r.read().decode())
    return _data


_STOP = {"i", "a", "an", "the", "to", "for", "of", "in", "on", "with", "and",
         "or", "my", "me", "want", "need", "agent", "agents", "ai", "llm"}


def _tokens(text: str) -> set:
    return {w for w in re.findall(r"[a-z0-9+#-]+", text.lower()) if w not in _STOP}


def _brief(p: dict, reason: str = "") -> dict:
    out = {
        "name": p["name"],
        "github_id": p["github_id"],
        "url": p["url"],
        "stars": p["stars"],
        "tier": p["tier"],
        "license_signal": p["license_signal"],
        "category": p["category_title"],
        "description": p["description"],
        "tags": p["tags"],
    }
    if reason:
        out["why"] = reason
    return out


@mcp.tool()
def pick_harness(use_case: str, max_complexity: str = "complex",
                 open_source_only: bool = False, limit: int = 5) -> str:
    """Recommend agent harnesses for a use case, ranked from a hand-curated list of 101.

    use_case: what you want to do, e.g. "terminal coding agent", "drop-in memory
    layer", "evaluate agents on coding benchmarks".
    max_complexity: cap on adoption surface — one of "super simple",
    "mostly simple", "slightly complex", "complex" (default: no cap).
    open_source_only: drop projects with restricted or unknown licenses.
    Returns JSON: ranked picks with a one-line reason each.
    """
    d = data()
    tiers: list = d["meta"]["tiers"]
    max_rank = tiers.index(max_complexity) + 1 if max_complexity in tiers else 4
    q = _tokens(use_case)

    # Curated use-case intents are the strongest signal: best word-overlap intent
    # seeds its hand-picked projects to the top, in curated order.
    seeded: dict = {}
    best = max(d["use_cases"], key=lambda u: len(q & _tokens(u["intent"])), default=None)
    if best and len(q & _tokens(best["intent"])) >= 2:
        for rank, gid in enumerate(best["picks"]):
            seeded[gid] = (100 - rank, f"curated pick for \"{best['intent']}\"")

    import math
    scored = []
    for p in d["projects"]:
        if p["tier_rank"] > max_rank:
            continue
        if open_source_only and p["license_signal"] != "open-source":
            continue
        if p["github_id"] in seeded:
            score, reason = seeded[p["github_id"]]
        else:
            overlap = q & _tokens(f"{p['description']} {' '.join(p['tags'])} {p['category_title']}")
            if not overlap:
                continue
            score = len(overlap) * 3 + math.log10(max(p["stars"], 2))
            reason = "matches: " + ", ".join(sorted(overlap))
        scored.append((score, p, reason))

    scored.sort(key=lambda t: -t[0])
    picks = [_brief(p, reason) for _, p, reason in scored[:limit]]
    return json.dumps({
        "use_case": use_case,
        "picks": picks,
        "source": d["meta"]["url"],
        "stars_captured": d["meta"]["stars_captured"],
    }, indent=2, ensure_ascii=False)


@mcp.tool()
def search_harnesses(query: str, limit: int = 10) -> str:
    """Keyword search across all 101 projects (name, description, tags, category).

    Returns JSON: matching projects sorted by relevance then stars.
    """
    d = data()
    q = _tokens(query)
    ql = query.lower()
    import math
    scored = []
    for p in d["projects"]:
        hay = f"{p['name']} {p['github_id']} {p['description']} {' '.join(p['tags'])} {p['category_title']}"
        name_hit = 50 if ql in p["name"].lower() or ql in p["github_id"].lower() else 0
        overlap = q & _tokens(hay)
        if not (name_hit or overlap):
            continue
        scored.append((name_hit + len(overlap) * 3 + math.log10(max(p["stars"], 2)), p))
    scored.sort(key=lambda t: -t[0])
    return json.dumps({"query": query, "results": [_brief(p) for _, p in scored[:limit]]},
                      indent=2, ensure_ascii=False)


@mcp.tool()
def get_harness(github_id: str) -> str:
    """Full record for one project by github_id (e.g. "anomalyco/opencode")."""
    for p in data()["projects"]:
        if p["github_id"].lower() == github_id.lower():
            return json.dumps(p, indent=2, ensure_ascii=False)
    return json.dumps({"error": f"unknown github_id: {github_id}",
                       "hint": "use search_harnesses to find the right id"})


@mcp.tool()
def list_categories() -> str:
    """The list's 9 categories and 13 curated use-case intents, with project counts."""
    d = data()
    counts: dict = {}
    for p in d["projects"]:
        counts[p["category"]] = counts.get(p["category"], 0) + 1
    return json.dumps({
        "categories": [dict(c, project_count=counts.get(c["id"], 0)) for c in d["categories"]],
        "use_cases": [u["intent"] for u in d["use_cases"]],
        "tiers": d["meta"]["tiers"],
    }, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run()
