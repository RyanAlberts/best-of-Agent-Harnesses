<!-- markdownlint-disable -->
<h1 align="center">
    Best of Agent Harnesses and Harness Techniques
    <br>
</h1>

<p align="center">
    <strong>🏆&nbsp; Curated list of AI agent harnesses, orchestration frameworks, and harness techniques for reliable agentic systems.</strong>
</p>

<p align="center">
    <a href="https://best-of.org" title="Best-of Badge"><img src="http://bit.ly/3o3EHNN"></a>
    <a href="#contents" title="Project Count"><img src="https://img.shields.io/badge/projects-82+-blue.svg?color=5ac4bf"></a>
    <a href="#contribution" title="Contributions welcome"><img src="https://img.shields.io/badge/contributions-welcome-green.svg"></a>
    <a href="https://github.com/RyanAlberts/best-of-Agent-Harnesses/releases" title="Updates"><img src="https://img.shields.io/github/release-date/RyanAlberts/best-of-Agent-Harnesses?color=green&label=updated"></a>
</p>

This list focuses on **agent harnesses**: the environments, scaffolding, and tooling that make AI agents reliable at long-running or complex tasks. It is for builders, platform engineers, and researchers who care about orchestration, context management, and guardrails—not just model choice.

## What is an agent harness?

An **agent harness** is everything around the model that makes agentic systems work in practice: environment design, intent specification, feedback loops, and the repository (or knowledge base) as the system of record. Engineers design scaffolding and guardrails so agents can do reliable work; the model generates, the harness controls what’s allowed, when to ask humans, and how to recover from failure.

- **OpenAI (harness engineering):** Harness = environment design, intent specification, feedback loops, and repository-as-system-of-record so agents (e.g. Codex) can execute reliably. Humans steer; agents execute.
- **Anthropic (long-running agents):** Session bridging (initializer + coding agent), feature lists, progress files, incremental work, clean state, and explicit testing (e.g. browser automation) so agents don’t one-shot or declare “done” too early.
- **Practitioners (e.g. Aakash Gupta):** Harness = human-in-the-loop, filesystem access, tool orchestration, sub-agent coordination, prompt presets, lifecycle hooks. “Model is commodity, harness is moat”—minimal intervention, progressive disclosure, fail-fast with recovery.

## Why harnesses matter

Better models make harnesses more important: more capabilities mean more failure modes, and production needs retry logic, fallbacks, and validation. Harness quality—not just model quality—determines whether agents actually ship. This list ranks projects by relevance to harness concerns (environment, orchestration, lifecycle, guardrails) and by stars/activity.

## Contents

