"""End-to-end site build — guards the renderer/graveyard seam.

The 2026-07-03 Pages outage: build_site.py rendered use-case picks without
the is_graveyard filter that generate.py's own renderers apply, so a
graveyarded pick crashed project_slug() at deploy time. Building the whole
site here makes any renderer that misses the filter fail in CI instead.
"""

import build_site
import generate


def _build(tmp_path, monkeypatch):
    out = tmp_path / "site"
    monkeypatch.setattr(build_site, "OUT", out)
    stats = build_site.build()
    return out, stats


def test_full_build_succeeds(tmp_path, monkeypatch):
    out, stats = _build(tmp_path, monkeypatch)
    assert (out / "index.html").exists()
    assert (out / "sitemap.xml").exists()
    assert stats["projects"] == generate.count_projects()


def test_graveyard_projects_have_no_pages_and_no_links(tmp_path, monkeypatch):
    out, _ = _build(tmp_path, monkeypatch)
    index = (out / "index.html").read_text()
    for p in generate.graveyard_projects():
        repo_slug = p.github_id.split("/")[-1].lower()
        assert not (out / "h" / repo_slug).exists()
        assert f'h/{repo_slug}/' not in index
        cid = next(c for c, _, _ in generate.CATEGORIES if p in generate.PROJECTS[c])
        cat_page = (out / "c" / cid / "index.html").read_text()
        assert f'h/{repo_slug}/' not in cat_page
