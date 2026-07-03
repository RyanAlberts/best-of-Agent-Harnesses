# Two-Flow Curation System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a deterministic graveyard/guardrail layer + candidate discovery to the weekly Action (Flow 1), and a biweekly judgment routine (Flow 2) that proposes curation improvements as a reviewed PR + notification.

**Architecture:** Flow 1 (GitHub Action) owns all third-party GitHub API work and writes `curation-queue.json`. Flow 2 (Claude routine, bound to this repo only) reads that file, never calls the GitHub API, and drafts a PR. See spec: `docs/superpowers/specs/2026-07-03-improve-flow-design.md`.

**Tech Stack:** Python 3.11 stdlib only (no new deps), pytest for tests, GitHub Actions, Claude Code routine.

## Global Constraints

- Python 3.11, standard library only — no new pip dependencies (matches existing scripts).
- Never hand-edit generated files (README.md, TAGS.md, harnesses.json, llms.txt, feed.json, *.svg, comparisons/*.md star rows). Edit `scripts/generate.py` data/logic.
- Commit identity: author + committer `Ryan Alexander Alberts <25306145+RyanAlberts@users.noreply.github.com>`, `TZ='America/Chicago'`. Never a personal email.
- `generate.py` must remain importable without side effects (guarded by `if __name__ == "__main__"`), so tests can `import generate`.
- All Flow 1 work is deterministic. Flow 2 never calls api.github.com for third-party repos.
- Land Flow 1 as a PR (reshapes the public README) — do not push straight to main.

---

## Task 1: Archived detection persists to a data structure

**Files:**
- Modify: `scripts/refresh_stars.py` (add archived capture + write `ARCHIVED` block into generate.py)
- Modify: `scripts/generate.py` (add `ARCHIVED` dict near `META`, ~line 507)
- Test: `tests/test_archived.py`

**Interfaces:**
- Produces: `generate.ARCHIVED: dict[str, str]` mapping `github_id -> "YYYY-MM-DD"` (date first seen archived). `refresh_stars.fetch()` already returns repo JSON containing `archived` (bool); capture it.

- [ ] **Step 1: Write failing test** — `tests/test_archived.py`:

```python
import generate
def test_archived_is_dict_of_dates():
    assert isinstance(generate.ARCHIVED, dict)
    for gid, since in generate.ARCHIVED.items():
        assert "/" in gid
        assert len(since) == 10 and since[4] == "-"  # YYYY-MM-DD
```

- [ ] **Step 2: Run, verify it fails** — `cd scripts && python3 -m pytest ../tests/test_archived.py -v` → FAIL (`ARCHIVED` undefined).
- [ ] **Step 3: Add `ARCHIVED` to generate.py** just after the `META` dict (post ~line 630): `ARCHIVED: "dict[str, str]" = {}` seeded with the 4 currently-archived ids and today's date (`spring-ai-community/spring-ai-tool-search-tool`, `RooCodeInc/Roo-Code`, `SeanHogg/BuilderForceAgents`, `gsd-build/get-shit-done` → `"2026-07-03"`).
- [ ] **Step 4: Extend `refresh_stars.py`** — in the fetch loop, record `archived` from the repo JSON; after writing META, rewrite the `ARCHIVED = {...}` block in generate.py: keep existing `since` dates for still-archived repos, add today's date for newly-archived, drop entries no longer archived. Preserve formatting like the existing META rewrite.
- [ ] **Step 5: Run test** → PASS.
- [ ] **Step 6: Commit** — `git commit -m "feat: persist archived repos + first-seen date"`.

## Task 2: Graveyard routing in generate.py

**Files:**
- Modify: `scripts/generate.py` — add `KEEP_DESPITE_ARCHIVED`, `is_graveyard()`, split ordering
- Test: `tests/test_graveyard.py`

**Interfaces:**
- Consumes: `generate.ARCHIVED` (Task 1).
- Produces: `generate.KEEP_DESPITE_ARCHIVED: set[str]`; `generate.is_graveyard(github_id: str) -> bool`; `generate.graveyard_projects() -> list[Project]`; `ordered_projects()` EXCLUDES graveyard entries.

- [ ] **Step 1: Write failing test** — `tests/test_graveyard.py`:

```python
import generate
def test_is_graveyard_respects_allowlist():
    gid = next(iter(generate.ARCHIVED))
    assert generate.is_graveyard(gid) is True
    generate.KEEP_DESPITE_ARCHIVED.add(gid)
    assert generate.is_graveyard(gid) is False
    generate.KEEP_DESPITE_ARCHIVED.discard(gid)
def test_ordered_excludes_graveyard():
    ids = {p.github_id for p in generate.ordered_projects()}
    assert not (ids & {g for g in generate.ARCHIVED if generate.is_graveyard(g)})
def test_graveyard_projects_are_archived():
    for p in generate.graveyard_projects():
        assert p.github_id in generate.ARCHIVED
```

- [ ] **Step 2: Run, verify fail** → FAIL.
- [ ] **Step 3: Implement** — add `KEEP_DESPITE_ARCHIVED: "set[str]" = set()` near `ARCHIVED`; `is_graveyard(gid)` = `gid in ARCHIVED and gid not in KEEP_DESPITE_ARCHIVED`; `graveyard_projects()` returns all Projects across PROJECTS whose id is graveyard, sorted by `stars_for` desc; modify `ordered_projects()` to skip `is_graveyard(x.github_id)`.
- [ ] **Step 4: Run** → PASS.
- [ ] **Step 5: Commit** — `git commit -m "feat: graveyard routing + KEEP_DESPITE_ARCHIVED allowlist"`.

## Task 3: Render the Graveyard section + exclude from counts/surfaces

**Files:**
- Modify: `scripts/generate.py` — `generate_readme()` (~1066), `count_projects()` (~972), `generate_harnesses_json()` (~1362), `generate_landscape_svg()` (~1477)
- Test: `tests/test_render_graveyard.py`

**Interfaces:**
- Consumes: `graveyard_projects()`, `is_graveyard()` (Task 2).
- Produces: README contains a `## ⚰️ Graveyard` section listing archived entries with last stars + `archived_since`; main category loops skip graveyard entries; `count_projects()` counts only live projects; a parallel `graveyard_count()`.

- [ ] **Step 1: Write failing test** — `tests/test_render_graveyard.py`:

```python
import generate
def test_readme_has_graveyard_section_and_excludes_from_main():
    md = generate.generate_readme()
    assert "## ⚰️ Graveyard" in md
    gid = next(g for g in generate.ARCHIVED if generate.is_graveyard(g))
    body, _, grave = md.partition("## ⚰️ Graveyard")
    assert gid in grave and gid not in body  # archived repo only under Graveyard
```

- [ ] **Step 2: Run, verify fail** → FAIL (no Graveyard section).
- [ ] **Step 3: Implement** — in `generate_readme()`, after the category loop, append a Graveyard section rendering `graveyard_projects()` (name, last stars via `format_stars`, `archived_since`, one-line "archived — kept for integrity"). Ensure the category rendering loop iterates live projects only (it uses `PROJECTS[cat_id]`; filter `is_graveyard`). Update `count_projects()` to exclude graveyard; add `graveyard_count()`. Exclude graveyard from `generate_harnesses_json()` projects array (or add `"archived": true` + separate list — choose exclusion from main array, add `graveyard` array) and from `generate_landscape_svg()` plotting.
- [ ] **Step 4: Run** → PASS; then full run `cd scripts && GH_TOKEN=$(gh auth token) TODAY=$(TZ=America/Chicago date +%F) python3 generate.py` and eyeball README Graveyard section.
- [ ] **Step 5: Commit** — `git commit -m "feat: render Graveyard section; exclude archived from live surfaces"`.

## Task 4: Integrity guardrails (fail loud)

**Files:**
- Create: `scripts/check_integrity.py`
- Test: `tests/test_integrity.py`

**Interfaces:**
- Produces: `check_integrity.main()` exits non-zero with a clear message if any invariant fails. Run in the Action after generate.py.

Invariants:
1. Every live category in `CATEGORIES` has ≥1 project.
2. README contains the custom intro marker (define a stable sentinel string present in `config/header.md`) and each `comparisons/*.md` still has its prose (file length ≥ N bytes / contains a known heading).
3. `live_count + graveyard_count` did not drop by >2 vs the value recorded in `harnesses.json` on the previous commit (read via `git show HEAD:harnesses.json`), unless the drop equals a graveyard move.

- [ ] **Step 1: Write failing test** — `tests/test_integrity.py` constructs a temp scenario (monkeypatch `generate.PROJECTS` to empty one category) and asserts `check_integrity.verify()` raises/returns error.
- [ ] **Step 2: Run, verify fail** → FAIL (module missing).
- [ ] **Step 3: Implement** `check_integrity.py` with a `verify() -> list[str]` returning violation strings and `main()` that prints them and `sys.exit(1)` if any.
- [ ] **Step 4: Run** → PASS.
- [ ] **Step 5: Commit** — `git commit -m "feat: integrity guardrails for regeneration"`.

## Task 5: Emit curation-queue.json

**Files:**
- Modify: `scripts/refresh_stars.py` (collect movers/moved/archived/failed into a dict)
- Create: `scripts/write_queue.py` (writes `curation-queue.json`)
- Test: `tests/test_queue.py`

**Interfaces:**
- Produces: `curation-queue.json` at repo root with keys `generated, movers, moved, archived, failed, candidates` (candidates filled by Task 6; `[]` for now). Schema per spec.

- [ ] **Step 1: Write failing test** — assert the JSON has all six keys and `generated` is `YYYY-MM-DD`.
- [ ] **Step 2: Run, verify fail** → FAIL.
- [ ] **Step 3: Implement** — have `refresh_stars.py` accumulate its already-computed movers/MOVED/ARCHIVED/FAILED and call `write_queue.write(data)`; candidates default `[]`.
- [ ] **Step 4: Run** → PASS.
- [ ] **Step 5: Commit** — `git commit -m "feat: emit curation-queue.json from the weekly audit"`.

## Task 6: Candidate discovery

**Files:**
- Create: `scripts/discover_candidates.py`
- Test: `tests/test_discover.py` (mock urllib; do NOT hit the network in tests)

**Interfaces:**
- Produces: `discover_candidates.find(token, known_ids) -> list[dict]` — GitHub search (`/search/repositories`) over agent-harness heuristics (topics: `ai-agents`, `llm-agents`, `agent-framework`; keywords in name/desc), min stars threshold (e.g. 300), excluding `known_ids` and archived. Merged into `curation-queue.json`.

- [ ] **Step 1: Write failing test** with a mocked search response asserting filtering (excludes known ids, excludes < min stars, excludes archived).
- [ ] **Step 2: Run, verify fail** → FAIL.
- [ ] **Step 3: Implement** using `urllib` + token, same header pattern as `refresh_stars.fetch`.
- [ ] **Step 4: Run** → PASS.
- [ ] **Step 5: Commit** — `git commit -m "feat: candidate discovery for new harnesses"`.

## Task 7: Wire Flow 1 Action

**Files:**
- Modify: `.github/workflows/weekly-rescore.yml`

- [ ] **Step 1:** After `generate.py`, add steps: run `discover_candidates.py` → merge into queue, run `check_integrity.py` (fails the job loudly), and include `curation-queue.json` in the commit. Keep the job summary.
- [ ] **Step 2:** Trigger via `workflow_dispatch`, confirm green + `curation-queue.json` on main + integrity step present.
- [ ] **Step 3: Commit** — `git commit -m "ci: run discovery + integrity, commit curation queue"`.

## Task 8: Flow 2 routine prompt

**Files:**
- Create: `.claude/routines/biweekly-improve.md` (versioned prompt; already drafted in this session — verify it matches final schema)

- [ ] **Step 1:** Ensure the prompt: reads `curation-queue.json`; auto-applies MOVED redirects; drafts ONE PR for judgment calls (new repos vetted vs CLAUDE.md bar, rebrands, KEEP_DESPITE_ARCHIVED additions, hygiene fixes in generate.py, stale-prose flags, ranking tweaks); commits noreply; posts PR link to Slack + relies on GitHub notification; **only touches the bound repo**.
- [ ] **Step 2: Commit** — `git commit -m "docs: biweekly improve routine prompt"`.

## Manual (CEO / UI — cannot be scripted)

- Connect the Slack connector (one-time OAuth) and attach it to the routine.
- Create the biweekly routine in claude.ai → Code → Routines from `biweekly-improve.md`, bound to `best-of-Agent-Harnesses`, biweekly cadence, Slack connector attached.
- Supervise the first Flow 2 run; merge/adjust its PR.

## Self-Review

- **Spec coverage:** graveyard (T1–3), guardrails (T4), queue (T5), discovery (T6), Action wiring (T7), routine (T8), notifications + manual UI steps (Manual). Ranking "other-variable" tweaks and hygiene fixes are Flow 2 prompt responsibilities (T8), not code. All spec sections mapped.
- **Placeholders:** integrity thresholds (N bytes, >2 delta) are concrete; sentinel strings to be read from actual `config/header.md` at execution.
- **Type consistency:** `ARCHIVED: dict[str,str]`, `KEEP_DESPITE_ARCHIVED: set[str]`, `is_graveyard(str)->bool`, `graveyard_projects()->list[Project]`, `count_projects()`/`graveyard_count()` used consistently across T1–4.
