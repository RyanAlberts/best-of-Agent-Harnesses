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
    <a href="#contents" title="Project Count"><img src="https://img.shields.io/badge/projects-101-blue.svg?color=5ac4bf"></a>
    <a href="#contribution" title="Contributions welcome"><img src="https://img.shields.io/badge/contributions-welcome-green.svg"></a>
    <a href="https://github.com/RyanAlberts/best-of-Agent-Harnesses/releases" title="Updates"><img src="https://img.shields.io/github/release-date/RyanAlberts/best-of-Agent-Harnesses?color=green&label=updated"></a>
</p>

## What is an agent harness?

An agent harness is the runtime that closes the loop between a stateless model and the outside world—managing perception, action, memory, and constraint enforcement—making it the de facto operating system of machine agency and, consequently, the layer where nearly all meaningful questions about AI autonomy, reliability, and control are actually resolved.

Every prior wave of automation was constrained by brittleness: you scripted exact behavior, and when the world deviated, the system broke. Foundation models inverted that problem—they're flexible but directionless, stateless, and disconnected from anything real. The agent harness exists to bridge that gap: it is the orchestration infrastructure that converts a model's per-turn reasoning into sustained, tool-using, error-recovering, goal-directed behavior across time. Architecturally, it plays the role the kernel played in operating systems or the controller played in industrial robotics—mediating between raw capability and a messy environment—but with a critical difference: the "capability" it governs is general-purpose cognition, which means the harness is simultaneously a scheduler, a permission system, a memory manager, and a policy enforcement layer, all under-specified and evolving in real time. The term itself barely exists in formal literature yet, which should concern anyone who cares about AI governance, because the harness is where abstract alignment goals either get operationalized into concrete constraints or quietly don't.

## Why harnesses matter

Better models make harnesses more important: more capabilities mean more failure modes, and production needs retry logic, fallbacks, and validation. Harness quality—not just model quality—determines whether agents actually ship. This list ranks projects by relevance to harness concerns (environment, orchestration, lifecycle, guardrails) and by stars/activity.

## Contents

