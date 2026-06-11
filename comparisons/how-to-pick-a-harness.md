# How to pick a harness

Six questions, in order. Each one eliminates most of the list; by the end you should be choosing between two or three projects, not 103. The [use-case index](../README.md#pick-by-use-case), the [landscape charts](../README.md#the-landscape-at-a-glance), and the head-to-head pages do the heavy lifting.

## 1. What do you actually want it to do?

Don't start from frameworks; start from the job. The [Pick by use case](../README.md#pick-by-use-case) index maps 14 reader intents ("turnkey coding agent today", "drop-in memory layer", "always-on personal agent in my chat apps") to 3–7 curated picks each. If your job is on that list, you're already down to a handful of candidates.

## 2. How much do you want to adopt?

The ⚖️ simplicity ↔ capability tier measures surface area: **super simple** (a file format) → **complex** (a platform with its own runtime and ecosystem). Rule of thumb: pick the *lowest* tier that solves the job, because every tier you go up is something you'll maintain, secure, and eventually migrate off. A skill pack on a harness you already run beats a new framework; a library beats a platform.

## 3. How much rope does it need?

The autonomy axis (★ = headless-ready) runs **step-gated → checkpoint-gated → bounded → headless**. Match it to your actual risk tolerance, not your ambition: if you'll review every change anyway, a step-gated tool like Cline wastes nothing; if you want overnight runs, only bounded-and-above qualifies, and the [Autonomy × Recovery grid](../README.md#the-landscape-at-a-glance) shows which. Remember autonomy is co-constructed — the harness's approval defaults shape real-world behavior as much as the model does.

## 4. What happens when it breaks?

Runs die: rate limits, crashed sandboxes, closed laptops. The recovery axis (✱ = durable) runs **none → retry → resumable → durable**. For anything long-running or unattended, treat **resumable** as the floor and **durable** as the bar for production — only a handful of projects clear it (see the top-right of the grid). A headless harness with no recovery story is an incident generator.

## 5. Who pays for the tokens?

The question that changed in 2026. Since **June 15, 2026**, programmatic and third-party-harness usage on Claude subscriptions draws from a separate, non-rollover [Agent SDK credit pool](https://thenewstack.io/anthropic-agent-sdk-credits/) ($20–$200/month by plan, billed at API rates) — an always-on agent on subscription auth is no longer flat-rate. So price the harness's *usage shape*: heartbeat-driven and always-on (OpenClaw, Hermes) burns idle tokens; session-based (terminal coding agents) doesn't. Field reports put unoptimized always-on monitoring at ~$360/month and the same workload under $10 after three fixes, in priority order: **wake less** (deterministic scripts that only invoke a model on a match), **route by tier** (cheap/free models for background work, a mid-tier model for conversations — never a frontier model on a heartbeat), and **slim the tool list** (large tool registries tax every turn). Your provider options: a first-party tool whose subscription covers it, a metered API key with budget caps, or open-weight models on your own hardware — and harnesses differ sharply in how well they support that third path. [OpenClaw vs Hermes](openclaw-vs-hermes.md) covers all of this in depth.

## 6. Can you walk away from it?

Prefer harnesses where your investment ports: instructions in open formats (AGENTS.md, SKILL.md), standard protocols (MCP), permissive licenses (the ✅ column), and state you can export. Switching costs between terminal coding agents are deliberately low — trying two is cheap ([comparison](terminal-coding-agents.md)). Switching costs between platforms are not — which is one more reason question 2 says to start low.

## Worked examples

- *"I want code reviews while I sleep"* → use case: coding agent; autonomy: headless ★; recovery: resumable+; billing: session-based → opencode headless, OpenHands, or Claude Code GitHub Actions (mind the credit pool).
- *"I want a personal assistant in Telegram"* → use case: always-on personal agent; billing: always-on (!) → [OpenClaw vs Hermes](openclaw-vs-hermes.md), budget decision first.
- *"My multi-agent pipeline must survive deploys"* → recovery: durable ✱ → LangGraph, n8n, Letta, or Cloudflare Agents ([comparison](multi-agent-orchestration.md)).

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). The same data is queryable by agents via the [MCP server](../mcp/) — `pick_harness(use_case, max_complexity, min_autonomy, min_recovery)` automates questions 1–4._
