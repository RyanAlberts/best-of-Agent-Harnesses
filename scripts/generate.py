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
    extra_tags: list = field(default_factory=list)  # manual tag overrides/additions

    @property
    def display_name(self) -> str:
        return self.link_name or self.name

    @property
    def tags(self) -> list:
        return auto_tag(self)


# Canonical tag vocabulary, ordered by discriminative value (most useful first).
# Tags are auto-derived from each project's description + axis + labels via the
# patterns below. Add to extra_tags=[...] on a Project to force a tag in.
TAG_RULES: "list[tuple[str, list[str]]]" = [
    ("mcp",            [r"\bMCP\b", r"Model Context Protocol", r"MCPs"]),
    ("memory",         [r"\bmemory\b", r"session(?:\s+bridging|s| capture)", r"persist(?:ent|ence)", r"long-horizon", r"stateful"]),
    ("multi-agent",    [r"multi[- ]agent", r"\bcrew\b", r"\bswarm\b", r"\bsquad\b", r"sub[- ]?agent", r"\bhandoffs?\b", r"group chat"]),
    ("evals",          [r"\beval(?:s|uation)?\b", r"benchmark", r"SWE-bench", r"scor(?:e|ing)", r"trace reasoning", r"judges?\b"]),
    ("voice",          [r"\bvoice\b"]),
    ("vision",         [r"\bvision\b", r"screenshots?", r"\bLMM[Ss]?\b", r"GPT-4V", r"\bmultimodal\b"]),
    ("browser",        [r"\bbrowser\b", r"Playwright", r"[Pp]uppeteer", r"headless"]),
    ("sandbox",        [r"sandbox", r"\bDocker(?:ized)?\b", r"\bE2B\b", r"Firecracker", r"isolat(?:ed|ion)"]),
    ("low-code",       [r"low-code", r"drag[- ]?drop", r"visual (?:DAG|workflow|bot|builder)", r"no-code", r"\bDAG\b"]),
    ("rag",            [r"\bRAG\b", r"retrieval[- ](?:augmented|first)", r"hybrid search", r"knowledge graph"]),
    ("tool-discovery", [r"tool (?:discovery|retrieval|routing|search)", r"on-demand tool", r"semantic routing"]),
    ("training",       [r"\btraining\b", r"\bRL\b", r"reinforcement", r"rollout", r"train (?:agents|policies)"]),
    ("workflow",       [r"\bworkflow\b", r"state[- ]machine", r"checkpointing", r"durable exec", r"graphs?\b"]),
    ("typed",          [r"type-safe", r"\bPydantic\b", r"TypeScript-first", r"decorators? for tools"]),
    ("local",          [r"self-hosted", r"\bOllama\b", r"on-prem", r"run (?:locally|on your laptop)"]),
    ("provider-agnostic", [r"provider[- ]agnostic", r"multi-provider", r"100\+ (?:LLMs|models)", r"any LLM", r"swap OpenAI vs Anthropic"]),
    ("cli",            [r"\bCLI\b", r"\bterminal\b"]),
    ("ide",            [r"\bIDE\b", r"VS Code", r"\bCursor\b", r"JetBrains"]),
    ("tui",            [r"\bTUI\b", r"Bubble Tea"]),
    ("rust",           [r"\bRust\b"]),
    ("python",         [r"\bPython\b"]),
    ("typescript",     [r"TypeScript", r"\bNode(?:[/.]js|/TS)?\b", r"\bTS\b"]),
]

# Languages we also infer from the `labels` field on each Project.
LABEL_TO_TAG = {"python": "python", "javascript": "typescript"}

# Cap visible chips per row so descriptions stay scannable.
MAX_TAG_CHIPS = 5


def auto_tag(p: "Project") -> list:
    """Derive sorted canonical tags for a project from its description, axis,
    manual extras, and language labels.  TAG_RULES order is preserved so the
    most discriminative tags render first; language tags trail.
    """
    text = f"{p.description}  {p.axis}"
    matched: list = []
    seen: set = set()
    for tag, patterns in TAG_RULES:
        if any(re.search(pat, text) for pat in patterns):
            if tag not in seen:
                matched.append(tag)
                seen.add(tag)
    for lbl in p.labels:
        t = LABEL_TO_TAG.get(lbl)
        if t and t not in seen:
            matched.append(t)
            seen.add(t)
    for t in p.extra_tags:
        if t not in seen:
            matched.append(t)
            seen.add(t)
    return matched


def tag_chips_md(tags: list) -> str:
    """Render a project's tag list as small inline chips, capped at MAX_TAG_CHIPS."""
    if not tags:
        return ""
    shown = tags[:MAX_TAG_CHIPS]
    return " <sup>" + " · ".join(f"`{t}`" for t in shown) + "</sup>"


