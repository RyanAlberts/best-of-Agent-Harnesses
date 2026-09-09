#!/usr/bin/env python3
"""Discover candidate agent-harness repos via GitHub search.

Runs as part of Flow 1 (weekly Action, full GitHub API access). Feeds new
candidates into curation-queue.json's `candidates` array for Flow 2's
judgment routine to vet. See docs/superpowers/specs/2026-07-03-improve-flow-design.md.

Auth: GH_TOKEN or GITHUB_TOKEN env var, same as refresh_stars.py.
"""

import json
import os
import re
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


ISSUE_REPO_URL = re.compile(r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)")


def _api(path: str, token: str) -> object:
    """Single GitHub REST call, `path` relative to https://api.github.com.
    The HTTP boundary for issue_submissions() — monkeypatched in tests."""
    req = urllib.request.Request(
        "https://api.github.com" + path,
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "best-of-agent-harnesses-discover",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def issue_submissions(token: str, repo: str, known_ids: set[str]) -> list[dict]:
    """Open "Add project" issues on `repo`, resolved to candidate entries.

    Same shape as find() plus "via": "issue #N", so the biweekly improve
    routine vets community submissions from the queue with real repo data
    instead of leaving the issues unanswered. No star floor on purpose: a
    submission below the bar earns a radar pin or a reply, never silence.
    """
    known_lower = {k.lower() for k in known_ids}
    out: list[dict] = []
    seen: set[str] = set()
    try:
        issues = _api(f"/repos/{repo}/issues?state=open&per_page=100", token)
    except Exception as e:  # rate limit/network — the search queries still run
        print(f"issue listing failed, skipping submissions: {e}", file=sys.stderr)
        return out
    for issue in issues:
        if issue.get("pull_request"):
            continue
        labels = {lab.get("name") for lab in issue.get("labels", [])}
        title = issue.get("title") or ""
        if "add-project" not in labels and not title.startswith("Add project:"):
            continue
        m = ISSUE_REPO_URL.search(issue.get("body") or "")
        if not m:
            continue
        gid = m.group(1).removesuffix(".git")
        if gid.lower() in known_lower or gid.lower() in seen:
            continue
        try:
            r = _api(f"/repos/{gid}", token)
        except Exception as e:
            print(f"submission #{issue.get('number')}: {gid} unreachable ({e})", file=sys.stderr)
            continue
        if r.get("archived"):
            continue
        seen.add(gid.lower())
        out.append({
            "id": r.get("full_name") or gid,
            "stars": r.get("stargazers_count", 0),
            "topics": r.get("topics", []),
            "desc": r.get("description") or "",
            "via": f"issue #{issue.get('number')}",
        })
    return out


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
    import pathlib
    import generate
    import write_queue

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("BLOCKED: set GH_TOKEN or GITHUB_TOKEN.")
    known = {p.github_id for plist in generate.PROJECTS.values() for p in plist} | set(generate.ARCHIVED)
    repo = os.environ.get("GITHUB_REPOSITORY", "RyanAlberts/best-of-Agent-Harnesses")
    submitted = issue_submissions(token, repo, known)
    submitted_ids = {c["id"].lower() for c in submitted}
    candidates = submitted + [c for c in find(token, known) if c["id"].lower() not in submitted_ids]
    queue_path = pathlib.Path(__file__).resolve().parent.parent / "curation-queue.json"
    data = json.loads(queue_path.read_text()) if queue_path.exists() else {}
    data["candidates"] = candidates
    write_queue.write(data, queue_path)
    print(f"discovered {len(candidates)} candidate(s), {len(submitted)} from open issues")


if __name__ == "__main__":
    main()
