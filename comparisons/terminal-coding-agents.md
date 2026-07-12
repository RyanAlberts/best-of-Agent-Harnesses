# Terminal coding agents: opencode vs Codex vs Gemini CLI vs crush vs goose

The most-asked pick in this list: *"I want a turnkey coding agent in my terminal today."* These five are the open(ish)-source field. The closed first-party products (Claude Code, Cursor's agent) aren't list entries, but they define the workflow all five implement: a tool-call loop with file edit, shell, and search tools, wrapped in a terminal UI.

What actually differs between them is the **harness** — the agent loop, provider wiring, sandboxing, and extension model — not the chat-in-a-terminal experience, which has converged.

| | [opencode](https://github.com/anomalyco/opencode) | [Gemini CLI](https://github.com/google-gemini/gemini-cli) | [Codex](https://github.com/openai/codex) | [goose](https://github.com/aaif-goose/goose) | [crush](https://github.com/charmbracelet/crush) |
|---|---|---|---|---|---|
| ⭐ Stars | 185k | 106k | 97.3k | 51.1k | 26.5k |
| Steward | anomaly (community) | Google (first-party) | OpenAI (first-party) | Linux Foundation AAIF | Charm |
| License | open source | open source | open source | open source | ⚠️ FSL-1.1-MIT |
| Core language | TypeScript | TypeScript | Rust | Rust | Go |
| Model lock-in | None — Claude, OpenAI, Gemini, local | Gemini-first | OpenAI-first, multi-provider supported | None — provider choice by design | None — multi-provider |
| Autonomy (list axis) | headless | bounded | bounded | headless | bounded |
| Recovery (list axis) | resumable | resumable | resumable | resumable | resumable |
| Distinctive harness bet | Plugins + MCP, client/server split | First-party Gemini integration, MCP | Sandboxed execution as the default posture | MCP/ACP extensions, recipes, no fixed UI | Session persistence, TUI polish |

_Stars as captured for the main list (see [README](../README.md#guide-to-rankings) for the capture date)._

## Pick by situation

- **You want maximum freedom and the biggest community** → **opencode**. No model lock-in, the largest star count and contributor base in the category, and a client/server architecture that lets the harness run somewhere other than the terminal rendering it. The default pick in this list's use-case index.
- **You live on Gemini (or want the generous first-party free tier)** → **Gemini CLI**. The harness is the plugin/MCP loop; the reason to choose it is first-party Gemini support and Google's pace of investment, not harness novelty.
- **You care most about safe autonomous execution** → **Codex**. Its defining bet is the sandboxed tool-call loop ([sandboxing docs](https://developers.openai.com/codex/concepts/sandboxing)) — the strongest default isolation posture of the five. Best experience on OpenAI models/plans.
- **You want the harness without a bundled UI** → **goose**. Foundation-governed, Rust, and built around MCP/ACP extensions and recipes; you bolt it into whatever shell you use. The pick when you're integrating an agent into your own surface rather than adopting someone's terminal app.
- **You want the nicest TUI and session ergonomics, and FSL is acceptable** → **crush**. Charm's Bubble Tea craftsmanship plus persistent sessions. The ⚠️ FSL-1.1-MIT license (converts to MIT after two years) is the one structural caveat — fine for individual use, check it for redistribution.

## What they share

All five: tool-call loop over file/shell/search tools, MCP support (native or via plugins), permission prompts before destructive actions, and a config file for custom instructions. Switching costs between them are low by design — your AGENTS.md/instructions files port almost unchanged, so trying two is cheap.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._
