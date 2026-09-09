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


def _fake_api_factory(issues, repos):
    def fake_api(path, token):
        if path.startswith("/repos/") and "/issues" in path:
            return issues
        gid = path[len("/repos/"):]
        if gid not in repos:
            raise RuntimeError("404")
        return repos[gid]
    return fake_api


def test_issue_submissions_resolve_open_add_project_issues(monkeypatch):
    issues = [
        {"number": 86, "title": "Add project: Prime Agent", "labels": [{"name": "add-project"}],
         "body": "### Repo URL\n\nhttps://github.com/PrimeIntellect-ai/prime-agent\n"},
        {"number": 74, "title": "Update project: X", "labels": [{"name": "update-project"}],
         "body": "https://github.com/some/other"},                        # not a submission
        {"number": 90, "title": "Add project: dupe", "labels": [],
         "body": "https://github.com/Known/Already-Listed"},               # already listed
        {"number": 57, "title": "Add project: no link", "labels": [{"name": "add-project"}],
         "body": "no repo url in the body"},                               # nothing to resolve
        {"number": 99, "title": "Add project: PR", "labels": [{"name": "add-project"}],
         "pull_request": {"url": "x"}, "body": "https://github.com/a/b"},  # PRs are not issues
        {"number": 12, "title": "Add project: gone", "labels": [{"name": "add-project"}],
         "body": "https://github.com/dead/archived-repo"},                # archived upstream
        {"number": 13, "title": "Add project: vanished", "labels": [{"name": "add-project"}],
         "body": "https://github.com/no/such-repo"},                      # 404 on lookup
    ]
    repos = {
        "PrimeIntellect-ai/prime-agent": {
            "full_name": "PrimeIntellect-ai/prime-agent", "stargazers_count": 20386,
            "topics": ["agents"], "description": "Coding and research agent", "archived": False,
        },
        "dead/archived-repo": {
            "full_name": "dead/archived-repo", "stargazers_count": 9000,
            "topics": [], "description": "", "archived": True,
        },
    }
    monkeypatch.setattr(discover_candidates, "_api", _fake_api_factory(issues, repos))

    result = discover_candidates.issue_submissions("fake-token", "o/r", {"known/already-listed"})

    assert result == [
        {
            "id": "PrimeIntellect-ai/prime-agent",
            "stars": 20386,
            "topics": ["agents"],
            "desc": "Coding and research agent",
            "via": "issue #86",
        }
    ]


def test_issue_submissions_survive_listing_failure(monkeypatch):
    def boom(path, token):
        raise RuntimeError("secondary rate limit exceeded")

    monkeypatch.setattr(discover_candidates, "_api", boom)

    assert discover_candidates.issue_submissions("fake-token", "o/r", set()) == []
