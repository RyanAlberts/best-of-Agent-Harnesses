import generate


def test_archived_is_dict_of_dates():
    assert isinstance(generate.ARCHIVED, dict)
    for gid, since in generate.ARCHIVED.items():
        assert "/" in gid
        assert len(since) == 10 and since[4] == "-"  # YYYY-MM-DD
