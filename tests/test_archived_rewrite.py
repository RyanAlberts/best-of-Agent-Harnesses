"""Regression coverage for the ARCHIVED block rewrite in refresh_stars.py —
the one piece of Flow 1 logic that previously had no test coverage at all.

Exercises rewrite_archived() / apply_archived_rewrite() / parse_archived_block()
against small in-memory fixture strings shaped like the real generate.py
block. Network-free: refresh_stars.py's executable body lives behind
`if __name__ == "__main__"`, so importing it here only defines functions —
no GH_TOKEN, no API calls.
"""

import pytest

import refresh_stars

FIXTURE_SRC = '''STARS_CAPTURED = "2026-06-01"

ARCHIVED: "dict[str, str]" = {
    "still/archived": "2026-01-01",
    "will/be-dropped": "2026-02-02",
}

KEEP_DESPITE_ARCHIVED: "set[str]" = set()

TIER_ORDER = ["super simple", "mostly simple", "slightly complex", "complex"]
'''

MANGLED_SRC = '''STARS_CAPTURED = "2026-06-01"

# ARCHIVED block missing / renamed — simulates generate.py format drift
TIER_ORDER = ["super simple", "mostly simple", "slightly complex", "complex"]
'''


def test_still_archived_keeps_original_since_date():
    new_archived = refresh_stars.rewrite_archived(["still/archived"], "2026-07-03", FIXTURE_SRC)
    assert new_archived["still/archived"] == "2026-01-01"


def test_newly_archived_gets_todays_date():
    new_archived = refresh_stars.rewrite_archived(
        ["still/archived", "brand/new"], "2026-07-03", FIXTURE_SRC
    )
    assert new_archived["brand/new"] == "2026-07-03"


def test_unarchived_repo_is_dropped():
    # "will/be-dropped" is in the existing block but not in archived_now.
    new_archived = refresh_stars.rewrite_archived(["still/archived"], "2026-07-03", FIXTURE_SRC)
    assert "will/be-dropped" not in new_archived


def test_apply_rewrite_round_trips_into_source():
    new_archived = refresh_stars.rewrite_archived(
        ["still/archived", "brand/new"], "2026-07-03", FIXTURE_SRC
    )
    new_src = refresh_stars.apply_archived_rewrite(FIXTURE_SRC, new_archived)
    reparsed = refresh_stars.parse_archived_block(new_src)
    assert reparsed == new_archived
    assert "will/be-dropped" not in new_src


def test_missing_block_raises_systemexit_on_parse():
    with pytest.raises(SystemExit):
        refresh_stars.parse_archived_block(MANGLED_SRC)


def test_missing_block_raises_systemexit_on_rewrite():
    with pytest.raises(SystemExit):
        refresh_stars.rewrite_archived(["still/archived"], "2026-07-03", MANGLED_SRC)


def test_apply_rewrite_refuses_when_block_absent():
    # apply_archived_rewrite operates on src directly (post today/META edits)
    # so it must independently guard against a vanished/mangled block rather
    # than silently returning src unchanged.
    with pytest.raises(SystemExit):
        refresh_stars.apply_archived_rewrite(MANGLED_SRC, {"still/archived": "2026-01-01"})
