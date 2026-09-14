# Managed vs self-hosted always-on agents

An always-on agent keeps working between your messages, and in 2026 you can rent one (Grok Bot, Claude Managed Agents), run one for your whole team (QM), run one for yourself (OpenClaw, Hermes), or keep one on your own laptop (OpenJarvis). This guide says who owns the computer in each case, who pays for idle time, and which one to pick.

| | [Grok Bot](https://docs.x.ai/grok-bot/approvals-security-and-privacy) | [Claude Managed Agents](https://platform.claude.com/docs/en/about-claude/pricing) | [QM](https://github.com/yc-software/qm) | [OpenClaw](https://github.com/openclaw/openclaw) / [Hermes](https://github.com/NousResearch/hermes-agent) | [OpenJarvis](https://github.com/open-jarvis/OpenJarvis) |
|---|---|---|---|---|---|
| Who runs it | xAI | Anthropic | You, for your team (Fly, AWS, or your own servers) | You, for yourself (a Mac mini, a VPS) | You, on the device in front of you |
| Where the agent's computer lives | One shared cloud computer per account | Anthropic's sandboxed sessions | Sandboxes your deployment allocates, plus Postgres for state | Your machine | Your machine; no cloud by default |
| Talk to it from | Desktop app (macOS, Windows), iPhone | Your own app, through the API | Slack and a web app, including shared rooms | WhatsApp, Telegram, Slack, Discord, and more | Desktop app and command line |
| Model | Grok, xAI's choice | Claude | Any: Pi, OpenCode, Codex, and Claude Code drive the same core | Any provider or local model | Local models (Qwen, Gemma, GPT-OSS) through Ollama, llama.cpp, or vLLM |
| License | Proprietary | Proprietary | MIT | MIT / MIT | Apache-2.0 |
| Cost shape | Subscription with a weekly usage allowance; extra usage billed from token cost | Tokens at API rates plus $0.08 per active session-hour; idle time is free | Your servers plus your model keys | Your hardware plus keys or a subscription | Your hardware; near-zero marginal cost |
| Approval model | Asks before sending, publishing, deleting, buying, or changing production; passwords and two-factor codes stay with you | Set by your code | Human-reviewed bulk writes; read-mostly by default | Relaxed by default (OpenClaw) or restrictive (Hermes) | Yours to set |

## What is Grok Bot, and is it an agent harness?

Grok Bot is xAI's always-on agent product, in beta since August 11, 2026. A Bot is a persistent, named agent: you message it from the Grok Bot app, give it a job and access to the tools it needs, and it keeps working on a cloud computer with a browser, files, and a command line while your own computer is off ([Composio's guide](https://composio.dev/content/guide-to-frok-bot), [xAI docs](https://docs.x.ai/grok-bot/approvals-security-and-privacy)). It is a harness in this list's sense: xAI owns the loop, the tool wiring, the memory, and the approval rules, and you rent the result. It is not in the ranked list because the list ranks open repositories, and Grok Bot has none.

Two design facts decide whether it fits you. All Bots on one account share the same cloud computer, files, browser sessions, and command-line credentials, so xAI's own docs say not to treat separate Bots as separate security boundaries. And the approval model is fixed by xAI: a Bot asks before sending messages, publishing, deleting, buying, or changing production systems, and passwords, two-factor codes, and CAPTCHAs stay with you. Skills (reusable workflows), routines (scheduled or event-triggered runs), and groups of two to six Bots working together round out the product. Access comes bundled with SuperGrok Heavy, Cursor Ultra, and eligible Cursor team plans, with a weekly usage allowance and extra usage billed from token cost ([pricing notes](https://www.eesel.ai/blog/grok-bot-pricing)).

## Grok Bot vs OpenClaw: who owns the computer?

This is the whole difference. OpenClaw runs on a machine you own, with the accounts you gave it, and its "free reign" defaults are yours to tighten; the [OpenClaw vs Hermes guide](openclaw-vs-hermes.md) covers the security posture, the update churn, and the token bill in depth. Grok Bot runs on a computer xAI owns, with approval gates xAI wrote, and a bill that tracks xAI's plan changes. Pick OpenClaw or Hermes if you want to read the code that touches your accounts, run any model, and own the state. Pick Grok Bot if you want an agent with a computer by tonight and one vendor holding the keys is acceptable.

## QM vs OpenClaw: personal or multiplayer?

QM (Quartermaster) is Y Combinator's own harness, open-sourced under MIT on July 31, 2026, after months of internal use across accounting, legal, events, and engineering ([repo](https://github.com/yc-software/qm), [MarkTechPost](https://www.marktechpost.com/2026/08/03/y-combinator-open-sources-qm-multiplayer-ai-agent-harness/)). Its README draws the line itself: most agents are designed like personal assistants; QM is designed for startups. Every person and every room gets its own scoped memory, files, credentials, permissions, crons, web apps, and sandbox, and people can work with it together in a Slack channel.

The architecture choice, from the team's talk at YC's Paper Club (52:00 in [the video](https://www.youtube.com/watch?v=n9xKblqyQ28)): pull the brain out of the sandbox. OpenClaw and Hermes give the agent its own computer, which is powerful and also traps every session inside that computer, so a fleet of fifty of them became a whack-a-mole of SSH repairs. QM stores everything in Postgres, treats sandboxes as a resource the agent dips into (a small one for simple work, a bigger machine for heavy dev jobs), and keeps the harness to three core tools: run code in a remote sandbox, read and write object storage, publish an internal app. Two lessons from running it: agents give up too early, so QM puts wall-clock and token budgets on goals; and the amount of knowledge you can safely put in a shared brain is bounded by how good your permission system is.

Pick OpenClaw or Hermes for one person and one machine. Pick QM when several people share one agent and you already have the permissions to keep their data apart.

## OpenJarvis: the model runs on your own device

OpenJarvis, from Stanford's Hazy Research and Scaling Intelligence labs, keeps the whole stack on the device: model inference, agent execution, memory, and learning ([repo](https://github.com/open-jarvis/OpenJarvis), [Stanford write-up](https://scalingintelligence.stanford.edu/blogs/openjarvis)). It defines five primitives (the interfaces, the agent logic, the model, the inference engine, and the tools, memory, and learning around them) and lets a cloud model tune that local configuration once, so you get the tuning without paying cloud prices at run time. The team's numbers from the talk (43:00): on-device models trail the frontier by six to twelve months, and an optimized local stack ran personal-assistant and coding tasks at 800 times lower cost than the cloud. Pick it when privacy or cost rules out the cloud and your tasks fit a model that runs on your hardware.

## Claude Managed Agents: the API-shaped version

Anthropic's Managed Agents (public beta since April 8, 2026) rent you the infrastructure, not a chat product: sandboxing, long-running sessions, state, and error recovery behind an API, billed at token rates plus $0.08 per session-hour while the session is active, with idle time free ([pricing](https://platform.claude.com/docs/en/about-claude/pricing)). You bring the interface and the agent logic. It belongs in this comparison because it is the managed answer for teams who want to ship their own product on top rather than adopt someone else's assistant.

## When managed beats self-hosted

Managed wins when you have no one to run servers, when the job needs a browser and a computer today, or when the vendor's approval model is stricter than what you would build. Self-hosted wins when the agent needs your credentials and you want to read the code that uses them, when you want to swap models (the [pairing rule](why-the-harness-matters.md) says the best harness depends on the model), when you need state you can export, or when the workload runs all day and a metered bill would hurt.

## Who pays for idle time?

Always-on means the clock runs while nothing happens. Grok Bot meters a weekly allowance and bills the overage from token cost. Managed Agents charge only while a session is active. QM, OpenClaw, and Hermes cost whatever your server and model keys cost, which the [OpenClaw vs Hermes guide](openclaw-vs-hermes.md#the-billing-scare-april-to-june-2026) shows can be $360 a month unoptimized and under $10 after three fixes. OpenJarvis costs electricity. Price the usage shape before you price the plan.

## Which one should you pick?

- *One person, one machine, a chat-app front end* → OpenClaw or Hermes ([head-to-head](openclaw-vs-hermes.md)).
- *A team sharing one agent in Slack, with per-room permissions* → QM.
- *A computer-using agent by tonight, vendor holds the keys* → Grok Bot.
- *Your own product on rented agent infrastructure* → Claude Managed Agents.
- *Nothing leaves the laptop* → OpenJarvis.

Autonomy and recovery scores for the open-source options are on their project pages in the [ranked list](../README.md#personal-agent-runtimes).

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). Facts checked 2026-09-14; corrections welcome as issues with a source link._

_Agents can query this page's data directly: `claude mcp add agent-harnesses -- uvx agent-harnesses-mcp` ([MCP server](../mcp/))._
