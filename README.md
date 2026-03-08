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
    <a href="#contents" title="Project Count"><img src="https://img.shields.io/badge/projects-55+-blue.svg?color=5ac4bf"></a>
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

- [Full-stack and long-running coding harnesses](#full-stack-and-long-running-coding-harnesses) _9 projects_
- [Multi-agent and orchestration frameworks](#multi-agent-and-orchestration-frameworks) _13 projects_
- [IDE and CLI agent integrations](#ide-and-cli-agent-integrations) _9 projects_
- [Evaluation and benchmarking harnesses](#evaluation-and-benchmarking-harnesses) _6 projects_
- [Research and task-specific harnesses](#research-and-task-specific-harnesses) _1 projects_
- [Libraries and SDKs](#libraries-and-sdks) _18 projects_

## Explanation

- 🥇🥈🥉&nbsp; Combined project-quality score
- ⭐️&nbsp; Star count from GitHub
- 🐣&nbsp; New project _(less than 6 months old)_
- 💤&nbsp; Inactive project _(6 months no activity)_
- 💀&nbsp; Dead project _(12 months no activity)_
- 📈📉&nbsp; Project is trending up or down
- ➕&nbsp; Project was recently added
- 👨‍💻&nbsp; Contributors count from GitHub
- 🔀&nbsp; Fork count from GitHub
- 📋&nbsp; Issue count from GitHub
- ⏱️&nbsp; Last update timestamp on package manager
- <img src="https://www.python.org/static/favicon.ico" style="display:inline;" width="13" height="13">&nbsp; Python
- <img src="https://cdn.icon-icons.com/icons2/2108/PNG/512/javascript_icon_130900.png" style="display:inline;" width="13" height="13">&nbsp; JavaScript/TypeScript

<br>

## Full-stack and long-running coding harnesses

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Spec-driven, multi-session, repo-scoped coding harnesses (e.g. GSD, Claude Agent SDK, OpenCode)._

| # | Project | Description |
|---|---------|-------------|
| 1 | [**get-shit-done**](https://github.com/gsd-build/get-shit-done) | Spec-driven meta-prompting and context engineering for Claude Code and others; goal-backward planning, wave-based execution, prevents context rot. |
| 2 | [**claude-agent-sdk-python**](https://github.com/anthropics/claude-agent-sdk-python) | Official Claude Agent SDK for Python: tools, MCP, long-running coding agents. |
| 3 | [**claude-agent-sdk-typescript**](https://github.com/anthropics/claude-agent-sdk-typescript) | Official Claude Agent SDK for TypeScript/Node. |
| 4 | [**claude-agent-sdk-demos**](https://github.com/anthropics/claude-agent-sdk-demos) | Example agents (email, research, Excel, etc.) using the Claude Agent SDK. |
| 5 | [**claude-quickstarts**](https://github.com/anthropics/claude-quickstarts) | Quickstarts including long-running autonomous coding with initializer + coding agent. |
| 6 | [**RepoMaster**](https://github.com/QuantaAlpha/RepoMaster) | Autonomous exploration of GitHub repos for complex coding tasks; function-call and dependency graphs. |
| 7 | [**coderClaw**](https://github.com/SeanHogg/coderClaw) | Multi-agent coding system (Creator, Reviewer, Test, Refactor, etc.); IDE-independent, self-hosted. |
| 8 | [**opencode**](https://github.com/opencode-ai/opencode) | Open-source AI coding agent for the terminal; multi-session, multi-provider. |
| 9 | [**crush**](https://github.com/charmbracelet/crush) | Successor to OpenCode; terminal-based AI coding agent (Charm). |

## Multi-agent and orchestration frameworks

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Sub-agents, handoffs, crews, and graph-based orchestration._

| # | Project | Description |
|---|---------|-------------|
| 1 | [**langgraph**](https://github.com/langchain-ai/langgraph) | Graph-based state machine for multi-step agent workflows; checkpointing, human-in-the-loop. |
| 2 | [**langchain**](https://github.com/langchain-ai/langchain) | Framework for LLM applications and agent chains; tools, memory, orchestration. |
| 3 | [**openai-agents-python**](https://github.com/openai/openai-agents-python) | OpenAI Agents SDK: handoffs, guardrails, multi-LLM support. |
| 4 | [**crewAI**](https://github.com/crewAIInc/crewAI) | Role-based autonomous agents; Crews and Flows for collaborative and event-driven workflows. |
| 5 | [**autogen**](https://github.com/microsoft/autogen) | Conversable agents, group chats, and multi-agent patterns (Microsoft; AG2 ecosystem). |
| 6 | [**mastra**](https://github.com/mastra-ai/mastra) | TypeScript framework for AI agents and workflows. |
| 7 | [**phidata**](https://github.com/phidata-ai/phidata) | Python framework for production agents with memory, knowledge, and tools. |
| 8 | [**agno**](https://github.com/agno-ai/agno) | Python agent framework with orchestration and tool use. |
| 9 | [**langflow**](https://github.com/langchain-ai/langflow) | UI and runtime for building and deploying LangChain/LangGraph flows. |
| 10 | [**letta**](https://github.com/letta/letta) | Python agent runtime and orchestration. |
| 11 | [**semantic-kernel**](https://github.com/microsoft/semantic-kernel) | Microsoft SDK for integrating LLMs with apps; plugins, planning, memory. |
| 12 | [**llama-index**](https://github.com/run-llama/llama_index) | Data framework and agents for LLM applications; RAG and tool use. |
| 13 | [**PraisonAI**](https://github.com/PraisonAI/PraisonAI) | Multi-agent framework for autonomous AI teams. |

## IDE and CLI agent integrations

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Cursor, MCP, Aider, OpenCode, and CLI wrappers that provide tools and context._

| # | Project | Description |
|---|---------|-------------|
| 1 | [**aider**](https://github.com/Aider-AI/aider) | AI pair programming in the terminal; git-aware, multi-model, MCP support. |
| 2 | [**mcp-servers**](https://github.com/modelcontextprotocol/servers) | Reference MCP servers and examples (Model Context Protocol). |
| 3 | [**specification**](https://github.com/modelcontextprotocol/specification) | Model Context Protocol spec and documentation. |
| 4 | [**best-of-mcp-servers**](https://github.com/tolkonepiu/best-of-mcp-servers) | Curated list of MCP servers. |
| 5 | [**Better-OpenCodeMCP**](https://github.com/ajhcs/Better-OpenCodeMCP) | MCP server for OpenCode CLI; async tasks, multi-model bridge. |
| 6 | [**python-sdk**](https://github.com/modelcontextprotocol/python-sdk) | Official MCP Python SDK for building servers and clients. |
| 7 | [**typescript-sdk**](https://github.com/modelcontextprotocol/typescript-sdk) | Official MCP TypeScript SDK. |
| 8 | [**continue**](https://github.com/continuedev/continue) | Open-source Copilot alternative; IDE extensions and context. |

## Evaluation and benchmarking harnesses

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_SWE-bench-style evals, agent benchmarks, and reproducibility._

| # | Project | Description |
|---|---------|-------------|
| 1 | [**SWE-bench**](https://github.com/princeton-nlp/SWE-bench) | Benchmark for LMs on real GitHub issues; Docker-based evaluation harness. |
| 2 | [**SWE-Gym**](https://github.com/SWE-Gym/SWE-Gym) | Training and evaluation for software engineering agents (ICML 2025). |
| 3 | [**SWE-bench-fork**](https://github.com/METR/SWE-bench-fork) | Fork and variants of SWE-bench evaluation. |
| 4 | [**swe-smith**](https://github.com/swe-bench/swe-smith) | Scaling data for SWE agents (NeurIPS 2025). |
| 5 | [**SWE-agent**](https://github.com/princeton-nlp/SWE-agent) | Agent and evaluation for SWE-bench. |

## Research and task-specific harnesses

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Deep research, document QA, and domain-specific agent loops._

| # | Project | Description |
|---|---------|-------------|
| 1 | [**openagents**](https://github.com/OpenAgentsInc/openagents) | Platform for AI agents; autopilot and agent network. |

## Libraries and SDKs

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Lightweight agent runtimes, tool loops, and provider-agnostic harness primitives._

| # | Project | Description |
|---|---------|-------------|
| 1 | [**pydantic-ai**](https://github.com/pydantic/pydantic-ai) | Type-safe Python agent framework; multi-provider, MCP, observability. |
| 2 | [**open-harness**](https://github.com/MaxGfeller/open-harness) | TypeScript agent SDK on Vercel AI SDK; tools, MCP, subagents. |
| 3 | [**vercel/ai**](https://github.com/vercel/ai) | Vercel AI SDK: streaming, tools, and agent patterns. |
| 4 | [**agent-harness**](https://github.com/haasonsaas/agent-harness) | Unified interface for swapping OpenAI and Anthropic agent SDKs. |
| 5 | [**inspector**](https://github.com/modelcontextprotocol/inspector) | Visual testing and debugging for MCP servers. |
| 6 | [**rasa**](https://github.com/rasa/rasa) | Conversational AI and agent framework. |
| 7 | [**botpress**](https://github.com/botpress/botpress) | Open-source conversational AI platform. |
| 8 | [**smolagents**](https://github.com/huggingface/smolagents) | Barebones library for code-first agents (Hugging Face). |
| 9 | [**awesome-ai-agents**](https://github.com/awesomelistsio/awesome-ai-agents) | Curated list of AI agent frameworks and tools. |
| 10 | [**awesome-ai-agents**](https://github.com/korchasa/awesome-ai-agents) | Auto-updated directory of AI agent resources. |
| 11 | [**awesome-ai-agent-frameworks**](https://github.com/axioma-ai-labs/awesome-ai-agent-frameworks) | Battle-tested agent framework recommendations. |
| 12 | [**awesome-ai-agents-frameworks**](https://github.com/mb-mal/awesome-ai-agents-frameworks) | Ranked list of AI agent frameworks. |
| 13 | [**awesome-ai-agents**](https://github.com/Deep-Insight-Labs/awesome-ai-agents) | Practical AI agent resources and ecosystem. |
| 14 | [**tinyclaw**](https://github.com/tinyclaw/tinyclaw) | Lightweight agent framework. |
| 15 | [**openfang**](https://github.com/openfang-ai/openfang) | Agent and harness tooling. |

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
