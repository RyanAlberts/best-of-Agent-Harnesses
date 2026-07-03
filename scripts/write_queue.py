#!/usr/bin/env python3
"""Write curation-queue.json — the handoff artifact from Flow 1 (weekly
audit, this repo's GitHub Action) to Flow 2 (a separate Claude routine that
reads this file and never calls the GitHub API).

Schema (top-level keys, exactly these six):
    generated  str              "YYYY-MM-DD"
    movers     list[{"id","from","to"}]
    moved      list[{"id","to"}]
    archived   list[{"id","since","stars"}]
    failed     list[{"id","status"}]
    candidates list                        (filled by Task 6; default [])
"""

import json
import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_PATH = REPO_ROOT / "curation-queue.json"

LIST_KEYS = ("movers", "moved", "archived", "failed", "candidates")


def write(data: dict, path: pathlib.Path | None = None) -> dict:
    """Normalize `data` to the curation-queue schema, write it as pretty
    JSON to `path` (default: repo-root curation-queue.json), and return the
    normalized dict."""
    normalized = dict(data)
    for key in LIST_KEYS:
        normalized.setdefault(key, [])
    normalized.setdefault("generated", "")

    out_path = path if path is not None else DEFAULT_PATH
    out_path.write_text(json.dumps(normalized, indent=2) + "\n")

    return normalized
