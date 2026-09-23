#!/usr/bin/env python3
"""A minimal agent harness: the loop, the tools, the permissions, the context,
and a transcript you can resume from. About 200 lines, one dependency.

    pip install anthropic            # then set ANTHROPIC_API_KEY
    python harness.py "add a --verbose flag to cli.py and run the tests"
    python harness.py --resume       # continue the last session after a crash

Every part a big harness has is here in its smallest form, marked with a
numbered comment. Read it top to bottom, then change whatever you want.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

MODEL = "claude-opus-5"
MAX_TURNS = 30             # 1. Budget: the loop always ends.
MAX_TOOL_OUTPUT = 10_000   # 2. Context guard: no tool result floods the window.
STATE = Path(".harness")
TRANSCRIPT = STATE / "transcript.jsonl"

# 3. Permissions: commands that run without asking, and commands that never run.
ALLOW = [r"^(ls|cat|head|tail|grep|rg|find|wc|pwd|git (status|diff|log|show))\b",
         r"^(pytest|python -m pytest|npm test|npm run test|go test|cargo test)\b"]
DENY = [r"\brm\s+-rf\b", r"\bgit\s+push\b", r"\bgit\s+reset\s+--hard\b", r"\bsudo\b",
        r"\bcurl\b.*\|\s*(ba|z)?sh\b", r"(^|\s)(cat|less|head|tail)\s+\S*\.env\b"]

SYSTEM = """You are a coding agent working in the current directory.
Use the tools to inspect files before you change them. Keep changes small.
Run the tests after you change code. When the task is done, reply with a
short summary of what you changed and how you checked it."""

TOOLS = [
    {"name": "read_file", "description": "Read a UTF-8 text file.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}},
                      "required": ["path"], "additionalProperties": False}},
    {"name": "write_file", "description": "Create or overwrite a text file with the full new content.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                      "required": ["path", "content"], "additionalProperties": False}},
    {"name": "run", "description": "Run a shell command in the current directory and return its output.",
     "input_schema": {"type": "object", "properties": {"command": {"type": "string"}},
                      "required": ["command"], "additionalProperties": False}},
]


def inside_workdir(path: str) -> Path:
    """4. Sandbox, file side: the agent can only touch files under the start directory."""
    p = (Path.cwd() / path).resolve()
    if Path.cwd().resolve() not in [p, *p.parents]:
        raise PermissionError(f"{path} is outside the working directory")
    return p


def approve(command: str, interactive: bool) -> "tuple[bool, str]":
    if any(re.search(rx, command) for rx in DENY):
        return False, "blocked by the harness deny list"
    # Auto-allow only single commands: `ls; rm -rf ~` must not ride on "ls".
    if not re.search(r"[;&|`<>\n]|\$\(", command) and any(re.search(rx, command) for rx in ALLOW):
        return True, ""
    if not interactive:
        return False, "needs approval and no human is attached (run interactively to approve)"
    answer = input(f"\nAllow `{command}`? [y/N] ").strip().lower()
    return answer == "y", "" if answer == "y" else "the user declined"


def run_tool(name: str, args: dict, interactive: bool) -> "tuple[str, bool]":
    """Execute one tool call. Returns (output, is_error)."""
    try:
        if name == "read_file":
            return inside_workdir(args["path"]).read_text(), False
        if name == "write_file":
            p = inside_workdir(args["path"])
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(args["content"])
            return f"wrote {len(args['content'])} characters to {args['path']}", False
        if name == "run":
            ok, why = approve(args["command"], interactive)
            if not ok:
                return f"not run: {why}", True
            r = subprocess.run(args["command"], shell=True, capture_output=True, text=True, timeout=300)
            return f"exit {r.returncode}\n{r.stdout}{r.stderr}", r.returncode != 0
        return f"unknown tool {name}", True
    except Exception as e:  # a failed tool is information for the model, not a crash
        return f"{type(e).__name__}: {e}", True


def clip(text: str) -> str:
    if len(text) <= MAX_TOOL_OUTPUT:
        return text
    half = MAX_TOOL_OUTPUT // 2
    return f"{text[:half]}\n... [{len(text) - MAX_TOOL_OUTPUT} characters cut] ...\n{text[-half:]}"


def load_context() -> str:
    """5. Context: the project's briefing file goes into every request."""
    for name in ("AGENTS.md", "CLAUDE.md"):
        if Path(name).exists():
            return f"{SYSTEM}\n\nProject instructions from {name}:\n{Path(name).read_text()}"
    return SYSTEM


def as_dict(block) -> dict:
    """SDK content blocks become plain dicts, so the transcript is plain JSON."""
    return block if isinstance(block, dict) else block.model_dump(exclude_none=True)


def save(messages: list) -> None:
    """6. Recovery: every turn is on disk, so a crash loses nothing."""
    STATE.mkdir(exist_ok=True)
    TRANSCRIPT.write_text("".join(json.dumps(m) + "\n" for m in messages))


def load() -> list:
    return [json.loads(line) for line in TRANSCRIPT.read_text().splitlines() if line.strip()]


def anthropic_model(system: str, messages: list):
    import anthropic  # imported here so the tests run without the SDK
    client = anthropic.Anthropic()
    return client.messages.create(model=MODEL, max_tokens=16000, system=system,
                                  tools=TOOLS, messages=messages)


def agent_loop(messages: list, model=anthropic_model, interactive: bool = True, log=print) -> str:
    """7. The loop: ask the model, run the tools it asks for, repeat until it stops."""
    system = load_context()
    for _ in range(MAX_TURNS):
        response = model(system, messages)
        content = [as_dict(b) for b in response.content]
        messages.append({"role": "assistant", "content": content})
        save(messages)
        for b in content:
            if b["type"] == "text" and b.get("text"):
                log(b["text"])
        if response.stop_reason == "refusal":
            return "stopped: the model declined this request"
        calls = [b for b in content if b["type"] == "tool_use"]
        if not calls and response.stop_reason == "max_tokens":
            messages.append({"role": "user", "content": "Your last reply was cut off. Continue."})
            continue
        if not calls:
            return "done"
        results = []
        for call in calls:  # all results go back in ONE user message
            log(f"-> {call['name']} {json.dumps(call['input'])[:120]}")
            output, is_error = run_tool(call["name"], call["input"], interactive)
            results.append({"type": "tool_result", "tool_use_id": call["id"],
                            "content": clip(output), "is_error": is_error})
        messages.append({"role": "user", "content": results})
        save(messages)
    return f"stopped: reached MAX_TURNS ({MAX_TURNS})"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("task", nargs="?", help="what the agent should do")
    ap.add_argument("--resume", action="store_true", help="continue the last session")
    ap.add_argument("--yes-to-nothing", action="store_true",
                    help="never prompt; commands outside ALLOW are refused (for CI)")
    a = ap.parse_args()
    if a.resume:
        messages = load()
        last = messages[-1]
        if last["role"] == "assistant" and any(b["type"] == "tool_use" for b in last["content"]):
            messages.pop()  # crashed before the tools ran: drop the unanswered calls
        if messages[-1]["role"] == "assistant":
            messages.append({"role": "user", "content": "Continue the task."})
    elif a.task:
        messages = [{"role": "user", "content": a.task}]
    else:
        sys.exit("give a task, or --resume")
    print(agent_loop(messages, interactive=not a.yes_to_nothing))


if __name__ == "__main__":
    main()
