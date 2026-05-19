#!/usr/bin/env python3
"""Generator for best-of-Agent-Harnesses projects.yaml and README.md.

All project data is defined here as structured Python. Running this script
produces both files deterministically.
"""

import re
from pathlib import Path
from dataclasses import dataclass, field

REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Project:
    name: str
    github_id: str
    description: str
    axis: str
    oss: str = "✅"
    labels: list = field(default_factory=list)
    link_name: str = ""  # If set, override display name in link

    @property
    def display_name(self) -> str:
        return self.link_name or self.name


# OSS markers:
# "✅"            standard OSS (MIT/Apache/BSD/GPL/MPL/CC0/AGPL)
# "⚠️ Fair-code"  n8n-style sustainable-use / commercial restrictions
# "⚠️ Elastic-2.0" mastra etc.
# "⚠️ BSL"       business source license
# "❓"           no license file

CATEGORIES = [
    ("progressive-disclosure", "Progressive disclosure harnesses",
     "Formats, runtimes, and patterns that reveal context, tools, or instructions in layers—index first, details on demand—to control tokens and improve agent focus (the \"map, not encyclopedia\" principle)."),
    ("coding-agent-products", "Coding agent products (IDEs, CLIs, full suites)",
     "Turnkey coding agents you install and run: IDE extensions, terminal CLIs, Dockerized workspaces. Each entry notes which part is the harness (the agent loop, tool wiring, approval model) versus the UI shell (VS Code extension, TUI, browser client)."),
    ("coding-harness-configs", "Coding harness configs and SDKs",
     "Skill packs, slash-command libraries, meta-prompting frameworks, and official SDKs that give you the harness (the agent loop, planning, memory, hooks) without bundling a specific IDE or CLI shell."),
    ("frameworks", "Frameworks",
     "General-purpose agent and LLM application frameworks (the app layer, not harnesses per se)."),
    ("multi-agent", "Multi-agent and orchestration",
     "Harnesses and patterns for multi-agent coordination and handoffs."),
    ("plugins-mcp-cli", "Plugins, MCPs, CLI tools",
     "IDE plugins, concrete MCP servers, and CLI tools that give agents tools and context."),
    ("evaluation", "Evaluation and benchmarking harnesses",
     "Agentic eval systems, reasoning benchmarks, and open agent benchmarks."),
    ("research-task", "Research and task-specific harnesses",
     "Deep research, document QA, and domain-specific agent loops."),
    ("libraries-sdks", "Libraries and SDKs",
     "Lightweight runtimes, tool loops, and provider-agnostic harness primitives."),
]

