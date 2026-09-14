"""Structured data and link hygiene on the Pages site.

Guide pages carry TechArticle JSON-LD with real dates, every page under a
section carries BreadcrumbList, guide links resolve on the site instead of
pointing at .md paths that 404 under /compare/, and the sitemap dates each
URL. These are what answer engines and crawlers read; a regression here is
invisible in the browser.
"""

import json
import re
import subprocess

import build_site
import generate


def _build(tmp_path, monkeypatch):
    out = tmp_path / "site"
    monkeypatch.setattr(build_site, "OUT", out)
    stats = build_site.build()
    return out, stats


def _ld(html):
    return [json.loads(m) for m in re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]


def test_guide_page_carries_techarticle_and_breadcrumbs(tmp_path, monkeypatch):
    out, _ = _build(tmp_path, monkeypatch)
    html = (out / "compare" / "why-the-harness-matters" / "index.html").read_text()
    blocks = _ld(html)
    article = next(b for b in blocks if b["@type"] == "TechArticle")
    assert article["headline"] == "Why the harness matters more than the model"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", article["datePublished"])
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", article["dateModified"])
    assert article["author"]["name"] == "Ryan Alberts"
    crumbs = next(b for b in blocks if b["@type"] == "BreadcrumbList")
    assert len(crumbs["itemListElement"]) == 3
    assert '<meta property="og:site_name" content="Best of Agent Harnesses">' in html


def test_project_and_category_pages_carry_breadcrumbs(tmp_path, monkeypatch):
    out, _ = _build(tmp_path, monkeypatch)
    p = next(iter(generate.ordered_projects()))
    project_html = (out / "h" / generate.project_slug(p.github_id) / "index.html").read_text()
    category_html = (out / "c" / generate.CATEGORIES[0][0] / "index.html").read_text()
    for html, depth in ((project_html, 3), (category_html, 2)):
        crumbs = next(b for b in _ld(html) if b["@type"] == "BreadcrumbList")
        assert len(crumbs["itemListElement"]) == depth


def test_guide_links_resolve_on_the_site(tmp_path, monkeypatch):
    out, _ = _build(tmp_path, monkeypatch)
    html = (out / "compare" / "how-to-pick-a-harness" / "index.html").read_text()
    hrefs = re.findall(r'href="([^"]+)"', html)
    assert 'href="../how-to-test-drive-a-harness/"' in html
    assert not any(h.endswith(".md") or ".md#" in h for h in hrefs), [h for h in hrefs if ".md" in h]
    assert not any(h.startswith("../README") for h in hrefs)


def test_sitemap_dates_every_url(tmp_path, monkeypatch):
    out, stats = _build(tmp_path, monkeypatch)
    sm = (out / "sitemap.xml").read_text()
    assert sm.count("<loc>") == stats["urls"]
    assert sm.count("<lastmod>") == stats["urls"]
    assert re.search(r"<lastmod>\d{4}-\d{2}-\d{2}</lastmod>", sm)


def test_llms_full_bundles_the_guides(tmp_path, monkeypatch):
    out, _ = _build(tmp_path, monkeypatch)
    full = (out / "llms-full.txt").read_text()
    assert full.startswith("# Best of Agent Harnesses")
    assert "# Why the harness matters more than the model" in full
    assert "llms-full.txt" in (out / "index.html").read_text()


def test_faq_page_links_the_sources_guide(tmp_path, monkeypatch):
    out, _ = _build(tmp_path, monkeypatch)
    faq = (out / "faq" / "index.html").read_text()
    assert "compare/why-the-harness-matters/" in faq
    assert "compare/managed-vs-self-hosted-always-on-agents/" in faq


def test_source_dates_falls_back_when_git_is_unavailable(monkeypatch):
    def boom(*args, **kwargs):
        raise OSError("no git")
    monkeypatch.setattr(subprocess, "run", boom)
    assert build_site.source_dates("comparisons/how-to-pick-a-harness.md") == (
        generate.STARS_CAPTURED, generate.STARS_CAPTURED)


def test_source_dates_orders_published_before_modified():
    published, modified = build_site.source_dates("comparisons/how-to-pick-a-harness.md")
    assert published <= modified
