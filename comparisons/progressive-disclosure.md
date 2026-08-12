# Context files for agents: AGENTS.md vs CLAUDE.md vs skills vs MCP tool search

A model has a context window: a fixed amount of text it can consider at once. Everything competes for that space: your instructions, the definitions of every tool the agent could call, and the output of every tool it already called. Context bloat is what happens when the "might need it" pile crowds out the actual task, and it makes every request slower, dumber, and more expensive. The fix has one name across all its forms: progressive disclosure. Give the model a map first, and load details only when they're needed.

Bloat enters through three doors: instructions, tool definitions, and tool output. The four things in the table guard the first two doors, and they're the ones people actually weigh against each other: the [AGENTS.md vs CLAUDE.md question](https://news.ycombinator.com/item?id=44957443) has produced some of the biggest agent-tooling threads on Hacker News (837 points; a [files-vs-skills follow-up](https://news.ycombinator.com/item?id=46809708) drew 524 more).

| | [AGENTS.md](https://agents.md) | CLAUDE.md | [Skills](https://github.com/anthropics/skills) | [MCP tool search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool) |
|---|---|---|---|---|
| What it is | An open, cross-tool briefing file at the repo root; 60k+ repos use it, and stewardship moved to the Linux Foundation in December 2025 | Claude Code's native briefing file: same job, one tool | Folders of instructions and scripts (SKILL.md) the agent loads only when the task matches | A built-in Claude Code feature: with many MCP servers connected, tool definitions load on demand instead of upfront |
| Door it guards | Instructions | Instructions | Instructions (on demand) | Tool definitions |
| Loaded | Every session | Every session | When triggered | When the agent searches for a tool |
| Read by | 20+ tools (Codex, Cursor, Copilot, Zed, more) | Claude Code | Claude Code, Claude.ai, the API, plus compatible harnesses | Claude Code (shipped January 2026, on by default; Anthropic claims ~85% fewer tool-definition tokens) |
| Scales by | Nesting: a file per directory scopes instructions to that part of the repo | Hierarchy: global, project, and local files stack | Adding skills costs almost nothing until triggered | Automatically |

_MCP is the Model Context Protocol, the standard way tools plug into agents. The [guide to rankings](../README.md#guide-to-rankings) defines this site's rating vocabulary._

## Which layer owns which instruction

This is the question people actually ask ("I have CLAUDE.md, AGENTS.md, skills, subagents, and MCP servers, and I don't know where anything belongs"), and it has a short answer:

- **The agent must always know it** (build commands, conventions, hard rules) → **AGENTS.md**, and keep it a map, not an encyclopedia. The community's hard-won rule: [a good one reads like a model upgrade, a bad one is worse than no docs](https://news.ycombinator.com/item?id=47938417).
- **Only Claude Code needs it** (your personal workflow rules) → **CLAUDE.md**. In mixed-tool teams the common pattern is AGENTS.md as the single source with CLAUDE.md pointing at it; Claude Code reading AGENTS.md natively is a [long-running feature request](https://github.com/anthropics/claude-code/issues/6235).
- **It's a procedure, only sometimes needed** (how to cut a release, how to write a PDF) → **a skill**. This is progressive disclosure in its purest form, and whole [packs of them exist](claude-code-skill-packs.md). The one caution from the field: skills only help when they trigger, which is exactly what the 524-point files-vs-skills thread found teams struggling with.
- **It's a tool** → an MCP server, and let **tool search** load the definitions. Before that feature, connecting many servers could eat a meaningful slice of the window before the first instruction; that pain built a whole cottage industry (below). For heavy tool users Anthropic also documents a stronger pattern: [give the agent a code environment that calls tools programmatically](https://www.anthropic.com/engineering/code-execution-with-mcp) instead of loading schemas at all.
- **Tool output floods the window** (huge JSON, logs, scraped pages) → summarize, offload to files, or use an output-side layer (below). This third door has no standard answer yet.

## The shelf: research and third-party layers

Worth knowing, mostly not worth building on today. [MCP-Zero](https://arxiv.org/abs/2506.01056) is the research result for tool-schema routing (~98% token reduction on the APIBank benchmark), but its [code](https://github.com/xfey/MCP-Zero) has been frozen since July 2025: cite the paper, don't build on the repo. [ToolGen](https://arxiv.org/abs/2410.03439) (ICLR 2025, a major machine-learning conference) showed retrieval and invocation can be one generative step; also frozen. [langgraph-bigtool](https://github.com/langchain-ai/langgraph-bigtool) is the maintained version of retrieve-then-load for LangGraph (LangChain's agent framework); [spring-ai-tool-search-tool](https://github.com/spring-ai-community/spring-ai-tool-search-tool) did the same for Java's Spring and has since been folded into Spring AI's core. On the output door, [context-mode](https://github.com/mksglu/context-mode) (19.7k stars) intercepts tool results and hands the model a summary, and [Headroom](https://github.com/headroomlabs-ai/headroom) compresses tool output as a library, proxy, or MCP server. Two cautions on context-mode: it's source-available under the Elastic License 2.0 rather than open source, and its npm installs have fallen by roughly a third from their May 2026 peak (per npm registry data) since the native tool-search feature shipped. The pattern to internalize: platform defaults keep absorbing this category, so prefer the built-in fix and treat third-party layers as bridges. For public websites, [llms.txt](https://llmstxt.org) is the same map-first idea applied to a site instead of a repo.

## Pick by situation

- **One repo, several tools touching it** → **AGENTS.md**, nested per directory in big repos. Free, no software, every major harness reads it.
- **Claude Code is your only harness** → **CLAUDE.md** is equivalent and native; adopt AGENTS.md the day a second tool shows up.
- **Procedures are bloating your briefing file** → move them to **skills**; the briefing file keeps the map.
- **Dozens of MCP servers** → the built-in **tool search** already fixed most of it; the code-execution pattern is the heavyweight option beyond that.
- **Output is the leak** → compaction plus file offloading first, then context-mode or Headroom if you need a dedicated layer.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). New to this decision? Start with [How to pick a harness](how-to-pick-a-harness.md). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._
