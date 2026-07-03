import json

import generate


def test_readme_has_graveyard_section_and_excludes_from_main():
    md = generate.generate_readme()
    assert "## ⚰️ Graveyard" in md
    gid = next(g for g in generate.ARCHIVED if generate.is_graveyard(g))
    body, _, grave = md.partition("## ⚰️ Graveyard")
    assert gid in grave and gid not in body  # archived repo only under Graveyard


def test_live_projects_excludes_all_graveyard_ids():
    graveyard_ids = {
        p.github_id
        for cat in generate.CATEGORIES
        for p in generate.PROJECTS[cat[0]]
        if generate.is_graveyard(p.github_id)
    }
    live_ids = {
        p.github_id
        for cat in generate.CATEGORIES
        for p in generate.live_projects(cat[0])
    }
    assert not (graveyard_ids & live_ids)


def test_graveyard_count_matches_archived_reconciliation():
    assert generate.graveyard_count() == len(
        [g for g in generate.ARCHIVED if generate.is_graveyard(g)]
    )


def test_harnesses_json_projects_and_graveyard_are_disjoint():
    doc = json.loads(generate.generate_harnesses_json())
    project_ids = {p["github_id"] for p in doc["projects"]}
    graveyard_ids = {g["github_id"] for g in doc["graveyard"]}
    assert not (project_ids & graveyard_ids)
