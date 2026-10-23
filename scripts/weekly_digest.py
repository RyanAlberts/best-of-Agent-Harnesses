#!/usr/bin/env python3
"""Weekly digest: what changed in the list since the previous refresh.

Diffs the previous harnesses.json (the committed copy, saved before
generate.py rewrites it) against the current one and writes:

  latest-changes.md   the human digest: the weekly release notes and the
                      site's /changes/ page
  changes.json        the same data for agents (MCP whats_new), newest week
                      first, capped at MAX_WEEKS

    cp harnesses.json /tmp/harnesses.before.json
    python3 scripts/refresh_stars.py && python3 scripts/generate.py
    python3 scripts/weekly_digest.py /tmp/harnesses.before.json

Prints the release title on stdout, or nothing when nothing changed, so the
workflow can skip the release on a quiet week.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate as g  # noqa: E402

MAX_WEEKS = 52
TOP_GAINERS = 10
TOP_FASTEST = 5
MIN_STARS_FOR_PCT = 500  # below this, a handful of stars swings the percentage


def _brief(p: dict, **extra) -> dict:
    return {"github_id": p["github_id"], "name": p["name"], "category": p.get("category_title", ""),
            "stars": p.get("stars", 0), "page_url": p.get("page_url", "")} | extra


def _new_items(before: dict, after: dict, key: str, id_field: str) -> list:
    old = {i[id_field] for i in before.get(key, [])}
    return [i for i in after.get(key, []) if i[id_field] not in old]


def diff(before: dict, after: dict) -> dict:
    b = {p["github_id"].lower(): p for p in before.get("projects", [])}
    a = {p["github_id"].lower(): p for p in after.get("projects", [])}
    added = [a[k] for k in a if k not in b]
    removed = [b[k] for k in b if k not in a]
    # A repo that moved org keeps its slug: that is a rename, not an add + remove.
    moved = {p.get("slug") for p in added} & {p.get("slug") for p in removed}
    added = [p for p in added if p.get("slug") not in moved]
    removed = [p for p in removed if p.get("slug") not in moved]
    both = [(b[k], a[k]) for k in a if k in b]

    gains = sorted(both, key=lambda t: t[1]["stars"] - t[0]["stars"], reverse=True)
    gainers = [_brief(new, delta=new["stars"] - old["stars"]) for old, new in gains[:TOP_GAINERS]
               if new["stars"] > old["stars"]]
    growth = sorted((t for t in both if t[0]["stars"] >= MIN_STARS_FOR_PCT),
                    key=lambda t: t[1]["stars"] / t[0]["stars"], reverse=True)
    fastest = [_brief(new, previous_stars=old["stars"], pct=round(100 * (new["stars"] / old["stars"] - 1), 1))
               for old, new in growth[:TOP_FASTEST] if new["stars"] > old["stars"]]
    archived = [_brief(new, archived=new["archived"]) for old, new in both
                if new.get("archived") and not old.get("archived")]
    guides = [{"slug": c["slug"], "title": c["title"], "url": f"{g.SITE_URL}compare/{c['slug']}/"}
              for c in _new_items(before, after, "comparisons", "slug")]
    skills = [{"name": s["name"], "title": s["title"], "url": f"{g.SITE_URL}skills/{s['name']}/"}
              for s in _new_items(before, after, "skills", "name")]
    templates = [{"slug": t["slug"], "title": t["title"], "url": f"{g.SITE_URL}templates/{t['slug']}/"}
                 for t in _new_items(before, after, "templates", "slug")]
    return {
        "date": after["meta"]["stars_captured"],
        "since": before.get("meta", {}).get("stars_captured", ""),
        "project_count": len(a),
        "added": [_brief(p, description=p.get("description", "")) for p in added],
        "removed": [_brief(p) for p in removed],
        "gainers": gainers,
        "fastest": fastest,
        "archived": archived,
        "new_guides": guides,
        "new_skills": skills,
        "new_templates": templates,
    }


def is_quiet(week: dict) -> bool:
    return not any(week[k] for k in ("added", "removed", "gainers", "archived",
                                     "new_guides", "new_skills", "new_templates"))


def title(week: dict) -> str:
    n = len(week["added"])
    lead = f"{n} new harness{'es' if n != 1 else ''}" if n else "star movers"
    top = week["gainers"][0] if week["gainers"] else None
    tail = f", {top['name']} +{top['delta']:,} stars" if top else ""
    return f"Week of {week['date']}: {lead}{tail}"


def _link(p: dict) -> str:
    return f"[{p['name']}]({p['page_url']})" if p.get("page_url") else p["name"]


def render_md(week: dict) -> str:
    since = f" since the {week['since']} refresh" if week["since"] else ""
    out = [
        f"# What changed in agent harnesses: {week['date']}",
        "",
        f"Changes to the best-of-Agent-Harnesses list{since}. The list now ranks {week['project_count']} "
        f"agent harnesses, and the star counts below come from GitHub on {week['date']}.",
        "",
    ]
    if week["added"]:
        out += ["## New on the list", ""]
        for p in week["added"]:
            first = p["description"].split(". ")[0].rstrip(".")
            out.append(f"- **{_link(p)}** ({p['category']}, {g.format_stars(p['stars'])} stars): {first}.")
        out.append("")
    if week["gainers"]:
        out += ["## Biggest star gains", "", "| Harness | Category | Stars | Gain |", "|---|---|---:|---:|"]
        out += [f"| {_link(p)} | {p['category']} | {g.format_stars(p['stars'])} | +{p['delta']:,} |"
                for p in week["gainers"]]
        out.append("")
    if week["fastest"]:
        out += ["## Fastest growing", "", f"Projects that already had {MIN_STARS_FOR_PCT}+ stars.", ""]
        out += [f"- {_link(p)}: +{p['pct']}% ({g.format_stars(p['previous_stars'])} to "
                f"{g.format_stars(p['stars'])} stars)" for p in week["fastest"]]
        out.append("")
    if week["archived"] or week["removed"]:
        out += ["## Archived or removed", ""]
        out += [f"- {_link(p)}: archived upstream {p['archived']}" for p in week["archived"]]
        out += [f"- {p['name']} (`{p['github_id']}`): left the ranked list" for p in week["removed"]]
        out.append("")
    new_docs = ([("Guide", d) for d in week["new_guides"]] + [("Skill", d) for d in week["new_skills"]]
                + [("Template", d) for d in week["new_templates"]])
    if new_docs:
        out += ["## New guides, skills, and templates", ""]
        out += [f"- {kind}: [{d['title']}]({d['url']})" for kind, d in new_docs]
        out.append("")
    out += [
        "## Get this every week",
        "",
        "Star and watch [the repo](https://github.com/RyanAlberts/best-of-Agent-Harnesses) "
        "(Watch, then Custom, then Releases) to get this digest each Sunday. "
        f"Browse every harness on [the site]({g.SITE_URL}). Agents can read the same data "
        "with the `whats_new` tool of the MCP server: `uvx agent-harnesses-mcp`.",
        "",
    ]
    return "\n".join(out)


def update_history(week: dict, path: Path) -> dict:
    try:
        weeks = json.loads(path.read_text()).get("weeks", [])
    except (OSError, ValueError):
        weeks = []
    weeks = [week] + [w for w in weeks if w.get("date") != week["date"]]
    return {"description": "Week-by-week changes to best-of-Agent-Harnesses, newest first.",
            "weeks": weeks[:MAX_WEEKS]}


def main(argv: list) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    before = json.loads(Path(argv[1]).read_text())
    after = json.loads((g.REPO_ROOT / "harnesses.json").read_text())
    week = diff(before, after)
    if is_quiet(week):
        return 0
    (g.REPO_ROOT / "latest-changes.md").write_text(render_md(week))
    history = update_history(week, g.REPO_ROOT / "changes.json")
    (g.REPO_ROOT / "changes.json").write_text(json.dumps(history, indent=1, ensure_ascii=False) + "\n")
    print(title(week))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
