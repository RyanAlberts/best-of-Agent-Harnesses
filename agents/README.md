# Agent templates

Don't just read the list. Hire it.

These are installable agents that navigate the harness space for you, powered by the same live data as the [ranked list](../README.md) — [harnesses.json](../harnesses.json) rescores every week, so the agents never go stale and never answer from training-data memory.

| Agent | What it does | Run it |
|-------|--------------|--------|
| [**harness-scout**](harness-scout.md) | You describe what you're building; it picks your harness, with two alternatives and evidence. Checks the graveyard so you never adopt a dead framework. | On demand |
| [**stack-auditor**](stack-auditor.md) | Points at your codebase, finds the harnesses you already depend on, and flags the ones that died. A dependency doctor for your agent stack. | On demand, or in CI |
| [**harness-radar**](harness-radar.md) | Diffs the list week over week: climbers, arrivals, deaths, graduations. Ends with the one change worth acting on. | Weekly, on a schedule |

## Install (Claude Code)

Each template is a standard subagent file. Drop it into your project's `.claude/agents/` (or `~/.claude/agents/` for all projects):

```sh
mkdir -p .claude/agents
curl -fsSL https://raw.githubusercontent.com/RyanAlberts/best-of-Agent-Harnesses/main/agents/harness-scout.md -o .claude/agents/harness-scout.md
```

Then ask normally: "what harness should I use for an unattended batch agent?" Claude Code routes to the scout on its own, or invoke it explicitly.

## Other tools

The YAML frontmatter is Claude Code convention; everything below it is a plain system prompt. Paste the body into any tool that takes custom instructions (Cursor rules, a GPT, an API system prompt) and it works the same way, as long as the tool can fetch a URL.

## Sharper answers: the MCP server

The templates fetch raw JSON, which any tool can do. If your tool speaks MCP, install the [agent-harnesses MCP server](../mcp/) instead and the same questions get answered through purpose-built tools (`recommend`, `compare_for`, `pick_harness`):

```sh
claude mcp add agent-harnesses -- uvx agent-harnesses-mcp
```

The scout template already prefers the MCP server when it's present, so installing both is the best setup.

## Design rules these agents follow

- **Fetch fresh, every run.** The dataset is the authority; a failed fetch means "say so and stop", never "answer from memory".
- **Graveyard is a hard veto.** Curation is the point: a starred repo is not automatically a credible one.
- **One pick, stated first.** Alternatives exist for named trade-offs, not for hedging.

Improvements welcome — same [contribution flow](../CONTRIBUTING.md) as the list itself.
