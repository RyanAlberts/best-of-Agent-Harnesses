# Terminal coding agents: opencode vs Codex vs Gemini CLI vs crush vs goose

The most-asked pick in this list: *"I want a turnkey coding agent in my terminal today."* A terminal coding agent is a program you run in your shell that takes a plain-language request, then works in a loop: the model proposes an action (edit this file, run this command, search the repo), the tool executes it and shows the model the result, and the loop continues until the job is done. That loop, plus the provider wiring, the sandboxing, and the extension model around it, is the **harness**, and it is what actually differs between these five; the chat-in-a-terminal experience on top has converged. The closed first-party products (Claude Code, Cursor's agent) aren't list entries, but they define the workflow all five implement.

Why the pick matters: these tools edit your files and run commands on your machine, so you are choosing a default safety posture and a provider relationship, not just an interface.

| | [opencode](https://github.com/anomalyco/opencode) | [Gemini CLI](https://github.com/google-gemini/gemini-cli) | [Codex](https://github.com/openai/codex) | [goose](https://github.com/aaif-goose/goose) | [crush](https://github.com/charmbracelet/crush) |
|---|---|---|---|---|---|
| ⭐ Stars | 195k | 106k | 105k | 52.6k | 27.2k |
| Steward | Anomaly (company, formerly SST) | Google (first-party) | OpenAI (first-party) | Linux Foundation AAIF (Agentic AI Foundation) | Charm |
| License | MIT | Apache-2.0 | Apache-2.0 | Apache-2.0 | ⚠️ FSL-1.1-MIT (Functional Source License; each release converts to MIT after two years) |
| Core language | TypeScript | TypeScript | Rust | Rust | Go |
| Model lock-in | None: 75+ providers, including local models | Gemini-first | OpenAI-first, other providers configurable | None: provider choice by design | None: multi-provider |
| Autonomy (list axis) | headless | bounded | bounded | headless | bounded |
| Recovery (list axis) | resumable | resumable | resumable | resumable | resumable |
| Distinctive harness bet | Client/server split: the agent runs as a server your terminal, IDE, or another machine connects to | First-party Gemini integration and a generous free tier | Sandboxed execution as the default posture | Extensions and recipes over a fixed experience; desktop app and CLI both first-party | Session persistence and terminal-interface polish |

_Stars as captured for the main list. The list-axis rows: autonomy is how unattended the tool is designed to run (step-gated → headless; "headless" means built for unsupervised runs, not that it lacks an interface), recovery is what survives a dead session (none → durable). Definitions: [guide to rankings](../README.md#guide-to-rankings)._

## Pick by situation

- **You want maximum freedom and the biggest community** → **opencode**. No model lock-in ([75+ providers](https://opencode.ai/docs/providers/), local models included), the largest star and contributor count in the category, and a [client/server design](https://opencode.ai/docs/server/) that lets the agent run somewhere other than the terminal displaying it: your laptop's terminal today, a remote box or IDE tomorrow. The default pick in this list's [use-case index](../README.md#pick-by-use-case).
- **You live on Gemini, or want the free tier** → **Gemini CLI**. Google's [personal-account tier](https://github.com/google-gemini/gemini-cli#readme) (60 requests/minute, 1,000/day) is the most generous first-party allowance in the category; the reason to choose it is Gemini integration and Google's pace of investment, not harness novelty.
- **You care most about safe autonomous execution** → **Codex**. Its defining bet is running the agent's actions inside a sandbox by default ([sandboxing docs](https://developers.openai.com/codex/concepts/sandboxing)): the strongest default isolation of the five. Best experience on OpenAI models and plans.
- **You're embedding an agent into your own tooling** → **goose**. Foundation-governed, built around extensions using MCP and ACP (the Model Context Protocol and Agent Client Protocol, the standard plugs for tools and for editor-agent connections) plus reusable task recipes. It ships both a desktop app and a CLI; the reason to pick it is the extension architecture, not the absence of one.
- **You want the nicest terminal experience, and the license is acceptable** → **crush**. Charm builds the terminal-UI tooling much of the ecosystem uses, and it shows, plus persistent per-project sessions. The FSL license is the one structural caveat: fine for individual use, check it before redistributing.

Three more names people shortlist, all on the main list: [aider](https://github.com/Aider-AI/aider) (48k stars, the original git-native terminal pair programmer, though its repo has been quiet since May 2026), [pi](https://github.com/earendil-works/pi) (the minimal multi-provider agent toolkit this list's oh-my-pi entry builds on), and [Qwen Code](https://github.com/QwenLM/qwen-code) (a Gemini CLI fork tuned for open-weight Qwen models).

## What they share

All five: the tool loop described above over file, shell, and search tools; MCP support for adding more tools; permission prompts before destructive actions; and a briefing file for custom instructions. Switching costs are low by design. All five read AGENTS.md, the shared instructions-file format (Gemini CLI defaults to its own GEMINI.md and needs one setting flipped; goose reads it in its developer extension), so trying two is cheap.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). New to this decision? Start with [How to pick a harness](how-to-pick-a-harness.md). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._
