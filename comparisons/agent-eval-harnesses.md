# Agent evals: SWE-bench vs inspect_ai vs Terminal-Bench

You changed your agent: new model, new prompt, new tools. Did it get better or worse? An eval is how you answer that with a number instead of a feeling. The word covers two different products, and knowing which one you need is most of the decision. A **benchmark** is a fixed public exam with a leaderboard: it tells you how a model or agent ranks against the field on tasks someone else wrote. An **eval framework** is a test runner for exams you write yourself: it tells you whether your agent works on your tasks. SWE-bench and Terminal-Bench are benchmarks; inspect_ai is a framework.

Why it matters: shipping on a public number alone has burned people. OpenAI [stopped reporting SWE-bench Verified results](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) after an audit found flawed test cases in a majority of the problems it sampled, and the loudest threads in this space are about [benchmark exploits](https://news.ycombinator.com/item?id=47733217), not benchmark scores.

| | [SWE-bench](https://github.com/SWE-bench/SWE-bench) | [inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai) | [Terminal-Bench](https://github.com/harbor-framework/terminal-bench) |
|---|---|---|---|
| ⭐ Stars | 5.6k | 2.5k | 482 |
| Shape | Benchmark: real GitHub issues, Docker harness | Framework: write tasks, attach scorers, run sandboxed across models | Benchmark: hard terminal tasks in containers |
| The question it answers | Can this agent fix real reported bugs in real repos? | Whatever question you write a task for | Can this agent do real work in a command-line shell? |
| Steward | The SWE-bench org (Princeton and Stanford researchers) | UK AI Security Institute, the UK government body that tests frontier models | The harbor-framework org |
| Maintenance (checked 2026-08-12) | Active | Active | Active |
| License | MIT | MIT | Apache-2.0 |

_Stars as captured for the main list. Star counts mislead here: these are small repos and field standards at the same time, and Terminal-Bench's count understates it (the same org's 1.0 task repo and its harbor runner hold several thousand more). Rating definitions for this site live in the [guide to rankings](../README.md#guide-to-rankings)._

## Pick by situation

- **You build a coding agent and want a number the field respects** → **SWE-bench**. Real GitHub issues, resolved or not, in a Docker harness. Know the family: [SWE-bench Verified](https://www.swebench.com/verified.html) is the 500-problem human-checked subset every launch cites, and [SWE-bench Pro](https://scale.com/blog/swe-bench-pro) is Scale's harder successor, built partly because the original's tasks have been public long enough to leak into training data.
- **You ship an agent product and need to know it works before users do** → **inspect_ai**. You define tasks, attach scorers (a scorer marks each attempt: either a scripted check or a second model grading the output, called model-graded), and run them in sandboxes across models. It is the framework behind the UK AISI's own evaluations, and [ready-made suites exist](https://github.com/UKGovernmentBEIS/inspect_evals) so you don't start from zero.
- **Your agent lives in a terminal** → **Terminal-Bench**. Containerized command-line tasks scored end to end, with a [public leaderboard](https://www.tbench.ai/leaderboard). This is the benchmark people now weigh [directly against SWE-bench](https://www.digitalapplied.com/blog/swe-bench-terminal-bench-benchmark-guide-2026) when the work is broader than fixing GitHub issues.

## A score is the model plus the harness

The same model produces different scores depending on the agent software (the harness) that drives it: one tracking site shows [Claude Opus 4.5 scoring 73.2 to 77.6 on SWE-bench Verified](https://tensorfeed.ai/harnesses/openhands) depending on whether SWE-agent, mini-SWE-agent, or OpenHands runs it. So read every leaderboard number as a stack number, not a model number, and when you compare your own runs, hold the harness constant. [SWE-agent](https://github.com/SWE-agent/SWE-agent) exists exactly for this: the reference harness published next to the benchmark.

## When the number lies

Three failure modes to check before trusting any benchmark score. **Aging**: public tasks end up in training data, so old exams flatter new models. **Broken tests**: OpenAI's audit found the majority of sampled SWE-bench Verified problems could be "solved" for the wrong reasons. **Gaming**: a [588-point Hacker News study](https://news.ycombinator.com/item?id=47733217) showed the major agent benchmarks can be exploited outright. This is also where AgentBench belongs now: the [ICLR 2024](https://arxiv.org/abs/2308.03688) benchmark (ICLR is a major machine-learning conference) that first scored LLMs as agents across eight environments, from OS shells to web shops. Its [leaderboard has run cold since 2025](https://benchmarkingagents.com/agentbench/), so treat it as the field's history, not a live target. For gaps these three don't cover, [AgencyBench](https://github.com/GAIR-NLP/AgencyBench) tests long tasks (about a million tokens and ninety tool calls per scenario) and [WebArena](https://github.com/web-arena-x/webarena) tests end-to-end web work.

## The adjacent purchase

Everything on this page is open source. The place money changes hands in evals is one layer up: hosted platforms that trace what your agent did in production and score it continuously. That decision, the most-compared purchase in the whole space, gets its own guide: [Eval and observability platforms](eval-platforms.md) (Langfuse vs LangSmith vs Braintrust vs Phoenix).

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). New to this decision? Start with [How to pick a harness](how-to-pick-a-harness.md). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._

_Agents can query this page's data directly: `claude mcp add agent-harnesses -- uvx agent-harnesses-mcp` ([MCP server](../mcp/))._
