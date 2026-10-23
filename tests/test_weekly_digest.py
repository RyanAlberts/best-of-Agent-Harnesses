"""weekly_digest.py: the diff behind latest-changes.md, changes.json, and the
weekly release."""

import json

import weekly_digest as w


def _p(gid, stars, slug=None, **kw):
    name = gid.split("/")[-1]
    return {"github_id": gid, "name": name, "slug": slug or name, "stars": stars,
            "category_title": "Coding agent products", "page_url": f"https://x/h/{slug or name}/",
            "description": f"{name} runs the loop. More text.", "archived": None} | kw


def _doc(date, projects, **kw):
    return {"meta": {"stars_captured": date}, "projects": projects} | kw


def test_diff_finds_adds_gains_and_new_guides():
    before = _doc("2026-10-18", [_p("a/big", 10_000), _p("b/small", 100), _p("c/gone", 50)])
    after = _doc("2026-10-25", [_p("a/big", 12_000), _p("b/small", 400), _p("d/new", 900)],
                 comparisons=[{"slug": "harness-engineering", "title": "Harness engineering"}])
    week = w.diff(before, after)
    assert [p["github_id"] for p in week["added"]] == ["d/new"]
    assert [p["github_id"] for p in week["removed"]] == ["c/gone"]
    assert [(p["github_id"], p["delta"]) for p in week["gainers"]] == [("a/big", 2000), ("b/small", 300)]
    # b/small tripled but is under the percentage floor; a/big grew 20%.
    assert [(p["github_id"], p["pct"]) for p in week["fastest"]] == [("a/big", 20.0)]
    assert week["new_guides"][0]["url"].endswith("/compare/harness-engineering/")
    assert w.title(week) == "Week of 2026-10-25: 1 new harness, big +2,000 stars"


def test_moved_repo_is_not_an_add_and_a_remove():
    before = _doc("2026-10-18", [_p("old-org/talon", 500, slug="talon")])
    after = _doc("2026-10-25", [_p("new-org/talon", 500, slug="talon")])
    week = w.diff(before, after)
    assert week["added"] == [] and week["removed"] == []
    assert w.is_quiet(week)


def test_markdown_is_plain_and_line_three_is_prose():
    before = _doc("2026-10-18", [_p("a/big", 10_000)])
    after = _doc("2026-10-25", [_p("a/big", 10_500, archived="2026-10-20"), _p("d/new", 900)])
    md = w.render_md(w.diff(before, after))
    lines = md.splitlines()
    assert lines[0] == "# What changed in agent harnesses: 2026-10-25"
    assert lines[2][0].isalpha()
    assert "\u2014" not in md
    assert "**[new](https://x/h/new/)**, 900 stars, Coding agent products: new runs the loop." in md
    assert "archived upstream 2026-10-20" in md


def test_history_replaces_same_date_and_caps(tmp_path):
    path = tmp_path / "changes.json"
    path.write_text(json.dumps({"weeks": [{"date": f"2025-{i:03d}"} for i in range(60)]}))
    out = w.update_history({"date": "2025-000", "fresh": True}, path)
    assert out["weeks"][0] == {"date": "2025-000", "fresh": True}
    assert len(out["weeks"]) == w.MAX_WEEKS
    assert [x["date"] for x in out["weeks"]].count("2025-000") == 1
