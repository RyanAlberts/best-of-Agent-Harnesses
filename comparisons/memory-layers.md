# Agent memory layers: Mem0 vs Zep vs Letta vs claude-mem

Agents forget. A model keeps nothing between sessions, so anything your agent should still know tomorrow (who the user is, what was decided, what failed last time) has to live in a memory system outside the model. "Add memory to my agent" then hides genuinely different products, and picking by star count instead of by shape is how teams end up adopting a whole runtime when they needed a plugin. The three shapes: a **memory layer** you call from any agent (Mem0, Zep), an **agent runtime** where memory is the core abstraction and your agents live inside it (Letta), and a **harness plugin** that gives the coding agent you already run automatic recall (claude-mem).

| | [Mem0](https://github.com/mem0ai/mem0) | [Graphiti / Zep](https://github.com/getzep/graphiti) | [Letta](https://github.com/letta-ai/letta) | [claude-mem](https://github.com/thedotmack/claude-mem) |
|---|---|---|---|---|
| ⭐ Stars | 64.8k | 30.6k | 24.6k | 93.3k |
| Shape | Memory layer / API | Memory layer / engine | Agent runtime with built-in memory | Harness plugin |
| Works with | Any agent or framework | Any agent or framework | Agents you build *inside* Letta | Claude Code, Codex, OpenClaw, Gemini, Copilot, and more |
| Memory model | Extracted facts, scoped per user, agent, or session, retrieved on demand | A temporal knowledge graph: facts about people and things, plus *when* they were true, so answers can change as facts change | Self-editing memory (the MemGPT research lineage): the agent maintains its own memory as part of how it thinks | Captures what a session did, compresses it with AI, and injects the relevant parts when you resume |
| License | Apache-2.0 | Apache-2.0 | Apache-2.0 | Apache-2.0 |
| Adoption surface (list tier) | slightly complex | slightly complex | mostly simple | slightly complex |

_Stars as captured for the main list; the [guide to rankings](../README.md#guide-to-rankings) defines the rating vocabulary. Mem0, Graphiti, and claude-mem run no agent loop of their own (your agent stays in charge); Letta is rated headless autonomy with durable recovery on the list's axes, because your agents run as persistent entities on its server._

## Pick by situation

- **You have an agent and want it to remember users** → **Mem0**. The default drop-in: store and retrieve scoped memories from any framework via an API or library, with hosted and self-managed backends. If you're asking the generic question, this is the generic answer.
- **Your memory questions involve time and relationships** ("what did this customer believe before the refund?") → **Graphiti**, the open-source engine behind Zep's hosted platform. Plain fact-stores overwrite; a temporal knowledge graph keeps the history, which is the difference when facts change and the change matters.
- **You're designing an agent *around* memory** → **Letta**. The MemGPT lineage: agents that manage their own memory as a first-class behavior rather than calling out to a store. You're adopting a runtime, not adding a layer; that's the right trade for long-lived, persistent-persona agents and over-engineering for "remember the user's name."
- **Your "agent" is a coding assistant you already run** → **claude-mem**. Don't build memory infrastructure for a harness that takes a plugin: it captures everything a session does and hands the relevant context to future sessions. It started Claude Code-only and now covers Codex, OpenClaw, Gemini, and Copilot too. Its star count, highest on this page, says how common this situation is.

Also in the same space on the main list: [cognee](https://github.com/topoteretes/cognee), which turns your data into a queryable knowledge graph plus vector store through an extract-and-load pipeline; it competes with Mem0 and Graphiti at the layer shape and shows up in most four-way memory comparisons.

## The question to ask first

*Who decides what gets remembered?* If your application code decides (you choose what to store and when to look it up), you want a memory layer: Mem0, Graphiti, or cognee. If the agent itself should decide as part of how it operates, you want a runtime: Letta. If you'd rather nobody has to decide because the tool records and recalls automatically, you want a harness plugin: claude-mem. Answer that one question and the shortlist usually collapses to one shape.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). New to this decision? Start with [How to pick a harness](how-to-pick-a-harness.md). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._

_Agents can query this page's data directly: `claude mcp add agent-harnesses -- uvx agent-harnesses-mcp` ([MCP server](../mcp/))._
