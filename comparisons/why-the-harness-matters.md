# Why the harness matters more than the model

The same model weights score about 30% on ARC-AGI-3 as a bare model and 95.5% inside a good harness, and that gap is the number agent builders keep quoting. This page collects who says the harness matters more than the model, what each of them measured, and what the claim does not mean.

[![YC Paper Club: Why the harness matters more than the model (video, 60 minutes)](https://i.ytimg.com/vi/n9xKblqyQ28/hqdefault.jpg)](https://www.youtube.com/watch?v=n9xKblqyQ28)

_Y Combinator's Paper Club session of September 7, 2026, with the authors of Prime Agent, OpenJarvis, and QM. One hour; the history of harnesses runs from 7:00 to 17:00._

## The claim

A model answers; an agent acts. The harness is the runtime that turns one into the other ([definition](../README.md#what-is-an-agent-harness)): the tool list, the approval rules, what the model sees each turn, what survives a crash, and, since 2026, what the agent is allowed to change about itself. "The harness matters more than the model" is shorthand for a measurable fact: hold the weights fixed, change only the harness, and benchmark scores move more than most model upgrades move them.

## The measurements

- **ARC-AGI-3, same weights, 30% to 95.5%.** A bare frontier model was verified at about 30% on the private ARC-AGI-3 set. [Prime Agent](https://arxiv.org/abs/2608.23552), a self-improving harness from Prime Intellect, reached 95.5% with Opus 5, above the reported human-expert baseline. The [YC talk](https://www.youtube.com/watch?v=n9xKblqyQ28) walks through the runs at 30:00, and the host adds that an NVIDIA harness has since reported 100%.
- **SWE-bench Pro, harness-only swap, 23% to 52%.** [@joelniklaus](https://x.com/joelniklaus/status/2085725862142623875) held the model fixed and changed the harness: GLM-5.2 went from 23% to 52% pass@1, and Gemma 4 26B from 15% to 36%. Latent Space's summary: swapping the harness "changed pass@1 more than many model upgrades do" ([AINews, Aug 8 2026](https://www.latent.space/p/ainews-zawinskis-law-of-multiagents)).
- **Cursor's benchmark, 46% to 80%.** [Cursor's benchmarking research](https://www.mindstudio.ai/blog/agent-harness-scaffolding-matters-more-than-model) found the same model passing 46% of tasks in one harness and 80% in another.
- **Rankings do not transfer.** [Harness-Bench](https://arxiv.org/abs/2605.27922) measured a rank correlation of about -0.05 between harness rankings on different models. The best harness for one model says almost nothing about the best harness for another.
- **Harness search beats hand design.** [Meta-Harness](https://arxiv.org/abs/2603.28052), from Stanford's IRIS lab, searched over harness code end to end and beat a state-of-the-art context manager by 7.7 points while using four times fewer context tokens.
- **Two harnesses, identical weights, 18 points apart.** The YC host's opening slide (1:00) shows an 18% gap between two harnesses on the same weights, the number he uses to answer the claim that harness work is not research.

The chart that opens the [decision guide](how-to-pick-a-harness.md#the-chart-to-internalize-first) plots the coding-benchmark spreads.

## Who says so

| Who | Role | What they say | Evidence | Source | Date |
|---|---|---|---|---|---|
| Y Combinator Paper Club | talk | Harnesses were "belittled as subpar research"; the numbers say otherwise | measurement, practitioner | [video](https://www.youtube.com/watch?v=n9xKblqyQ28) | 2026-09 |
| Prime Intellect (Seth Karten et al.) | paper | Prime Agent: 95.5% on ARC-AGI-3 with Opus 5 through a recursive-language-model harness | measurement | [arXiv:2608.23552](https://arxiv.org/abs/2608.23552), [blog](https://www.primeintellect.ai/blog/prime-agent) | 2026-08 |
| Karten et al., Continual Harness | paper | The agent edits its own prompt, skills, memory, and sub-agents mid-episode | paper | [arXiv:2605.09998](https://arxiv.org/abs/2605.09998) | 2026-05 |
| Stanford IRIS (Lee, Finn et al.), Meta-Harness | paper | End-to-end search over harness code: +7.7 points, four times fewer context tokens | measurement | [arXiv:2603.28052](https://arxiv.org/abs/2603.28052) | 2026-03 |
| Harness-Bench | paper | Harness rankings barely transfer across models (rank correlation about -0.05) | measurement | [arXiv:2605.27922](https://arxiv.org/abs/2605.27922) | 2026-05 |
| @joelniklaus | practitioner analysis | SWE-bench Pro: 23% to 52% and 15% to 36% from the harness alone | measurement | [x.com](https://x.com/joelniklaus/status/2085725862142623875) | 2026-08 |
| Cursor (via MindStudio) | vendor benchmark | Same model, 46% in one harness, 80% in another | measurement | [write-up](https://www.mindstudio.ai/blog/agent-harness-scaffolding-matters-more-than-model) | 2026 |
| Endor Labs | practitioner report | Claude Fable 5: same model, different harness, very different result | measurement | [post](https://www.endorlabs.com/learn/claude-fable-5-take-two-same-model-different-harness-and-a-very-different-result) | 2026-06 |
| SWE-agent (Princeton) | paper | Coined the agent-computer interface: how tools are presented changes what a model can do | paper | [arXiv:2405.15793](https://arxiv.org/abs/2405.15793) | 2024-05 |
| Anthropic | lab guidance | Effective harnesses for long-running agents; build simple before you build frameworks | lab guidance | [long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), [building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | 2024-2026 |
| OpenAI | lab guidance | "Harness engineering": environment design, feedback loops, the repo as system of record | lab guidance | [post](https://openai.com/index/harness-engineering/) | 2026 |
| LangChain (Harrison Chase, Vivek Trivedy) | lab guidance | Better Harness: hill-climb the harness with evals as the training signal | lab guidance | [post](https://blog.langchain.com/better-harness-a-recipe-for-harness-hill-climbing-with-evals/), [Chase](https://x.com/hwchase17/status/2041929684741747171) | 2026-04 |
| Andrej Karpathy | practitioner | The model is "the kernel process of a new Operating System"; the harness is the rest of the OS | practitioner | [x.com](https://x.com/karpathy/status/1707437820045062561) | 2023-09 |
| Karpathy's autoresearch, field reports | practitioner | Overnight research loops lived or died on harness affordances, not raw model quality | practitioner | [repo](https://github.com/karpathy/autoresearch), [AINews](https://www.latent.space/p/ainews-autoresearch-sparks-of-recursive) | 2026-03 |
| Simon Willison | practitioner | "An LLM agent runs tools in a loop to achieve a goal"; the harness is everything around the loop | definition | [post](https://simonwillison.net/2025/Sep/18/agents/) | 2025-09 |
| swyx, Latent Space | practitioner | Asked "Is Harness Engineering real?", then declared "Meta-Harness Summer" | practitioner | [AINews](https://www.latent.space/p/ainews-is-harness-engineering-real) | 2026 |
| Jerry Liu (LlamaIndex) | practitioner | The framework era is over; what matters now is skills, tools, and context quality | practitioner | [VentureBeat](https://venturebeat.com/infrastructure/the-ai-scaffolding-layer-is-collapsing-llamaindexs-ceo-explains-what-survives) | 2026 |
| Aakash Gupta | commentary | "2025 was agents, 2026 is agent harnesses" | commentary | [Medium](https://aakashgupta.medium.com/2025-was-agents-2026-is-agent-harnesses-heres-why-that-changes-everything-073e9877655e) | 2026 |
| Awesome-Agent-Harness survey | survey | 110+ papers and 23 systems organized into a harness taxonomy | paper | [GitHub](https://github.com/Gloriaameng/Awesome-Agent-Harness) | 2026 |
| The 2026 explainer wave | commentary | "The harness matters more than the model" as a blog genre | commentary | [Medium](https://medium.com/@Micheal-Lanham/building-agents-in-2026-why-the-harness-matters-more-than-the-model-eb72448fee04), [dev.to](https://dev.to/max_quimby/harness-engineering-the-developer-skill-that-matters-more-than-your-ai-model-in-2026-47ke), [Tencent Cloud](https://www.tencentcloud.com/techpedia/147786?lang=en), [Infralovers](https://www.infralovers.com/blog/2026-03-13-harness-engineering-rahmen-wichtiger-als-modell/) | 2026 |

Measurement rows are the evidence; commentary rows show how far the claim has spread. Every link was checked on 2026-09-14. Missing an authority? Open an issue with the primary source.

## What the claim does not mean

The YC talk adds the nuance the slogan drops. Timestamps point into [the video](https://www.youtube.com/watch?v=n9xKblqyQ28).

1. **Two eras, and the gains are in the second one.** The static harness (7:00 to 13:00) ran from GPT-2's sampling loop in 2019 through few-shot prompts, chain of thought, tools, editable memory, skills, reflection, sub-agents, and recursive language models: a fixed program around a fixed model. The self-improving harness (14:00 to 17:00) lets the agent change its own prompt ([DSPy](https://github.com/stanfordnlp/dspy), [GEPA](https://arxiv.org/abs/2507.19457)), its own code ([Darwin Gödel Machine](https://arxiv.org/abs/2505.22954)), or its whole harness state ([Continual Harness](https://arxiv.org/abs/2605.09998), [Meta-Harness](https://arxiv.org/abs/2603.28052)). The recent jumps come from the second era.
2. **More harness is not the claim. The right harness is.** YC's QM runs on three core tools and calls itself an "AGI-anticipating harness" (57:00). Prime Agent's rule (25:00) is to expose what the model cannot do for itself, such as compaction, a persistent REPL, and programmatic sub-agents, and to drop imposed procedure like fixed plan-act-critique loops, which models now run on their own.
3. **The harness is a cost lever, not only a score lever.** One popular harness spent about $5,000 on ARC-AGI-3 without progress before the run was cut off (33:00), while Prime Agent finished the set. Working on context programmatically, instead of stuffing it into the prompt, is what saved the money.
4. **Long-horizon failure is a harness problem.** Agents "give up way too early" (57:30), so QM sets wall-clock and token budgets on goals and will not let the agent quit before the budget is spent. The QM team notes that OpenAI and Anthropic used a similar technique on open math problems.
5. **Automatic self-improvement still needs a person in the loop.** QM's team tried hill-climbing on their trace set and hit "main character syndrome" (53:00): each agent fixes the piece of the elephant it can see.
6. **It is a pairing, not a winner.** Because rankings barely transfer across models, "best harness" only means something for a given model, and the choice must be re-asked whenever the model changes.

## What to do about it

- Pick the harness with the same care as the model, and re-pick when the model changes. The [six questions](how-to-pick-a-harness.md) turn this list into that decision; the [two-week test drive](how-to-test-drive-a-harness.md) checks it on your own repos.
- Treat the harness as a first-class variable in every benchmark you read or run. A score without the harness named is half a number.
- Budget long-horizon runs explicitly: wall-clock time and tokens, per goal.
- Prefer thin harnesses that expose capabilities over thick ones that impose procedure, and expect the right amount of harness to shrink as models improve.
- Let your agent choose. The [MCP server](../mcp/) in this repo exposes `recommend` and `pick_harness`, so a coding agent can pick a harness matched to its model and task instead of inheriting whichever one someone else benchmarked.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). Corrections and missing sources: open an issue with the primary link._

_Agents can query this page's data directly: `claude mcp add agent-harnesses -- uvx agent-harnesses-mcp` ([MCP server](../mcp/))._
