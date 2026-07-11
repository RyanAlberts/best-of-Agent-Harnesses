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
def test_graveyard_projects_are_archived_or_flagged():
    for p in generate.graveyard_projects():
        assert (
            p.github_id in generate.ARCHIVED
            or p.github_id in generate.INTEGRITY_FLAGGED
        )


def test_integrity_flagged_repo_is_graveyarded_with_reason():
    for gid in generate.INTEGRITY_FLAGGED:
        assert generate.is_graveyard(gid) is True
        # a real, non-empty public reason must render, and it is not the archival copy
        reason = generate.graveyard_reason(gid)
        assert reason and reason == generate.INTEGRITY_FLAGGED[gid][1]
        assert generate.graveyard_since(gid) == generate.INTEGRITY_FLAGGED[gid][0]
