import discover_candidates


def _fake_search(query, token):
    """Canned GitHub search response, one repo per outcome under test."""
    return {
        "items": [
            {
                "full_name": "Known/Already-Listed",
                "stargazers_count": 5000,
                "topics": ["ai-agents"],
                "description": "Already in the list",
                "archived": False,
            },
            {
                "full_name": "tiny/under-threshold",
                "stargazers_count": 10,
                "topics": ["ai-agents"],
                "description": "Too few stars",
                "archived": False,
            },
            {
                "full_name": "dead/archived-repo",
                "stargazers_count": 9000,
                "topics": ["agent-framework"],
                "description": "Archived, should be excluded",
                "archived": True,
            },
            {
                "full_name": "cool/new-harness",
                "stargazers_count": 1200,
                "topics": ["ai-agents", "coding-agent"],
                "description": "A qualifying new harness",
                "archived": False,
            },
        ]
    }


def test_find_filters_known_understarred_and_archived(monkeypatch):
    monkeypatch.setattr(discover_candidates, "_search", _fake_search)

    known_ids = {"known/already-listed"}  # lowercase, as known_ids are stored
    result = discover_candidates.find("fake-token", known_ids, min_stars=300)

    assert result == [
        {
            "id": "cool/new-harness",
            "stars": 1200,
            "topics": ["ai-agents", "coding-agent"],
            "desc": "A qualifying new harness",
        }
    ]


def test_find_deduplicates_across_queries(monkeypatch):
    def fake_search(query, token):
        return {
            "items": [
                {
                    "full_name": "cool/new-harness",
                    "stargazers_count": 1200,
                    "topics": ["ai-agents"],
                    "description": "Seen twice across two queries",
                    "archived": False,
                }
            ]
        }

    monkeypatch.setattr(discover_candidates, "_search", fake_search)

    result = discover_candidates.find("fake-token", set(), min_stars=300)

    assert len(result) == 1
    assert result[0]["id"] == "cool/new-harness"


def test_find_survives_one_failed_query(monkeypatch):
    """A single rate-limited/failed query must not crash find() or lose
    candidates found by the other queries."""
    calls = {"count": 0}

    def flaky_search(query, token):
        calls["count"] += 1
        if calls["count"] == 1:
            raise RuntimeError("secondary rate limit exceeded")
        return {
            "items": [
                {
                    "full_name": "cool/new-harness",
                    "stargazers_count": 1200,
                    "topics": ["ai-agents"],
                    "description": "Survives a failed sibling query",
                    "archived": False,
                }
            ]
        }

    monkeypatch.setattr(discover_candidates, "_search", flaky_search)

    result = discover_candidates.find("fake-token", set(), min_stars=300)

    assert calls["count"] == len(discover_candidates.QUERIES)
    assert len(result) == 1
    assert result[0]["id"] == "cool/new-harness"
