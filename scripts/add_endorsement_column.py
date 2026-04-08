#!/usr/bin/env python3
"""Add or refresh the Prominent voice column using GitHub About + QUOTE_OVERRIDES."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from endorsements_data import QUOTE_OVERRIDES  # noqa: E402

ROW_RE = re.compile(
    r"^(\|\s*\d+\s*\|\s*)"
    r"(\[\*\*[^\]]+\*\*\]\()"
    r"(https://github.com/[^/]+/[^)]+)"
    r"(\)\s*\|\s*)"
    r"(.*?)"
    r"(\s*\|\s*)"
    r"([^|]+?)"
    r"(\s*\|)\s*$"
)


def gh_description(github_id: str) -> str:
    out = subprocess.run(
        ["gh", "repo", "view", github_id, "--json", "description,owner"],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(out.stdout)
    desc = (data.get("description") or "").strip()
    owner = data.get("owner", {}).get("login", github_id.split("/")[0])
    if not desc:
        return f"**{owner} (GitHub maintainer):** *(no About blurb)*"
    if len(desc) > 220:
        desc = desc[:217] + "…"
    return f"**{owner} (GitHub About):** “{desc}”"


def endorsement_for(github_id: str) -> str:
    if github_id in QUOTE_OVERRIDES:
        return QUOTE_OVERRIDES[github_id]
    try:
        return gh_description(github_id)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return f"**{github_id}:** *(no public `gh repo view` result—check path or auth)*"


def escape_cell(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ")


def process_readme() -> None:
    text = README.read_text(encoding="utf-8")
    lines = text.splitlines()
    out_lines: list[str] = []
    cache: dict[str, str] = {}

    for line in lines:
        if line.strip() == "| # | Project | Description | Simplicity ↔ capability |":
            out_lines.append(
                "| # | Project | Description | Simplicity ↔ capability | Prominent voice |"
            )
            continue
        if line.strip() == "|---|---------|-------------|-------------------------|":
            out_lines.append(
                "|---|---------|-------------|-------------------------|-----------------|"
            )
            continue

        m = ROW_RE.match(line)
        if m:
            g1, g2, url, g4, desc, g6, axis, g8 = m.groups()
            path = url.removeprefix("https://github.com/")
            if path not in cache:
                cache[path] = escape_cell(endorsement_for(path))
            cell = cache[path]
            axis_clean = axis.strip()
            out_lines.append(
                f"{g1}{g2}{url}{g4}{desc}{g6}{axis_clean} | {cell}{g8}"
            )
            continue

        out_lines.append(line)

    README.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    print(f"Updated {README} ({len(cache)} unique repos)")


if __name__ == "__main__":
    process_readme()