PROJECTS: dict[str, list[Project]] = {
    "progressive-disclosure": [
        Project("agents.md", "agentsmd/agents.md",
                "Open format for repo-scoped agent briefings; v1.1 adds hierarchical scope and progressive disclosure so agents get a map of what exists, then load only what's relevant.",
                "super simple (format only)", labels=["javascript"]),
        Project("awesome-cursorrules", "PatrickJS/awesome-cursorrules",
                "Curated .cursorrules and skills that leverage Cursor's index-then-load model; the canonical collection for rules-as-progressive-disclosure in the IDE.",
                "super simple (content bundle)"),
        Project("MCP-Zero", "xfey/MCP-Zero",
                "Active tool discovery for autonomous agents: model requests tools by requirement; hierarchical semantic routing over 308 servers / 2,797 tools with ~98% token reduction (APIBank).",
                "complex (3k tools, full routing)"),
        Project("langgraph-bigtool", "langchain-ai/langgraph-bigtool",
                "Build LangGraph agents with large tool sets; retrieval and on-demand tool loading so agents scale beyond context without stuffing every schema upfront.",
                "slightly complex (large tool sets)", labels=["python"]),
        Project("spring-ai-tool-search-tool", "spring-ai-community/spring-ai-tool-search-tool",
                "Dynamic tool discovery for Spring AI: model gets a search tool first, then pulls definitions for relevant tools; 34–64% token reduction across providers.",
                "mostly simple (search-then-load)"),
        Project("ToolGen", "Reason-Wang/ToolGen",
                "ICLR 2025: unified tool retrieval and calling via generation; 47k+ tools without context stuffing—retrieval and invocation in one generative step.",
                "complex (47k+ tools)", oss="❓", labels=["python"]),
        Project("ToolRAG", "antl3x/ToolRAG",
                "Semantic tool retrieval for LLMs; serves only the tools the user query demands (MCP-compatible), unlimited tool sets with zero context penalty.",
                "mostly simple (query-driven retrieval)"),
    ],
    "coding-agent-products": [
        Project("Cline", "cline/cline",
                "VS Code extension whose **harness** is a plan-then-act loop with per-step human approval and cost transparency; the VS Code integration is the UI shell. Open-source counterweight to Cursor.",
                "slightly complex (plan-then-act, approval gates)", labels=["javascript"]),
        Project("Roo-Code", "RooCodeInc/Roo-Code", "",
                "slightly complex (IDE extension, MCP-first)", labels=["javascript"], link_name="Roo Code"),
        Project("Codex", "openai/codex",
                "OpenAI's terminal coding agent. The **harness** is the sandboxed tool-call loop with multi-provider support; the CLI is the shell. Reference implementation for \"official CLI that ships code.\"",
                "slightly complex (reference CLI, sandboxed)"),
        Project("Gemini CLI", "google-gemini/gemini-cli",
                "Google's first-party terminal agent for Gemini. The **harness** is the plugin/MCP tool-call loop; the terminal is the shell—Google's parallel to Claude Code / Codex, not just an API.",
                "slightly complex (official CLI, plugins, MCP)", labels=["javascript"]),
        Project("crush", "charmbracelet/crush",
                "Charm's terminal coding agent (Charm's fork of the original OpenCode). The **harness** is the tool-calling loop with session persistence; the Bubble Tea TUI is the shell.",
                "slightly complex (terminal agent, TUI)", oss="⚠️ FSL-1.1-MIT"),
        Project("opencode", "anomalyco/opencode",
                "Open-source terminal coding agent (formerly `sst/opencode`; transferred to anomalyco). The **harness** is a multi-provider tool-call loop (Claude, OpenAI, Gemini, local) with strong plugin and MCP support; the TUI is the shell. 100% OSS, very actively shipped.",
                "slightly complex (multi-provider, plugins, MCP)", labels=["javascript"]),
        Project("OpenHands", "OpenHands/OpenHands",
                "Dockerized software-engineering agent. The **harness** is the bash/editor/browser toolset with micro-agents and event-stream session bridging; Docker is the sandbox. Main OSS choice for teams self-hosting autonomous repo work.",
                "complex (Docker runtime, multi-surface agent — product suite)", oss="⚠️ (multi-license)", labels=["python"]),
        Project("goose", "aaif-goose/goose",
                "Block-originated Rust agent, now stewarded by the Linux Foundation's Agentic AI Foundation (`aaif-goose/goose`). The **harness** is the MCP/ACP extension model with recipes and provider choice; there's no fixed UI slot—you bolt it into whatever shell you use.",
                "slightly complex (extensions, MCP/ACP)"),
        Project("claw-code-agent", "HarnessLab/claw-code-agent",
                "Python reimplementation of the Claude Code agent architecture with zero external dependencies; interactive chat, streaming, plugin runtime, nested agent delegation, cost tracking, MCP transport—portable harness without the Rust/TS toolchain.",
                "slightly complex (pure Python, plugin runtime)", oss="❓", labels=["python"]),
        Project("coderClaw", "SeanHogg/coderClaw",
                "Self-hosted multi-role coding system (Creator, Reviewer, Test, Refactor, etc.) with AST and semantic maps; IDE-agnostic, chat-channel triggers.",
                "slightly complex (multi-role, AST/semantic)", oss="❓", labels=["javascript"]),
    ],
    "coding-harness-configs": [
        Project("get-shit-done", "gsd-build/get-shit-done",
                "Goal-backward planning and wave-based execution over fresh context windows; avoids context rot by design. Python/JS meta-prompting for Claude Code, OpenCode, Gemini CLI.",
                "mostly simple (meta-prompting, you own stack)"),
        Project("GStack", "garrytan/gstack",
                "Garry Tan's Claude Code skill stack: 23 slash-command modes (CEO/eng/design review, QA, ship, browse, retro, …) that structure one assistant as a virtual engineering team. Daily driver while running YC.",
                "slightly complex (multi-role slash-command harness)", labels=["javascript"]),
        Project("everything-claude-code", "affaan-m/everything-claude-code",
                "The breakout 2026 harness pack for Claude Code: 28 specialized subagents, 119 reusable skills, 60 slash commands, 34 rules, 20+ automated hooks. Ships a full \"AI engineering team\" as config.",
                "complex (subagents + skills + hooks — product suite)"),
        Project("superpowers", "obra/superpowers",
                "Performance-oriented harness pack for Claude Code, Codex, OpenCode, Cursor: skills, instincts, memory, security, research-first workflows. Treats harness engineering itself as the performance lever.",
                "complex (multi-IDE skill stack — product suite)"),
        Project("pmstack", "RyanAlberts/pmstack",
                "Claude Code config for AI product managers: CLAUDE.md plus skills for competitive analysis, PRD-from-signal, metric frameworks, stakeholder briefs, and agent eval design. \"GStack for PMs.\"",
                "super simple (skills bundle, PM-focused)"),
        Project("Claude Agent SDK", "anthropics/claude-agent-sdk-python",
                "Official Anthropic SDK (Python + [TypeScript](https://github.com/anthropics/claude-agent-sdk-typescript), [demos](https://github.com/anthropics/claude-agent-sdk-demos), [quickstarts](https://github.com/anthropics/claude-quickstarts)): built-in tools, MCP, long-running coding agents with session bridging.",
                "complex (full SDK, session bridging — product suite)", labels=["python"]),
        Project("AutoHarness", "aiming-lab/AutoHarness",
                "Lightweight governance harness: wraps any LLM client in ~2 lines for automated harness engineering—6–14 step pipeline, YAML constitution, risk-pattern matching, session persistence with cost tracking, multi-agent profiles.",
                "super simple (2-line wrapper, YAML gov)", labels=["python"]),
        Project("RepoMaster", "QuantaAlpha/RepoMaster",
                "Repo-scoped research harness: builds function-call and module-dependency graphs to explore only what's needed; large relative gains on MLE-bench and GitTaskBench with lower token use.",
                "slightly complex (graph-based exploration)", oss="❓", labels=["python"]),
        Project("SWE-agent", "SWE-agent/SWE-agent",
                "LM-driven harness built for SWE-bench: edit state, command execution, and issue-focused loop—the reference agent stack next to the benchmark itself.",
                "slightly complex (SWE-bench pairing, stateful edits)", labels=["python"]),
        Project("OpenHarness (HKUDS)", "HKUDS/OpenHarness",
                "Open agent harness with a built-in personal agent (\"Ohmo\") that runs across Feishu, Slack, Telegram, and Discord; core tool-use, skills, memory, multi-agent coordination with auto-compaction for multi-day sessions.",
                "complex (personal agent + multi-channel — product suite)"),
        Project("Anthropic Skills", "anthropics/skills",
                "Anthropic's official Agent Skills repository: SKILL.md-based folders (instructions, scripts, resources) Claude dynamically loads on Claude Code, Claude.ai, and the API. The reference for progressive-disclosure skill packs in 2026.",
                "mostly simple (official skills format)", link_name="Anthropic Skills"),
    ],
    "frameworks": [
        Project("langgraph", "langchain-ai/langgraph",
                "State-machine graphs over LLM steps; checkpointing, human-in-the-loop, and durable execution so workflows survive restarts.",
                "slightly complex (graphs, checkpointing, durable exec)", labels=["python"]),
        Project("langchain", "langchain-ai/langchain",
                "Chains, tools, retrievers, and agents; the usual entry point for \"add tools to an LLM\" in Python/JS.",
                "complex (kitchen-sink ecosystem — product suite)", labels=["python"]),
        Project("llama-index", "run-llama/llama_index",
                "Data-centric: indexing, RAG, and query engines; agent abstractions sit on top of your data pipelines.",
                "complex (RAG + agents — product suite)", labels=["python"]),
        Project("semantic-kernel", "microsoft/semantic-kernel",
                "Microsoft's plugin and planner layer for LLMs; C#, Python, Java; strong on enterprise auth and orchestration.",
                "complex (enterprise, multi-language — product suite)", labels=["python"]),
        Project("mastra", "mastra-ai/mastra",
                "TypeScript-first; agents, tools, and workflows with a single runtime and minimal boilerplate.",
                "slightly complex (TS-first, minimal boilerplate)", oss="⚠️ Elastic-2.0", labels=["javascript"]),
        Project("agno", "agno-agi/agno",
                "Python agents with memory, knowledge bases, tools, and structured outputs; continues the PhiData-era product line under the Agno name—production apps, evals, and pipelines.",
                "complex (memory, KB, observability — product suite)", labels=["python"]),
        Project("letta", "letta-ai/letta",
                "Python agent runtime with tool use and control flow; lean API; stateful agents with long-horizon memory.",
                "mostly simple (lean API)", labels=["python"]),
        Project("langflow", "langflow-ai/langflow",
                "Low-code UI to build and deploy LangChain/LangGraph flows; visual DAG editor and one-click run.",
                "complex (low-code, visual — product suite)", labels=["python"]),
        Project("rasa", "RasaHQ/rasa",
                "Conversational AI stack (NLU, dialogue, actions); long-standing OSS choice for chat and voice bots.",
                "complex (full stack — product suite)", labels=["python"]),
        Project("botpress", "botpress/botpress",
                "Visual bot builder and runtime; multi-channel, open-source alternative to commercial bot platforms.",
                "complex (visual builder, multi-channel — product suite)", labels=["javascript"]),
        Project("Dify", "langgenius/dify",
                "One-stop LLM app platform: visual workflows, RAG pipeline, 50+ tools, model management; \"ship from prototype to prod\" in a single UI.",
                "complex (one-stop platform — product suite)", oss="⚠️ Fair-code", labels=["python"]),
        Project("n8n", "n8n-io/n8n",
                "Fair-code workflow engine with 400+ nodes and native AI nodes; the self-hosted Zapier that actually does agents and LangChain.",
                "complex (400+ nodes, workflow engine — product suite)", oss="⚠️ Fair-code", labels=["javascript"]),
        Project("AutoGPT", "Significant-Gravitas/AutoGPT",
                "The original autonomous loop: goal in, agent iterates with tools and memory; Forge is the dev framework, Benchmark the eval harness.",
                "complex (autonomous loop, tools, memory — product suite)", oss="⚠️ Polyform-SU", labels=["python"]),
        Project("AIlice", "myshell-ai/AIlice",
                "Fully autonomous general-purpose agent; one binary, Docker-ready, for when you want \"set goal and walk away\" without a framework.",
                "slightly complex (autonomous, one binary)", labels=["python"]),
        Project("Bee Agent Framework", "i-am-bee/beeai-framework",
                "Python + TypeScript, LF AI–backed; MCP/ACP, workflows, Requirement Agent; the one that pushes \"production multi-agent\" without LangChain.",
                "complex (production multi-agent — product suite)"),
        Project("agent-squad", "2FastLabs/agent-squad",
                "AWS-originated orchestrator (now under 2FastLabs): intent classification, streaming, SupervisorAgent; \"agent-as-tools\" so one agent delegates to a squad.",
                "slightly complex (squad orchestration)"),
        Project("SuperAgentX", "superagentxai/superagentx",
                "Lightweight multi-agent orchestrator with an AGI-angle; minimal surface, docs-first, for teams that want orchestration without the kitchen sink.",
                "mostly simple (minimal surface)", labels=["python"]),
        Project("AgentVerse", "OpenBMB/AgentVerse",
                "Task-solving and simulation envs for multi-LLM agents; deploy many agents in custom environments without building infra from scratch.",
                "complex (simulation envs, multi-agent — product suite)", labels=["python"]),
        Project("R2R", "SciPhi-AI/R2R",
                "RAG-first: hybrid search, knowledge graphs, multimodal; the framework for \"production RAG\" when you care more about retrieval than chat UI.",
                "complex (production RAG — product suite)", labels=["python"]),
        Project("Google ADK", "google/adk-python",
                "Google's official Agent Development Kit: code-first Python toolkit for building, evaluating, and deploying agents. Optimized for Gemini but model-agnostic; deploys to Cloud Run / Vertex AI; ships a dev UI with eval and a code-execution sandbox.",
                "complex (official Google SDK, eval, deploy — product suite)", labels=["python"], link_name="Google ADK"),
        Project("AgentStack", "agentstack-ai/AgentStack",
                "Scaffolds full agent projects; plugs in CrewAI, LangGraph, OpenAI Swarm, LlamaStack and wires AgentOps observability from day one.",
                "slightly complex (scaffold, multi-backend)"),
        Project("AgentSilex", "howl-anderson/agentsilex",
                "~300 lines of readable agent code on top of LiteLLM; the \"I want to see the whole loop\" option for learning or minimal production.",
                "super simple (~300 LOC)", labels=["python"]),
        Project("Flowise", "FlowiseAI/Flowise",
                "Drag-and-drop LangChain UI; deploy flows without code. The low-code sibling to Langflow, with a different component and hosting story.",
                "complex (low-code, drag-drop — product suite)", oss="⚠️ Apache+CLA", labels=["javascript"]),
        Project("browser-use", "browser-use/browser-use",
                "Python layer over Playwright: natural-language goals become browser actions—web-agent loop without hand-rolling MCP or a custom driver for every site.",
                "slightly complex (LLM + browser, Playwright)", labels=["python"]),
    ],
    "multi-agent": [
        Project("openai-agents-python", "openai/openai-agents-python",
                "Handoffs, guardrails, and multi-LLM routing; minimal surface so you own the loop.",
                "mostly simple (minimal surface)", labels=["python"]),
        Project("crewAI", "crewAIInc/crewAI",
                "Role-based agents (roles, goals, backstories) in Crews; Flows add event-driven and hierarchical control for production.",
                "complex (roles, Flows, production — product suite)", labels=["python"]),
        Project("autogen", "microsoft/autogen",
                "Conversable agents and group chats; code execution and human-in-the-loop; Microsoft origin, AG2 ecosystem.",
                "complex (group chat, code exec, AG2 — product suite)", oss="✅ CC-BY", labels=["python"]),
        Project("PraisonAI", "MervinPraison/PraisonAI",
                "Autonomous multi-agent teams with a single entry point; emphasis on minimal config.",
                "mostly simple (single entry, minimal config)", labels=["python"]),
        Project("AgentRL", "THUDM/AgentRL",
                "Multitask, multiturn RL for LLM agents; Ray-based scaling, rollout/actor workers—for teams that want to train agents, not just run them.",
                "complex (RL, Ray, train agents — product suite)", labels=["python"]),
    ],
    "plugins-mcp-cli": [
        Project("aider", "Aider-AI/aider",
                "Git-aware CLI pair programmer; edits in-repo, supports multiple models and MCP so agents see version control and tools.",
                "slightly complex (CLI, git-aware, MCP)", labels=["python"]),
        Project("agentlog", "RyanAlberts/agentlog",
                "Persistent decision memory for any project: `remember`, `recall`, `reflect`. Single-file Python CLI that stores decisions as JSONL and uses Claude or Gemini to retrieve and synthesize patterns—Karpathy's LLM Wiki concept as a CLI.",
                "super simple (one file, three commands)", labels=["python"]),
        Project("claude-mem", "thedotmack/claude-mem",
                "Claude Code plugin that captures everything an agent does during a session, AI-compresses it (via claude-agent-sdk), and injects the relevant context into future sessions—session-to-session memory as a drop-in.",
                "slightly complex (session capture + compression)"),
        Project("Better-OpenCodeMCP", "ajhcs/Better-OpenCodeMCP",
                "MCP server for OpenCode/Crush: async task execution, model bridging (e.g. Claude→Gemini), process pooling.",
                "mostly simple (MCP server, model bridging)", labels=["javascript"]),
        Project("MCP Python SDK", "modelcontextprotocol/python-sdk",
                "Official SDK to build and consume MCP servers/clients in Python; stdio and SSE transports.",
                "mostly simple (SDK only)", labels=["python"]),
        Project("MCP TypeScript SDK", "modelcontextprotocol/typescript-sdk",
                "Official MCP implementation for Node/TS; reference for the protocol.",
                "mostly simple (protocol reference)", labels=["javascript"]),
        Project("continue", "continuedev/continue",
                "Open-source IDE extension (VS Code, JetBrains); in-editor completion and chat with local or API models.",
                "complex (IDE extension, multi-editor — product suite)", labels=["javascript"]),
        Project("MCP Inspector", "modelcontextprotocol/inspector",
                "GUI to test and debug MCP servers; inspect tools, resources, and prompts.",
                "super simple (debug GUI)", labels=["javascript"]),
        Project("github-mcp-server", "github/github-mcp-server",
                "GitHub's official MCP server (Go): repos, issues, PRs, code search, Actions. Replaces the older community `cyanheads/github-mcp-server` as the canonical way to give agents GitHub access.",
                "slightly complex (official GitHub MCP)"),
        Project("MCP Registry", "modelcontextprotocol/registry",
                "Official, community-driven registry for MCP servers—the \"app store\" MCP clients use to discover servers. Maintained by Anthropic + ecosystem maintainers; v0.1 API frozen, production-grade.",
                "slightly complex (official discovery layer)"),
        Project("Docker MCP Gateway", "docker/mcp-gateway",
                "Docker's official MCP CLI plugin / gateway; container-aware MCP tooling from Docker (replaces deprecated `docker/mcp-servers` path).",
                "slightly complex (Docker-aware MCPs)"),
        Project("puppeteer-real-browser-mcp", "withLinda/puppeteer-real-browser-mcp-server",
                "Puppeteer MCP with real-browser and anti-detection; for agents that need to drive sites that block headless.",
                "mostly simple (real browser, anti-detect)", oss="❓", labels=["javascript"]),
    ],
    "evaluation": [
        Project("ARC-AGI-2", "arcprize/ARC-AGI-2",
                "ARC Prize task set: grid-based abstraction/reasoning; public and private splits for generalization.",
                "super simple (task set)"),
        Project("arc-agi-benchmarking", "arcprize/arc-agi-benchmarking",
                "Runner for ARC-AGI: multi-provider (OpenAI, Anthropic, Gemini, etc.), rate limits, retries, and scoring.",
                "mostly simple (runner, multi-provider)", labels=["python"]),
        Project("AgencyBench", "GAIR-NLP/AgencyBench",
                "Long-horizon agent benchmark: 32 scenarios, 138 tasks, ~1M tokens and ~90 tool calls; Docker sandbox and rubric-based + LLM judges.",
                "complex (32 scenarios, Docker, judges — product suite)", labels=["python"]),
        Project("TRAIL", "patronus-ai/trail-benchmark",
                "Trace reasoning and agentic issue localization; 148 long-context traces, 841 errors, 20+ error types; Hugging Face dataset.",
                "mostly simple (traces, Hugging Face)"),
        Project("AgentBench", "THUDM/AgentBench",
                "ICLR'24 benchmark: agents across AlfWorld, DB, knowledge graphs, OS, webshop; Docker Compose, function-calling interface.",
                "complex (multi-env, Docker Compose — product suite)", labels=["python"]),
        Project("WebArena", "web-arena-x/webarena",
                "Realistic web env (e.g. e‑commerce, CMS, dev tools); 812 tasks; measures end-to-end web agent success.",
                "complex (812 tasks, web env — product suite)", labels=["python"]),
        Project("SWE-bench", "SWE-bench/SWE-bench",
                "LMs resolve real GitHub issues; Docker harness, instance IDs; standard for code-agent evals.",
                "slightly complex (real GitHub issues, standard)", labels=["python"]),
        Project("SWE-Gym", "SWE-Gym/SWE-Gym",
                "Training and evaluation for SWE agents and verifiers (ICML 2025).",
                "slightly complex (training + eval, ICML)", labels=["python"]),
        Project("swe-smith", "SWE-bench/SWE-smith",
                "Data generation for SWE agents; 50k+ instances across 128 repos; used for SWE-agent-LM training.",
                "slightly complex (50k+ instances, data gen)", labels=["python"]),
        Project("SUPER", "allenai/super-benchmark",
                "Agents that set up and run ML/NLP from GitHub repos; 45 expert problems, 152 masked tasks, 602 AutoGen tasks; Docker-based.",
                "slightly complex (ML/NLP repos, Docker)", labels=["python"]),
        Project("VitaBench", "meituan-longcat/vitabench",
                "ICLR'26: 66 tools, real-world apps (delivery, travel, retail); 100 cross-scenario + 300 single-scenario tasks; adopted by Qwen/Seed.",
                "complex (66 tools, cross-scenario — product suite)"),
        Project("letta-evals", "letta-ai/letta-evals",
                "Eval harness for stateful Letta agents; configurable suites and grading (LLM or rule-based) so you can measure what you ship.",
                "mostly simple (Letta-specific harness)", labels=["python"]),
        Project("WebVoyager", "MinorJerry/WebVoyager",
                "End-to-end web agent with LMMs: screenshots + actions on real sites; benchmark on 15 sites, GPT-4V for automatic eval.",
                "slightly complex (LMMs, screenshots, 15 sites)"),
        Project("inspect_evals", "UKGovernmentBEIS/inspect_evals",
                "UK AISI/Arcadia/Vector: GAIA and other evals in Inspect AI; level 1–3, sandboxed, tool-calling solvers.",
                "slightly complex (Inspect AI, UK gov)"),
        Project("inspect_ai", "UKGovernmentBEIS/inspect_ai",
                "Inspect AI core: composable eval tasks, sandboxes, scorers, and multi-model runs; the framework behind inspect_evals, not just the task bundle.",
                "complex (eval framework, AISI stack — product suite)", labels=["python"]),
        Project("Agent Lightning", "microsoft/agent-lightning",
                "Microsoft's training-oriented harness: optimization loops for agent behavior—when you need to improve policies over rollouts, not only score a fixed prompt.",
                "complex (agent training, Microsoft stack — product suite)", labels=["python"]),
    ],
    "research-task": [
        Project("gpt-researcher", "assafelovic/gpt-researcher",
                "Autonomous deep-research agent: web + local sources, citation-grounded reports, multi-agent and deep-research modes. The reference open-source research harness.",
                "complex (deep research, multi-agent — product suite)", labels=["python"]),
        Project("openagents", "OpenAgentsInc/openagents",
                "Platform for autonomous agents and autopilot-style workflows; decentralized/Nostr-oriented (Pylon runtime, actively shipped in 2026).",
                "complex (platform, decentralized — product suite)"),
    ],
    "libraries-sdks": [
        Project("deepagents", "langchain-ai/deepagents",
                "LangChain's Python+TypeScript agent harness on top of LangGraph: planning tool, virtual filesystem, shell sandbox, sub-agent spawning—the \"Claude Code-style\" harness as a reusable library.",
                "slightly complex (planning, files, sub-agents)", labels=["python"]),
        Project("pydantic-ai", "pydantic/pydantic-ai",
                "Type-safe Python agents with Pydantic I/O; multi-provider, MCP, Logfire observability, and human-in-the-loop.",
                "slightly complex (type-safe, MCP, Logfire)", labels=["python"]),
        Project("open-harness", "MaxGfeller/open-harness",
                "TypeScript Agent class on Vercel AI SDK; streaming events, filesystem/bash tools, MCP, and subagent delegation.",
                "slightly complex (streaming, tools, subagents)", labels=["javascript"]),
        Project("vercel/ai", "vercel/ai",
                "React and Node SDK for streaming, tool calls, and agent-style UIs; provider-agnostic.",
                "slightly complex (React/Node SDK, provider-agnostic)", labels=["javascript"]),
        Project("smolagents", "huggingface/smolagents",
                "Code-as-action agents: model outputs Python executed in sandbox (E2B, Modal, etc.); ~1k LOC core.",
                "mostly simple (code-as-action, ~1k LOC)", labels=["python"]),
        Project("strands-agents", "strands-agents/sdk-python",
                "Model-driven Python SDK; decorators for tools, native MCP, multi-agent; \"minimal code\" without sacrificing provider choice.",
                "mostly simple (decorators, MCP, minimal code)", labels=["python"]),
        Project("openai-agents-js", "openai/openai-agents-js",
                "Official OpenAI Agents SDK for Node/TS: handoffs, guardrails, voice; the JS counterpart to openai-agents-python.",
                "slightly complex (handoffs, guardrails, voice)", labels=["javascript"]),
        Project("LiteLLM", "BerriAI/litellm",
                "One interface to 100+ LLMs; routing, caching, budgets. Not an agent framework—the pipe every agent framework uses.",
                "mostly simple (LLM pipe only)", labels=["python"]),
        Project("Composio", "ComposioHQ/composio",
                "1,000+ toolkits with auth, tool search, and a sandboxed workbench—drop-in tool layer so agents stop reinventing OAuth + integrations. Python and TypeScript.",
                "complex (1k+ tools, auth, search — product suite)"),
        Project("Mem0", "mem0ai/mem0",
                "Universal memory layer for AI agents: stores user/org/session memory, retrieves on demand. Apache-2.0; the de-facto memory primitive paired with most harnesses in 2026.",
                "slightly complex (memory layer, multi-platform)", labels=["python"]),
        Project("Cloudflare Agents", "cloudflare/agents",
                "Persistent, stateful agents on Durable Objects: state, websockets, scheduling, and AI chat baked in. The serverless answer to \"where does the agent live?\"",
                "slightly complex (Durable Objects, stateful)", labels=["javascript"]),
        Project("E2B", "e2b-dev/E2B",
                "Firecracker sandboxes for executing agent-generated code; the hosted isolation layer many tool-calling demos use instead of running arbitrary LLM output on your laptop.",
                "slightly complex (sandbox API, code execution)", labels=["python"]),
        Project("Daytona", "daytonaio/daytona",
                "Elastic dev environments for AI-generated code: workspaces, Git, previews—infra harness between \"the model wrote a patch\" and \"it ran in a real machine.\"",
                "slightly complex (dev env API, isolation)"),
        Project("Community-curated agent lists", "brandonhimpfen/awesome-ai-agents",
                "Broader directories: e.g. [brandonhimpfen/awesome-ai-agents](https://github.com/brandonhimpfen/awesome-ai-agents), [axioma-ai-labs/awesome-ai-agent-frameworks](https://github.com/axioma-ai-labs/awesome-ai-agent-frameworks), [mb-mal/awesome-ai-agents-frameworks](https://github.com/mb-mal/awesome-ai-agents-frameworks)—differ by scope and update cadence.",
                "super simple (curated lists)", oss="❓"),
    ],
}