- [Full-stack and long-running coding harnesses](#full-stack-and-long-running-coding-harnesses) _10 projects_
- [Frameworks](#frameworks) _26 projects_
- [Multi-agent and orchestration](#multi-agent-and-orchestration) _5 projects_
- [Plugins, MCPs, CLI tools](#plugins-mcps-cli-tools) _10 projects_
- [Evaluation and benchmarking harnesses](#evaluation-and-benchmarking-harnesses) _15 projects_
- [Research and task-specific harnesses](#research-and-task-specific-harnesses) _3 projects_
- [Libraries and SDKs](#libraries-and-sdks) _13 projects_

## Explanation

- 🥇🥈🥉&nbsp; Combined project-quality score
- ⭐️&nbsp; Star count from GitHub
- 🐣&nbsp; New project _(less than 6 months old)_
- 💤&nbsp; Inactive project _(6 months no activity)_
- 💀&nbsp; Dead project _(12 months no activity)_
- 📈📉&nbsp; Project is trending up or down
- 👨‍💻&nbsp; Contributors count from GitHub
- 🔀&nbsp; Fork count from GitHub
- 📋&nbsp; Issue count from GitHub
- ⏱️&nbsp; Last update timestamp on package manager

<br>

## Full-stack and long-running coding harnesses

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Spec-driven, multi-session, repo-scoped coding harnesses._

| # | Project | Description |
|---|---------|-------------|
| 1 | [**get-shit-done**](https://github.com/gsd-build/get-shit-done) | Goal-backward planning and wave-based execution over fresh context windows; avoids context rot by design. Python/JS meta-prompting for Claude Code, OpenCode, Gemini CLI. |
| 2 | [**Claude Agent SDK**](https://github.com/anthropics/claude-agent-sdk-python) | Official SDK (Python + [TypeScript](https://github.com/anthropics/claude-agent-sdk-typescript), [demos](https://github.com/anthropics/claude-agent-sdk-demos), [quickstarts](https://github.com/anthropics/claude-quickstarts)): built-in tools, MCP, long-running coding agents with session bridging. |
| 3 | [**RepoMaster**](https://github.com/QuantaAlpha/RepoMaster) | Repo-scoped agent that builds function-call and module-dependency graphs to explore only what’s needed; large relative gains on MLE-bench and GitTaskBench with lower token use. |
| 4 | [**coderClaw**](https://github.com/SeanHogg/coderClaw) | Self-hosted multi-role coding system (Creator, Reviewer, Test, Refactor, etc.) with AST and semantic maps; IDE-agnostic, chat-channel triggers. |
| 5 | [**opencode**](https://github.com/opencode-ai/opencode) | Terminal-first AI coding agent; multi-session, 75+ providers; archived in favor of Crush. |
| 6 | [**crush**](https://github.com/charmbracelet/crush) | Charm’s terminal-based coding agent; successor to OpenCode, Bubble Tea TUI. |
| 7 | [**Cline**](https://github.com/cline/cline) | VS Code extension that acts like a junior dev: plan-then-act, human approval per step, cost transparency; the open-source Cursor counterweight. |
| 8 | [**Codive**](https://github.com/toliaqat/codive) | Rust binary: CLI + TUI + web client, any LLM, voice input; single-binary speed and MCP so you’re not tied to one IDE. |
| 9 | [**Codex**](https://github.com/openai/codex) | OpenAI’s own terminal coding agent; local run, sandboxed execution, multi-provider; the reference implementation for “CLI that writes code.” |
| 10 | [**Hydra**](https://github.com/PrimeLocus/Hydra) | Multi-agent dispatcher: routes tasks across Claude, Gemini, Codex with queues and parallel runs; for teams that want one entry point. |

## Frameworks

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_General-purpose agent and LLM application frameworks (the app layer, not harnesses per se)._

| # | Project | Description |
|---|---------|-------------|
| 1 | [**langgraph**](https://github.com/langchain-ai/langgraph) | State-machine graphs over LLM steps; checkpointing, human-in-the-loop, and durable execution so workflows survive restarts. |
| 2 | [**langchain**](https://github.com/langchain-ai/langchain) | Chains, tools, retrievers, and agents; the usual entry point for “add tools to an LLM” in Python/JS. |
| 3 | [**llama-index**](https://github.com/run-llama/llama_index) | Data-centric: indexing, RAG, and query engines; agent abstractions sit on top of your data pipelines. |
| 4 | [**semantic-kernel**](https://github.com/microsoft/semantic-kernel) | Microsoft’s plugin and planner layer for LLMs; C#, Python, Java; strong on enterprise auth and orchestration. |
| 5 | [**mastra**](https://github.com/mastra-ai/mastra) | TypeScript-first; agents, tools, and workflows with a single runtime and minimal boilerplate. |
| 6 | [**phidata**](https://github.com/phidata-ai/phidata) | Python agents with persistent memory, knowledge bases, and tools; targets production apps with minimal glue. |
| 7 | [**agno**](https://github.com/agno-ai/agno) | Python framework focused on observability and structured outputs; good fit for eval and pipeline use cases. |
| 8 | [**letta**](https://github.com/letta/letta) | Python agent runtime with tool use and control flow; lean API. |
| 9 | [**langflow**](https://github.com/langchain-ai/langflow) | Low-code UI to build and deploy LangChain/LangGraph flows; visual DAG editor and one-click run. |
| 10 | [**rasa**](https://github.com/rasa/rasa) | Conversational AI stack (NLU, dialogue, actions); long-standing OSS choice for chat and voice bots. |
| 11 | [**botpress**](https://github.com/botpress/botpress) | Visual bot builder and runtime; multi-channel, open-source alternative to commercial bot platforms. |
| 12 | [**Dify**](https://github.com/langgenius/dify) | One-stop LLM app platform: visual workflows, RAG pipeline, 50+ tools, model management; “ship from prototype to prod” in a single UI. |
| 13 | [**n8n**](https://github.com/n8n-io/n8n) | Fair-code workflow engine with 400+ nodes and native AI nodes; the self-hosted Zapier that actually does agents and LangChain. |
| 14 | [**Auto-GPT**](https://github.com/Significant-Gravitas/Auto-GPT) | The original autonomous loop: goal in, agent iterates with tools and memory; Forge is the dev framework, Benchmark the eval harness. |
| 15 | [**Auto-GPT-Forge**](https://github.com/Significant-Gravitas/Auto-GPT-Forge) | Template and harness for building your own Auto-GPT-style agent; Agent Protocol–aligned, so you focus on logic not boilerplate. |
| 16 | [**AIlice**](https://github.com/myshell-ai/AIlice) | Fully autonomous general-purpose agent; one binary, Docker-ready, for when you want “set goal and walk away” without a framework. |
| 17 | [**Bee Agent Framework**](https://github.com/i-am-bee/bee-agent-framework) | Python + TypeScript, LF AI–backed; MCP/ACP, workflows, Requirement Agent; the one that pushes “production multi-agent” without LangChain. |
| 18 | [**agent-squad**](https://github.com/awslabs/agent-squad) | AWS-flavored orchestrator: intent classification, streaming, SupervisorAgent; “agent-as-tools” so one agent delegates to a squad. |
| 19 | [**SuperAgentX**](https://github.com/superagentxai/superagentx) | Lightweight multi-agent orchestrator with an AGI-angle; minimal surface, docs-first, for teams that want orchestration without the kitchen sink. |
| 20 | [**AgentVerse**](https://github.com/openbmb/agentverse) | Task-solving and simulation envs for multi-LLM agents; deploy many agents in custom environments without building infra from scratch. |
| 21 | [**R2R**](https://github.com/SciPhi-AI/R2R) | RAG-first: hybrid search, knowledge graphs, multimodal; the framework for “production RAG” when you care more about retrieval than chat UI. |
| 22 | [**LiteSwarm**](https://github.com/GlyphyAI/liteswarm) | Async-only, LiteLLM-backed Python; dynamic agent switching and type-safe context—for devs who want 100+ models without LangGraph’s weight. |
| 23 | [**AgentStack**](https://github.com/AgentOps-AI/AgentStack) | Scaffolds full agent projects; plugs in CrewAI, LangGraph, OpenAI Swarm, LlamaStack and wires AgentOps observability from day one. |
| 24 | [**AgentSilex**](https://github.com/howl-anderson/agentsilex) | ~300 lines of readable agent code on top of LiteLLM; the “I want to see the whole loop” option for learning or minimal production. |
| 25 | [**Flowise**](https://github.com/FlowiseAI/Flowise) | Drag-and-drop LangChain UI; deploy flows without code. The low-code sibling to Langflow, with a different component and hosting story. |
| 26 | [**GraphFusionAI**](https://github.com/GraphFusion/graphfusionai) | Modular agent components and examples; small surface for when you want to compose your own graph without a big framework. |

## Multi-agent and orchestration

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Harnesses and patterns for multi-agent coordination and handoffs._

| # | Project | Description |
|---|---------|-------------|
| 1 | [**openai-agents-python**](https://github.com/openai/openai-agents-python) | Handoffs, guardrails, and multi-LLM routing; minimal surface so you own the loop. |
| 2 | [**crewAI**](https://github.com/crewAIInc/crewAI) | Role-based agents (roles, goals, backstories) in Crews; Flows add event-driven and hierarchical control for production. |
| 3 | [**autogen**](https://github.com/microsoft/autogen) | Conversable agents and group chats; code execution and human-in-the-loop; Microsoft origin, AG2 ecosystem. |
| 4 | [**PraisonAI**](https://github.com/PraisonAI/PraisonAI) | Autonomous multi-agent teams with a single entry point; emphasis on minimal config. |
| 5 | [**AgentRL**](https://github.com/THUDM/AgentRL) | Multitask, multiturn RL for LLM agents; Ray-based scaling, rollout/actor workers—for teams that want to train agents, not just run them. |

## Plugins, MCPs, CLI tools

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_IDE plugins, concrete MCP servers, and CLI tools that give agents tools and context._

| # | Project | Description |
|---|---------|-------------|
| 1 | [**aider**](https://github.com/Aider-AI/aider) | Git-aware CLI pair programmer; edits in-repo, supports multiple models and MCP so agents see version control and tools. |
| 2 | [**Better-OpenCodeMCP**](https://github.com/ajhcs/Better-OpenCodeMCP) | MCP server for OpenCode/Crush: async task execution, model bridging (e.g. Claude→Gemini), process pooling. |
| 3 | [**MCP Python SDK**](https://github.com/modelcontextprotocol/python-sdk) | Official SDK to build and consume MCP servers/clients in Python; stdio and SSE transports. |
| 4 | [**MCP TypeScript SDK**](https://github.com/modelcontextprotocol/typescript-sdk) | Official MCP implementation for Node/TS; reference for the protocol. |
| 5 | [**continue**](https://github.com/continuedev/continue) | Open-source IDE extension (VS Code, JetBrains); in-editor completion and chat with local or API models. |
| 6 | [**MCP Inspector**](https://github.com/modelcontextprotocol/inspector) | GUI to test and debug MCP servers; inspect tools, resources, and prompts. |
| 7 | [**github-mcp-server**](https://github.com/cyanheads/github-mcp-server) | MCP server for GitHub: repos, issues, PRs, code search; so your agent can “use GitHub” without hand-rolled API glue. |
| 8 | [**docker-mcp-servers**](https://github.com/docker/mcp-servers) | Docker’s official MCP servers; reference implementations for container-aware tooling and context. |
| 9 | [**puppeteer-mcp-server**](https://github.com/merajmehrabi/puppeteer-mcp-server) | Browser automation via MCP: tabs, screenshots, forms, JS execution; the one that connects to existing Chrome for dev/debug. |
| 10 | [**puppeteer-real-browser-mcp**](https://github.com/withLinda/puppeteer-real-browser-mcp-server) | Puppeteer MCP with real-browser and anti-detection; for agents that need to drive sites that block headless. |

## Evaluation and benchmarking harnesses

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Agentic eval systems, reasoning benchmarks, and open agent benchmarks._

| # | Project | Description |
|---|---------|-------------|
| 1 | [**ARC-AGI-2**](https://github.com/arcprize/ARC-AGI-2) | ARC Prize task set: grid-based abstraction/reasoning; public and private splits for generalization. |
| 2 | [**arc-agi-benchmarking**](https://github.com/arcprize/arc-agi-benchmarking) | Runner for ARC-AGI: multi-provider (OpenAI, Anthropic, Gemini, etc.), rate limits, retries, and scoring. |
| 3 | [**AgencyBench**](https://github.com/GAIR-NLP/AgencyBench) | Long-horizon agent benchmark: 32 scenarios, 138 tasks, ~1M tokens and ~90 tool calls; Docker sandbox and rubric-based + LLM judges. |
| 4 | [**TRAIL**](https://github.com/patronus-ai/trail-benchmark) | Trace reasoning and agentic issue localization; 148 long-context traces, 841 errors, 20+ error types; Hugging Face dataset. |
| 5 | [**AgentBench**](https://github.com/THUDM/AgentBench) | ICLR’24 benchmark: agents across AlfWorld, DB, knowledge graphs, OS, webshop; Docker Compose, function-calling interface. |
| 6 | [**WebArena**](https://github.com/web-arena-x/webarena) | Realistic web env (e.g. e‑commerce, CMS, dev tools); 812 tasks; measures end-to-end web agent success. |
| 7 | [**SWE-bench**](https://github.com/princeton-nlp/SWE-bench) | LMs resolve real GitHub issues; Docker harness, instance IDs; standard for code-agent evals. |
| 8 | [**SWE-Gym**](https://github.com/SWE-Gym/SWE-Gym) | Training and evaluation for SWE agents and verifiers (ICML 2025). |
| 9 | [**swe-smith**](https://github.com/swe-bench/swe-smith) | Data generation for SWE agents; 50k+ instances across 128 repos; used for SWE-agent-LM training. |
| 10 | [**SUPER**](https://github.com/allenai/super-benchmark) | Agents that set up and run ML/NLP from GitHub repos; 45 expert problems, 152 masked tasks, 602 AutoGen tasks; Docker-based. |
| 11 | [**VitaBench**](https://github.com/meituan-longcat/vitabench) | ICLR’26: 66 tools, real-world apps (delivery, travel, retail); 100 cross-scenario + 300 single-scenario tasks; adopted by Qwen/Seed. |
| 12 | [**letta-evals**](https://github.com/letta-ai/letta-evals) | Eval harness for stateful Letta agents; configurable suites and grading (LLM or rule-based) so you can measure what you ship. |
| 13 | [**gaia-agent**](https://github.com/sassarini-marco/gaia-agent) | Modular runner for the GAIA benchmark (450 real-world assistant questions); multi-agent evaluation without the Inspect AI lock-in. |
| 14 | [**WebVoyager**](https://github.com/MinorJerry/WebVoyager) | End-to-end web agent with LMMs: screenshots + actions on real sites; benchmark on 15 sites, GPT-4V for automatic eval. |
| 15 | [**inspect_evals**](https://github.com/UKGovernmentBEIS/inspect_evals) | UK AISI/Arcadia/Vector: GAIA and other evals in Inspect AI; level 1–3, sandboxed, tool-calling solvers. |

## Research and task-specific harnesses

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Deep research, document QA, and domain-specific agent loops._

| # | Project | Description |
|---|---------|-------------|
| 1 | [**openagents**](https://github.com/OpenAgentsInc/openagents) | Platform for autonomous agents and autopilot-style workflows; decentralized/Nostr-oriented. |
| 2 | [**multi-scale-agentic-rag-playbook**](https://github.com/nvidia-ai-technology-center/multi-scale-agentic-rag-playbook) | NVIDIA’s playbook: RAG at different scales with LangGraph agents, abstract search, and query routing—reference architecture, not a product. |
| 3 | [**Agentic_RAG_System**](https://github.com/sriramE5/Agentic_RAG_System) | Ollama + LangChain, FAISS/BM25/RRF retrieval and an agentic reasoning loop; one concrete stack for “RAG that corrects itself.” |

## Libraries and SDKs

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Lightweight runtimes, tool loops, and provider-agnostic harness primitives._

| # | Project | Description |
|---|---------|-------------|
| 1 | [**pydantic-ai**](https://github.com/pydantic/pydantic-ai) | Type-safe Python agents with Pydantic I/O; multi-provider, MCP, Logfire observability, and human-in-the-loop. |
| 2 | [**open-harness**](https://github.com/MaxGfeller/open-harness) | TypeScript Agent class on Vercel AI SDK; streaming events, filesystem/bash tools, MCP, and subagent delegation. |
| 3 | [**vercel/ai**](https://github.com/vercel/ai) | React and Node SDK for streaming, tool calls, and agent-style UIs; provider-agnostic. |
| 4 | [**agent-harness**](https://github.com/haasonsaas/agent-harness) | Thin Python shim to swap OpenAI vs Anthropic agent SDKs behind one interface. |
| 5 | [**smolagents**](https://github.com/huggingface/smolagents) | Code-as-action agents: model outputs Python executed in sandbox (E2B, Modal, etc.); ~1k LOC core. |
| 6 | [**Community-curated agent lists**](https://github.com/awesomelistsio/awesome-ai-agents) | Broader directories: e.g. [awesomelistsio/awesome-ai-agents](https://github.com/awesomelistsio/awesome-ai-agents), [axioma-ai-labs/awesome-ai-agent-frameworks](https://github.com/axioma-ai-labs/awesome-ai-agent-frameworks), [mb-mal/awesome-ai-agents-frameworks](https://github.com/mb-mal/awesome-ai-agents-frameworks)—differ by scope and update cadence. |
| 7 | [**agentic**](https://github.com/transitive-bullshit/agentic) | TypeScript agent stdlib: works with any LLM and the TS AI SDK; few abstractions, so you own the loop and the UI. |
| 8 | [**strands-agents**](https://github.com/strands-agents/sdk-python) | Model-driven Python SDK; decorators for tools, native MCP, multi-agent; “minimal code” without sacrificing provider choice. |
| 9 | [**LiteLLM**](https://github.com/BerriAI/litellm) | One interface to 100+ LLMs; routing, caching, budgets. Not an agent framework—the pipe every agent framework uses. |
| 10 | [**litellm2**](https://github.com/markolofsen/litellm2) | LiteLLM plus structured Pydantic outputs, budget controls, and agent-style tool loops; OpenRouter-default option. |
| 11 | [**openai-agents-js**](https://github.com/openai/openai-agents-js) | Official OpenAI Agents SDK for Node/TS: handoffs, guardrails, voice; the JS counterpart to openai-agents-python. |
| 12 | [**agent-framework**](https://github.com/maxmoundas/agent-framework) | LiteLLM-backed Python with dynamic tool registry, query routing, memory, and Streamlit UI; “full-stack agent app” in one repo. |
| 13 | [**agentic-ai**](https://github.com/vorachet/agentic-ai) | Agentic AI stdlib for TypeScript; any LLM, any TS AI SDK; another “thin layer so you own the rest” option. |

<br>

---

## Related Resources

- [**Awesome**](https://github.com/sindresorhus/awesome): Awesome lists on many topics
- [**OpenAI – Harness engineering**](https://openai.com/index/harness-engineering/): Environment design, intent, feedback loops, repo-as-system-of-record
- [**Anthropic – Effective harnesses for long-running agents**](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): Session bridging, feature lists, incremental progress, testing
- [**Aakash Gupta (Medium) – 2026 is agent harnesses**](https://aakashgupta.medium.com/2025-was-agents-2026-is-agent-harnesses-heres-why-that-changes-everything-073e9877655e): Harness as moat, minimal intervention, progressive disclosure
- [**LangChain**](https://python.langchain.com/), [**Anthropic**](https://docs.anthropic.com/), [**OpenAI**](https://platform.openai.com/docs): Official docs for major agent platforms

## Contribution

Contributions are welcome. To add or suggest projects:

- Open an [issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues) with the repo URL, category, and a short description.
- Or submit a [pull request](https://github.com/RyanAlberts/best-of-Agent-Harnesses/pulls) editing [projects.yaml](https://github.com/RyanAlberts/best-of-Agent-Harnesses/blob/main/projects.yaml) (and optionally README.md).

For contribution guidelines, see [CONTRIBUTING.md](https://github.com/RyanAlberts/best-of-Agent-Harnesses/blob/main/CONTRIBUTING.md) and the [Code of Conduct](https://github.com/RyanAlberts/best-of-Agent-Harnesses/blob/main/.github/CODE_OF_CONDUCT.md).

## License

[![CC BY-SA 4.0](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
