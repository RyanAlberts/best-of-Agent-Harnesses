# Repo notes for AI coding agents

## Commit identity (required)

All commits in this repo must be authored as:

- **Name:** `Ryan Alexander Alberts`
- **Email:** `ryan.a.alberts@gmail.com`

so they count toward [@RyanAlberts](https://github.com/RyanAlberts)'s GitHub contribution graph. Set both author and committer — GitHub matches on author email, but matching the committer too keeps the trailer clean.

If the local `git config` is wrong or unset, override per-commit instead of editing global config:

```sh
git -c user.email='ryan.a.alberts@gmail.com' \
    -c user.name='Ryan Alexander Alberts' \
    commit --author='Ryan Alexander Alberts <ryan.a.alberts@gmail.com>' \
    -m "..."
```

Do not use `noreply@anthropic.com`, `@users.noreply.github.com`, or any university email unless explicitly requested. Get it right on the first commit; don't amend just to fix attribution unless asked.

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
