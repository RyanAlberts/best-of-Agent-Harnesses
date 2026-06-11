#!/usr/bin/env python3
"""Refresh META star counts in generate.py from the GitHub API.

Rewrites each star count in place, bumps STARS_CAPTURED (and the META comment
date) to today in America/Chicago, and prints a movers summary. Run
scripts/generate.py afterwards to regenerate every derived output.

Auth: GH_TOKEN or GITHUB_TOKEN env var, required — 101 unauthenticated
requests exceeds GitHub's 60/hr anonymous rate limit.
"""

import json
import os
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

GEN = Path(__file__).resolve().parent / "generate.py"

token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
if not token:
    sys.exit("BLOCKED: set GH_TOKEN or GITHUB_TOKEN — anonymous rate limit is too low for ~101 repos.")

src = GEN.read_text()
ids = re.findall(r'^\s*"([^"\s]+/[^"\s]+)":\s*\(\d+,', src, re.M)
if not ids or len(ids) != len(set(ids)):
    sys.exit(f"BLOCKED: META parse failed ({len(ids)} ids, {len(set(ids))} unique) — format changed?")


def fetch(gid: str) -> tuple:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{gid}",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "best-of-agent-harnesses-refresh",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.loads(r.read().decode())
    return d["stargazers_count"], d["full_name"], d.get("archived", False)


changed, failed, moved, archived = [], [], [], []
for gid in ids:
    try:
        n, full, is_archived = fetch(gid)
    except Exception as e:  # 404, network — keep the old count, report loudly
        failed.append((gid, str(e)))
        continue
    if full.lower() != gid.lower():
        moved.append((gid, full))
    if is_archived:
        archived.append(gid)
    old = int(re.search(r'"%s":\s*\((\d+),' % re.escape(gid), src).group(1))
    if old != n:
        src = re.sub(r'("%s":\s*\()\d+(,)' % re.escape(gid), r"\g<1>%d\g<2>" % n, src)
        changed.append((gid, old, n))

today = datetime.now(ZoneInfo("America/Chicago")).strftime("%Y-%m-%d")
src = re.sub(r'STARS_CAPTURED = "\d{4}-\d{2}-\d{2}"', f'STARS_CAPTURED = "{today}"', src)
src = re.sub(r"# Star counts captured \d{4}-\d{2}-\d{2}", f"# Star counts captured {today}", src)
GEN.write_text(src)

print(f"Refreshed {len(ids)} repos: {len(changed)} changed, {len(failed)} failed. Capture date -> {today}")
print("Top movers:")
for gid, old, n in sorted(changed, key=lambda t: -abs(t[2] - t[1]))[:15]:
    print(f"  {gid}: {old} -> {n} ({n - old:+d})")
if moved:
    print("MOVED — update github_id + META key in generate.py (see CLAUDE.md curation rules):")
    for a, b in moved:
        print(f"  {a} -> {b}")
if archived:
    print("ARCHIVED — flag in description or drop per CLAUDE.md curation bar:")
    for a in archived:
        print(f"  {a}")
if failed:
    print("FAILED (old counts kept):")
    for a, e in failed:
        print(f"  {a}: {e}")
    if len(failed) > 5:
        sys.exit("Too many failures — aborting so a partial rescore isn't committed.")
