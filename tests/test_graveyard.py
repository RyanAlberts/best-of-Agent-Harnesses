import generate
def test_is_graveyard_respects_allowlist():
    gid = next(iter(generate.ARCHIVED))
    assert generate.is_graveyard(gid) is True
    generate.KEEP_DESPITE_ARCHIVED.add(gid)
    assert generate.is_graveyard(gid) is False
    generate.KEEP_DESPITE_ARCHIVED.discard(gid)
def test_ordered_excludes_graveyard():
    ids = {p.github_id for p in generate.ordered_projects()}
    assert not (ids & {g for g in generate.ARCHIVED if generate.is_graveyard(g)})
def test_graveyard_projects_are_archived():
    for p in generate.graveyard_projects():
        assert p.github_id in generate.ARCHIVED