# Fill in Roo-Code description that was empty
PROJECTS["coding-agent-products"][1].description = (
    "VS Code/Cursor extension in the Cline lineage. The **harness** is the approval-gated agent with custom modes and a strong MCP story; the IDE is the UI. Popular community fork when you want that workflow without the upstream extension."
)


# Stars + examples link, keyed by github_id (post-move where applicable).
# Star counts captured 2026-05-19 from the GitHub API; refresh by re-running
# scripts/fetch_metadata.py (or the inline batched search_repositories calls).
# Examples link: official docs, examples folder, leaderboard, or paper —
# whichever is the most useful "show me it in action" link for that project.
META: dict[str, tuple[int, str, str]] = {
    # progressive-disclosure
    "agentsmd/agents.md": (21487, "https://github.com/agentsmd/agents.md/blob/main/AGENTS.md", "Self-hosting AGENTS.md"),
    "PatrickJS/awesome-cursorrules": (39563, "https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/pytorch-scikit-learn-cursorrules-prompt-file.mdc", "PyTorch cursorrules"),
    "xfey/MCP-Zero": (483, "https://github.com/xfey/MCP-Zero/blob/master/MCP-zero/experiment_apibank.py", "APIBank experiment"),
    "langchain-ai/langgraph-bigtool": (537, "https://github.com/langchain-ai/langgraph-bigtool#quickstart", "Math-library tool agent"),
    "spring-ai-community/spring-ai-tool-search-tool": (70, "https://github.com/spring-ai-community/spring-ai-tool-search-tool/tree/main/examples/tool-search-tool-demo", "Tool Search demo app"),
    "Reason-Wang/ToolGen": (178, "https://github.com/Reason-Wang/ToolGen/blob/master/scripts/eval_full_pipeline.sh", "Full eval pipeline"),
    "antl3x/ToolRAG": (25, "https://github.com/antl3x/ToolRAG/blob/main/packages/%40antl3x-toolrag/README.md", "MCP server retrieval"),
    # coding-agent-products
    "cline/cline": (61982, "https://docs.cline.bot/features/plan-and-act", "Plan & Act mode"),
    "RooCodeInc/Roo-Code": (24100, "https://docs.roocode.com/features/custom-modes", "Custom modes guide"),
    "openai/codex": (83556, "https://developers.openai.com/codex/concepts/sandboxing", "Sandboxing concept"),
    "google-gemini/gemini-cli": (104261, "https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md", "MCP server setup"),
    "charmbracelet/crush": (24388, "https://charm.land/blog/crush-comes-home/", "Crush launch post"),
    "anomalyco/opencode": (162190, "https://opencode.ai/docs/agents/", "Agent system page"),
    "OpenHands/OpenHands": (74003, "https://docs.all-hands.dev/usage/prompting/microagents-repo", "Repository microagents"),
    "aaif-goose/goose": (45481, "https://block.github.io/goose/docs/guides/recipes/", "Goose recipes guide"),
    "HarnessLab/claw-code-agent": (482, "https://github.com/HarnessLab/claw-code-agent#-quick-start", "Quick Start guide"),
    "SeanHogg/coderClaw": (3, "https://github.com/SeanHogg/coderClaw#readme", "Multi-agent README"),
    # coding-harness-configs
    "gsd-build/get-shit-done": (62931, "https://github.com/gsd-build/get-shit-done/blob/main/commands/gsd/ship.md", "gsd:ship command"),
    "garrytan/gstack": (99093, "https://github.com/garrytan/gstack/blob/main/ship/SKILL.md", "/ship SKILL.md"),
    "affaan-m/everything-claude-code": (186548, "https://github.com/affaan-m/everything-claude-code/blob/main/skills/autonomous-agent-harness/SKILL.md", "autonomous-agent-harness skill"),
    "obra/superpowers": (196763, "https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md", "TDD skill"),
    "RyanAlberts/pmstack": (1, "https://github.com/RyanAlberts/pmstack/blob/main/skills/prd-from-signal.md", "PRD-from-signal skill"),
    "anthropics/claude-agent-sdk-python": (6932, "https://github.com/anthropics/claude-agent-sdk-demos/blob/main/research-agent/research_agent/agent.py", "Research agent demo"),
    "aiming-lab/AutoHarness": (280, "https://github.com/aiming-lab/AutoHarness/blob/main/examples/full_pipeline_demo.py", "Full pipeline demo"),
    "QuantaAlpha/RepoMaster": (522, "https://github.com/QuantaAlpha/RepoMaster/blob/main/example/pdf_parse.md", "PDF-parse case study"),
    "SWE-agent/SWE-agent": (19241, "https://github.com/SWE-agent/SWE-agent/blob/main/config/default.yaml", "Default agent config"),
    "HKUDS/OpenHarness": (12698, "https://github.com/HKUDS/OpenHarness/blob/main/.claude/skills/harness-eval/SKILL.md", "harness-eval skill"),
    "anthropics/skills": (137005, "https://github.com/anthropics/skills/blob/main/skills/docx/SKILL.md", "docx skill"),
    # frameworks
    "langchain-ai/langgraph": (32357, "https://github.com/langchain-ai/langgraph/blob/main/examples/customer-support/customer-support.ipynb", "Customer support agent"),
    "langchain-ai/langchain": (137048, "https://github.com/langchain-ai/langchain-academy/blob/main/module-1/agent.ipynb", "Build an agent notebook"),
    "run-llama/llama_index": (49495, "https://github.com/run-llama/llama_index/blob/main/docs/examples/agent/agent_workflow_research_assistant.ipynb", "Research assistant workflow"),
    "microsoft/semantic-kernel": (27933, "https://github.com/microsoft/semantic-kernel/blob/main/python/samples/getting_started_with_agents/chat_completion/step01_chat_completion_agent_simple.py", "Chat completion agent"),
    "mastra-ai/mastra": (24010, "https://github.com/mastra-ai/mastra/tree/main/examples/durable-agents", "Durable research agent"),
    "agno-agi/agno": (40187, "https://github.com/agno-agi/agno/blob/main/cookbook/02_agents/01_quickstart/agent_with_tools.py", "Agent with tools"),
    "letta-ai/letta": (22791, "https://github.com/letta-ai/agent-file/tree/main/agents/%40letta-ai/loop", "Loop .af agent file"),
    "langflow-ai/langflow": (148459, "https://github.com/langflow-ai/langflow/blob/main/docs/docs/Tutorials/chat-with-rag.mdx", "Chat with RAG flow"),
    "RasaHQ/rasa": (21172, "https://github.com/RasaHQ/rasa-demo", "Sara conversational demo"),
    "botpress/botpress": (14697, "https://github.com/botpress/v12/tree/master/examples/interbot", "Inter-bot delegation"),
    "langgenius/dify": (141806, "https://github.com/langgenius/dify-docs/blob/main/en/use-dify/tutorials/customer-service-bot.mdx", "Customer-service bot"),
    "n8n-io/n8n": (188586, "https://github.com/n8n-io/n8n-docs/blob/main/docs/advanced-ai/examples/agent-chain-comparison.md", "Agent vs chain workflow"),
    "Significant-Gravitas/AutoGPT": (184401, "https://github.com/Significant-Gravitas/AutoGPT/blob/master/autogpt_platform/graph_templates/Medium%20Blogger_v28.json", "Medium blogger graph"),
    "myshell-ai/AIlice": (1409, "https://github.com/myshell-ai/AIlice#cool-things-we-can-do", "Task showcase"),
    "i-am-bee/beeai-framework": (3259, "https://github.com/i-am-bee/beeai-framework/blob/main/python/examples/agents/react.py", "ReAct agent example"),
    "2FastLabs/agent-squad": (7630, "https://github.com/2FastLabs/agent-squad/tree/main/examples/ecommerce-support-simulator", "E-commerce support sim"),
    "superagentxai/superagentx": (195, "https://github.com/superagentxai/superagentx/blob/master/examples/agents/parallel_agents.py", "Parallel marketing agents"),
    "OpenBMB/AgentVerse": (5038, "https://github.com/OpenBMB/AgentVerse/blob/main/agentverse/tasks/simulation/nlp_classroom_9players/config.yaml", "NLP classroom sim"),
    "SciPhi-AI/R2R": (7837, "https://github.com/SciPhi-AI/R2R/blob/main/py/core/examples/hello_r2r.py", "hello_r2r RAG example"),
    "google/adk-python": (19706, "https://github.com/google/adk-samples/tree/main/python/agents/travel-concierge", "Travel concierge agent"),
    "agentstack-ai/AgentStack": (2154, "https://github.com/agentstack-ai/AgentStack/tree/main/examples/research_assistant", "Research assistant crew"),
    "howl-anderson/agentsilex": (450, "https://github.com/howl-anderson/agentsilex/blob/main/demo/simple_agent.py", "Simple weather agent"),
    "FlowiseAI/Flowise": (52919, "https://github.com/FlowiseAI/Flowise/blob/main/packages/server/marketplaces/agentflowsv2/Agentic%20RAG.json", "Agentic RAG flow"),
    "browser-use/browser-use": (94517, "https://github.com/browser-use/browser-use/blob/main/examples/use-cases/shopping.py", "Grocery shopping agent"),
    # multi-agent
    "openai/openai-agents-python": (26440, "https://github.com/openai/openai-agents-python/blob/main/examples/customer_service/main.py", "Airline customer service handoffs"),
    "crewAIInc/crewAI": (51670, "https://github.com/crewAIInc/crewAI-examples/blob/main/crews/trip_planner/trip_agents.py", "Trip planner crew"),
    "microsoft/autogen": (58149, "https://github.com/microsoft/autogen/tree/main/python/samples/core_distributed-group-chat", "Distributed group chat"),
    "MervinPraison/PraisonAI": (7823, "https://github.com/MervinPraison/PraisonAI/blob/main/examples/python/general/orchestrator-workers.py", "Orchestrator-workers pattern"),
    "THUDM/AgentRL": (286, "https://github.com/THUDM/AgentRL/blob/main/examples/training/async_trainer.py", "Async GRPO trainer"),
    # plugins-mcp-cli
    "Aider-AI/aider": (44989, "https://github.com/Aider-AI/aider/blob/main/aider/repomap.py", "Repo map source"),
    "RyanAlberts/agentlog": (0, "https://github.com/RyanAlberts/agentlog/blob/main/example-log/decisions.jsonl", "Sample decisions.jsonl"),
    "thedotmack/claude-mem": (76591, "https://github.com/thedotmack/claude-mem/blob/main/plugin/hooks/hooks.json", "Lifecycle hooks config"),
    "ajhcs/Better-OpenCodeMCP": (6, "https://github.com/ajhcs/Better-OpenCodeMCP/blob/main/src/tools/opencode.tool.ts", "opencode delegate tool"),
    "modelcontextprotocol/python-sdk": (23053, "https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/servers/simple-tool/mcp_simple_tool/server.py", "Website fetcher server"),
    "modelcontextprotocol/typescript-sdk": (12460, "https://github.com/modelcontextprotocol/typescript-sdk/blob/main/examples/server/src/simpleStreamableHttp.ts", "Streamable HTTP server"),
    "continuedev/continue": (33257, "https://github.com/continuedev/continue/blob/main/extensions/vscode/README.md", "VS Code extension demos"),
    "modelcontextprotocol/inspector": (9799, "https://github.com/modelcontextprotocol/inspector/blob/main/README.md", "Inspector UI walkthrough"),
    "github/github-mcp-server": (29957, "https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md", "Remote server toolsets"),
    "modelcontextprotocol/registry": (6830, "https://github.com/modelcontextprotocol/registry/blob/main/data/seed.json", "Registry seed entries"),
    "docker/mcp-gateway": (1394, "https://github.com/docker/mcp-gateway/blob/main/docs/mcp-gateway.md", "Gateway usage walkthrough"),
    "withLinda/puppeteer-real-browser-mcp-server": (22, "https://github.com/withLinda/puppeteer-real-browser-mcp-server/blob/main/README.md", "11 anti-detection tools"),
    # evaluation
    "arcprize/ARC-AGI-2": (700, "https://arcprize.org/leaderboard", "ARC Prize leaderboard"),
    "arcprize/arc-agi-benchmarking": (350, "https://github.com/arcprize/arc-agi-benchmarking/blob/main/docs/examples/prompt_example_o3.md", "o3 prompt example"),
    "GAIR-NLP/AgencyBench": (84, "https://github.com/GAIR-NLP/AgencyBench#leaderboard", "AgencyBench leaderboard"),
    "patronus-ai/trail-benchmark": (18, "https://huggingface.co/datasets/PatronusAI/TRAIL", "TRAIL dataset card"),
    "THUDM/AgentBench": (3429, "https://arxiv.org/abs/2308.03688", "AgentBench ICLR'24 paper"),
    "web-arena-x/webarena": (1475, "https://docs.google.com/spreadsheets/d/1M801lEpBbKSNwP-vDBkC_pF7LdyGU1f_ufZb_NWNBZQ/edit", "WebArena leaderboard"),
    "SWE-bench/SWE-bench": (4968, "https://www.swebench.com/verified.html", "SWE-bench Verified leaderboard"),
    "SWE-Gym/SWE-Gym": (678, "https://arxiv.org/abs/2412.21139", "SWE-Gym ICML 2025 paper"),
    "SWE-bench/SWE-smith": (649, "https://huggingface.co/datasets/SWE-bench/SWE-smith-trajectories", "SWE-smith trajectories"),
    "allenai/super-benchmark": (52, "https://arxiv.org/abs/2409.07440", "SUPER EMNLP paper"),
    "meituan-longcat/vitabench": (132, "https://arxiv.org/abs/2509.26490", "VitaBench paper"),
    "letta-ai/letta-evals": (71, "https://github.com/letta-ai/letta-leaderboard/blob/main/leaderboard/locomo/locomo_benchmark.py", "LoCoMo memory benchmark"),
    "MinorJerry/WebVoyager": (1087, "https://github.com/MinorJerry/WebVoyager/blob/main/data/WebVoyager_data.jsonl", "643 web tasks dataset"),
    "UKGovernmentBEIS/inspect_evals": (500, "https://github.com/UKGovernmentBEIS/inspect_evals/blob/main/src/inspect_evals/swe_bench/README.md", "inspect SWE-bench eval"),
    "UKGovernmentBEIS/inspect_ai": (2076, "https://inspect.aisi.org.uk/tutorial.html", "Inspect tutorial example"),
    "microsoft/agent-lightning": (17193, "https://github.com/microsoft/agent-lightning/blob/main/examples/apo/README.md", "APO room-booking example"),
    # research-task
    "assafelovic/gpt-researcher": (27131, "https://github.com/assafelovic/gpt-researcher/blob/master/docs/blog/2024-05-19-gptr-langgraph/index.md", "Multi-agent LangGraph walkthrough"),
    "OpenAgentsInc/openagents": (419, "https://github.com/OpenAgentsInc/openagents/blob/main/docs/reports/nexus/2026-04-23-autopilot-pylon-production-earning-proof.md", "Production earning proof"),
    # libraries-sdks
    "langchain-ai/deepagents": (22954, "https://github.com/langchain-ai/deepagents/tree/main/examples/deep_research", "Deep research agent"),
    "pydantic/pydantic-ai": (17131, "https://github.com/pydantic/pydantic-ai/blob/main/examples/pydantic_ai_examples/bank_support.py", "Bank support agent"),
    "MaxGfeller/open-harness": (518, "https://github.com/MaxGfeller/open-harness/tree/main/examples/cli", "Terminal CLI agent"),
    "vercel/ai": (24315, "https://github.com/vercel/ai/tree/main/examples/next-agent", "Next.js agent example"),
    "huggingface/smolagents": (27377, "https://github.com/huggingface/smolagents/blob/main/examples/rag.py", "RAG code agent"),
    "strands-agents/sdk-python": (5884, "https://github.com/strands-agents/samples/tree/main/python/01-learn/01-first-agent", "First agent tutorial"),
    "openai/openai-agents-js": (3054, "https://github.com/openai/openai-agents-js/tree/main/examples/financial-research-agent", "Financial research agent"),
    "BerriAI/litellm": (47469, "https://github.com/BerriAI/litellm/blob/main/cookbook/anthropic_agent_sdk/main.py", "Anthropic Agent SDK gateway"),
    "ComposioHQ/composio": (28328, "https://github.com/ComposioHQ/composio#quick-start", "HackerNews agent quickstart"),
    "mem0ai/mem0": (56055, "https://github.com/mem0ai/mem0/tree/main/examples/mem0-demo", "Next.js memory demo"),
    "cloudflare/agents": (4928, "https://github.com/cloudflare/agents/tree/main/examples/playground", "SDK playground app"),
    "e2b-dev/E2B": (12238, "https://github.com/e2b-dev/e2b-cookbook/tree/main/examples/anthropic-claude-code-in-sandbox-python", "Claude Code in sandbox"),
    "daytonaio/daytona": (72441, "https://github.com/daytonaio/daytona/tree/main/examples/python/charts", "Charts in sandbox"),
    "brandonhimpfen/awesome-ai-agents": (11, "https://github.com/brandonhimpfen/awesome-ai-agents#frameworks", "Frameworks section"),
}


