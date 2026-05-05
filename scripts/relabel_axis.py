#!/usr/bin/env python3
"""One-shot helper: rewrite the axis values in scripts/generate.py to the new
4-tier scale (super simple / mostly simple / slightly complex / complex
(product suite)). Run once, inspect the diff, then delete this file.

Uses ast to locate axis literals so we're not at the mercy of regex against
descriptions that contain inline markdown, escaped quotes, etc.
"""
from __future__ import annotations
import ast
from pathlib import Path

# Editorial mapping: github_id -> new axis string. Every Project() entry in
# scripts/generate.py must be covered.
NEW_AXIS: dict[str, str] = {
    # progressive-disclosure
    "agentsmd/agents.md": "super simple (format only)",
    "PatrickJS/awesome-cursorrules": "super simple (content bundle)",
    "xfey/MCP-Zero": "complex (3k tools, full routing)",
    "langchain-ai/langgraph-bigtool": "slightly complex (large tool sets)",
    "spring-ai-community/spring-ai-tool-search-tool": "mostly simple (search-then-load)",
    "Reason-Wang/ToolGen": "complex (47k+ tools)",
    "antl3x/ToolRAG": "mostly simple (query-driven retrieval)",
    # coding-agent-products
    "cline/cline": "slightly complex (plan-then-act, approval gates)",
    "RooCodeInc/Roo-Code": "slightly complex (IDE extension, MCP-first)",
    "openai/codex": "slightly complex (reference CLI, sandboxed)",
    "google-gemini/gemini-cli": "slightly complex (official CLI, plugins, MCP)",
    "charmbracelet/crush": "slightly complex (terminal agent, TUI)",
    "anomalyco/opencode": "slightly complex (multi-provider, plugins, MCP)",
    "OpenHands/OpenHands": "complex (Docker runtime, multi-surface agent — product suite)",
    "aaif-goose/goose": "slightly complex (extensions, MCP/ACP)",
    "HarnessLab/claw-code-agent": "slightly complex (pure Python, plugin runtime)",
    "SeanHogg/coderClaw": "slightly complex (multi-role, AST/semantic)",
    # coding-harness-configs
    "gsd-build/get-shit-done": "mostly simple (meta-prompting, you own stack)",
    "garrytan/gstack": "slightly complex (multi-role slash-command harness)",
    "affaan-m/everything-claude-code": "complex (subagents + skills + hooks — product suite)",
    "obra/superpowers": "complex (multi-IDE skill stack — product suite)",
    "RyanAlberts/pmstack": "super simple (skills bundle, PM-focused)",
    "anthropics/claude-agent-sdk-python": "complex (full SDK, session bridging — product suite)",
    "aiming-lab/AutoHarness": "super simple (2-line wrapper, YAML gov)",
    "QuantaAlpha/RepoMaster": "slightly complex (graph-based exploration)",
    "SWE-agent/SWE-agent": "slightly complex (SWE-bench pairing, stateful edits)",
    "HKUDS/OpenHarness": "complex (personal agent + multi-channel — product suite)",
    "anthropics/skills": "mostly simple (official skills format)",
    # frameworks
    "langchain-ai/langgraph": "slightly complex (graphs, checkpointing, durable exec)",
    "langchain-ai/langchain": "complex (kitchen-sink ecosystem — product suite)",
    "run-llama/llama_index": "complex (RAG + agents — product suite)",
    "microsoft/semantic-kernel": "complex (enterprise, multi-language — product suite)",
    "mastra-ai/mastra": "slightly complex (TS-first, minimal boilerplate)",
    "agno-agi/agno": "complex (memory, KB, observability — product suite)",
    "letta-ai/letta": "mostly simple (lean API)",
    "langflow-ai/langflow": "complex (low-code, visual — product suite)",
    "RasaHQ/rasa": "complex (full stack — product suite)",
    "botpress/botpress": "complex (visual builder, multi-channel — product suite)",
    "langgenius/dify": "complex (one-stop platform — product suite)",
    "n8n-io/n8n": "complex (400+ nodes, workflow engine — product suite)",
    "Significant-Gravitas/AutoGPT": "complex (autonomous loop, tools, memory — product suite)",
    "myshell-ai/AIlice": "slightly complex (autonomous, one binary)",
    "i-am-bee/beeai-framework": "complex (production multi-agent — product suite)",
    "2FastLabs/agent-squad": "slightly complex (squad orchestration)",
    "superagentxai/superagentx": "mostly simple (minimal surface)",
    "OpenBMB/AgentVerse": "complex (simulation envs, multi-agent — product suite)",
    "SciPhi-AI/R2R": "complex (production RAG — product suite)",
    "google/adk-python": "complex (official Google SDK, eval, deploy — product suite)",
    "agentstack-ai/AgentStack": "slightly complex (scaffold, multi-backend)",
    "howl-anderson/agentsilex": "super simple (~300 LOC)",
    "FlowiseAI/Flowise": "complex (low-code, drag-drop — product suite)",
    "browser-use/browser-use": "slightly complex (LLM + browser, Playwright)",
    # multi-agent
    "openai/openai-agents-python": "mostly simple (minimal surface)",
    "crewAIInc/crewAI": "complex (roles, Flows, production — product suite)",
    "microsoft/autogen": "complex (group chat, code exec, AG2 — product suite)",
    "MervinPraison/PraisonAI": "mostly simple (single entry, minimal config)",
    "THUDM/AgentRL": "complex (RL, Ray, train agents — product suite)",
    # plugins-mcp-cli
    "Aider-AI/aider": "slightly complex (CLI, git-aware, MCP)",
    "RyanAlberts/agentlog": "super simple (one file, three commands)",
    "thedotmack/claude-mem": "slightly complex (session capture + compression)",
    "ajhcs/Better-OpenCodeMCP": "mostly simple (MCP server, model bridging)",
    "modelcontextprotocol/python-sdk": "mostly simple (SDK only)",
    "modelcontextprotocol/typescript-sdk": "mostly simple (protocol reference)",
    "continuedev/continue": "complex (IDE extension, multi-editor — product suite)",
    "modelcontextprotocol/inspector": "super simple (debug GUI)",
    "github/github-mcp-server": "slightly complex (official GitHub MCP)",
    "modelcontextprotocol/registry": "slightly complex (official discovery layer)",
    "docker/mcp-gateway": "slightly complex (Docker-aware MCPs)",
    "withLinda/puppeteer-real-browser-mcp-server": "mostly simple (real browser, anti-detect)",
    # evaluation
    "arcprize/ARC-AGI-2": "super simple (task set)",
    "arcprize/arc-agi-benchmarking": "mostly simple (runner, multi-provider)",
    "GAIR-NLP/AgencyBench": "complex (32 scenarios, Docker, judges — product suite)",
    "patronus-ai/trail-benchmark": "mostly simple (traces, Hugging Face)",
    "THUDM/AgentBench": "complex (multi-env, Docker Compose — product suite)",
    "web-arena-x/webarena": "complex (812 tasks, web env — product suite)",
    "SWE-bench/SWE-bench": "slightly complex (real GitHub issues, standard)",
    "SWE-Gym/SWE-Gym": "slightly complex (training + eval, ICML)",
    "SWE-bench/SWE-smith": "slightly complex (50k+ instances, data gen)",
    "allenai/super-benchmark": "slightly complex (ML/NLP repos, Docker)",
    "meituan-longcat/vitabench": "complex (66 tools, cross-scenario — product suite)",
    "letta-ai/letta-evals": "mostly simple (Letta-specific harness)",
    "MinorJerry/WebVoyager": "slightly complex (LMMs, screenshots, 15 sites)",
    "UKGovernmentBEIS/inspect_evals": "slightly complex (Inspect AI, UK gov)",
    "UKGovernmentBEIS/inspect_ai": "complex (eval framework, AISI stack — product suite)",
    "microsoft/agent-lightning": "complex (agent training, Microsoft stack — product suite)",
    # research-task
    "assafelovic/gpt-researcher": "complex (deep research, multi-agent — product suite)",
    "OpenAgentsInc/openagents": "complex (platform, decentralized — product suite)",
    # libraries-sdks
    "langchain-ai/deepagents": "slightly complex (planning, files, sub-agents)",
    "pydantic/pydantic-ai": "slightly complex (type-safe, MCP, Logfire)",
    "MaxGfeller/open-harness": "slightly complex (streaming, tools, subagents)",
    "vercel/ai": "slightly complex (React/Node SDK, provider-agnostic)",
    "huggingface/smolagents": "mostly simple (code-as-action, ~1k LOC)",
    "strands-agents/sdk-python": "mostly simple (decorators, MCP, minimal code)",
    "openai/openai-agents-js": "slightly complex (handoffs, guardrails, voice)",
    "BerriAI/litellm": "mostly simple (LLM pipe only)",
    "ComposioHQ/composio": "complex (1k+ tools, auth, search — product suite)",
    "mem0ai/mem0": "slightly complex (memory layer, multi-platform)",
    "cloudflare/agents": "slightly complex (Durable Objects, stateful)",
    "e2b-dev/E2B": "slightly complex (sandbox API, code execution)",
    "daytonaio/daytona": "slightly complex (dev env API, isolation)",
    "brandonhimpfen/awesome-ai-agents": "super simple (curated lists)",
}