def slug(s: str) -> str:
    """Lowercase a heading and convert to a GitHub-style anchor slug."""
    s = s.lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


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
    ("personal-agent-runtimes", "Personal agent runtimes",
     "Always-on, self-hosted agents you run as a daemon and talk to from chat apps: gateway runtimes, second brains, and self-improving assistants. The agent as a product you operate, not a library you build with."),
    ("frameworks", "Frameworks",
     "General-purpose agent and LLM application frameworks (the app layer, not harnesses per se)."),
    ("multi-agent", "Multi-agent and orchestration",
     "Harnesses and patterns for multi-agent coordination and handoffs."),
    ("plugins-mcp-cli", "Plugins, MCPs, CLI tools",
     "IDE plugins, concrete MCP servers, and CLI tools that give agents tools and context."),
    ("memory", "Memory and state",
     "Persistent memory layers that give agents recall across turns and sessions: knowledge graphs, vector stores, and session-capture tools that survive a restart. The state a harness needs but rarely ships with."),
    ("evaluation", "Evaluation and benchmarking harnesses",
     "Agentic eval systems, reasoning benchmarks, and open agent benchmarks."),
    ("observability", "Observability and eval-ops",
     "Tracing, monitoring, and production evaluation for live agent runs: capture every step, tool call, and token, then score and debug in the loop. Distinct from the fixed-task benchmarks above—this is what you run against your own traffic."),
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
        Project("oh-my-pi", "can1357/oh-my-pi",
                "Terminal coding agent (fork of Pi) that wires the IDE into the **harness**: hash-anchored edits, a 32-tool loop tuned per-model, LSP rename/references/diagnostics on every write, a real DAP debugger (lldb/dlv/debugpy), long-lived Python + Bun execution kernels that call back into the agent's tools, browser control, and 40+ providers (Claude/OpenAI/Gemini/local). ~55k-line Rust core.",
                "slightly complex (terminal agent, LSP/DAP, multi-provider)", labels=["rust"]),
        Project("pi", "earendil-works/pi",
                "The upstream AI agent toolkit behind this list's oh-my-pi fork: a unified multi-provider LLM API, agent loop, and TUI shell providing the **harness** that oh-my-pi's Rust rewrite builds on.",
                "slightly complex (multi-provider agent loop, TUI)", oss="❓"),
        Project("AgentBox", "madarco/agentbox",
                "Runs multiple coding agents in parallel, each in its own sandboxed VM, locally or in the cloud, from one command. The **harness** contribution is the VM-per-agent isolation and fleet fan-out layer; whichever agent runs inside owns the loop.",
                "slightly complex (VM-per-agent sandbox, parallel fan-out)", labels=["javascript"]),
        Project("Proliferate", "proliferate-ai/proliferate",
                "Open-source AI IDE for Claude Code, Codex, OpenCode, and more. The **harness** contribution is the workspace/session orchestration layer: run multiple coding agents in parallel, locally or in the cloud, with isolated workspaces, reusable workflows, and shared team context.",
                "complex (multi-agent workspace orchestration — product suite)", labels=["javascript"]),
        Project("Cline", "cline/cline",
                "VS Code extension whose **harness** is a plan-then-act loop with per-step human approval and cost transparency; the VS Code integration is the UI shell. Open-source counterweight to Cursor.",
                "slightly complex (plan-then-act, approval gates)", labels=["javascript"]),
        Project("Roo-Code", "RooCodeInc/Roo-Code",
                "VS Code/Cursor extension in the Cline lineage. The **harness** is the approval-gated agent with custom modes and a strong MCP story; the IDE is the UI. Popular community fork when you want that workflow without the upstream extension.",
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
        Project("coderClaw", "SeanHogg/BuilderForceAgents",
                "Self-hosted multi-role coding system (Creator, Reviewer, Test, Refactor, etc.) with AST and semantic maps; IDE-agnostic, chat-channel triggers.",
                "slightly complex (multi-role, AST/semantic)", oss="❓", labels=["javascript"]),
        Project("Open Interpreter", "openinterpreter/openinterpreter",
                "Lightweight terminal coding agent oriented to open models (DeepSeek, Kimi, Qwen). The **harness** is a code-execution loop — the model writes code, the harness executes it with confirmation gates; the CLI is the shell. The original \"let the LLM run code on my machine\" project, reborn for open weights.",
                "mostly simple (lean code-exec loop)", labels=["python"]),
    ],
    "coding-harness-configs": [
        Project("LoopTroop", "looptroop-ai/LoopTroop",
                "Config layer that chains LLM councils for planning, Ralph loops for iterative refinement, and OpenCode worktrees for shipping. The **harness** contribution is the council → loop → worktree pipeline; OpenCode underneath executes.",
                "mostly simple (config pipeline over OpenCode)", labels=["javascript"]),
        Project("get-shit-done", "gsd-build/get-shit-done",
                "Goal-backward planning and wave-based execution over fresh context windows; avoids context rot by design. Python/JS meta-prompting for Claude Code, OpenCode, Gemini CLI.",
                "mostly simple (meta-prompting, you own stack)"),
        Project("GStack", "garrytan/gstack",
                "Garry Tan's Claude Code skill stack: 23 slash-command modes (CEO/eng/design review, QA, ship, browse, retro, …) that structure one assistant as a virtual engineering team. Daily driver while running YC.",
                "slightly complex (multi-role slash-command harness)", labels=["javascript"]),
        Project("everything-claude-code", "affaan-m/ECC",
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
        Project("Anthropic Skills", "anthropics/skills",
                "Anthropic's official Agent Skills repository: SKILL.md-based folders (instructions, scripts, resources) Claude dynamically loads on Claude Code, Claude.ai, and the API. The reference for progressive-disclosure skill packs in 2026.",
                "mostly simple (official skills format)", link_name="Anthropic Skills"),
        Project("Claude Code Subagents", "wshobson/agents",
                "Cross-harness marketplace of drop-in subagents and skills for Claude Code, Codex CLI, Cursor, OpenCode, and Copilot; specialized, production-ready agent definitions you install rather than hand-write.",
                "super simple (drop-in agent packs)", link_name="wshobson/agents"),
        Project("agents-cli", "google/agents-cli",
                "Google's official CLI and skill pack that layers agent-creation, evaluation, and deployment skills on top of whatever coding assistant you already run, rather than shipping its own agent loop—the **harness** as a config/skills add-on, not a new runtime.",
                "mostly simple (skills/CLI layer, no new runtime)", oss="❓"),
        Project("skillhub", "iflytek/skillhub",
                "iFlytek's self-hosted registry for publishing, versioning, and governing agent skill packages—the **harness** config layer treated as an enterprise artifact store rather than a CLI or IDE shell.",
                "mostly simple (skill registry/governance)", oss="❓"),
    ],
    "personal-agent-runtimes": [
        Project("Talon", "dylanneve1/talon",
                "Multi-platform personal agent living in Telegram, Discord, Teams, and the terminal. The **harness** is a pluggable-backend loop (Claude, Kilo, OpenCode, Codex, OpenAI Agents) with full MCP tool access and persistent background agents (Goals, Heartbeat, Dream); the chat apps are shells.",
                "slightly complex (multi-platform, pluggable backends, MCP)", labels=["javascript"]),
        Project("OpenClaw", "openclaw/openclaw",
                "Self-hosted, always-on personal agent (formerly Clawdbot/Moltbot): a gateway + event-loop runtime that treats messages, heartbeats, crons, and webhooks as one input queue, persists state to local files, and lives in your chat apps (WhatsApp, Telegram, Slack, Discord). 13,700+ community skills; the fastest-growing repo in GitHub history.",
                "complex (always-on runtime, channels, skill ecosystem — product suite)",
                labels=["javascript"], extra_tags=["multi-agent"]),
        Project("Hermes", "NousResearch/hermes-agent",
                "Nous Research's self-improving agent: a learning loop turns experience into reusable skills, builds a persistent user model across sessions, and checkpoints state to disk with rollback; lean enough for a $5 VPS, driven from chat, and model-agnostic (Nous Portal, OpenRouter, OpenAI, or any endpoint).",
                "slightly complex (lean runtime, learning loop, disk-first memory)",
                labels=["python"], extra_tags=["provider-agnostic"]),
        Project("Khoj", "khoj-ai/khoj",
                "Self-hostable \"AI second brain\": answers over your docs and the web, custom agents, scheduled automations, and multi-client reach (web, Obsidian, Emacs, WhatsApp). A personal-agent harness with retrieval at the core.",
                "complex (server + clients — product suite)", labels=["python"]),
        Project("Eliza", "elizaOS/eliza",
                "Open \"agentic operating system\" (elizaOS): persistent multi-agent runtime with character files, a plugin ecosystem, and social/platform integrations — the harness behind a large share of autonomous social agents.",
                "complex (runtime + plugin ecosystem — product suite)", labels=["javascript"]),
        Project("Agent Zero", "agent0ai/agent-zero",
                "Organic, prompt-defined personal agent framework: hierarchical sub-agents, persistent memory, browser and code tools, and self-modifying behavior; runs in Docker with a web UI.",
                "slightly complex (prompt-defined, Docker + web UI)", oss="❓", labels=["python"]),
        Project("OpenHarness (HKUDS)", "HKUDS/OpenHarness",
                "Open agent harness with a built-in personal agent (\"Ohmo\") that runs across Feishu, Slack, Telegram, and Discord; core tool-use, skills, memory, multi-agent coordination with auto-compaction for multi-day sessions.",
                "complex (personal agent + multi-channel — product suite)"),
        Project("AIlice", "myshell-ai/AIlice",
                "Fully autonomous general-purpose agent; one binary, Docker-ready, for when you want \"set goal and walk away\" without a framework.",
                "slightly complex (autonomous, one binary)", labels=["python"]),
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
        Project("youtu-agent", "TencentCloudADP/youtu-agent",
                "Tencent Cloud's agent framework: a minimal tool-calling **harness** designed to perform well with open-source models, positioned as a lighter alternative to heavier orchestration frameworks.",
                "mostly simple (minimal loop, open-model focus)", oss="❓"),
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
        Project("MetaGPT", "FoundationAgents/MetaGPT",
                "The \"AI software company\" multi-agent framework: role-played PM, architect, and engineer agents turn a one-line requirement into specs, designs, and code along an SOP assembly line. The landmark of the genre; development pace has slowed in 2026.",
                "complex (role pipeline, SOPs — product suite)", labels=["python"]),
        Project("OpenManus", "FoundationAgents/OpenManus",
                "Open, invite-free general agent from the MetaGPT team: planning plus tool use over a multi-agent loop, aimed at reproducing Manus-style autonomous task completion on your own keys.",
                "complex (multi-agent + tools)", labels=["python"]),
        Project("ChatDev", "OpenBMB/ChatDev",
                "Multi-agent software-company simulation (CEO, CTO, programmer, tester) built on chat chains with communicative dehallucination; ChatDev 2.0 continues the line. MetaGPT's conversational sibling.",
                "slightly complex (chat-chain simulation)", labels=["python"]),
        Project("Microsoft Agent Framework", "microsoft/agent-framework",
                "Microsoft's convergence of AutoGen and Semantic Kernel: build, orchestrate, and deploy agents and multi-agent workflows in Python and .NET, with graph-based workflows and checkpointing — the designated successor harness for both lines.",
                "slightly complex (Python/.NET SDK, graph workflows)", labels=["python"]),
    ],
    "plugins-mcp-cli": [
        Project("aider", "Aider-AI/aider",
                "Git-aware CLI pair programmer; edits in-repo, supports multiple models and MCP so agents see version control and tools.",
                "slightly complex (CLI, git-aware, MCP)", labels=["python"]),
        Project("agentlog", "RyanAlberts/agentlog",
                "Persistent decision memory for any project: `remember`, `recall`, `reflect`. Single-file Python CLI that stores decisions as JSONL and uses Claude or Gemini to retrieve and synthesize patterns—Karpathy's LLM Wiki concept as a CLI.",
                "super simple (one file, three commands)", labels=["python"]),
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
        Project("agent-vault", "Infisical/agent-vault",
                "Infisical's HTTP credential proxy that fronts secrets for Claude Code, OpenClaw, and other agent harnesses so the agent's tool calls never see raw credentials—a **harness** security layer, not an agent loop itself.",
                "mostly simple (credential proxy)", oss="❓"),
        Project("MCP Servers", "modelcontextprotocol/servers",
                "The official reference collection of Model Context Protocol servers (filesystem, git, fetch, memory, time, and more)—the canonical, vetted toolset agents connect to, and the pattern every other MCP server is measured against.",
                "mostly simple (reference servers)", labels=["javascript"]),
        Project("Context7", "upstash/context7",
                "MCP server that injects up-to-date, version-specific library docs into an agent's context on demand; kills the stale-training-data hallucinations that plague codegen.",
                "super simple (drop-in MCP)", labels=["javascript"]),
        Project("Playwright MCP", "microsoft/playwright-mcp",
                "Playwright's official MCP server: structured browser control (navigate, click, fill, extract) via the accessibility tree rather than screenshots, so web tasks stay fast and deterministic.",
                "mostly simple (browser MCP)", labels=["javascript"]),
    ],
    "memory": [
        Project("cognee", "topoteretes/cognee",
                "Open-source memory layer for agents: an extract–cognify–load pipeline that turns your data into a queryable knowledge graph plus vector store, so agents recall facts and relationships across sessions instead of re-reading context.",
                "slightly complex (graph + vector memory)", labels=["python"]),
        Project("Mem0", "mem0ai/mem0",
                "Universal memory layer for AI agents: stores user/org/session memory, retrieves on demand. Apache-2.0; the de-facto memory primitive paired with most harnesses in 2026.",
                "slightly complex (memory layer, multi-platform)", labels=["python"]),
        Project("claude-mem", "thedotmack/claude-mem",
                "Claude Code plugin that captures everything an agent does during a session, AI-compresses it (via claude-agent-sdk), and injects the relevant context into future sessions—session-to-session memory as a drop-in.",
                "slightly complex (session capture + compression)"),
    ],
    "evaluation": [
        Project("agent-qa", "vostride/agent-qa",
                "Self-improving QA **harness** for web and mobile apps: natural-language tests, memory-backed self-healing, dashboard/CLI, MCP and skills support, plus sandboxed hooks for production regression checks.",
                "slightly complex (web/mobile QA, memory, MCP)", oss="⚠️ FSL-1.1-ALv2", labels=["javascript"]),
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
    "observability": [
        Project("Langfuse", "langfuse/langfuse",
                "Open-source LLM engineering platform: full-trace observability, online and offline evals, prompt management, and cost metrics for agent runs in production—the monitoring layer most harnesses lack out of the box.",
                "slightly complex (tracing + evals platform)", labels=["javascript"]),
        Project("MLflow", "mlflow/mlflow",
                "Mature ML platform now covering GenAI: MLflow Tracing captures every agent step, tool call, and token, with built-in LLM evals and prompt versioning—observability for teams already standardized on MLflow.",
                "complex (full ML + GenAI platform)", labels=["python"]),
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
        Project("strands-agents", "strands-agents/harness-sdk",
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


# Stars + examples link, keyed by github_id (post-move where applicable).
# Star counts captured 2026-07-12 from the GitHub API; refresh by re-running
# scripts/refresh_stars.py (rewrites the counts below and bumps STARS_CAPTURED).
# Examples link: official docs, examples folder, leaderboard, or paper —
# whichever is the most useful "show me it in action" link for that project.
META: dict[str, tuple[int, str, str]] = {
    # progressive-disclosure
    "agentsmd/agents.md": (22962, "https://github.com/agentsmd/agents.md/blob/main/AGENTS.md", "Self-hosting AGENTS.md"),
    "PatrickJS/awesome-cursorrules": (40300, "https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/pytorch-scikit-learn-cursorrules-prompt-file.mdc", "PyTorch cursorrules"),
    "xfey/MCP-Zero": (490, "https://github.com/xfey/MCP-Zero/blob/master/MCP-zero/experiment_apibank.py", "APIBank experiment"),
    "langchain-ai/langgraph-bigtool": (545, "https://github.com/langchain-ai/langgraph-bigtool#quickstart", "Math-library tool agent"),
    "spring-ai-community/spring-ai-tool-search-tool": (77, "https://github.com/spring-ai-community/spring-ai-tool-search-tool/tree/main/examples/tool-search-tool-demo", "Tool Search demo app"),
    "Reason-Wang/ToolGen": (182, "https://github.com/Reason-Wang/ToolGen/blob/master/scripts/eval_full_pipeline.sh", "Full eval pipeline"),
    "antl3x/ToolRAG": (29, "https://github.com/antl3x/ToolRAG/blob/main/packages/%40antl3x-toolrag/README.md", "MCP server retrieval"),
    # coding-agent-products
    "can1357/oh-my-pi": (17388, "https://github.com/can1357/oh-my-pi/blob/main/docs/lsp-config.md", "LSP wired into edits"),
    "earendil-works/pi": (69847, "https://github.com/earendil-works/pi#readme", "Project README"),
    "madarco/agentbox": (247, "https://github.com/madarco/agentbox#readme", "Parallel agents quick start"),
    "proliferate-ai/proliferate": (151, "https://github.com/proliferate-ai/proliferate#readme", "Product README"),
    "cline/cline": (64568, "https://docs.cline.bot/features/plan-and-act", "Plan & Act mode"),
    "RooCodeInc/Roo-Code": (24321, "https://docs.roocode.com/features/custom-modes", "Custom modes guide"),
    "openai/codex": (97332, "https://developers.openai.com/codex/concepts/sandboxing", "Sandboxing concept"),
    "google-gemini/gemini-cli": (105932, "https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md", "MCP server setup"),
    "charmbracelet/crush": (26480, "https://charm.land/blog/crush-comes-home/", "Crush launch post"),
    "anomalyco/opencode": (184990, "https://opencode.ai/docs/agents/", "Agent system page"),
    "OpenHands/OpenHands": (80539, "https://docs.all-hands.dev/usage/prompting/microagents-repo", "Repository microagents"),
    "aaif-goose/goose": (51108, "https://block.github.io/goose/docs/guides/recipes/", "Goose recipes guide"),
    "HarnessLab/claw-code-agent": (528, "https://github.com/HarnessLab/claw-code-agent#-quick-start", "Quick Start guide"),
    "SeanHogg/BuilderForceAgents": (3, "https://github.com/SeanHogg/BuilderForceAgents#readme", "Multi-agent README"),
    # coding-harness-configs
    "looptroop-ai/LoopTroop": (60, "https://github.com/looptroop-ai/LoopTroop#readme", "Council → loop → worktree pipeline"),
    "gsd-build/get-shit-done": (64740, "https://github.com/gsd-build/get-shit-done/blob/main/commands/gsd/ship.md", "gsd:ship command"),
    "garrytan/gstack": (121403, "https://github.com/garrytan/gstack/blob/main/ship/SKILL.md", "/ship SKILL.md"),
    "affaan-m/ECC": (228818, "https://github.com/affaan-m/ECC/blob/main/skills/autonomous-agent-harness/SKILL.md", "autonomous-agent-harness skill"),
    "obra/superpowers": (252846, "https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md", "TDD skill"),
    "RyanAlberts/pmstack": (5, "https://github.com/RyanAlberts/pmstack/blob/main/skills/prd-from-signal.md", "PRD-from-signal skill"),
    "anthropics/claude-agent-sdk-python": (7595, "https://github.com/anthropics/claude-agent-sdk-demos/blob/main/research-agent/research_agent/agent.py", "Research agent demo"),
    "aiming-lab/AutoHarness": (347, "https://github.com/aiming-lab/AutoHarness/blob/main/examples/full_pipeline_demo.py", "Full pipeline demo"),
    "QuantaAlpha/RepoMaster": (533, "https://github.com/QuantaAlpha/RepoMaster/blob/main/example/pdf_parse.md", "PDF-parse case study"),
    "SWE-agent/SWE-agent": (19782, "https://github.com/SWE-agent/SWE-agent/blob/main/config/default.yaml", "Default agent config"),
    "HKUDS/OpenHarness": (14735, "https://github.com/HKUDS/OpenHarness/blob/main/.claude/skills/harness-eval/SKILL.md", "harness-eval skill"),
    "anthropics/skills": (160503, "https://github.com/anthropics/skills/blob/main/skills/docx/SKILL.md", "docx skill"),
    "google/agents-cli": (5060, "https://github.com/google/agents-cli#readme", "Project README"),
    "iflytek/skillhub": (3986, "https://github.com/iflytek/skillhub#readme", "Project README"),
    # frameworks
    "langchain-ai/langgraph": (37095, "https://github.com/langchain-ai/langgraph/blob/main/examples/customer-support/customer-support.ipynb", "Customer support agent"),
    "langchain-ai/langchain": (141595, "https://github.com/langchain-ai/langchain-academy/blob/main/module-1/agent.ipynb", "Build an agent notebook"),
    "run-llama/llama_index": (50796, "https://github.com/run-llama/llama_index/blob/main/docs/examples/agent/agent_workflow_research_assistant.ipynb", "Research assistant workflow"),
    "microsoft/semantic-kernel": (28300, "https://github.com/microsoft/semantic-kernel/blob/main/python/samples/getting_started_with_agents/chat_completion/step01_chat_completion_agent_simple.py", "Chat completion agent"),
    "mastra-ai/mastra": (26107, "https://github.com/mastra-ai/mastra/tree/main/examples/durable-agents", "Durable research agent"),
    "agno-agi/agno": (41110, "https://github.com/agno-agi/agno/blob/main/cookbook/02_agents/01_quickstart/agent_with_tools.py", "Agent with tools"),
    "letta-ai/letta": (23750, "https://github.com/letta-ai/agent-file/tree/main/agents/%40letta-ai/loop", "Loop .af agent file"),
    "langflow-ai/langflow": (151747, "https://github.com/langflow-ai/langflow/blob/main/docs/docs/Tutorials/chat-with-rag.mdx", "Chat with RAG flow"),
    "RasaHQ/rasa": (21238, "https://github.com/RasaHQ/rasa-demo", "Sara conversational demo"),
    "botpress/botpress": (14781, "https://github.com/botpress/v12/tree/master/examples/interbot", "Inter-bot delegation"),
    "langgenius/dify": (148580, "https://github.com/langgenius/dify-docs/blob/main/en/use-dify/tutorials/customer-service-bot.mdx", "Customer-service bot"),
    "n8n-io/n8n": (196154, "https://github.com/n8n-io/n8n-docs/blob/main/docs/advanced-ai/examples/agent-chain-comparison.md", "Agent vs chain workflow"),
    "Significant-Gravitas/AutoGPT": (185490, "https://github.com/Significant-Gravitas/AutoGPT/blob/master/autogpt_platform/graph_templates/Medium%20Blogger_v28.json", "Medium blogger graph"),
    "myshell-ai/AIlice": (1409, "https://github.com/myshell-ai/AIlice#cool-things-we-can-do", "Task showcase"),
    "i-am-bee/beeai-framework": (3315, "https://github.com/i-am-bee/beeai-framework/blob/main/python/examples/agents/react.py", "ReAct agent example"),
    "2FastLabs/agent-squad": (7697, "https://github.com/2FastLabs/agent-squad/tree/main/examples/ecommerce-support-simulator", "E-commerce support sim"),
    "superagentxai/superagentx": (200, "https://github.com/superagentxai/superagentx/blob/master/examples/agents/parallel_agents.py", "Parallel marketing agents"),
    "openclaw/openclaw": (382671, "https://github.com/openclaw/openclaw/blob/main/docs/agent-runtime-architecture.md", "Agent runtime architecture"),
    "NousResearch/hermes-agent": (213557, "https://github.com/NousResearch/hermes-agent/tree/main/skills", "Built-in skills"),
    "dylanneve1/talon": (64, "https://github.com/dylanneve1/talon#readme", "Multi-platform setup"),
    "openinterpreter/openinterpreter": (64351, "https://github.com/openinterpreter/openinterpreter#readme", "Quick start"),
    "FoundationAgents/MetaGPT": (69322, "https://github.com/FoundationAgents/MetaGPT/blob/main/examples/build_customized_agent.py", "Build a customized agent"),
    "OpenBMB/ChatDev": (33713, "https://github.com/OpenBMB/ChatDev#readme", "Company simulation quickstart"),
    "microsoft/agent-framework": (12058, "https://github.com/microsoft/agent-framework/tree/main/python/samples", "Python samples"),
    "khoj-ai/khoj": (35663, "https://github.com/khoj-ai/khoj#readme", "Feature tour"),
    "elizaOS/eliza": (18730, "https://github.com/elizaOS/eliza#readme", "Agent quickstart"),
    "agent0ai/agent-zero": (18403, "https://github.com/agent0ai/agent-zero#readme", "Framework tour"),
    "OpenBMB/AgentVerse": (5078, "https://github.com/OpenBMB/AgentVerse/blob/main/agentverse/tasks/simulation/nlp_classroom_9players/config.yaml", "NLP classroom sim"),
    "SciPhi-AI/R2R": (7925, "https://github.com/SciPhi-AI/R2R/blob/main/py/core/examples/hello_r2r.py", "hello_r2r RAG example"),
    "google/adk-python": (20572, "https://github.com/google/adk-samples/tree/main/python/agents/travel-concierge", "Travel concierge agent"),
    "agentstack-ai/AgentStack": (2168, "https://github.com/agentstack-ai/AgentStack/tree/main/examples/research_assistant", "Research assistant crew"),
    "howl-anderson/agentsilex": (451, "https://github.com/howl-anderson/agentsilex/blob/main/demo/simple_agent.py", "Simple weather agent"),
    "FlowiseAI/Flowise": (54543, "https://github.com/FlowiseAI/Flowise/blob/main/packages/server/marketplaces/agentflowsv2/Agentic%20RAG.json", "Agentic RAG flow"),
    "browser-use/browser-use": (104359, "https://github.com/browser-use/browser-use/blob/main/examples/use-cases/shopping.py", "Grocery shopping agent"),
    "TencentCloudADP/youtu-agent": (4580, "https://github.com/TencentCloudADP/youtu-agent#readme", "Project README"),
    # multi-agent
    "openai/openai-agents-python": (27839, "https://github.com/openai/openai-agents-python/blob/main/examples/customer_service/main.py", "Airline customer service handoffs"),
    "crewAIInc/crewAI": (55382, "https://github.com/crewAIInc/crewAI-examples/blob/main/crews/trip_planner/trip_agents.py", "Trip planner crew"),
    "microsoft/autogen": (59674, "https://github.com/microsoft/autogen/tree/main/python/samples/core_distributed-group-chat", "Distributed group chat"),
    "MervinPraison/PraisonAI": (8410, "https://github.com/MervinPraison/PraisonAI/blob/main/examples/python/general/orchestrator-workers.py", "Orchestrator-workers pattern"),
    "THUDM/AgentRL": (314, "https://github.com/THUDM/AgentRL/blob/main/examples/training/async_trainer.py", "Async GRPO trainer"),
    # plugins-mcp-cli
    "Aider-AI/aider": (47312, "https://github.com/Aider-AI/aider/blob/main/aider/repomap.py", "Repo map source"),
    "RyanAlberts/agentlog": (1, "https://github.com/RyanAlberts/agentlog/blob/main/example-log/decisions.jsonl", "Sample decisions.jsonl"),
    "thedotmack/claude-mem": (86925, "https://github.com/thedotmack/claude-mem/blob/main/plugin/hooks/hooks.json", "Lifecycle hooks config"),
    "ajhcs/Better-OpenCodeMCP": (8, "https://github.com/ajhcs/Better-OpenCodeMCP/blob/main/src/tools/opencode.tool.ts", "opencode delegate tool"),
    "modelcontextprotocol/python-sdk": (23593, "https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/servers/simple-tool/mcp_simple_tool/server.py", "Website fetcher server"),
    "modelcontextprotocol/typescript-sdk": (12832, "https://github.com/modelcontextprotocol/typescript-sdk/blob/main/examples/server/src/simpleStreamableHttp.ts", "Streamable HTTP server"),
    "continuedev/continue": (34831, "https://github.com/continuedev/continue/blob/main/extensions/vscode/README.md", "VS Code extension demos"),
    "modelcontextprotocol/inspector": (10348, "https://github.com/modelcontextprotocol/inspector/blob/main/README.md", "Inspector UI walkthrough"),
    "github/github-mcp-server": (31385, "https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md", "Remote server toolsets"),
    "modelcontextprotocol/registry": (7009, "https://github.com/modelcontextprotocol/registry/blob/main/data/seed.json", "Registry seed entries"),
    "docker/mcp-gateway": (1479, "https://github.com/docker/mcp-gateway/blob/main/docs/mcp-gateway.md", "Gateway usage walkthrough"),
    "withLinda/puppeteer-real-browser-mcp-server": (24, "https://github.com/withLinda/puppeteer-real-browser-mcp-server/blob/main/README.md", "11 anti-detection tools"),
    "Infisical/agent-vault": (1857, "https://github.com/Infisical/agent-vault#readme", "Project README"),
    # evaluation
    "vostride/agent-qa": (157, "https://github.com/vostride/agent-qa#readme", "Natural-language QA harness"),
    "arcprize/ARC-AGI-2": (725, "https://arcprize.org/leaderboard", "ARC Prize leaderboard"),
    "arcprize/arc-agi-benchmarking": (351, "https://github.com/arcprize/arc-agi-benchmarking/blob/main/docs/examples/prompt_example_o3.md", "o3 prompt example"),
    "GAIR-NLP/AgencyBench": (89, "https://github.com/GAIR-NLP/AgencyBench#leaderboard", "AgencyBench leaderboard"),
    "patronus-ai/trail-benchmark": (21, "https://huggingface.co/datasets/PatronusAI/TRAIL", "TRAIL dataset card"),
    "THUDM/AgentBench": (3562, "https://arxiv.org/abs/2308.03688", "AgentBench ICLR'24 paper"),
    "web-arena-x/webarena": (1540, "https://docs.google.com/spreadsheets/d/1M801lEpBbKSNwP-vDBkC_pF7LdyGU1f_ufZb_NWNBZQ/edit", "WebArena leaderboard"),
    "SWE-bench/SWE-bench": (5399, "https://www.swebench.com/verified.html", "SWE-bench Verified leaderboard"),
    "SWE-Gym/SWE-Gym": (701, "https://arxiv.org/abs/2412.21139", "SWE-Gym ICML 2025 paper"),
    "SWE-bench/SWE-smith": (697, "https://huggingface.co/datasets/SWE-bench/SWE-smith-trajectories", "SWE-smith trajectories"),
    "allenai/super-benchmark": (53, "https://arxiv.org/abs/2409.07440", "SUPER EMNLP paper"),
    "meituan-longcat/vitabench": (156, "https://arxiv.org/abs/2509.26490", "VitaBench paper"),
    "letta-ai/letta-evals": (77, "https://github.com/letta-ai/letta-leaderboard/blob/main/leaderboard/locomo/locomo_benchmark.py", "LoCoMo memory benchmark"),
    "MinorJerry/WebVoyager": (1104, "https://github.com/MinorJerry/WebVoyager/blob/main/data/WebVoyager_data.jsonl", "643 web tasks dataset"),
    "UKGovernmentBEIS/inspect_evals": (578, "https://github.com/UKGovernmentBEIS/inspect_evals/blob/main/src/inspect_evals/swe_bench/README.md", "inspect SWE-bench eval"),
    "UKGovernmentBEIS/inspect_ai": (2332, "https://inspect.aisi.org.uk/tutorial.html", "Inspect tutorial example"),
    "microsoft/agent-lightning": (17381, "https://github.com/microsoft/agent-lightning/blob/main/examples/apo/README.md", "APO room-booking example"),
    # research-task
    "assafelovic/gpt-researcher": (28268, "https://github.com/assafelovic/gpt-researcher/blob/master/docs/blog/2024-05-19-gptr-langgraph/index.md", "Multi-agent LangGraph walkthrough"),
    "OpenAgentsInc/openagents": (439, "https://github.com/OpenAgentsInc/openagents/blob/main/docs/reports/nexus/2026-04-23-autopilot-pylon-production-earning-proof.md", "Production earning proof"),
    # libraries-sdks
    "langchain-ai/deepagents": (26129, "https://github.com/langchain-ai/deepagents/tree/main/examples/deep_research", "Deep research agent"),
    "pydantic/pydantic-ai": (18442, "https://github.com/pydantic/pydantic-ai/blob/main/examples/pydantic_ai_examples/bank_support.py", "Bank support agent"),
    "MaxGfeller/open-harness": (585, "https://github.com/MaxGfeller/open-harness/tree/main/examples/cli", "Terminal CLI agent"),
    "vercel/ai": (25504, "https://github.com/vercel/ai/tree/main/examples/next-agent", "Next.js agent example"),
    "huggingface/smolagents": (28310, "https://github.com/huggingface/smolagents/blob/main/examples/rag.py", "RAG code agent"),
    "strands-agents/harness-sdk": (6533, "https://github.com/strands-agents/samples/tree/main/python/01-learn/01-first-agent", "First agent tutorial"),
    "openai/openai-agents-js": (3371, "https://github.com/openai/openai-agents-js/tree/main/examples/financial-research-agent", "Financial research agent"),
    "BerriAI/litellm": (53331, "https://github.com/BerriAI/litellm/blob/main/cookbook/anthropic_agent_sdk/main.py", "Anthropic Agent SDK gateway"),
    "ComposioHQ/composio": (29201, "https://github.com/ComposioHQ/composio#quick-start", "HackerNews agent quickstart"),
    "mem0ai/mem0": (60656, "https://github.com/mem0ai/mem0/tree/main/examples/mem0-demo", "Next.js memory demo"),
    "cloudflare/agents": (5246, "https://github.com/cloudflare/agents/tree/main/examples/playground", "SDK playground app"),
    "e2b-dev/E2B": (12937, "https://github.com/e2b-dev/e2b-cookbook/tree/main/examples/anthropic-claude-code-in-sandbox-python", "Claude Code in sandbox"),
    "daytonaio/daytona": (72204, "https://github.com/daytonaio/daytona/tree/main/examples/python/charts", "Charts in sandbox"),
    "brandonhimpfen/awesome-ai-agents": (12, "https://github.com/brandonhimpfen/awesome-ai-agents#frameworks", "Frameworks section"),
    # memory
    "topoteretes/cognee": (27612, "https://github.com/topoteretes/cognee#readme", "Quickstart"),
    # observability
    "langfuse/langfuse": (30962, "https://langfuse.com/docs", "Docs"),
    "mlflow/mlflow": (26988, "https://mlflow.org", "Docs"),
    # plugins-mcp-cli (MCP infrastructure)
    "modelcontextprotocol/servers": (88369, "https://github.com/modelcontextprotocol/servers#readme", "Server catalog"),
    "upstash/context7": (58961, "https://context7.com", "Docs"),
    "microsoft/playwright-mcp": (34980, "https://github.com/microsoft/playwright-mcp#readme", "Setup & config"),
    # multi-agent
    "FoundationAgents/OpenManus": (57224, "https://github.com/FoundationAgents/OpenManus#readme", "Quickstart"),
    # coding-harness-configs
    "wshobson/agents": (37830, "https://github.com/wshobson/agents#readme", "Agent catalog"),
}


# Date the star counts in META were last captured. Single source for the
# README explanation line, harnesses.json, llms.txt, and the landscape SVG.
STARS_CAPTURED = "2026-07-12"

# Repos currently archived upstream, keyed by github_id, mapped to the date
# first observed archived (YYYY-MM-DD). Maintained by scripts/refresh_stars.py.
ARCHIVED: "dict[str, str]" = {
    "spring-ai-community/spring-ai-tool-search-tool": "2026-07-03",
    "RooCodeInc/Roo-Code": "2026-07-03",
    "SeanHogg/BuilderForceAgents": "2026-07-03",
    "gsd-build/get-shit-done": "2026-07-03",
}

# github_ids that are archived upstream (present in ARCHIVED) but should stay
# out of the Graveyard and remain in normal ordering. Empty by default.
KEEP_DESPITE_ARCHIVED: "set[str]" = set()

# Repos routed to the Graveyard for a curation-integrity reason rather than
# upstream archival — e.g. star manipulation. Keyed by github_id, mapped to
# (date flagged YYYY-MM-DD, short public reason). Kept in the list, not deleted,
# so the record stays honest and the exclusion is auditable. Excluded from the
# ranked count, the landscape chart, and harnesses.json's main list.
INTEGRITY_FLAGGED: "dict[str, tuple[str, str]]" = {
    "affaan-m/ECC": (
        "2026-07-11",
        "suspected star manipulation — ~228k stars / ~35k forks on a repo "
        "created 2026-01 with no matching install base, dependents, or discussion; "
        "fork-to-star ratio and growth curve are inconsistent with organic adoption",
    ),
}

# Community members whose submissions shaped the list — rendered as the
# thank-you block at the top of the README. Add a tuple when a submission
# lands (as a listing or a radar pin); this is deliberately hand-curated
# because co-authored commits don't show up in GitHub's contributors API.
CONTRIBUTORS: "list[tuple[str, str]]" = [
    ("oldschoola", "oh-my-pi"),
    ("madarco", "AgentBox"),
    ("pranshuchittora", "agent-qa"),
    ("claudiusthebot", "Talon"),
    ("liviux", "LoopTroop"),
    ("rishabhpoddar", "TeamCopilot, on the radar"),
    ("ShukantPal", "Proliferate"),
]

# ---------------------------------------------------------------------------
# On the radar — up-and-coming candidates surfaced publicly before they clear
# the curation bar: repos the weekly discovery scan keeps finding, plus
# community submissions that are promising but not listable yet. Pins are
# editorial; stars and descriptions hydrate from curation-queue.json (rewritten
# by the weekly Action), so rows refresh without touching this file. An entry
# graduates by becoming a Project above (it then drops off the radar
# automatically) or gets unpinned.
RADAR: "list[dict]" = [
    {"id": "bytedance/deer-flow", "via": "weekly discovery"},
    {"id": "ChromeDevTools/chrome-devtools-mcp", "via": "weekly discovery"},
    {"id": "BloopAI/vibe-kanban", "via": "weekly discovery"},
    {"id": "Kilo-Org/kilocode", "via": "weekly discovery"},
    {"id": "QwenLM/qwen-code", "via": "weekly discovery"},
    {"id": "openai/symphony", "via": "weekly discovery"},
    {"id": "gastownhall/beads", "via": "weekly discovery"},
    {"id": "plandex-ai/plandex", "via": "weekly discovery"},
    {"id": "ag2ai/ag2", "via": "weekly discovery"},
    {"id": "IBM/mcp-context-forge", "via": "weekly discovery"},
    {"id": "evalstate/fast-agent", "via": "weekly discovery"},
    {"id": "cocoindex-io/cocoindex-code", "via": "weekly discovery"},
    {"id": "google-antigravity/antigravity-cli", "via": "weekly discovery"},
    {"id": "rishabhpoddar/teamcopilot", "via": "community · PR #21", "stars": 14,
     "desc": "Deploy AI agents for your team to automate business workflows and coding."},
]


def queue_candidates() -> "dict[str, dict]":
    """curation-queue.json's candidates keyed by github_id ({} if unreadable)."""
    import json
    try:
        q = json.loads((REPO_ROOT / "curation-queue.json").read_text())
    except (OSError, ValueError):
        return {}
    return {c["id"]: c for c in q.get("candidates", []) if c.get("id")}


def radar_entries() -> list:
    """RADAR pins hydrated from the queue, minus anything already listed,
    sorted by stars. Descriptions are the repos' own — unvetted."""
    listed = {p.github_id.lower() for plist in PROJECTS.values() for p in plist}
    qc = queue_candidates()
    out = []
    for pin in RADAR:
        gid = pin["id"]
        if gid.lower() in listed:
            continue
        c = qc.get(gid, {})
        desc = (pin.get("desc") or c.get("desc") or "").replace("|", "\\|").replace("\n", " ").strip()
        if len(desc) > 160:
            desc = desc[:157].rstrip() + "…"
        out.append({
            "github_id": gid,
            "stars": c.get("stars", pin.get("stars", 0)),
            "desc": desc,
            "via": pin.get("via", "weekly discovery"),
        })
    return sorted(out, key=lambda e: -e["stars"])

# Canonical 4-tier order of the simplicity ↔ capability axis (least → most
# adoption surface). Every Project.axis must start with one of these.
TIER_ORDER = ["super simple", "mostly simple", "slightly complex", "complex"]


def tier_of(p: "Project") -> str:
    for t in sorted(TIER_ORDER, key=len, reverse=True):
        if p.axis.startswith(t):
            return t
    raise ValueError(f"{p.github_id}: axis {p.axis!r} doesn't start with a canonical tier")


# ---------------------------------------------------------------------------
# Harness-behavior axes (editorial, assigned from public docs — corrections
# from maintainers welcome via issue/PR).
#
# autonomy — the regime the project is DESIGNED to run agents at:
#   step-gated (human approves each action) -> checkpoint-gated (human steers
#   at plan/turn boundaries) -> bounded (full-task autonomy inside sandbox/
#   guardrail walls) -> headless (built for unattended runs, batches, fleets).
#   "n/a" = doesn't own an agent loop (formats, skill packs, components,
#   datasets, infra).
# recovery — what happens when a run dies mid-task:
#   none (start over) -> retry (per-call retries/fallbacks) -> resumable
#   (session/checkpoint resume after interruption) -> durable (persisted
#   execution state survives restarts). "n/a" = doesn't execute.
# ---------------------------------------------------------------------------
AUTONOMY_TIERS = ["step-gated", "checkpoint-gated", "bounded", "headless"]
RECOVERY_TIERS = ["none", "retry", "resumable", "durable"]

AXES: "dict[str, tuple[str, str]]" = {
    # progressive-disclosure
    "PatrickJS/awesome-cursorrules": ("n/a", "n/a"),
    "agentsmd/agents.md": ("n/a", "n/a"),
    "langchain-ai/langgraph-bigtool": ("bounded", "durable"),
    "xfey/MCP-Zero": ("bounded", "none"),
    "Reason-Wang/ToolGen": ("n/a", "n/a"),
    "spring-ai-community/spring-ai-tool-search-tool": ("n/a", "n/a"),
    "antl3x/ToolRAG": ("n/a", "n/a"),
    # coding-agent-products
    "can1357/oh-my-pi": ("bounded", "resumable"),
    "earendil-works/pi": ("bounded", "resumable"),
    "madarco/agentbox": ("n/a", "n/a"),
    "proliferate-ai/proliferate": ("bounded", "resumable"),
    "anomalyco/opencode": ("headless", "resumable"),
    "google-gemini/gemini-cli": ("bounded", "resumable"),
    "openai/codex": ("bounded", "resumable"),
    "OpenHands/OpenHands": ("headless", "resumable"),
    "cline/cline": ("step-gated", "resumable"),
    "aaif-goose/goose": ("headless", "resumable"),
    "charmbracelet/crush": ("bounded", "resumable"),
    "RooCodeInc/Roo-Code": ("step-gated", "resumable"),
    "HarnessLab/claw-code-agent": ("checkpoint-gated", "none"),
    "SeanHogg/BuilderForceAgents": ("bounded", "none"),
    # coding-harness-configs
    "looptroop-ai/LoopTroop": ("bounded", "retry"),
    "obra/superpowers": ("n/a", "n/a"),
    "affaan-m/ECC": ("n/a", "n/a"),
    "anthropics/skills": ("n/a", "n/a"),
    "google/agents-cli": ("n/a", "n/a"),
    "iflytek/skillhub": ("n/a", "n/a"),
    "garrytan/gstack": ("n/a", "n/a"),
    "gsd-build/get-shit-done": ("bounded", "resumable"),
    "SWE-agent/SWE-agent": ("headless", "resumable"),
    "HKUDS/OpenHarness": ("bounded", "resumable"),
    "anthropics/claude-agent-sdk-python": ("headless", "resumable"),
    "QuantaAlpha/RepoMaster": ("headless", "none"),
    "aiming-lab/AutoHarness": ("bounded", "none"),
    "RyanAlberts/pmstack": ("n/a", "n/a"),
    # frameworks
    "n8n-io/n8n": ("headless", "durable"),
    "Significant-Gravitas/AutoGPT": ("headless", "resumable"),
    "langflow-ai/langflow": ("headless", "retry"),
    "langgenius/dify": ("headless", "retry"),
    "langchain-ai/langchain": ("bounded", "retry"),
    "browser-use/browser-use": ("bounded", "retry"),
    "TencentCloudADP/youtu-agent": ("bounded", "retry"),
    "FlowiseAI/Flowise": ("headless", "retry"),
    "run-llama/llama_index": ("bounded", "retry"),
    "agno-agi/agno": ("bounded", "resumable"),
    "langchain-ai/langgraph": ("headless", "durable"),
    "microsoft/semantic-kernel": ("bounded", "retry"),
    "mastra-ai/mastra": ("bounded", "durable"),
    "letta-ai/letta": ("headless", "durable"),
    "RasaHQ/rasa": ("headless", "resumable"),
    "google/adk-python": ("headless", "resumable"),
    "botpress/botpress": ("headless", "resumable"),
    "SciPhi-AI/R2R": ("headless", "retry"),
    "2FastLabs/agent-squad": ("bounded", "resumable"),
    "OpenBMB/AgentVerse": ("headless", "none"),
    "i-am-bee/beeai-framework": ("bounded", "resumable"),
    "agentstack-ai/AgentStack": ("n/a", "n/a"),
    "myshell-ai/AIlice": ("bounded", "none"),
    "howl-anderson/agentsilex": ("bounded", "none"),
    "openclaw/openclaw": ("headless", "resumable"),
    "NousResearch/hermes-agent": ("headless", "resumable"),
    "dylanneve1/talon": ("headless", "resumable"),
    "openinterpreter/openinterpreter": ("bounded", "resumable"),
    "FoundationAgents/MetaGPT": ("headless", "resumable"),
    "OpenBMB/ChatDev": ("headless", "none"),
    "microsoft/agent-framework": ("bounded", "resumable"),
    "khoj-ai/khoj": ("headless", "resumable"),
    "elizaOS/eliza": ("headless", "resumable"),
    "agent0ai/agent-zero": ("bounded", "resumable"),
    "superagentxai/superagentx": ("bounded", "none"),
    # multi-agent
    "microsoft/autogen": ("bounded", "resumable"),
    "crewAIInc/crewAI": ("bounded", "resumable"),
    "openai/openai-agents-python": ("bounded", "resumable"),
    "MervinPraison/PraisonAI": ("bounded", "none"),
    "THUDM/AgentRL": ("headless", "resumable"),
    # plugins-mcp-cli
    "thedotmack/claude-mem": ("n/a", "n/a"),
    "Aider-AI/aider": ("checkpoint-gated", "resumable"),
    "continuedev/continue": ("checkpoint-gated", "resumable"),
    "github/github-mcp-server": ("n/a", "n/a"),
    "modelcontextprotocol/python-sdk": ("n/a", "n/a"),
    "modelcontextprotocol/typescript-sdk": ("n/a", "n/a"),
    "modelcontextprotocol/inspector": ("n/a", "n/a"),
    "modelcontextprotocol/registry": ("n/a", "n/a"),
    "docker/mcp-gateway": ("n/a", "n/a"),
    "withLinda/puppeteer-real-browser-mcp-server": ("n/a", "n/a"),
    "Infisical/agent-vault": ("n/a", "n/a"),
    "ajhcs/Better-OpenCodeMCP": ("n/a", "n/a"),
    "RyanAlberts/agentlog": ("n/a", "n/a"),
    # evaluation
    "vostride/agent-qa": ("headless", "retry"),
    "microsoft/agent-lightning": ("headless", "resumable"),
    "SWE-bench/SWE-bench": ("headless", "resumable"),
    "THUDM/AgentBench": ("headless", "none"),
    "UKGovernmentBEIS/inspect_ai": ("headless", "resumable"),
    "web-arena-x/webarena": ("headless", "none"),
    "MinorJerry/WebVoyager": ("headless", "none"),
    "arcprize/ARC-AGI-2": ("n/a", "n/a"),
    "SWE-Gym/SWE-Gym": ("headless", "none"),
    "SWE-bench/SWE-smith": ("headless", "none"),
    "UKGovernmentBEIS/inspect_evals": ("headless", "resumable"),
    "arcprize/arc-agi-benchmarking": ("headless", "retry"),
    "meituan-longcat/vitabench": ("headless", "none"),
    "GAIR-NLP/AgencyBench": ("headless", "none"),
    "letta-ai/letta-evals": ("headless", "none"),
    "allenai/super-benchmark": ("headless", "none"),
    "patronus-ai/trail-benchmark": ("n/a", "n/a"),
    # research-task
    "assafelovic/gpt-researcher": ("bounded", "retry"),
    "OpenAgentsInc/openagents": ("headless", "resumable"),
    # libraries-sdks
    "daytonaio/daytona": ("n/a", "n/a"),
    "mem0ai/mem0": ("n/a", "n/a"),
    "BerriAI/litellm": ("n/a", "retry"),
    "ComposioHQ/composio": ("n/a", "n/a"),
    "huggingface/smolagents": ("bounded", "none"),
    "vercel/ai": ("bounded", "retry"),
    "langchain-ai/deepagents": ("bounded", "durable"),
    "pydantic/pydantic-ai": ("bounded", "durable"),
    "e2b-dev/E2B": ("n/a", "n/a"),
    "strands-agents/harness-sdk": ("bounded", "resumable"),
    "cloudflare/agents": ("headless", "durable"),
    "openai/openai-agents-js": ("bounded", "resumable"),
    "MaxGfeller/open-harness": ("bounded", "none"),
    "brandonhimpfen/awesome-ai-agents": ("n/a", "n/a"),
    # memory (state layers — no agent loop of their own)
    "topoteretes/cognee": ("n/a", "n/a"),
    # observability (tracing/eval-ops infra — no agent loop of their own)
    "langfuse/langfuse": ("n/a", "n/a"),
    "mlflow/mlflow": ("n/a", "n/a"),
    # plugins-mcp-cli (MCP infrastructure — tools/servers, not loops)
    "modelcontextprotocol/servers": ("n/a", "n/a"),
    "upstash/context7": ("n/a", "n/a"),
    "microsoft/playwright-mcp": ("n/a", "n/a"),
    # multi-agent
    "FoundationAgents/OpenManus": ("bounded", "none"),
    # coding-harness-configs (skill/subagent packs — no loop)
    "wshobson/agents": ("n/a", "n/a"),
}


def axes_for(github_id: str) -> tuple:
    if github_id not in AXES:
        raise KeyError(f"AXES is missing an entry for {github_id} — score it before generating")
    a, r = AXES[github_id]
    if a != "n/a" and a not in AUTONOMY_TIERS:
        raise ValueError(f"{github_id}: bad autonomy tier {a!r}")
    if r != "n/a" and r not in RECOVERY_TIERS:
        raise ValueError(f"{github_id}: bad recovery tier {r!r}")
    return a, r


def autonomy_rank(a: str) -> int:
    return AUTONOMY_TIERS.index(a) + 1 if a in AUTONOMY_TIERS else 0


def recovery_rank(r: str) -> int:
    return RECOVERY_TIERS.index(r) + 1 if r in RECOVERY_TIERS else 0


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


# ---------------------------------------------------------------------------
# "Pick by use case" reader-intent index.
#
# Each entry is (intent, [github_ids], category_title_for_See_link).
# github_ids must reference projects that exist in PROJECTS — find_project()
# raises so a typo cannot ship. Keep each intent's pick list to 3–7 items:
# enough to compare, few enough to act on. Lead each list with the most
# canonical / highest-leverage pick.
# ---------------------------------------------------------------------------
USE_CASES: "list[tuple[str, list[str], str]]" = [
    ("I want a turnkey coding agent today",
     ["anomalyco/opencode", "cline/cline", "openai/codex",
      "google-gemini/gemini-cli", "OpenHands/OpenHands",
      "charmbracelet/crush", "RooCodeInc/Roo-Code"],
     "Coding agent products (IDEs, CLIs, full suites)"),
    ("I want an always-on personal agent that lives in my chat apps",
     ["openclaw/openclaw", "NousResearch/hermes-agent", "khoj-ai/khoj",
      "agent0ai/agent-zero", "HKUDS/OpenHarness"],
     "Personal agent runtimes"),
    ("I want to extend Claude Code, Codex, or OpenCode with skills and slash commands",
     ["anthropics/skills", "wshobson/agents",
      "obra/superpowers", "garrytan/gstack", "RyanAlberts/pmstack"],
     "Coding harness configs and SDKs"),
    ("I want to build my own coding harness from scratch",
     ["anthropics/claude-agent-sdk-python", "google/adk-python",
      "aiming-lab/AutoHarness", "SWE-agent/SWE-agent",
      "QuantaAlpha/RepoMaster", "HarnessLab/claw-code-agent"],
     "Coding harness configs and SDKs"),
    ("I want a drop-in memory layer for agents",
     ["mem0ai/mem0", "thedotmack/claude-mem", "RyanAlberts/agentlog",
      "agno-agi/agno", "letta-ai/letta"],
     "Plugins, MCPs, CLI tools"),
    ("I want to plug hundreds to thousands of tools without context bloat",
     ["xfey/MCP-Zero", "Reason-Wang/ToolGen", "antl3x/ToolRAG",
      "langchain-ai/langgraph-bigtool",
      "spring-ai-community/spring-ai-tool-search-tool"],
     "Progressive disclosure harnesses"),
    ("I want multi-agent orchestration",
     ["openai/openai-agents-python", "crewAIInc/crewAI",
      "microsoft/autogen", "microsoft/agent-framework",
      "MervinPraison/PraisonAI", "2FastLabs/agent-squad"],
     "Multi-agent and orchestration"),
    ("I want a general LLM app framework",
     ["langchain-ai/langgraph", "langchain-ai/langchain",
      "run-llama/llama_index", "pydantic/pydantic-ai",
      "agno-agi/agno"],
     "Frameworks"),
    ("I want low-code / visual workflows",
     ["langflow-ai/langflow", "FlowiseAI/Flowise",
      "langgenius/dify", "n8n-io/n8n"],
     "Frameworks"),
    ("I want browser-using agents",
     ["browser-use/browser-use", "MinorJerry/WebVoyager",
      "withLinda/puppeteer-real-browser-mcp-server"],
     "Plugins, MCPs, CLI tools"),
    ("I want sandboxed code execution for agent-generated code",
     ["e2b-dev/E2B", "daytonaio/daytona",
      "huggingface/smolagents", "OpenHands/OpenHands"],
     "Libraries and SDKs"),
    ("I want to evaluate or benchmark agents",
     ["SWE-bench/SWE-bench", "GAIR-NLP/AgencyBench",
      "UKGovernmentBEIS/inspect_ai", "web-arena-x/webarena",
      "arcprize/ARC-AGI-2", "meituan-longcat/vitabench"],
     "Evaluation and benchmarking harnesses"),
    ("I want a deep research / autonomous research agent",
     ["langchain-ai/deepagents", "assafelovic/gpt-researcher",
      "OpenAgentsInc/openagents"],
     "Research and task-specific harnesses"),
    ("I want a provider-agnostic LLM pipe (not a framework)",
     ["BerriAI/litellm", "vercel/ai"],
     "Libraries and SDKs"),
]


def find_project(github_id: str) -> "Project":
    for plist in PROJECTS.values():
        for p in plist:
            if p.github_id == github_id:
                return p
    raise KeyError(f"USE_CASES references unknown github_id: {github_id}")


def render_use_cases() -> list:
    lines = [
        "## Pick by use case",
        "",
        "_Reader's index: pick by what you want to do, not by category. Tag chips (e.g. <sup>`mcp` · `memory`</sup>) next to each row let you cross-filter by capability — see [TAGS.md](TAGS.md) for the full cross-reference._",
        "",
    ]
    for intent, ids, cat_title in USE_CASES:
        picks: list = []
        for gid in ids:
            if is_graveyard(gid):
                continue
            p = find_project(gid)
            picks.append(f"[{p.display_name}](https://github.com/{p.github_id})")
        anchor = slug(cat_title)
        lines.append(
            f"- **{intent}** — {', '.join(picks)} · see [{cat_title}](#{anchor})"
        )
    lines.append("")
    return lines


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
        for p in live_projects(cat_id):
            lines.append(f"  - name: {p.name}")
            lines.append(f"    github_id: {p.github_id}")
            if p.labels:
                lbls = ", ".join(f'"{l}"' for l in p.labels)
                lines.append(f"    labels: [{lbls}]")
            lines.append(f"    category: \"{cat_id}\"")
    lines.append("")
    return "\n".join(lines)


def count_projects() -> int:
    """Live project count — excludes graveyard (see is_graveyard)."""
    return sum(
        1 for c, _, _ in CATEGORIES for p in PROJECTS[c] if not is_graveyard(p.github_id)
    )


def graveyard_count() -> int:
    return len(graveyard_projects())


# ---------------------------------------------------------------------------
# Discoverability surfaces (GEO/SEO): stable per-project slugs and deep links,
# a data-derived FAQ, schema.org JSON-LD, and a JSON Feed of refreshes. The
# GitHub Pages site (scripts/build_site.py) renders HTML from the same data.
# ---------------------------------------------------------------------------

SITE_ORIGIN = "https://ryanalberts.github.io"
BASE_PATH = "/best-of-Agent-Harnesses"  # GitHub Pages project-site path
SITE_URL = f"{SITE_ORIGIN}{BASE_PATH}/"
REPO_HTTP = "https://github.com/RyanAlberts/best-of-Agent-Harnesses"
RAW_BASE = "https://raw.githubusercontent.com/RyanAlberts/best-of-Agent-Harnesses/main"


def is_graveyard(github_id: str) -> bool:
    """True if a repo is archived (and not kept out) or flagged for integrity."""
    archived = github_id in ARCHIVED and github_id not in KEEP_DESPITE_ARCHIVED
    return archived or github_id in INTEGRITY_FLAGGED


def graveyard_since(github_id: str) -> str:
    """Date a repo entered the Graveyard: archival date or integrity-flag date."""
    if github_id in ARCHIVED:
        return ARCHIVED[github_id]
    return INTEGRITY_FLAGGED[github_id][0]


def graveyard_reason(github_id: str) -> str:
    """Why a repo is in the Graveyard — archival or the integrity-flag reason."""
    if github_id in ARCHIVED and github_id not in INTEGRITY_FLAGGED:
        return "archived upstream — kept for citation"
    return INTEGRITY_FLAGGED[github_id][1]


def graveyard_projects() -> list:
    """All Projects across every category that route to the Graveyard, stars descending."""
    out: list = []
    for projects in PROJECTS.values():
        out += [p for p in projects if is_graveyard(p.github_id)]
    return sorted(out, key=lambda p: stars_for(p.github_id), reverse=True)


def ordered_projects() -> list:
    """All projects in canonical display order: category order, stars descending.

    Excludes projects routed to the Graveyard (see is_graveyard)."""
    out: list = []
    for cat_id, _, _ in CATEGORIES:
        projects = [p for p in PROJECTS[cat_id] if not is_graveyard(p.github_id)]
        out += sorted(projects, key=lambda x: stars_for(x.github_id), reverse=True)
    return out


def live_projects(cat_id: str) -> "list[Project]":
    """Non-archived projects in a single category, in PROJECTS insertion order."""
    return [p for p in PROJECTS[cat_id] if not is_graveyard(p.github_id)]


_SLUG_MAP: "dict[str, str]" = {}


def project_slug(github_id: str) -> str:
    """Stable, unique anchor/URL slug for a project (its repo name, deduped)."""
    if not _SLUG_MAP:
        used: set = set()
        for p in ordered_projects():
            base = slug(p.github_id.split("/")[-1]) or slug(p.github_id.replace("/", "-"))
            s, n = base, 2
            while s in used:
                s = f"{base}-{n}"
                n += 1
            used.add(s)
            _SLUG_MAP[p.github_id] = s
    return _SLUG_MAP[github_id]


def project_anchor_url(github_id: str) -> str:
    """Deep link to the project's row in the README."""
    return f"{REPO_HTTP}#{project_slug(github_id)}"


def project_page_url(github_id: str) -> str:
    """Canonical URL of the project's page on the GitHub Pages site."""
    return f"{SITE_URL}h/{project_slug(github_id)}/"


def build_faq() -> list:
    """Question/answer pairs derived from the list data — the shape AI answer
    engines cite. Each item: {kind, q, a, slug}. `kind` is use-case | derived |
    concept so each surface can include the right subset."""
    faq: list = []

    def add(kind: str, q: str, a: str) -> None:
        faq.append({"kind": kind, "q": q, "a": a, "slug": slug(q)})

    for intent, ids, cat_title in USE_CASES:
        live_ids = [g for g in ids if not is_graveyard(g)]
        picks = ", ".join(find_project(g).display_name for g in live_ids[:3])
        add("use-case", f"What is the best agent harness if {intent}?",
            f"Top picks: {picks}. See the “{cat_title}” category for the full ranked list.")

    headless = [p for p in ordered_projects() if axes_for(p.github_id)[0] == "headless"]
    durable = [p for p in ordered_projects() if axes_for(p.github_id)[1] == "durable"]
    oss = [p for p in ordered_projects() if oss_signal(p.oss) == "open-source"]
    add("derived", "Which agent harnesses can run unattended (headless)?",
        "Harnesses designed for unattended runs, batches, and fleets: "
        + ", ".join(p.display_name for p in headless[:8]) + ".")
    add("derived", "Which agent harnesses survive a crash mid-task (durable)?",
        "Harnesses whose execution state persists across restarts: "
        + ", ".join(p.display_name for p in durable[:8]) + ".")
    add("derived", "How many of these agent harnesses are open source?",
        f"{len(oss)} of {count_projects()} carry a standard open-source license; the rest are "
        "source-available or unclear, and flagged per row.")

    add("concept", "What is an agent harness?",
        "The runtime that turns a model into an agent: it decides what the model's reasoning "
        "is allowed to touch, and supplies the orchestration, tool wiring, memory, error "
        "recovery, and guardrails around per-turn inference.")
    add("concept", "How is this list ranked?",
        "By relevance to harness concerns (environment, orchestration, lifecycle, guardrails) "
        f"and by GitHub stars (captured {STARS_CAPTURED}); each project also carries an "
        "adoption-surface tier and autonomy/recovery scores.")
    add("concept", "How can an AI agent use this list directly?",
        "Three machine-readable surfaces: harnesses.json (structured), llms.txt (one file), "
        "and an MCP server (uvx agent-harnesses-mcp) exposing recommend, pick_harness, and search_harnesses.")
    return faq


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
        f"    <a href=\"{SITE_URL}\" title=\"Browse the searchable site\"><img src=\"https://img.shields.io/badge/website-live-5ac4bf.svg\"></a>",
        "    <a href=\"#for-agents\" title=\"Agents can query this list — MCP server, llms.txt & JSON\"><img src=\"https://img.shields.io/badge/agents-query%20this%20list-5ac4bf.svg\"></a>",
        "    <a href=\"#contribution\" title=\"Contributions welcome\"><img src=\"https://img.shields.io/badge/contributions-welcome-green.svg\"></a>",
        "    <a href=\"https://github.com/RyanAlberts/best-of-Agent-Harnesses/commits/main\" title=\"Updates\"><img src=\"https://img.shields.io/github/last-commit/RyanAlberts/best-of-Agent-Harnesses?color=green&label=updated\"></a>",
        "</p>",
        "",
        "<p align=\"center\">",
        f"    🌐 <strong><a href=\"{SITE_URL}\">Browse the searchable site</a></strong> — one page per harness, filter by capability, autonomy &amp; recovery.",
        "</p>",
        "",
        "<p align=\"center\">",
        "    🤖 <strong>Agents can query this list</strong> — an <a href=\"#for-agents\">MCP server</a> (<code>recommend</code>, <code>pick_harness</code>, …), <a href=\"llms.txt\">llms.txt</a> &amp; <a href=\"harnesses.json\">JSON</a>, so your agent recommends harnesses too.",
        "</p>",
        "",
        "<p align=\"center\">",
        "    🧡 <strong>A curated list is only as good as the people who stop mid-scroll to point at what it's missing.</strong><br>",
        "    These folks did exactly that — found a gap, wrote it up, and made the list better than one maintainer ever could.",
        f"    <a href=\"#-thank-you-contributors\"><strong>Meet the {len(CONTRIBUTORS)} →</strong></a>",
        "</p>",
        "",
        "## What is an agent harness?",
        "",
        "A model answers; an agent acts. An agent harness is the runtime that turns one into the other — the model thinks; the harness decides what that thinking is allowed to touch.",
        "",
        "Every prior wave of automation was constrained by brittleness: you scripted exact behavior, and when the world deviated, the system broke. Foundation models inverted that problem—they're flexible but directionless, stateless, and disconnected from anything real. The agent harness exists to bridge that gap: it is the orchestration infrastructure that converts a model's per-turn reasoning into sustained, tool-using, error-recovering, goal-directed behavior across time. Architecturally, it plays the role the kernel played in operating systems or the controller played in industrial robotics—mediating between raw capability and a messy environment—but with a critical difference: the \"capability\" it governs is general-purpose cognition, which means the harness is simultaneously a scheduler, a permission system, a memory manager, and a policy enforcement layer, all under-specified and evolving in real time.",
        "",
        "## Why harnesses matter",
        "",
        "Better models make harnesses more important: more capabilities mean more failure modes, and production needs retry logic, fallbacks, and validation. Harness quality—not just model quality—determines whether agents actually ship. This list ranks projects by relevance to harness concerns (environment, orchestration, lifecycle, guardrails) and by stars/activity.",
        "",
        "## The landscape at a glance",
        "",
        "[![The Agent Harness Landscape — all projects plotted by adoption surface area against GitHub stars](assets/landscape.svg)](assets/landscape.svg)",
        "",
        f"_Every project in the list, plotted by adoption surface area (the [simplicity ↔ capability axis](#guide-to-rankings)) against GitHub stars. Colors are categories; the largest projects in each tier are labeled._",
        "",
        "[![Autonomy × Recovery — every loop-owning project placed by designed autonomy regime and failure-recovery tier](assets/axes-grid.svg)](assets/axes-grid.svg)",
        "",
        "_The same projects placed by how much unsupervised rope they're designed to give (autonomy) and what happens when a run dies (recovery). In the tables below, ★ marks headless-ready projects and ✱ marks durable ones. Both charts regenerate from the list data on every refresh._",
        "",
        "## How to Pick a Harness",
        "",
        "_Start with the guide, then the head-to-head decision pages — grounded in the same data as the tables below:_",
        "",
        "- [**How to pick a harness**](comparisons/how-to-pick-a-harness.md) — six questions that turn this list into a decision, including the post–June 2026 billing reality",
        "- [**OpenClaw vs Hermes**](comparisons/openclaw-vs-hermes.md) — the always-on personal-agent debate: presence vs discipline, plus what the field reports actually say",
        "- [**Terminal coding agents** — opencode vs Codex vs Gemini CLI vs crush vs goose](comparisons/terminal-coding-agents.md)",
        "- [**Multi-agent orchestration** — OpenAI Agents SDK vs CrewAI vs AutoGen vs LangGraph](comparisons/multi-agent-orchestration.md)",
        "- [**Agent memory layers** — Mem0 vs Letta vs claude-mem](comparisons/memory-layers.md)",
        "",
    ]
    header += render_use_cases()
    header += [
        "## For agents",
        "",
        "This list is also published in machine-readable form, so coding agents and research agents can recommend harnesses — not just humans browsing GitHub:",
        "",
        "- [**harnesses.json**](harnesses.json) — every project with category, complexity tier, capability tags, stars, license signal, and a concrete example link, plus the full use-case index.",
        "- [**llms.txt**](llms.txt) — the entire list in one agent-readable file. Point any agent at the [raw URL](https://raw.githubusercontent.com/RyanAlberts/best-of-Agent-Harnesses/main/llms.txt).",
        "- [**MCP server**](mcp/) — `recommend` (one opinionated pick + alternatives + what to *avoid*, e.g. repos flagged for star manipulation), `pick_harness` (ranked, with complexity/autonomy/recovery filters), `search_harnesses`, `get_harness`, `list_categories`, plus `list_comparisons`/`get_comparison` for the decision guides. Published to PyPI and the [official MCP registry](https://registry.modelcontextprotocol.io) as `io.github.RyanAlberts/agent-harnesses`. One-line install (needs [uv](https://docs.astral.sh/uv/)):",
        "",
        "```sh",
        "claude mcp add agent-harnesses -- uvx agent-harnesses-mcp",
        "```",
        "",
        "## Contents",
        "",
        "- [The landscape at a glance](#the-landscape-at-a-glance)",
        "- [How to Pick a Harness](#how-to-pick-a-harness)",
        "- [Pick by use case](#pick-by-use-case)",
        "- [For agents: harnesses.json, llms.txt, MCP server](#for-agents)",
        "- [FAQ](#faq)",
    ]
    for cat_id, title, _ in CATEGORIES:
        count = len(live_projects(cat_id))
        anchor = slug(title)
        header.append(f"- [{title}](#{anchor}) _{count} projects_")
    header += [
        "",
        "## Guide to rankings",
        "",
        f"- ⭐ **Stars** — GitHub star count, captured {STARS_CAPTURED}; tables sort by stars descending.",
        "- ⚖️ **Simplicity ↔ capability** — adoption surface, 4 tiers: **super simple** (a format, one concept) → **mostly simple** (thin layer) → **slightly complex** (real SDK) → **complex** (product suite).",
        "- ★ **Headless-ready** — designed for unattended runs, batches, and fleets (the top of the autonomy scale: step-gated → checkpoint-gated → bounded → headless).",
        "- ✱ **Durable** — persisted execution state survives restarts mid-task (the top of the recovery scale: none → retry → resumable → durable).",
        "- ✅ **Open source** — ✅ standard OSS license · ⚠️ source-available/restricted · ❓ no or unclear license.",
        "- 🏷️ **Tags** — capability chips auto-derived from descriptions; full cross-reference in [TAGS.md](TAGS.md).",
        "- 🎯 **Examples** — one concrete \"show me it in action\" link per project, not a docs root.",
        "",
        "Every project's full autonomy and recovery tier is plotted in the [grid above](#the-landscape-at-a-glance) and carried in [harnesses.json](harnesses.json) and [llms.txt](llms.txt); scores are editorial, from public docs — maintainer corrections via issue/PR are merged fast.",
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
        sorted_projects = sorted(live_projects(cat_id), key=lambda x: stars_for(x.github_id), reverse=True)
        for i, p in enumerate(sorted_projects, 1):
            stars = stars_for(p.github_id)
            stars_cell = f"[{format_stars(stars)}](https://github.com/{p.github_id}/stargazers)"
            examples_cell = f"[{example_label_for(p.github_id)}]({examples_for(p.github_id)})"
            chips = tag_chips_md(p.tags)
            autonomy, recovery = axes_for(p.github_id)
            marks = ("&#8202;★" if autonomy == "headless" else "") + ("&#8202;✱" if recovery == "durable" else "")
            anchor = f'<a name="{project_slug(p.github_id)}"></a>'
            row = f"| {i} | {anchor}[**{p.display_name}**](https://github.com/{p.github_id}){marks} | {stars_cell} | {p.description}{chips} | {p.oss} | {p.axis} | {examples_cell} |"
            body.append(row)
        body.append("")
    graveyard = graveyard_projects()
    if graveyard:
        body.append("## ⚰️ Graveyard")
        body.append("")
        body.append(
            "_Archived upstream, or flagged for curation integrity (e.g. suspected star "
            "manipulation). Kept here — not deleted — for citation and transparency; "
            "excluded from the ranked count, the landscape chart, and harnesses.json's "
            "main list. Curation is the point: a starred repo is not automatically a "
            "credible one._"
        )
        body.append("")
        body.append("| Project | Last ⭐ Stars | Since | Why it's here |")
        body.append("|---------|--------------|-------|---------------|")
        for p in graveyard:
            gid = p.github_id
            stars_cell = format_stars(stars_for(gid))
            row = f"| [{p.display_name}](https://github.com/{gid}) | {stars_cell} | {graveyard_since(gid)} | {graveyard_reason(gid)} |"
            body.append(row)
        body.append("")
    radar = radar_entries()
    if radar:
        body.append("## 🔭 On the radar")
        body.append("")
        body.append(
            "_Up-and-coming candidates — surfaced by the weekly discovery scan or "
            "submitted by the community — that haven't cleared the "
            "[curation bar](CONTRIBUTING.md#curation-bar) or a vetting pass yet. "
            "Stars refresh weekly from the discovery queue; descriptions are the "
            "projects' own, unvetted. Entries graduate into the ranked list above "
            "or drop off._"
        )
        body.append("")
        body.append("| Project | ⭐ Stars | What it says it is | Via |")
        body.append("|---------|---------|--------------------|-----|")
        for e in radar:
            gid = e["github_id"]
            stars_cell = f"[{format_stars(e['stars'])}](https://github.com/{gid}/stargazers)" if e["stars"] else "—"
            body.append(f"| [**{gid.split('/')[-1]}**](https://github.com/{gid}) | {stars_cell} | {e['desc']} | {e['via']} |")
        body.append("")
    body += ["## FAQ", ""]
    for item in build_faq():
        if item["kind"] == "use-case":
            continue  # use-case Q&A already lives in "Pick by use case"; full set is in llms.txt / harnesses.json
        body += [f"### {item['q']}", "", item["a"], ""]
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
        "## 🧡 Thank you, contributors",
        "",
        "The people who stopped mid-scroll, found a gap, and wrote it up — this list is better for each of them:",
        "",
        " · ".join(f"[**@{login}**](https://github.com/{login}) — {what}" for login, what in CONTRIBUTORS),
        "",
        "Accepted submissions land with **co-author credit** on the commit that ships them. Promising "
        "projects that are still early aren't turned away — they get pinned to [🔭 On the radar](#-on-the-radar) "
        "and graduate as they grow. [Add yours →](CONTRIBUTING.md)",
        "",
        "## Contribution",
        "",
        "Contributions are welcome. To add or suggest projects:",
        "",
        "- Open an [issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues) with the repo URL, category, and a short description.",
        "- Or submit a pull request against [scripts/generate.py](https://github.com/RyanAlberts/best-of-Agent-Harnesses/blob/main/scripts/generate.py) — this README, projects.yaml, and TAGS.md are generated from it, so direct edits to them can't merge.",
        "",
        "Promising projects that don't clear the curation bar yet get pinned to [🔭 On the radar](#-on-the-radar) — a submission that lands there isn't rejected, it's queued.",
        "",
        "For contribution guidelines, see [CONTRIBUTING.md](https://github.com/RyanAlberts/best-of-Agent-Harnesses/blob/main/CONTRIBUTING.md) and the [Code of Conduct](https://github.com/RyanAlberts/best-of-Agent-Harnesses/blob/main/.github/CODE_OF_CONDUCT.md).",
        "",
        "### Show your listing",
        "",
        "If your project is in this list, you're welcome to show it in your README:",
        "",
        "[![Best of Agent Harnesses](https://img.shields.io/badge/%F0%9F%8F%86_Best_of-Agent_Harnesses-5ac4bf)](https://github.com/RyanAlberts/best-of-Agent-Harnesses)",
        "",
        "```md",
        "[![Best of Agent Harnesses](https://img.shields.io/badge/%F0%9F%8F%86_Best_of-Agent_Harnesses-5ac4bf)](https://github.com/RyanAlberts/best-of-Agent-Harnesses)",
        "```",
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
        "    <a href=\"https://github.com/RyanAlberts/best-of-Agent-Harnesses/commits/main\" title=\"Updates\"><img src=\"https://img.shields.io/github/last-commit/RyanAlberts/best-of-Agent-Harnesses?color=green&label=updated\"></a>\n"
        "</p>\n"
        "\n"
        "## What is an agent harness?\n"
        "\n"
        "A model answers; an agent acts. An agent harness is the runtime that turns one into the other — the model thinks; the harness decides what that thinking is allowed to touch.\n"
        "\n"
        "Every prior wave of automation was constrained by brittleness: you scripted exact behavior, and when the world deviated, the system broke. Foundation models inverted that problem—they're flexible but directionless, stateless, and disconnected from anything real. The agent harness exists to bridge that gap: it is the orchestration infrastructure that converts a model's per-turn reasoning into sustained, tool-using, error-recovering, goal-directed behavior across time. Architecturally, it plays the role the kernel played in operating systems or the controller played in industrial robotics—mediating between raw capability and a messy environment—but with a critical difference: the \"capability\" it governs is general-purpose cognition, which means the harness is simultaneously a scheduler, a permission system, a memory manager, and a policy enforcement layer, all under-specified and evolving in real time.\n"
        "\n"
        "If you want to add or update projects, open an [issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues), submit a [pull request](https://github.com/RyanAlberts/best-of-Agent-Harnesses/pulls), or edit [projects.yaml](https://github.com/RyanAlberts/best-of-Agent-Harnesses/blob/main/projects.yaml). Contributions are welcome!\n"
    )


def generate_tags_md() -> str:
    """Cross-reference page: every canonical tag listed once, with the
    projects that carry it grouped by category.  Auto-derived from PROJECTS
    + TAG_RULES; do not hand-edit TAGS.md.
    """
    by_tag: dict = {tag: [] for tag, _ in TAG_RULES}
    by_tag.setdefault("python", [])
    by_tag.setdefault("typescript", [])
    for cat_id, cat_title, _ in CATEGORIES:
        for p in live_projects(cat_id):
            for t in p.tags:
                by_tag.setdefault(t, []).append((p, cat_title))

    total = count_projects()
    lines = [
        "<!-- markdownlint-disable -->",
        "# Tags — cross-reference",
        "",
        f"_Auto-generated from `scripts/generate.py`. {total} projects across "
        f"{sum(1 for v in by_tag.values() if v)} canonical tags. Edit projects "
        f"in `generate.py` (not here) and rerun the script._",
        "",
        "Tag chips appear next to each project in [README.md](README.md). This "
        "page lists every tag once with the projects that carry it, grouped "
        "by category and sorted by GitHub stars within each category.",
        "",
        "## All tags",
        "",
    ]
    tag_order = [t for t, _ in TAG_RULES] + ["python", "typescript"]
    seen_tags: set = set()
    chip_index: list = []
    for t in tag_order:
        if t in seen_tags:
            continue
        seen_tags.add(t)
        count = len(by_tag.get(t, []))
        if count == 0:
            continue
        chip_index.append(f"[`{t}`](#{slug(t)}) ({count})")
    lines.append(" · ".join(chip_index))
    lines.append("")

    for t in tag_order:
        entries = by_tag.get(t, [])
        if not entries:
            continue
        lines.append("---")
        lines.append("")
        lines.append(f"## `{t}`")
        lines.append("")
        by_cat: dict = {ct: [] for _, ct, _ in CATEGORIES}
        for p, ct in entries:
            by_cat[ct].append(p)
        for _, ct, _ in CATEGORIES:
            picks = by_cat.get(ct) or []
            if not picks:
                continue
            picks = sorted(picks, key=lambda x: stars_for(x.github_id), reverse=True)
            lines.append(f"**{ct}**")
            lines.append("")
            for p in picks:
                stars = stars_for(p.github_id)
                star_str = f" — ⭐{format_stars(stars)}" if stars else ""
                lines.append(
                    f"- [{p.display_name}](https://github.com/{p.github_id}){star_str} — {p.description}"
                )
            lines.append("")
    return "\n".join(lines)


def oss_signal(marker: str) -> str:
    if marker.startswith("✅"):
        return "open-source"
    if marker.startswith("⚠️"):
        rest = marker.replace("⚠️", "").strip()
        return f"restricted ({rest})" if rest else "restricted"
    return "unknown"


def comparisons_index() -> list:
    """Index of comparisons/*.md for harnesses.json — slug, title, and first
    prose paragraph as summary — so the MCP server can list and fetch the
    decision guides without hardcoding them."""
    out = []
    for f in sorted((REPO_ROOT / "comparisons").glob("*.md")):
        lines = f.read_text().split("\n")
        title = next((l[2:].strip() for l in lines if l.startswith("# ")), f.stem)
        summary = next((l.strip() for l in lines
                        if l.strip() and not l.startswith(("#", "|", "_", "-", "[", "<", "!"))), "")
        out.append({
            "slug": f.stem,
            "title": title,
            "summary": summary[:300],
            "url": f"https://github.com/RyanAlberts/best-of-Agent-Harnesses/blob/main/comparisons/{f.name}",
            "raw_url": f"https://raw.githubusercontent.com/RyanAlberts/best-of-Agent-Harnesses/main/comparisons/{f.name}",
        })
    return out


def generate_harnesses_json() -> str:
    import json
    projects = []
    for cat_id, cat_title, _ in CATEGORIES:
        for p in sorted(live_projects(cat_id), key=lambda x: stars_for(x.github_id), reverse=True):
            tier = tier_of(p)
            autonomy, recovery = axes_for(p.github_id)
            projects.append({
                "name": p.display_name,
                "github_id": p.github_id,
                "url": f"https://github.com/{p.github_id}",
                "slug": project_slug(p.github_id),
                "anchor_url": project_anchor_url(p.github_id),
                "page_url": project_page_url(p.github_id),
                "description": p.description,
                "category": cat_id,
                "category_title": cat_title,
                "stars": stars_for(p.github_id),
                "tier": tier,
                "tier_rank": TIER_ORDER.index(tier) + 1,
                "axis": p.axis,
                "autonomy": autonomy,
                "autonomy_rank": autonomy_rank(autonomy),
                "recovery": recovery,
                "recovery_rank": recovery_rank(recovery),
                "license_signal": oss_signal(p.oss),
                "tags": p.tags,
                "example": {"label": example_label_for(p.github_id), "url": examples_for(p.github_id)},
            })
    doc = {
        "meta": {
            "name": "best-of-Agent-Harnesses",
            "description": "Hand-curated, ranked list of AI agent harnesses, orchestration frameworks, and harness techniques.",
            "url": "https://github.com/RyanAlberts/best-of-Agent-Harnesses",
            "site_url": SITE_URL,
            "llms_txt_url": f"{RAW_BASE}/llms.txt",
            "jsonld_url": f"{RAW_BASE}/harnesses.jsonld",
            "feed_url": f"{SITE_URL}feed.json",
            "license": "CC-BY-SA-4.0",
            "stars_captured": STARS_CAPTURED,
            "project_count": count_projects(),
            "graveyard_count": graveyard_count(),
            "tiers": TIER_ORDER,
            "tier_help": "Adoption surface area, least to most: tier_rank 1 = format-only/single concept, 4 = platform with its own runtime and ecosystem.",
            "autonomy_tiers": AUTONOMY_TIERS,
            "autonomy_help": "Designed autonomy regime, least to most: rank 1 = human approves each action, 4 = built for unattended runs and fleets. rank 0 / 'n/a' = doesn't own an agent loop.",
            "recovery_tiers": RECOVERY_TIERS,
            "recovery_help": "Behavior when a run dies mid-task, weakest to strongest: rank 1 = start over, 4 = persisted execution state survives restarts. rank 0 / 'n/a' = doesn't execute.",
        },
        "categories": [{"id": c, "title": t, "subtitle": s} for c, t, s in CATEGORIES],
        "use_cases": [
            {"intent": intent, "picks": [g for g in ids if not is_graveyard(g)], "category_title": cat}
            for intent, ids, cat in USE_CASES
        ],
        "faq": build_faq(),
        "comparisons": comparisons_index(),
        "projects": projects,
        "graveyard": [
            {
                "github_id": p.github_id,
                "name": p.display_name,
                "last_stars": stars_for(p.github_id),
                "since": graveyard_since(p.github_id),
                "reason": graveyard_reason(p.github_id),
            }
            for p in graveyard_projects()
        ],
        "radar": radar_entries(),
    }
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def generate_llms_txt() -> str:
    total = count_projects()
    n_categories = len(CATEGORIES)
    lines = [
        "# Best of Agent Harnesses",
        "",
        f"> Hand-curated, ranked list of {total} AI agent harnesses — the runtimes that close the loop between a stateless model and the outside world. {n_categories} categories, a 4-tier adoption-surface rating (simplicity ↔ capability), capability tags, a license signal, and one concrete example link per project. Stars captured {STARS_CAPTURED}.",
        "",
        "Maintained at https://github.com/RyanAlberts/best-of-Agent-Harnesses (CC-BY-SA-4.0).",
        "Structured data: https://raw.githubusercontent.com/RyanAlberts/best-of-Agent-Harnesses/main/harnesses.json",
        f"Tiers, least to most adoption surface: {' → '.join(TIER_ORDER)}.",
        "",
        "## Pick by use case",
        "",
    ]
    for intent, ids, _ in USE_CASES:
        live_ids = [g for g in ids if not is_graveyard(g)]
        picks = ", ".join(f"{find_project(g).display_name} (https://github.com/{g})" for g in live_ids)
        lines.append(f"- {intent}: {picks}")
    lines.append("")
    lines += ["## FAQ", ""]
    for item in build_faq():
        lines.append(f"### {item['q']}")
        lines.append(item["a"])
        lines.append("")
    for cat_id, title, subtitle in CATEGORIES:
        lines.append(f"## {title} ({len(live_projects(cat_id))} projects)")
        lines.append("")
        lines.append(f"{subtitle}")
        lines.append("")
        for p in sorted(live_projects(cat_id), key=lambda x: stars_for(x.github_id), reverse=True):
            tags = (" [" + ", ".join(p.tags) + "]") if p.tags else ""
            autonomy, recovery = axes_for(p.github_id)
            lines.append(
                f"- [{p.display_name}](https://github.com/{p.github_id}) — "
                f"⭐{format_stars(stars_for(p.github_id))}, {tier_of(p)}, autonomy: {autonomy}, "
                f"recovery: {recovery}, {oss_signal(p.oss)}: {p.description}{tags}"
            )
        lines.append("")
    return "\n".join(lines)


# Category colors + short legend labels for the landscape SVG.
LANDSCAPE_STYLE = {
    "progressive-disclosure": ("#8b5cf6", "Progressive disclosure"),
    "coding-agent-products": ("#ef4444", "Coding agents"),
    "coding-harness-configs": ("#f59e0b", "Configs & SDKs"),
    "personal-agent-runtimes": ("#0ea5e9", "Personal agents"),
    "frameworks": ("#3b82f6", "Frameworks"),
    "multi-agent": ("#ec4899", "Multi-agent"),
    "plugins-mcp-cli": ("#10b981", "Plugins & MCP"),
    "memory": ("#84cc16", "Memory & state"),
    "evaluation": ("#64748b", "Evals & benchmarks"),
    "observability": ("#6366f1", "Observability"),
    "research-task": ("#14b8a6", "Research"),
    "libraries-sdks": ("#a16207", "Libraries & SDKs"),
}

LABELS_PER_TIER = 6  # label the top-N starred projects in each tier column


def generate_landscape_svg() -> str:
    import hashlib
    import math
    from xml.sax.saxutils import escape

    W, H = 1320, 880
    X0, X1, Y0, Y1 = 80, 1290, 168, 750
    colw = (X1 - X0) / len(TIER_ORDER)
    lo, hi = 0.3, 5.4  # log10 star range: ~2 to ~250k

    def ypos(stars: int) -> float:
        return Y1 - (math.log10(max(stars, 2)) - lo) / (hi - lo) * (Y1 - Y0)

    def xpos(tier: str, github_id: str) -> float:
        col = TIER_ORDER.index(tier)
        jitter = int(hashlib.md5(github_id.encode()).hexdigest(), 16) % 1000 / 1000
        return X0 + colw * (col + 0.18 + 0.64 * jitter)

    pts = []
    for cat_id, _, _ in CATEGORIES:
        for p in live_projects(cat_id):
            s = stars_for(p.github_id)
            pts.append((p, cat_id, tier_of(p), s, xpos(tier_of(p), p.github_id), ypos(s)))

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="-apple-system, \'Segoe UI\', Helvetica, Arial, sans-serif">',
        f'<rect width="{W}" height="{H}" fill="#ffffff" rx="8"/>',
        f'<text x="{W/2}" y="52" text-anchor="middle" font-size="30" font-weight="700" fill="#111827">The Agent Harness Landscape</text>',
        f'<text x="{W/2}" y="80" text-anchor="middle" font-size="15" fill="#6b7280">{count_projects()} hand-curated projects · GitHub stars vs. adoption surface area · stars captured {STARS_CAPTURED}</text>',
    ]

    # legend (wraps to a second row when categories overflow the width)
    lx = X0
    ly = 110
    for cat_id, _, _ in CATEGORIES:
        color, label = LANDSCAPE_STYLE[cat_id]
        if lx > X1 - 180:
            lx = X0
            ly += 22
        svg.append(f'<circle cx="{lx}" cy="{ly - 4}" r="6" fill="{color}"/>')
        svg.append(f'<text x="{lx + 11}" y="{ly}" font-size="12.5" fill="#374151">{escape(label)}</text>')
        lx += 11 + len(label) * 6.6 + 26

    # horizontal gridlines at star decades
    for decade, lab in [(10, "10"), (100, "100"), (1000, "1k"), (10000, "10k"), (100000, "100k")]:
        y = ypos(decade)
        svg.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X1}" y2="{y:.1f}" stroke="#e5e7eb" stroke-width="1"/>')
        svg.append(f'<text x="{X0 - 10}" y="{y + 4:.1f}" text-anchor="end" font-size="12" fill="#9ca3af">{lab}</text>')
    svg.append(f'<text x="30" y="{(Y0 + Y1) / 2:.0f}" font-size="13" fill="#6b7280" transform="rotate(-90 30 {(Y0 + Y1) / 2:.0f})" text-anchor="middle">GitHub stars (log scale)</text>')

    # tier column separators + captions
    tier_counts = {t: 0 for t in TIER_ORDER}
    for _, _, t, _, _, _ in pts:
        tier_counts[t] += 1
    for i, t in enumerate(TIER_ORDER):
        cx = X0 + colw * (i + 0.5)
        if i:
            x = X0 + colw * i
            svg.append(f'<line x1="{x:.1f}" y1="{Y0}" x2="{x:.1f}" y2="{Y1}" stroke="#e5e7eb" stroke-width="1" stroke-dasharray="4 4"/>')
        svg.append(f'<text x="{cx:.1f}" y="{Y1 + 30}" text-anchor="middle" font-size="15" font-weight="600" fill="#111827">{escape(t)}</text>')
        svg.append(f'<text x="{cx:.1f}" y="{Y1 + 50}" text-anchor="middle" font-size="12" fill="#9ca3af">{tier_counts[t]} projects</text>')
    svg.append(f'<line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="#d1d5db" stroke-width="1.5"/>')
    svg.append(f'<text x="{(X0 + X1) / 2}" y="{Y1 + 80}" text-anchor="middle" font-size="13" fill="#6b7280">←  less to adopt: a file format, one concept&#160;&#160;·&#160;&#160;simplicity ↔ capability&#160;&#160;·&#160;&#160;full platforms with their own runtime: more to adopt  →</text>')

    # pick label set: top-N starred per tier
    labeled = set()
    for t in TIER_ORDER:
        col = sorted((q for q in pts if q[2] == t), key=lambda q: q[3], reverse=True)
        labeled.update(q[0].github_id for q in col[:LABELS_PER_TIER])

    # dots (small first so labeled big dots draw on top)
    for p, cat_id, t, s, x, y in sorted(pts, key=lambda q: q[3]):
        color, _ = LANDSCAPE_STYLE[cat_id]
        big = p.github_id in labeled
        r = 6.5 if big else 4.5
        svg.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" fill-opacity="0.85" stroke="#ffffff" stroke-width="1.2">'
            f'<title>{escape(p.display_name)} — ⭐{format_stars(s)}</title></circle>'
        )

    # labels with greedy vertical de-overlap per column
    for i, t in enumerate(TIER_ORDER):
        col = sorted((q for q in pts if q[2] == t and q[0].github_id in labeled), key=lambda q: q[5])
        last_y = -1e9
        for p, cat_id, _, s, x, y in col:
            ty = max(y + 4.5, last_y + 16)
            last_y = ty
            anchor, tx = ("start", x + 10)
            if x > X0 + colw * (i + 0.72):  # too close to the right edge of the column
                anchor, tx = ("end", x - 10)
            svg.append(f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}" font-size="13" font-weight="600" fill="#1f2937">{escape(p.display_name)}</text>')

    svg.append(f'<text x="{X1}" y="{H - 18}" text-anchor="end" font-size="12" fill="#9ca3af">github.com/RyanAlberts/best-of-Agent-Harnesses · CC BY-SA 4.0 · regenerated by scripts/generate.py</text>')
    svg.append('</svg>')
    return "\n".join(svg) + "\n"


