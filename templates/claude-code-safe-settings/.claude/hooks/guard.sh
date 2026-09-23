#!/usr/bin/env bash
# PreToolUse hook for Claude Code: blocks dangerous shell commands anywhere in
# the command line, including chained ones (`ls && git push --force`), which
# permission rules can miss. Exit 2 blocks the call and shows stderr to Claude.
# Needs jq or python3 to read the hook's JSON input.

input="$(cat)"
if command -v jq >/dev/null 2>&1; then
  cmd="$(printf '%s' "$input" | jq -r '.tool_input.command // ""')"
else
  cmd="$(printf '%s' "$input" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))')"
fi

block() {
  echo "Blocked by .claude/hooks/guard.sh: $1. Ask the user to run it themselves if it is really needed." >&2
  exit 2
}

# Destructive git
printf '%s' "$cmd" | grep -Eq 'git[[:space:]]+push[^;&|]*(--force|[[:space:]]-f([[:space:]]|$)|--mirror|--delete|[[:space:]]:[^[:space:]])' && block "force-push or remote delete"
printf '%s' "$cmd" | grep -Eq 'git[[:space:]]+reset[[:space:]]+--hard' && block "git reset --hard discards work"
printf '%s' "$cmd" | grep -Eq 'git[[:space:]]+clean[[:space:]]+-[a-zA-Z]*f' && block "git clean deletes untracked files"
printf '%s' "$cmd" | grep -Eq 'git[[:space:]]+(checkout|restore)[[:space:]]+(--[[:space:]]+)?\.([[:space:]]|$)' && block "discarding all local changes"
printf '%s' "$cmd" | grep -Eq 'git[[:space:]]+branch[[:space:]]+-D' && block "force-deleting a branch"

# Destructive files and privilege
printf '%s' "$cmd" | grep -Eq 'rm[[:space:]]+(-[a-zA-Z]*[rR][a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*[rR]|--recursive[[:space:]]+--force|--force[[:space:]]+--recursive)' && block "recursive forced delete"
printf '%s' "$cmd" | grep -Eq '(^|[;&|[:space:]])sudo[[:space:]]' && block "sudo"

# Secrets: reading them through the shell gets around Read() deny rules.
# Example files (.env.example, .env.sample, .env.template) are not secrets.
scan="$(printf '%s' "$cmd" | sed -E 's/\.env\.(example|sample|template)//g')"
printf '%s' "$scan" | grep -Eq '(cat|less|more|head|tail|grep|awk|sed|scp|base64|xxd)[^;&|]*(\.env([.[:space:]]|$)|\.pem|id_rsa|id_ed25519|\.aws/credentials|\.ssh/)' && block "reading secrets through the shell"
printf '%s' "$cmd" | grep -Eq '(^|[;&|[:space:]])(printenv|env)([[:space:]]*$|[[:space:]]*[;&|])' && block "dumping environment variables"

# Remote code
printf '%s' "$cmd" | grep -Eq '(curl|wget)[^;&]*\|[[:space:]]*(sudo[[:space:]]+)?(ba|z)?sh' && block "piping a download into a shell"

exit 0