def stars_for(github_id: str) -> int:
    return META.get(github_id, (0, "", ""))[0]


def examples_for(github_id: str) -> str:
    return META.get(github_id, (0, "", ""))[1] or f"https://github.com/{github_id}#readme"


def example_label_for(github_id: str) -> str:
    return META.get(github_id, (0, "", ""))[2] or "Examples"


def format_stars(n: int) -> str:
    if n >= 1000:
        if n >= 100000:
            return f"{round(n/1000)}k"
        return f"{n/1000:.1f}k".replace(".0k", "k")
    return str(n)


def generate_yaml() -> str:
    lines = [
        "configuration:",
        "  min_stars: 0",
        "  min_projectrank: 0",
        "  require_github: True",
        "  allowed_licenses: [\"all\"]",
        "  hide_project_license: True",
        "  markdown_header_file: \"config/header.md\"",
        "  markdown_footer_file: \"config/footer.md\"",
        "  projects_history_folder: \"history\"",
        "",
        "categories:",
    ]
    for cat_id, title, subtitle in CATEGORIES:
        lines.append(f"  - category: \"{cat_id}\"")
        lines.append(f"    title: \"{title}\"")
        safe_sub = subtitle.replace('"', '\\"')
        lines.append(f"    subtitle: \"{safe_sub}\"")
    lines += [
        "",
        "labels:",
        "  - label: \"python\"",
        "    image: \"https://www.python.org/static/favicon.ico\"",
        "    description: \"Python-based\"",
        "  - label: \"javascript\"",
        "    image: \"https://cdn.icon-icons.com/icons2/2108/PNG/512/javascript_icon_130900.png\"",
        "    description: \"JavaScript/TypeScript-based\"",
        "",
        "projects:",
    ]
    for cat_id, title, _ in CATEGORIES:
        lines.append(f"  # {title}")
        for p in PROJECTS[cat_id]:
            lines.append(f"  - name: {p.name}")
            lines.append(f"    github_id: {p.github_id}")
            if p.labels:
                lbls = ", ".join(f'"{l}"' for l in p.labels)
                lines.append(f"    labels: [{lbls}]")
            lines.append(f"    category: \"{cat_id}\"")
    lines.append("")
    return "\n".join(lines)


