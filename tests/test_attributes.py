"""Validation tests for attributes/ deep-dive files (attributes/RUBRIC.md)."""
import json

import pytest

import generate as gen


def _live_slug_and_gid():
    p = next(p for cat_id, _, _ in gen.CATEGORIES for p in gen.live_projects(cat_id))
    return gen.project_slug(p.github_id), p.github_id


def _good(gid):
    ax = {"rating": "strong", "detail": "d", "evidence": "https://example.com/docs"}
    return {
        "github_id": gid, "researched": "2026-07-19",
        "tooling_sandboxing": dict(ax),
        "context_memory": {"rating": "basic", "detail": "d", "evidence": "https://example.com/x"},
        "lifecycle_hooks": {"rating": "full", "detail": "d", "evidence": "https://example.com/x"},
        "prompt_optimization": {"rating": "unknown", "detail": "looked in docs, nothing"},
        "build_vs_buy": {"tier": 2, "label": "blueprint", "detail": "d",
                         "evidence": "https://example.com/x"},
    }


def _write(tmp_path, slug, doc):
    (tmp_path / f"{slug}.json").write_text(json.dumps(doc))
    return tmp_path


def test_good_file_merges(tmp_path):
    slug, gid = _live_slug_and_gid()
    out = gen.load_deep_dives(_write(tmp_path, slug, _good(gid)))
    dd = out[gid]
    assert dd["tooling_sandboxing"]["rank"] == 3
    assert dd["context_memory"]["rank"] == 2
    assert dd["lifecycle_hooks"]["rank"] == 3
    assert dd["prompt_optimization"]["rank"] == 0
    assert dd["build_vs_buy"] == {"tier": 2, "label": "blueprint", "detail": "d",
                                  "evidence": "https://example.com/x"}


def test_bad_rating_fails(tmp_path):
    slug, gid = _live_slug_and_gid()
    doc = _good(gid)
    doc["lifecycle_hooks"]["rating"] = "excellent"
    with pytest.raises(SystemExit, match="lifecycle_hooks.rating"):
        gen.load_deep_dives(_write(tmp_path, slug, doc))


def test_rating_without_evidence_fails(tmp_path):
    slug, gid = _live_slug_and_gid()
    doc = _good(gid)
    del doc["tooling_sandboxing"]["evidence"]
    with pytest.raises(SystemExit, match="without an evidence URL"):
        gen.load_deep_dives(_write(tmp_path, slug, doc))


def test_missing_axis_fails(tmp_path):
    slug, gid = _live_slug_and_gid()
    doc = _good(gid)
    del doc["context_memory"]
    with pytest.raises(SystemExit, match="missing axis context_memory"):
        gen.load_deep_dives(_write(tmp_path, slug, doc))


def test_label_tier_mismatch_fails(tmp_path):
    slug, gid = _live_slug_and_gid()
    doc = _good(gid)
    doc["build_vs_buy"]["label"] = "managed"
    with pytest.raises(SystemExit, match="build_vs_buy.label"):
        gen.load_deep_dives(_write(tmp_path, slug, doc))


def test_orphan_slug_fails(tmp_path):
    _, gid = _live_slug_and_gid()
    with pytest.raises(SystemExit, match="no live project"):
        gen.load_deep_dives(_write(tmp_path, "not-a-real-slug", _good(gid)))


def test_repo_attributes_dir_is_valid():
    # Whatever is committed under attributes/ must pass validation end to end.
    gen.load_deep_dives()
