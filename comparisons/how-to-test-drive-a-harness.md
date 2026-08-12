# How to test-drive a harness

Spec sheets cannot answer "which harness should I use," because an agent's performance is a property of the *pairing* between harness and model, not of either alone: the same model passes [46% of tasks in one harness and 80% in another](https://www.mindstudio.ai/blog/agent-harness-scaffolding-matters-more-than-model) in Cursor's benchmarking research, harness swaps moved [SWE-bench Pro scores by 21 to 29 points](https://x.com/joelniklaus/status/2085725862142623875), and harness rankings barely transfer between models (rank correlation about -0.05). Public benchmarks don't rescue you either: OpenAI [stopped reporting SWE-bench Verified](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) after auditing its tasks, and a leaderboard position measures someone else's repos, not yours. The only comparison that transfers to your work is running your work. This page is the protocol: an afternoon to set up, about two weeks to run, numbers at the end.

## Step 1: shortlist two or three, no more

Use [How to pick a harness](how-to-pick-a-harness.md) and the [use-case index](../README.md#pick-by-use-case) to get to 2-3 candidates. Trialing more than three divides your task set until no candidate gets enough data; the decision guides exist so you don't have to trial five.

## Step 2: make the race fair

- **Hold the model constant where you can.** If both harnesses accept the same model, use it, so you're measuring the harness. Where a candidate is first-party-only, accept the confound and write it down: you're comparing stacks, not harnesses.
- **Port your instructions once.** Write one AGENTS.md briefing and give every candidate the same one (the [terminal-agents guide](terminal-coding-agents.md) covers the two tools that need a setting flipped). Same MCP tools on each side.
- **Pin versions and write them down.** The pairing you test is the pairing you ship; harnesses ship weekly and behavior moves.
- **Fresh git worktree per candidate per task**, so no candidate inherits another's leftovers.
- **Define what "pass" means per task before running anything.** Written down, so the goalposts can't move after you've seen an output you like.

## Step 3: build the task set from your own work

Generic prompts measure nothing. The [error-analysis-first rule](https://www.lennysnewsletter.com/p/building-eval-systems-that-improve-your-ai-product) from Hamel Husain and Shreya Shankar's eval playbook applies fully here: you can't know what to test until you look at how work actually fails in your shop. The practical version is a golden-replay set, [pulled from your own recently merged work](https://futureagi.com/blog/evaluating-coding-agents-2026/): take 8-12 real, completed tasks from the last month (merged PRs, closed tickets) where you know what good looked like. Cover the spread:

- one small bugfix and one multi-file feature (the bread and butter)
- one refactor with tests (does it keep them green or delete them?)
- one question about unfamiliar code (comprehension, not generation)
- one long task that will blow past a single context window (compaction behavior)
- one task with destructive potential, run deliberately (does the permission model catch it?)

## Step 4: measure these seven things

The 2026 harness-effects research ([Harness-Bench](https://arxiv.org/abs/2605.27922)) scores configurations on success, token cost, robustness, and traceability; the columns below are that list extended with the two things buyers report caring about most, integration friction and exit cost.

| Dimension | Record per task | Why it predicts |
|---|---|---|
| Output quality | Human accept / accept-with-rework / reject | The only score that matters. Never let the agent grade itself: [one builder's overnight run](https://x.com/Skaly__Bull/status/2087662420672332087) self-passed 31 of 40 tasks; a human reading the same outputs passed 18 |
| Interventions | Times you had to redirect mid-task | The real autonomy number, whatever the marketing says |
| Plan drift | Did the final diff match the stated plan? | Catches harnesses that narrate one thing and do another |
| Wall-clock | Minutes per accepted task | Latency compounds across a team |
| Cost | Dollars per *accepted* task, not per token | Cheap tokens on rejected work is expensive work; note the bill shape too ([question 5](how-to-pick-a-harness.md)) |
| Robustness | Kill it mid-task; note what resumes | The recovery axis, observed instead of read |
| Setup friction | Minutes from clean machine to first accepted task, plus MCP/tool wiring effort | The adoption-surface tier, observed instead of read |

## Step 5: score against your own baseline

Absolute scores mean little; compare against how the same work goes without the candidate. Your repo already knows your baseline: time-to-merge, acceptance rate, and rework rate for recent human-authored changes. [A two-week trial with three to five engineers on real tickets](https://ucstrategies.com/news/autonomous-coding-agents-evaluation-framework/) produces enough accepted-task data for a fair comparison; a solo trial needs the full task set above instead.

Copy-paste scorecard:

```
| Task | Pass criteria | Harness A: verdict / interventions / min / $ | Harness B: verdict / interventions / min / $ |
|------|---------------|----------------------------------------------|----------------------------------------------|
| 1.   |               |                                              |                                              |
```

## The walk-away test

Before deciding, run one more test on the *winner*: export what you built during the trial (the briefing file, any skills, memory, traces) and time how long it takes to make the runner-up work with it. That number is your future switching cost, and it's the practical version of the [vendor-decoupling argument](progressive-disclosure.md): instructions, skills, memory, and tools should outlive any one harness or model, which is exactly why they belong in open formats. LangChain's Harrison Chase has argued the same from the other side: harness configuration is model-specific tuning, so when your model changes, the trial needs re-running, and portable assets are what make the re-run cheap.

## Pitfalls, all field-reported

- **The novelty window.** The first week flatters every new tool. The second week is where update churn and permission fights show up; the [OpenClaw vs Hermes field reports](openclaw-vs-hermes.md) found release breakage, not capability, was the top reason people switched.
- **Leaderboard transfer.** A 70% benchmark score doesn't survive contact with your repo's conventions; that's what [Agent evals](agent-eval-harnesses.md) calls the model-plus-harness problem, and it's why this page exists.
- **Grading your own homework.** Applies to the humans too: whoever ran the trial wants their favorite to win, so have a second person judge accept/reject on the diffs alone.
- **Deciding on price-per-token.** The spread that matters is dollars per accepted task; a harness that's 20% pricier per token and 40% better on acceptance is the cheap one.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). New to this decision? Start with [How to pick a harness](how-to-pick-a-harness.md). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._

_Agents can query this page's data directly: `claude mcp add agent-harnesses -- uvx agent-harnesses-mcp` ([MCP server](../mcp/))._
