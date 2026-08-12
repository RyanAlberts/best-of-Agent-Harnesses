# How to pick a harness

This is the decision guide for [best-of-Agent-Harnesses](../README.md), a curated, ranked list of the runtimes that turn an AI model into a working agent: the software that decides what the model's thinking is allowed to touch. Six questions, in order. Each one eliminates most of the list; by the end you should be choosing between two or three projects instead of the entire list. The [use-case index](../README.md#pick-by-use-case), the [landscape charts](../README.md#the-landscape-at-a-glance), and the head-to-head comparison pages linked throughout do the heavy lifting.

## 1. What do you actually want it to do?

Don't start from frameworks; start from the job. The [Pick by use case](../README.md#pick-by-use-case) index maps 14 reader intents ("turnkey coding agent today", "drop-in memory layer", "always-on personal agent in my chat apps") to 2-7 curated picks each. If your job is on that list, you're already down to a handful of candidates.

## 2. How much do you want to adopt?

Every project carries a simplicity-to-capability tier measuring how much you take on by adopting it: **super simple** (a file format, nothing to run) → **mostly simple** (a small library or content bundle) → **slightly complex** (a real tool with moving parts) → **complex** (a platform with its own runtime and ecosystem). Rule of thumb: pick the *lowest* tier that solves the job, because every tier you go up is something you'll maintain, secure, and eventually migrate off. A skill pack on a harness you already run beats a new framework; a library beats a platform.

## 3. How much rope does it need?

The autonomy rating (★ in the tables = ready for unattended runs) describes how much a harness is designed to do without you watching: **step-gated** (asks before every action) → **checkpoint-gated** (asks at milestones) → **bounded** (runs free inside limits you set) → **headless** (built to run with nobody watching; here that's about supervision, not whether it has an interface). Match it to your actual risk tolerance, not your ambition: if you'll review every change anyway, a step-gated tool like Cline wastes nothing; if you want overnight runs, only bounded and above qualify, and the [Autonomy × Recovery grid](../README.md#the-landscape-at-a-glance) shows which. Autonomy is also shaped by configuration as much as by the model: the harness's approval defaults decide what actually happens on your machine.

## 4. What happens when it breaks?

Runs die: rate limits, crashed sandboxes, closed laptops. The recovery rating (✱ = durable) describes what survives: **none** (start over) → **retry** (it re-attempts failed steps) → **resumable** (a dead session can pick up where it stopped) → **durable** (execution state is persisted; even a process restart or redeploy doesn't lose the run). For anything long-running or unattended, treat **resumable** as the floor and **durable** as the bar for production; only a handful of projects clear it. A headless harness with no recovery story is an incident generator.

## 5. Who pays for the tokens?

The question 2026 keeps re-asking. In April 2026, Anthropic banned third-party agents from running on flat-rate Claude subscriptions; it then announced a separate metered credit pool for such usage, and on June 15, [paused that change the day it was due to take effect](https://thenewstack.io/anthropic-pauses-claude-agent-sdk-subscription-change/). As of August 2026, programmatic and third-party usage draws from normal subscription limits again, and Anthropic says any revised plan will come with notice. The lesson stands regardless of where the policy lands: **an always-on agent's economics can change under you, so price the usage shape, not the plan.** Heartbeat-driven agents (ones a timer wakes up all day, like OpenClaw and Hermes) burn tokens while idle; session-based tools (terminal coding agents) don't. Field reports put one unoptimized always-on setup near $360/month and the same workload under $10 after three fixes, in priority order: **wake less** (scripts that only invoke a model on a match), **route by tier** (cheap models for background work, never a frontier model on a timer), and **slim the tool list** (large tool registries tax every request). Your insurance policy is provider flexibility: harnesses differ sharply in how well they support metered API keys with budget caps and open-weight models on your own hardware. [OpenClaw vs Hermes](openclaw-vs-hermes.md) covers all of this in depth.

## 6. Can you walk away from it?

Prefer harnesses where your investment ports: instructions in open file formats (AGENTS.md for repo briefings, SKILL.md for on-demand procedures; see [Context files](progressive-disclosure.md)), standard protocols (MCP, the Model Context Protocol, the standard way tools plug into agents), permissive licenses (the license column in every table), and state you can export. Switching costs between terminal coding agents are deliberately low; trying two is cheap ([comparison](terminal-coding-agents.md)). Switching costs between platforms are not, which is one more reason question 2 says to start low.

## Worked examples

- *"I want code reviews while I sleep"* → use case: coding agent; autonomy: headless ★; recovery: resumable or better → opencode headless or OpenHands.
- *"I want a personal assistant in Telegram"* → use case: always-on personal agent; billing shape: always-on (watch question 5) → [OpenClaw vs Hermes](openclaw-vs-hermes.md), budget decision first.
- *"My multi-agent pipeline must survive deploys"* → recovery: durable ✱ → LangGraph (see the [orchestration comparison](multi-agent-orchestration.md)), or n8n, Letta, and Cloudflare Agents from the main list, all rated durable.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). The same data is queryable by agents via the [MCP server](../mcp/): `pick_harness(use_case, max_complexity, min_autonomy, min_recovery)` automates questions 1-4._

_Agents can query this page's data directly: `claude mcp add agent-harnesses -- uvx agent-harnesses-mcp` ([MCP server](../mcp/))._