def refresh_comparisons() -> list:
    """Patch the "⭐ Stars" row of each table in comparisons/*.md to current
    META counts, matching columns by the github.com links in the table header.
    The prose in those pages is hand-written; only the stars row is touched.
    """
    updated = []
    for f in sorted((REPO_ROOT / "comparisons").glob("*.md")):
        lines = f.read_text().split("\n")
        header_ids: list = []
        dirty = False
        for i, line in enumerate(lines):
            if not line.startswith("|"):
                continue
            if "github.com/" in line and not header_ids:
                header_ids = re.findall(r"github\.com/([\w.-]+/[\w.-]+)\)", line)
            elif line.startswith("| ⭐ Stars |") and header_ids:
                if all(stars_for(g) > 0 for g in header_ids):
                    cells = " | ".join(format_stars(stars_for(g)) for g in header_ids)
                    new_line = f"| ⭐ Stars | {cells} |"
                    if new_line != line:
                        lines[i] = new_line
                        dirty = True
                else:
                    print(f"WARNING: {f.name}: unknown github_id in table header, stars row left alone")
                header_ids = []
        if dirty:
            f.write_text("\n".join(lines))
            updated.append(f.name)
    return updated


def generate_axes_svg() -> str:
    """Autonomy × Recovery grid: every loop-owning project as a dot in a 4×4
    matrix; the top-starred project in each cell is labeled. n/a entries
    (formats, components, datasets) are excluded and counted in the footer.
    """
    import hashlib
    from xml.sax.saxutils import escape

    W, H = 1100, 800
    X0, X1, Y0, Y1 = 190, 1060, 130, 660
    cw = (X1 - X0) / len(AUTONOMY_TIERS)
    ch = (Y1 - Y0) / len(RECOVERY_TIERS)

    pts, na = [], 0
    for cat_id, _, _ in CATEGORIES:
        for p in live_projects(cat_id):
            a, r = axes_for(p.github_id)
            if a == "n/a" or r == "n/a":
                na += 1
                continue
            ai, ri = AUTONOMY_TIERS.index(a), RECOVERY_TIERS.index(r)
            h = int(hashlib.md5(p.github_id.encode()).hexdigest(), 16)
            jx, jy = (h % 1000) / 1000, (h // 1000 % 1000) / 1000
            x = X0 + cw * (ai + 0.15 + 0.70 * jx)
            y = Y1 - ch * (ri + 0.20 + 0.60 * jy)
            pts.append((p, cat_id, ai, ri, x, y))

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="-apple-system, \'Segoe UI\', Helvetica, Arial, sans-serif">',
        f'<rect width="{W}" height="{H}" fill="#ffffff" rx="8"/>',
        f'<text x="{W/2}" y="50" text-anchor="middle" font-size="28" font-weight="700" fill="#111827">Autonomy × Recovery</text>',
        f'<text x="{W/2}" y="78" text-anchor="middle" font-size="14.5" fill="#6b7280">how much rope each harness is designed to give · what happens when a run dies mid-task</text>',
        f'<text x="{W/2}" y="100" text-anchor="middle" font-size="12.5" fill="#9ca3af">★ headless column = unattended-ready &#160;·&#160; ✱ durable row = survives restarts &#160;·&#160; colors follow the landscape chart</text>',
    ]

    # grid + axis tier labels
    for i in range(len(AUTONOMY_TIERS) + 1):
        x = X0 + cw * i
        svg.append(f'<line x1="{x:.1f}" y1="{Y0}" x2="{x:.1f}" y2="{Y1}" stroke="#e5e7eb" stroke-width="1"/>')
    for i in range(len(RECOVERY_TIERS) + 1):
        y = Y0 + ch * i
        svg.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X1}" y2="{y:.1f}" stroke="#e5e7eb" stroke-width="1"/>')
    for i, t in enumerate(AUTONOMY_TIERS):
        cx = X0 + cw * (i + 0.5)
        mark = " ★" if t == "headless" else ""
        svg.append(f'<text x="{cx:.1f}" y="{Y1 + 28}" text-anchor="middle" font-size="14.5" font-weight="600" fill="#111827">{escape(t)}{mark}</text>')
    svg.append(f'<text x="{(X0 + X1) / 2}" y="{Y1 + 56}" text-anchor="middle" font-size="13" fill="#6b7280">autonomy: human approves each step&#160;&#160;→&#160;&#160;built for unattended fleets</text>')
    for i, t in enumerate(RECOVERY_TIERS):
        cy = Y0 + ch * (len(RECOVERY_TIERS) - i - 0.5)
        mark = " ✱" if t == "durable" else ""
        svg.append(f'<text x="{X0 - 14}" y="{cy + 5:.1f}" text-anchor="end" font-size="14.5" font-weight="600" fill="#111827">{escape(t)}{mark}</text>')
    svg.append(f'<text x="44" y="{(Y0 + Y1) / 2:.0f}" font-size="13" fill="#6b7280" transform="rotate(-90 44 {(Y0 + Y1) / 2:.0f})" text-anchor="middle">recovery: crash = start over&#160;&#160;→&#160;&#160;survives restarts</text>')

    # faint per-cell counts
    cells: dict = {}
    for p, cat_id, ai, ri, x, y in pts:
        cells.setdefault((ai, ri), []).append((p, cat_id, x, y))
    for (ai, ri), members in cells.items():
        bx = X0 + cw * (ai + 1) - 10
        by = Y1 - ch * ri - 8
        svg.append(f'<text x="{bx:.1f}" y="{by:.1f}" text-anchor="end" font-size="12" fill="#d1d5db" font-weight="700">{len(members)}</text>')

    # dots, biggest stars on top
    for p, cat_id, ai, ri, x, y in sorted(pts, key=lambda q: stars_for(q[0].github_id)):
        color, _ = LANDSCAPE_STYLE[cat_id]
        svg.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{color}" fill-opacity="0.85" stroke="#ffffff" stroke-width="1.2">'
            f'<title>{escape(p.display_name)} — ⭐{format_stars(stars_for(p.github_id))}</title></circle>'
        )

    # label the top-starred project per cell
    for (ai, ri), members in cells.items():
        p, cat_id, x, y = max(members, key=lambda m: stars_for(m[0].github_id))
        anchor, tx = ("start", x + 9)
        if x > X0 + cw * (ai + 0.6):
            anchor, tx = ("end", x - 9)
        svg.append(f'<text x="{tx:.1f}" y="{y + 4.5:.1f}" text-anchor="{anchor}" font-size="12.5" font-weight="600" fill="#1f2937">{escape(p.display_name)}</text>')

    svg.append(f'<text x="{X1}" y="{H - 16}" text-anchor="end" font-size="12" fill="#9ca3af">{len(pts)} loop-owning projects shown · {na} format/component entries (n/a) omitted · full tiers in harnesses.json</text>')
    svg.append('</svg>')
    return "\n".join(svg) + "\n"


