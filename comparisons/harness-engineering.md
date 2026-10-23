# Harness engineering: what it is, and the tools for each practice

Harness engineering means building everything around an AI model that turns it into a dependable agent: what it sees, which tools it gets, what it may do without asking, and how it checks its work. The model stays the same; you change its surroundings until a mistake it made once stops happening.

Essays explain the idea. This page maps each practice to the open-source projects in [this list](../README.md) that do it, with the list's own ratings: **autonomy** (how much it does without asking you), **recovery** (what survives when a run dies), and **complexity** (how much you take on by adopting it). A file format, library, or add-on with no agent loop of its own carries only a complexity rating.

## Where the term came from

Mitchell Hashimoto named the practice in [My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey) on February 5, 2026. In a step called Engineer the Harness, he wrote, "I've grown to calling this 'harness engineering.'" His rule: each time an agent makes a mistake, build a fix so it never makes that mistake again. The fix is a new line in AGENTS.md (a plain file of instructions the agent reads) or a small tool the agent can run. He said he was not trying to coin a term.

Six days later, on February 11, OpenAI published [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) by Ryan Lopopolo. Over five months, a small team built an internal product with no hand-written code: about a million lines and roughly 1,500 merged pull requests, all written by Codex. The engineers' job became designing the environment, stating intent, and building feedback loops.