- [Progressive disclosure harnesses](#progressive-disclosure-harnesses) _7 projects_
- [Coding agent products (IDEs, CLIs, full suites)](#coding-agent-products-ides-clis-full-suites) _10 projects_
- [Coding harness configs and SDKs](#coding-harness-configs-and-sdks) _11 projects_
- [Frameworks](#frameworks) _24 projects_
- [Multi-agent and orchestration](#multi-agent-and-orchestration) _5 projects_
- [Plugins, MCPs, CLI tools](#plugins-mcps-cli-tools) _12 projects_
- [Evaluation and benchmarking harnesses](#evaluation-and-benchmarking-harnesses) _16 projects_
- [Research and task-specific harnesses](#research-and-task-specific-harnesses) _2 projects_
- [Libraries and SDKs](#libraries-and-sdks) _14 projects_

## Explanation

- **Simplicity ↔ capability:** Where each project sits on the axis from minimal/simple (lean API, format only, thin layer) to high capability (full platform, many features, kitchen-sink).
- **OSS:** ✅ = standard open-source license (MIT/Apache/BSD/GPL/MPL/AGPL/CC0). ⚠️ = source-available or restricted (e.g. n8n Fair-code, Elastic-2.0, Polyform). ❓ = no license file or unclear terms.
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

## Progressive disclosure harnesses

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Formats, runtimes, and patterns that reveal context, tools, or instructions in layers—index first, details on demand—to control tokens and improve agent focus (the "map, not encyclopedia" principle)._

| # | Project | Description | OSS | Simplicity ↔ capability |
|---|---------|-------------|-----|-------------------------|
| 1 | [**agents.md**](https://github.com/agentsmd/agents.md) | Open format for repo-scoped agent briefings; v1.1 adds hierarchical scope and progressive disclosure so agents get a map of what exists, then load only what's relevant. | ✅ | Simple (format only) |
| 2 | [**awesome-cursorrules**](https://github.com/PatrickJS/awesome-cursorrules) | Curated .cursorrules and skills that leverage Cursor's index-then-load model; the canonical collection for rules-as-progressive-disclosure in the IDE. | ✅ | Simple (content bundle) |
| 3 | [**MCP-Zero**](https://github.com/xfey/MCP-Zero) | Active tool discovery for autonomous agents: model requests tools by requirement; hierarchical semantic routing over 308 servers / 2,797 tools with ~98% token reduction (APIBank). | ✅ | Capability (3k tools, full routing) |
| 4 | [**langgraph-bigtool**](https://github.com/langchain-ai/langgraph-bigtool) | Build LangGraph agents with large tool sets; retrieval and on-demand tool loading so agents scale beyond context without stuffing every schema upfront. | ✅ | Capability (large tool sets) |
| 5 | [**spring-ai-tool-search-tool**](https://github.com/spring-ai-community/spring-ai-tool-search-tool) | Dynamic tool discovery for Spring AI: model gets a search tool first, then pulls definitions for relevant tools; 34–64% token reduction across providers. | ✅ | Mid (search-then-load) |
| 6 | [**ToolGen**](https://github.com/Reason-Wang/ToolGen) | ICLR 2025: unified tool retrieval and calling via generation; 47k+ tools without context stuffing—retrieval and invocation in one generative step. | ❓ | Capability (47k+ tools) |
| 7 | [**ToolRAG**](https://github.com/antl3x/ToolRAG) | Semantic tool retrieval for LLMs; serves only the tools the user query demands (MCP-compatible), unlimited tool sets with zero context penalty. | ✅ | Mid (query-driven retrieval) |

## Coding agent products (IDEs, CLIs, full suites)

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Turnkey coding agents you install and run: IDE extensions, terminal CLIs, Dockerized workspaces. Each entry notes which part is the harness (the agent loop, tool wiring, approval model) versus the UI shell (VS Code extension, TUI, browser client)._

| # | Project | Description | OSS | Simplicity ↔ capability |
|---|---------|-------------|-----|-------------------------|
| 1 | [**Cline**](https://github.com/cline/cline) | VS Code extension whose **harness** is a plan-then-act loop with per-step human approval and cost transparency; the VS Code integration is the UI shell. Open-source counterweight to Cursor. | ✅ | Mid (plan-then-act, approval gates) |
| 2 | [**Roo Code**](https://github.com/RooCodeInc/Roo-Code) | VS Code/Cursor extension in the Cline lineage. The **harness** is the approval-gated agent with custom modes and a strong MCP story; the IDE is the UI. Popular community fork when you want that workflow without the upstream extension. | ✅ | Mid (IDE extension, MCP-first) |
| 3 | [**Codex**](https://github.com/openai/codex) | OpenAI's terminal coding agent. The **harness** is the sandboxed tool-call loop with multi-provider support; the CLI is the shell. Reference implementation for "official CLI that ships code." | ✅ | Mid (reference CLI, sandboxed) |
| 4 | [**Gemini CLI**](https://github.com/google-gemini/gemini-cli) | Google's first-party terminal agent for Gemini. The **harness** is the plugin/MCP tool-call loop; the terminal is the shell—Google's parallel to Claude Code / Codex, not just an API. | ✅ | Mid (official CLI, plugins, MCP) |
| 5 | [**crush**](https://github.com/charmbracelet/crush) | Charm's terminal coding agent (Charm's fork of the original OpenCode). The **harness** is the tool-calling loop with session persistence; the Bubble Tea TUI is the shell. | ⚠️ FSL-1.1-MIT | Mid (terminal agent, TUI) |
| 6 | [**opencode**](https://github.com/sst/opencode) | SST's open-source terminal coding agent—the line of OpenCode that kept the name. The **harness** is a multi-provider tool-call loop (Claude, OpenAI, Gemini, local) with strong plugin and MCP support; the TUI is the shell. 100% OSS, very actively shipped. | ✅ | Mid (multi-provider, plugins, MCP) |
| 7 | [**OpenHands**](https://github.com/OpenHands/OpenHands) | Dockerized software-engineering agent. The **harness** is the bash/editor/browser toolset with micro-agents and event-stream session bridging; Docker is the sandbox. Main OSS choice for teams self-hosting autonomous repo work. | ⚠️ (multi-license) | Capability (Docker runtime, multi-surface agent) |
| 8 | [**goose**](https://github.com/block/goose) | Block's extensible Rust agent. The **harness** is the MCP/ACP extension model with recipes and provider choice; there's no fixed UI slot—you bolt it into whatever shell you use. | ✅ | Mid (extensions, MCP/ACP) |
| 9 | [**claw-code-agent**](https://github.com/HarnessLab/claw-code-agent) | Python reimplementation of the Claude Code agent architecture with zero external dependencies; interactive chat, streaming, plugin runtime, nested agent delegation, cost tracking, MCP transport—portable harness without the Rust/TS toolchain. | ❓ | Capability (pure Python, plugin runtime) |
| 10 | [**coderClaw**](https://github.com/SeanHogg/coderClaw) | Self-hosted multi-role coding system (Creator, Reviewer, Test, Refactor, etc.) with AST and semantic maps; IDE-agnostic, chat-channel triggers. | ❓ | Capability (multi-role, AST/semantic) |

## Coding harness configs and SDKs

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Skill packs, slash-command libraries, meta-prompting frameworks, and official SDKs that give you the harness (the agent loop, planning, memory, hooks) without bundling a specific IDE or CLI shell._

| # | Project | Description | OSS | Simplicity ↔ capability |
|---|---------|-------------|-----|-------------------------|
| 1 | [**get-shit-done**](https://github.com/gsd-build/get-shit-done) | Goal-backward planning and wave-based execution over fresh context windows; avoids context rot by design. Python/JS meta-prompting for Claude Code, OpenCode, Gemini CLI. | ✅ | Mid (meta-prompting, you own stack) |
| 2 | [**GStack**](https://github.com/garrytan/gstack) | Garry Tan's Claude Code skill stack: 23 slash-command modes (CEO/eng/design review, QA, ship, browse, retro, …) that structure one assistant as a virtual engineering team. Daily driver while running YC. | ✅ | Capability (multi-role slash-command harness) |
| 3 | [**everything-claude-code**](https://github.com/affaan-m/everything-claude-code) | The breakout 2026 harness pack for Claude Code (approaching 160k stars): 28 specialized subagents, 119 reusable skills, 60 slash commands, 34 rules, 20+ automated hooks. Ships a full "AI engineering team" as config. | ✅ | Capability (subagents + skills + hooks) |
| 4 | [**superpowers**](https://github.com/obra/superpowers) | Performance-oriented harness pack for Claude Code, Codex, OpenCode, Cursor: skills, instincts, memory, security, research-first workflows. Treats harness engineering itself as the performance lever. | ✅ | Capability (multi-IDE skill stack) |
| 5 | [**pmstack**](https://github.com/RyanAlberts/pmstack) | Claude Code config for AI product managers: CLAUDE.md plus skills for competitive analysis, PRD-from-signal, metric frameworks, stakeholder briefs, and agent eval design. "GStack for PMs." | ✅ | Simple (skills bundle, PM-focused) |
| 6 | [**Claude Agent SDK**](https://github.com/anthropics/claude-agent-sdk-python) | Official Anthropic SDK (Python + [TypeScript](https://github.com/anthropics/claude-agent-sdk-typescript), [demos](https://github.com/anthropics/claude-agent-sdk-demos), [quickstarts](https://github.com/anthropics/claude-quickstarts)): built-in tools, MCP, long-running coding agents with session bridging. | ✅ | Capability (full SDK, session bridging) |
| 7 | [**AutoHarness**](https://github.com/aiming-lab/AutoHarness) | Lightweight governance harness: wraps any LLM client in ~2 lines for automated harness engineering—6–14 step pipeline, YAML constitution, risk-pattern matching, session persistence with cost tracking, multi-agent profiles. | ✅ | Simple (2-line wrapper, YAML gov) |
| 8 | [**RepoMaster**](https://github.com/QuantaAlpha/RepoMaster) | Repo-scoped research harness: builds function-call and module-dependency graphs to explore only what's needed; large relative gains on MLE-bench and GitTaskBench with lower token use. | ❓ | Capability (graph-based exploration) |
| 9 | [**SWE-agent**](https://github.com/SWE-agent/SWE-agent) | LM-driven harness built for SWE-bench: edit state, command execution, and issue-focused loop—the reference agent stack next to the benchmark itself. | ✅ | Capability (SWE-bench pairing, stateful edits) |
| 10 | [**OpenHarness (HKUDS)**](https://github.com/HKUDS/OpenHarness) | Open agent harness with a built-in personal agent ("Ohmo") that runs across Feishu, Slack, Telegram, and Discord; core tool-use, skills, memory, multi-agent coordination with auto-compaction for multi-day sessions. | ✅ | Capability (personal agent + multi-channel) |
| 11 | [**Anthropic Skills**](https://github.com/anthropics/skills) | Anthropic's official Agent Skills repository: SKILL.md-based folders (instructions, scripts, resources) Claude dynamically loads on Claude Code, Claude.ai, and the API. The reference for progressive-disclosure skill packs in 2026. | ✅ | Mid (official skills format) |

## Frameworks

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_General-purpose agent and LLM application frameworks (the app layer, not harnesses per se)._

| # | Project | Description | OSS | Simplicity ↔ capability |
|---|---------|-------------|-----|-------------------------|
| 1 | [**langgraph**](https://github.com/langchain-ai/langgraph) | State-machine graphs over LLM steps; checkpointing, human-in-the-loop, and durable execution so workflows survive restarts. | ✅ | Capability (graphs, checkpointing, durable exec) |
| 2 | [**langchain**](https://github.com/langchain-ai/langchain) | Chains, tools, retrievers, and agents; the usual entry point for "add tools to an LLM" in Python/JS. | ✅ | Capability (kitchen-sink ecosystem) |
| 3 | [**llama-index**](https://github.com/run-llama/llama_index) | Data-centric: indexing, RAG, and query engines; agent abstractions sit on top of your data pipelines. | ✅ | Capability (RAG + agents) |
| 4 | [**semantic-kernel**](https://github.com/microsoft/semantic-kernel) | Microsoft's plugin and planner layer for LLMs; C#, Python, Java; strong on enterprise auth and orchestration. | ✅ | Capability (enterprise, multi-language) |
| 5 | [**mastra**](https://github.com/mastra-ai/mastra) | TypeScript-first; agents, tools, and workflows with a single runtime and minimal boilerplate. | ⚠️ Elastic-2.0 | Mid (TS-first, minimal boilerplate) |
| 6 | [**agno**](https://github.com/agno-agi/agno) | Python agents with memory, knowledge bases, tools, and structured outputs; continues the PhiData-era product line under the Agno name—production apps, evals, and pipelines. | ✅ | Capability (memory, KB, observability) |
| 7 | [**letta**](https://github.com/letta-ai/letta) | Python agent runtime with tool use and control flow; lean API; stateful agents with long-horizon memory. | ✅ | Simple (lean API) |
| 8 | [**langflow**](https://github.com/langflow-ai/langflow) | Low-code UI to build and deploy LangChain/LangGraph flows; visual DAG editor and one-click run. | ✅ | Capability (low-code, visual) |
| 9 | [**rasa**](https://github.com/rasa/rasa) | Conversational AI stack (NLU, dialogue, actions); long-standing OSS choice for chat and voice bots. | ✅ | Capability (full stack) |
| 10 | [**botpress**](https://github.com/botpress/botpress) | Visual bot builder and runtime; multi-channel, open-source alternative to commercial bot platforms. | ✅ | Capability (visual builder, multi-channel) |
| 11 | [**Dify**](https://github.com/langgenius/dify) | One-stop LLM app platform: visual workflows, RAG pipeline, 50+ tools, model management; "ship from prototype to prod" in a single UI. | ⚠️ Fair-code | Capability (one-stop platform) |
| 12 | [**n8n**](https://github.com/n8n-io/n8n) | Fair-code workflow engine with 400+ nodes and native AI nodes; the self-hosted Zapier that actually does agents and LangChain. | ⚠️ Fair-code | Capability (400+ nodes, workflow engine) |
| 13 | [**AutoGPT**](https://github.com/Significant-Gravitas/AutoGPT) | The original autonomous loop: goal in, agent iterates with tools and memory; Forge is the dev framework, Benchmark the eval harness. | ⚠️ Polyform-SU | Capability (autonomous loop, tools, memory) |
| 14 | [**AIlice**](https://github.com/myshell-ai/AIlice) | Fully autonomous general-purpose agent; one binary, Docker-ready, for when you want "set goal and walk away" without a framework. | ✅ | Capability (autonomous, one binary) |
| 15 | [**Bee Agent Framework**](https://github.com/i-am-bee/beeai-framework) | Python + TypeScript, LF AI–backed; MCP/ACP, workflows, Requirement Agent; the one that pushes "production multi-agent" without LangChain. | ✅ | Capability (production multi-agent) |
| 16 | [**agent-squad**](https://github.com/2FastLabs/agent-squad) | AWS-originated orchestrator (now under 2FastLabs): intent classification, streaming, SupervisorAgent; "agent-as-tools" so one agent delegates to a squad. | ✅ | Capability (squad orchestration) |
| 17 | [**SuperAgentX**](https://github.com/superagentxai/superagentx) | Lightweight multi-agent orchestrator with an AGI-angle; minimal surface, docs-first, for teams that want orchestration without the kitchen sink. | ✅ | Simple (minimal surface) |
| 18 | [**AgentVerse**](https://github.com/OpenBMB/AgentVerse) | Task-solving and simulation envs for multi-LLM agents; deploy many agents in custom environments without building infra from scratch. | ✅ | Capability (simulation envs, multi-agent) |
| 19 | [**R2R**](https://github.com/SciPhi-AI/R2R) | RAG-first: hybrid search, knowledge graphs, multimodal; the framework for "production RAG" when you care more about retrieval than chat UI. | ✅ | Capability (production RAG) |
| 20 | [**Google ADK**](https://github.com/google/adk-python) | Google's official Agent Development Kit: code-first Python toolkit for building, evaluating, and deploying agents. Optimized for Gemini but model-agnostic; deploys to Cloud Run / Vertex AI; ships a dev UI with eval and a code-execution sandbox. | ✅ | Capability (official Google SDK, eval, deploy) |
| 21 | [**AgentStack**](https://github.com/agentstack-ai/AgentStack) | Scaffolds full agent projects; plugs in CrewAI, LangGraph, OpenAI Swarm, LlamaStack and wires AgentOps observability from day one. | ✅ | Capability (scaffold, multi-backend) |
| 22 | [**AgentSilex**](https://github.com/howl-anderson/agentsilex) | ~300 lines of readable agent code on top of LiteLLM; the "I want to see the whole loop" option for learning or minimal production. | ✅ | Simple (~300 LOC) |
| 23 | [**Flowise**](https://github.com/FlowiseAI/Flowise) | Drag-and-drop LangChain UI; deploy flows without code. The low-code sibling to Langflow, with a different component and hosting story. | ⚠️ Apache+CLA | Capability (low-code, drag-drop) |
| 24 | [**browser-use**](https://github.com/browser-use/browser-use) | Python layer over Playwright: natural-language goals become browser actions—web-agent loop without hand-rolling MCP or a custom driver for every site. | ✅ | Mid (LLM + browser, Playwright) |

## Multi-agent and orchestration

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Harnesses and patterns for multi-agent coordination and handoffs._

| # | Project | Description | OSS | Simplicity ↔ capability |
|---|---------|-------------|-----|-------------------------|
| 1 | [**openai-agents-python**](https://github.com/openai/openai-agents-python) | Handoffs, guardrails, and multi-LLM routing; minimal surface so you own the loop. | ✅ | Simple (minimal surface) |
| 2 | [**crewAI**](https://github.com/crewAIInc/crewAI) | Role-based agents (roles, goals, backstories) in Crews; Flows add event-driven and hierarchical control for production. | ✅ | Capability (roles, Flows, production) |
| 3 | [**autogen**](https://github.com/microsoft/autogen) | Conversable agents and group chats; code execution and human-in-the-loop; Microsoft origin, AG2 ecosystem. | ✅ CC-BY | Capability (group chat, code exec, AG2) |
| 4 | [**PraisonAI**](https://github.com/MervinPraison/PraisonAI) | Autonomous multi-agent teams with a single entry point; emphasis on minimal config. | ✅ | Mid (single entry, minimal config) |
| 5 | [**AgentRL**](https://github.com/THUDM/AgentRL) | Multitask, multiturn RL for LLM agents; Ray-based scaling, rollout/actor workers—for teams that want to train agents, not just run them. | ✅ | Capability (RL, Ray, train agents) |

## Plugins, MCPs, CLI tools

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_IDE plugins, concrete MCP servers, and CLI tools that give agents tools and context._

| # | Project | Description | OSS | Simplicity ↔ capability |
|---|---------|-------------|-----|-------------------------|
| 1 | [**aider**](https://github.com/Aider-AI/aider) | Git-aware CLI pair programmer; edits in-repo, supports multiple models and MCP so agents see version control and tools. | ✅ | Mid (CLI, git-aware, MCP) |
| 2 | [**agentlog**](https://github.com/RyanAlberts/agentlog) | Persistent decision memory for any project: `remember`, `recall`, `reflect`. Single-file Python CLI that stores decisions as JSONL and uses Claude or Gemini to retrieve and synthesize patterns—Karpathy's LLM Wiki concept as a CLI. | ✅ | Simple (one file, three commands) |
| 3 | [**claude-mem**](https://github.com/thedotmack/claude-mem) | Claude Code plugin that captures everything an agent does during a session, AI-compresses it (via claude-agent-sdk), and injects the relevant context into future sessions—session-to-session memory as a drop-in. | ✅ | Capability (session capture + compression) |
| 4 | [**Better-OpenCodeMCP**](https://github.com/ajhcs/Better-OpenCodeMCP) | MCP server for OpenCode/Crush: async task execution, model bridging (e.g. Claude→Gemini), process pooling. | ✅ | Mid (MCP server, model bridging) |
| 5 | [**MCP Python SDK**](https://github.com/modelcontextprotocol/python-sdk) | Official SDK to build and consume MCP servers/clients in Python; stdio and SSE transports. | ✅ | Simple (SDK only) |
| 6 | [**MCP TypeScript SDK**](https://github.com/modelcontextprotocol/typescript-sdk) | Official MCP implementation for Node/TS; reference for the protocol. | ✅ | Simple (protocol reference) |
| 7 | [**continue**](https://github.com/continuedev/continue) | Open-source IDE extension (VS Code, JetBrains); in-editor completion and chat with local or API models. | ✅ | Capability (IDE extension, multi-editor) |
| 8 | [**MCP Inspector**](https://github.com/modelcontextprotocol/inspector) | GUI to test and debug MCP servers; inspect tools, resources, and prompts. | ✅ | Simple (debug GUI) |
| 9 | [**github-mcp-server**](https://github.com/github/github-mcp-server) | GitHub's official MCP server (Go): repos, issues, PRs, code search, Actions. Replaces the older community `cyanheads/github-mcp-server` as the canonical way to give agents GitHub access. | ✅ | Mid (official GitHub MCP) |
| 10 | [**MCP Registry**](https://github.com/modelcontextprotocol/registry) | Official, community-driven registry for MCP servers—the "app store" MCP clients use to discover servers. Maintained by Anthropic + ecosystem maintainers; v0.1 API frozen, production-grade. | ✅ | Mid (official discovery layer) |
| 11 | [**Docker MCP Gateway**](https://github.com/docker/mcp-gateway) | Docker's official MCP CLI plugin / gateway; container-aware MCP tooling from Docker (replaces deprecated `docker/mcp-servers` path). | ✅ | Mid (Docker-aware MCPs) |
| 12 | [**puppeteer-real-browser-mcp**](https://github.com/withLinda/puppeteer-real-browser-mcp-server) | Puppeteer MCP with real-browser and anti-detection; for agents that need to drive sites that block headless. | ❓ | Mid (real browser, anti-detect) |

## Evaluation and benchmarking harnesses

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Agentic eval systems, reasoning benchmarks, and open agent benchmarks._

| # | Project | Description | OSS | Simplicity ↔ capability |
|---|---------|-------------|-----|-------------------------|
| 1 | [**ARC-AGI-2**](https://github.com/arcprize/ARC-AGI-2) | ARC Prize task set: grid-based abstraction/reasoning; public and private splits for generalization. | ✅ | Simple (task set) |
| 2 | [**arc-agi-benchmarking**](https://github.com/arcprize/arc-agi-benchmarking) | Runner for ARC-AGI: multi-provider (OpenAI, Anthropic, Gemini, etc.), rate limits, retries, and scoring. | ✅ | Mid (runner, multi-provider) |
| 3 | [**AgencyBench**](https://github.com/GAIR-NLP/AgencyBench) | Long-horizon agent benchmark: 32 scenarios, 138 tasks, ~1M tokens and ~90 tool calls; Docker sandbox and rubric-based + LLM judges. | ✅ | Capability (32 scenarios, Docker, judges) |
| 4 | [**TRAIL**](https://github.com/patronus-ai/trail-benchmark) | Trace reasoning and agentic issue localization; 148 long-context traces, 841 errors, 20+ error types; Hugging Face dataset. | ✅ | Mid (traces, Hugging Face) |
| 5 | [**AgentBench**](https://github.com/THUDM/AgentBench) | ICLR'24 benchmark: agents across AlfWorld, DB, knowledge graphs, OS, webshop; Docker Compose, function-calling interface. | ✅ | Capability (multi-env, Docker Compose) |
| 6 | [**WebArena**](https://github.com/web-arena-x/webarena) | Realistic web env (e.g. e‑commerce, CMS, dev tools); 812 tasks; measures end-to-end web agent success. | ✅ | Capability (812 tasks, web env) |
| 7 | [**SWE-bench**](https://github.com/SWE-bench/SWE-bench) | LMs resolve real GitHub issues; Docker harness, instance IDs; standard for code-agent evals. | ✅ | Capability (real GitHub issues, standard) |
| 8 | [**SWE-Gym**](https://github.com/SWE-Gym/SWE-Gym) | Training and evaluation for SWE agents and verifiers (ICML 2025). | ✅ | Capability (training + eval, ICML) |
| 9 | [**swe-smith**](https://github.com/SWE-bench/SWE-smith) | Data generation for SWE agents; 50k+ instances across 128 repos; used for SWE-agent-LM training. | ✅ | Capability (50k+ instances, data gen) |
| 10 | [**SUPER**](https://github.com/allenai/super-benchmark) | Agents that set up and run ML/NLP from GitHub repos; 45 expert problems, 152 masked tasks, 602 AutoGen tasks; Docker-based. | ✅ | Capability (ML/NLP repos, Docker) |
| 11 | [**VitaBench**](https://github.com/meituan-longcat/vitabench) | ICLR'26: 66 tools, real-world apps (delivery, travel, retail); 100 cross-scenario + 300 single-scenario tasks; adopted by Qwen/Seed. | ✅ | Capability (66 tools, cross-scenario) |
| 12 | [**letta-evals**](https://github.com/letta-ai/letta-evals) | Eval harness for stateful Letta agents; configurable suites and grading (LLM or rule-based) so you can measure what you ship. | ✅ | Mid (Letta-specific harness) |
| 13 | [**WebVoyager**](https://github.com/MinorJerry/WebVoyager) | End-to-end web agent with LMMs: screenshots + actions on real sites; benchmark on 15 sites, GPT-4V for automatic eval. | ✅ | Capability (LMMs, screenshots, 15 sites) |
| 14 | [**inspect_evals**](https://github.com/UKGovernmentBEIS/inspect_evals) | UK AISI/Arcadia/Vector: GAIA and other evals in Inspect AI; level 1–3, sandboxed, tool-calling solvers. | ✅ | Mid (Inspect AI, UK gov) |
| 15 | [**inspect_ai**](https://github.com/UKGovernmentBEIS/inspect_ai) | Inspect AI core: composable eval tasks, sandboxes, scorers, and multi-model runs; the framework behind inspect_evals, not just the task bundle. | ✅ | Capability (eval framework, AISI stack) |
| 16 | [**Agent Lightning**](https://github.com/microsoft/agent-lightning) | Microsoft's training-oriented harness: optimization loops for agent behavior—when you need to improve policies over rollouts, not only score a fixed prompt. | ✅ | Capability (agent training, Microsoft stack) |

## Research and task-specific harnesses

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Deep research, document QA, and domain-specific agent loops._

| # | Project | Description | OSS | Simplicity ↔ capability |
|---|---------|-------------|-----|-------------------------|
| 1 | [**gpt-researcher**](https://github.com/assafelovic/gpt-researcher) | Autonomous deep-research agent: web + local sources, citation-grounded reports, multi-agent and deep-research modes. The reference open-source research harness. | ✅ | Capability (deep research, multi-agent) |
| 2 | [**openagents**](https://github.com/OpenAgentsInc/openagents) | Platform for autonomous agents and autopilot-style workflows; decentralized/Nostr-oriented (Pylon runtime, actively shipped in 2026). | ✅ | Capability (platform, decentralized) |

## Libraries and SDKs

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Lightweight runtimes, tool loops, and provider-agnostic harness primitives._

| # | Project | Description | OSS | Simplicity ↔ capability |
|---|---------|-------------|-----|-------------------------|
| 1 | [**deepagents**](https://github.com/langchain-ai/deepagents) | LangChain's Python+TypeScript agent harness on top of LangGraph: planning tool, virtual filesystem, shell sandbox, sub-agent spawning—the "Claude Code-style" harness as a reusable library. | ✅ | Capability (planning, files, sub-agents) |
| 2 | [**pydantic-ai**](https://github.com/pydantic/pydantic-ai) | Type-safe Python agents with Pydantic I/O; multi-provider, MCP, Logfire observability, and human-in-the-loop. | ✅ | Capability (type-safe, MCP, Logfire) |
| 3 | [**open-harness**](https://github.com/MaxGfeller/open-harness) | TypeScript Agent class on Vercel AI SDK; streaming events, filesystem/bash tools, MCP, and subagent delegation. | ✅ | Capability (streaming, tools, subagents) |
| 4 | [**vercel/ai**](https://github.com/vercel/ai) | React and Node SDK for streaming, tool calls, and agent-style UIs; provider-agnostic. | ✅ | Mid (React/Node SDK, provider-agnostic) |
| 5 | [**smolagents**](https://github.com/huggingface/smolagents) | Code-as-action agents: model outputs Python executed in sandbox (E2B, Modal, etc.); ~1k LOC core. | ✅ | Mid (code-as-action, ~1k LOC) |
| 6 | [**strands-agents**](https://github.com/strands-agents/sdk-python) | Model-driven Python SDK; decorators for tools, native MCP, multi-agent; "minimal code" without sacrificing provider choice. | ✅ | Mid (decorators, MCP, minimal code) |
| 7 | [**openai-agents-js**](https://github.com/openai/openai-agents-js) | Official OpenAI Agents SDK for Node/TS: handoffs, guardrails, voice; the JS counterpart to openai-agents-python. | ✅ | Capability (handoffs, guardrails, voice) |
| 8 | [**LiteLLM**](https://github.com/BerriAI/litellm) | One interface to 100+ LLMs; routing, caching, budgets. Not an agent framework—the pipe every agent framework uses. | ✅ | Simple (LLM pipe only) |
| 9 | [**Composio**](https://github.com/ComposioHQ/composio) | 1,000+ toolkits with auth, tool search, and a sandboxed workbench—drop-in tool layer so agents stop reinventing OAuth + integrations. Python and TypeScript. | ✅ | Capability (1k+ tools, auth, search) |
| 10 | [**Mem0**](https://github.com/mem0ai/mem0) | Universal memory layer for AI agents: stores user/org/session memory, retrieves on demand. Apache-2.0; the de-facto memory primitive paired with most harnesses in 2026. | ✅ | Capability (memory layer, multi-platform) |
| 11 | [**Cloudflare Agents**](https://github.com/cloudflare/agents) | Persistent, stateful agents on Durable Objects: state, websockets, scheduling, and AI chat baked in. The serverless answer to "where does the agent live?" | ✅ | Capability (Durable Objects, stateful) |
| 12 | [**E2B**](https://github.com/e2b-dev/E2B) | Firecracker sandboxes for executing agent-generated code; the hosted isolation layer many tool-calling demos use instead of running arbitrary LLM output on your laptop. | ✅ | Mid (sandbox API, code execution) |
| 13 | [**Daytona**](https://github.com/daytonaio/daytona) | Elastic dev environments for AI-generated code: workspaces, Git, previews—infra harness between "the model wrote a patch" and "it ran in a real machine." | ✅ | Mid (dev env API, isolation) |
| 14 | [**Community-curated agent lists**](https://github.com/brandonhimpfen/awesome-ai-agents) | Broader directories: e.g. [brandonhimpfen/awesome-ai-agents](https://github.com/brandonhimpfen/awesome-ai-agents), [axioma-ai-labs/awesome-ai-agent-frameworks](https://github.com/axioma-ai-labs/awesome-ai-agent-frameworks), [mb-mal/awesome-ai-agents-frameworks](https://github.com/mb-mal/awesome-ai-agents-frameworks)—differ by scope and update cadence. | ❓ | Simple (curated lists) |

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
