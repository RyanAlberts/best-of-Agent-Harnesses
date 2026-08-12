# Eval and observability platforms: Langfuse vs LangSmith vs Braintrust vs Phoenix

Benchmarks tell you how a model ranks; your production agent still fails in ways no public exam covers. An eval and observability platform is where teams watch what their agent actually did (tracing: recording every step, tool call, and token of a run) and score it continuously (evals: checks that run on those traces, in CI or on live traffic). This is also where the eval budget actually gets spent, which makes it the most-compared purchase in the whole evaluation space. Our [Agent evals](agent-eval-harnesses.md) page covers the open-source benchmarks and frameworks one layer down.

| | [Langfuse](https://github.com/langfuse/langfuse) | [LangSmith](https://www.langchain.com/langsmith) | [Braintrust](https://www.braintrust.dev/) | [Phoenix](https://github.com/Arize-ai/phoenix) |
|---|---|---|---|---|
| What it is | Open-source tracing, evals, and prompt management in one platform | LangChain's commercial platform for the full agent lifecycle | Eval-first platform: versioned datasets, scoring, CI release gates | Arize's local-first tracing and eval layer, with managed Arize AX above it |
| Open source? | Yes: MIT core (33k stars; enterprise folders separately licensed) | No: closed platform, open client SDK only | No: closed platform, open SDKs only | Source-available: Elastic License 2.0 (11k stars), self-hostable but not OSI open source |
| Self-hosting | Free, first-class (Docker Compose, Helm) | Enterprise-only, paid | Enterprise-only, paid | Free, local-first by design |
| Center of gravity | Traces first, evals on top | Lifecycle: tracing, evals, deployment, tuned for LangChain/LangGraph | Scores first: "what reaches production" gates | Traces and experiments, on your own machine |
| Free tier (checked 2026-08-12) | Hobby cloud: 50k units/month, plus unlimited free self-host ([pricing](https://langfuse.com/pricing)) | Developer: 5k traces/month, 1 seat ([pricing](https://www.langchain.com/pricing)) | Starter: $10 credits, 14-day retention ([pricing](https://www.braintrust.dev/pricing)) | Self-host free with no event caps; managed AX from $0 ([pricing](https://arize.com/pricing/)) |
| Steward | Langfuse, acquired by [ClickHouse in January 2026](https://clickhouse.com/blog/clickhouse-acquires-langfuse-open-source-llm-observability) | LangChain | Braintrust | Arize AI |

_No star row here because two of the four have no open-source core to count. Langfuse, Phoenix, and Opik (below) carry entries in this list's [observability category](../README.md#observability-and-eval-ops)._

## Pick by situation

The vendors' own head-to-head pages, read against each other, agree more than you'd expect:

- **You want open source, self-hosting, and predictable cost** → **Langfuse**. The cleanest open-source credential of the four (MIT core) and the one whose [own positioning](https://langfuse.com/faq/all/best-phoenix-arize-alternatives) leads with exactly that. The cost gap it advertises is real but dated: a widely cited mid-2026 calculation put a million events near [$101/month on Langfuse Core against roughly $2,514/month on LangSmith Plus](https://www.morphllm.com/comparisons/langfuse-vs-langsmith); the units aren't equivalent and LangSmith's pricing model has since changed, so treat that as an order-of-magnitude signal, not current math.
- **You build on LangChain or LangGraph** → **LangSmith**. First-party tracing for that stack with the least integration work; [LangChain's own comparison](https://www.langchain.com/resources/langsmith-vs-langfuse) pitches it as covering the full lifecycle. The trades: closed platform, and self-hosting is an Enterprise feature, not an option you can default to.
- **Evals gate your releases** → **Braintrust**. Its bet is that scoring, not tracing, is the product: versioned datasets, experiments, and regression gates deciding what ships. [Its own LangSmith comparison](https://www.braintrust.dev/articles/langsmith-vs-braintrust) draws the same line. Closed platform; on-prem is Enterprise-only.
- **You want tracing on your laptop before you buy anything** → **Phoenix**. Local-first and free to self-host with no event caps; [Arize's framing](https://arize.com/pricing/) is stay local, graduate to the managed AX platform when you outgrow it. Mind the license: Elastic 2.0 is source-available, not open source, and restricts reselling Phoenix as a hosted service.

The fifth name that keeps appearing in these comparisons: [Opik](https://github.com/comet-ml/opik) (Comet, 21.3k stars, Apache-2.0), whose whole core feature set is free to self-host under a plain open-source license; the pick when Langfuse's enterprise-folder split bothers you.

## How this layer relates to the benchmarks

These platforms score *your* traffic continuously; benchmark frameworks like [SWE-bench and inspect_ai](agent-eval-harnesses.md) score fixed task sets once. Mature setups use both: a benchmark to choose the base model, a platform to catch the regressions your users would otherwise find. Dev-time eval libraries (promptfoo, DeepEval, Ragas) plug into either layer; worth knowing that [OpenAI acquired promptfoo in March 2026](https://openai.com/index/openai-to-acquire-promptfoo/), which has non-OpenAI teams re-checking their neutrality assumptions.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). New to this decision? Start with [How to pick a harness](how-to-pick-a-harness.md). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._

_Agents can query this page's data directly: `claude mcp add agent-harnesses -- uvx agent-harnesses-mcp` ([MCP server](../mcp/))._