LangChain's [The Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness) (March 10) gave the short formula: agent = model + harness, where the harness is all the code, settings, and logic that is not the model. Birgitta Böckeler of Thoughtworks wrote [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) (April 2), and Lilian Weng's [Harness Engineering for Self-Improvement](https://lilianweng.github.io/posts/2026-07-04-harness/) (July 4) took it into research. The idea is older than the name: [SWE-agent](https://arxiv.org/abs/2405.15793) (May 2024) showed that how tools are presented to a model changes what it can do. [The measurements behind the idea](why-the-harness-matters.md) have their own page.

## Context delivery

Context is what the model sees each turn, and the common mistake is one giant instruction file. OpenAI's team found it crowded out the task and went stale fast. Their fix was a short AGENTS.md, about 100 lines, that works as a table of contents for deeper docs kept in the repo. Load details only when a task needs them ([Context files](progressive-disclosure.md) has more), and shrink bulky tool output first.

- [agents.md](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/agentsmd/): super simple. The open format for repo briefings.
- [Anthropic Skills](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/skills/): mostly simple. Instruction folders the agent loads only when a task calls for them.
- [Headroom](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/headroom/): mostly simple. Compresses logs, files, and tool output before the model sees them.

Check yours: [agents-md-checker](../skills/agents-md-checker/) shows which instruction files each coding agent loads.

## Tool design

A tool's shape matters as much as how many tools there are. Anthropic's [guide to writing tools for agents](https://www.anthropic.com/research/writing-tools-for-agents) (September 11, 2025) advises a few well-chosen tools instead of one for every call a service offers, plus clear names, short responses, and error messages that say what to do next. Claude Code caps a tool response at 25,000 tokens (the units models read and bill by) unless told otherwise. The model reads every tool's description on each request, so some projects load tools only on demand.

- [MCP Servers](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/servers/): mostly simple. Official reference tools for the Model Context Protocol (MCP), the standard way tools plug into agents.
- [langgraph-bigtool](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/langgraph-bigtool/): bounded autonomy, durable recovery, slightly complex. Loads only the tools a step needs from a large set.
- [Playwright MCP](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/playwright-mcp/): mostly simple. Browser control through the page's structure, not screenshots.

Check yours: [tool-design-checker](../skills/tool-design-checker/) grades your MCP tools the way a model reads them.

## Permissions and approvals

Permissions set what the agent may do without asking you. Asking before every step sounds safe, but people stop reading what they approve; Anthropic calls it approval fatigue. Its [sandboxing write-up](https://www.anthropic.com/research/claude-code-sandboxing) (October 20, 2025) moves safety into fixed limits instead: only certain folders, only approved servers. Anthropic reports this cut permission prompts by 84% in internal use. Both limits matter: with folder limits alone, a hijacked agent can still send your keys out over the network.

- [Cline](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/cline/): step-gated autonomy, resumable recovery, slightly complex. Plans first, then asks before each step.
- [aider](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/aider/): checkpoint-gated autonomy, resumable recovery, slightly complex. A terminal pair programmer that works through git.
- [Codex](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/codex/): bounded autonomy, resumable recovery, slightly complex. OpenAI's coding agent, which runs its commands in a sandbox.
- [agent-vault](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/agent-vault/): mostly simple. Holds your secrets so the agent's tool calls never see raw keys.

Check yours: [sandbox-check](../skills/sandbox-check/) shows what your agent can reach, and [guardrail-tester](../skills/guardrail-tester/) tries about 90 dangerous commands against your rules.

## Verification loops

An agent that cannot check its own work hands the checking to you. Hashimoto found that an agent with a way to verify its work usually fixes its own mistakes. OpenAI's team had Codex review its own pull request, ask other agents to review it, and repeat until every reviewer was satisfied. Böckeler sorts these controls into guides, which steer the agent before it acts, and sensors, which check after. Start with checks that give the same answer every time, such as tests and linters, and add a second model as reviewer only where no fixed check exists.

- [chrome-devtools-mcp](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/chrome-devtools-mcp/): mostly simple. Shows the agent the browser's console and network, so it can see what its change did.
- [planning-with-files](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/planning-with-files/): mostly simple. Plans kept in files, with a fixed completion check.
- [Symphony](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/symphony/): headless autonomy, resumable recovery, complex. Runs one task many times in isolation and surfaces the runs that pass.
- [agent-qa](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/agent-qa/): headless autonomy, retry recovery, slightly complex. Tests web and mobile apps from plain-language test cases.

Check yours: [claim-check](../skills/claim-check/) finds the times your agent said tests passed without a passing run.

## Memory and state

A new session starts with no memory of the last one, so anything that matters must live outside the model. Anthropic's [write-up on long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) (November 26, 2025) keeps that state in plain files and git: a progress log, a feature list where every feature starts out marked as failing, and a commit at the end of each session. The next session reads them before it changes anything. The [memory layers comparison](memory-layers.md) goes deeper.

- [claude-mem](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/claude-mem/): slightly complex. Records what the agent did and feeds the useful part into later sessions.
- [Mem0](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/mem0/): slightly complex. A memory layer for facts about users, teams, and sessions.
- [beads](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/beads/): mostly simple. Keeps decisions and task state outside the agent, so they survive resets and model swaps.
- [letta](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/letta/): headless autonomy, durable recovery, mostly simple. An agent runtime with long-term memory built in.

## Recovery after a crash

Runs die: rate limits, crashed sandboxes, closed laptops. Recovery decides whether the agent starts over, retries the step, resumes the session, or continues from saved state even after a restart, which this list calls durable. Those Anthropic agents use git to undo a bad change and run a quick end-to-end test before new work, so a half-finished session gets fixed first. This is where the list is thinnest: of the 52 projects built to run with nobody watching, 22 can only start over or retry a step, and just 5 are durable.

- [LangGraph](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/langgraph/): headless autonomy, durable recovery, slightly complex. Saves checkpoints so a workflow survives restarts.
- [Cloudflare Agents](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/agents-2/): headless autonomy, durable recovery, slightly complex. Agents that keep their state on Cloudflare.
- [QM](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/qm/): headless autonomy, durable recovery, complex. Y Combinator's shared work agent, with sessions and its work queue in a database.
- [n8n](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/n8n/): headless autonomy, durable recovery, complex. A self-hosted workflow engine with AI steps.

## Observability

Observability means seeing inside a run, for you and for the agent. OpenAI gave each copy of the app its own short-lived logs, metrics, and traces that Codex could search, so a goal such as startup under 800 milliseconds became one the agent could check itself. For people, tracing tools record every step and tool call, so you can find where a run went wrong and what it cost.

- [Langfuse](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/langfuse/): slightly complex. Traces, evaluations, and cost numbers for agent runs.
- [Arize Phoenix](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/phoenix/): slightly complex. Tracing and evaluations that run on your own laptop or servers.
- [Opik](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/opik/): slightly complex. Tracing, scoring, and experiment comparison, free to host yourself.

Check yours: [session-waste-report](../skills/session-waste-report/) shows which agent habits cost the most, and [runaway-guard](../skills/runaway-guard/) stops a session that loops, keeps failing, or passes a dollar limit.

## Measuring the harness

Every change to the harness is a guess until you measure it. LangChain's [Better Harness recipe](https://www.langchain.com/blog/better-harness-a-recipe-for-harness-hill-climbing-with-evals) (April 8, 2026) changes one thing at a time and keeps a change only if new test tasks pass and no old one breaks, then confirms the gain on tasks held back from tuning. Measure with the model you will use: [Harness-Bench](https://arxiv.org/abs/2605.27922) (May 2026) found that results depend on the pairing of model and harness.

- [SWE-bench](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/swe-bench/): headless autonomy, resumable recovery, slightly complex. Real GitHub issues; the standard test for coding agents.
- [Terminal-Bench](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/terminal-bench/): headless autonomy, no recovery, slightly complex. Hard terminal tasks, scored from start to finish.
- [inspect_ai](https://ryanalberts.github.io/best-of-Agent-Harnesses/h/inspect_ai/): headless autonomy, resumable recovery, complex. A framework for your own test tasks and scoring.

Check yours: [harness-test-drive](../skills/harness-test-drive/) runs Claude Code, Codex, and Gemini CLI on tasks from your own git history ([full trial](how-to-test-drive-a-harness.md)).

## Harness engineering vs picking a framework

Picking a framework is a one-time choice of runtime: LangGraph or crewAI, Codex or Cline. Harness engineering is the work that continues after the pick: every rule, check, tool, and limit you add because the agent got something wrong. Böckeler draws the same line between the harness built into a coding agent and the outer harness its users build. The pick still matters: the runtime sets the ceiling on autonomy and recovery, and rule files cannot add recovery a runtime lacks. Most of the outer harness moves with you: AGENTS.md files, skills, MCP tools, and test tasks work across runtimes, so keep them in plain files.

## Where to go next

To choose the runtime, start with [How to pick a harness](how-to-pick-a-harness.md): six questions that cut this list to two or three candidates. To let your coding agent do the lookup, add the [MCP server](../mcp/): `claude mcp add agent-harnesses -- uvx agent-harnesses-mcp`. Its `pick_harness` tool filters by the same ratings used on this page.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). Sources checked 2026-10-23; counts from the list's data of 2026-10-18. Corrections: open an issue with the primary link._

_Agents can query this page's data directly: `claude mcp add agent-harnesses -- uvx agent-harnesses-mcp` ([MCP server](../mcp/))._
