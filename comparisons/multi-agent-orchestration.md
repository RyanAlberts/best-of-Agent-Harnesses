# Multi-agent orchestration: OpenAI Agents SDK vs CrewAI vs AutoGen vs LangGraph

Four very different answers to "how should multiple agents coordinate?" — and the differences are architectural, not cosmetic. Picking wrong here is expensive: the coordination model shapes your whole codebase.

| | [openai-agents-python](https://github.com/openai/openai-agents-python) | [CrewAI](https://github.com/crewAIInc/crewAI) | [AutoGen](https://github.com/microsoft/autogen) | [LangGraph](https://github.com/langchain-ai/langgraph) |
|---|---|---|---|---|
| ⭐ Stars | 27.1k | 53.3k | 58.9k | 34.5k |
| Coordination model | **Handoffs** — agents transfer control like a call-center escalation | **Roles** — agents with goals/backstories collaborate in Crews; Flows for control | **Conversation** — agents talk in group chats until done | **Graph** — explicit state machine; agents are nodes |
| Adoption surface (list tier) | mostly simple | complex (product suite) | complex (product suite) | slightly complex |
| Control flow visibility | Medium — emergent from handoff rules | Low-medium — declarative, framework decides | Low — emergent from dialogue | High — you drew the graph |
| Production posture | Guardrails, tracing; you own the loop | Flows, hierarchical control | Code execution, human-in-the-loop | Checkpointing, durable execution, human-in-the-loop |

_Stars as captured for the main list (see [README](../README.md#explanation) for the capture date)._

## Pick by situation

- **You want the least framework between you and the model** → **OpenAI Agents SDK**. Handoffs + guardrails and almost nothing else; the list rates it the smallest adoption surface of the four. Multi-LLM routing means it's not OpenAI-only in practice. Start here if you're unsure — it's the cheapest to walk away from.
- **You think in org charts** → **CrewAI**. Role-based crews are the fastest path to a working multi-agent demo and the most readable to non-engineers. The trade: it's a product suite — you adopt its worldview, and stepping outside the declarative model means fighting it. Flows mitigate this for production control flow.
- **Your problem is genuinely conversational** → **AutoGen**. Group chat is a great fit when agents *should* debate (review panels, negotiation sims, brainstorming) and an awkward fit when you wanted a pipeline. One watch item: Microsoft has been converging its agent efforts into the Microsoft Agent Framework — check the roadmap before betting a new production system on AutoGen specifically.
- **It's going to production and must survive restarts** → **LangGraph**. Explicit graphs, checkpointing, and durable execution make it the infrastructure-grade choice; the same explicitness makes it the most up-front design work of the four. If your "multi-agent system" is honestly a workflow with LLM steps, this is the right honesty.

## The unfashionable default

A majority of "multi-agent" use cases in the wild are one orchestrator delegating to stateless sub-tasks. All four frameworks can express that — and so can a `for` loop over your provider's SDK. Reach for orchestration frameworks when agents need to *interact*, not just fan out.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._
