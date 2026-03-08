---

## name: Best of Agent Harnesses README
overview: "Transform the README in RyanAlberts/best-of-Agent-Harnesses from its current template into a Best of Agent Harnesses and Harness Techniques curated list: add an opinionated definition/summary, define future-proof categories, research and grade 50+ GitHub repos, rank them within categories, and rewrite the README while preserving only Explanation, Related Resources, and Contribution sections."
todos: []
isProject: false

# Best of Agent Harnesses README Update

## Scope

- **Target file:** **README.md** in the repo [RyanAlberts/best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). (Clone the repo into your workspace to edit; the file path will be `best-of-Agent-Harnesses/README.md`.)
- **Keep:** Generic sections only — "Explanation" (grading icons/legend), "Related Resources", "Contribution" (adapted for this list).
- **Remove:** All current template placeholder content (e.g. the 25 best-of lists in categories like Machine Learning & Data Engineering, Web Development, best-of-ml-python, etc.) so no generic best-of template content remains.
- **Add:** Title "Best of Agent Harnesses and Harness Techniques"; opinionated summary defining agent harnesses; categorized, ranked list of 50+ AI agent harness repos; include GSD-build/get-shit-done as an example.

## 1. Definition and Summary (paraphrased, non-plagiarized)

Synthesize from the three sources:

- **OpenAI (harness engineering):** Harness = environment design, intent specification, feedback loops, and repository-as-system-of-record so agents (e.g. Codex) can do reliable work; engineers design scaffolding and guardrails, not write code.
- **Anthropic (effective harnesses):** Long-running agents need session bridging (initializer + coding agent), feature lists, progress files, incremental work, clean state, and explicit testing (e.g. browser automation) to avoid one-shotting or premature "done."
- **Aakash Gupta (Medium):** Harness = everything around the model (human-in-the-loop, filesystem access, tool orchestration, sub-agent coordination, prompt presets, lifecycle hooks); "model is commodity, harness is moat"; minimal intervention, progressive disclosure, fail-fast with recovery.

**Deliverable:** A concise "What is an agent harness?" intro and a short "Why harnesses matter" / "Techniques" subsection that sets up the curated list.

## 2. Future-proof categories

Proposed categories (broad enough to add repos later):

- **Full-stack and long-running coding harnesses** — Spec-driven, multi-session, repo-scoped coding (e.g. GSD, Claude Agent SDK, Codex-style workflows).
- **Multi-agent and orchestration frameworks** — Sub-agents, handoffs, crews, graphs (e.g. LangChain/LangGraph, OpenAI Swarm/Agents SDK, CrewAI, AutoGen).
- **IDE and CLI agent integrations** — Cursor, MCP, Aider, OpenCode, and CLI wrappers that provide tools and context.
- **Evaluation and benchmarking harnesses** — SWE-bench-style, agent evals, and reproducibility tooling.
- **Research and task-specific harnesses** — Deep research, document/question-answering, and domain-specific agent loops.
- **Libraries and SDKs** — Lightweight agent runtimes, tool loops, and provider-agnostic harness primitives (e.g. Vercel AI SDK agents, OpenHarness, Pydantic AI).

Optional catch-all: **Techniques and practices** — AGENTS.md, execution plans, repo layout for agents (can be a short section or folded into intro).

## 3. Repo research and grading (50+ repos)

- **Sources:** GitHub search, awesome lists (e.g. awesome-ai-agents, awesome-ai-agent-frameworks), and cited repos (GSD, Claude Agent SDK, OpenAI Swarm/Agents SDK, LangChain/LangGraph, OpenHarness, RepoMaster, CoderClaw, etc.).
- **Grading:** Use the same legend as the template: project-quality score (or star-based tier), stars, age (new/inactive/dead), trending, contributors, forks, issues, last update. Apply consistently so new repos can be added later.
- **Output:** A structured list (e.g. markdown or YAML-friendly) with repo slug, category, 1–2 line description, and grade fields.

## 4. Ranking within categories

- Within each category, rank by: relevance to "agent harness" (environment, orchestration, lifecycle, guardrails), then by stars/activity/quality.
- GSD-build/get-shit-done appears in "Full-stack and long-running coding harnesses" (or equivalent) as the requested example.

## 5. README structure (final)

- **Title and tagline:** Best of Agent Harnesses and Harness Techniques.
- **Short intro:** What this list is and who it's for.
- **Summary:** "What is an agent harness?" + "Why harnesses matter" / techniques (paraphrased from the three URLs).
- **Contents:** TOC linking to categories.
- **Explanation:** Reuse template's grading legend (icons for score, stars, new/inactive/dead, trending, contributors, forks, issues, etc.).
- **Categories:** Each category has a subtitle and a ranked list of projects with: name, grade, short description, GitHub link, and optional clone/install line.
- **Related Resources:** Keep section; point to Awesome, official docs (OpenAI, Anthropic, LangChain), and the three definition URLs.
- **Contribution:** Short "how to suggest or add projects" (issue or PR), no generator-specific YAML/contributing links unless we add a projects file later.

## 6. Execution order

1. Write the new README shell: title, intro, definition/summary, Explanation block, placeholder category headers.
2. Populate categories with the 50+ researched repos, ranked; ensure GSD and key SDKs are included.
3. Add Related Resources and Contribution.
4. Remove any remaining template-only content; ensure no generic best-of placeholder categories or projects remain.

## Key files

- **README.md** in [RyanAlberts/best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses) — sole file to update for this task. Repo may also use `projects.yaml` for generator-driven updates; the plan focuses on the README content.

## References (for summary and Related Resources)

- [https://openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/)
- [https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [https://aakashgupta.medium.com/2025-was-agents-2026-is-agent-harnesses-heres-why-that-changes-everything-073e9877655e](https://aakashgupta.medium.com/2025-was-agents-2026-is-agent-harnesses-heres-why-that-changes-everything-073e9877655e)

