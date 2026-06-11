# OpenClaw vs Hermes: the always-on personal-agent debate

The loudest harness argument of 2026. Both are open-source (MIT), self-hosted, always-on personal agents you talk to from chat apps — and they're the two most-starred projects on this entire list. The Reddit debate treats them as rivals; the architecture says they're different bets that happen to share a category.

| | [OpenClaw](https://github.com/openclaw/openclaw) | [Hermes](https://github.com/NousResearch/hermes-agent) |
|---|---|---|
| ⭐ Stars | 378k | 191k |
| Steward | OpenClaw Foundation (community) | Nous Research |
| License | MIT | MIT |
| Core language | TypeScript | Python |
| The bet | **Ubiquity** — a gateway + event-loop runtime where messages, heartbeats, crons, and webhooks are all one input queue; lives in every chat app you use | **Compounding** — a learning loop that turns experience into reusable skills and a persistent user model; the agent is better next month than it was last month |
| Ecosystem | 13,700+ community skills (ClawHub), native multi-agent, the most channels and integrations of any open agent | Lean by design: stateless-by-default sub-agents, disk-first memory, checkpoint/rollback |
| Footprint | Heavier; its own runtime and ecosystem to adopt | "$5 VPS and forget"; easiest setup of the two |
| Model story | Any provider | Model-agnostic by design — Nous Portal, OpenRouter (200+ models), OpenAI, or your own endpoint; open-weights-friendly |
| Autonomy (list axis) | headless | headless |
| Recovery (list axis) | resumable | resumable (checkpoint/rollback is a marquee feature) |

_Stars as captured for the main list (see [README](../README.md#guide-to-rankings) for the capture date)._

## The billing earthquake (April → June 2026)

You can't pick between these two without understanding what happened to subscription-powered harnesses:

- **Early April 2026:** Anthropic banned third-party agents and harnesses from running on Claude subscriptions, citing capacity and service issues — an estimated 135,000+ OpenClaw instances were running on subscription auth at the time.
- **June 15, 2026:** Anthropic [reinstated third-party agent usage](https://venturebeat.com/technology/anthropic-reinstates-openclaw-and-third-party-agent-usage-on-claude-subscriptions-with-a-catch) — with a catch. Programmatic usage (Agent SDK, `claude -p`, GitHub Actions, and third-party harnesses like OpenClaw and Hermes) now draws from a [separate monthly "Agent SDK credits" pool](https://thenewstack.io/anthropic-agent-sdk-credits/): $20–$200 depending on plan, billed at API rates, non-rollover. The stated reason: first-party tools are engineered to maximize prompt-cache hits; third-party harnesses largely bypass that optimization and cost more to serve.

What this means in practice: **an always-on harness pointed at a Claude subscription is no longer flat-rate.** A heartbeat-driven agent that polls every few minutes can drain a $20 credit pool in days. Both projects responded the same way — first-class support for routing to other providers and open-weight models. Hermes is structurally better positioned here (model-agnosticism and open weights are Nous's founding thesis); OpenClaw is provider-flexible but its community grew up on subscription-auth Claude, so more of its users felt the change.

## What the community actually concluded

Across the ~1,300-comment Reddit debate ([analysis](https://kilo.ai/openclaw/vs-hermes), [comparison](https://composio.dev/content/openclaw-vs-hermes-agent)), the consensus is less "which is better" and more "which problem do you have":

- **Pick OpenClaw when the problem is orchestration.** More channels, more integrations, the largest skill ecosystem, native multi-agent. If you want one agent reachable from everywhere that can coordinate many things, breadth wins.
- **Pick Hermes when the problem is automation that should improve over time.** The learning loop, default memory, and checkpoint/rollback make repeated task loops get cheaper and more reliable with use. If you want a fire-and-forget specialist on a cheap VPS, lean wins.
- **The power-user pattern is both:** OpenClaw as the orchestrator (planning, decomposition, multi-step coordination), Hermes as the execution specialist (fast, repeatable task loops). They compose better than they compete.

## The question to ask first

*Do you want an agent that's everywhere, or an agent that's learning?* Everywhere → OpenClaw. Learning → Hermes. Both, with a budget → OpenClaw orchestrating Hermes workers, on open-weight models or a metered API key you actually monitor.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). New to this decision? Start with [How to pick a harness](how-to-pick-a-harness.md). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._
