# Design: Two-flow curation system (weekly audit + biweekly improve)

Date: 2026-07-03
Status: Approved (design decisions confirmed by CEO 2026-07-03)
Repo: RyanAlberts/best-of-Agent-Harnesses

## Problem

The list must stay accurate and improve over time. Two failure classes matter:
1. **Decay** — star counts, moved/renamed repos, and newly-archived projects drift the list out of date. Missing these is bad.
2. **Stagnation** — new harnesses never get added; the README/editorial/navigation content goes stale or gets silently dropped by regeneration.

The prior mechanism (a single Claude Code cloud routine doing everything) broke permanently when Claude Code tightened routine sessions to a **per-repo GitHub API allowlist**: `refresh_stars.py` reads ~110 *third-party* repos, all of which now 403 (they can't be added to a per-repo allowlist because they aren't owned). See `memory/project_boah_rescore_routine_403.md`.

## Solution overview

Split the work by capability into two independent flows:

- **Flow 1 — Weekly Audit** (deterministic; GitHub Action). Already live. Has full GitHub API access on GitHub-hosted runners. Owns *all* third-party GitHub reads.
- **Flow 2 — Biweekly Improve** (judgment; Claude routine). Reasons over data Flow 1 produces. **Only ever reads/writes the bound repo `best-of-Agent-Harnesses`**, so it never touches the per-repo scoping wall.

The two communicate through a file committed to the repo (`curation-queue.json`), not through live API calls. This is the load-bearing design decision: it is what lets a Claude routine participate at all.

## Goals

- Weekly deterministic refresh keeps stars/ranking current and archived repos quarantined — automatic, zero-cost, no agent.
- Biweekly judgment pass proposes real improvements (new repos, rebrand resolution, hygiene, editorial freshness) as a reviewable PR + push notification.
- Nothing editorial is ever silently lost; archived history is retained, not deleted.
- The loop closes: agent proposes → CEO merges → next audit renders it.

## Non-goals

- Flow 2 does **not** call the GitHub API directly (avoids the 403 wall). All API work is Flow 1's.
- No auto-merge of judgment PRs. The CEO is the merge gate for anything non-mechanical.
- No metered LLM API spend — Flow 2 runs on the Claude Max subscription via the routine.

## Architecture

```
Flow 1 (GitHub Action, weekly, deterministic)
  refresh_stars.py  ──> live stars, MOVED, ARCHIVED, FAILED for ~110 repos
  discover_candidates.py (NEW) ──> GitHub search for plausible new harnesses
  generate.py ──> renders README/TAGS/json/svg; graveyard split; guardrail checks
  writes curation-queue.json (detection + candidates) ──> commits to main
        │
        ▼  (file in repo, no API)
Flow 2 (Claude routine, biweekly, judgment, HYBRID)
  reads curation-queue.json (only touches the bound repo)
  - auto-applies mechanical: MOVED github_id redirects
  - drafts ONE PR for judgment calls: new repos, rebrands, graveyard-rescues,
    hygiene fixes (in generate.py/source), stale-prose flags, ranking tweaks
  - notifies CEO: GitHub PR (email+mobile push) + Slack
        │
        ▼
  CEO reviews + merges PR ──> next Flow 1 run renders the changes (loop closed)
```

## Flow 1 details (deterministic — extend the existing Action)

Existing: refresh stars → re-rank → regenerate → commit → fail-email. Additions:

### 1a. Graveyard split
- `refresh_stars.py` already detects `archived`. Stamp each archived entry with `archived: true` and `archived_since: <YYYY-MM-DD first-seen-archived>` in the generate.py META/data.
- `generate.py` renders archived entries in a dedicated **⚰️ Graveyard** section (running list), pulled OUT of the main categories, retaining last-known star count + archive date. Never delete a graveyard entry → integrity.
- **Allowlist override:** a `KEEP_DESPITE_ARCHIVED` set in `generate.py`. Archived repos on this list stay in the main list (flagged), not graveyarded. Flow 2 proposes additions to this set (historically-important repos).

