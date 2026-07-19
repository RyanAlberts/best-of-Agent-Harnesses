# Agent memory layers: Mem0 vs Letta vs claude-mem

"Add memory to my agent" hides three different products: a **memory API** you call from any agent (Mem0), an **agent runtime** where memory is the core abstraction (Letta), and a **plugin** that gives one specific harness perfect recall (claude-mem). They're barely competitors — the comparison that matters is which *shape* fits your stack.

| | [Mem0](https://github.com/mem0ai/mem0) | [claude-mem](https://github.com/thedotmack/claude-mem) | [Letta](https://github.com/letta-ai/letta) |
|---|---|---|---|
| ⭐ Stars | 61.2k | 87.8k | 23.9k |
| Shape | Memory layer / API | Claude Code plugin | Agent runtime with built-in memory |
| Works with | Any agent or framework | Claude Code only | Agents you build *in* Letta |
| Memory model | Extracted facts (user/org/session scoped), retrieved on demand | Session capture → AI compression → context injection on resume | Self-editing agent memory (the MemGPT lineage) |
| Adoption surface (list tier) | slightly complex | slightly complex | mostly simple |
| Autonomy (list axis) | n/a — memory layer, no loop | n/a — plugin, host owns the loop | headless |
| Recovery (list axis) | n/a | n/a | durable |
| License | open source (Apache-2.0) | open source | open source |

_Stars as captured for the main list (see [README](../README.md#guide-to-rankings) for the capture date)._

## Pick by situation

- **You have an agent and want it to remember users** → **Mem0**. The de-facto drop-in: store and retrieve scoped memories from any framework via API/library, with hosted or self-managed backends. If you're asking the generic question, this is the generic answer — which is why it leads the use-case index in the main list.
- **Your "agent" is Claude Code** → **claude-mem**. Don't build memory infrastructure for a harness that takes a plugin: it captures everything a session does, compresses it, and injects the relevant context into future sessions. Zero architecture decisions. Its star count — highest of the three — says how common this situation is.
- **You're designing an agent *around* memory** → **Letta**. The MemGPT lineage: agents that manage their own memory hierarchy as a first-class behavior, not a bolt-on retrieval call. You're adopting a runtime, not adding a layer — the right trade for long-horizon, persistent-persona agents, and over-engineering for "remember the user's name."

## The question to ask first

*Who owns the memory — the application or the agent?* Application-owned (you decide what to store and when to recall) → Mem0. Agent-owned (the agent decides, as part of its loop) → Letta. Harness-owned (the harness remembers for you) → claude-mem. Answer that and the pick usually falls out.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._
