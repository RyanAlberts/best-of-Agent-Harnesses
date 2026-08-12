"""Refresh contributors.json from the GitHub issues/PRs API.

The thank-you roster in the README intro is generated from contributors.json,
so the "Meet the N" count can never go stale again. This script rewrites that
file from live data: every external (non-owner, non-bot) author of an issue or
pull request on the repo, with their contributions oldest-first.

Editorial control stays in scripts/generate.py: CONTRIB_NOTES overrides the
displayed label per login, CONTRIB_EXCLUDE hides promo-only authors.

Run weekly by .github/workflows/weekly-rescore.yml alongside refresh_stars.py;
uses GH_TOKEN when set (higher rate limit), anonymous otherwise.
"""
import json
import os
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REPO = "RyanAlberts/best-of-Agent-Harnesses"
OWNER = "RyanAlberts"


def fetch(url: str):
    headers = {"Accept": "application/vnd.github+json",
               "User-Agent": "best-of-agent-harnesses-refresh"}
    if os.environ.get("GH_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GH_TOKEN']}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as r:
        return json.load(r), r.headers.get("Link", "") or ""


def main() -> None:
    items, page = [], 1
    while True:
        data, link = fetch(
            f"https://api.github.com/repos/{REPO}/issues"
            f"?state=all&per_page=100&page={page}")
        items += data
        if 'rel="next"' not in link:
            break
        page += 1

    people: dict = {}
    for it in items:
        login = it["user"]["login"]
        if login == OWNER or login.endswith("[bot]"):
            continue
        p = people.setdefault(login, {"login": login, "contributions": []})
        p["contributions"].append({
            "kind": "pr" if "pull_request" in it else "issue",
            "number": it["number"],
            "title": it["title"],
        })

    for p in people.values():
        p["contributions"].sort(key=lambda c: c["number"])
    roster = sorted(people.values(), key=lambda p: p["contributions"][0]["number"])

    out = REPO_ROOT / "contributors.json"
    out.write_text(json.dumps(roster, indent=2, ensure_ascii=False) + "\n")
    print(f"contributors.json: {len(roster)} external contributors, "
          f"{sum(len(p['contributions']) for p in roster)} contributions")


if __name__ == "__main__":
    main()
