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

import write_queue

GEN = Path(__file__).resolve().parent / "generate.py"


def today_chicago() -> str:
    """Today's date in America/Chicago. Override with TODAY=YYYY-MM-DD for
    sandboxes missing tzdata or running Python <3.9."""
    override = os.environ.get("TODAY", "")
    if override:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", override):
            sys.exit(f"BLOCKED: TODAY={override!r} is not YYYY-MM-DD.")
        return override
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("America/Chicago")).strftime("%Y-%m-%d")
    except Exception as e:
        sys.exit(
            f"BLOCKED: can't resolve America/Chicago ({e!r} — Python <3.9 or no tzdata).\n"
            "Re-run as: TODAY=YYYY-MM-DD python3 scripts/refresh_stars.py\n"
            "(use today's date in America/Chicago, not UTC)."
        )


def fetch(gid: str, token: str) -> tuple:
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


def parse_archived_block(src: str) -> dict:
    """Locate the existing ARCHIVED block with a scoped regex (not a bare
    substring slice) and parse its "id": "date" pairs. Exits loudly if the
    block can't be found, rather than silently treating it as empty."""
    m = re.search(r'ARCHIVED:\s*"dict\[str, str\]"\s*=\s*\{(.*?)\}', src, re.DOTALL)
    if m is None:
        sys.exit("BLOCKED: ARCHIVED block not found in generate.py — refusing to write")
    return dict(re.findall(r'"([^"\s]+/[^"\s]+)":\s*"(\d{4}-\d{2}-\d{2})"', m.group(1)))


def rewrite_archived(archived_now: list, today: str, src: str) -> dict:
    """Keep existing `since` dates for still-archived repos, add today's
    date for newly-archived repos, drop entries no longer archived."""
    existing_archived = parse_archived_block(src)
    return {gid: existing_archived.get(gid, today) for gid in archived_now}


def apply_archived_rewrite(src: str, new_archived: dict) -> str:
    """Rewrite the ARCHIVED block in `src` with `new_archived`, using
    re.subn and validating exactly one match — refuses to write otherwise."""
    archived_lines = "\n".join(f'    "{gid}": "{since}",' for gid, since in new_archived.items())
    new_block = (
        "ARCHIVED: \"dict[str, str]\" = {\n" + archived_lines + ("\n" if archived_lines else "") + "}"
    )
    new_src, n = re.subn(
        r'ARCHIVED:\s*"dict\[str, str\]"\s*=\s*\{.*?\}',
        new_block,
        src,
        flags=re.DOTALL,
    )
    if n != 1:
        sys.exit(f"BLOCKED: ARCHIVED block rewrite matched {n} times — refusing to write")
    return new_src


def main() -> None:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("BLOCKED: set GH_TOKEN or GITHUB_TOKEN — anonymous rate limit is too low for ~101 repos.")

    today = today_chicago()  # resolve early: fail before any API calls, not after

    src = GEN.read_text()
    ids = re.findall(r'^\s*"([^"\s]+/[^"\s]+)":\s*\(\d+,', src, re.M)
    if not ids or len(ids) != len(set(ids)):
        sys.exit(f"BLOCKED: META parse failed ({len(ids)} ids, {len(set(ids))} unique) — format changed?")

    changed, failed, moved, archived = [], [], [], []
    archived_stars = {}
    for gid in ids:
        try:
            n, full, is_archived = fetch(gid, token)
        except Exception as e:  # 404, network — keep the old count, report loudly
            failed.append((gid, str(e)))
            continue
        if full.lower() != gid.lower():
            moved.append((gid, full))
        if is_archived:
            archived.append(gid)
            archived_stars[gid] = n
        old = int(re.search(r'"%s":\s*\((\d+),' % re.escape(gid), src).group(1))
        if old != n:
            src = re.sub(r'("%s":\s*\()\d+(,)' % re.escape(gid), r"\g<1>%d\g<2>" % n, src)
            changed.append((gid, old, n))

    if failed:
        print("FAILED (old counts kept):")
        for a, e in failed:
            print(f"  {a}: {e}")
        if len(failed) > 5:
            sys.exit("Too many failures — aborting WITHOUT writing, so a stale rescore "
                     "can't be stamped with today's date.")

    src = re.sub(r'STARS_CAPTURED = "\d{4}-\d{2}-\d{2}"', f'STARS_CAPTURED = "{today}"', src)
    src = re.sub(r"# Star counts captured \d{4}-\d{2}-\d{2}", f"# Star counts captured {today}", src)

    new_archived = rewrite_archived(archived, today, src)
    src = apply_archived_rewrite(src, new_archived)

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

    # Hand off to Flow 2 (a separate Claude routine that reads this file and
    # never calls the GitHub API) — see .superpowers/sdd for the two-flow design.
    write_queue.write({
        "generated": today,
        "movers": [{"id": gid, "from": old, "to": n} for gid, old, n in changed],
        "moved": [{"id": a, "to": b} for a, b in moved],
        "archived": [{"id": gid, "since": new_archived[gid], "stars": archived_stars[gid]} for gid in archived],
        "failed": [{"id": gid, "status": err} for gid, err in failed],
        "candidates": [],
    })


if __name__ == "__main__":
    main()
