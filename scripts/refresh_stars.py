#!/usr/bin/env python3
"""Refresh META star counts in generate.py from the GitHub API.

Rewrites each star count in place, bumps STARS_CAPTURED (and the META comment
date) to today in America/Chicago, and prints a movers summary. Run
scripts/generate.py afterwards to regenerate every derived output.

WHERE THIS RUNS: .github/workflows/weekly-rescore.yml, on GitHub-hosted infra
with unrestricted api.github.com access. Do NOT run it from a Claude Code
cloud session/routine — those are scoped to their own configured repositories
and can't read third-party star counts, so every fetch 403s. The script
detects that case and says so rather than silently keeping stale counts.

Auth: GH_TOKEN or GITHUB_TOKEN env var, required — 144 unauthenticated
requests exceeds GitHub's 60/hr anonymous rate limit.
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

import write_queue

GEN = Path(__file__).resolve().parent / "generate.py"

# Exact substring from the routine-scoping 403 body returned for a repo not
# in this routine's Repositories list: distinguishes that from ordinary
# 404s, rate limits, or network errors.
SCOPE_MARKER = "GitHub access to this repository is not enabled for this session"


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


def is_scope_error(e: Exception) -> bool:
    """True if `e` is the routine's own repo-scoping 403 (repo not yet added
    to this routine's Repositories list), not an ordinary 404/rate-limit/
    network failure. Distinguishing the two turns a same-looking 403 into an
    actionable "add this repo to the routine" signal instead of noise."""
    if not (isinstance(e, urllib.error.HTTPError) and e.code == 403):
        return False
    try:
        body = json.loads(e.read().decode())
    except Exception:
        return False
    return SCOPE_MARKER in body.get("message", "")


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

    changed, failed, moved, archived, scope_missing = [], [], [], [], []
    archived_stars = {}
    for gid in ids:
        try:
            n, full, is_archived = fetch(gid, token)
        except Exception as e:  # 404, network — keep the old count, report loudly
            if is_scope_error(e):
                scope_missing.append(gid)
            else:
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

    if scope_missing:
        print()
        print("=" * 70)
        print("WRONG PLACE: this script is being run from a repo-scoped session")
        print("=" * 70)
        print(
            f"{len(scope_missing)} of {len(ids)} repos returned a session-scoping 403.\n"
            "\n"
            "That means this is running inside a Claude Code cloud session (routine),\n"
            "whose GitHub access is limited to its own configured repositories. It\n"
            "cannot read star counts for the third-party repos in META, and no amount\n"
            "of routine configuration reliably fixes that.\n"
            "\n"
            "The rescore is ALREADY automated somewhere that works:\n"
            "  .github/workflows/weekly-rescore.yml — Sundays 09:00 America/Chicago,\n"
            "  on GitHub-hosted infra with unrestricted api.github.com access.\n"
            "\n"
            "Don't run this from a routine. To trigger a rescore manually, use the\n"
            "workflow's workflow_dispatch (Actions tab -> weekly-rescore -> Run\n"
            "workflow) instead. A Claude routine should only READ the results:\n"
            "curation-queue.json, git log, and this repo's own issues/PRs.\n"
        )

    if failed:
        print("FAILED (old counts kept, unrelated to routine scope):")
        for a, e in failed:
            print(f"  {a}: {e}")

    if len(failed) + len(scope_missing) > 5:
        sys.exit("Too many failures — aborting WITHOUT writing, so a stale rescore "
                 "can't be stamped with today's date.")

    src = re.sub(r'STARS_CAPTURED = "\d{4}-\d{2}-\d{2}"', f'STARS_CAPTURED = "{today}"', src)
    src = re.sub(r"# Star counts captured \d{4}-\d{2}-\d{2}", f"# Star counts captured {today}", src)

    new_archived = rewrite_archived(archived, today, src)
    src = apply_archived_rewrite(src, new_archived)

    GEN.write_text(src)

    print(f"Refreshed {len(ids)} repos: {len(changed)} changed, {len(failed)} failed, "
          f"{len(scope_missing)} missing from routine scope. Capture date -> {today}")
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
        "failed": (
            [{"id": gid, "status": err} for gid, err in failed]
            + [{"id": gid, "status": "routine-scope: not in this routine's Repositories list"}
               for gid in scope_missing]
        ),
        "candidates": [],
    })


if __name__ == "__main__":
    main()
