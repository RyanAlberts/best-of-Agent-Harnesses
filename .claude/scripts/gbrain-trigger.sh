#!/usr/bin/env bash
# UserPromptSubmit hook: when the user mentions a gbrain/remote-control trigger
# phrase, inject the saved bootstrap prompt as additionalContext so the
# assistant surfaces the Mac-side setup instructions.
set -euo pipefail

INPUT="$(cat)"
PROMPT="$(printf '%s' "$INPUT" | jq -r '.prompt // empty')"

# Case-insensitive match against trigger phrases.
# "remote set ?up" matches both "remote setup" and "remote set up".
# "g ?brain" matches both "gbrain" and "g brain".
if printf '%s' "$PROMPT" | grep -qiE 'add this to my brain|remember this|remote set ?up|remote skills|g ?brain on mobile'; then
    REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
    CTX="$(cat "$REPO_ROOT/.claude/prompts/gbrain-mobile-bootstrap.md")"
    jq -n --arg ctx "$CTX" '{
        hookSpecificOutput: {
            hookEventName: "UserPromptSubmit",
            additionalContext: $ctx
        }
    }'
fi