def count_projects() -> int:
    return sum(len(PROJECTS[c]) for c, _, _ in CATEGORIES)


def generate_readme() -> str:
    total = count_projects()
    header = [
        "<!-- markdownlint-disable -->",
        "<h1 align=\"center\">",
        "    Best of Agent Harnesses and Harness Techniques",
        "    <br>",
        "</h1>",
        "",
        "<p align=\"center\">",
        "    <strong>🏆&nbsp; Curated list of AI agent harnesses, orchestration frameworks, and harness techniques for reliable agentic systems.</strong>",
        "</p>",
        "",
        "<p align=\"center\">",
        "    <a href=\"https://best-of.org\" title=\"Best-of Badge\"><img src=\"http://bit.ly/3o3EHNN\"></a>",
        f"    <a href=\"#contents\" title=\"Project Count\"><img src=\"https://img.shields.io/badge/projects-{total}-blue.svg?color=5ac4bf\"></a>",
        "    <a href=\"#contribution\" title=\"Contributions welcome\"><img src=\"https://img.shields.io/badge/contributions-welcome-green.svg\"></a>",
        "    <a href=\"https://github.com/RyanAlberts/best-of-Agent-Harnesses/releases\" title=\"Updates\"><img src=\"https://img.shields.io/github/release-date/RyanAlberts/best-of-Agent-Harnesses?color=green&label=updated\"></a>",
        "</p>",
        "",
        "## What is an agent harness?",
        "",
        "An agent harness is the runtime that closes the loop between a stateless model and the outside world—managing perception, action, memory, and constraint enforcement—making it the de facto operating system of machine agency and, consequently, the layer where nearly all meaningful questions about AI autonomy, reliability, and control are actually resolved.",
        "",
        "Every prior wave of automation was constrained by brittleness: you scripted exact behavior, and when the world deviated, the system broke. Foundation models inverted that problem—they're flexible but directionless, stateless, and disconnected from anything real. The agent harness exists to bridge that gap: it is the orchestration infrastructure that converts a model's per-turn reasoning into sustained, tool-using, error-recovering, goal-directed behavior across time. Architecturally, it plays the role the kernel played in operating systems or the controller played in industrial robotics—mediating between raw capability and a messy environment—but with a critical difference: the \"capability\" it governs is general-purpose cognition, which means the harness is simultaneously a scheduler, a permission system, a memory manager, and a policy enforcement layer, all under-specified and evolving in real time. The term itself barely exists in formal literature yet, which should concern anyone who cares about AI governance, because the harness is where abstract alignment goals either get operationalized into concrete constraints or quietly don't.",
        "",
        "## Why harnesses matter",
        "",
        "Better models make harnesses more important: more capabilities mean more failure modes, and production needs retry logic, fallbacks, and validation. Harness quality—not just model quality—determines whether agents actually ship. This list ranks projects by relevance to harness concerns (environment, orchestration, lifecycle, guardrails) and by stars/activity.",
        "",
        "## Contents",
        "",
    ]
    def slug(s: str) -> str:
        s = s.lower()
        s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
        s = re.sub(r"\s+", "-", s)
        s = re.sub(r"-+", "-", s).strip("-")
        return s
    for cat_id, title, _ in CATEGORIES:
        count = len(PROJECTS[cat_id])
        anchor = slug(title)
        header.append(f"- [{title}](#{anchor}) _{count} projects_")
    header += [
        "",
        "## Explanation",
        "",
        "- **⭐ Stars:** GitHub star count, captured 2026-05-19. Each table is sorted by stars descending. Click a star count to jump to the GitHub repo's stargazers page.",
        "- **Examples:** One concrete instance of the harness in action — a specific skill file, demo script, sample agent, leaderboard with scores, or feature walkthrough — not a docs root or examples index. The link text names what's at the link.",
        "- **Simplicity ↔ capability:** Where each project sits on a 4-tier scale describing how much surface area you take on when adopting it: **super simple** (format-only, single file, one concept) → **mostly simple** (lean API, thin layer over a primitive) → **slightly complex** (multi-file SDK, several knobs, real abstractions) → **complex (product suite)** (platform with its own runtime, UI, ecosystem).",
        "- **Open source:** ✅ = standard open-source license (MIT/Apache/BSD/GPL/MPL/AGPL/CC0). ⚠️ = source-available or restricted (e.g. n8n Fair-code, Elastic-2.0, Polyform). ❓ = no license file or unclear terms.",
        "",
        "<br>",
        "",
    ]
    body = list(header)
    for cat_id, title, subtitle in CATEGORIES:
        body.append(f"## {title}")
        body.append("")
        body.append("<a href=\"#contents\"><img align=\"right\" width=\"15\" height=\"15\" src=\"https://git.io/JtehR\" alt=\"Back to top\"></a>")
        body.append("")
        body.append(f"_{subtitle}_")
        body.append("")
        body.append("| # | Project | ⭐ Stars | Description | Open source | Simplicity ↔ capability | Examples |")
        body.append("|---|---------|---------|-------------|-------------|-------------------------|----------|")
        sorted_projects = sorted(PROJECTS[cat_id], key=lambda x: stars_for(x.github_id), reverse=True)
        for i, p in enumerate(sorted_projects, 1):
            stars = stars_for(p.github_id)
            stars_cell = f"[{format_stars(stars)}](https://github.com/{p.github_id}/stargazers)"
            examples_cell = f"[{example_label_for(p.github_id)}]({examples_for(p.github_id)})"
            row = f"| {i} | [**{p.display_name}**](https://github.com/{p.github_id}) | {stars_cell} | {p.description} | {p.oss} | {p.axis} | {examples_cell} |"
            body.append(row)
        body.append("")
    body += [
        "<br>",
        "",
        "---",
        "",
        "## Related Resources",
        "",
        "- [**Awesome**](https://github.com/sindresorhus/awesome): Awesome lists on many topics",
        "- [**OpenAI – Harness engineering**](https://openai.com/index/harness-engineering/): Environment design, intent, feedback loops, repo-as-system-of-record",
        "- [**Anthropic – Effective harnesses for long-running agents**](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): Session bridging, feature lists, incremental progress, testing",
        "- [**Aakash Gupta (Medium) – 2026 is agent harnesses**](https://aakashgupta.medium.com/2025-was-agents-2026-is-agent-harnesses-heres-why-that-changes-everything-073e9877655e): Harness as moat, minimal intervention, progressive disclosure",
        "- [**LangChain**](https://python.langchain.com/), [**Anthropic**](https://docs.anthropic.com/), [**OpenAI**](https://platform.openai.com/docs): Official docs for major agent platforms",
        "",
        "## Contribution",
        "",
        "Contributions are welcome. To add or suggest projects:",
        "",
        "- Open an [issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues) with the repo URL, category, and a short description.",
        "- Or submit a [pull request](https://github.com/RyanAlberts/best-of-Agent-Harnesses/pulls) editing [projects.yaml](https://github.com/RyanAlberts/best-of-Agent-Harnesses/blob/main/projects.yaml) (and optionally README.md).",
        "",
        "For contribution guidelines, see [CONTRIBUTING.md](https://github.com/RyanAlberts/best-of-Agent-Harnesses/blob/main/CONTRIBUTING.md) and the [Code of Conduct](https://github.com/RyanAlberts/best-of-Agent-Harnesses/blob/main/.github/CODE_OF_CONDUCT.md).",
        "",
        "## License",
        "",
        "[![CC BY-SA 4.0](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)](https://creativecommons.org/licenses/by-sa/4.0/)",
        "",
    ]
    return "\n".join(body)


