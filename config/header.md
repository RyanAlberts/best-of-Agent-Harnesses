<!-- markdownlint-disable -->
<h1 align="center">
    Best of Agent Harnesses and Harness Techniques
    <br>
</h1>

<p align="center">
    <strong>🏆&nbsp; Curated list of AI agent harnesses, orchestration frameworks, and harness techniques for reliable agentic systems.</strong>
</p>

<p align="center">
    <a href="#contents" title="Project Count"><img src="https://img.shields.io/badge/projects-169-blue.svg?color=5ac4bf"></a>
    <a href="#contribution" title="Contributions welcome"><img src="https://img.shields.io/badge/contributions-welcome-green.svg"></a>
    <a href="https://github.com/RyanAlberts/best-of-Agent-Harnesses/commits/main" title="Updates"><img src="https://img.shields.io/github/last-commit/RyanAlberts/best-of-Agent-Harnesses?color=green&label=updated"></a>
</p>

## What is an agent harness?

A model answers; an agent acts. An agent harness is the runtime that turns one into the other: the model thinks, the harness decides what that thinking is allowed to touch.

Simon Willison's definition of the agent itself is the cleanest: "an LLM agent runs tools in a loop to achieve a goal" (simonwillison.net). The harness is everything around that loop: which tools exist, what needs approval, what the model sees each turn, what survives a crash. Andrej Karpathy named the architecture back in 2023: the model is "the kernel process of a new Operating System", and the harness is the rest of that OS, its scheduler, permissions, and memory. The SWE-agent paper (arXiv:2405.15793) proved the stakes by coining the agent-computer interface: how tools and feedback are presented changes what a model can do, independent of the model. The field's advice has since converged on investing here rather than in framework plumbing, from Anthropic's build-simple guidance to Jerry Liu's argument that the framework era is over and the layers that matter now are skills, tools, and context quality. Those are the layers this list catalogs.

If you want to add or update projects, open an [issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues), submit a [pull request](https://github.com/RyanAlberts/best-of-Agent-Harnesses/pulls), or edit [projects.yaml](https://github.com/RyanAlberts/best-of-Agent-Harnesses/blob/main/projects.yaml). Contributions are welcome!
