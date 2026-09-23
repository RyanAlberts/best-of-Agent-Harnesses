# Minimal agent harness in Python

A working coding-agent harness in about 180 lines of Python: the loop, three tools, a permission gate, a context file, a turn budget, and a transcript you can resume after a crash. Copy it to learn how harnesses work, or as the start of your own.

Claude Code, Codex, and OpenCode are much bigger, but they are built from the same seven parts. Each part is marked with a numbered comment in [harness.py](harness.py):

| # | Part | What it does here | What the big harnesses add |
|---|---|---|---|
| 1 | Budget | Stops after 30 model turns | Token and dollar budgets, per-task limits |
| 2 | Context guard | Cuts any tool output over 10,000 characters to its head and tail | Compaction, summaries, offloading output to files |
| 3 | Permissions | Allow list, deny list, and a yes/no prompt for everything else | Rule files, modes, classifiers, per-project policy |
| 4 | Sandbox | File tools cannot leave the start directory | Containers, network egress rules, OS-level sandboxes |
| 5 | Context | Loads `AGENTS.md` (or `CLAUDE.md`) into every request | Nested files, skills that load on demand, memory |
| 6 | Recovery | Saves every turn to `.harness/transcript.jsonl`; `--resume` continues | Durable sessions, checkpoints, rewind |
| 7 | Loop | Ask the model, run the tools it asks for, send all results back in one message, repeat | Parallel tools, subagents, hooks before and after each tool |

## Use it

```sh
pip install anthropic
export ANTHROPIC_API_KEY=...        # or run `ant auth login` once
python harness.py "add a --verbose flag to cli.py and run the tests"
python harness.py --resume          # after a crash or Ctrl-C
python harness.py --yes-to-nothing "run the tests and summarize failures"   # never prompts
```

It uses `claude-opus-5` through the official `anthropic` SDK. To use another model, change `MODEL`; to use another provider, replace the one function `anthropic_model()`. The loop only needs a response with `stop_reason` and a list of content blocks.

## Test it without an API key

[test_harness.py](test_harness.py) swaps the model for a scripted stand-in and checks a full task, the permission rules, the file sandbox, output clipping, the turn budget, and resume:

```sh
pip install pytest
python -m pytest test_harness.py -q
```

## Know the limits before you rely on it

- **The shell sandbox is a list of patterns, not isolation.** A command you approve runs with your user's full rights. Run it inside a container for anything you would not type yourself; the [sandboxing guide](../../comparisons/sandboxed-code-execution.md) compares the options.
- **Auto-approval is narrow on purpose.** Only single read-only commands and test runners skip the prompt. Anything with `;`, `&&`, `|`, `$( )`, or a redirect asks first, so `ls; rm -rf ~` cannot ride on `ls`.
- **No streaming and no compaction.** Long tasks eventually fill the context window. That is the first thing to add, and the reason bigger harnesses exist.
- **A refusal stops the loop.** The harness prints why and exits instead of retrying on another model.

## Go further

- Walk through building it step by step: [Build your own agent harness](../../playbooks/build-your-own-agent-harness.md).
- Decide whether you should build at all: [How to pick a harness](../../comparisons/how-to-pick-a-harness.md) and the [Build your own coding harness picks](../../README.md#pick-by-use-case).
- Give it a better briefing file: the [AGENTS.md template](../agents-md/).