def py_dq_string(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main() -> None:
    path = Path("scripts/generate.py")
    src = path.read_text()
    tree = ast.parse(src)

    # Collect (axis_node, github_id) for every Project(...) call.
    edits: list[tuple[ast.Constant, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "Project":
            if len(node.args) < 4:
                continue
            gid_node = node.args[1]
            axis_node = node.args[3]
            if not (isinstance(gid_node, ast.Constant) and isinstance(axis_node, ast.Constant)):
                continue
            gid = gid_node.value
            if gid not in NEW_AXIS:
                raise SystemExit(f"Project {gid!r} is not in NEW_AXIS — refusing to relabel partial.")
            edits.append((axis_node, NEW_AXIS[gid]))

    covered = {gid for _, gid in [(e[0], e[0].value) for e in edits if False]}  # noqa: silence
    project_ids = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "Project":
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
                project_ids.add(node.args[1].value)
    extras = set(NEW_AXIS) - project_ids
    if extras:
        raise SystemExit(f"NEW_AXIS has unknown github_ids not in generate.py: {sorted(extras)}")

    # Apply edits in reverse-source order so offsets in earlier locations stay valid.
    edits.sort(key=lambda e: (e[0].lineno, e[0].col_offset), reverse=True)
    lines = src.splitlines(keepends=True)
    for axis_node, new_axis in edits:
        if axis_node.lineno != axis_node.end_lineno:
            raise SystemExit(f"Axis literal at line {axis_node.lineno} spans multiple lines; aborting.")
        line_idx = axis_node.lineno - 1
        line = lines[line_idx]
        new_literal = py_dq_string(new_axis)
        new_line = line[: axis_node.col_offset] + new_literal + line[axis_node.end_col_offset :]
        lines[line_idx] = new_line

    path.write_text("".join(lines))
    print(f"Relabelled {len(edits)} Project axis values.")


if __name__ == "__main__":
    main()
