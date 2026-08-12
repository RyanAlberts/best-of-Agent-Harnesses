# Multi-agent orchestration: OpenAI Agents SDK vs CrewAI vs AutoGen vs Agent Framework vs LangGraph

Orchestration is the layer that coordinates several AI agents working on one job: who acts next, what they share, and what happens when a step fails. The five frameworks here answer that with genuinely different architectures, and the pick is expensive to get wrong because the coordination model shapes your whole codebase, not just one file. One of the five also changed status in a way most comparison articles haven't caught up with: AutoGen, still the most-starred name in the category, is officially in maintenance mode.

| | [openai-agents-python](https://github.com/openai/openai-agents-python) | [CrewAI](https://github.com/crewAIInc/crewAI) | [AutoGen](https://github.com/microsoft/autogen) | [Agent Framework](https://github.com/microsoft/agent-framework) | [LangGraph](https://github.com/langchain-ai/langgraph) |
|---|---|---|---|---|---|
| ⭐ Stars | 28.5k | 56.9k | 60.3k | 12.7k | 39.3k |
| Coordination model | **Handoffs**: one agent passes the whole conversation to another, like a call-center transfer | **Roles**: agents defined by role, goal, and backstory collaborate in Crews; Flows (its event-driven control layer) steer production paths | **Conversation**: agents talk in a group chat until a stop condition ends it | **Workflows**: graph-based workflows merging the AutoGen and Semantic Kernel lines, in Python and .NET | **Graph**: you draw an explicit map of states and steps; agents are nodes on it |
| Status (checked 2026-08-12) | Active | Active | ⚠️ Maintenance mode: its own README says no new features and points new users at Agent Framework | Active: the designated successor, 1.0 GA in April 2026 | Active |
| How visible is the control flow | Medium: it emerges from the handoff rules you wrote | Low to medium: declarative, the framework decides | Low: it emerges from the dialogue | High: workflows are explicit | Highest: you drew the map yourself |
| Production features | Guardrails (checks that block bad inputs/outputs) and tracing (a step-by-step run log); you own the loop | Flows, hierarchical control | Code execution, human approval points | Graph workflows, checkpointing, .NET + Python | Checkpointing (saving run state so it can restart), durable execution, human approval points |
| Autonomy (list axis) | bounded | bounded | bounded | bounded | headless |
| Recovery (list axis) | resumable | resumable | resumable | resumable | durable |
| Adoption surface (list tier) | mostly simple | complex (product suite) | complex (product suite) | slightly complex | slightly complex |

_Stars as captured for the main list. The list-axis rows use this site's rating ladders: autonomy runs step-gated → headless (how unattended a tool is designed to run), recovery runs none → durable (what survives a crash); definitions in the [guide to rankings](../README.md#guide-to-rankings)._

## Pick by situation

- **You want the least framework between you and the model** → **OpenAI Agents SDK**. Handoffs plus guardrails and almost nothing else; the smallest adoption surface of the five, and multi-provider in practice ([LiteLLM and per-agent model adapters](https://openai.github.io/openai-agents-python/models/) mean it is not OpenAI-only). Start here if unsure: it is the cheapest to abandon if you outgrow it.
- **You think in team structures** → **CrewAI**. Role-based crews are the fastest path to a working multi-agent demo and the most readable to non-engineers. The trade: it is a product suite, so you adopt its worldview, and stepping outside the declarative style means fighting the framework. Flows exist to win back control in production.
- **Your problem is genuinely conversational** → **AutoGen**, with eyes open. Group chat fits problems where agents *should* debate (review panels, negotiation simulations, brainstorming) and fights you when you wanted a pipeline. The status row is the real caveat: [Microsoft's own README](https://github.com/microsoft/autogen) declares maintenance mode, so treat it as stable-but-frozen. The community continuation is [AG2](https://github.com/ag2ai/ag2), which carries the original conversation-based line forward.
- **You're on Microsoft's stack, or leaving AutoGen** → **Agent Framework**. The convergence of AutoGen and Semantic Kernel, generally available since April 2026, with graph workflows and checkpointing in Python and .NET. It is where Microsoft's investment actually goes now.
- **It's going to production and must survive restarts** → **LangGraph**. Explicit graphs, checkpointing, and durable execution make it the infrastructure-grade choice; the same explicitness makes it the most up-front design work of the five. If your "multi-agent system" is really a workflow with LLM steps, LangGraph is the framework that says so out loud.

Worth knowing beyond the table: [Google ADK](https://github.com/google/adk-python) (Google's engineering-first framework, with agent-to-agent interop), [Agno](https://github.com/agno-agi/agno) (performance and multi-modal focus), and [Mastra](https://github.com/mastra-ai/mastra) (the TypeScript-native answer in a Python-first field) all show up in buyer comparisons now, and all three are on the main list.

## The unfashionable default

Most "multi-agent" systems in the wild are one coordinator delegating to workers that don't talk to each other and keep no state of their own. All five frameworks can express that, and so can a plain loop over your provider's SDK. Reach for an orchestration framework when agents need to *interact*: share evolving state, contest each other's outputs, or hand a live task around. If they just need to run in parallel and report back, you may not have a framework problem at all.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). New to this decision? Start with [How to pick a harness](how-to-pick-a-harness.md). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._
