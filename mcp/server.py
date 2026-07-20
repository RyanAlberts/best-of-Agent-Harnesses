#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp>=1.2"]
# ///
"""MCP server for best-of-Agent-Harnesses.

Serves the curated list (harnesses.json) as tools so agents can recommend
agent harnesses: recommend, compare, compare_for, pick_harness,
search_harnesses, get_harness, list_categories.

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
        "page_url": p.get("page_url", ""),
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


def _ranked(d: dict, use_case: str, max_rank: int = 4, min_a: int = 0,
            min_r: int = 0, open_source_only: bool = False,
            language: str = "") -> list:
    """Score the live projects against a use case. Returns [(score, project,
    reason)] sorted best-first. The best word-overlap curated use-case intent
    seeds its hand-picked projects to the top, in curated order — everything
    else is scored by token overlap plus a log-stars tiebreak. Shared by
    pick_harness and recommend so both rank identically."""
    import math
    q = _tokens(use_case)
    seeded: dict = {}
    best = max(d["use_cases"], key=lambda u: len(_overlap(q, _tokens(u["intent"]))), default=None)
    if best and len(_overlap(q, _tokens(best["intent"]))) >= 2:
        for rank, gid in enumerate(best["picks"]):
            seeded[gid] = (100 - rank, f"curated pick for \"{best['intent']}\"")
    lang = language.strip().lower()
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
        if lang and lang not in [t.lower() for t in p["tags"]]:
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
    return scored


@mcp.tool()
def pick_harness(use_case: str, max_complexity: str = "complex",
                 min_autonomy: str = "", min_recovery: str = "",
                 open_source_only: bool = False, limit: int = 5) -> str:
    """Recommend agent harnesses for a use case, ranked from a hand-curated list of 100+.

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
    scored = _ranked(d, use_case, max_rank, min_a, min_r, open_source_only)
    picks = [_brief(p, reason) for _, p, reason in scored[:limit]]
    return json.dumps({
        "use_case": use_case,
        "picks": picks,
        "source": d["meta"]["url"],
        "stars_captured": d["meta"]["stars_captured"],
    }, indent=2, ensure_ascii=False)


@mcp.tool()
def recommend(need: str, language: str = "", must_run_unattended: bool = False,
              open_source_only: bool = False) -> str:
    """Opinionated single recommendation for a need — a decision, not a list.

    Where pick_harness returns a ranked shortlist, recommend commits: one top
    pick with the reason, up to two alternatives, any listed harnesses to AVOID
    for this need (archived, or flagged for star manipulation — with why), and
    the most relevant decision guide to read next. Use this when an agent or user
    asks "what should I actually use for X?".

    need: plain-language description of what you're building, e.g. "an always-on
    personal assistant in my chat apps" or "evaluate a coding agent on benchmarks".
    language: optional — restrict to a language/runtime tag (python, javascript,
    typescript, rust).
    must_run_unattended: require a harness designed to run a whole task with no
    human in the loop (autonomy bounded or headless).
    open_source_only: drop restricted or unknown-license projects.
    Returns JSON: {recommendation, alternatives, avoid, see_also, source}.
    """
    d = data()
    a_tiers: list = d["meta"].get("autonomy_tiers", [])
    min_a = (a_tiers.index("bounded") + 1) if (must_run_unattended and "bounded" in a_tiers) else 0
    scored = _ranked(d, need, max_rank=4, min_a=min_a, open_source_only=open_source_only,
                     language=language)

    if not scored:
        return json.dumps({
            "need": need,
            "recommendation": None,
            "message": "No confident match. Try search_harnesses, or relax the "
                       "language / must_run_unattended constraints.",
            "source": d["meta"]["url"],
        }, indent=2, ensure_ascii=False)

    top = _brief(scored[0][1], scored[0][2])
    alternatives = [_brief(p, reason) for _, p, reason in scored[1:3]]

    # What to avoid: graveyard entries (archived or integrity-flagged) whose name
    # matches the need — surfaces curation intelligence a raw star sort would miss.
    # Hyphens/slashes are split so a compound name like "everything-claude-code"
    # matches "claude"/"code"; candidates are ranked by star count so the most
    # temptingly-popular flagged repo (the one you'd be fooled into picking) leads.
    q = _tokens(need)
    avoid_cands = []
    for g in d.get("graveyard", []):
        hay = _tokens(f"{g.get('name', '')} {g.get('github_id', '')}".replace("-", " ").replace("/", " "))
        if _overlap(q, hay):
            avoid_cands.append(g)
    avoid_cands.sort(key=lambda g: g.get("last_stars", 0), reverse=True)
    avoid = [{
        "name": g.get("name"),
        "github_id": g.get("github_id"),
        "stars": g.get("last_stars"),
        "reason": g.get("reason", "in the graveyard — not recommended"),
    } for g in avoid_cands[:2]]

    # See also: the decision guide whose title/summary best overlaps the need.
    see_also = None
    guides = d.get("comparisons", [])
    if guides:
        g = max(guides, key=lambda c: len(_overlap(q, _tokens(f"{c['title']} {c.get('summary', '')}"))))
        if _overlap(q, _tokens(f"{g['title']} {g.get('summary', '')}")):
            see_also = {"slug": g["slug"], "title": g["title"],
                        "how": "fetch full text with get_comparison(slug)"}

    return json.dumps({
        "need": need,
        "recommendation": top,
        "alternatives": alternatives,
        "avoid": avoid,
        "see_also": see_also,
        "source": d["meta"]["url"],
        "stars_captured": d["meta"]["stars_captured"],
    }, indent=2, ensure_ascii=False)


