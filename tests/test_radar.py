"""radar_entries(): editorial pins hydrated from curation-queue.json."""

import pytest

import generate


def test_radar_never_shows_listed_projects(monkeypatch):
    monkeypatch.setattr(generate, "RADAR", [{"id": "cline/cline", "via": "weekly discovery"}])
    assert generate.radar_entries() == []


def test_radar_hydrates_stars_and_desc_from_queue(monkeypatch):
    qc = generate.queue_candidates()
    listed = {p.github_id for plist in generate.PROJECTS.values() for p in plist}
    unlisted = [gid for gid in qc if gid not in listed]
    if not unlisted:
        pytest.skip("queue has no unlisted candidates to hydrate from")
    gid = unlisted[0]
    monkeypatch.setattr(generate, "RADAR", [{"id": gid, "via": "weekly discovery"}])
    (entry,) = generate.radar_entries()
    assert entry["stars"] == qc[gid]["stars"]


def test_radar_pin_metadata_fallback_when_not_in_queue(monkeypatch):
    monkeypatch.setattr(generate, "RADAR", [
        {"id": "example/not-in-queue", "via": "community · PR #0", "stars": 14, "desc": "Fallback desc"}
    ])
    (entry,) = generate.radar_entries()
    assert entry["stars"] == 14
    assert entry["desc"] == "Fallback desc"
    assert entry["via"] == "community · PR #0"
