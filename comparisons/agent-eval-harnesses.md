# Agent eval harnesses: SWE-bench vs inspect_ai vs AgentBench

"Evaluate my agent" hides two different products. A benchmark is a fixed exam with a leaderboard: SWE-bench and AgentBench tell you where a model or harness ranks against the field, on tasks someone else wrote. An eval framework is tooling for writing your own exam: inspect_ai measures your agent on your tasks. Star counts mislead in this category; these are small repos and load-bearing standards at the same time.

| | [SWE-bench](https://github.com/SWE-bench/SWE-bench) | [inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai) | [AgentBench](https://github.com/THUDM/AgentBench) |
|---|---|---|---|
| ⭐ Stars | 5.6k | 2.5k | 3.7k |
| Shape | Benchmark: real GitHub issues + Docker harness | Eval framework: composable tasks, scorers, sandboxes, multi-model runs | Benchmark: multi-environment suite (OS, DB, knowledge graphs, webshop, AlfWorld) |
| The question it answers | Can this agent resolve real GitHub issues? | Whatever question you write a task for | How does this LLM perform as a general agent across domains? ([ICLR'24 paper](https://arxiv.org/abs/2308.03688)) |
| Steward | SWE-bench org | UK AI Security Institute (AISI) | THUDM (Tsinghua) |
| Maintenance (checked 2026-08-12) | Active | Active | Quiet since February 2026 |
| License | MIT | MIT | Apache-2.0 |
| Autonomy (list axis) | headless | headless | headless |
| Recovery (list axis) | resumable | resumable | none |
| Adoption surface (list tier) | slightly complex | complex (product suite) | complex (product suite) |

_Stars as captured for the main list (see [README](../README.md#guide-to-rankings) for the capture date)._

## Pick by situation

- **You build a coding agent and want a number the field respects** → **SWE-bench**. Real GitHub issues resolved inside a Docker harness; the [Verified leaderboard](https://www.swebench.com/verified.html) is the score every coding-agent launch cites. Its siblings extend the line: [SWE-smith](https://github.com/SWE-bench/SWE-smith) generates training data (50k+ instances across 128 repos), and [SWE-agent](https://github.com/SWE-agent/SWE-agent) is the reference harness built against the benchmark.
- **You ship an agent product and need to measure it before users do** → **inspect_ai**. The framework behind the UK AISI's evaluations: you write tasks, attach scorers (rule-based or model-graded), and run them sandboxed across models. [inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals) adds ready-made suites (GAIA and others) when you want standard tasks inside the same tooling.
- **You research general agent ability across domains** → **AgentBench**. Environments from OS shells to web shops in one Docker Compose suite; the ICLR'24 landmark of the genre. The repo has been quiet since February 2026, so treat it as a reference exam rather than a live target.

## Benchmark scores are not your eval

A leaderboard number tells you how a model plus its harness performed on someone else's tasks at some point in the past. Two cautions follow. Fixed public exams age: their tasks live on the internet models train on, and a quiet benchmark (see the maintenance row) no longer patches what the field learns to exploit. And your product fails in ways no public suite covers. The durable setup is a benchmark for choosing your base model, plus a framework like inspect_ai holding the tasks only you can write. For the gaps between these three, [AgencyBench](https://github.com/GAIR-NLP/AgencyBench) covers long-horizon work (~1M tokens, ~90 tool calls per scenario) and [WebArena](https://github.com/web-arena-x/webarena) covers end-to-end web tasks.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). New to this decision? Start with [How to pick a harness](how-to-pick-a-harness.md). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._