@mcp.tool()
def search_harnesses(query: str, limit: int = 10) -> str:
    """Keyword search across all 100+ projects (name, description, tags, category).

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
def compare(github_ids: list[str]) -> str:
    """Side-by-side comparison of 2-4 harnesses by github_id — for "should I use X or Y?".

    Answers the head-to-head question with the list's curation intelligence
    instead of a raw spec dump: each project's record aligned on the list's
    axes, an edge summary naming which project leads on stars / adoption
    simplicity / autonomy / failure recovery, a warning when a requested id is
    in the graveyard (archived or integrity-flagged), and the decision guide
    covering this matchup when one exists.

    github_ids: 2-4 ids, e.g. ["openclaw/openclaw", "NousResearch/hermes-agent"]
    — use search_harnesses to find an id.
    Returns JSON: {projects, edges, warnings, see_also, source, stars_captured}.
    Edge values are lists of names (more than one = a tie); an axis is omitted
    when fewer than two of the compared projects are rated on it.
    """
    d = data()
    ids = [g.strip() for g in github_ids if g and g.strip()]
    if not 2 <= len(ids) <= 4:
        return json.dumps({"error": "pass 2-4 github_ids"})
    by_id = {p["github_id"].lower(): p for p in d["projects"]}
    grave = {g.get("github_id", "").lower(): g for g in d.get("graveyard", [])}
    projects, warnings, unknown = [], [], []
    for gid in ids:
        if (p := by_id.get(gid.lower())):
            projects.append(p)
        elif (g := grave.get(gid.lower())):
            warnings.append({
                "github_id": g["github_id"],
                "warning": "in the graveyard, not comparable: "
                           + g.get("reason", "not recommended"),
                "last_stars": g.get("last_stars"),
            })
        else:
            unknown.append(gid)
    if unknown:
        return json.dumps({"error": f"unknown github_ids: {', '.join(unknown)}",
                           "hint": "use search_harnesses to find the right id"})

    return json.dumps(_compare_payload(d, projects, warnings),
                      indent=2, ensure_ascii=False)


def _dd_rank(p: dict, axis: str) -> int:
    return ((p.get("deep_dive") or {}).get(axis) or {}).get("rank", 0)


def _compare_payload(d: dict, projects: list, warnings: list) -> dict:
    """Shared by compare and compare_for: axis edges, guide pointer, records."""
    edges = {}
    for label, key, best in [
        ("most_stars", lambda p: p.get("stars", 0), max),
        ("simplest_adoption", lambda p: p.get("tier_rank", 0), min),
        ("highest_autonomy", lambda p: p.get("autonomy_rank", 0), max),
        ("strongest_recovery", lambda p: p.get("recovery_rank", 0), max),
        ("strongest_sandboxing", lambda p: _dd_rank(p, "tooling_sandboxing"), max),
        ("strongest_memory", lambda p: _dd_rank(p, "context_memory"), max),
        ("fullest_lifecycle_hooks", lambda p: _dd_rank(p, "lifecycle_hooks"), max),
        ("most_prompt_optimization", lambda p: _dd_rank(p, "prompt_optimization"), max),
    ]:
        rated = [p for p in projects if key(p)]
        if len(rated) >= 2:
            top = best(key(p) for p in rated)
            edges[label] = [p["name"] for p in rated if key(p) == top]

    # See also: the guide that mentions at least two of the compared projects.
    see_also = None
    name_tokens = [_tokens(p["name"]) for p in projects]
    best_guide, best_hits = None, 1
    for c in d.get("comparisons", []):
        hay = _tokens(f"{c['title']} {c.get('summary', '')}")
        hits = sum(1 for t in name_tokens if _overlap(t, hay))
        if hits > best_hits:
            best_guide, best_hits = c, hits
    if best_guide:
        see_also = {"slug": best_guide["slug"], "title": best_guide["title"],
                    "how": "fetch full text with get_comparison(slug)"}

    return {
        "projects": [dict(_brief(p), deep_dive=p.get("deep_dive")) for p in projects],
        "edges": edges,
        "warnings": warnings,
        "see_also": see_also,
        "source": d["meta"]["url"],
        "stars_captured": d["meta"]["stars_captured"],
    }


@mcp.tool()
def compare_for(use_case: str, limit: int = 3, open_source_only: bool = False) -> str:
    """Pick the top harnesses for a use case or task and compare them side by side.

    One call for "compare the best options for X": candidates are ranked the
    same way pick_harness ranks them, the top 2-4 are compared head-to-head
    (per-axis edge lists incl. the researched deep-dive axes — sandboxing,
    context memory, lifecycle hooks, prompt optimization — plus each project's
    build-vs-buy tier), with each pick's ranking reason and the decision guide
    covering the matchup when one exists.

    use_case: the task, e.g. "sandboxed code execution for generated code".
    limit: how many top candidates to compare (2-4, default 3).
    Returns JSON: {use_case, projects, why_picked, edges, warnings, see_also, source}.
    """
    d = data()
    n = max(2, min(int(limit), 4))
    scored = _ranked(d, use_case, open_source_only=open_source_only)
    if len(scored) < 2:
        return json.dumps({
            "use_case": use_case,
            "message": "Fewer than two confident matches — try search_harnesses "
                       "or a more concrete task description.",
            "source": d["meta"]["url"],
        }, indent=2, ensure_ascii=False)
    top = scored[:n]
    payload = _compare_payload(d, [p for _, p, _ in top], [])
    payload = dict({"use_case": use_case}, **payload)
    payload["why_picked"] = {p["name"]: reason for _, p, reason in top}
    return json.dumps(payload, indent=2, ensure_ascii=False)


@mcp.tool()
def list_comparisons() -> str:
    """The list's head-to-head decision guides (e.g. "OpenClaw vs Hermes",
    "How to pick a harness") — slug, title, and summary for each. Fetch the
    full text of one with get_comparison(slug)."""
    return json.dumps({"comparisons": data().get("comparisons", [])},
                      indent=2, ensure_ascii=False)


@mcp.tool()
def get_comparison(slug: str) -> str:
    """Full markdown of one decision guide by slug (see list_comparisons).
    Guides cover architecture trade-offs, field reports, and the post-June-2026
    billing reality — use them when a user is choosing between specific
    harnesses, not just browsing."""
    for c in data().get("comparisons", []):
        if c["slug"] == slug:
            local = Path(__file__).resolve().parent.parent / "comparisons" / f"{slug}.md"
            if local.exists():
                return local.read_text()
            with urllib.request.urlopen(c["raw_url"], timeout=15) as r:
                return r.read().decode()
    return json.dumps({"error": f"unknown slug: {slug}",
                       "available": [c["slug"] for c in data().get("comparisons", [])]})


@mcp.tool()
def list_categories() -> str:
    """The list's 10 categories and 14 curated use-case intents, with project counts."""
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
        "deep_dive_vocab": d["meta"].get("deep_dive_vocab", {}),
        "deep_dive_help": d["meta"].get("deep_dive_help", ""),
    }, indent=2, ensure_ascii=False)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