def generate_header_md() -> str:
    total = count_projects()
    return (
        "<!-- markdownlint-disable -->\n"
        "<h1 align=\"center\">\n"
        "    Best of Agent Harnesses and Harness Techniques\n"
        "    <br>\n"
        "</h1>\n"
        "\n"
        "<p align=\"center\">\n"
        "    <strong>🏆&nbsp; Curated list of AI agent harnesses, orchestration frameworks, and harness techniques for reliable agentic systems.</strong>\n"
        "</p>\n"
        "\n"
        "<p align=\"center\">\n"
        "    <a href=\"https://best-of.org\" title=\"Best-of Badge\"><img src=\"http://bit.ly/3o3EHNN\"></a>\n"
        f"    <a href=\"#contents\" title=\"Project Count\"><img src=\"https://img.shields.io/badge/projects-{total}-blue.svg?color=5ac4bf\"></a>\n"
        "    <a href=\"#contribution\" title=\"Contributions welcome\"><img src=\"https://img.shields.io/badge/contributions-welcome-green.svg\"></a>\n"
        "    <a href=\"https://github.com/RyanAlberts/best-of-Agent-Harnesses/releases\" title=\"Updates\"><img src=\"https://img.shields.io/github/release-date/RyanAlberts/best-of-Agent-Harnesses?color=green&label=updated\"></a>\n"
        "</p>\n"
        "\n"
        "## What is an agent harness?\n"
        "\n"
        "An agent harness is the runtime that closes the loop between a stateless model and the outside world—managing perception, action, memory, and constraint enforcement—making it the de facto operating system of machine agency and, consequently, the layer where nearly all meaningful questions about AI autonomy, reliability, and control are actually resolved.\n"
        "\n"
        "Every prior wave of automation was constrained by brittleness: you scripted exact behavior, and when the world deviated, the system broke. Foundation models inverted that problem—they're flexible but directionless, stateless, and disconnected from anything real. The agent harness exists to bridge that gap: it is the orchestration infrastructure that converts a model's per-turn reasoning into sustained, tool-using, error-recovering, goal-directed behavior across time. Architecturally, it plays the role the kernel played in operating systems or the controller played in industrial robotics—mediating between raw capability and a messy environment—but with a critical difference: the \"capability\" it governs is general-purpose cognition, which means the harness is simultaneously a scheduler, a permission system, a memory manager, and a policy enforcement layer, all under-specified and evolving in real time. The term itself barely exists in formal literature yet, which should concern anyone who cares about AI governance, because the harness is where abstract alignment goals either get operationalized into concrete constraints or quietly don't.\n"
        "\n"
        "If you want to add or update projects, open an [issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues), submit a [pull request](https://github.com/RyanAlberts/best-of-Agent-Harnesses/pulls), or edit [projects.yaml](https://github.com/RyanAlberts/best-of-Agent-Harnesses/blob/main/projects.yaml). Contributions are welcome!\n"
    )


def main():
    yaml_content = generate_yaml()
    readme_content = generate_readme()
    header_content = generate_header_md()
    (REPO_ROOT / "projects.yaml").write_text(yaml_content)
    (REPO_ROOT / "README.md").write_text(readme_content)
    (REPO_ROOT / "config" / "header.md").write_text(header_content)
    print(f"Wrote {count_projects()} projects across {len(CATEGORIES)} categories.")
    for cat_id, title, _ in CATEGORIES:
        print(f"  {title}: {len(PROJECTS[cat_id])}")


if __name__ == "__main__":
    main()
