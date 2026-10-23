# agent-harnesses MCP server

`mcp-name: io.github.RyanAlberts/agent-harnesses`

The [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses) list as an MCP server, so agents can recommend harnesses instead of you reading 100+ table rows.

Single file, stdio transport, no clone needed — it fetches [harnesses.json](../harnesses.json) from this repo at startup (or reads it locally from a checkout). Requires [uv](https://docs.astral.sh/uv/).

<!-- HOSTED-URL-PENDING: hidden until the hosted address answers; see "Hosted connector (maintainer runbook)" below.
## Use it without installing

Add the server to your AI app by its web address. There is nothing to install and no sign-in.

Address: `https://HOSTED_URL/mcp`

- **Claude.ai and Claude Desktop:** open Settings, then Connectors, then Add custom connector. Paste the address and choose no sign-in. Free plans allow one custom connector.
- **ChatGPT:** add a custom MCP server, paste the address (it ends in `/mcp`), and choose no authentication. Your plan or workspace settings decide whether custom servers are allowed.
- **Cursor:** add this to `.cursor/mcp.json`:

  ```json
  {"mcpServers": {"agent-harnesses": {"url": "https://HOSTED_URL/mcp"}}}
  ```

- **Claude Code:** `claude mcp add --transport http agent-harnesses https://HOSTED_URL/mcp`

The hosted server runs the same `server.py` as the package, with the same tools. It reads the list from this repo's `main` branch and refreshes it every hour.
HOSTED-URL-PENDING -->

## Install

Published on [PyPI](https://pypi.org/project/agent-harnesses-mcp/) and the [official MCP registry](https://registry.modelcontextprotocol.io) as `io.github.RyanAlberts/agent-harnesses`. Claude Code:

```sh
claude mcp add agent-harnesses -- uvx agent-harnesses-mcp
```

Any other MCP client (Cursor, Codex, Gemini CLI, ...):

```json
{
  "mcpServers": {
    "agent-harnesses": {
      "command": "uvx",
      "args": ["agent-harnesses-mcp"]
    }
  }
}
```

No-install alternative — run the single source file straight from this repo:

```sh
claude mcp add agent-harnesses -- uv run https://raw.githubusercontent.com/RyanAlberts/best-of-Agent-Harnesses/main/mcp/server.py
```

## Tools

| Tool | What it does |
|---|---|
| `recommend(need, language?, must_run_unattended?, open_source_only?)` | **Opinionated single recommendation** — a decision, not a list. Returns one top pick with the reason, up to two alternatives, any harnesses to **avoid** for this need (archived, or flagged for star manipulation — with why), and the most relevant decision guide to read next. |
| `pick_harness(use_case, max_complexity?, min_autonomy?, min_recovery?, open_source_only?, limit?)` | Ranked recommendations for a use case, seeded by the list's hand-curated use-case index. `max_complexity` caps adoption surface (`super simple` → `complex`); `min_autonomy` requires a designed autonomy regime (`step-gated` → `headless`); `min_recovery` requires a failure-recovery tier (`none` → `durable`). |
| `pick_infrastructure(need, level?, include_live_search?, open_source_only?, limit?)` | **Full-stack picks that aren't limited to the list.** Infers (or takes) the stack level (model-access, harness, orchestration, sandboxing, browser, memory, context, tools, evals, observability, security, skills), returns curated picks plus a **live discovery pass**: a GitHub search for fresh repos (already-listed and graveyard repos removed) and recent high-signal Hacker News stories, both labeled `unvetted`. Degrades gracefully offline; live search sends only the need text to api.github.com and hn.algolia.com. |
| `compare(github_ids)` | **Side-by-side of 2–4 harnesses** — "should I use X or Y?". Records aligned on the list's axes — including the researched deep-dive axes (sandboxing, context memory, lifecycle hooks, prompt optimization, build-vs-buy tier) — an edge summary naming who leads where, a warning when a requested repo is in the graveyard (archived or integrity-flagged), and the decision guide covering the matchup when one exists. |
| `compare_for(use_case, limit?, open_source_only?)` | **Task-based comparison** — "compare the best options for X" in one call. Ranks candidates like `pick_harness`, takes the top 2–4, and returns the full side-by-side with each pick's ranking reason. |
| `search_harnesses(query, limit?)` | Keyword search across names, descriptions, tags, and categories. |
| `get_harness(github_id)` | Full record for one project. |
| `list_comparisons()` | The head-to-head decision guides (OpenClaw vs Hermes, terminal coding agents, …) with summaries. |
| `get_comparison(slug)` | Full markdown of one guide — architecture trade-offs, field reports, billing reality. Always current: served from the repo's `main`. |
| `list_templates()` | Copy-paste setup files (an AGENTS.md every coding agent reads, safe Claude Code settings, a minimal Python harness, …) with the files each contains. |
| `get_template(slug)` | A template's README plus the full content and target path of every file, so your agent can write them into your project and adapt them. |
| `list_playbooks()` / `get_playbook(slug)` | Step-by-step setup guides (build your own harness, one AGENTS.md for every agent, …). |
| `list_skills()` | Agent skills that check your own setup (what your agent can reach, whether its "tests pass" claims hold, where your tokens go, which guardrails leak, …), each with its install command. |
| `get_skill(name, target)` | Every file of one skill with the path to write it to, under `.claude/skills/` or `.agents/skills/`, so your agent can install it for you. |
| `list_categories()` | The categories, use-case intents, and the complexity/autonomy/recovery scales. |
| `whats_new(since?, limit?)` | The weekly digest: harnesses added or removed, the biggest star gains, the fastest growers, projects archived upstream, and new guides, skills, and templates. Pass `since` (YYYY-MM-DD) to catch up on everything after a date. |

Example: *"recommend('an always-on personal assistant that lives in my chat apps', open_source_only=True)"* → one top pick with the reason, two alternatives, anything to avoid for this need, and the guide to read next.

Example: *"compare(['openclaw/openclaw', 'NousResearch/hermes-agent'])"* → both records side by side, who leads on which axis, and a pointer to the *OpenClaw vs Hermes* guide.

Example: *"compare_for('an always-on personal assistant in my chat apps')"* → OpenClaw vs Hermes vs Khoj with each pick's ranking reason and the axis edges — OpenClaw leads stars, Hermes is simplest to adopt, Khoj takes the sandboxing edge (its generated code always runs isolated; the others' sandboxes are opt-in), OpenClaw and Hermes share the lifecycle-hooks edge — plus the *OpenClaw vs Hermes* decision guide to read next.

Example: *"compare_for('sandboxed code execution for generated code')"* → E2B vs Daytona vs smolagents side by side with `why_picked` reasons for each.

Example: *"pick_harness('sandboxed code execution for generated code', max_complexity='slightly complex', open_source_only=True)"* → E2B, smolagents, Daytona... each with stars, tier, license signal, and a one-line reason.

Data is regenerated by [`scripts/generate.py`](../scripts/generate.py); star counts carry a `stars_captured` date, and the comparisons index is rebuilt from `comparisons/*.md` on every refresh — the server always serves current `main`.

## Distribution

The server is packaged as **`agent-harnesses-mcp`** (this directory's `pyproject.toml`) and live in the official MCP registry as **`io.github.RyanAlberts/agent-harnesses`** (`server.json` at the repo root), which directories like Glama and PulseMCP crawl. The registry validates PyPI ownership via the `mcp-name:` marker at the top of this README — keep it.

## Publishing (maintainer runbook)

Releases are automated by [`.github/workflows/publish-mcp.yml`](../.github/workflows/publish-mcp.yml) on a `mcp-v*` tag: it builds the wheel, publishes to PyPI via trusted publishing, and publishes `server.json` to the official MCP registry via GitHub OIDC.

One-time setup, then never again:
1. On pypi.org: create the project name `agent-harnesses-mcp` → Settings → Publishing → add a **trusted publisher**: owner `RyanAlberts`, repo `best-of-Agent-Harnesses`, workflow `publish-mcp.yml`. No API tokens.
2. Nothing for the MCP registry — GitHub OIDC from this repo authorizes the `io.github.RyanAlberts/*` namespace automatically.

Per release: bump the version in `mcp/pyproject.toml` **and** `server.json` (the workflow fails loudly on mismatch), then `git tag mcp-v<version> && git push origin mcp-v<version>`.

Directories like Glama, PulseMCP, and mcpservers.org crawl the official registry — no per-directory submissions needed. (Smithery's current publish flow takes hosted-HTTP servers or `.mcpb` bundles, not stdio-from-GitHub, so this server isn't listed there by design.)

## Hosted connector (maintainer runbook)

The address in "Use it without installing" is a free Vercel Hobby project whose root directory is `mcp/`. Vercel imports `app` from [`app.py`](app.py) (set by `[tool.vercel]` in `pyproject.toml`), which serves `server.py` as a stateless Streamable HTTP app at `/mcp`. With no checkout around it, `server.py` fetches the list from `main` and refetches it every hour, so list updates need no redeploy. Hobby never bills: past its limits the project pauses.

Run the same mode locally with `uv run mcp/server.py --http`, then point a client at `http://127.0.0.1:8000/mcp`. [`tests/test_mcp_http.py`](../tests/test_mcp_http.py) starts it this way, lists the tools, and calls one.

First deploy, from this directory:

```sh
vercel login
vercel link --yes --project agent-harnesses-mcp
vercel deploy --prod
```

`vercel deploy --prod` prints the production address. Check that it answers:

```sh
curl -s -X POST https://<address>/mcp -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | head -c 200
```

A reply that starts with `event: message` and lists tools means it works. A Vercel login page means Deployment Protection covers the address: set it to Standard, which leaves production public. Then put the address into the hidden "Use it without installing" section at the top of this file and remove the two comment lines around it.

Run `vercel deploy --prod` again only when `server.py` or `app.py` changes.
