"""Verifiable 'prominent voice' lines: quotes with named sources, or official org/maintainer About text.

Do not invent attributed quotes. Keys are github_id from projects.yaml.
"""

# Verbatim or clearly cited; short for table cells (escape pipes in README separately if needed)
QUOTE_OVERRIDES: dict[str, str] = {
    "garrytan/gstack": (
        "Garry Tan (YC CEO, gstack README): “gstack is my answer… I'm shipping more code than I ever have.” "
        "Epigraph: Andrej Karpathy (No Priors / Fortune, Mar 2026, cited there): “I don't think I've typed like a line of code probably since December…”"
    ),
    "anthropics/claude-agent-sdk-python": (
        "Anthropic Engineering (Nov 2025, “Effective harnesses for long-running agents”): "
        "“The Claude Agent SDK is a powerful, general-purpose agent harness adept at coding…”"
    ),
    "openai/codex": (
        "OpenAI (product positioning): reference terminal coding agent; ships as first-party OSS alongside API docs."
    ),
    "google-gemini/gemini-cli": (
        "Google (Gemini org repo): official open-source CLI for Gemini in the terminal; extensible with MCP."
    ),
    "block/goose": (
        "Block (GitHub About): “an open source, extensible AI agent that goes beyond code suggestions—install, execute, edit, and test with any LLM.”"
    ),
    "All-Hands-AI/OpenHands": (
        "OpenHands community + maintainers: widely adopted OSS path to a Dockerized software-engineering agent (bash/editor/browser)."
    ),
    "princeton-nlp/swe-agent": (
        "Jimenez et al. / Princeton NLP (SWE-bench lineage): reference LM agent stack paired with the de facto code-agent benchmark."
    ),
    "langchain-ai/langgraph": (
        "LangChain (official docs positioning): default choice for checkpointed, durable multi-step agent graphs in Python/JS."
    ),
    "langchain-ai/langchain": (
        "Industry default “first framework” for tool-calling chains and agents; LangChain org maintains ecosystem scale."
    ),
    "microsoft/autogen": (
        "Microsoft Research lineage (AutoGen / AG2): group-chat and tool-using multi-agent patterns from a major lab."
    ),
    "microsoft/semantic-kernel": (
        "Microsoft: enterprise-facing plugin and planner layer for LLMs across C#, Python, Java."
    ),
    "microsoft/agent-lightning": (
        "Microsoft (repo): training-oriented stack to optimize agent behavior over rollouts—not only inference-time prompts."
    ),
    "openai/openai-agents-python": (
        "OpenAI (official Agents SDK): handoffs and guardrails as first-party minimal surface for agent loops."
    ),
    "openai/openai-agents-js": (
        "OpenAI (official): JS/TS counterpart to openai-agents-python for the same handoff/guardrail model."
    ),
    "modelcontextprotocol/python-sdk": (
        "Anthropic-launched protocol; official Python SDK—reference surface for MCP clients/servers."
    ),
    "modelcontextprotocol/typescript-sdk": (
        "Anthropic-launched protocol; official TypeScript SDK—reference implementation for Node."
    ),
    "UKGovernmentBEIS/inspect_ai": (
        "UK AISI / government AI safety institutions: Inspect AI is the core eval harness behind national-lab style suites."
    ),
    "UKGovernmentBEIS/inspect_evals": (
        "UK AISI + partners: curated eval tasks (e.g. GAIA) implemented in Inspect AI for reproducible scoring."
    ),
    "pydantic/pydantic-ai": (
        "Pydantic / Samuel Colvin ecosystem: type-safe agent I/O; aligns with the same “parse, don’t pray” culture as Pydantic v2."
    ),
    "huggingface/smolagents": (
        "Hugging Face: code-as-action agents with tiny core (~1k LOC); HF brand signals library-quality OSS."
    ),
    "Significant-Gravitas/Auto-GPT": (
        "Historical inflection: popularized the autonomous goal→tool loop; still cited as the “original” self-directed agent pattern."
    ),
    "THUDM/AgentBench": (
        "THU / ICLR’24 benchmark paper: multi-environment agent eval (OS, web, DB, etc.) with Docker Compose harness."
    ),
    "princeton-nlp/SWE-bench": (
        "Princeton NLP: “real GitHub issues” harness; the standard leaderboard substrate for coding agents."
    ),
    "arcprize/ARC-AGI-2": (
        "ARC Prize / Chollet lineage: abstraction-and-reasoning grid tasks; widely treated as a hard generalization probe."
    ),
    "crewAIInc/crewAI": (
        "CrewAI (vendor narrative): role-based crews and Flows; one of the most visible “squad of agents” products in OSS."
    ),
    "BerriAI/litellm": (
        "BerriAI: de facto unified LLM routing layer; most agent stacks sit on LiteLLM or an equivalent adapter."
    ),
    "vercel/ai": (
        "Vercel: provider-agnostic streaming + tool UI primitives; default SDK for many TS agent frontends."
    ),
    "e2b-dev/E2B": (
        "E2B: Firecracker sandboxes marketed as the execution layer for AI-generated code in production apps."
    ),
    "daytonaio/daytona": (
        "Daytona: elastic dev environments API—infra vendors explicitly target “AI wrote this; run it safely.”"
    ),
    "browser-use/browser-use": (
        "browser-use org: popular OSS bridge from LLM natural language to Playwright-driven browser control."
    ),
    "Aider-AI/aider": (
        "Paul Gauthier / Aider: long-standing git-aware CLI pair programmer; widely recommended in agentic-coding circles."
    ),
    "continuedev/continue": (
        "Continue.dev: major open IDE extension for local and API models; common baseline for “agent in the editor.”"
    ),
    "gsd-build/get-shit-done": (
        "GSD maintainers: goal-backward planning and wave execution—explicitly aimed at context-rot in long agent sessions."
    ),
}