### 1b. Integrity guardrails (fail loud)
After generate.py, the Action asserts and fails (→ fail-email) if:
- any category that was non-empty last run is now empty,
- the custom intro block or any comparison's prose block is missing/shorter-than-threshold,
- total project_count dropped by more than a small delta without a corresponding graveyard move.
Purpose: regeneration can never silently drop editorial/navigation content.

### 1c. Candidate discovery (feeds Flow 2)
- `discover_candidates.py` (new) uses GitHub search (Action has API) for plausible new harnesses (query heuristics: topics/keywords like "agent", "coding-agent", "agent-harness"; min stars; not already listed; not archived).
- Writes candidates + the run's MOVED/ARCHIVED/FAILED/movers into `curation-queue.json`.

## Flow 2 details (judgment — Claude routine, hybrid)

- **Host:** Claude Code cloud routine (always-on, subscription-billed). Bound repo: `best-of-Agent-Harnesses` ONLY. Reads `curation-queue.json` + the repo's own files. Never calls api.github.com for third-party repos.
- **Cadence:** biweekly.
- **Versioned prompt:** `.claude/routines/biweekly-improve.md` (source of truth; the app routine pastes from it), same pattern as `weekly-rescore.md`.
- **Hybrid output:**
  - Auto-apply (mechanical, low-risk): `MOVED` → update `github_id` + META key.
  - One PR for judgment calls: vetted new repos (against the curation bar in CLAUDE.md), rebrand resolutions, `KEEP_DESPITE_ARCHIVED` additions, README/editorial hygiene fixes **made in generate.py/templates/source (never the rendered files)**, stale comparison-prose flags (>60d since last edit), ranking "other-variable" tweaks.
  - PR body summarizes each proposed change with rationale + evidence.
- **Commit identity:** noreply (`25306145+RyanAlberts@users.noreply.github.com`), per repo CLAUDE.md. NOTE: the retired weekly-rescore app routine had drifted to a personal email — this routine must use noreply.

## Notification

Both channels, on PR creation:
1. **GitHub** — the PR itself (email + Claude/GitHub mobile push). Always available.
2. **Slack** — routine posts a message with the PR link + a one-line summary. **Requires** the Slack connector to be authorized on the account and attached to the routine (see Open items).

## Data model: curation-queue.json

```jsonc
{
  "generated": "2026-07-03",           // Flow 1 run date (America/Chicago)
  "movers": [ {"id": "...", "from": N, "to": M} ],
  "moved":    [ {"id": "old/name", "to": "new/name"} ],
  "archived": [ {"id": "...", "since": "YYYY-MM-DD", "stars": N} ],
  "failed":   [ {"id": "...", "status": "404|403|..."} ],
  "candidates": [ {"id": "owner/repo", "stars": N, "topics": [...], "desc": "..."} ]
}
```

## Decisions (confirmed)

- Flow 2 host: **Claude routine** (not a second Action calling the API — avoids metered spend + key mgmt).
- Notification: **both** GitHub + Slack.
- Cadence: **biweekly**.
- Graveyard: **auto-graveyard-except-`KEEP_DESPITE_ARCHIVED`-allowlist**.

## Open items (need CEO / external)

1. **Slack connector** — not currently connected (the Claude Code UI shows "Try the Slack app — Install"; `plugin:productivity:slack` is unauthorized). One-time OAuth by the CEO required; cannot be done headlessly. Until then, Flow 2 notifies via GitHub only.
2. **App routine creation** — the biweekly routine must be created in claude.ai → Code → Routines from the versioned prompt, bound to `best-of-Agent-Harnesses`, Slack connector attached. (The versioned prompt + queue will be ready; creation is a UI step.)

## Rollout order

1. Flow 1 code: `archived`/`archived_since` + Graveyard rendering + `KEEP_DESPITE_ARCHIVED` + guardrail asserts + `curation-queue.json` emission. Test locally, PR.
2. `discover_candidates.py` + wire into the Action + queue.
3. `.claude/routines/biweekly-improve.md` prompt.
4. CEO: connect Slack, create the routine, first supervised run.
```
