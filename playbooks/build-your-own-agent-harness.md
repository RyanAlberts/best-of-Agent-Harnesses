# Build your own agent harness

Build a working coding agent in about an hour: a loop, three tools, permissions, a context file, a budget, and crash recovery, in one Python file you fully understand. You finish with the minimal harness template running on your own repo.

**Time:** about 1 hour. **Template:** [minimal agent harness](../templates/minimal-harness/). **You need:** Python 3.10 or later, an Anthropic API key, and a small repo with tests to practice on.

**Should you build at all?** Usually not for daily work: Claude Code, Codex, and OpenCode are free to try and far more capable. Build one to learn how they work, to run an agent inside your own product, or when no existing harness lets you control what you need. The [how to pick a harness](../comparisons/how-to-pick-a-harness.md) guide helps you decide, and the list's [Build your own coding harness](../README.md#pick-by-use-case) picks show the kits other people build on.

## Step 1: Get the template running

```sh
mkdir my-harness && cd my-harness
curl -fsSLO https://raw.githubusercontent.com/RyanAlberts/best-of-Agent-Harnesses/main/templates/minimal-harness/harness.py
curl -fsSLO https://raw.githubusercontent.com/RyanAlberts/best-of-Agent-Harnesses/main/templates/minimal-harness/test_harness.py
pip install anthropic pytest
python -m pytest test_harness.py -q
```

The tests use a scripted stand-in for the model, so they pass without a key. That stand-in is also your first lesson: the harness does not care what the model is. It needs a function that takes the conversation and returns a stop reason plus content blocks.

## Step 2: Read the loop

Open `harness.py` and find `agent_loop`. This is the whole idea of an agent, in Simon Willison's words "tools in a loop to achieve a goal":

1. Send the conversation and the tool list to the model.
2. Save the reply to the transcript.
3. If the reply asks for tools, run each one and send **all** the results back in **one** message.
4. If it asks for nothing, the task is done.

Two details matter more than they look. Tool errors go back to the model as results marked `is_error`, not as crashes, so the model can read the error and try something else. And the loop has a hard turn limit (`MAX_TURNS`), because a model that keeps calling tools will otherwise run until your bill stops it.

## Step 3: Point it at a real task

Copy `harness.py` into a small repo that has tests, set your key, and give it a task you could do yourself in ten minutes:

```sh
export ANTHROPIC_API_KEY=...
python harness.py "the test in tests/test_dates.py fails; find out why and fix it"
```

Watch the `->` lines: each is one tool call. Expect it to read files, run the test, edit, and run the test again. When a command is outside the allow list, the harness asks you first. Say no once on purpose and watch the model adjust.

## Step 4: Tune the permissions

Open the `ALLOW` and `DENY` lists. Add your project's test and lint commands to `ALLOW` so the agent stops asking. Notice the rule that anything with `;`, `&&`, `|`, `$( )`, or a redirect always asks: without it, `ls; rm -rf ~` would run because it starts with `ls`. Real harnesses have the same problem, which is why Claude Code pairs permission rules with hooks (see the [safe Claude Code settings template](../templates/claude-code-safe-settings/)).

If the agent will run anything you would not type yourself, run the whole harness in a container. The [sandboxing guide](../comparisons/sandboxed-code-execution.md) compares Docker, E2B, Daytona, and Modal.

## Step 5: Give it context

Create an `AGENTS.md` in the repo with your build commands and rules; the harness puts it into every request. Use the [AGENTS.md template](../templates/agents-md/) and see how much less the agent has to explore. This is the cheapest improvement you can make to any harness, including the big ones.

## Step 6: Break it, then resume

Start a longer task and press Ctrl-C in the middle. Run `python harness.py --resume`. The transcript in `.harness/transcript.jsonl` has every turn, so the agent continues where it stopped. If the crash came after the model asked for tools but before they ran, resume drops those unanswered calls and asks again. Durable execution in production harnesses is this idea with a database instead of a file.

## Step 7: Add the next feature

Pick the one your tasks hit first:

- **Long tasks fill the context window.** Add compaction: when the conversation gets long, ask the model to summarize the early turns and replace them. Anthropic's API also offers server-side compaction.
- **Slow replies feel frozen.** Switch `messages.create` to streaming and print text as it arrives.
- **You want a second opinion.** Add a tool that starts a fresh `agent_loop` with its own messages: that is a subagent.
- **You need an audit trail.** Log each tool call with a timestamp next to the transcript.

Keep the tests passing as you go: add one scripted turn to `test_harness.py` for each feature.

## When to stop building

When your harness needs parallel tool calls, a plugin system, and a UI, you are rebuilding an existing one. At that point, compare your needs with the [terminal coding agents guide](../comparisons/terminal-coding-agents.md) and the kits in the list's Build-your-own picks; many are libraries you can embed instead of a product you have to adopt.

---

_Part of [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses). Spot an error or a step that failed for you? [Open an issue](https://github.com/RyanAlberts/best-of-Agent-Harnesses/issues)._

_Agents can fetch the template files directly: `claude mcp add agent-harnesses -- uvx agent-harnesses-mcp`, then `get_template("minimal-harness")`._
