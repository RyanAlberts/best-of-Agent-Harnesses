# Safe Claude Code settings: permissions and a guard hook

Project settings that stop Claude Code from force-pushing, wiping work, reading secrets, or piping downloads into a shell, while leaving everyday commands alone. Two files, copy and commit.

## What is in this template

| File | What it does |
|---|---|
| [.claude/settings.json](.claude/settings.json) | Permission rules: read-only git runs without asking; pushes, commits, publishing, and infrastructure tools ask first; secrets, force-pushes, hard resets, `rm -rf`, and `sudo` are denied. Also turns off bypass mode for this project. |
| [.claude/hooks/guard.sh](.claude/hooks/guard.sh) | A `PreToolUse` hook that checks every shell command before it runs, including chained ones such as `npm test && git push --force`. It blocks with exit code 2, and Claude sees the reason. |

## Why both

Permission rules match the start of a command, and Claude Code's own docs warn that [argument patterns are fragile](https://code.claude.com/docs/en/permissions). A `Read(.env)` deny rule also does not stop `cat .env` in the shell. The hook covers those gaps by reading the whole command line. Hooks cannot loosen the rules: a deny rule still wins even if the hook allows the call ([docs](https://code.claude.com/docs/en/permissions)). Each layer only adds limits.

What the hook blocks:

- `git push --force`, `-f`, `--mirror`, `--delete`, and `git push origin :branch`
- `git reset --hard`, `git clean -f`, `git checkout .`, `git restore .`, `git branch -D`
- `rm -rf` in any flag order, and `sudo`
- Reading `.env`, `.pem`, SSH keys, or AWS credentials through `cat`, `grep`, `head`, `base64`, and similar (`.env.example` is allowed)
- `env` and `printenv` with no arguments
- `curl ... | sh` and `wget ... | bash`

## Install

From the root of your repo:

```sh
mkdir -p .claude/hooks
curl -fsSL https://raw.githubusercontent.com/RyanAlberts/best-of-Agent-Harnesses/main/templates/claude-code-safe-settings/.claude/settings.json -o .claude/settings.json
curl -fsSL https://raw.githubusercontent.com/RyanAlberts/best-of-Agent-Harnesses/main/templates/claude-code-safe-settings/.claude/hooks/guard.sh -o .claude/hooks/guard.sh
chmod +x .claude/hooks/guard.sh
```

If you already have a `.claude/settings.json`, merge the `permissions` and `hooks` blocks by hand instead of overwriting it. The hook needs `jq` or `python3`.

Open Claude Code in the repo once and accept the trust prompt. Until you do, Claude Code ignores the project's `allow` rules.

## Check that it works

Test the hook without starting a session:

```sh
echo '{"tool_name":"Bash","tool_input":{"command":"npm test && git push --force"}}' | .claude/hooks/guard.sh; echo "exit $?"
```

You should see a `Blocked by .claude/hooks/guard.sh` message and `exit 2`. Then, in a session, run `/permissions` to see the rules Claude Code loaded and `/hooks` to see the hook.

## Adjust it

- **Too strict?** `rm -rf build` is denied too. Delete the `"Bash(rm -rf *)"` deny rule and the `rm` line in `guard.sh` if your workflow needs it, or add a narrower allow rule.
- **Personal changes** go in `.claude/settings.local.json`, which git ignores, so the team file stays the shared baseline.
- **Whole organization?** Put the same rules in managed settings, which users cannot override.

## Limits

Pattern checks catch mistakes and obvious prompt injection, not a determined attacker: a script file the agent writes and then runs is not inspected. For real isolation, run the agent in a container or turn on Claude Code's sandbox; the [sandboxing guide](../../comparisons/sandboxed-code-execution.md) compares options.

## Go further

- Pair it with a shared briefing file: [One AGENTS.md for every coding agent](../agents-md/).
- See how permissions work inside a harness by reading one: [Minimal agent harness in Python](../minimal-harness/).
