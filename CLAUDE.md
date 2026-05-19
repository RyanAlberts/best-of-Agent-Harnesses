# Repo notes for AI coding agents

## Commit identity (required)

All commits in this repo must be authored as:

- **Name:** `Ryan Alexander Alberts`
- **Email:** `ryan.a.alberts@gmail.com`

so they count toward [@RyanAlberts](https://github.com/RyanAlberts)'s GitHub contribution graph. Set both author and committer — GitHub matches on author email, but matching the committer too keeps the trailer clean.

If the local `git config` is wrong or unset, override per-commit instead of editing global config:

```sh
TZ='America/Chicago' \
git -c user.email='ryan.a.alberts@gmail.com' \
    -c user.name='Ryan Alexander Alberts' \
    commit --author='Ryan Alexander Alberts <ryan.a.alberts@gmail.com>' \
    -m "..."
```

`TZ='America/Chicago'` is required on every commit. The user works from Dallas, TX (CST/CDT) and the contribution graph buckets commits by their local timezone; UTC-stamped commits land on the wrong calendar day. Do not rely on whatever timezone the sandbox happens to be in.

Do not use `noreply@anthropic.com`, `@users.noreply.github.com`, or any university email unless explicitly requested. Get it right on the first commit; don't amend just to fix attribution unless asked.

## Branching and pushing (required)

Land changes on `main` by default — no review ceremony. If the working branch is a `claude/*` branch, fast-forward `main` to it and push. If branch protection rejects direct pushes to `main` (HTTP 403), open a PR from the working branch and immediately self-merge it via the GitHub API; don't wait for review unless the user explicitly asks. Only keep a separate feature branch when the user explicitly asks for a PR or review.

## Verifying contribution credit (required)

After every push, verify the new commits credit [@RyanAlberts](https://github.com/RyanAlberts) before reporting the work as done. For each newly pushed commit SHA on `main`:

1. Call `mcp__github__get_commit` (or `list_commits`).
2. Assert both:
   - `author.login == "RyanAlberts"` (not `null`)
   - `commit.author.email == "ryan.a.alberts@gmail.com"` (or `RyanAlberts@users.noreply.github.com` for merge commits the GitHub API itself authored)
3. If `author.login` is `null`, the author email isn't a verified email on the account. Don't silently move on — stop, tell the user the SHA and the bad email, and offer to amend:
   - On a `claude/*` working branch: amend with the canonical email and force-push the working branch.
   - Already on `main`: amend locally, then re-land via the PR-then-self-merge fallback. Never force-push `main`.
4. If `author.login` is correct but the contribution graph still shows nothing, suspect commit dates in the future relative to GitHub's real-world clock — the graph backfills retroactively when the calendar reaches that date. Surface this to the user; don't attempt to rewrite dates.

Skip this check only if the user explicitly says "don't validate."

## How the list is generated

`projects.yaml`, `README.md`, and `config/header.md` are all produced by `scripts/generate.py`. Edit the Python data structures in that script — never hand-edit the three output files — then run:

```sh
python3 scripts/generate.py
```

`REPO_ROOT` in the script resolves relative to the file, so it works from any checkout.

## Style conventions for entries

- **Description:** one sentence that names the **harness** (the agent loop, tool wiring, approval model) and contrasts it with the UI shell where relevant. Bold the word **harness** when distinguishing harness vs. shell.
- **OSS marker:** `✅` for standard OSS (MIT/Apache/BSD/GPL/MPL/AGPL/CC0); `⚠️ <license>` for source-available/restricted (Fair-code, Elastic-2.0, Polyform, FSL); `❓` for missing or unclear license.
- **Simplicity ↔ capability:** short parenthetical positioning the project on the axis (e.g., "Simple (format only)", "Mid (CLI, git-aware, MCP)", "Capability (Docker runtime, multi-surface agent)").
- Categories are fixed in `CATEGORIES`; don't invent new ones without discussion.

## Curation bar

- Skip personal repos with single-digit stars or fewer than ~10 commits.
- Skip archived/abandoned projects unless they're historically important; flag them in the description.
- When a project has moved org (e.g. `awslabs/agent-squad` → `2FastLabs/agent-squad`), update `github_id` to the new canonical location.
- When an official version supersedes a community version (e.g. official `github/github-mcp-server` vs. older community forks), prefer the official.
