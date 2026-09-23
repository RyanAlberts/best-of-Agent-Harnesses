# One AGENTS.md for every coding agent

One briefing file that Codex, Claude Code, Cursor, OpenCode, GitHub Copilot, Gemini CLI, and Aider all read, so you write your build commands, conventions, and hard rules once instead of once per tool.

## What is in this template

| File | Copy it to | Why |
|---|---|---|
| [AGENTS.md](AGENTS.md) | the repo root | The briefing file. Fill in the `<...>` parts and delete what does not apply. |
| [CLAUDE.md](CLAUDE.md) | the repo root, only if you need it | Claude Code 2.1.277 and later reads `AGENTS.md` by itself when there is no `CLAUDE.md` ([docs](https://code.claude.com/docs/en/memory#agents-md)). Add this one-line import for older versions, or when you want Claude-only rules on top. |
| [.gemini/settings.json](.gemini/settings.json) | `.gemini/settings.json` | Gemini CLI reads `GEMINI.md` unless you point it at `AGENTS.md` ([agents.md](https://agents.md)). |
| [.aider.conf.yml](.aider.conf.yml) | the repo root | Aider loads the file only when told to ([agents.md](https://agents.md)). |

Codex, Cursor, OpenCode, GitHub Copilot's coding agent, Zed, Warp, Jules, goose, Amp, and Windsurf read `AGENTS.md` with no extra file ([the list at agents.md](https://agents.md)).

## Install

```sh
curl -fsSLO https://raw.githubusercontent.com/RyanAlberts/best-of-Agent-Harnesses/main/templates/agents-md/AGENTS.md
```

Or ask your agent to do it: with the [MCP server](../../mcp/) installed, say "get the agents-md template and fill it in for this repo". The agent reads your build files and fills in the commands; check what it writes.

## Why the file is shaped this way

- **Commands first.** Agents run them more than they read prose. Include the one-file test command: it is what the agent runs while it works.
- **Short.** The file loads into every session and every line costs context. Claude Code's docs target under 200 lines; this template starts near 60. Long procedures go in `docs/` and get a link, so the agent loads them only when the task needs them. The [context files guide](../../comparisons/progressive-disclosure.md) explains this pattern.
- **Always, Ask first, Never.** Three lists read faster than paragraphs, and "ask first" gives the agent a safe middle option instead of guessing.
- **Nested files for big repos.** A subdirectory can have its own `AGENTS.md`; the closest file to the code being edited wins.

Instructions are advice, not enforcement. An agent can still ignore "Never push to main". To block an action for real, use a permission rule or a hook: the [safe Claude Code settings template](../claude-code-safe-settings/) does this for Claude Code.

## Go further

- Step by step, including how to test that each tool picked the file up: [Write one AGENTS.md for every coding agent](../../playbooks/one-agents-md-for-every-coding-agent.md).
- Compare AGENTS.md, CLAUDE.md, skills, and MCP tool search: [Context files for agents](../../comparisons/progressive-disclosure.md).
