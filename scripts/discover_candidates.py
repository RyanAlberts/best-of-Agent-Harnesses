#!/usr/bin/env python3
"""Discover candidate agent-harness repos via GitHub search.

Runs as part of Flow 1 (weekly Action, full GitHub API access). Feeds new
candidates into curation-queue.json's `candidates` array for Flow 2's
judgment routine to vet. See docs/superpowers/specs/2026-07-03-improve-flow-design.md.

Auth: GH_TOKEN or GITHUB_TOKEN env var, same as refresh_stars.py.
"""

import json
import os
import sys
import urllib.parse
import urllib.request

# Heuristic queries: topics known to tag agent harnesses, plus keyword
# searches over name/description for projects that don't tag consistently.
QUERIES = [
    "topic:ai-agents",
    "topic:llm-agents",
    "topic:agent-framework",
    "topic:coding-agent",
    '"agent harness" in:name,description',
    '"coding agent" in:name,description',
]


def _search(query: str, token: str) -> dict:
    """Single GitHub code-search call. The HTTP boundary — monkeypatched in
    tests so `find()` never touches the network."""
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode(
        {"q": query, "sort": "stars", "order": "desc", "per_page": 30}
    )
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "best-of-agent-harnesses-discover",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def find(token: str, known_ids: set[str], min_stars: int = 300) -> list[dict]:
    """Search GitHub for plausible new agent-harness repos, filtered to
    those not already known, not archived, and above `min_stars`.

    Returns a list of dicts shaped {"id", "stars", "topics", "desc"} —
    matching curation-queue.json's `candidates` entry shape.
    """
    known_lower = {k.lower() for k in known_ids}
    seen: dict[str, dict] = {}

    for query in QUERIES:
        try:
            data = _search(query, token)
        except Exception as e:  # rate limit/network — skip this query, keep the rest
            print(f"search query failed, skipping: {query!r} ({e})", file=sys.stderr)
            continue
        for item in data.get("items", []):
            full_name = item.get("full_name")
            if not full_name:
                continue
            if full_name.lower() in known_lower:
                continue
            if item.get("archived", False):
                continue
            stars = item.get("stargazers_count", 0)
            if stars < min_stars:
                continue
            if full_name in seen:
                continue
            seen[full_name] = {
                "id": full_name,
                "stars": stars,
                "topics": item.get("topics", []),
                "desc": item.get("description") or "",
            }

    return list(seen.values())


def main() -> None:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("BLOCKED: set GH_TOKEN or GITHUB_TOKEN.")
    candidates = find(token, known_ids=set())
    print(json.dumps(candidates, indent=2))


if __name__ == "__main__":
    main()
