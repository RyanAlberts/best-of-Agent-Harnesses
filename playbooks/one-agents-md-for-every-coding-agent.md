# Write one AGENTS.md for every coding agent

Write one briefing file that Codex, Claude Code, Cursor, OpenCode, Copilot, Gemini CLI, and Aider all read, test that each tool actually loaded it, and keep it short enough to help instead of hurt. You finish with the AGENTS.md template filled in for your repo.

**Time:** 30 minutes. **Template:** [one AGENTS.md for every coding agent](../templates/agents-md/). **You need:** a repo and at least one coding agent.

A good briefing file reads like a model upgrade; a bad one is worse than none, because it fills the context window with things the agent did not need (the [context files guide](../comparisons/progressive-disclosure.md) covers the debate). The steps below keep it on the good side.

## Step 1: Start from the template

```sh
curl -fsSLO https://raw.githubusercontent.com/RyanAlberts/best-of-Agent-Harnesses/main/templates/agents-md/AGENTS.md
```

If you already have a `CLAUDE.md`, `.cursorrules`, or `GEMINI.md`, open it next to the template. You are merging them into one file.

## Step 2: Fill in the commands first

Write the exact commands for install, build, full test, one-file test, lint, and run. Copy them from your `package.json`, `Makefile`, or CI file, then run each one to make sure it works. Agents run these commands more than they read anything else in the file, and a wrong command costs a whole round of failed attempts.

You can let your agent draft this: "Read package.json and the CI config, then fill in the Commands section of AGENTS.md. Run each command to check it." Check the result yourself.

## Step 3: Write rules the agent could not guess

For Conventions and Boundaries, write only what the code does not already show. "Use TypeScript" is visible in the repo; "never edit files in src/generated/, change the generator instead" is not. A useful test for each line: has an agent, or a new teammate, gotten this wrong before? If not, cut it.

Sort hard rules into **Always**, **Ask first**, and **Never**. "Ask first" matters: it gives the agent a safe option instead of guessing between doing and not doing.

## Step 4: Move long procedures out

The file loads into every session, so keep it under about 150 lines. Anything that is a multi-step procedure (releasing, database migrations, adding an API endpoint) goes in `docs/`, with one line in AGENTS.md pointing to it. The agent opens the doc only when the task needs it. For monorepos, give each package its own `AGENTS.md`; the file closest to the code being edited wins.

## Step 5: Connect the tools that need a nudge

Most tools read `AGENTS.md` at the repo root with no setup: Codex, Cursor, OpenCode, GitHub Copilot's coding agent, Zed, Warp, Jules, goose, Amp, and Windsurf ([agents.md](https://agents.md)). Three need a small extra step, and the template includes each file:

- **Claude Code** 2.1.277 and later reads `AGENTS.md` when the repo has no `CLAUDE.md` ([docs](https://code.claude.com/docs/en/memory#agents-md)). If you keep a `CLAUDE.md`, or run an older version, put `@AGENTS.md` on its first line.
- **Gemini CLI**: add `.gemini/settings.json` with `{"context": {"fileName": "AGENTS.md"}}`.
- **Aider**: add `.aider.conf.yml` with `read: AGENTS.md`.

Then delete the old per-tool files, or reduce each to a pointer, so the rules live in one place.

## Step 6: Test that each tool loaded it

Do not assume. In each tool, start a fresh session and ask: "What is the one-file test command for this repo, and what are you never allowed to do here?" The answer should quote your file. In Claude Code, `/context` lists the memory files it loaded, and a session with no `CLAUDE.md` prints a line naming the `AGENTS.md` it read.

## Step 7: Back the Never list with enforcement

AGENTS.md is advice. A model can still push to main if it decides that is what you want. For anything that must not happen, add a technical block as well: permission rules and a hook in Claude Code (the [safe settings template](../templates/claude-code-safe-settings/)), approval settings in Codex, and branch protection on the remote for everyone.

## Step 8: Keep it current

Treat the file like code. When an agent makes the same mistake twice, add one line. When a line stops being true, delete it. Review it when you change your build or test setup, since a stale command is the most common way these files go bad.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). Spot an error or a tool that reads the file differently? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._

_Agents can fetch the template directly: `claude mcp add agent-harnesses -- uvx agent-harnesses-mcp`, then `get_template("agents-md")`._