def generate_jsonld() -> str:
    """schema.org JSON-LD (Dataset + ItemList of SoftwareApplications). GitHub
    strips inline JSON-LD from rendered READMEs, so this is served as a
    standalone file and embedded in every Pages-site page, where search crawlers
    and AI answer engines can read it."""
    import json
    items = []
    for i, p in enumerate(ordered_projects(), 1):
        items.append({
            "@type": "ListItem",
            "position": i,
            "item": {
                "@type": "SoftwareApplication",
                "name": p.display_name,
                "url": f"https://github.com/{p.github_id}",
                "description": p.description,
                "applicationCategory": "DeveloperApplication",
                "keywords": ", ".join(p.tags),
            },
        })
    doc = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": "Best of Agent Harnesses",
        "description": "Hand-curated, ranked list of AI agent harnesses, orchestration frameworks, and harness techniques.",
        "url": SITE_URL,
        "sameAs": REPO_HTTP,
        "license": "https://creativecommons.org/licenses/by-sa/4.0/",
        "creator": {"@type": "Person", "name": "Ryan Alberts", "url": "https://github.com/RyanAlberts"},
        "dateModified": STARS_CAPTURED,
        "keywords": ["agent harness", "AI agents", "LLM", "MCP", "agentic AI", "orchestration"],
        "distribution": [{
            "@type": "DataDownload",
            "encodingFormat": "application/json",
            "contentUrl": f"{RAW_BASE}/harnesses.json",
        }],
        "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": items},
    }
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def generate_feed_json() -> str:
    """JSON Feed 1.1 of list refreshes — one dated item per stars-capture date,
    so aggregators and agents can subscribe to "what changed." Prepends the
    current refresh to any existing items (dedup by id, newest first, cap 50)."""
    import json
    top = ordered_projects()[:5]
    item = {
        "id": f"refresh-{STARS_CAPTURED}",
        "title": f"Agent Harnesses list refreshed — {STARS_CAPTURED}",
        "url": REPO_HTTP,
        "date_published": f"{STARS_CAPTURED}T00:00:00Z",
        "content_text": (
            f"{count_projects()} harnesses across {len(CATEGORIES)} categories. "
            f"Stars captured {STARS_CAPTURED}. Most-starred: "
            + ", ".join(p.display_name for p in top) + "."
        ),
    }
    items = [item]
    existing = REPO_ROOT / "feed.json"
    if existing.exists():
        try:
            prev = json.loads(existing.read_text()).get("items", [])
            items += [it for it in prev if it.get("id") != item["id"]]
        except (ValueError, OSError):
            pass
    doc = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": "best-of-Agent-Harnesses — updates",
        "home_page_url": REPO_HTTP,
        "feed_url": f"{SITE_URL}feed.json",
        "description": "Weekly refreshes of the curated agent-harness list.",
        "authors": [{"name": "Ryan Alberts", "url": "https://github.com/RyanAlberts"}],
        "items": items[:50],
    }
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def generate_social_svg() -> str:
    """1280×640 social-preview card. Counts are live so it never drifts.
    Rasterize for GitHub (Settings → Social preview needs PNG/JPG) with:
        rsvg-convert assets/social-preview.svg -o assets/social-preview.png"""
    total = count_projects()
    ncat = len(CATEGORIES)
    bg, fg, sub, accent = "#0d1117", "#f0f6fc", "#9ca3af", "#5ac4bf"
    f = "Helvetica,Arial,sans-serif"
    return "\n".join([
        '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="640" viewBox="0 0 1280 640">',
        f'  <rect width="1280" height="640" fill="{bg}"/>',
        f'  <rect x="0" y="0" width="1280" height="10" fill="{accent}"/>',
        f'  <rect x="80" y="150" width="44" height="44" rx="10" fill="{accent}"/>',
        f'  <text x="140" y="184" font-family="{f}" font-size="32" fill="{accent}" font-weight="700">best-of-Agent-Harnesses</text>',
        f'  <text x="80" y="300" font-family="{f}" font-size="74" fill="{fg}" font-weight="800">Best of Agent Harnesses</text>',
        f'  <text x="80" y="378" font-family="{f}" font-size="38" fill="{sub}">The runtimes that close the loop between a model and the world.</text>',
        f'  <text x="80" y="500" font-family="{f}" font-size="36" fill="{fg}" font-weight="600">{total} harnesses · {ncat} categories · MCP-ready · weekly-rescored</text>',
        f'  <text x="80" y="566" font-family="{f}" font-size="27" fill="{sub}">github.com/RyanAlberts/best-of-Agent-Harnesses</text>',
        '</svg>',
        '',
    ])


