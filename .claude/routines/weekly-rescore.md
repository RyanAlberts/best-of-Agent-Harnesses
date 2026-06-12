# Weekly rescore routine — paste this as the routine prompt in claude.ai → Routines

<!-- Versioned here so the routine prompt evolves with the repo. When the
     generation pipeline changes, update this file in the same PR, then paste
     the new prompt into the routine. -->

## First-run smoke test (run once before enabling the full prompt below)

The routines sandbox differs from interactive CC sessions. Paste THIS as the
routine prompt first, hit "Run now", read the log, then replace it with the
full prompt. It proves the environment without committing or pushing anything.

    SMOKE TEST for the weekly rescore of RyanAlberts/best-of-Agent-Harnesses.
    Do NOT commit, push, or open a PR. Goal: prove this sandbox can run the
    rescore, then report.

    1. Pre-flight: if GH_TOKEN is unset, print BLOCKED and stop.
    2. cd /home/user/best-of-Agent-Harnesses
       git remote set-url origin https://x-access-token:${GH_TOKEN}@github.com/RyanAlberts/best-of-Agent-Harnesses.git
       git checkout main && git fetch origin && git reset --hard origin/main
    3. Environment probes — report each result verbatim:
       python3 --version
       python3 -c "from zoneinfo import ZoneInfo; print(ZoneInfo('America/Chicago'))"
       which git jq curl
       (If the zoneinfo probe fails, the rescore still works — prefix step 4
       with TODAY=YYYY-MM-DD, today's date in America/Chicago, and say so.)
    4. python3 scripts/refresh_stars.py
    5. python3 scripts/generate.py
    6. python3 -c "import json; d=json.load(open('harnesses.json')); assert d['meta']['project_count']==len(d['projects']); print('sanity ok:', d['meta']['stars_captured'])"
    7. git status --porcelain && git diff --stat — confirm only these change:
       scripts/generate.py, README.md, TAGS.md, projects.yaml, config/header.md,
       harnesses.json, llms.txt, assets/landscape.svg, comparisons/*.md.
    8. REPORT: probe results, the refresh_stars summary (counts changed /
       MOVED / ARCHIVED / FAILED), the diff stat, and a one-line verdict:
       "SMOKE TEST PASSED — enable the full weekly-rescore prompt" or exactly
       what failed.
    9. Discard everything so the real run starts clean:
       git reset --hard origin/main

## Full prompt

Weekly rescore for RyanAlberts/best-of-Agent-Harnesses. Use today's date in
America/Chicago — call it TODAY, format YYYY-MM-DD.

PRE-FLIGHT — verify routines env is in use, fail loud otherwise:
1. Check GH_TOKEN is present:
     if [ -z "$GH_TOKEN" ]; then
       echo "BLOCKED: GH_TOKEN not set. This routine must run under the"
       echo "'routines' environment, not Default. Edit the routine via"
       echo "/schedule on your laptop or claude.ai → Routines and switch"
       echo "its environment to 'routines'."
       exit 1
     fi
2. Wire GH_TOKEN into git and sync the env clone to current main (the clone
   is stale between runs; any local commits on it are disposable):
     cd /home/user/best-of-Agent-Harnesses
     git remote set-url origin \
       https://x-access-token:${GH_TOKEN}@github.com/RyanAlberts/best-of-Agent-Harnesses.git
     git checkout main && git fetch origin && git reset --hard origin/main

RESCORE — two scripts do ALL regeneration. Never hand-edit dates, star
counts, or any generated file. If you find yourself editing README.md,
TAGS.md, projects.yaml, config/header.md, harnesses.json, llms.txt,
assets/landscape.svg, or a "⭐ Stars" row in comparisons/*.md — stop: those
are owned by the scripts.
3. python3 scripts/refresh_stars.py
   - Fetches live star counts for all ~101 repos (uses GH_TOKEN), rewrites
     META inside scripts/generate.py, bumps STARS_CAPTURED to TODAY.
   - If it BLOCKS on timezone resolution (no tzdata / old Python), re-run as:
     TODAY=YYYY-MM-DD python3 scripts/refresh_stars.py
   - Prints: top movers, MOVED repos, ARCHIVED repos, FAILED fetches.
     Save this output for the PR body.
   - It exits non-zero on too many failures: stop and report; never commit
     a partial rescore.
4. If it printed MOVED entries: update each one's github_id and its META key
   in scripts/generate.py to the new canonical location (CLAUDE.md curation
   rule). Mechanical redirect-following only — do NOT change display names
   or descriptions, and do NOT drop archived projects; flag rebrands and
   ARCHIVED entries in the PR body for editorial review instead.
5. python3 scripts/generate.py
   - Regenerates everything derived or dated: README.md, projects.yaml,
     config/header.md, TAGS.md, harnesses.json, llms.txt,
     assets/landscape.svg (the landscape graphic embeds the capture date —
     this step is what keeps it current), and patches the "⭐ Stars" rows
     inside comparisons/*.md.

SANITY — fail loud on any mismatch:
6. python3 -c "import json; d=json.load(open('harnesses.json')); \
     assert d['meta']['stars_captured']=='TODAY', d['meta']['stars_captured']; \
     assert d['meta']['project_count']==len(d['projects']); print('sanity ok')"
   (substitute the real TODAY value)
7. git status --porcelain — every changed file must be one of:
   scripts/generate.py, README.md, TAGS.md, projects.yaml, config/header.md,
   harnesses.json, llms.txt, assets/landscape.svg, comparisons/*.md.
   Anything else changed: stop and report.
8. Rank movers: from git diff README.md, list projects that moved more than
   2 positions within a category (or "none").

COMMIT (TZ, signing off, identity overrides):
9.  git checkout -b weekly-rescore-TODAY
10. TZ='America/Chicago' git -c commit.gpgsign=false \
        -c user.email='25306145+RyanAlberts@users.noreply.github.com' \
        -c user.name='Ryan Alexander Alberts' \
        commit -a --author='Ryan Alexander Alberts <25306145+RyanAlberts@users.noreply.github.com>' \
        -m "weekly rescore TODAY"
    (The noreply address is REQUIRED — never put a personal email in a commit.)

PUSH (PAT-auth via the rewritten origin URL):
11. git push -u origin weekly-rescore-TODAY

PR + MERGE (PAT-auth via curl):
12. Create the PR as before (POST /repos/RyanAlberts/best-of-Agent-Harnesses/pulls,
    head weekly-rescore-TODAY, base main, title "Weekly rescore TODAY").
    The PR body must include, in this order:
    - Capture date TODAY and how many star counts changed
    - Top 10 star movers (from step 3 output)
    - Rank movers >2 positions (step 8), or "none"
    - MOVED repos applied (step 4) and any ARCHIVED/rebrand flags needing
      editorial review
    - FAILED fetches, if any
    - COMPARISONS FRESHNESS: for each comparisons/*.md, the date of the last
      commit touching it (git log -1 --format=%cs -- <file>). Flag any page
      older than 60 days as "needs an editorial review pass" — the star rows
      auto-patch but the prose claims do not.
    - WEEKLY PULSE: issues and PRs on RyanAlberts/best-of-Agent-Harnesses
      updated in the last 7 days — title + URL each, via
      curl -fsS -H "Authorization: token $GH_TOKEN" \
        "https://api.github.com/repos/RyanAlberts/best-of-Agent-Harnesses/issues?state=all&since=<ISO date 7 days ago>"
      Maintainer corrections arrive as replies to the badge-outreach issues
      on other repos and as issues here; surface them, do not act on them.
13. Merge it: PUT .../pulls/$PR/merge with {"merge_method":"merge"}.

VERIFY credit:
14. curl -fsS -H "Authorization: token $GH_TOKEN" \
        https://api.github.com/repos/RyanAlberts/best-of-Agent-Harnesses/commits/main \
        | jq '{sha:.sha, login:.author.login, email:.commit.author.email}'
    Assert login=="RyanAlberts" and email ends with "@users.noreply.github.com".
    A personal email in the author field is a policy violation — report it.

Exit criteria: rescore commit on main with TODAY's actual star counts (not
just a date bump — refresh_stars.py must report changed counts), credited to
@RyanAlberts; harnesses.json, llms.txt, and assets/landscape.svg all stamped
TODAY; comparison "⭐ Stars" rows in sync; PR body contains movers, curation
flags, and the weekly pulse.
