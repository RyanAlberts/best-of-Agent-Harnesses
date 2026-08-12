"""Append a weekly traffic snapshot to traffic-history.jsonl.

GitHub's traffic API only retains 14 days, so trend analysis beyond two weeks
is impossible unless someone records it. This script captures views, clones,
top paths, top referrers, star count, and MCP PyPI downloads into one JSON
line per run. Run weekly by .github/workflows/weekly-rescore.yml; needs a
token with push access (the traffic API requires it) in GH_TOKEN.
"""
import datetime
import json
import os
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REPO = "RyanAlberts/best-of-Agent-Harnesses"


def fetch(url: str):
    headers = {"Accept": "application/vnd.github+json",
               "User-Agent": "best-of-agent-harnesses-snapshot"}
    if os.environ.get("GH_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GH_TOKEN']}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as r:
        return json.load(r)


def main() -> None:
    base = f"https://api.github.com/repos/{REPO}"
    snap = {
        "captured": datetime.date.today().isoformat(),
        "views": fetch(f"{base}/traffic/views"),
        "clones": fetch(f"{base}/traffic/clones"),
        "paths": fetch(f"{base}/traffic/popular/paths"),
        "referrers": fetch(f"{base}/traffic/popular/referrers"),
        "stars": fetch(base).get("stargazers_count"),
        "forks": fetch(base).get("forks_count"),
    }
    try:
        snap["mcp_pypi_recent"] = fetch(
            "https://pypistats.org/api/packages/agent-harnesses-mcp/recent")["data"]
    except Exception:
        snap["mcp_pypi_recent"] = None

    out = REPO_ROOT / "traffic-history.jsonl"
    with out.open("a") as f:
        f.write(json.dumps(snap, separators=(",", ":")) + "\n")
    print(f"traffic-history.jsonl: appended snapshot for {snap['captured']} "
          f"(views {snap['views']['count']}, stars {snap['stars']})")


if __name__ == "__main__":
    main()
