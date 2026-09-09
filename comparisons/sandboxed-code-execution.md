# Agent sandboxing: what it is and how to pick

An AI agent does not just suggest code. It runs code, opens web pages, and edits files on a real computer. Agent sandboxing means making that computer a disposable one, so that when the agent makes a mistake, or a malicious web page talks it into one, the damage lands in a box you can throw away instead of on your laptop or your production servers. In August 2026 [an agent hacked a gym's booking system](https://www.bbc.com/news/articles/cn0nww2qlp7o) to get its user into a full pilates class; nobody asked it to. Docker's answer to the category, launched the same month to a [687-point Hacker News thread](https://news.ycombinator.com/item?id=49239751), was pitched as the fix for "what happens when the agent does something you didn't ask for."

This page gives you the concepts first, because the products only make sense once you have them. Then it compares the field.

## The problem, in one sentence

You are combining untrusted code with a trusted machine. The untrusted code comes from two places: the model itself, which writes and runs programs nobody reviewed, and the internet, because any web page or file an agent reads can contain instructions that steer it (this is called prompt injection). The fix is the same for both: give the agent its own machine.

## Two different jobs share the name "sandboxing"

Vendors use one word for two different products, and most confusion in this space traces back to that. A [widely shared ranking thread on r/AI_Agents](https://old.reddit.com/r/AI_Agents/comments/1sh2x4p/i_compared_sandbox_options_for_ai_agents_heres_my/) landed on the same conclusion: "best sandbox" depends on which job you mean.

1. **Sandbox the agent.** The whole agent program runs inside the box: it can only see and break what the box contains. This is what [Docker Sandboxes](https://www.docker.com/products/docker-sandboxes/) does for Claude Code, Codex CLI, Copilot CLI, and Gemini CLI, and what [Agent Sandbox](https://github.com/kubernetes-sigs/agent-sandbox) does on Kubernetes.
2. **Give the agent a sandbox.** The agent runs wherever it already runs, and gets a disposable remote computer as a tool for executing the code it writes. This is E2B's and Modal's product, often called a code interpreter.

Careful setups do both: the thread's author runs generated code in a sandbox even when the agent itself is already in one.

## The concepts that decide the pick

- **Isolation boundary.** How hard is the wall? From weakest to strongest: a process sandbox (tools like bubblewrap restrict what one program can touch; no infrastructure, but the operating system kernel is shared), a container (its own filesystem, still a shared kernel, so a kernel bug is an escape route), a user-space kernel (gVisor, which Modal uses: syscalls hit a decoy kernel first), and a microVM (a lightweight virtual machine with its own kernel and a hardware-enforced boundary; E2B and Vercel Sandbox run Firecracker, the microVM engine built for AWS Lambda, and [Docker built its own equivalent](https://www.docker.com/blog/why-microvms-the-architecture-behind-docker-sandboxes/) so it works on macOS and Windows).
- **Lifecycle.** Agents create and destroy machines constantly, so start-up time is a per-turn tax: [one 2026 benchmark write-up](https://particula.tech/blog/modal-vs-e2b-vs-daytona-vs-vercel-sandbox-ai-code-execution) measured cold starts around 90ms for Daytona and 150ms for E2B. Snapshot and fork let you checkpoint a machine's exact state and branch it; pause and resume lets a long job idle without paying for compute. Warm pools (pre-booted sandboxes waiting for work) are how Kubernetes-based setups dodge the cold start entirely.
- **The network boundary.** The most-missed axis. A sandbox can isolate the filesystem perfectly and still let the code inside open a connection and send your secrets out. Look for outbound-network controls: a domain allowlist at minimum (Docker's Sandbox Kits declare allowed network domains in the sandbox spec), inspection of what is actually sent at best.
- **State.** Does the box keep files and installed packages between turns and sessions, or is every run a fresh machine? Code-interpreter products lean stateless; agent-workspace products lean stateful.
- **Where it runs.** A hosted API (fastest to adopt, someone else's cloud), your own cluster (data stays home, you operate it), or your own laptop (for running coding agents unsupervised locally).

## The field, August 2026

Start with the open-source anchors this list tracks:

| | [E2B](https://github.com/e2b-dev/E2B) | [Daytona](https://github.com/daytonaio/daytona) | [Agent Sandbox](https://github.com/kubernetes-sigs/agent-sandbox) |
|---|---|---|---|
| ⭐ Stars | 13.7k | 71.7k | 3.8k |
| License | Apache-2.0 | ⚠️ AGPL-3.0 at v0.190.0, the final open release | Apache-2.0 |
| Maintenance (checked 2026-08-12) | Active | ⚠️ Unmaintained since June 2026 | Active |

_Stars as captured for the main list (see the [guide to rankings](../README.md#guide-to-rankings), which also defines the autonomy, recovery, and adoption-surface ratings used across this site). None of these three runs an agent loop of its own; they are the floor an agent stands on._

The wider field includes closed products, and in this category they matter. Isolation and deployment claims below come from each vendor's own documentation or the linked write-ups.

| Product | Runs | Isolation | The one thing to know |
|---|---|---|---|
| [E2B](https://github.com/e2b-dev/E2B) | Hosted API (open-source infra) | Firecracker microVMs | The default code-interpreter pick; its [cookbook runs all of Claude Code inside a sandbox](https://github.com/e2b-dev/e2b-cookbook/tree/main/examples/anthropic-claude-code-in-sandbox-python) |
| [Modal](https://modal.com) | Hosted API | gVisor | The pick when the sandbox side needs GPUs; E2B's [most-compared rival](https://northflank.com/blog/e2b-vs-modal) |
| [Daytona](https://github.com/daytonaio/daytona) | Hosted | Containers, optional stronger runtimes | Fastest measured cold starts; ⚠️ public repo unmaintained since June 2026 (below) |
| [Vercel Sandbox](https://vercel.com/docs/vercel-sandbox) | Hosted | Firecracker microVMs | Bills active CPU time rather than sandbox lifetime |
| [Cloudflare Sandboxes](https://developers.cloudflare.com/sandbox) | Hosted (edge) | Containers | Sandboxes next to Workers, for edge-shaped apps |
| [AWS Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/) | Managed, your AWS account | Managed sandbox | The enterprise-AWS answer, code interpreter included |
| [GKE Agent Sandbox](https://cloud.google.com/blog/products/containers-kubernetes/agentic-ai-on-kubernetes-and-gke/) | Your GKE cluster | gVisor | GA May 2026; Google's launch claims 300 sandbox starts per second |
| [Agent Sandbox](https://github.com/kubernetes-sigs/agent-sandbox) | Your Kubernetes cluster | Pod plus a runtime you choose | The open Kubernetes-native primitive: Sandbox resource, warm pools, claims |
| [Docker Sandboxes](https://www.docker.com/products/docker-sandboxes/) | Your laptop | MicroVMs (works on macOS/Windows) | Run coding agents unsupervised locally; the August 2026 launch that put the category on front pages |
| [microsandbox](https://github.com/superradcompany/microsandbox) | Your laptop or self-host | MicroVMs | Local-first and open source (Apache-2.0) |
| bubblewrap and friends | Your laptop | Process sandbox | The zero-infrastructure baseline; better than nothing, weakest wall |

Newer hosted entrants (Blaxel, Runloop, Morph, Beam) compete mostly on idle pricing and cold starts; they fill the ["E2B alternatives" lists](https://www.beam.cloud/blog/best-e2b-alternatives) worth scanning before you commit.

## Two neighbors that are not sandboxes

[smolagents](https://github.com/huggingface/smolagents) (28.7k stars) is not a sandbox: it is an agent library whose actions are Python code, and it plugs *into* E2B, Modal, Docker, or Blaxel to run that code. Its real rivals are agent frameworks like LangGraph and CrewAI. [OpenHands](https://github.com/OpenHands/OpenHands) is a full coding agent with the Docker sandbox already wired, for when assembling agent plus sandbox yourself is the part you don't want.

## Pick by situation

- **You're building a product whose agent writes and runs code** → **E2B**, or **Modal** if that code needs GPUs. Hosted, per-second billing, strong isolation.
- **You're a platform team and the code must stay on your infrastructure** → **Agent Sandbox** on any Kubernetes, **GKE Agent Sandbox** on Google, or **AgentCore** on AWS.
- **You want to run Claude Code or Codex unsupervised on your own machine** → **Docker Sandboxes**, or **microsandbox** if you want it open source.
- **You were evaluating Daytona** → read the [repo banner](https://github.com/daytonaio/daytona#readme) first. Core development moved to a private codebase in June 2026 and the public repo gets no further updates. The 72k stars measure what it was. Choose it today only as the hosted product, or fork v0.190.0 and accept AGPL plus sole maintenance.
- **Watch the bill shape**, not just the price: E2B and Daytona bill the full time a sandbox is alive; Vercel bills active CPU only. An agent that thinks for minutes between commands pays very differently on each.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). New to this decision? Start with [How to pick a harness](how-to-pick-a-harness.md). Spot an error or a stale claim? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._

_Agents can query this page's data directly: `claude mcp add agent-harnesses -- uvx agent-harnesses-mcp` ([MCP server](../mcp/))._
