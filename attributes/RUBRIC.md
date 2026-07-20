# Deep-dive attribute rubric

One JSON file per researched project (`attributes/<slug>.json`, slug = the project's `slug` in
`harnesses.json`; JSON so `generate.py` stays stdlib-only in the weekly-rescore workflow).
`scripts/generate.py` validates every file against this rubric and merges it into each
project's `deep_dive` object in `harnesses.json`, which feeds the MCP server. A file that
violates the vocabulary, omits an axis, or is missing evidence fails the build loudly.

**Scope.** Only runtime harnesses are researched: categories `progressive-disclosure`,
`coding-agent-products`, `coding-harness-configs`, `personal-agent-runtimes`, `frameworks`,
`multi-agent`, `memory`, `research-task`. Projects in other categories (single-purpose
plugins/MCP tools, eval benches, observability, pure libraries) carry no file — the MCP reports
them as not deep-dive rated rather than pretending a sandbox rating for a linter plugin.

**Evidence rule.** Every rating except `unknown` MUST carry an `evidence` URL pointing at a doc
page, README section, or source file that demonstrates the claim. If you cannot find evidence,
the rating is `unknown` with a one-line `detail` saying what you looked for. Never infer a
rating from the project's marketing copy alone.

## File schema

```json
{
  "github_id": "openclaw/openclaw",
  "researched": "2026-07-19",
  "tooling_sandboxing":  {"rating": "strong", "detail": "One sentence: what mechanism, at what rigor.", "evidence": "https://..."},
  "context_memory":      {"rating": "strong", "detail": "...", "evidence": "https://..."},
  "lifecycle_hooks":     {"rating": "full", "detail": "...", "evidence": "https://..."},
  "prompt_optimization": {"rating": "native", "detail": "...", "evidence": "https://..."},
  "build_vs_buy":        {"tier": 2, "label": "blueprint", "detail": "One sentence: why this tier.", "evidence": "https://..."}
}
```

Rating vocabularies: `tooling_sandboxing`/`context_memory`: `strong | basic | none | unknown`;
`lifecycle_hooks`: `full | partial | none | unknown`; `prompt_optimization`:
`native | configurable | none | unknown`. All four axes and `build_vs_buy` are required.
`label` must match `tier` (1=build, 2=blueprint, 3=managed).

## Axis definitions

### tooling_sandboxing — how it acts
How tool execution is contained. Grounded in the sandbox-rigor ladder (allowlist → container
isolation → managed cloud sandbox) from [Agent Harness Engineering]
(https://engineeratheart.medium.com/the-definitive-guide-to-agent-harness-engineering-5f5edf25fd73)
and the harness definition ("a container, a virtual machine, or a restricted filesystem") from
[PuppyGraph](https://www.puppygraph.com/blog/agent-harness).

- `strong` — enforced isolation ships in the harness AND governs the default execution
  path: container/VM/microVM execution, an enforced command allowlist, or a restricted
  filesystem the agent cannot escape by default. Executor-selection architectures count
  when the shipped executors are isolated and host execution is a flagged dev-only escape
  hatch. A host-default path with an opt-in sandbox flag is `basic`.
- `basic` — approval gates, permission prompts, or configurable restrictions exist, but
  execution is on the host by default; isolation is opt-in or delegated to an external tool.
- `none` — tools/commands run directly with the user's privileges; nothing intercepts them.
- `unknown` — no evidence either way.

### context_memory — how it remembers
- `strong` — persistent memory across sessions (vector/graph/file-based) OR built-in context
  engineering of the conversation/task context itself: compaction/summarization, session
  resume, retrieval on demand. Retrieval that only scopes TOOL DEFINITIONS (progressive
  disclosure of tools) is `basic` at most — it manages the tool surface, not memory.
- `basic` — manages the live session's context (history threading, token budgeting) but
  nothing survives the process or gets compacted intelligently.
- `none` — stateless request/response; the caller owns all context.
- `unknown` — no evidence either way.

### lifecycle_hooks — interception points
The "before and after" interception pattern (before: validation/blocking; during: timeout;
after: error classification and tool traces) per Agent Harness Engineering.

- `full` — user-definable before AND after hooks that can BLOCK or rewrite an action
  (pre-tool-use validation, policy enforcement), plus tool-call tracing/logging. The
  interception point must be PROGRAMMABLE (custom logic: hook code, middleware, filters,
  or an in-loop primitive like interrupt()/suspend()); fixed built-in approval prompts or
  permission configs that merely ask a human are `partial`.
- `partial` — observable but not enforceable: event callbacks, middleware, or trace logging
  exist, but they cannot veto an action before it executes (or only cover a subset).
  Output guardrails/validators that run AFTER the action, and run/crew-level kickoff
  callbacks, are `partial` — `full` requires stopping a tool call before it runs.
- `none` — no interception surface; you get what the loop does.
- `unknown` — no evidence either way.

### prompt_optimization — refinement support
- `native` — the harness itself optimizes prompts: refinement loops, automatic prompt tuning
  (DSPy-style compilers, self-improving system prompts, eval-driven prompt search).
- `configurable` — user-specific rules and system-prompt adjustment are first-class
  (rules files, CLAUDE.md/AGENTS.md-style instruction layering, per-project system prompts)
  but the harness does not itself improve them.
- `none` — prompts are hardcoded or only reachable by forking.
- `unknown` — no evidence either way.

### build_vs_buy — adoption tier (how it scales)
Three tiers, per the architectural-comparison framing (Direct API orchestration vs blueprints
vs managed) and the build/buy criteria in Agent Harness Engineering:

- `tier: 1`, `label: build` — **Direct API orchestration.** You write and own the loop; the
  project is an SDK/primitive set you compose (maximum control and security; needs
  distributed-systems capacity). Signals: "library you import", no opinionated runtime.
- `tier: 2`, `label: blueprint` — **Agent blueprints & frameworks.** An opinionated,
  self-hostable runtime/framework where you configure blueprints, rules, and logic rather
  than writing the loop (model flexibility, compliance via self-hosting). Signals: config-driven
  agents, plugin/skill systems, you run the process.
- `tier: 3`, `label: managed` — **Managed infrastructure.** The execution stack runs on a
  vendor platform; fastest time to market, least operational ownership. Signals: hosted
  control plane required for core value, usage-billed execution.

Edge rule: projects offering both (open-core with a hosted platform) get the tier of their
*primary published artifact* — the thing the GitHub repo installs — with the alternative named
in `detail`.

## Rank derivation (generate.py)
`strong/full/native = 3`, `basic/partial/configurable = 2`, `none = 1`, `unknown = 0` (excluded
from comparisons). `build_vs_buy` is categorical — no rank, no "better" direction.
