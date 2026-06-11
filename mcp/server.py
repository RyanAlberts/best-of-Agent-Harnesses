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


def _overlap(q: set, hay: set) -> set:
    """Query tokens with a match in hay, tolerating inflections: tokens of 4+
    chars match if either is a prefix of the other (benchmark/benchmarks,
    evaluate/evaluates)."""
    hits = set()
    for w in q:
        for h in hay:
            if w == h or (len(w) >= 4 and len(h) >= 4 and (w.startswith(h) or h.startswith(w))):
                hits.add(w)
                break
    return hits


def _brief(p: dict, reason: str = "") -> dict:
    out = {
        "name": p["name"],
        "github_id": p["github_id"],
        "url": p["url"],
        "stars": p["stars"],
        "tier": p["tier"],
        "autonomy": p.get("autonomy", "n/a"),
        "recovery": p.get("recovery", "n/a"),
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
                 min_autonomy: str = "", min_recovery: str = "",
                 open_source_only: bool = False, limit: int = 5) -> str:
    """Recommend agent harnesses for a use case, ranked from a hand-curated list of 101.

    use_case: what you want to do, e.g. "terminal coding agent", "drop-in memory
    layer", "evaluate agents on coding benchmarks".
    max_complexity: cap on adoption surface — one of "super simple",
    "mostly simple", "slightly complex", "complex" (default: no cap).
    min_autonomy: require at least this designed autonomy regime — one of
    "step-gated", "checkpoint-gated", "bounded", "headless" (e.g. "bounded"
    means "must be able to run a whole task unattended"; excludes n/a entries).
    min_recovery: require at least this failure-recovery tier — one of "none",
    "retry", "resumable", "durable" (excludes n/a entries).
    open_source_only: drop projects with restricted or unknown licenses.
    Returns JSON: ranked picks with a one-line reason each.
    """
    d = data()
    tiers: list = d["meta"]["tiers"]
    max_rank = tiers.index(max_complexity) + 1 if max_complexity in tiers else 4
    a_tiers: list = d["meta"].get("autonomy_tiers", [])
    r_tiers: list = d["meta"].get("recovery_tiers", [])
    min_a = a_tiers.index(min_autonomy) + 1 if min_autonomy in a_tiers else 0
    min_r = r_tiers.index(min_recovery) + 1 if min_recovery in r_tiers else 0
    q = _tokens(use_case)

    # Curated use-case intents are the strongest signal: best word-overlap intent
    # seeds its hand-picked projects to the top, in curated order.
    seeded: dict = {}
    best = max(d["use_cases"], key=lambda u: len(_overlap(q, _tokens(u["intent"]))), default=None)
    if best and len(_overlap(q, _tokens(best["intent"]))) >= 2:
        for rank, gid in enumerate(best["picks"]):
            seeded[gid] = (100 - rank, f"curated pick for \"{best['intent']}\"")

    import math
    scored = []
    for p in d["projects"]:
        if p["tier_rank"] > max_rank:
            continue
        if min_a and p.get("autonomy_rank", 0) < min_a:
            continue
        if min_r and p.get("recovery_rank", 0) < min_r:
            continue
        if open_source_only and p["license_signal"] != "open-source":
            continue
        if p["github_id"] in seeded:
            score, reason = seeded[p["github_id"]]
        else:
            overlap = _overlap(q, _tokens(f"{p['description']} {' '.join(p['tags'])} {p['category_title']}"))
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
        overlap = _overlap(q, _tokens(hay))
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
        "autonomy_tiers": d["meta"].get("autonomy_tiers", []),
        "recovery_tiers": d["meta"].get("recovery_tiers", []),
    }, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run()
