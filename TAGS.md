<!-- markdownlint-disable -->
# Tags — cross-reference

_Auto-generated from `scripts/generate.py`. 131 projects across 22 canonical tags. Edit projects in `generate.py` (not here) and rerun the script._

Tag chips appear next to each project in [README.md](README.md). This page lists every tag once with the projects that carry it, grouped by category and sorted by GitHub stars within each category.

## All tags

[`mcp`](#mcp) (28) · [`memory`](#memory) (22) · [`multi-agent`](#multi-agent) (21) · [`evals`](#evals) (17) · [`voice`](#voice) (2) · [`vision`](#vision) (3) · [`browser`](#browser) (6) · [`sandbox`](#sandbox) (20) · [`low-code`](#low-code) (4) · [`rag`](#rag) (5) · [`tool-discovery`](#tool-discovery) (5) · [`training`](#training) (5) · [`workflow`](#workflow) (8) · [`typed`](#typed) (3) · [`local`](#local) (2) · [`provider-agnostic`](#provider-agnostic) (11) · [`cli`](#cli) (16) · [`ide`](#ide) (9) · [`tui`](#tui) (4) · [`rust`](#rust) (5) · [`python`](#python) (67) · [`typescript`](#typescript) (35)

---

## `mcp`

**Progressive disclosure harnesses**

- [ToolRAG](https://github.com/antl3x/ToolRAG) — ⭐29 — Semantic tool retrieval for LLMs; serves only the tools the user query demands (MCP-compatible), unlimited tool sets with zero context penalty.

**Coding agent products (IDEs, CLIs, full suites)**

- [opencode](https://github.com/anomalyco/opencode) — ⭐185k — Open-source terminal coding agent (formerly `sst/opencode`; transferred to anomalyco). The **harness** is a multi-provider tool-call loop (Claude, OpenAI, Gemini, local) with strong plugin and MCP support; the TUI is the shell. 100% OSS, very actively shipped.
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) — ⭐106k — Google's first-party terminal agent for Gemini. The **harness** is the plugin/MCP tool-call loop; the terminal is the shell—Google's parallel to Claude Code / Codex, not just an API.
- [goose](https://github.com/aaif-goose/goose) — ⭐51.1k — Block-originated Rust agent, now stewarded by the Linux Foundation's Agentic AI Foundation (`aaif-goose/goose`). The **harness** is the MCP/ACP extension model with recipes and provider choice; there's no fixed UI slot—you bolt it into whatever shell you use.
- [Roo Code](https://github.com/RooCodeInc/Roo-Code) — ⭐24.3k — VS Code/Cursor extension in the Cline lineage. The **harness** is the approval-gated agent with custom modes and a strong MCP story; the IDE is the UI. Popular community fork when you want that workflow without the upstream extension.
- [jcode](https://github.com/1jehuang/jcode) — ⭐8.3k — Rust terminal coding agent that bills itself outright as a "Coding Agent Harness": a TUI/CLI shell over a multi-provider (Claude, OpenAI) tool-call loop with MCP support.
- [claw-code-agent](https://github.com/HarnessLab/claw-code-agent) — ⭐528 — Python reimplementation of the Claude Code agent architecture with zero external dependencies; interactive chat, streaming, plugin runtime, nested agent delegation, cost tracking, MCP transport—portable harness without the Rust/TS toolchain.

**Coding harness configs and SDKs**

- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python) — ⭐7.6k — Official Anthropic SDK (Python + [TypeScript](https://github.com/anthropics/claude-agent-sdk-typescript), [demos](https://github.com/anthropics/claude-agent-sdk-demos), [quickstarts](https://github.com/anthropics/claude-quickstarts)): built-in tools, MCP, long-running coding agents with session bridging.

**Personal agent runtimes**

- [Talon](https://github.com/dylanneve1/talon) — ⭐64 — Multi-platform personal agent living in Telegram, Discord, Teams, and the terminal. The **harness** is a pluggable-backend loop (Claude, Kilo, OpenCode, Codex, OpenAI Agents) with full MCP tool access and persistent background agents (Goals, Heartbeat, Dream); the chat apps are shells.

**Frameworks**

- [browser-use](https://github.com/browser-use/browser-use) — ⭐104k — Python layer over Playwright: natural-language goals become browser actions—web-agent loop without hand-rolling MCP or a custom driver for every site.
- [Bee Agent Framework](https://github.com/i-am-bee/beeai-framework) — ⭐3.3k — Python + TypeScript, LF AI–backed; MCP/ACP, workflows, Requirement Agent; the one that pushes "production multi-agent" without LangChain.
- [CUGA](https://github.com/cuga-project/cuga-agent) — ⭐859 — Open-source generalist agent **harness** for the enterprise: OpenAPI/MCP integrations, composable reasoning modes, and policy/guardrail-aware execution for complex web and API task completion.

**Plugins, MCPs, CLI tools**

- [MCP Servers](https://github.com/modelcontextprotocol/servers) — ⭐88.4k — The official reference collection of Model Context Protocol servers (filesystem, git, fetch, memory, time, and more)—the canonical, vetted toolset agents connect to, and the pattern every other MCP server is measured against.
- [Context7](https://github.com/upstash/context7) — ⭐59k — MCP server that injects up-to-date, version-specific library docs into an agent's context on demand; kills the stale-training-data hallucinations that plague codegen.
- [aider](https://github.com/Aider-AI/aider) — ⭐47.3k — Git-aware CLI pair programmer; edits in-repo, supports multiple models and MCP so agents see version control and tools.
- [Playwright MCP](https://github.com/microsoft/playwright-mcp) — ⭐35k — Playwright's official MCP server: structured browser control (navigate, click, fill, extract) via the accessibility tree rather than screenshots, so web tasks stay fast and deterministic.
- [github-mcp-server](https://github.com/github/github-mcp-server) — ⭐31.4k — GitHub's official MCP server (Go): repos, issues, PRs, code search, Actions. Replaces the older community `cyanheads/github-mcp-server` as the canonical way to give agents GitHub access.
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) — ⭐23.6k — Official SDK to build and consume MCP servers/clients in Python; stdio and SSE transports.
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) — ⭐12.8k — Official MCP implementation for Node/TS; reference for the protocol.
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector) — ⭐10.3k — GUI to test and debug MCP servers; inspect tools, resources, and prompts.
- [MCP Registry](https://github.com/modelcontextprotocol/registry) — ⭐7k — Official, community-driven registry for MCP servers—the "app store" MCP clients use to discover servers. Maintained by Anthropic + ecosystem maintainers; v0.1 API frozen, production-grade.
- [Docker MCP Gateway](https://github.com/docker/mcp-gateway) — ⭐1.5k — Docker's official MCP CLI plugin / gateway; container-aware MCP tooling from Docker (replaces deprecated `docker/mcp-servers` path).
- [puppeteer-real-browser-mcp](https://github.com/withLinda/puppeteer-real-browser-mcp-server) — ⭐24 — Puppeteer MCP with real-browser and anti-detection; for agents that need to drive sites that block headless.
- [Better-OpenCodeMCP](https://github.com/ajhcs/Better-OpenCodeMCP) — ⭐8 — MCP server for OpenCode/Crush: async task execution, model bridging (e.g. Claude→Gemini), process pooling.

**Evaluation and benchmarking harnesses**

- [agent-qa](https://github.com/vostride/agent-qa) — ⭐157 — Self-improving QA **harness** for web and mobile apps: natural-language tests, memory-backed self-healing, dashboard/CLI, MCP and skills support, plus sandboxed hooks for production regression checks.

**Libraries and SDKs**

- [pydantic-ai](https://github.com/pydantic/pydantic-ai) — ⭐18.4k — Type-safe Python agents with Pydantic I/O; multi-provider, MCP, Logfire observability, and human-in-the-loop.
- [strands-agents](https://github.com/strands-agents/harness-sdk) — ⭐6.5k — Model-driven Python SDK; decorators for tools, native MCP, multi-agent; "minimal code" without sacrificing provider choice.
- [open-harness](https://github.com/MaxGfeller/open-harness) — ⭐585 — TypeScript Agent class on Vercel AI SDK; streaming events, filesystem/bash tools, MCP, and subagent delegation.

---

## `memory`

**Coding agent products (IDEs, CLIs, full suites)**

- [OpenHands](https://github.com/OpenHands/OpenHands) — ⭐80.5k — Dockerized software-engineering agent. The **harness** is the bash/editor/browser toolset with micro-agents and event-stream session bridging; Docker is the sandbox. Main OSS choice for teams self-hosting autonomous repo work.
- [crush](https://github.com/charmbracelet/crush) — ⭐26.5k — Charm's terminal coding agent (Charm's fork of the original OpenCode). The **harness** is the tool-calling loop with session persistence; the Bubble Tea TUI is the shell.

**Coding harness configs and SDKs**

- [superpowers](https://github.com/obra/superpowers) — ⭐253k — Performance-oriented harness pack for Claude Code, Codex, OpenCode, Cursor: skills, instincts, memory, security, research-first workflows. Treats harness engineering itself as the performance lever.
- [SWE-agent](https://github.com/SWE-agent/SWE-agent) — ⭐19.8k — LM-driven harness built for SWE-bench: edit state, command execution, and issue-focused loop—the reference agent stack next to the benchmark itself.
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python) — ⭐7.6k — Official Anthropic SDK (Python + [TypeScript](https://github.com/anthropics/claude-agent-sdk-typescript), [demos](https://github.com/anthropics/claude-agent-sdk-demos), [quickstarts](https://github.com/anthropics/claude-quickstarts)): built-in tools, MCP, long-running coding agents with session bridging.
- [AutoHarness](https://github.com/aiming-lab/AutoHarness) — ⭐347 — Lightweight governance harness: wraps any LLM client in ~2 lines for automated harness engineering—6–14 step pipeline, YAML constitution, risk-pattern matching, session persistence with cost tracking, multi-agent profiles.

**Personal agent runtimes**

- [Hermes](https://github.com/NousResearch/hermes-agent) — ⭐214k — Nous Research's self-improving agent: a learning loop turns experience into reusable skills, builds a persistent user model across sessions, and checkpoints state to disk with rollback; lean enough for a $5 VPS, driven from chat, and model-agnostic (Nous Portal, OpenRouter, OpenAI, or any endpoint).
- [Eliza](https://github.com/elizaOS/eliza) — ⭐18.7k — Open "agentic operating system" (elizaOS): persistent multi-agent runtime with character files, a plugin ecosystem, and social/platform integrations — the harness behind a large share of autonomous social agents.
- [Agent Zero](https://github.com/agent0ai/agent-zero) — ⭐18.4k — Organic, prompt-defined personal agent framework: hierarchical sub-agents, persistent memory, browser and code tools, and self-modifying behavior; runs in Docker with a web UI.
- [OpenHarness (HKUDS)](https://github.com/HKUDS/OpenHarness) — ⭐14.7k — Open agent harness with a built-in personal agent ("Ohmo") that runs across Feishu, Slack, Telegram, and Discord; core tool-use, skills, memory, multi-agent coordination with auto-compaction for multi-day sessions.
- [Talon](https://github.com/dylanneve1/talon) — ⭐64 — Multi-platform personal agent living in Telegram, Discord, Teams, and the terminal. The **harness** is a pluggable-backend loop (Claude, Kilo, OpenCode, Codex, OpenAI Agents) with full MCP tool access and persistent background agents (Goals, Heartbeat, Dream); the chat apps are shells.

**Frameworks**

- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) — ⭐185k — The original autonomous loop: goal in, agent iterates with tools and memory; Forge is the dev framework, Benchmark the eval harness.
- [agno](https://github.com/agno-agi/agno) — ⭐41.1k — Python agents with memory, knowledge bases, tools, and structured outputs; continues the PhiData-era product line under the Agno name—production apps, evals, and pipelines.
- [letta](https://github.com/letta-ai/letta) — ⭐23.8k — Python agent runtime with tool use and control flow; lean API; stateful agents with long-horizon memory.

**Plugins, MCPs, CLI tools**

- [MCP Servers](https://github.com/modelcontextprotocol/servers) — ⭐88.4k — The official reference collection of Model Context Protocol servers (filesystem, git, fetch, memory, time, and more)—the canonical, vetted toolset agents connect to, and the pattern every other MCP server is measured against.
- [agentlog](https://github.com/RyanAlberts/agentlog) — ⭐1 — Persistent decision memory for any project: `remember`, `recall`, `reflect`. Single-file Python CLI that stores decisions as JSONL and uses Claude or Gemini to retrieve and synthesize patterns—Karpathy's LLM Wiki concept as a CLI.

**Memory and state**

- [claude-mem](https://github.com/thedotmack/claude-mem) — ⭐86.9k — Claude Code plugin that captures everything an agent does during a session, AI-compresses it (via claude-agent-sdk), and injects the relevant context into future sessions—session-to-session memory as a drop-in.
- [Mem0](https://github.com/mem0ai/mem0) — ⭐60.7k — Universal memory layer for AI agents: stores user/org/session memory, retrieves on demand. Apache-2.0; the de-facto memory primitive paired with most harnesses in 2026.
- [cognee](https://github.com/topoteretes/cognee) — ⭐27.6k — Open-source memory layer for agents: an extract–cognify–load pipeline that turns your data into a queryable knowledge graph plus vector store, so agents recall facts and relationships across sessions instead of re-reading context.

**Evaluation and benchmarking harnesses**

- [agent-qa](https://github.com/vostride/agent-qa) — ⭐157 — Self-improving QA **harness** for web and mobile apps: natural-language tests, memory-backed self-healing, dashboard/CLI, MCP and skills support, plus sandboxed hooks for production regression checks.
- [letta-evals](https://github.com/letta-ai/letta-evals) — ⭐77 — Eval harness for stateful Letta agents; configurable suites and grading (LLM or rule-based) so you can measure what you ship.

**Libraries and SDKs**

- [Cloudflare Agents](https://github.com/cloudflare/agents) — ⭐5.2k — Persistent, stateful agents on Durable Objects: state, websockets, scheduling, and AI chat baked in. The serverless answer to "where does the agent live?"

---

## `multi-agent`

**Coding agent products (IDEs, CLIs, full suites)**

- [Proliferate](https://github.com/proliferate-ai/proliferate) — ⭐151 — Open-source AI IDE for Claude Code, Codex, OpenCode, and more. The **harness** contribution is the workspace/session orchestration layer: run multiple coding agents in parallel, locally or in the cloud, with isolated workspaces, reusable workflows, and shared team context.

**Coding harness configs and SDKs**

- [wshobson/agents](https://github.com/wshobson/agents) — ⭐37.8k — Cross-harness marketplace of drop-in subagents and skills for Claude Code, Codex CLI, Cursor, OpenCode, and Copilot; specialized, production-ready agent definitions you install rather than hand-write.
- [AutoHarness](https://github.com/aiming-lab/AutoHarness) — ⭐347 — Lightweight governance harness: wraps any LLM client in ~2 lines for automated harness engineering—6–14 step pipeline, YAML constitution, risk-pattern matching, session persistence with cost tracking, multi-agent profiles.

**Personal agent runtimes**

- [OpenClaw](https://github.com/openclaw/openclaw) — ⭐383k — Self-hosted, always-on personal agent (formerly Clawdbot/Moltbot): a gateway + event-loop runtime that treats messages, heartbeats, crons, and webhooks as one input queue, persists state to local files, and lives in your chat apps (WhatsApp, Telegram, Slack, Discord). 13,700+ community skills; the fastest-growing repo in GitHub history.
- [Eliza](https://github.com/elizaOS/eliza) — ⭐18.7k — Open "agentic operating system" (elizaOS): persistent multi-agent runtime with character files, a plugin ecosystem, and social/platform integrations — the harness behind a large share of autonomous social agents.
- [Agent Zero](https://github.com/agent0ai/agent-zero) — ⭐18.4k — Organic, prompt-defined personal agent framework: hierarchical sub-agents, persistent memory, browser and code tools, and self-modifying behavior; runs in Docker with a web UI.
- [OpenHarness (HKUDS)](https://github.com/HKUDS/OpenHarness) — ⭐14.7k — Open agent harness with a built-in personal agent ("Ohmo") that runs across Feishu, Slack, Telegram, and Discord; core tool-use, skills, memory, multi-agent coordination with auto-compaction for multi-day sessions.

**Frameworks**

- [agent-squad](https://github.com/2FastLabs/agent-squad) — ⭐7.7k — AWS-originated orchestrator (now under 2FastLabs): intent classification, streaming, SupervisorAgent; "agent-as-tools" so one agent delegates to a squad.
- [AgentVerse](https://github.com/OpenBMB/AgentVerse) — ⭐5.1k — Task-solving and simulation envs for multi-LLM agents; deploy many agents in custom environments without building infra from scratch.
- [Bee Agent Framework](https://github.com/i-am-bee/beeai-framework) — ⭐3.3k — Python + TypeScript, LF AI–backed; MCP/ACP, workflows, Requirement Agent; the one that pushes "production multi-agent" without LangChain.
- [SuperAgentX](https://github.com/superagentxai/superagentx) — ⭐200 — Lightweight multi-agent orchestrator with an AGI-angle; minimal surface, docs-first, for teams that want orchestration without the kitchen sink.

**Multi-agent and orchestration**

- [MetaGPT](https://github.com/FoundationAgents/MetaGPT) — ⭐69.3k — The "AI software company" multi-agent framework: role-played PM, architect, and engineer agents turn a one-line requirement into specs, designs, and code along an SOP assembly line. The landmark of the genre; development pace has slowed in 2026.
- [autogen](https://github.com/microsoft/autogen) — ⭐59.7k — Conversable agents and group chats; code execution and human-in-the-loop; Microsoft origin, AG2 ecosystem.
- [OpenManus](https://github.com/FoundationAgents/OpenManus) — ⭐57.2k — Open, invite-free general agent from the MetaGPT team: planning plus tool use over a multi-agent loop, aimed at reproducing Manus-style autonomous task completion on your own keys.
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) — ⭐12.1k — Microsoft's convergence of AutoGen and Semantic Kernel: build, orchestrate, and deploy agents and multi-agent workflows in Python and .NET, with graph-based workflows and checkpointing — the designated successor harness for both lines.
- [PraisonAI](https://github.com/MervinPraison/PraisonAI) — ⭐8.4k — Autonomous multi-agent teams with a single entry point; emphasis on minimal config.

**Research and task-specific harnesses**

- [gpt-researcher](https://github.com/assafelovic/gpt-researcher) — ⭐28.3k — Autonomous deep-research agent: web + local sources, citation-grounded reports, multi-agent and deep-research modes. The reference open-source research harness.

**Libraries and SDKs**

- [deepagents](https://github.com/langchain-ai/deepagents) — ⭐26.1k — LangChain's Python+TypeScript agent harness on top of LangGraph: planning tool, virtual filesystem, shell sandbox, sub-agent spawning—the "Claude Code-style" harness as a reusable library.
- [strands-agents](https://github.com/strands-agents/harness-sdk) — ⭐6.5k — Model-driven Python SDK; decorators for tools, native MCP, multi-agent; "minimal code" without sacrificing provider choice.
- [openai-agents-js](https://github.com/openai/openai-agents-js) — ⭐3.4k — Official OpenAI Agents SDK for Node/TS: handoffs, guardrails, voice; the JS counterpart to openai-agents-python.
- [open-harness](https://github.com/MaxGfeller/open-harness) — ⭐585 — TypeScript Agent class on Vercel AI SDK; streaming events, filesystem/bash tools, MCP, and subagent delegation.

---

## `evals`

**Coding harness configs and SDKs**

- [SWE-agent](https://github.com/SWE-agent/SWE-agent) — ⭐19.8k — LM-driven harness built for SWE-bench: edit state, command execution, and issue-focused loop—the reference agent stack next to the benchmark itself.
- [agents-cli](https://github.com/google/agents-cli) — ⭐5.1k — Google's official CLI and skill pack that layers agent-creation, evaluation, and deployment skills on top of whatever coding assistant you already run, rather than shipping its own agent loop—the **harness** as a config/skills add-on, not a new runtime.
- [pmstack](https://github.com/RyanAlberts/pmstack) — ⭐5 — Claude Code config for AI product managers: CLAUDE.md plus skills for competitive analysis, PRD-from-signal, metric frameworks, stakeholder briefs, and agent eval design. "GStack for PMs."

**Frameworks**

- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) — ⭐185k — The original autonomous loop: goal in, agent iterates with tools and memory; Forge is the dev framework, Benchmark the eval harness.
- [agno](https://github.com/agno-agi/agno) — ⭐41.1k — Python agents with memory, knowledge bases, tools, and structured outputs; continues the PhiData-era product line under the Agno name—production apps, evals, and pipelines.
- [Google ADK](https://github.com/google/adk-python) — ⭐20.6k — Google's official Agent Development Kit: code-first Python toolkit for building, evaluating, and deploying agents. Optimized for Gemini but model-agnostic; deploys to Cloud Run / Vertex AI; ships a dev UI with eval and a code-execution sandbox.

**Evaluation and benchmarking harnesses**

- [Agent Lightning](https://github.com/microsoft/agent-lightning) — ⭐17.4k — Microsoft's training-oriented harness: optimization loops for agent behavior—when you need to improve policies over rollouts, not only score a fixed prompt.
- [SWE-bench](https://github.com/SWE-bench/SWE-bench) — ⭐5.4k — LMs resolve real GitHub issues; Docker harness, instance IDs; standard for code-agent evals.
- [AgentBench](https://github.com/THUDM/AgentBench) — ⭐3.6k — ICLR'24 benchmark: agents across AlfWorld, DB, knowledge graphs, OS, webshop; Docker Compose, function-calling interface.
- [inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai) — ⭐2.3k — Inspect AI core: composable eval tasks, sandboxes, scorers, and multi-model runs; the framework behind inspect_evals, not just the task bundle.
- [WebVoyager](https://github.com/MinorJerry/WebVoyager) — ⭐1.1k — End-to-end web agent with LMMs: screenshots + actions on real sites; benchmark on 15 sites, GPT-4V for automatic eval.
- [SWE-Gym](https://github.com/SWE-Gym/SWE-Gym) — ⭐701 — Training and evaluation for SWE agents and verifiers (ICML 2025).
- [inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals) — ⭐578 — UK AISI/Arcadia/Vector: GAIA and other evals in Inspect AI; level 1–3, sandboxed, tool-calling solvers.
- [arc-agi-benchmarking](https://github.com/arcprize/arc-agi-benchmarking) — ⭐351 — Runner for ARC-AGI: multi-provider (OpenAI, Anthropic, Gemini, etc.), rate limits, retries, and scoring.
- [AgencyBench](https://github.com/GAIR-NLP/AgencyBench) — ⭐89 — Long-horizon agent benchmark: 32 scenarios, 138 tasks, ~1M tokens and ~90 tool calls; Docker sandbox and rubric-based + LLM judges.

**Observability and eval-ops**

- [Langfuse](https://github.com/langfuse/langfuse) — ⭐31k — Open-source LLM engineering platform: full-trace observability, online and offline evals, prompt management, and cost metrics for agent runs in production—the monitoring layer most harnesses lack out of the box.
- [MLflow](https://github.com/mlflow/mlflow) — ⭐27k — Mature ML platform now covering GenAI: MLflow Tracing captures every agent step, tool call, and token, with built-in LLM evals and prompt versioning—observability for teams already standardized on MLflow.

---

## `voice`

**Frameworks**

- [rasa](https://github.com/RasaHQ/rasa) — ⭐21.2k — Conversational AI stack (NLU, dialogue, actions); long-standing OSS choice for chat and voice bots.

**Libraries and SDKs**

- [openai-agents-js](https://github.com/openai/openai-agents-js) — ⭐3.4k — Official OpenAI Agents SDK for Node/TS: handoffs, guardrails, voice; the JS counterpart to openai-agents-python.

---

## `vision`

**Frameworks**

- [R2R](https://github.com/SciPhi-AI/R2R) — ⭐7.9k — RAG-first: hybrid search, knowledge graphs, multimodal; the framework for "production RAG" when you care more about retrieval than chat UI.

**Plugins, MCPs, CLI tools**

- [Playwright MCP](https://github.com/microsoft/playwright-mcp) — ⭐35k — Playwright's official MCP server: structured browser control (navigate, click, fill, extract) via the accessibility tree rather than screenshots, so web tasks stay fast and deterministic.

**Evaluation and benchmarking harnesses**

- [WebVoyager](https://github.com/MinorJerry/WebVoyager) — ⭐1.1k — End-to-end web agent with LMMs: screenshots + actions on real sites; benchmark on 15 sites, GPT-4V for automatic eval.

---

## `browser`

**Coding agent products (IDEs, CLIs, full suites)**

- [OpenHands](https://github.com/OpenHands/OpenHands) — ⭐80.5k — Dockerized software-engineering agent. The **harness** is the bash/editor/browser toolset with micro-agents and event-stream session bridging; Docker is the sandbox. Main OSS choice for teams self-hosting autonomous repo work.
- [oh-my-pi](https://github.com/can1357/oh-my-pi) — ⭐17.4k — Terminal coding agent (fork of Pi) that wires the IDE into the **harness**: hash-anchored edits, a 32-tool loop tuned per-model, LSP rename/references/diagnostics on every write, a real DAP debugger (lldb/dlv/debugpy), long-lived Python + Bun execution kernels that call back into the agent's tools, browser control, and 40+ providers (Claude/OpenAI/Gemini/local). ~55k-line Rust core.

**Personal agent runtimes**

- [Agent Zero](https://github.com/agent0ai/agent-zero) — ⭐18.4k — Organic, prompt-defined personal agent framework: hierarchical sub-agents, persistent memory, browser and code tools, and self-modifying behavior; runs in Docker with a web UI.

**Frameworks**

- [browser-use](https://github.com/browser-use/browser-use) — ⭐104k — Python layer over Playwright: natural-language goals become browser actions—web-agent loop without hand-rolling MCP or a custom driver for every site.

**Plugins, MCPs, CLI tools**

- [Playwright MCP](https://github.com/microsoft/playwright-mcp) — ⭐35k — Playwright's official MCP server: structured browser control (navigate, click, fill, extract) via the accessibility tree rather than screenshots, so web tasks stay fast and deterministic.
- [puppeteer-real-browser-mcp](https://github.com/withLinda/puppeteer-real-browser-mcp-server) — ⭐24 — Puppeteer MCP with real-browser and anti-detection; for agents that need to drive sites that block headless.

---

## `sandbox`

**Coding agent products (IDEs, CLIs, full suites)**

- [Codex](https://github.com/openai/codex) — ⭐97.3k — OpenAI's terminal coding agent. The **harness** is the sandboxed tool-call loop with multi-provider support; the CLI is the shell. Reference implementation for "official CLI that ships code."
- [OpenHands](https://github.com/OpenHands/OpenHands) — ⭐80.5k — Dockerized software-engineering agent. The **harness** is the bash/editor/browser toolset with micro-agents and event-stream session bridging; Docker is the sandbox. Main OSS choice for teams self-hosting autonomous repo work.
- [AgentBox](https://github.com/madarco/agentbox) — ⭐247 — Runs multiple coding agents in parallel, each in its own sandboxed VM, locally or in the cloud, from one command. The **harness** contribution is the VM-per-agent isolation and fleet fan-out layer; whichever agent runs inside owns the loop.
- [Proliferate](https://github.com/proliferate-ai/proliferate) — ⭐151 — Open-source AI IDE for Claude Code, Codex, OpenCode, and more. The **harness** contribution is the workspace/session orchestration layer: run multiple coding agents in parallel, locally or in the cloud, with isolated workspaces, reusable workflows, and shared team context.

**Personal agent runtimes**

- [Agent Zero](https://github.com/agent0ai/agent-zero) — ⭐18.4k — Organic, prompt-defined personal agent framework: hierarchical sub-agents, persistent memory, browser and code tools, and self-modifying behavior; runs in Docker with a web UI.
- [AIlice](https://github.com/myshell-ai/AIlice) — ⭐1.4k — Fully autonomous general-purpose agent; one binary, Docker-ready, for when you want "set goal and walk away" without a framework.

**Frameworks**

- [Google ADK](https://github.com/google/adk-python) — ⭐20.6k — Google's official Agent Development Kit: code-first Python toolkit for building, evaluating, and deploying agents. Optimized for Gemini but model-agnostic; deploys to Cloud Run / Vertex AI; ships a dev UI with eval and a code-execution sandbox.

**Plugins, MCPs, CLI tools**

- [Docker MCP Gateway](https://github.com/docker/mcp-gateway) — ⭐1.5k — Docker's official MCP CLI plugin / gateway; container-aware MCP tooling from Docker (replaces deprecated `docker/mcp-servers` path).

**Evaluation and benchmarking harnesses**

- [SWE-bench](https://github.com/SWE-bench/SWE-bench) — ⭐5.4k — LMs resolve real GitHub issues; Docker harness, instance IDs; standard for code-agent evals.
- [AgentBench](https://github.com/THUDM/AgentBench) — ⭐3.6k — ICLR'24 benchmark: agents across AlfWorld, DB, knowledge graphs, OS, webshop; Docker Compose, function-calling interface.
- [inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai) — ⭐2.3k — Inspect AI core: composable eval tasks, sandboxes, scorers, and multi-model runs; the framework behind inspect_evals, not just the task bundle.
- [inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals) — ⭐578 — UK AISI/Arcadia/Vector: GAIA and other evals in Inspect AI; level 1–3, sandboxed, tool-calling solvers.
- [agent-qa](https://github.com/vostride/agent-qa) — ⭐157 — Self-improving QA **harness** for web and mobile apps: natural-language tests, memory-backed self-healing, dashboard/CLI, MCP and skills support, plus sandboxed hooks for production regression checks.
- [AgencyBench](https://github.com/GAIR-NLP/AgencyBench) — ⭐89 — Long-horizon agent benchmark: 32 scenarios, 138 tasks, ~1M tokens and ~90 tool calls; Docker sandbox and rubric-based + LLM judges.
- [SUPER](https://github.com/allenai/super-benchmark) — ⭐53 — Agents that set up and run ML/NLP from GitHub repos; 45 expert problems, 152 masked tasks, 602 AutoGen tasks; Docker-based.

**Libraries and SDKs**

- [Daytona](https://github.com/daytonaio/daytona) — ⭐72.2k — Elastic dev environments for AI-generated code: workspaces, Git, previews—infra harness between "the model wrote a patch" and "it ran in a real machine."
- [Composio](https://github.com/ComposioHQ/composio) — ⭐29.2k — 1,000+ toolkits with auth, tool search, and a sandboxed workbench—drop-in tool layer so agents stop reinventing OAuth + integrations. Python and TypeScript.
- [smolagents](https://github.com/huggingface/smolagents) — ⭐28.3k — Code-as-action agents: model outputs Python executed in sandbox (E2B, Modal, etc.); ~1k LOC core.
- [deepagents](https://github.com/langchain-ai/deepagents) — ⭐26.1k — LangChain's Python+TypeScript agent harness on top of LangGraph: planning tool, virtual filesystem, shell sandbox, sub-agent spawning—the "Claude Code-style" harness as a reusable library.
- [E2B](https://github.com/e2b-dev/E2B) — ⭐12.9k — Firecracker sandboxes for executing agent-generated code; the hosted isolation layer many tool-calling demos use instead of running arbitrary LLM output on your laptop.

---

## `low-code`

**Frameworks**

- [langflow](https://github.com/langflow-ai/langflow) — ⭐152k — Low-code UI to build and deploy LangChain/LangGraph flows; visual DAG editor and one-click run.
- [Dify](https://github.com/langgenius/dify) — ⭐149k — One-stop LLM app platform: visual workflows, RAG pipeline, 50+ tools, model management; "ship from prototype to prod" in a single UI.
- [Flowise](https://github.com/FlowiseAI/Flowise) — ⭐54.5k — Drag-and-drop LangChain UI; deploy flows without code. The low-code sibling to Langflow, with a different component and hosting story.
- [botpress](https://github.com/botpress/botpress) — ⭐14.8k — Visual bot builder and runtime; multi-channel, open-source alternative to commercial bot platforms.

---

## `rag`

**Frameworks**

- [Dify](https://github.com/langgenius/dify) — ⭐149k — One-stop LLM app platform: visual workflows, RAG pipeline, 50+ tools, model management; "ship from prototype to prod" in a single UI.
- [llama-index](https://github.com/run-llama/llama_index) — ⭐50.8k — Data-centric: indexing, RAG, and query engines; agent abstractions sit on top of your data pipelines.
- [R2R](https://github.com/SciPhi-AI/R2R) — ⭐7.9k — RAG-first: hybrid search, knowledge graphs, multimodal; the framework for "production RAG" when you care more about retrieval than chat UI.

**Memory and state**

- [cognee](https://github.com/topoteretes/cognee) — ⭐27.6k — Open-source memory layer for agents: an extract–cognify–load pipeline that turns your data into a queryable knowledge graph plus vector store, so agents recall facts and relationships across sessions instead of re-reading context.

**Evaluation and benchmarking harnesses**

- [AgentBench](https://github.com/THUDM/AgentBench) — ⭐3.6k — ICLR'24 benchmark: agents across AlfWorld, DB, knowledge graphs, OS, webshop; Docker Compose, function-calling interface.

---

## `tool-discovery`

**Progressive disclosure harnesses**

- [langgraph-bigtool](https://github.com/langchain-ai/langgraph-bigtool) — ⭐545 — Build LangGraph agents with large tool sets; retrieval and on-demand tool loading so agents scale beyond context without stuffing every schema upfront.
- [MCP-Zero](https://github.com/xfey/MCP-Zero) — ⭐490 — Active tool discovery for autonomous agents: model requests tools by requirement; hierarchical semantic routing over 308 servers / 2,797 tools with ~98% token reduction (APIBank).
- [ToolGen](https://github.com/Reason-Wang/ToolGen) — ⭐182 — ICLR 2025: unified tool retrieval and calling via generation; 47k+ tools without context stuffing—retrieval and invocation in one generative step.
- [ToolRAG](https://github.com/antl3x/ToolRAG) — ⭐29 — Semantic tool retrieval for LLMs; serves only the tools the user query demands (MCP-compatible), unlimited tool sets with zero context penalty.

**Libraries and SDKs**

- [Composio](https://github.com/ComposioHQ/composio) — ⭐29.2k — 1,000+ toolkits with auth, tool search, and a sandboxed workbench—drop-in tool layer so agents stop reinventing OAuth + integrations. Python and TypeScript.

---

## `training`

**Multi-agent and orchestration**

- [AgentRL](https://github.com/THUDM/AgentRL) — ⭐314 — Multitask, multiturn RL for LLM agents; Ray-based scaling, rollout/actor workers—for teams that want to train agents, not just run them.

**Plugins, MCPs, CLI tools**

- [Context7](https://github.com/upstash/context7) — ⭐59k — MCP server that injects up-to-date, version-specific library docs into an agent's context on demand; kills the stale-training-data hallucinations that plague codegen.

**Evaluation and benchmarking harnesses**

- [Agent Lightning](https://github.com/microsoft/agent-lightning) — ⭐17.4k — Microsoft's training-oriented harness: optimization loops for agent behavior—when you need to improve policies over rollouts, not only score a fixed prompt.
- [SWE-Gym](https://github.com/SWE-Gym/SWE-Gym) — ⭐701 — Training and evaluation for SWE agents and verifiers (ICML 2025).
- [swe-smith](https://github.com/SWE-bench/SWE-smith) — ⭐697 — Data generation for SWE agents; 50k+ instances across 128 repos; used for SWE-agent-LM training.

---

## `workflow`

**Coding agent products (IDEs, CLIs, full suites)**

- [Roo Code](https://github.com/RooCodeInc/Roo-Code) — ⭐24.3k — VS Code/Cursor extension in the Cline lineage. The **harness** is the approval-gated agent with custom modes and a strong MCP story; the IDE is the UI. Popular community fork when you want that workflow without the upstream extension.

**Coding harness configs and SDKs**

- [RepoMaster](https://github.com/QuantaAlpha/RepoMaster) — ⭐533 — Repo-scoped research harness: builds function-call and module-dependency graphs to explore only what's needed; large relative gains on MLE-bench and GitTaskBench with lower token use.

**Frameworks**

- [n8n](https://github.com/n8n-io/n8n) — ⭐196k — Fair-code workflow engine with 400+ nodes and native AI nodes; the self-hosted Zapier that actually does agents and LangChain.
- [langgraph](https://github.com/langchain-ai/langgraph) — ⭐37.1k — State-machine graphs over LLM steps; checkpointing, human-in-the-loop, and durable execution so workflows survive restarts.
- [R2R](https://github.com/SciPhi-AI/R2R) — ⭐7.9k — RAG-first: hybrid search, knowledge graphs, multimodal; the framework for "production RAG" when you care more about retrieval than chat UI.

**Multi-agent and orchestration**

- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) — ⭐12.1k — Microsoft's convergence of AutoGen and Semantic Kernel: build, orchestrate, and deploy agents and multi-agent workflows in Python and .NET, with graph-based workflows and checkpointing — the designated successor harness for both lines.

**Memory and state**

- [cognee](https://github.com/topoteretes/cognee) — ⭐27.6k — Open-source memory layer for agents: an extract–cognify–load pipeline that turns your data into a queryable knowledge graph plus vector store, so agents recall facts and relationships across sessions instead of re-reading context.

**Evaluation and benchmarking harnesses**

- [AgentBench](https://github.com/THUDM/AgentBench) — ⭐3.6k — ICLR'24 benchmark: agents across AlfWorld, DB, knowledge graphs, OS, webshop; Docker Compose, function-calling interface.

---

## `typed`

**Frameworks**

- [mastra](https://github.com/mastra-ai/mastra) — ⭐26.1k — TypeScript-first; agents, tools, and workflows with a single runtime and minimal boilerplate.

**Libraries and SDKs**

- [pydantic-ai](https://github.com/pydantic/pydantic-ai) — ⭐18.4k — Type-safe Python agents with Pydantic I/O; multi-provider, MCP, Logfire observability, and human-in-the-loop.
- [strands-agents](https://github.com/strands-agents/harness-sdk) — ⭐6.5k — Model-driven Python SDK; decorators for tools, native MCP, multi-agent; "minimal code" without sacrificing provider choice.

---

## `local`

**Coding harness configs and SDKs**

- [skillhub](https://github.com/iflytek/skillhub) — ⭐4k — iFlytek's self-hosted registry for publishing, versioning, and governing agent skill packages—the **harness** config layer treated as an enterprise artifact store rather than a CLI or IDE shell.

**Frameworks**

- [n8n](https://github.com/n8n-io/n8n) — ⭐196k — Fair-code workflow engine with 400+ nodes and native AI nodes; the self-hosted Zapier that actually does agents and LangChain.

---

## `provider-agnostic`

**Coding agent products (IDEs, CLIs, full suites)**

- [opencode](https://github.com/anomalyco/opencode) — ⭐185k — Open-source terminal coding agent (formerly `sst/opencode`; transferred to anomalyco). The **harness** is a multi-provider tool-call loop (Claude, OpenAI, Gemini, local) with strong plugin and MCP support; the TUI is the shell. 100% OSS, very actively shipped.
- [Codex](https://github.com/openai/codex) — ⭐97.3k — OpenAI's terminal coding agent. The **harness** is the sandboxed tool-call loop with multi-provider support; the CLI is the shell. Reference implementation for "official CLI that ships code."
- [pi](https://github.com/earendil-works/pi) — ⭐69.8k — The upstream AI agent toolkit behind this list's oh-my-pi fork: a unified multi-provider LLM API, agent loop, and TUI shell providing the **harness** that oh-my-pi's Rust rewrite builds on.
- [oh-my-pi](https://github.com/can1357/oh-my-pi) — ⭐17.4k — Terminal coding agent (fork of Pi) that wires the IDE into the **harness**: hash-anchored edits, a 32-tool loop tuned per-model, LSP rename/references/diagnostics on every write, a real DAP debugger (lldb/dlv/debugpy), long-lived Python + Bun execution kernels that call back into the agent's tools, browser control, and 40+ providers (Claude/OpenAI/Gemini/local). ~55k-line Rust core.
- [jcode](https://github.com/1jehuang/jcode) — ⭐8.3k — Rust terminal coding agent that bills itself outright as a "Coding Agent Harness": a TUI/CLI shell over a multi-provider (Claude, OpenAI) tool-call loop with MCP support.

**Coding harness configs and SDKs**

- [AutoHarness](https://github.com/aiming-lab/AutoHarness) — ⭐347 — Lightweight governance harness: wraps any LLM client in ~2 lines for automated harness engineering—6–14 step pipeline, YAML constitution, risk-pattern matching, session persistence with cost tracking, multi-agent profiles.

**Personal agent runtimes**

- [Hermes](https://github.com/NousResearch/hermes-agent) — ⭐214k — Nous Research's self-improving agent: a learning loop turns experience into reusable skills, builds a persistent user model across sessions, and checkpoints state to disk with rollback; lean enough for a $5 VPS, driven from chat, and model-agnostic (Nous Portal, OpenRouter, OpenAI, or any endpoint).

**Evaluation and benchmarking harnesses**

- [arc-agi-benchmarking](https://github.com/arcprize/arc-agi-benchmarking) — ⭐351 — Runner for ARC-AGI: multi-provider (OpenAI, Anthropic, Gemini, etc.), rate limits, retries, and scoring.

**Libraries and SDKs**

- [LiteLLM](https://github.com/BerriAI/litellm) — ⭐53.3k — One interface to 100+ LLMs; routing, caching, budgets. Not an agent framework—the pipe every agent framework uses.
- [vercel/ai](https://github.com/vercel/ai) — ⭐25.5k — React and Node SDK for streaming, tool calls, and agent-style UIs; provider-agnostic.
- [pydantic-ai](https://github.com/pydantic/pydantic-ai) — ⭐18.4k — Type-safe Python agents with Pydantic I/O; multi-provider, MCP, Logfire observability, and human-in-the-loop.

---

## `cli`

**Coding agent products (IDEs, CLIs, full suites)**

- [opencode](https://github.com/anomalyco/opencode) — ⭐185k — Open-source terminal coding agent (formerly `sst/opencode`; transferred to anomalyco). The **harness** is a multi-provider tool-call loop (Claude, OpenAI, Gemini, local) with strong plugin and MCP support; the TUI is the shell. 100% OSS, very actively shipped.
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) — ⭐106k — Google's first-party terminal agent for Gemini. The **harness** is the plugin/MCP tool-call loop; the terminal is the shell—Google's parallel to Claude Code / Codex, not just an API.
- [Codex](https://github.com/openai/codex) — ⭐97.3k — OpenAI's terminal coding agent. The **harness** is the sandboxed tool-call loop with multi-provider support; the CLI is the shell. Reference implementation for "official CLI that ships code."
- [Open Interpreter](https://github.com/openinterpreter/openinterpreter) — ⭐64.4k — Lightweight terminal coding agent oriented to open models (DeepSeek, Kimi, Qwen). The **harness** is a code-execution loop — the model writes code, the harness executes it with confirmation gates; the CLI is the shell. The original "let the LLM run code on my machine" project, reborn for open weights.
- [crush](https://github.com/charmbracelet/crush) — ⭐26.5k — Charm's terminal coding agent (Charm's fork of the original OpenCode). The **harness** is the tool-calling loop with session persistence; the Bubble Tea TUI is the shell.
- [oh-my-pi](https://github.com/can1357/oh-my-pi) — ⭐17.4k — Terminal coding agent (fork of Pi) that wires the IDE into the **harness**: hash-anchored edits, a 32-tool loop tuned per-model, LSP rename/references/diagnostics on every write, a real DAP debugger (lldb/dlv/debugpy), long-lived Python + Bun execution kernels that call back into the agent's tools, browser control, and 40+ providers (Claude/OpenAI/Gemini/local). ~55k-line Rust core.
- [jcode](https://github.com/1jehuang/jcode) — ⭐8.3k — Rust terminal coding agent that bills itself outright as a "Coding Agent Harness": a TUI/CLI shell over a multi-provider (Claude, OpenAI) tool-call loop with MCP support.

**Coding harness configs and SDKs**

- [get-shit-done](https://github.com/gsd-build/get-shit-done) — ⭐64.7k — Goal-backward planning and wave-based execution over fresh context windows; avoids context rot by design. Python/JS meta-prompting for Claude Code, OpenCode, Gemini CLI.
- [wshobson/agents](https://github.com/wshobson/agents) — ⭐37.8k — Cross-harness marketplace of drop-in subagents and skills for Claude Code, Codex CLI, Cursor, OpenCode, and Copilot; specialized, production-ready agent definitions you install rather than hand-write.
- [agents-cli](https://github.com/google/agents-cli) — ⭐5.1k — Google's official CLI and skill pack that layers agent-creation, evaluation, and deployment skills on top of whatever coding assistant you already run, rather than shipping its own agent loop—the **harness** as a config/skills add-on, not a new runtime.
- [skillhub](https://github.com/iflytek/skillhub) — ⭐4k — iFlytek's self-hosted registry for publishing, versioning, and governing agent skill packages—the **harness** config layer treated as an enterprise artifact store rather than a CLI or IDE shell.

**Personal agent runtimes**

- [Talon](https://github.com/dylanneve1/talon) — ⭐64 — Multi-platform personal agent living in Telegram, Discord, Teams, and the terminal. The **harness** is a pluggable-backend loop (Claude, Kilo, OpenCode, Codex, OpenAI Agents) with full MCP tool access and persistent background agents (Goals, Heartbeat, Dream); the chat apps are shells.

**Plugins, MCPs, CLI tools**

- [aider](https://github.com/Aider-AI/aider) — ⭐47.3k — Git-aware CLI pair programmer; edits in-repo, supports multiple models and MCP so agents see version control and tools.
- [Docker MCP Gateway](https://github.com/docker/mcp-gateway) — ⭐1.5k — Docker's official MCP CLI plugin / gateway; container-aware MCP tooling from Docker (replaces deprecated `docker/mcp-servers` path).
- [agentlog](https://github.com/RyanAlberts/agentlog) — ⭐1 — Persistent decision memory for any project: `remember`, `recall`, `reflect`. Single-file Python CLI that stores decisions as JSONL and uses Claude or Gemini to retrieve and synthesize patterns—Karpathy's LLM Wiki concept as a CLI.

**Evaluation and benchmarking harnesses**

- [agent-qa](https://github.com/vostride/agent-qa) — ⭐157 — Self-improving QA **harness** for web and mobile apps: natural-language tests, memory-backed self-healing, dashboard/CLI, MCP and skills support, plus sandboxed hooks for production regression checks.

---

## `ide`

**Progressive disclosure harnesses**

- [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) — ⭐40.3k — Curated .cursorrules and skills that leverage Cursor's index-then-load model; the canonical collection for rules-as-progressive-disclosure in the IDE.

**Coding agent products (IDEs, CLIs, full suites)**

- [Cline](https://github.com/cline/cline) — ⭐64.6k — VS Code extension whose **harness** is a plan-then-act loop with per-step human approval and cost transparency; the VS Code integration is the UI shell. Open-source counterweight to Cursor.
- [Roo Code](https://github.com/RooCodeInc/Roo-Code) — ⭐24.3k — VS Code/Cursor extension in the Cline lineage. The **harness** is the approval-gated agent with custom modes and a strong MCP story; the IDE is the UI. Popular community fork when you want that workflow without the upstream extension.
- [oh-my-pi](https://github.com/can1357/oh-my-pi) — ⭐17.4k — Terminal coding agent (fork of Pi) that wires the IDE into the **harness**: hash-anchored edits, a 32-tool loop tuned per-model, LSP rename/references/diagnostics on every write, a real DAP debugger (lldb/dlv/debugpy), long-lived Python + Bun execution kernels that call back into the agent's tools, browser control, and 40+ providers (Claude/OpenAI/Gemini/local). ~55k-line Rust core.
- [Proliferate](https://github.com/proliferate-ai/proliferate) — ⭐151 — Open-source AI IDE for Claude Code, Codex, OpenCode, and more. The **harness** contribution is the workspace/session orchestration layer: run multiple coding agents in parallel, locally or in the cloud, with isolated workspaces, reusable workflows, and shared team context.

**Coding harness configs and SDKs**

- [superpowers](https://github.com/obra/superpowers) — ⭐253k — Performance-oriented harness pack for Claude Code, Codex, OpenCode, Cursor: skills, instincts, memory, security, research-first workflows. Treats harness engineering itself as the performance lever.
- [wshobson/agents](https://github.com/wshobson/agents) — ⭐37.8k — Cross-harness marketplace of drop-in subagents and skills for Claude Code, Codex CLI, Cursor, OpenCode, and Copilot; specialized, production-ready agent definitions you install rather than hand-write.
- [skillhub](https://github.com/iflytek/skillhub) — ⭐4k — iFlytek's self-hosted registry for publishing, versioning, and governing agent skill packages—the **harness** config layer treated as an enterprise artifact store rather than a CLI or IDE shell.

**Plugins, MCPs, CLI tools**

- [continue](https://github.com/continuedev/continue) — ⭐34.8k — Open-source IDE extension (VS Code, JetBrains); in-editor completion and chat with local or API models.

---

## `tui`

**Coding agent products (IDEs, CLIs, full suites)**

- [opencode](https://github.com/anomalyco/opencode) — ⭐185k — Open-source terminal coding agent (formerly `sst/opencode`; transferred to anomalyco). The **harness** is a multi-provider tool-call loop (Claude, OpenAI, Gemini, local) with strong plugin and MCP support; the TUI is the shell. 100% OSS, very actively shipped.
- [pi](https://github.com/earendil-works/pi) — ⭐69.8k — The upstream AI agent toolkit behind this list's oh-my-pi fork: a unified multi-provider LLM API, agent loop, and TUI shell providing the **harness** that oh-my-pi's Rust rewrite builds on.
- [crush](https://github.com/charmbracelet/crush) — ⭐26.5k — Charm's terminal coding agent (Charm's fork of the original OpenCode). The **harness** is the tool-calling loop with session persistence; the Bubble Tea TUI is the shell.
- [jcode](https://github.com/1jehuang/jcode) — ⭐8.3k — Rust terminal coding agent that bills itself outright as a "Coding Agent Harness": a TUI/CLI shell over a multi-provider (Claude, OpenAI) tool-call loop with MCP support.

---

## `rust`

**Coding agent products (IDEs, CLIs, full suites)**

- [pi](https://github.com/earendil-works/pi) — ⭐69.8k — The upstream AI agent toolkit behind this list's oh-my-pi fork: a unified multi-provider LLM API, agent loop, and TUI shell providing the **harness** that oh-my-pi's Rust rewrite builds on.
- [goose](https://github.com/aaif-goose/goose) — ⭐51.1k — Block-originated Rust agent, now stewarded by the Linux Foundation's Agentic AI Foundation (`aaif-goose/goose`). The **harness** is the MCP/ACP extension model with recipes and provider choice; there's no fixed UI slot—you bolt it into whatever shell you use.
- [oh-my-pi](https://github.com/can1357/oh-my-pi) — ⭐17.4k — Terminal coding agent (fork of Pi) that wires the IDE into the **harness**: hash-anchored edits, a 32-tool loop tuned per-model, LSP rename/references/diagnostics on every write, a real DAP debugger (lldb/dlv/debugpy), long-lived Python + Bun execution kernels that call back into the agent's tools, browser control, and 40+ providers (Claude/OpenAI/Gemini/local). ~55k-line Rust core.
- [jcode](https://github.com/1jehuang/jcode) — ⭐8.3k — Rust terminal coding agent that bills itself outright as a "Coding Agent Harness": a TUI/CLI shell over a multi-provider (Claude, OpenAI) tool-call loop with MCP support.
- [claw-code-agent](https://github.com/HarnessLab/claw-code-agent) — ⭐528 — Python reimplementation of the Claude Code agent architecture with zero external dependencies; interactive chat, streaming, plugin runtime, nested agent delegation, cost tracking, MCP transport—portable harness without the Rust/TS toolchain.

---

## `python`

**Progressive disclosure harnesses**

- [langgraph-bigtool](https://github.com/langchain-ai/langgraph-bigtool) — ⭐545 — Build LangGraph agents with large tool sets; retrieval and on-demand tool loading so agents scale beyond context without stuffing every schema upfront.
- [ToolGen](https://github.com/Reason-Wang/ToolGen) — ⭐182 — ICLR 2025: unified tool retrieval and calling via generation; 47k+ tools without context stuffing—retrieval and invocation in one generative step.

**Coding agent products (IDEs, CLIs, full suites)**

- [OpenHands](https://github.com/OpenHands/OpenHands) — ⭐80.5k — Dockerized software-engineering agent. The **harness** is the bash/editor/browser toolset with micro-agents and event-stream session bridging; Docker is the sandbox. Main OSS choice for teams self-hosting autonomous repo work.
- [Open Interpreter](https://github.com/openinterpreter/openinterpreter) — ⭐64.4k — Lightweight terminal coding agent oriented to open models (DeepSeek, Kimi, Qwen). The **harness** is a code-execution loop — the model writes code, the harness executes it with confirmation gates; the CLI is the shell. The original "let the LLM run code on my machine" project, reborn for open weights.
- [oh-my-pi](https://github.com/can1357/oh-my-pi) — ⭐17.4k — Terminal coding agent (fork of Pi) that wires the IDE into the **harness**: hash-anchored edits, a 32-tool loop tuned per-model, LSP rename/references/diagnostics on every write, a real DAP debugger (lldb/dlv/debugpy), long-lived Python + Bun execution kernels that call back into the agent's tools, browser control, and 40+ providers (Claude/OpenAI/Gemini/local). ~55k-line Rust core.
- [claw-code-agent](https://github.com/HarnessLab/claw-code-agent) — ⭐528 — Python reimplementation of the Claude Code agent architecture with zero external dependencies; interactive chat, streaming, plugin runtime, nested agent delegation, cost tracking, MCP transport—portable harness without the Rust/TS toolchain.

**Coding harness configs and SDKs**

- [get-shit-done](https://github.com/gsd-build/get-shit-done) — ⭐64.7k — Goal-backward planning and wave-based execution over fresh context windows; avoids context rot by design. Python/JS meta-prompting for Claude Code, OpenCode, Gemini CLI.
- [SWE-agent](https://github.com/SWE-agent/SWE-agent) — ⭐19.8k — LM-driven harness built for SWE-bench: edit state, command execution, and issue-focused loop—the reference agent stack next to the benchmark itself.
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python) — ⭐7.6k — Official Anthropic SDK (Python + [TypeScript](https://github.com/anthropics/claude-agent-sdk-typescript), [demos](https://github.com/anthropics/claude-agent-sdk-demos), [quickstarts](https://github.com/anthropics/claude-quickstarts)): built-in tools, MCP, long-running coding agents with session bridging.
- [RepoMaster](https://github.com/QuantaAlpha/RepoMaster) — ⭐533 — Repo-scoped research harness: builds function-call and module-dependency graphs to explore only what's needed; large relative gains on MLE-bench and GitTaskBench with lower token use.
- [AutoHarness](https://github.com/aiming-lab/AutoHarness) — ⭐347 — Lightweight governance harness: wraps any LLM client in ~2 lines for automated harness engineering—6–14 step pipeline, YAML constitution, risk-pattern matching, session persistence with cost tracking, multi-agent profiles.

**Personal agent runtimes**

- [Hermes](https://github.com/NousResearch/hermes-agent) — ⭐214k — Nous Research's self-improving agent: a learning loop turns experience into reusable skills, builds a persistent user model across sessions, and checkpoints state to disk with rollback; lean enough for a $5 VPS, driven from chat, and model-agnostic (Nous Portal, OpenRouter, OpenAI, or any endpoint).
- [Khoj](https://github.com/khoj-ai/khoj) — ⭐35.7k — Self-hostable "AI second brain": answers over your docs and the web, custom agents, scheduled automations, and multi-client reach (web, Obsidian, Emacs, WhatsApp). A personal-agent harness with retrieval at the core.
- [Agent Zero](https://github.com/agent0ai/agent-zero) — ⭐18.4k — Organic, prompt-defined personal agent framework: hierarchical sub-agents, persistent memory, browser and code tools, and self-modifying behavior; runs in Docker with a web UI.
- [AIlice](https://github.com/myshell-ai/AIlice) — ⭐1.4k — Fully autonomous general-purpose agent; one binary, Docker-ready, for when you want "set goal and walk away" without a framework.

**Frameworks**

- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) — ⭐185k — The original autonomous loop: goal in, agent iterates with tools and memory; Forge is the dev framework, Benchmark the eval harness.
- [langflow](https://github.com/langflow-ai/langflow) — ⭐152k — Low-code UI to build and deploy LangChain/LangGraph flows; visual DAG editor and one-click run.
- [Dify](https://github.com/langgenius/dify) — ⭐149k — One-stop LLM app platform: visual workflows, RAG pipeline, 50+ tools, model management; "ship from prototype to prod" in a single UI.
- [langchain](https://github.com/langchain-ai/langchain) — ⭐142k — Chains, tools, retrievers, and agents; the usual entry point for "add tools to an LLM" in Python/JS.
- [browser-use](https://github.com/browser-use/browser-use) — ⭐104k — Python layer over Playwright: natural-language goals become browser actions—web-agent loop without hand-rolling MCP or a custom driver for every site.
- [llama-index](https://github.com/run-llama/llama_index) — ⭐50.8k — Data-centric: indexing, RAG, and query engines; agent abstractions sit on top of your data pipelines.
- [agno](https://github.com/agno-agi/agno) — ⭐41.1k — Python agents with memory, knowledge bases, tools, and structured outputs; continues the PhiData-era product line under the Agno name—production apps, evals, and pipelines.
- [langgraph](https://github.com/langchain-ai/langgraph) — ⭐37.1k — State-machine graphs over LLM steps; checkpointing, human-in-the-loop, and durable execution so workflows survive restarts.
- [semantic-kernel](https://github.com/microsoft/semantic-kernel) — ⭐28.3k — Microsoft's plugin and planner layer for LLMs; C#, Python, Java; strong on enterprise auth and orchestration.
- [letta](https://github.com/letta-ai/letta) — ⭐23.8k — Python agent runtime with tool use and control flow; lean API; stateful agents with long-horizon memory.
- [rasa](https://github.com/RasaHQ/rasa) — ⭐21.2k — Conversational AI stack (NLU, dialogue, actions); long-standing OSS choice for chat and voice bots.
- [Google ADK](https://github.com/google/adk-python) — ⭐20.6k — Google's official Agent Development Kit: code-first Python toolkit for building, evaluating, and deploying agents. Optimized for Gemini but model-agnostic; deploys to Cloud Run / Vertex AI; ships a dev UI with eval and a code-execution sandbox.
- [R2R](https://github.com/SciPhi-AI/R2R) — ⭐7.9k — RAG-first: hybrid search, knowledge graphs, multimodal; the framework for "production RAG" when you care more about retrieval than chat UI.
- [AgentVerse](https://github.com/OpenBMB/AgentVerse) — ⭐5.1k — Task-solving and simulation envs for multi-LLM agents; deploy many agents in custom environments without building infra from scratch.
- [Bee Agent Framework](https://github.com/i-am-bee/beeai-framework) — ⭐3.3k — Python + TypeScript, LF AI–backed; MCP/ACP, workflows, Requirement Agent; the one that pushes "production multi-agent" without LangChain.
- [mini-coding-agent](https://github.com/rasbt/mini-coding-agent) — ⭐1k — Minimal, readable coding-agent **harness** in Python from ML educator Sebastian Raschka (rasbt), built to explain the core loop — tool calls, edits, execution — without framework scaffolding.
- [AgentSilex](https://github.com/howl-anderson/agentsilex) — ⭐451 — ~300 lines of readable agent code on top of LiteLLM; the "I want to see the whole loop" option for learning or minimal production.
- [SuperAgentX](https://github.com/superagentxai/superagentx) — ⭐200 — Lightweight multi-agent orchestrator with an AGI-angle; minimal surface, docs-first, for teams that want orchestration without the kitchen sink.

**Multi-agent and orchestration**

- [MetaGPT](https://github.com/FoundationAgents/MetaGPT) — ⭐69.3k — The "AI software company" multi-agent framework: role-played PM, architect, and engineer agents turn a one-line requirement into specs, designs, and code along an SOP assembly line. The landmark of the genre; development pace has slowed in 2026.
- [autogen](https://github.com/microsoft/autogen) — ⭐59.7k — Conversable agents and group chats; code execution and human-in-the-loop; Microsoft origin, AG2 ecosystem.
- [OpenManus](https://github.com/FoundationAgents/OpenManus) — ⭐57.2k — Open, invite-free general agent from the MetaGPT team: planning plus tool use over a multi-agent loop, aimed at reproducing Manus-style autonomous task completion on your own keys.
- [crewAI](https://github.com/crewAIInc/crewAI) — ⭐55.4k — Role-based agents (roles, goals, backstories) in Crews; Flows add event-driven and hierarchical control for production.
- [ChatDev](https://github.com/OpenBMB/ChatDev) — ⭐33.7k — Multi-agent software-company simulation (CEO, CTO, programmer, tester) built on chat chains with communicative dehallucination; ChatDev 2.0 continues the line. MetaGPT's conversational sibling.
- [openai-agents-python](https://github.com/openai/openai-agents-python) — ⭐27.8k — Handoffs, guardrails, and multi-LLM routing; minimal surface so you own the loop.
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) — ⭐12.1k — Microsoft's convergence of AutoGen and Semantic Kernel: build, orchestrate, and deploy agents and multi-agent workflows in Python and .NET, with graph-based workflows and checkpointing — the designated successor harness for both lines.
- [PraisonAI](https://github.com/MervinPraison/PraisonAI) — ⭐8.4k — Autonomous multi-agent teams with a single entry point; emphasis on minimal config.
- [AgentRL](https://github.com/THUDM/AgentRL) — ⭐314 — Multitask, multiturn RL for LLM agents; Ray-based scaling, rollout/actor workers—for teams that want to train agents, not just run them.

**Plugins, MCPs, CLI tools**

- [aider](https://github.com/Aider-AI/aider) — ⭐47.3k — Git-aware CLI pair programmer; edits in-repo, supports multiple models and MCP so agents see version control and tools.
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) — ⭐23.6k — Official SDK to build and consume MCP servers/clients in Python; stdio and SSE transports.
- [agentlog](https://github.com/RyanAlberts/agentlog) — ⭐1 — Persistent decision memory for any project: `remember`, `recall`, `reflect`. Single-file Python CLI that stores decisions as JSONL and uses Claude or Gemini to retrieve and synthesize patterns—Karpathy's LLM Wiki concept as a CLI.

**Memory and state**

- [Mem0](https://github.com/mem0ai/mem0) — ⭐60.7k — Universal memory layer for AI agents: stores user/org/session memory, retrieves on demand. Apache-2.0; the de-facto memory primitive paired with most harnesses in 2026.
- [cognee](https://github.com/topoteretes/cognee) — ⭐27.6k — Open-source memory layer for agents: an extract–cognify–load pipeline that turns your data into a queryable knowledge graph plus vector store, so agents recall facts and relationships across sessions instead of re-reading context.

**Evaluation and benchmarking harnesses**

- [Agent Lightning](https://github.com/microsoft/agent-lightning) — ⭐17.4k — Microsoft's training-oriented harness: optimization loops for agent behavior—when you need to improve policies over rollouts, not only score a fixed prompt.
- [SWE-bench](https://github.com/SWE-bench/SWE-bench) — ⭐5.4k — LMs resolve real GitHub issues; Docker harness, instance IDs; standard for code-agent evals.
- [AgentBench](https://github.com/THUDM/AgentBench) — ⭐3.6k — ICLR'24 benchmark: agents across AlfWorld, DB, knowledge graphs, OS, webshop; Docker Compose, function-calling interface.
- [inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai) — ⭐2.3k — Inspect AI core: composable eval tasks, sandboxes, scorers, and multi-model runs; the framework behind inspect_evals, not just the task bundle.
- [WebArena](https://github.com/web-arena-x/webarena) — ⭐1.5k — Realistic web env (e.g. e‑commerce, CMS, dev tools); 812 tasks; measures end-to-end web agent success.
- [SWE-Gym](https://github.com/SWE-Gym/SWE-Gym) — ⭐701 — Training and evaluation for SWE agents and verifiers (ICML 2025).
- [swe-smith](https://github.com/SWE-bench/SWE-smith) — ⭐697 — Data generation for SWE agents; 50k+ instances across 128 repos; used for SWE-agent-LM training.
- [arc-agi-benchmarking](https://github.com/arcprize/arc-agi-benchmarking) — ⭐351 — Runner for ARC-AGI: multi-provider (OpenAI, Anthropic, Gemini, etc.), rate limits, retries, and scoring.
- [AgencyBench](https://github.com/GAIR-NLP/AgencyBench) — ⭐89 — Long-horizon agent benchmark: 32 scenarios, 138 tasks, ~1M tokens and ~90 tool calls; Docker sandbox and rubric-based + LLM judges.
- [letta-evals](https://github.com/letta-ai/letta-evals) — ⭐77 — Eval harness for stateful Letta agents; configurable suites and grading (LLM or rule-based) so you can measure what you ship.
- [SUPER](https://github.com/allenai/super-benchmark) — ⭐53 — Agents that set up and run ML/NLP from GitHub repos; 45 expert problems, 152 masked tasks, 602 AutoGen tasks; Docker-based.

**Observability and eval-ops**

- [MLflow](https://github.com/mlflow/mlflow) — ⭐27k — Mature ML platform now covering GenAI: MLflow Tracing captures every agent step, tool call, and token, with built-in LLM evals and prompt versioning—observability for teams already standardized on MLflow.

**Research and task-specific harnesses**

- [gpt-researcher](https://github.com/assafelovic/gpt-researcher) — ⭐28.3k — Autonomous deep-research agent: web + local sources, citation-grounded reports, multi-agent and deep-research modes. The reference open-source research harness.

**Libraries and SDKs**

- [LiteLLM](https://github.com/BerriAI/litellm) — ⭐53.3k — One interface to 100+ LLMs; routing, caching, budgets. Not an agent framework—the pipe every agent framework uses.
- [Composio](https://github.com/ComposioHQ/composio) — ⭐29.2k — 1,000+ toolkits with auth, tool search, and a sandboxed workbench—drop-in tool layer so agents stop reinventing OAuth + integrations. Python and TypeScript.
- [smolagents](https://github.com/huggingface/smolagents) — ⭐28.3k — Code-as-action agents: model outputs Python executed in sandbox (E2B, Modal, etc.); ~1k LOC core.
- [deepagents](https://github.com/langchain-ai/deepagents) — ⭐26.1k — LangChain's Python+TypeScript agent harness on top of LangGraph: planning tool, virtual filesystem, shell sandbox, sub-agent spawning—the "Claude Code-style" harness as a reusable library.
- [pydantic-ai](https://github.com/pydantic/pydantic-ai) — ⭐18.4k — Type-safe Python agents with Pydantic I/O; multi-provider, MCP, Logfire observability, and human-in-the-loop.
- [E2B](https://github.com/e2b-dev/E2B) — ⭐12.9k — Firecracker sandboxes for executing agent-generated code; the hosted isolation layer many tool-calling demos use instead of running arbitrary LLM output on your laptop.
- [strands-agents](https://github.com/strands-agents/harness-sdk) — ⭐6.5k — Model-driven Python SDK; decorators for tools, native MCP, multi-agent; "minimal code" without sacrificing provider choice.

---

## `typescript`

**Progressive disclosure harnesses**

- [agents.md](https://github.com/agentsmd/agents.md) — ⭐23k — Open format for repo-scoped agent briefings; v1.1 adds hierarchical scope and progressive disclosure so agents get a map of what exists, then load only what's relevant.

**Coding agent products (IDEs, CLIs, full suites)**

- [opencode](https://github.com/anomalyco/opencode) — ⭐185k — Open-source terminal coding agent (formerly `sst/opencode`; transferred to anomalyco). The **harness** is a multi-provider tool-call loop (Claude, OpenAI, Gemini, local) with strong plugin and MCP support; the TUI is the shell. 100% OSS, very actively shipped.
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) — ⭐106k — Google's first-party terminal agent for Gemini. The **harness** is the plugin/MCP tool-call loop; the terminal is the shell—Google's parallel to Claude Code / Codex, not just an API.
- [Cline](https://github.com/cline/cline) — ⭐64.6k — VS Code extension whose **harness** is a plan-then-act loop with per-step human approval and cost transparency; the VS Code integration is the UI shell. Open-source counterweight to Cursor.
- [Roo Code](https://github.com/RooCodeInc/Roo-Code) — ⭐24.3k — VS Code/Cursor extension in the Cline lineage. The **harness** is the approval-gated agent with custom modes and a strong MCP story; the IDE is the UI. Popular community fork when you want that workflow without the upstream extension.
- [claw-code-agent](https://github.com/HarnessLab/claw-code-agent) — ⭐528 — Python reimplementation of the Claude Code agent architecture with zero external dependencies; interactive chat, streaming, plugin runtime, nested agent delegation, cost tracking, MCP transport—portable harness without the Rust/TS toolchain.
- [AgentBox](https://github.com/madarco/agentbox) — ⭐247 — Runs multiple coding agents in parallel, each in its own sandboxed VM, locally or in the cloud, from one command. The **harness** contribution is the VM-per-agent isolation and fleet fan-out layer; whichever agent runs inside owns the loop.
- [Proliferate](https://github.com/proliferate-ai/proliferate) — ⭐151 — Open-source AI IDE for Claude Code, Codex, OpenCode, and more. The **harness** contribution is the workspace/session orchestration layer: run multiple coding agents in parallel, locally or in the cloud, with isolated workspaces, reusable workflows, and shared team context.

**Coding harness configs and SDKs**

- [GStack](https://github.com/garrytan/gstack) — ⭐121k — Garry Tan's Claude Code skill stack: 23 slash-command modes (CEO/eng/design review, QA, ship, browse, retro, …) that structure one assistant as a virtual engineering team. Daily driver while running YC.
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python) — ⭐7.6k — Official Anthropic SDK (Python + [TypeScript](https://github.com/anthropics/claude-agent-sdk-typescript), [demos](https://github.com/anthropics/claude-agent-sdk-demos), [quickstarts](https://github.com/anthropics/claude-quickstarts)): built-in tools, MCP, long-running coding agents with session bridging.
- [LoopTroop](https://github.com/looptroop-ai/LoopTroop) — ⭐60 — Config layer that chains LLM councils for planning, Ralph loops for iterative refinement, and OpenCode worktrees for shipping. The **harness** contribution is the council → loop → worktree pipeline; OpenCode underneath executes.

**Personal agent runtimes**

- [OpenClaw](https://github.com/openclaw/openclaw) — ⭐383k — Self-hosted, always-on personal agent (formerly Clawdbot/Moltbot): a gateway + event-loop runtime that treats messages, heartbeats, crons, and webhooks as one input queue, persists state to local files, and lives in your chat apps (WhatsApp, Telegram, Slack, Discord). 13,700+ community skills; the fastest-growing repo in GitHub history.
- [Eliza](https://github.com/elizaOS/eliza) — ⭐18.7k — Open "agentic operating system" (elizaOS): persistent multi-agent runtime with character files, a plugin ecosystem, and social/platform integrations — the harness behind a large share of autonomous social agents.
- [Talon](https://github.com/dylanneve1/talon) — ⭐64 — Multi-platform personal agent living in Telegram, Discord, Teams, and the terminal. The **harness** is a pluggable-backend loop (Claude, Kilo, OpenCode, Codex, OpenAI Agents) with full MCP tool access and persistent background agents (Goals, Heartbeat, Dream); the chat apps are shells.

**Frameworks**

- [n8n](https://github.com/n8n-io/n8n) — ⭐196k — Fair-code workflow engine with 400+ nodes and native AI nodes; the self-hosted Zapier that actually does agents and LangChain.
- [Flowise](https://github.com/FlowiseAI/Flowise) — ⭐54.5k — Drag-and-drop LangChain UI; deploy flows without code. The low-code sibling to Langflow, with a different component and hosting story.
- [mastra](https://github.com/mastra-ai/mastra) — ⭐26.1k — TypeScript-first; agents, tools, and workflows with a single runtime and minimal boilerplate.
- [botpress](https://github.com/botpress/botpress) — ⭐14.8k — Visual bot builder and runtime; multi-channel, open-source alternative to commercial bot platforms.
- [Bee Agent Framework](https://github.com/i-am-bee/beeai-framework) — ⭐3.3k — Python + TypeScript, LF AI–backed; MCP/ACP, workflows, Requirement Agent; the one that pushes "production multi-agent" without LangChain.

**Plugins, MCPs, CLI tools**

- [MCP Servers](https://github.com/modelcontextprotocol/servers) — ⭐88.4k — The official reference collection of Model Context Protocol servers (filesystem, git, fetch, memory, time, and more)—the canonical, vetted toolset agents connect to, and the pattern every other MCP server is measured against.
- [Context7](https://github.com/upstash/context7) — ⭐59k — MCP server that injects up-to-date, version-specific library docs into an agent's context on demand; kills the stale-training-data hallucinations that plague codegen.
- [Playwright MCP](https://github.com/microsoft/playwright-mcp) — ⭐35k — Playwright's official MCP server: structured browser control (navigate, click, fill, extract) via the accessibility tree rather than screenshots, so web tasks stay fast and deterministic.
- [continue](https://github.com/continuedev/continue) — ⭐34.8k — Open-source IDE extension (VS Code, JetBrains); in-editor completion and chat with local or API models.
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) — ⭐12.8k — Official MCP implementation for Node/TS; reference for the protocol.
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector) — ⭐10.3k — GUI to test and debug MCP servers; inspect tools, resources, and prompts.
- [puppeteer-real-browser-mcp](https://github.com/withLinda/puppeteer-real-browser-mcp-server) — ⭐24 — Puppeteer MCP with real-browser and anti-detection; for agents that need to drive sites that block headless.
- [Better-OpenCodeMCP](https://github.com/ajhcs/Better-OpenCodeMCP) — ⭐8 — MCP server for OpenCode/Crush: async task execution, model bridging (e.g. Claude→Gemini), process pooling.

**Evaluation and benchmarking harnesses**

- [agent-qa](https://github.com/vostride/agent-qa) — ⭐157 — Self-improving QA **harness** for web and mobile apps: natural-language tests, memory-backed self-healing, dashboard/CLI, MCP and skills support, plus sandboxed hooks for production regression checks.

**Observability and eval-ops**

- [Langfuse](https://github.com/langfuse/langfuse) — ⭐31k — Open-source LLM engineering platform: full-trace observability, online and offline evals, prompt management, and cost metrics for agent runs in production—the monitoring layer most harnesses lack out of the box.

**Libraries and SDKs**

- [Composio](https://github.com/ComposioHQ/composio) — ⭐29.2k — 1,000+ toolkits with auth, tool search, and a sandboxed workbench—drop-in tool layer so agents stop reinventing OAuth + integrations. Python and TypeScript.
- [deepagents](https://github.com/langchain-ai/deepagents) — ⭐26.1k — LangChain's Python+TypeScript agent harness on top of LangGraph: planning tool, virtual filesystem, shell sandbox, sub-agent spawning—the "Claude Code-style" harness as a reusable library.
- [vercel/ai](https://github.com/vercel/ai) — ⭐25.5k — React and Node SDK for streaming, tool calls, and agent-style UIs; provider-agnostic.
- [Cloudflare Agents](https://github.com/cloudflare/agents) — ⭐5.2k — Persistent, stateful agents on Durable Objects: state, websockets, scheduling, and AI chat baked in. The serverless answer to "where does the agent live?"
- [openai-agents-js](https://github.com/openai/openai-agents-js) — ⭐3.4k — Official OpenAI Agents SDK for Node/TS: handoffs, guardrails, voice; the JS counterpart to openai-agents-python.
- [open-harness](https://github.com/MaxGfeller/open-harness) — ⭐585 — TypeScript Agent class on Vercel AI SDK; streaming events, filesystem/bash tools, MCP, and subagent delegation.

---

## `python`

**Progressive disclosure harnesses**

- [langgraph-bigtool](https://github.com/langchain-ai/langgraph-bigtool) — ⭐545 — Build LangGraph agents with large tool sets; retrieval and on-demand tool loading so agents scale beyond context without stuffing every schema upfront.
- [ToolGen](https://github.com/Reason-Wang/ToolGen) — ⭐182 — ICLR 2025: unified tool retrieval and calling via generation; 47k+ tools without context stuffing—retrieval and invocation in one generative step.

**Coding agent products (IDEs, CLIs, full suites)**

- [OpenHands](https://github.com/OpenHands/OpenHands) — ⭐80.5k — Dockerized software-engineering agent. The **harness** is the bash/editor/browser toolset with micro-agents and event-stream session bridging; Docker is the sandbox. Main OSS choice for teams self-hosting autonomous repo work.
- [Open Interpreter](https://github.com/openinterpreter/openinterpreter) — ⭐64.4k — Lightweight terminal coding agent oriented to open models (DeepSeek, Kimi, Qwen). The **harness** is a code-execution loop — the model writes code, the harness executes it with confirmation gates; the CLI is the shell. The original "let the LLM run code on my machine" project, reborn for open weights.
- [oh-my-pi](https://github.com/can1357/oh-my-pi) — ⭐17.4k — Terminal coding agent (fork of Pi) that wires the IDE into the **harness**: hash-anchored edits, a 32-tool loop tuned per-model, LSP rename/references/diagnostics on every write, a real DAP debugger (lldb/dlv/debugpy), long-lived Python + Bun execution kernels that call back into the agent's tools, browser control, and 40+ providers (Claude/OpenAI/Gemini/local). ~55k-line Rust core.
- [claw-code-agent](https://github.com/HarnessLab/claw-code-agent) — ⭐528 — Python reimplementation of the Claude Code agent architecture with zero external dependencies; interactive chat, streaming, plugin runtime, nested agent delegation, cost tracking, MCP transport—portable harness without the Rust/TS toolchain.

**Coding harness configs and SDKs**

- [get-shit-done](https://github.com/gsd-build/get-shit-done) — ⭐64.7k — Goal-backward planning and wave-based execution over fresh context windows; avoids context rot by design. Python/JS meta-prompting for Claude Code, OpenCode, Gemini CLI.
- [SWE-agent](https://github.com/SWE-agent/SWE-agent) — ⭐19.8k — LM-driven harness built for SWE-bench: edit state, command execution, and issue-focused loop—the reference agent stack next to the benchmark itself.
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python) — ⭐7.6k — Official Anthropic SDK (Python + [TypeScript](https://github.com/anthropics/claude-agent-sdk-typescript), [demos](https://github.com/anthropics/claude-agent-sdk-demos), [quickstarts](https://github.com/anthropics/claude-quickstarts)): built-in tools, MCP, long-running coding agents with session bridging.
- [RepoMaster](https://github.com/QuantaAlpha/RepoMaster) — ⭐533 — Repo-scoped research harness: builds function-call and module-dependency graphs to explore only what's needed; large relative gains on MLE-bench and GitTaskBench with lower token use.
- [AutoHarness](https://github.com/aiming-lab/AutoHarness) — ⭐347 — Lightweight governance harness: wraps any LLM client in ~2 lines for automated harness engineering—6–14 step pipeline, YAML constitution, risk-pattern matching, session persistence with cost tracking, multi-agent profiles.

**Personal agent runtimes**

- [Hermes](https://github.com/NousResearch/hermes-agent) — ⭐214k — Nous Research's self-improving agent: a learning loop turns experience into reusable skills, builds a persistent user model across sessions, and checkpoints state to disk with rollback; lean enough for a $5 VPS, driven from chat, and model-agnostic (Nous Portal, OpenRouter, OpenAI, or any endpoint).
- [Khoj](https://github.com/khoj-ai/khoj) — ⭐35.7k — Self-hostable "AI second brain": answers over your docs and the web, custom agents, scheduled automations, and multi-client reach (web, Obsidian, Emacs, WhatsApp). A personal-agent harness with retrieval at the core.
- [Agent Zero](https://github.com/agent0ai/agent-zero) — ⭐18.4k — Organic, prompt-defined personal agent framework: hierarchical sub-agents, persistent memory, browser and code tools, and self-modifying behavior; runs in Docker with a web UI.
- [AIlice](https://github.com/myshell-ai/AIlice) — ⭐1.4k — Fully autonomous general-purpose agent; one binary, Docker-ready, for when you want "set goal and walk away" without a framework.

**Frameworks**

- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) — ⭐185k — The original autonomous loop: goal in, agent iterates with tools and memory; Forge is the dev framework, Benchmark the eval harness.
- [langflow](https://github.com/langflow-ai/langflow) — ⭐152k — Low-code UI to build and deploy LangChain/LangGraph flows; visual DAG editor and one-click run.
- [Dify](https://github.com/langgenius/dify) — ⭐149k — One-stop LLM app platform: visual workflows, RAG pipeline, 50+ tools, model management; "ship from prototype to prod" in a single UI.
- [langchain](https://github.com/langchain-ai/langchain) — ⭐142k — Chains, tools, retrievers, and agents; the usual entry point for "add tools to an LLM" in Python/JS.
- [browser-use](https://github.com/browser-use/browser-use) — ⭐104k — Python layer over Playwright: natural-language goals become browser actions—web-agent loop without hand-rolling MCP or a custom driver for every site.
- [llama-index](https://github.com/run-llama/llama_index) — ⭐50.8k — Data-centric: indexing, RAG, and query engines; agent abstractions sit on top of your data pipelines.
- [agno](https://github.com/agno-agi/agno) — ⭐41.1k — Python agents with memory, knowledge bases, tools, and structured outputs; continues the PhiData-era product line under the Agno name—production apps, evals, and pipelines.
- [langgraph](https://github.com/langchain-ai/langgraph) — ⭐37.1k — State-machine graphs over LLM steps; checkpointing, human-in-the-loop, and durable execution so workflows survive restarts.
- [semantic-kernel](https://github.com/microsoft/semantic-kernel) — ⭐28.3k — Microsoft's plugin and planner layer for LLMs; C#, Python, Java; strong on enterprise auth and orchestration.
- [letta](https://github.com/letta-ai/letta) — ⭐23.8k — Python agent runtime with tool use and control flow; lean API; stateful agents with long-horizon memory.
- [rasa](https://github.com/RasaHQ/rasa) — ⭐21.2k — Conversational AI stack (NLU, dialogue, actions); long-standing OSS choice for chat and voice bots.
- [Google ADK](https://github.com/google/adk-python) — ⭐20.6k — Google's official Agent Development Kit: code-first Python toolkit for building, evaluating, and deploying agents. Optimized for Gemini but model-agnostic; deploys to Cloud Run / Vertex AI; ships a dev UI with eval and a code-execution sandbox.
- [R2R](https://github.com/SciPhi-AI/R2R) — ⭐7.9k — RAG-first: hybrid search, knowledge graphs, multimodal; the framework for "production RAG" when you care more about retrieval than chat UI.
- [AgentVerse](https://github.com/OpenBMB/AgentVerse) — ⭐5.1k — Task-solving and simulation envs for multi-LLM agents; deploy many agents in custom environments without building infra from scratch.
- [Bee Agent Framework](https://github.com/i-am-bee/beeai-framework) — ⭐3.3k — Python + TypeScript, LF AI–backed; MCP/ACP, workflows, Requirement Agent; the one that pushes "production multi-agent" without LangChain.
- [mini-coding-agent](https://github.com/rasbt/mini-coding-agent) — ⭐1k — Minimal, readable coding-agent **harness** in Python from ML educator Sebastian Raschka (rasbt), built to explain the core loop — tool calls, edits, execution — without framework scaffolding.
- [AgentSilex](https://github.com/howl-anderson/agentsilex) — ⭐451 — ~300 lines of readable agent code on top of LiteLLM; the "I want to see the whole loop" option for learning or minimal production.
- [SuperAgentX](https://github.com/superagentxai/superagentx) — ⭐200 — Lightweight multi-agent orchestrator with an AGI-angle; minimal surface, docs-first, for teams that want orchestration without the kitchen sink.

**Multi-agent and orchestration**

- [MetaGPT](https://github.com/FoundationAgents/MetaGPT) — ⭐69.3k — The "AI software company" multi-agent framework: role-played PM, architect, and engineer agents turn a one-line requirement into specs, designs, and code along an SOP assembly line. The landmark of the genre; development pace has slowed in 2026.
- [autogen](https://github.com/microsoft/autogen) — ⭐59.7k — Conversable agents and group chats; code execution and human-in-the-loop; Microsoft origin, AG2 ecosystem.
- [OpenManus](https://github.com/FoundationAgents/OpenManus) — ⭐57.2k — Open, invite-free general agent from the MetaGPT team: planning plus tool use over a multi-agent loop, aimed at reproducing Manus-style autonomous task completion on your own keys.
- [crewAI](https://github.com/crewAIInc/crewAI) — ⭐55.4k — Role-based agents (roles, goals, backstories) in Crews; Flows add event-driven and hierarchical control for production.
- [ChatDev](https://github.com/OpenBMB/ChatDev) — ⭐33.7k — Multi-agent software-company simulation (CEO, CTO, programmer, tester) built on chat chains with communicative dehallucination; ChatDev 2.0 continues the line. MetaGPT's conversational sibling.
- [openai-agents-python](https://github.com/openai/openai-agents-python) — ⭐27.8k — Handoffs, guardrails, and multi-LLM routing; minimal surface so you own the loop.
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) — ⭐12.1k — Microsoft's convergence of AutoGen and Semantic Kernel: build, orchestrate, and deploy agents and multi-agent workflows in Python and .NET, with graph-based workflows and checkpointing — the designated successor harness for both lines.
- [PraisonAI](https://github.com/MervinPraison/PraisonAI) — ⭐8.4k — Autonomous multi-agent teams with a single entry point; emphasis on minimal config.
- [AgentRL](https://github.com/THUDM/AgentRL) — ⭐314 — Multitask, multiturn RL for LLM agents; Ray-based scaling, rollout/actor workers—for teams that want to train agents, not just run them.

**Plugins, MCPs, CLI tools**

- [aider](https://github.com/Aider-AI/aider) — ⭐47.3k — Git-aware CLI pair programmer; edits in-repo, supports multiple models and MCP so agents see version control and tools.
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) — ⭐23.6k — Official SDK to build and consume MCP servers/clients in Python; stdio and SSE transports.
- [agentlog](https://github.com/RyanAlberts/agentlog) — ⭐1 — Persistent decision memory for any project: `remember`, `recall`, `reflect`. Single-file Python CLI that stores decisions as JSONL and uses Claude or Gemini to retrieve and synthesize patterns—Karpathy's LLM Wiki concept as a CLI.

**Memory and state**

- [Mem0](https://github.com/mem0ai/mem0) — ⭐60.7k — Universal memory layer for AI agents: stores user/org/session memory, retrieves on demand. Apache-2.0; the de-facto memory primitive paired with most harnesses in 2026.
- [cognee](https://github.com/topoteretes/cognee) — ⭐27.6k — Open-source memory layer for agents: an extract–cognify–load pipeline that turns your data into a queryable knowledge graph plus vector store, so agents recall facts and relationships across sessions instead of re-reading context.

**Evaluation and benchmarking harnesses**

- [Agent Lightning](https://github.com/microsoft/agent-lightning) — ⭐17.4k — Microsoft's training-oriented harness: optimization loops for agent behavior—when you need to improve policies over rollouts, not only score a fixed prompt.
- [SWE-bench](https://github.com/SWE-bench/SWE-bench) — ⭐5.4k — LMs resolve real GitHub issues; Docker harness, instance IDs; standard for code-agent evals.
- [AgentBench](https://github.com/THUDM/AgentBench) — ⭐3.6k — ICLR'24 benchmark: agents across AlfWorld, DB, knowledge graphs, OS, webshop; Docker Compose, function-calling interface.
- [inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai) — ⭐2.3k — Inspect AI core: composable eval tasks, sandboxes, scorers, and multi-model runs; the framework behind inspect_evals, not just the task bundle.
- [WebArena](https://github.com/web-arena-x/webarena) — ⭐1.5k — Realistic web env (e.g. e‑commerce, CMS, dev tools); 812 tasks; measures end-to-end web agent success.
- [SWE-Gym](https://github.com/SWE-Gym/SWE-Gym) — ⭐701 — Training and evaluation for SWE agents and verifiers (ICML 2025).
- [swe-smith](https://github.com/SWE-bench/SWE-smith) — ⭐697 — Data generation for SWE agents; 50k+ instances across 128 repos; used for SWE-agent-LM training.
- [arc-agi-benchmarking](https://github.com/arcprize/arc-agi-benchmarking) — ⭐351 — Runner for ARC-AGI: multi-provider (OpenAI, Anthropic, Gemini, etc.), rate limits, retries, and scoring.
- [AgencyBench](https://github.com/GAIR-NLP/AgencyBench) — ⭐89 — Long-horizon agent benchmark: 32 scenarios, 138 tasks, ~1M tokens and ~90 tool calls; Docker sandbox and rubric-based + LLM judges.
- [letta-evals](https://github.com/letta-ai/letta-evals) — ⭐77 — Eval harness for stateful Letta agents; configurable suites and grading (LLM or rule-based) so you can measure what you ship.
- [SUPER](https://github.com/allenai/super-benchmark) — ⭐53 — Agents that set up and run ML/NLP from GitHub repos; 45 expert problems, 152 masked tasks, 602 AutoGen tasks; Docker-based.

**Observability and eval-ops**

- [MLflow](https://github.com/mlflow/mlflow) — ⭐27k — Mature ML platform now covering GenAI: MLflow Tracing captures every agent step, tool call, and token, with built-in LLM evals and prompt versioning—observability for teams already standardized on MLflow.

**Research and task-specific harnesses**

- [gpt-researcher](https://github.com/assafelovic/gpt-researcher) — ⭐28.3k — Autonomous deep-research agent: web + local sources, citation-grounded reports, multi-agent and deep-research modes. The reference open-source research harness.

**Libraries and SDKs**

- [LiteLLM](https://github.com/BerriAI/litellm) — ⭐53.3k — One interface to 100+ LLMs; routing, caching, budgets. Not an agent framework—the pipe every agent framework uses.
- [Composio](https://github.com/ComposioHQ/composio) — ⭐29.2k — 1,000+ toolkits with auth, tool search, and a sandboxed workbench—drop-in tool layer so agents stop reinventing OAuth + integrations. Python and TypeScript.
- [smolagents](https://github.com/huggingface/smolagents) — ⭐28.3k — Code-as-action agents: model outputs Python executed in sandbox (E2B, Modal, etc.); ~1k LOC core.
- [deepagents](https://github.com/langchain-ai/deepagents) — ⭐26.1k — LangChain's Python+TypeScript agent harness on top of LangGraph: planning tool, virtual filesystem, shell sandbox, sub-agent spawning—the "Claude Code-style" harness as a reusable library.
- [pydantic-ai](https://github.com/pydantic/pydantic-ai) — ⭐18.4k — Type-safe Python agents with Pydantic I/O; multi-provider, MCP, Logfire observability, and human-in-the-loop.
- [E2B](https://github.com/e2b-dev/E2B) — ⭐12.9k — Firecracker sandboxes for executing agent-generated code; the hosted isolation layer many tool-calling demos use instead of running arbitrary LLM output on your laptop.
- [strands-agents](https://github.com/strands-agents/harness-sdk) — ⭐6.5k — Model-driven Python SDK; decorators for tools, native MCP, multi-agent; "minimal code" without sacrificing provider choice.

---

## `typescript`

**Progressive disclosure harnesses**

- [agents.md](https://github.com/agentsmd/agents.md) — ⭐23k — Open format for repo-scoped agent briefings; v1.1 adds hierarchical scope and progressive disclosure so agents get a map of what exists, then load only what's relevant.

**Coding agent products (IDEs, CLIs, full suites)**

- [opencode](https://github.com/anomalyco/opencode) — ⭐185k — Open-source terminal coding agent (formerly `sst/opencode`; transferred to anomalyco). The **harness** is a multi-provider tool-call loop (Claude, OpenAI, Gemini, local) with strong plugin and MCP support; the TUI is the shell. 100% OSS, very actively shipped.
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) — ⭐106k — Google's first-party terminal agent for Gemini. The **harness** is the plugin/MCP tool-call loop; the terminal is the shell—Google's parallel to Claude Code / Codex, not just an API.
- [Cline](https://github.com/cline/cline) — ⭐64.6k — VS Code extension whose **harness** is a plan-then-act loop with per-step human approval and cost transparency; the VS Code integration is the UI shell. Open-source counterweight to Cursor.
- [Roo Code](https://github.com/RooCodeInc/Roo-Code) — ⭐24.3k — VS Code/Cursor extension in the Cline lineage. The **harness** is the approval-gated agent with custom modes and a strong MCP story; the IDE is the UI. Popular community fork when you want that workflow without the upstream extension.
- [claw-code-agent](https://github.com/HarnessLab/claw-code-agent) — ⭐528 — Python reimplementation of the Claude Code agent architecture with zero external dependencies; interactive chat, streaming, plugin runtime, nested agent delegation, cost tracking, MCP transport—portable harness without the Rust/TS toolchain.
- [AgentBox](https://github.com/madarco/agentbox) — ⭐247 — Runs multiple coding agents in parallel, each in its own sandboxed VM, locally or in the cloud, from one command. The **harness** contribution is the VM-per-agent isolation and fleet fan-out layer; whichever agent runs inside owns the loop.
- [Proliferate](https://github.com/proliferate-ai/proliferate) — ⭐151 — Open-source AI IDE for Claude Code, Codex, OpenCode, and more. The **harness** contribution is the workspace/session orchestration layer: run multiple coding agents in parallel, locally or in the cloud, with isolated workspaces, reusable workflows, and shared team context.

**Coding harness configs and SDKs**

- [GStack](https://github.com/garrytan/gstack) — ⭐121k — Garry Tan's Claude Code skill stack: 23 slash-command modes (CEO/eng/design review, QA, ship, browse, retro, …) that structure one assistant as a virtual engineering team. Daily driver while running YC.
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python) — ⭐7.6k — Official Anthropic SDK (Python + [TypeScript](https://github.com/anthropics/claude-agent-sdk-typescript), [demos](https://github.com/anthropics/claude-agent-sdk-demos), [quickstarts](https://github.com/anthropics/claude-quickstarts)): built-in tools, MCP, long-running coding agents with session bridging.
- [LoopTroop](https://github.com/looptroop-ai/LoopTroop) — ⭐60 — Config layer that chains LLM councils for planning, Ralph loops for iterative refinement, and OpenCode worktrees for shipping. The **harness** contribution is the council → loop → worktree pipeline; OpenCode underneath executes.

**Personal agent runtimes**

- [OpenClaw](https://github.com/openclaw/openclaw) — ⭐383k — Self-hosted, always-on personal agent (formerly Clawdbot/Moltbot): a gateway + event-loop runtime that treats messages, heartbeats, crons, and webhooks as one input queue, persists state to local files, and lives in your chat apps (WhatsApp, Telegram, Slack, Discord). 13,700+ community skills; the fastest-growing repo in GitHub history.
- [Eliza](https://github.com/elizaOS/eliza) — ⭐18.7k — Open "agentic operating system" (elizaOS): persistent multi-agent runtime with character files, a plugin ecosystem, and social/platform integrations — the harness behind a large share of autonomous social agents.
- [Talon](https://github.com/dylanneve1/talon) — ⭐64 — Multi-platform personal agent living in Telegram, Discord, Teams, and the terminal. The **harness** is a pluggable-backend loop (Claude, Kilo, OpenCode, Codex, OpenAI Agents) with full MCP tool access and persistent background agents (Goals, Heartbeat, Dream); the chat apps are shells.

**Frameworks**

- [n8n](https://github.com/n8n-io/n8n) — ⭐196k — Fair-code workflow engine with 400+ nodes and native AI nodes; the self-hosted Zapier that actually does agents and LangChain.
- [Flowise](https://github.com/FlowiseAI/Flowise) — ⭐54.5k — Drag-and-drop LangChain UI; deploy flows without code. The low-code sibling to Langflow, with a different component and hosting story.
- [mastra](https://github.com/mastra-ai/mastra) — ⭐26.1k — TypeScript-first; agents, tools, and workflows with a single runtime and minimal boilerplate.
- [botpress](https://github.com/botpress/botpress) — ⭐14.8k — Visual bot builder and runtime; multi-channel, open-source alternative to commercial bot platforms.
- [Bee Agent Framework](https://github.com/i-am-bee/beeai-framework) — ⭐3.3k — Python + TypeScript, LF AI–backed; MCP/ACP, workflows, Requirement Agent; the one that pushes "production multi-agent" without LangChain.

**Plugins, MCPs, CLI tools**

- [MCP Servers](https://github.com/modelcontextprotocol/servers) — ⭐88.4k — The official reference collection of Model Context Protocol servers (filesystem, git, fetch, memory, time, and more)—the canonical, vetted toolset agents connect to, and the pattern every other MCP server is measured against.
- [Context7](https://github.com/upstash/context7) — ⭐59k — MCP server that injects up-to-date, version-specific library docs into an agent's context on demand; kills the stale-training-data hallucinations that plague codegen.
- [Playwright MCP](https://github.com/microsoft/playwright-mcp) — ⭐35k — Playwright's official MCP server: structured browser control (navigate, click, fill, extract) via the accessibility tree rather than screenshots, so web tasks stay fast and deterministic.
- [continue](https://github.com/continuedev/continue) — ⭐34.8k — Open-source IDE extension (VS Code, JetBrains); in-editor completion and chat with local or API models.
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) — ⭐12.8k — Official MCP implementation for Node/TS; reference for the protocol.
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector) — ⭐10.3k — GUI to test and debug MCP servers; inspect tools, resources, and prompts.
- [puppeteer-real-browser-mcp](https://github.com/withLinda/puppeteer-real-browser-mcp-server) — ⭐24 — Puppeteer MCP with real-browser and anti-detection; for agents that need to drive sites that block headless.
- [Better-OpenCodeMCP](https://github.com/ajhcs/Better-OpenCodeMCP) — ⭐8 — MCP server for OpenCode/Crush: async task execution, model bridging (e.g. Claude→Gemini), process pooling.

**Evaluation and benchmarking harnesses**

- [agent-qa](https://github.com/vostride/agent-qa) — ⭐157 — Self-improving QA **harness** for web and mobile apps: natural-language tests, memory-backed self-healing, dashboard/CLI, MCP and skills support, plus sandboxed hooks for production regression checks.

**Observability and eval-ops**

- [Langfuse](https://github.com/langfuse/langfuse) — ⭐31k — Open-source LLM engineering platform: full-trace observability, online and offline evals, prompt management, and cost metrics for agent runs in production—the monitoring layer most harnesses lack out of the box.

**Libraries and SDKs**

- [Composio](https://github.com/ComposioHQ/composio) — ⭐29.2k — 1,000+ toolkits with auth, tool search, and a sandboxed workbench—drop-in tool layer so agents stop reinventing OAuth + integrations. Python and TypeScript.
- [deepagents](https://github.com/langchain-ai/deepagents) — ⭐26.1k — LangChain's Python+TypeScript agent harness on top of LangGraph: planning tool, virtual filesystem, shell sandbox, sub-agent spawning—the "Claude Code-style" harness as a reusable library.
- [vercel/ai](https://github.com/vercel/ai) — ⭐25.5k — React and Node SDK for streaming, tool calls, and agent-style UIs; provider-agnostic.
- [Cloudflare Agents](https://github.com/cloudflare/agents) — ⭐5.2k — Persistent, stateful agents on Durable Objects: state, websockets, scheduling, and AI chat baked in. The serverless answer to "where does the agent live?"
- [openai-agents-js](https://github.com/openai/openai-agents-js) — ⭐3.4k — Official OpenAI Agents SDK for Node/TS: handoffs, guardrails, voice; the JS counterpart to openai-agents-python.
- [open-harness](https://github.com/MaxGfeller/open-harness) — ⭐585 — TypeScript Agent class on Vercel AI SDK; streaming events, filesystem/bash tools, MCP, and subagent delegation.
