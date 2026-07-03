# Biweekly improve routine — paste as the routine prompt in claude.ai → Code → Routines

<!-- Versioned here so the prompt evolves with the repo. This is Flow 2 (judgment)
     of the two-flow curation system. Flow 1 is the weekly GitHub Action
     (.github/workflows/weekly-rescore.yml), which does ALL third-party GitHub API
     work and writes curation-queue.json. Spec:
     docs/superpowers/specs/2026-07-03-improve-flow-design.md -->

## Setup (one-time, in the routine's config)
- Repository: bind ONLY `RyanAlberts/best-of-Agent-Harnesses`.
- Connectors: Slack (for notification).
- Cadence: biweekly.

## Prompt

Biweekly curation-improvement pass for RyanAlberts/best-of-Agent-Harnesses.
Use today's date in America/Chicago as TODAY (YYYY-MM-DD).

HARD RULE — you MUST NOT call the GitHub REST API for any third-party repo.
This session is scoped to the bound repo only; third-party calls will 403. ALL
external repo data you need is already in `curation-queue.json`, produced by the
weekly Action. Work only from that file and the repo's own contents.

PRE-FLIGHT:
1. cd into the repo. `git fetch origin && git checkout main && git reset --hard origin/main`.
2. Read `curation-queue.json`. If it is missing or its `generated` date is older
   than 21 days, STOP and report "stale/absent queue — check the weekly Action";
   do not proceed on stale data.

APPLY (hybrid — mechanical auto, judgment via PR):

A. Auto-apply (mechanical, low-risk) — directly on a working branch:
   - For each entry in `queue.moved`: update that project's `github_id` and its
     `META` key in `scripts/generate.py` from the old to the new canonical name.
     Mechanical redirect only — do NOT change display names or descriptions.

B. Judgment calls — assemble into ONE pull request with a clear body. For each,
   include the rationale + the evidence line from the queue:
   - `queue.candidates`: vet each against the curation bar in CLAUDE.md (skip
     single-digit-star or <~10-commit repos; prefer official over community).
     Add the ones that clearly belong, in the right CATEGORY, with a one-sentence
     harness-focused description and the OSS marker. Flag borderline ones in the
     PR body for a decision instead of adding.
   - `queue.archived` rebrands / historically-important repos: if an archived
     repo is historically important, propose adding it to
     `KEEP_DESPITE_ARCHIVED` in `scripts/generate.py` (keeps it in the live list,
     flagged) rather than letting it graveyard. Explain why.
   - README / editorial hygiene: review the RENDERED README/TAGS for AI-slop,
     dead structure, incoherent ordering, or stale claims. Fix at the SOURCE
     (`scripts/generate.py`, templates, or project data) — NEVER hand-edit the
     rendered files; they are regenerated. If you change generation logic, run
     `python3 scripts/generate.py` and include the regenerated output in the PR.
   - Editorial freshness: for each `comparisons/*.md`, if the last commit
     touching it is >60 days old (`git log -1 --format=%cs -- <file>`), flag it
     in the PR body as "needs an editorial review pass" — do NOT rewrite prose
     unprompted.
   - Ranking beyond stars: raw star ordering is already automatic in the Action.
     Only propose a manual reposition when a project's Simplicity↔capability
     placement is clearly wrong or a fast-riser is mis-slotted; explain the call.

COMMIT + PR (noreply identity is REQUIRED — never a personal email):
- Branch: `improve-TODAY`.
- Commit auto-applied + judgment changes:
    TZ='America/Chicago' git -c commit.gpgsign=false \
      -c user.email='25306145+RyanAlberts@users.noreply.github.com' \
      -c user.name='Ryan Alexander Alberts' \
      commit -a --author='Ryan Alexander Alberts <25306145+RyanAlberts@users.noreply.github.com>' \
      -m "curation improvements TODAY"
- Push the branch and open a PR (base main) titled "Curation improvements TODAY".
  The PR body MUST list, in sections: MOVED redirects applied; new repos added;
  borderline candidates for decision; KEEP_DESPITE_ARCHIVED proposals; hygiene
  fixes; stale comparison pages (>60d); ranking proposals. If a section is empty,
  say "none".
- Do NOT merge. The CEO is the merge gate.

NOTIFY:
- Post to Slack: the PR URL + a one-line summary of what it proposes (e.g.
  "2 new repos, 1 graveyard-rescue, 3 hygiene fixes, 1 page flagged stale").
- The GitHub PR itself also notifies via email/mobile — that is the primary
  channel; Slack is the ping.

EXIT CRITERIA: a single open PR on best-of-Agent-Harnesses with the proposed
improvements + a structured body, credited to @RyanAlberts (noreply), and a
Slack message linking it. If the queue was empty of actionable items, open no PR
and post "biweekly improve: nothing actionable this cycle" to Slack.
