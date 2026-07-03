#!/usr/bin/env python3
"""Post-regeneration integrity guardrails.

Runs after scripts/generate.py in the weekly Action to fail loud if
regeneration silently dropped editorial content or emptied a category.
Importing this module (or generate.py) has no side effects.
"""

import json
import subprocess
import sys
from pathlib import Path

import generate

REPO_ROOT = Path(__file__).resolve().parent.parent

# Stable sentence from generate.generate_header_md() / config/header.md.
# Hardcoded (not re-derived) so a bug in the generator that mangles its own
# source text still gets caught.
INTRO_SENTINEL = (
    "A model answers; an agent acts. An agent harness is the runtime that "
    "turns one into the other"
)

# Smallest current comparisons/*.md file is memory-layers.md at 2973 bytes.
# Floor set well below that so real prose passes but a truncated/emptied
# file trips it.
COMPARISON_MIN_BYTES = 1000

# Total (live + graveyard) is allowed to drop by at most this much without
# failing; anything more indicates outright project loss rather than a
# graveyard move (which preserves the total).
MAX_ALLOWED_TOTAL_DROP = 2


def _previous_totals() -> "dict | None":
    """Read meta.project_count/meta.graveyard_count from harnesses.json at HEAD.

    Returns None if the previous commit's harnesses.json lacks these keys
    (e.g. an older commit before this metadata existed) or the file/commit
    isn't available at all.
    """
    try:
        raw = subprocess.run(
            ["git", "show", "HEAD:harnesses.json"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (subprocess.CalledProcessError, OSError):
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    meta = data.get("meta", {})
    if "project_count" not in meta or "graveyard_count" not in meta:
        return None
    return {
        "project_count": meta["project_count"],
        "graveyard_count": meta["graveyard_count"],
    }


def verify() -> "list[str]":
    """Return a list of human-readable violation strings; empty = all good."""
    violations: "list[str]" = []

    # 1. Every category has at least one live project.
    for cat_id, title, _ in generate.CATEGORIES:
        if len(generate.live_projects(cat_id)) < 1:
            violations.append(f"category '{cat_id}' ({title}) has zero live projects")

    # 2a. README.md still carries the editorial intro.
    readme_path = REPO_ROOT / "README.md"
    if not readme_path.exists():
        violations.append("README.md is missing")
    elif INTRO_SENTINEL not in readme_path.read_text(encoding="utf-8"):
        violations.append(
            "README.md is missing the intro sentinel "
            f"(expected substring: {INTRO_SENTINEL!r})"
        )

    # 2b. Each comparisons/*.md still has real prose.
    comparisons_dir = REPO_ROOT / "comparisons"
    comparison_files = sorted(comparisons_dir.glob("*.md")) if comparisons_dir.is_dir() else []
    if not comparison_files:
        violations.append("comparisons/ directory has no .md files")
    for f in comparison_files:
        text = f.read_text(encoding="utf-8")
        size = len(text.encode("utf-8"))
        if size < COMPARISON_MIN_BYTES:
            violations.append(
                f"comparisons/{f.name} is only {size} bytes "
                f"(floor: {COMPARISON_MIN_BYTES})"
            )
        if not any(line.lstrip().startswith("#") for line in text.splitlines()):
            violations.append(f"comparisons/{f.name} has no markdown heading")

    # 3. No mass data loss vs the previous commit.
    previous = _previous_totals()
    if previous is None:
        violations_note = (
            "skipping mass-data-loss check: previous commit's harnesses.json "
            "has no project_count/graveyard_count"
        )
        print(f"note: {violations_note}", file=sys.stderr)
    else:
        previous_total = previous["project_count"] + previous["graveyard_count"]
        current_total = generate.count_projects() + generate.graveyard_count()
        if current_total < previous_total - MAX_ALLOWED_TOTAL_DROP:
            violations.append(
                f"total projects dropped from {previous_total} to {current_total} "
                f"(more than {MAX_ALLOWED_TOTAL_DROP} lost — possible mass data loss)"
            )

    return violations


def main() -> None:
    violations = verify()
    if violations:
        for v in violations:
            print(f"INTEGRITY VIOLATION: {v}")
        sys.exit(1)
    print("integrity OK")
    sys.exit(0)


if __name__ == "__main__":
    main()