def main():
    all_ids = {p.github_id for plist in PROJECTS.values() for p in plist}
    orphans = set(AXES) - all_ids
    if orphans:
        raise KeyError(f"AXES has entries for unknown projects: {sorted(orphans)}")
    yaml_content = generate_yaml()
    readme_content = generate_readme()
    header_content = generate_header_md()
    tags_content = generate_tags_md()
    (REPO_ROOT / "projects.yaml").write_text(yaml_content)
    (REPO_ROOT / "README.md").write_text(readme_content)
    (REPO_ROOT / "config" / "header.md").write_text(header_content)
    (REPO_ROOT / "TAGS.md").write_text(tags_content)
    (REPO_ROOT / "harnesses.json").write_text(generate_harnesses_json())
    (REPO_ROOT / "harnesses.jsonld").write_text(generate_jsonld())
    (REPO_ROOT / "llms.txt").write_text(generate_llms_txt())
    (REPO_ROOT / "feed.json").write_text(generate_feed_json())
    (REPO_ROOT / "assets").mkdir(exist_ok=True)
    (REPO_ROOT / "assets" / "landscape.svg").write_text(generate_landscape_svg())
    (REPO_ROOT / "assets" / "axes-grid.svg").write_text(generate_axes_svg())
    (REPO_ROOT / "assets" / "social-preview.svg").write_text(generate_social_svg())
    refreshed = refresh_comparisons()
    if refreshed:
        print(f"Comparison star rows refreshed: {', '.join(refreshed)}")
    total = count_projects()
    print(f"Wrote {total} projects across {len(CATEGORIES)} categories.")
    for cat_id, title, _ in CATEGORIES:
        print(f"  {title}: {len(PROJECTS[cat_id])}")
    tag_counts: dict = {}
    for cat_id, _, _ in CATEGORIES:
        for p in PROJECTS[cat_id]:
            for t in p.tags:
                tag_counts[t] = tag_counts.get(t, 0) + 1
    print(f"Tag coverage: {len(tag_counts)} tags across {total} projects.")
    for t in sorted(tag_counts, key=lambda x: (-tag_counts[x], x)):
        print(f"  {t}: {tag_counts[t]}")


if __name__ == "__main__":
    main()
