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

- **⭐ Stars:** GitHub star count, captured 2026-05-05. Each table is sorted by stars descending. Click a star count to jump to the GitHub repo's stargazers page.
- **Examples:** A link to the project in action — official docs, examples folder, leaderboard, or paper — whichever is the most useful "show me how it works" link.
- **Simplicity ↔ capability:** Where each project sits on a 4-tier scale describing how much surface area you take on when adopting it: **super simple** (format-only, single file, one concept) → **mostly simple** (lean API, thin layer over a primitive) → **slightly complex** (multi-file SDK, several knobs, real abstractions) → **complex (product suite)** (platform with its own runtime, UI, ecosystem).
- **Open source:** ✅ = standard open-source license (MIT/Apache/BSD/GPL/MPL/AGPL/CC0). ⚠️ = source-available or restricted (e.g. n8n Fair-code, Elastic-2.0, Polyform). ❓ = no license file or unclear terms.

<br>

## Progressive disclosure harnesses

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Formats, runtimes, and patterns that reveal context, tools, or instructions in layers—index first, details on demand—to control tokens and improve agent focus (the "map, not encyclopedia" principle)._

| # | Project | ⭐ Stars | Description | Open source | Simplicity ↔ capability | Examples |
|---|---------|---------|-------------|-------------|-------------------------|----------|
| 1 | [**awesome-cursorrules**](https://github.com/PatrickJS/awesome-cursorrules) | [39.4k](https://github.com/PatrickJS/awesome-cursorrules/stargazers) | Curated .cursorrules and skills that leverage Cursor's index-then-load model; the canonical collection for rules-as-progressive-disclosure in the IDE. | ✅ | super simple (content bundle) | [Examples](https://github.com/PatrickJS/awesome-cursorrules#rules) |
| 2 | [**agents.md**](https://github.com/agentsmd/agents.md) | [21k](https://github.com/agentsmd/agents.md/stargazers) | Open format for repo-scoped agent briefings; v1.1 adds hierarchical scope and progressive disclosure so agents get a map of what exists, then load only what's relevant. | ✅ | super simple (format only) | [Examples](https://agents.md) |
| 3 | [**langgraph-bigtool**](https://github.com/langchain-ai/langgraph-bigtool) | [533](https://github.com/langchain-ai/langgraph-bigtool/stargazers) | Build LangGraph agents with large tool sets; retrieval and on-demand tool loading so agents scale beyond context without stuffing every schema upfront. | ✅ | slightly complex (large tool sets) | [Examples](https://github.com/langchain-ai/langgraph-bigtool#example-usage) |
| 4 | [**MCP-Zero**](https://github.com/xfey/MCP-Zero) | [480](https://github.com/xfey/MCP-Zero/stargazers) | Active tool discovery for autonomous agents: model requests tools by requirement; hierarchical semantic routing over 308 servers / 2,797 tools with ~98% token reduction (APIBank). | ✅ | complex (3k tools, full routing) | [Examples](https://arxiv.org/abs/2506.01056) |
| 5 | [**ToolGen**](https://github.com/Reason-Wang/ToolGen) | [177](https://github.com/Reason-Wang/ToolGen/stargazers) | ICLR 2025: unified tool retrieval and calling via generation; 47k+ tools without context stuffing—retrieval and invocation in one generative step. | ❓ | complex (47k+ tools) | [Examples](https://github.com/Reason-Wang/ToolGen#quick-start) |
| 6 | [**spring-ai-tool-search-tool**](https://github.com/spring-ai-community/spring-ai-tool-search-tool) | [66](https://github.com/spring-ai-community/spring-ai-tool-search-tool/stargazers) | Dynamic tool discovery for Spring AI: model gets a search tool first, then pulls definitions for relevant tools; 34–64% token reduction across providers. | ✅ | mostly simple (search-then-load) | [Examples](https://github.com/spring-ai-community/spring-ai-tool-search-tool#examples) |
| 7 | [**ToolRAG**](https://github.com/antl3x/ToolRAG) | [22](https://github.com/antl3x/ToolRAG/stargazers) | Semantic tool retrieval for LLMs; serves only the tools the user query demands (MCP-compatible), unlimited tool sets with zero context penalty. | ✅ | mostly simple (query-driven retrieval) | [Examples](https://github.com/antl3x/ToolRAG#quick-start) |

## Coding agent products (IDEs, CLIs, full suites)

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Turnkey coding agents you install and run: IDE extensions, terminal CLIs, Dockerized workspaces. Each entry notes which part is the harness (the agent loop, tool wiring, approval model) versus the UI shell (VS Code extension, TUI, browser client)._

| # | Project | ⭐ Stars | Description | Open source | Simplicity ↔ capability | Examples |
|---|---------|---------|-------------|-------------|-------------------------|----------|
| 1 | [**opencode**](https://github.com/anomalyco/opencode) | [155k](https://github.com/anomalyco/opencode/stargazers) | Open-source terminal coding agent (formerly `sst/opencode`; transferred to anomalyco). The **harness** is a multi-provider tool-call loop (Claude, OpenAI, Gemini, local) with strong plugin and MCP support; the TUI is the shell. 100% OSS, very actively shipped. | ✅ | slightly complex (multi-provider, plugins, MCP) | [Examples](https://opencode.ai/docs) |
| 2 | [**Gemini CLI**](https://github.com/google-gemini/gemini-cli) | [103k](https://github.com/google-gemini/gemini-cli/stargazers) | Google's first-party terminal agent for Gemini. The **harness** is the plugin/MCP tool-call loop; the terminal is the shell—Google's parallel to Claude Code / Codex, not just an API. | ✅ | slightly complex (official CLI, plugins, MCP) | [Examples](https://github.com/google-gemini/gemini-cli/tree/main/docs) |
| 3 | [**Codex**](https://github.com/openai/codex) | [80k](https://github.com/openai/codex/stargazers) | OpenAI's terminal coding agent. The **harness** is the sandboxed tool-call loop with multi-provider support; the CLI is the shell. Reference implementation for "official CLI that ships code." | ✅ | slightly complex (reference CLI, sandboxed) | [Examples](https://developers.openai.com/codex) |
| 4 | [**OpenHands**](https://github.com/OpenHands/OpenHands) | [72.6k](https://github.com/OpenHands/OpenHands/stargazers) | Dockerized software-engineering agent. The **harness** is the bash/editor/browser toolset with micro-agents and event-stream session bridging; Docker is the sandbox. Main OSS choice for teams self-hosting autonomous repo work. | ⚠️ (multi-license) | complex (Docker runtime, multi-surface agent — product suite) | [Examples](https://docs.all-hands.dev/) |
| 5 | [**Cline**](https://github.com/cline/cline) | [61.4k](https://github.com/cline/cline/stargazers) | VS Code extension whose **harness** is a plan-then-act loop with per-step human approval and cost transparency; the VS Code integration is the UI shell. Open-source counterweight to Cursor. | ✅ | slightly complex (plan-then-act, approval gates) | [Examples](https://docs.cline.bot/) |
| 6 | [**goose**](https://github.com/aaif-goose/goose) | [43.8k](https://github.com/aaif-goose/goose/stargazers) | Block-originated Rust agent, now stewarded by the Linux Foundation's Agentic AI Foundation (`aaif-goose/goose`). The **harness** is the MCP/ACP extension model with recipes and provider choice; there's no fixed UI slot—you bolt it into whatever shell you use. | ✅ | slightly complex (extensions, MCP/ACP) | [Examples](https://block.github.io/goose/docs/quickstart) |
| 7 | [**Roo Code**](https://github.com/RooCodeInc/Roo-Code) | [23.9k](https://github.com/RooCodeInc/Roo-Code/stargazers) | VS Code/Cursor extension in the Cline lineage. The **harness** is the approval-gated agent with custom modes and a strong MCP story; the IDE is the UI. Popular community fork when you want that workflow without the upstream extension. | ✅ | slightly complex (IDE extension, MCP-first) | [Examples](https://docs.roocode.com/) |
| 8 | [**crush**](https://github.com/charmbracelet/crush) | [23.9k](https://github.com/charmbracelet/crush/stargazers) | Charm's terminal coding agent (Charm's fork of the original OpenCode). The **harness** is the tool-calling loop with session persistence; the Bubble Tea TUI is the shell. | ⚠️ FSL-1.1-MIT | slightly complex (terminal agent, TUI) | [Examples](https://charm.land/blog/crush-launch/) |
| 9 | [**claw-code-agent**](https://github.com/HarnessLab/claw-code-agent) | [453](https://github.com/HarnessLab/claw-code-agent/stargazers) | Python reimplementation of the Claude Code agent architecture with zero external dependencies; interactive chat, streaming, plugin runtime, nested agent delegation, cost tracking, MCP transport—portable harness without the Rust/TS toolchain. | ❓ | slightly complex (pure Python, plugin runtime) | [Examples](https://github.com/HarnessLab/claw-code-agent#getting-started) |
| 10 | [**coderClaw**](https://github.com/SeanHogg/coderClaw) | [3](https://github.com/SeanHogg/coderClaw/stargazers) | Self-hosted multi-role coding system (Creator, Reviewer, Test, Refactor, etc.) with AST and semantic maps; IDE-agnostic, chat-channel triggers. | ❓ | slightly complex (multi-role, AST/semantic) | [Examples](https://github.com/SeanHogg/coderClaw#readme) |

## Coding harness configs and SDKs

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Skill packs, slash-command libraries, meta-prompting frameworks, and official SDKs that give you the harness (the agent loop, planning, memory, hooks) without bundling a specific IDE or CLI shell._

| # | Project | ⭐ Stars | Description | Open source | Simplicity ↔ capability | Examples |
|---|---------|---------|-------------|-------------|-------------------------|----------|
| 1 | [**superpowers**](https://github.com/obra/superpowers) | [178k](https://github.com/obra/superpowers/stargazers) | Performance-oriented harness pack for Claude Code, Codex, OpenCode, Cursor: skills, instincts, memory, security, research-first workflows. Treats harness engineering itself as the performance lever. | ✅ | complex (multi-IDE skill stack — product suite) | [Examples](https://github.com/obra/superpowers#quickstart) |
| 2 | [**everything-claude-code**](https://github.com/affaan-m/everything-claude-code) | [173k](https://github.com/affaan-m/everything-claude-code/stargazers) | The breakout 2026 harness pack for Claude Code: 28 specialized subagents, 119 reusable skills, 60 slash commands, 34 rules, 20+ automated hooks. Ships a full "AI engineering team" as config. | ✅ | complex (subagents + skills + hooks — product suite) | [Examples](https://github.com/affaan-m/everything-claude-code#quickstart) |
| 3 | [**Anthropic Skills**](https://github.com/anthropics/skills) | [128k](https://github.com/anthropics/skills/stargazers) | Anthropic's official Agent Skills repository: SKILL.md-based folders (instructions, scripts, resources) Claude dynamically loads on Claude Code, Claude.ai, and the API. The reference for progressive-disclosure skill packs in 2026. | ✅ | mostly simple (official skills format) | [Examples](https://github.com/anthropics/skills/tree/main) |
| 4 | [**GStack**](https://github.com/garrytan/gstack) | [89.2k](https://github.com/garrytan/gstack/stargazers) | Garry Tan's Claude Code skill stack: 23 slash-command modes (CEO/eng/design review, QA, ship, browse, retro, …) that structure one assistant as a virtual engineering team. Daily driver while running YC. | ✅ | slightly complex (multi-role slash-command harness) | [Examples](https://github.com/garrytan/gstack#getting-started) |
| 5 | [**get-shit-done**](https://github.com/gsd-build/get-shit-done) | [60k](https://github.com/gsd-build/get-shit-done/stargazers) | Goal-backward planning and wave-based execution over fresh context windows; avoids context rot by design. Python/JS meta-prompting for Claude Code, OpenCode, Gemini CLI. | ✅ | mostly simple (meta-prompting, you own stack) | [Examples](https://get-shit-done.dev) |
| 6 | [**SWE-agent**](https://github.com/SWE-agent/SWE-agent) | [19.1k](https://github.com/SWE-agent/SWE-agent/stargazers) | LM-driven harness built for SWE-bench: edit state, command execution, and issue-focused loop—the reference agent stack next to the benchmark itself. | ✅ | slightly complex (SWE-bench pairing, stateful edits) | [Examples](https://swe-agent.com/latest/usage/) |
| 7 | [**OpenHarness (HKUDS)**](https://github.com/HKUDS/OpenHarness) | [11.9k](https://github.com/HKUDS/OpenHarness/stargazers) | Open agent harness with a built-in personal agent ("Ohmo") that runs across Feishu, Slack, Telegram, and Discord; core tool-use, skills, memory, multi-agent coordination with auto-compaction for multi-day sessions. | ✅ | complex (personal agent + multi-channel — product suite) | [Examples](https://github.com/HKUDS/OpenHarness#getting-started) |
| 8 | [**Claude Agent SDK**](https://github.com/anthropics/claude-agent-sdk-python) | [6.7k](https://github.com/anthropics/claude-agent-sdk-python/stargazers) | Official Anthropic SDK (Python + [TypeScript](https://github.com/anthropics/claude-agent-sdk-typescript), [demos](https://github.com/anthropics/claude-agent-sdk-demos), [quickstarts](https://github.com/anthropics/claude-quickstarts)): built-in tools, MCP, long-running coding agents with session bridging. | ✅ | complex (full SDK, session bridging — product suite) | [Examples](https://github.com/anthropics/claude-agent-sdk-demos) |
| 9 | [**RepoMaster**](https://github.com/QuantaAlpha/RepoMaster) | [521](https://github.com/QuantaAlpha/RepoMaster/stargazers) | Repo-scoped research harness: builds function-call and module-dependency graphs to explore only what's needed; large relative gains on MLE-bench and GitTaskBench with lower token use. | ❓ | slightly complex (graph-based exploration) | [Examples](https://github.com/QuantaAlpha/RepoMaster#examples) |
| 10 | [**AutoHarness**](https://github.com/aiming-lab/AutoHarness) | [266](https://github.com/aiming-lab/AutoHarness/stargazers) | Lightweight governance harness: wraps any LLM client in ~2 lines for automated harness engineering—6–14 step pipeline, YAML constitution, risk-pattern matching, session persistence with cost tracking, multi-agent profiles. | ✅ | super simple (2-line wrapper, YAML gov) | [Examples](https://github.com/aiming-lab/AutoHarness#quickstart) |
| 11 | [**pmstack**](https://github.com/RyanAlberts/pmstack) | [0](https://github.com/RyanAlberts/pmstack/stargazers) | Claude Code config for AI product managers: CLAUDE.md plus skills for competitive analysis, PRD-from-signal, metric frameworks, stakeholder briefs, and agent eval design. "GStack for PMs." | ✅ | super simple (skills bundle, PM-focused) | [Examples](https://github.com/RyanAlberts/pmstack#quickstart) |

## Frameworks

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_General-purpose agent and LLM application frameworks (the app layer, not harnesses per se)._

| # | Project | ⭐ Stars | Description | Open source | Simplicity ↔ capability | Examples |
|---|---------|---------|-------------|-------------|-------------------------|----------|
| 1 | [**n8n**](https://github.com/n8n-io/n8n) | [187k](https://github.com/n8n-io/n8n/stargazers) | Fair-code workflow engine with 400+ nodes and native AI nodes; the self-hosted Zapier that actually does agents and LangChain. | ⚠️ Fair-code | complex (400+ nodes, workflow engine — product suite) | [Examples](https://docs.n8n.io/advanced-ai/examples/) |
| 2 | [**AutoGPT**](https://github.com/Significant-Gravitas/AutoGPT) | [184k](https://github.com/Significant-Gravitas/AutoGPT/stargazers) | The original autonomous loop: goal in, agent iterates with tools and memory; Forge is the dev framework, Benchmark the eval harness. | ⚠️ Polyform-SU | complex (autonomous loop, tools, memory — product suite) | [Examples](https://docs.agpt.co/) |
| 3 | [**langflow**](https://github.com/langflow-ai/langflow) | [148k](https://github.com/langflow-ai/langflow/stargazers) | Low-code UI to build and deploy LangChain/LangGraph flows; visual DAG editor and one-click run. | ✅ | complex (low-code, visual — product suite) | [Examples](https://docs.langflow.org/tutorials) |
| 4 | [**Dify**](https://github.com/langgenius/dify) | [140k](https://github.com/langgenius/dify/stargazers) | One-stop LLM app platform: visual workflows, RAG pipeline, 50+ tools, model management; "ship from prototype to prod" in a single UI. | ⚠️ Fair-code | complex (one-stop platform — product suite) | [Examples](https://docs.dify.ai/) |
| 5 | [**langchain**](https://github.com/langchain-ai/langchain) | [136k](https://github.com/langchain-ai/langchain/stargazers) | Chains, tools, retrievers, and agents; the usual entry point for "add tools to an LLM" in Python/JS. | ✅ | complex (kitchen-sink ecosystem — product suite) | [Examples](https://python.langchain.com/docs/tutorials/) |
| 6 | [**browser-use**](https://github.com/browser-use/browser-use) | [92.1k](https://github.com/browser-use/browser-use/stargazers) | Python layer over Playwright: natural-language goals become browser actions—web-agent loop without hand-rolling MCP or a custom driver for every site. | ✅ | slightly complex (LLM + browser, Playwright) | [Examples](https://docs.browser-use.com/examples/) |
| 7 | [**Flowise**](https://github.com/FlowiseAI/Flowise) | [52.5k](https://github.com/FlowiseAI/Flowise/stargazers) | Drag-and-drop LangChain UI; deploy flows without code. The low-code sibling to Langflow, with a different component and hosting story. | ⚠️ Apache+CLA | complex (low-code, drag-drop — product suite) | [Examples](https://docs.flowiseai.com/) |
| 8 | [**llama-index**](https://github.com/run-llama/llama_index) | [49.1k](https://github.com/run-llama/llama_index/stargazers) | Data-centric: indexing, RAG, and query engines; agent abstractions sit on top of your data pipelines. | ✅ | complex (RAG + agents — product suite) | [Examples](https://docs.llamaindex.ai/en/stable/examples/) |
| 9 | [**agno**](https://github.com/agno-agi/agno) | [39.9k](https://github.com/agno-agi/agno/stargazers) | Python agents with memory, knowledge bases, tools, and structured outputs; continues the PhiData-era product line under the Agno name—production apps, evals, and pipelines. | ✅ | complex (memory, KB, observability — product suite) | [Examples](https://docs.agno.com/examples/introduction) |
| 10 | [**langgraph**](https://github.com/langchain-ai/langgraph) | [31.2k](https://github.com/langchain-ai/langgraph/stargazers) | State-machine graphs over LLM steps; checkpointing, human-in-the-loop, and durable execution so workflows survive restarts. | ✅ | slightly complex (graphs, checkpointing, durable exec) | [Examples](https://langchain-ai.github.io/langgraph/tutorials/) |
| 11 | [**semantic-kernel**](https://github.com/microsoft/semantic-kernel) | [27.8k](https://github.com/microsoft/semantic-kernel/stargazers) | Microsoft's plugin and planner layer for LLMs; C#, Python, Java; strong on enterprise auth and orchestration. | ✅ | complex (enterprise, multi-language — product suite) | [Examples](https://github.com/microsoft/semantic-kernel/tree/main/python/samples) |
| 12 | [**mastra**](https://github.com/mastra-ai/mastra) | [23.6k](https://github.com/mastra-ai/mastra/stargazers) | TypeScript-first; agents, tools, and workflows with a single runtime and minimal boilerplate. | ⚠️ Elastic-2.0 | slightly complex (TS-first, minimal boilerplate) | [Examples](https://mastra.ai/examples) |
| 13 | [**letta**](https://github.com/letta-ai/letta) | [22.4k](https://github.com/letta-ai/letta/stargazers) | Python agent runtime with tool use and control flow; lean API; stateful agents with long-horizon memory. | ✅ | mostly simple (lean API) | [Examples](https://docs.letta.com/quickstart) |
| 14 | [**rasa**](https://github.com/RasaHQ/rasa) | [21.1k](https://github.com/RasaHQ/rasa/stargazers) | Conversational AI stack (NLU, dialogue, actions); long-standing OSS choice for chat and voice bots. | ✅ | complex (full stack — product suite) | [Examples](https://rasa.com/docs/learn/concepts/) |
| 15 | [**Google ADK**](https://github.com/google/adk-python) | [19.4k](https://github.com/google/adk-python/stargazers) | Google's official Agent Development Kit: code-first Python toolkit for building, evaluating, and deploying agents. Optimized for Gemini but model-agnostic; deploys to Cloud Run / Vertex AI; ships a dev UI with eval and a code-execution sandbox. | ✅ | complex (official Google SDK, eval, deploy — product suite) | [Examples](https://google.github.io/adk-docs/) |
| 16 | [**botpress**](https://github.com/botpress/botpress) | [14.7k](https://github.com/botpress/botpress/stargazers) | Visual bot builder and runtime; multi-channel, open-source alternative to commercial bot platforms. | ✅ | complex (visual builder, multi-channel — product suite) | [Examples](https://botpress.com/docs) |
| 17 | [**R2R**](https://github.com/SciPhi-AI/R2R) | [7.8k](https://github.com/SciPhi-AI/R2R/stargazers) | RAG-first: hybrid search, knowledge graphs, multimodal; the framework for "production RAG" when you care more about retrieval than chat UI. | ✅ | complex (production RAG — product suite) | [Examples](https://r2r-docs.sciphi.ai/) |
| 18 | [**agent-squad**](https://github.com/2FastLabs/agent-squad) | [7.6k](https://github.com/2FastLabs/agent-squad/stargazers) | AWS-originated orchestrator (now under 2FastLabs): intent classification, streaming, SupervisorAgent; "agent-as-tools" so one agent delegates to a squad. | ✅ | slightly complex (squad orchestration) | [Examples](https://2fastlabs.github.io/agent-squad/) |
| 19 | [**AgentVerse**](https://github.com/OpenBMB/AgentVerse) | [5k](https://github.com/OpenBMB/AgentVerse/stargazers) | Task-solving and simulation envs for multi-LLM agents; deploy many agents in custom environments without building infra from scratch. | ✅ | complex (simulation envs, multi-agent — product suite) | [Examples](https://github.com/OpenBMB/AgentVerse#examples) |
| 20 | [**Bee Agent Framework**](https://github.com/i-am-bee/beeai-framework) | [3.2k](https://github.com/i-am-bee/beeai-framework/stargazers) | Python + TypeScript, LF AI–backed; MCP/ACP, workflows, Requirement Agent; the one that pushes "production multi-agent" without LangChain. | ✅ | complex (production multi-agent — product suite) | [Examples](https://framework.beeai.dev/) |
| 21 | [**AgentStack**](https://github.com/agentstack-ai/AgentStack) | [2.1k](https://github.com/agentstack-ai/AgentStack/stargazers) | Scaffolds full agent projects; plugs in CrewAI, LangGraph, OpenAI Swarm, LlamaStack and wires AgentOps observability from day one. | ✅ | slightly complex (scaffold, multi-backend) | [Examples](https://docs.agentstack.sh/) |
| 22 | [**AIlice**](https://github.com/myshell-ai/AIlice) | [1.4k](https://github.com/myshell-ai/AIlice/stargazers) | Fully autonomous general-purpose agent; one binary, Docker-ready, for when you want "set goal and walk away" without a framework. | ✅ | slightly complex (autonomous, one binary) | [Examples](https://github.com/myshell-ai/AIlice#examples) |
| 23 | [**AgentSilex**](https://github.com/howl-anderson/agentsilex) | [450](https://github.com/howl-anderson/agentsilex/stargazers) | ~300 lines of readable agent code on top of LiteLLM; the "I want to see the whole loop" option for learning or minimal production. | ✅ | super simple (~300 LOC) | [Examples](https://github.com/howl-anderson/agentsilex#examples) |
| 24 | [**SuperAgentX**](https://github.com/superagentxai/superagentx) | [191](https://github.com/superagentxai/superagentx/stargazers) | Lightweight multi-agent orchestrator with an AGI-angle; minimal surface, docs-first, for teams that want orchestration without the kitchen sink. | ✅ | mostly simple (minimal surface) | [Examples](https://docs.superagentx.ai/) |

## Multi-agent and orchestration

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Harnesses and patterns for multi-agent coordination and handoffs._

| # | Project | ⭐ Stars | Description | Open source | Simplicity ↔ capability | Examples |
|---|---------|---------|-------------|-------------|-------------------------|----------|
| 1 | [**autogen**](https://github.com/microsoft/autogen) | [57.7k](https://github.com/microsoft/autogen/stargazers) | Conversable agents and group chats; code execution and human-in-the-loop; Microsoft origin, AG2 ecosystem. | ✅ CC-BY | complex (group chat, code exec, AG2 — product suite) | [Examples](https://microsoft.github.io/autogen/dev/user-guide/) |
| 2 | [**crewAI**](https://github.com/crewAIInc/crewAI) | [50.6k](https://github.com/crewAIInc/crewAI/stargazers) | Role-based agents (roles, goals, backstories) in Crews; Flows add event-driven and hierarchical control for production. | ✅ | complex (roles, Flows, production — product suite) | [Examples](https://github.com/crewAIInc/crewAI-examples) |
| 3 | [**openai-agents-python**](https://github.com/openai/openai-agents-python) | [25.9k](https://github.com/openai/openai-agents-python/stargazers) | Handoffs, guardrails, and multi-LLM routing; minimal surface so you own the loop. | ✅ | mostly simple (minimal surface) | [Examples](https://github.com/openai/openai-agents-python/tree/main/examples) |
| 4 | [**PraisonAI**](https://github.com/MervinPraison/PraisonAI) | [7k](https://github.com/MervinPraison/PraisonAI/stargazers) | Autonomous multi-agent teams with a single entry point; emphasis on minimal config. | ✅ | mostly simple (single entry, minimal config) | [Examples](https://docs.praison.ai/cookbooks) |
| 5 | [**AgentRL**](https://github.com/THUDM/AgentRL) | [281](https://github.com/THUDM/AgentRL/stargazers) | Multitask, multiturn RL for LLM agents; Ray-based scaling, rollout/actor workers—for teams that want to train agents, not just run them. | ✅ | complex (RL, Ray, train agents — product suite) | [Examples](https://github.com/THUDM/AgentRL#quick-start) |

## Plugins, MCPs, CLI tools

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_IDE plugins, concrete MCP servers, and CLI tools that give agents tools and context._

| # | Project | ⭐ Stars | Description | Open source | Simplicity ↔ capability | Examples |
|---|---------|---------|-------------|-------------|-------------------------|----------|
| 1 | [**claude-mem**](https://github.com/thedotmack/claude-mem) | [72k](https://github.com/thedotmack/claude-mem/stargazers) | Claude Code plugin that captures everything an agent does during a session, AI-compresses it (via claude-agent-sdk), and injects the relevant context into future sessions—session-to-session memory as a drop-in. | ✅ | slightly complex (session capture + compression) | [Examples](https://github.com/thedotmack/claude-mem#quickstart) |
| 2 | [**aider**](https://github.com/Aider-AI/aider) | [44.3k](https://github.com/Aider-AI/aider/stargazers) | Git-aware CLI pair programmer; edits in-repo, supports multiple models and MCP so agents see version control and tools. | ✅ | slightly complex (CLI, git-aware, MCP) | [Examples](https://aider.chat/docs/) |
| 3 | [**continue**](https://github.com/continuedev/continue) | [33k](https://github.com/continuedev/continue/stargazers) | Open-source IDE extension (VS Code, JetBrains); in-editor completion and chat with local or API models. | ✅ | complex (IDE extension, multi-editor — product suite) | [Examples](https://docs.continue.dev/) |
| 4 | [**github-mcp-server**](https://github.com/github/github-mcp-server) | [29.5k](https://github.com/github/github-mcp-server/stargazers) | GitHub's official MCP server (Go): repos, issues, PRs, code search, Actions. Replaces the older community `cyanheads/github-mcp-server` as the canonical way to give agents GitHub access. | ✅ | slightly complex (official GitHub MCP) | [Examples](https://github.com/github/github-mcp-server#tools) |
| 5 | [**MCP Python SDK**](https://github.com/modelcontextprotocol/python-sdk) | [22.9k](https://github.com/modelcontextprotocol/python-sdk/stargazers) | Official SDK to build and consume MCP servers/clients in Python; stdio and SSE transports. | ✅ | mostly simple (SDK only) | [Examples](https://github.com/modelcontextprotocol/python-sdk/tree/main/examples) |
| 6 | [**MCP TypeScript SDK**](https://github.com/modelcontextprotocol/typescript-sdk) | [12.3k](https://github.com/modelcontextprotocol/typescript-sdk/stargazers) | Official MCP implementation for Node/TS; reference for the protocol. | ✅ | mostly simple (protocol reference) | [Examples](https://github.com/modelcontextprotocol/typescript-sdk/tree/main/examples) |
| 7 | [**MCP Inspector**](https://github.com/modelcontextprotocol/inspector) | [9.7k](https://github.com/modelcontextprotocol/inspector/stargazers) | GUI to test and debug MCP servers; inspect tools, resources, and prompts. | ✅ | super simple (debug GUI) | [Examples](https://github.com/modelcontextprotocol/inspector#readme) |
| 8 | [**MCP Registry**](https://github.com/modelcontextprotocol/registry) | [6.8k](https://github.com/modelcontextprotocol/registry/stargazers) | Official, community-driven registry for MCP servers—the "app store" MCP clients use to discover servers. Maintained by Anthropic + ecosystem maintainers; v0.1 API frozen, production-grade. | ✅ | slightly complex (official discovery layer) | [Examples](https://registry.modelcontextprotocol.io) |
| 9 | [**Docker MCP Gateway**](https://github.com/docker/mcp-gateway) | [1.4k](https://github.com/docker/mcp-gateway/stargazers) | Docker's official MCP CLI plugin / gateway; container-aware MCP tooling from Docker (replaces deprecated `docker/mcp-servers` path). | ✅ | slightly complex (Docker-aware MCPs) | [Examples](https://docs.docker.com/ai/mcp-gateway/) |
| 10 | [**puppeteer-real-browser-mcp**](https://github.com/withLinda/puppeteer-real-browser-mcp-server) | [21](https://github.com/withLinda/puppeteer-real-browser-mcp-server/stargazers) | Puppeteer MCP with real-browser and anti-detection; for agents that need to drive sites that block headless. | ❓ | mostly simple (real browser, anti-detect) | [Examples](https://github.com/withLinda/puppeteer-real-browser-mcp-server#readme) |
| 11 | [**Better-OpenCodeMCP**](https://github.com/ajhcs/Better-OpenCodeMCP) | [6](https://github.com/ajhcs/Better-OpenCodeMCP/stargazers) | MCP server for OpenCode/Crush: async task execution, model bridging (e.g. Claude→Gemini), process pooling. | ✅ | mostly simple (MCP server, model bridging) | [Examples](https://github.com/ajhcs/Better-OpenCodeMCP#readme) |
| 12 | [**agentlog**](https://github.com/RyanAlberts/agentlog) | [0](https://github.com/RyanAlberts/agentlog/stargazers) | Persistent decision memory for any project: `remember`, `recall`, `reflect`. Single-file Python CLI that stores decisions as JSONL and uses Claude or Gemini to retrieve and synthesize patterns—Karpathy's LLM Wiki concept as a CLI. | ✅ | super simple (one file, three commands) | [Examples](https://github.com/RyanAlberts/agentlog#quickstart) |

## Evaluation and benchmarking harnesses

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Agentic eval systems, reasoning benchmarks, and open agent benchmarks._

| # | Project | ⭐ Stars | Description | Open source | Simplicity ↔ capability | Examples |
|---|---------|---------|-------------|-------------|-------------------------|----------|
| 1 | [**Agent Lightning**](https://github.com/microsoft/agent-lightning) | [17.1k](https://github.com/microsoft/agent-lightning/stargazers) | Microsoft's training-oriented harness: optimization loops for agent behavior—when you need to improve policies over rollouts, not only score a fixed prompt. | ✅ | complex (agent training, Microsoft stack — product suite) | [Examples](https://github.com/microsoft/agent-lightning/tree/main/examples) |
| 2 | [**SWE-bench**](https://github.com/SWE-bench/SWE-bench) | [4.8k](https://github.com/SWE-bench/SWE-bench/stargazers) | LMs resolve real GitHub issues; Docker harness, instance IDs; standard for code-agent evals. | ✅ | slightly complex (real GitHub issues, standard) | [Examples](https://www.swebench.com/) |
| 3 | [**AgentBench**](https://github.com/THUDM/AgentBench) | [3.4k](https://github.com/THUDM/AgentBench/stargazers) | ICLR'24 benchmark: agents across AlfWorld, DB, knowledge graphs, OS, webshop; Docker Compose, function-calling interface. | ✅ | complex (multi-env, Docker Compose — product suite) | [Examples](https://github.com/THUDM/AgentBench#leaderboard) |
| 4 | [**inspect_ai**](https://github.com/UKGovernmentBEIS/inspect_ai) | [2k](https://github.com/UKGovernmentBEIS/inspect_ai/stargazers) | Inspect AI core: composable eval tasks, sandboxes, scorers, and multi-model runs; the framework behind inspect_evals, not just the task bundle. | ✅ | complex (eval framework, AISI stack — product suite) | [Examples](https://inspect.aisi.org.uk/) |
| 5 | [**WebArena**](https://github.com/web-arena-x/webarena) | [1.5k](https://github.com/web-arena-x/webarena/stargazers) | Realistic web env (e.g. e‑commerce, CMS, dev tools); 812 tasks; measures end-to-end web agent success. | ✅ | complex (812 tasks, web env — product suite) | [Examples](https://webarena.dev/) |
| 6 | [**WebVoyager**](https://github.com/MinorJerry/WebVoyager) | [1.1k](https://github.com/MinorJerry/WebVoyager/stargazers) | End-to-end web agent with LMMs: screenshots + actions on real sites; benchmark on 15 sites, GPT-4V for automatic eval. | ✅ | slightly complex (LMMs, screenshots, 15 sites) | [Examples](https://github.com/MinorJerry/WebVoyager#quick-start) |
| 7 | [**ARC-AGI-2**](https://github.com/arcprize/ARC-AGI-2) | [697](https://github.com/arcprize/ARC-AGI-2/stargazers) | ARC Prize task set: grid-based abstraction/reasoning; public and private splits for generalization. | ✅ | super simple (task set) | [Examples](https://arcprize.org/) |
| 8 | [**SWE-Gym**](https://github.com/SWE-Gym/SWE-Gym) | [672](https://github.com/SWE-Gym/SWE-Gym/stargazers) | Training and evaluation for SWE agents and verifiers (ICML 2025). | ✅ | slightly complex (training + eval, ICML) | [Examples](https://github.com/SWE-Gym/SWE-Gym#quick-start) |
| 9 | [**swe-smith**](https://github.com/SWE-bench/SWE-smith) | [640](https://github.com/SWE-bench/SWE-smith/stargazers) | Data generation for SWE agents; 50k+ instances across 128 repos; used for SWE-agent-LM training. | ✅ | slightly complex (50k+ instances, data gen) | [Examples](https://swesmith.com/) |
| 10 | [**inspect_evals**](https://github.com/UKGovernmentBEIS/inspect_evals) | [479](https://github.com/UKGovernmentBEIS/inspect_evals/stargazers) | UK AISI/Arcadia/Vector: GAIA and other evals in Inspect AI; level 1–3, sandboxed, tool-calling solvers. | ✅ | slightly complex (Inspect AI, UK gov) | [Examples](https://ukgovernmentbeis.github.io/inspect_evals/) |
| 11 | [**arc-agi-benchmarking**](https://github.com/arcprize/arc-agi-benchmarking) | [348](https://github.com/arcprize/arc-agi-benchmarking/stargazers) | Runner for ARC-AGI: multi-provider (OpenAI, Anthropic, Gemini, etc.), rate limits, retries, and scoring. | ✅ | mostly simple (runner, multi-provider) | [Examples](https://github.com/arcprize/arc-agi-benchmarking#getting-started) |
| 12 | [**VitaBench**](https://github.com/meituan-longcat/vitabench) | [124](https://github.com/meituan-longcat/vitabench/stargazers) | ICLR'26: 66 tools, real-world apps (delivery, travel, retail); 100 cross-scenario + 300 single-scenario tasks; adopted by Qwen/Seed. | ✅ | complex (66 tools, cross-scenario — product suite) | [Examples](https://github.com/meituan-longcat/vitabench#tasks) |
| 13 | [**AgencyBench**](https://github.com/GAIR-NLP/AgencyBench) | [80](https://github.com/GAIR-NLP/AgencyBench/stargazers) | Long-horizon agent benchmark: 32 scenarios, 138 tasks, ~1M tokens and ~90 tool calls; Docker sandbox and rubric-based + LLM judges. | ✅ | complex (32 scenarios, Docker, judges — product suite) | [Examples](https://github.com/GAIR-NLP/AgencyBench#leaderboard) |
| 14 | [**letta-evals**](https://github.com/letta-ai/letta-evals) | [70](https://github.com/letta-ai/letta-evals/stargazers) | Eval harness for stateful Letta agents; configurable suites and grading (LLM or rule-based) so you can measure what you ship. | ✅ | mostly simple (Letta-specific harness) | [Examples](https://docs.letta.com/api-reference/evaluations) |
| 15 | [**SUPER**](https://github.com/allenai/super-benchmark) | [51](https://github.com/allenai/super-benchmark/stargazers) | Agents that set up and run ML/NLP from GitHub repos; 45 expert problems, 152 masked tasks, 602 AutoGen tasks; Docker-based. | ✅ | slightly complex (ML/NLP repos, Docker) | [Examples](https://huggingface.co/datasets/allenai/super) |
| 16 | [**TRAIL**](https://github.com/patronus-ai/trail-benchmark) | [18](https://github.com/patronus-ai/trail-benchmark/stargazers) | Trace reasoning and agentic issue localization; 148 long-context traces, 841 errors, 20+ error types; Hugging Face dataset. | ✅ | mostly simple (traces, Hugging Face) | [Examples](https://huggingface.co/datasets/PatronusAI/TRAIL) |

## Research and task-specific harnesses

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Deep research, document QA, and domain-specific agent loops._

| # | Project | ⭐ Stars | Description | Open source | Simplicity ↔ capability | Examples |
|---|---------|---------|-------------|-------------|-------------------------|----------|
| 1 | [**gpt-researcher**](https://github.com/assafelovic/gpt-researcher) | [26.9k](https://github.com/assafelovic/gpt-researcher/stargazers) | Autonomous deep-research agent: web + local sources, citation-grounded reports, multi-agent and deep-research modes. The reference open-source research harness. | ✅ | complex (deep research, multi-agent — product suite) | [Examples](https://docs.gptr.dev/) |
| 2 | [**openagents**](https://github.com/OpenAgentsInc/openagents) | [414](https://github.com/OpenAgentsInc/openagents/stargazers) | Platform for autonomous agents and autopilot-style workflows; decentralized/Nostr-oriented (Pylon runtime, actively shipped in 2026). | ✅ | complex (platform, decentralized — product suite) | [Examples](https://openagents.com/) |

## Libraries and SDKs

<a href="#contents"><img align="right" width="15" height="15" src="https://git.io/JtehR" alt="Back to top"></a>

_Lightweight runtimes, tool loops, and provider-agnostic harness primitives._

| # | Project | ⭐ Stars | Description | Open source | Simplicity ↔ capability | Examples |
|---|---------|---------|-------------|-------------|-------------------------|----------|
| 1 | [**Daytona**](https://github.com/daytonaio/daytona) | [72.4k](https://github.com/daytonaio/daytona/stargazers) | Elastic dev environments for AI-generated code: workspaces, Git, previews—infra harness between "the model wrote a patch" and "it ran in a real machine." | ✅ | slightly complex (dev env API, isolation) | [Examples](https://www.daytona.io/docs/) |
| 2 | [**Mem0**](https://github.com/mem0ai/mem0) | [54.8k](https://github.com/mem0ai/mem0/stargazers) | Universal memory layer for AI agents: stores user/org/session memory, retrieves on demand. Apache-2.0; the de-facto memory primitive paired with most harnesses in 2026. | ✅ | slightly complex (memory layer, multi-platform) | [Examples](https://docs.mem0.ai/examples/overview) |
| 3 | [**LiteLLM**](https://github.com/BerriAI/litellm) | [45.7k](https://github.com/BerriAI/litellm/stargazers) | One interface to 100+ LLMs; routing, caching, budgets. Not an agent framework—the pipe every agent framework uses. | ✅ | mostly simple (LLM pipe only) | [Examples](https://docs.litellm.ai/docs/) |
| 4 | [**Composio**](https://github.com/ComposioHQ/composio) | [28.1k](https://github.com/ComposioHQ/composio/stargazers) | 1,000+ toolkits with auth, tool search, and a sandboxed workbench—drop-in tool layer so agents stop reinventing OAuth + integrations. Python and TypeScript. | ✅ | complex (1k+ tools, auth, search — product suite) | [Examples](https://docs.composio.dev/) |
| 5 | [**smolagents**](https://github.com/huggingface/smolagents) | [27.1k](https://github.com/huggingface/smolagents/stargazers) | Code-as-action agents: model outputs Python executed in sandbox (E2B, Modal, etc.); ~1k LOC core. | ✅ | mostly simple (code-as-action, ~1k LOC) | [Examples](https://huggingface.co/docs/smolagents/examples) |
| 6 | [**vercel/ai**](https://github.com/vercel/ai) | [24k](https://github.com/vercel/ai/stargazers) | React and Node SDK for streaming, tool calls, and agent-style UIs; provider-agnostic. | ✅ | slightly complex (React/Node SDK, provider-agnostic) | [Examples](https://ai-sdk.dev/examples) |
| 7 | [**deepagents**](https://github.com/langchain-ai/deepagents) | [22.2k](https://github.com/langchain-ai/deepagents/stargazers) | LangChain's Python+TypeScript agent harness on top of LangGraph: planning tool, virtual filesystem, shell sandbox, sub-agent spawning—the "Claude Code-style" harness as a reusable library. | ✅ | slightly complex (planning, files, sub-agents) | [Examples](https://docs.langchain.com/labs/deep-agents/overview) |
| 8 | [**pydantic-ai**](https://github.com/pydantic/pydantic-ai) | [16.8k](https://github.com/pydantic/pydantic-ai/stargazers) | Type-safe Python agents with Pydantic I/O; multi-provider, MCP, Logfire observability, and human-in-the-loop. | ✅ | slightly complex (type-safe, MCP, Logfire) | [Examples](https://ai.pydantic.dev/examples/) |
| 9 | [**E2B**](https://github.com/e2b-dev/E2B) | [12k](https://github.com/e2b-dev/E2B/stargazers) | Firecracker sandboxes for executing agent-generated code; the hosted isolation layer many tool-calling demos use instead of running arbitrary LLM output on your laptop. | ✅ | slightly complex (sandbox API, code execution) | [Examples](https://e2b.dev/docs) |
| 10 | [**strands-agents**](https://github.com/strands-agents/sdk-python) | [5.8k](https://github.com/strands-agents/sdk-python/stargazers) | Model-driven Python SDK; decorators for tools, native MCP, multi-agent; "minimal code" without sacrificing provider choice. | ✅ | mostly simple (decorators, MCP, minimal code) | [Examples](https://strandsagents.com/latest/documentation/docs/examples/) |
| 11 | [**Cloudflare Agents**](https://github.com/cloudflare/agents) | [4.9k](https://github.com/cloudflare/agents/stargazers) | Persistent, stateful agents on Durable Objects: state, websockets, scheduling, and AI chat baked in. The serverless answer to "where does the agent live?" | ✅ | slightly complex (Durable Objects, stateful) | [Examples](https://developers.cloudflare.com/agents/getting-started/) |
| 12 | [**openai-agents-js**](https://github.com/openai/openai-agents-js) | [2.9k](https://github.com/openai/openai-agents-js/stargazers) | Official OpenAI Agents SDK for Node/TS: handoffs, guardrails, voice; the JS counterpart to openai-agents-python. | ✅ | slightly complex (handoffs, guardrails, voice) | [Examples](https://github.com/openai/openai-agents-js/tree/main/examples) |
| 13 | [**open-harness**](https://github.com/MaxGfeller/open-harness) | [498](https://github.com/MaxGfeller/open-harness/stargazers) | TypeScript Agent class on Vercel AI SDK; streaming events, filesystem/bash tools, MCP, and subagent delegation. | ✅ | slightly complex (streaming, tools, subagents) | [Examples](https://github.com/MaxGfeller/open-harness#examples) |
| 14 | [**Community-curated agent lists**](https://github.com/brandonhimpfen/awesome-ai-agents) | [10](https://github.com/brandonhimpfen/awesome-ai-agents/stargazers) | Broader directories: e.g. [brandonhimpfen/awesome-ai-agents](https://github.com/brandonhimpfen/awesome-ai-agents), [axioma-ai-labs/awesome-ai-agent-frameworks](https://github.com/axioma-ai-labs/awesome-ai-agent-frameworks), [mb-mal/awesome-ai-agents-frameworks](https://github.com/mb-mal/awesome-ai-agents-frameworks)—differ by scope and update cadence. | ❓ | super simple (curated lists) | [Examples](https://github.com/brandonhimpfen/awesome-ai-agents#readme) |

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
