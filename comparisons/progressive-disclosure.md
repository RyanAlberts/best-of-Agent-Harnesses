# Progressive disclosure: agents.md vs MCP-Zero vs langgraph-bigtool vs context-mode

Context bloat enters through three doors: instructions the agent might need, tool schemas it might call, and tool output it already produced. Progressive disclosure is one principle (give the model a map first, details only on demand) applied at each door. These four projects guard different doors, so the pick is less "which is best" and more "which door is leaking."

| | [agents.md](https://github.com/agentsmd/agents.md) | [MCP-Zero](https://github.com/xfey/MCP-Zero) | [langgraph-bigtool](https://github.com/langchain-ai/langgraph-bigtool) | [context-mode](https://github.com/mksglu/context-mode) |
|---|---|---|---|---|
| ⭐ Stars | 23.5k | 502 | 552 | 19.7k |
| Door it guards | Instructions | Tool schemas (protocol level) | Tool schemas (framework level) | Tool output |
| How | Open format for repo-scoped briefings; v1.1 hands agents a map of what exists, then loads only what's relevant | The model requests tools by requirement; hierarchical semantic routing over 308 servers / 2,797 tools, ~98% token reduction on APIBank | LangGraph agents retrieve and load tools on demand from large registries instead of stuffing every schema upfront | Sandboxes tool output before it reaches the model (claimed 98% reduction); persists session memory across 17 agent platforms via MCP and hooks |
| Shape | Format only, nothing to run | Research code with a paper | Library in the LangGraph ecosystem | Drop-in MCP/hooks layer |
| Maintenance (checked 2026-08-12) | Stable spec; last change March 2026 | Frozen since July 2025 | Active | Active |
| License | MIT | MIT | MIT | ⚠️ custom license |
| Autonomy (list axis) | n/a: format | bounded | bounded | n/a: layer |
| Recovery (list axis) | n/a | none | durable | n/a |
| Adoption surface (list tier) | super simple | complex | slightly complex | mostly simple |

_Stars as captured for the main list (see [README](../README.md#guide-to-rankings) for the capture date)._

## Pick by situation

- **Instructions are the leak** (a repo briefing that reads like an encyclopedia) → **agents.md** v1.1. Hierarchical scope means the agent reads a map, then opens only the briefing it needs. It is a format, not software: nothing to run, and the major harnesses already read it.
- **Tool schemas are the leak** (hundreds of MCP tools taxing every request) → depends on your stack. On LangGraph, **langgraph-bigtool** is the maintained implementation of retrieve-then-load. **MCP-Zero** is still worth an afternoon of reading for its routing design and the measured ~98% reduction, but the code has been frozen since July 2025: cite the paper, don't build on the repo. Spring shops have [spring-ai-tool-search-tool](https://github.com/spring-ai-community/spring-ai-tool-search-tool) (34-64% measured reduction across providers), [ToolRAG](https://github.com/antl3x/ToolRAG) covers MCP-compatible semantic retrieval, and [ToolGen](https://github.com/Reason-Wang/ToolGen) (ICLR 2025) is the research result showing retrieval and invocation can be one generative step, also frozen.
- **Tool output is the leak** (JSON blobs, logs, and scraped pages flooding the window) → **context-mode**, which sandboxes results before the model sees them, or [Headroom](https://github.com/headroomlabs-ai/headroom), which compresses tool output with content-aware compressors and drops in as a library, HTTP proxy, or MCP server. Check context-mode's custom license before commercial use.

## Read the star column as a maturity signal

The adoption gap in the table is the finding: the format and the drop-in output layer carry five-figure star counts, while tool-schema routing is still research-grade code in the hundreds. That matches how the pain distributes. Every agent's instructions and outputs bloat; thousand-tool registries stay rare. So measure before adopting: count the tokens each door actually costs you in one session, then fix the biggest leak first. Skill packs are this same principle applied to instructions at the harness level ([Claude Code skill packs](claude-code-skill-packs.md)), and the list's whole [progressive-disclosure category](../README.md#progressive-disclosure-harnesses) maps the rest of the field.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). New to this decision? Start with [How to pick a harness](how-to-pick-a-harness.md). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._
