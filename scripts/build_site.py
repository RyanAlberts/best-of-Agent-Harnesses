#!/usr/bin/env python3
"""Static-site generator for best-of-Agent-Harnesses.

Renders the GitHub Pages site (one indexable, citeable URL per project,
category, and comparison) from the SAME data as the README — it imports the
data structures and helpers from generate.py, so the site can never drift from
the list. Each page carries schema.org JSON-LD, a canonical URL, OpenGraph
tags, and is listed in sitemap.xml, so search crawlers and AI answer engines
index and cite individual entries rather than one 73 KB README.

    python3 scripts/build_site.py        # writes ./site/

Only build-time dependency beyond the stdlib is `markdown` (comparison pages).
"""

import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate as g  # noqa: E402

try:
    import markdown
except ImportError:
    sys.exit("build_site.py needs `markdown`: pip install markdown")

ROOT = g.REPO_ROOT
OUT = ROOT / "site"
ORIGIN = g.SITE_ORIGIN
BASE = g.BASE_PATH  # "/best-of-Agent-Harnesses"
OG_IMAGE = f"{ORIGIN}{BASE}/assets/social-preview.png"
GITHUB_REPO = "https://github.com/RyanAlberts/best-of-Agent-Harnesses"
AUTHOR = {"@type": "Person", "name": "Ryan Alberts", "url": "https://github.com/RyanAlberts"}


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def u(path: str = "") -> str:
    """Root-absolute site URL for internal links (depth-independent)."""
    return f"{BASE}/{path}".rstrip("/") + ("/" if path else "/")


def abs_url(path: str = "") -> str:
    return ORIGIN + u(path)


def source_dates(rel_path: str) -> "tuple[str, str]":
    """(datePublished, dateModified) for a source file from git history, so
    guide pages carry real dates for answer engines; STARS_CAPTURED when the
    file is not committed yet or git is unavailable (pages.yml checks out
    with fetch-depth 0 so the history is present at deploy time)."""
    try:
        out = subprocess.run(["git", "log", "--follow", "--format=%as", "--", rel_path],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        out = []
    return (out[-1], out[0]) if out else (g.STARS_CAPTURED, g.STARS_CAPTURED)


def breadcrumb_ld(crumbs: "list[tuple[str, str]]") -> dict:
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": name, "item": url}
            for i, (name, url) in enumerate(crumbs, 1)
        ],
    }


def site_links(md: str) -> str:
    """Rewrite the guides' repo-relative links for the site. Sibling guides go
    to their site pages, assets to the site copy, and everything else under
    the repo root (README anchors, mcp/, attributes/) to GitHub, so no guide
    page links to a .md path that does not exist under /compare/."""
    md = re.sub(r"\]\(\.\./README\.md(#[^)]*)?\)", lambda m: f"]({GITHUB_REPO}{m.group(1) or ''})", md)
    md = re.sub(r"\]\(\.\./assets/([^)]+)\)", lambda m: f"]({u()}assets/{m.group(1)})", md)
    md = re.sub(r"\]\(\.\./comparisons/([\w-]+)\.md(#[^)]*)?\)", lambda m: f"]({u('compare/' + m.group(1))}{m.group(2) or ''})", md)
    md = re.sub(r"\]\(\.\./playbooks/([\w-]+)\.md(#[^)]*)?\)", lambda m: f"]({u('playbooks/' + m.group(1))}{m.group(2) or ''})", md)
    md = re.sub(r"\]\(\.\./templates/([\w-]+)/?(?:README\.md)?(#[^)]*)?\)", lambda m: f"]({u('templates/' + m.group(1))}{m.group(2) or ''})", md)
    md = re.sub(r"\]\(\.\./([^)#]+?)/?(#[^)]*)?\)", lambda m: f"]({GITHUB_REPO}/tree/main/{m.group(1)}{m.group(2) or ''})", md)
    md = re.sub(r"\]\(([\w-]+)\.md(#[^)]*)?\)", lambda m: f"](../{m.group(1)}/{m.group(2) or ''})", md)
    return md


# --------------------------------------------------------------------------- #
# Shared chrome
# --------------------------------------------------------------------------- #

def page(title: str, description: str, canonical_path: str, body: str,
         jsonld: "list | dict | None" = None) -> str:
    desc = esc(description[:200])
    ld = ""
    if jsonld is not None:
        blocks = jsonld if isinstance(jsonld, list) else [jsonld]
        ld = "".join(
            f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>'
            for b in blocks
        )
    nav = (
        f'<a href="{u()}">Home</a>'
        f'<a href="{u("faq")}">FAQ</a>'
        f'<a href="{u("radar")}">Radar</a>'
        f'<a href="{u()}#compare">Compare</a>'
        f'<a href="{u()}#templates">Templates</a>'
        f'<a href="{u()}#playbooks">Playbooks</a>'
        f'<a href="{u()}#agents">For agents</a>'
        f'<a href="https://github.com/RyanAlberts/best-of-Agent-Harnesses" title="Star this list on GitHub">'
        f'<img src="https://img.shields.io/github/stars/RyanAlberts/best-of-Agent-Harnesses?style=social&label=Star" '
        f'alt="Star best-of-Agent-Harnesses on GitHub" height="20" style="vertical-align:middle"></a>'
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{abs_url(canonical_path)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Best of Agent Harnesses">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{abs_url(canonical_path)}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="alternate" type="application/feed+json" title="Updates" href="{u()}feed.json">
<link rel="icon" type="image/svg+xml" href="{u()}favicon.svg">
<link rel="stylesheet" href="{u()}styles.css">
{ld}
</head>
<body>
<header class="nav"><div class="wrap"><a class="brand" href="{u()}">best-of-Agent-Harnesses</a><nav>{nav}</nav></div></header>
<main class="wrap">
{body}
</main>
<footer class="wrap"><p>Curated by <a href="https://github.com/RyanAlberts">Ryan Alberts</a> ·
<a href="https://creativecommons.org/licenses/by-sa/4.0/">CC-BY-SA-4.0</a> ·
generated from <a href="{u()}harnesses.json">harnesses.json</a> ·
<a href="{u()}llms.txt">llms.txt</a> · stars captured {esc(g.STARS_CAPTURED)}</p></footer>
</body>
</html>
"""


def project_meta(p) -> dict:
    autonomy, recovery = g.axes_for(p.github_id)
    return {
        "name": p.display_name,
        "github_id": p.github_id,
        "slug": g.project_slug(p.github_id),
        "stars": g.stars_for(p.github_id),
        "stars_h": g.format_stars(g.stars_for(p.github_id)),
        "tier": g.tier_of(p),
        "autonomy": autonomy,
        "recovery": recovery,
        "oss": p.oss,
        "oss_signal": g.oss_signal(p.oss),
        "tags": p.tags,
        "description": p.description,
        "example_url": g.examples_for(p.github_id),
        "example_label": g.example_label_for(p.github_id),
        "category_id": next(cid for cid, _, _ in g.CATEGORIES if p in g.PROJECTS[cid]),
    }


# --------------------------------------------------------------------------- #
# Pages
# --------------------------------------------------------------------------- #

def render_index() -> str:
    total = g.count_projects()
    cat_titles = {cid: t for cid, t, _ in g.CATEGORIES}
    rows = []
    for p in sorted(g.ordered_projects(), key=lambda x: g.stars_for(x.github_id), reverse=True):
        m = project_meta(p)
        tagstr = " ".join(m["tags"])
        chips = "".join(f'<span class="chip">{esc(t)}</span>' for t in m["tags"][:5])
        rows.append(
            f'<tr data-name="{esc((m["name"]+" "+m["description"]+" "+tagstr).lower())}" '
            f'data-category="{esc(m["category_id"])}" data-tier="{esc(m["tier"])}" '
            f'data-oss="{"1" if m["oss_signal"]=="open-source" else "0"}" data-stars="{m["stars"]}">'
            f'<td><a href="{u("h/"+m["slug"])}"><strong>{esc(m["name"])}</strong></a><div class="chips">{chips}</div></td>'
            f'<td>{esc(cat_titles[m["category_id"]])}</td>'
            f'<td class="num">{esc(m["stars_h"])}</td>'
            f'<td>{esc(m["tier"])}</td>'
            f'<td>{esc(m["oss"])}</td></tr>'
        )
    cat_opts = "".join(f'<option value="{esc(cid)}">{esc(t)}</option>' for cid, t, _ in g.CATEGORIES)
    tier_opts = "".join(f'<option value="{esc(t)}">{esc(t)}</option>' for t in g.TIER_ORDER)

    use_cases = "".join(
        f'<li><strong>{esc(intent)}</strong> — '
        + ", ".join(
            f'<a href="{u("h/"+g.project_slug(gid))}">{esc(g.find_project(gid).display_name)}</a>'
            for gid in [i for i in ids if not g.is_graveyard(i)][:5]
        )
        + "</li>"
        for intent, ids, _ in g.USE_CASES
    )
    comparisons = "".join(
        f'<li><a href="{u("compare/"+c["slug"])}">{esc(c["title"])}</a> — {esc(c["summary"][:140])}</li>'
        for c in g.comparisons_index()
    )
    templates = "".join(
        f'<li><a href="{u("templates/"+t["slug"])}">{esc(t["title"])}</a> — {esc(t["summary"][:140])}</li>'
        for t in g.templates_index()
    )
    playbooks = "".join(
        f'<li><a href="{u("playbooks/"+pb["slug"])}">{esc(pb["title"])}</a> — {esc(pb["summary"][:140])}</li>'
        for pb in g.playbooks_index()
    )
    cat_cards = "".join(
        f'<a class="card" href="{u("c/"+cid)}"><strong>{esc(t)}</strong>'
        f'<span>{len(g.live_projects(cid))} projects</span></a>'
        for cid, t, _ in g.CATEGORIES
    )
    faq_teaser = "".join(
        f'<li><a href="{u("faq")}#{item["slug"]}">{esc(item["q"])}</a></li>'
        for item in g.build_faq() if item["kind"] != "use-case"
    )

    body = f"""
<section class="hero">
  <h1>Best of Agent Harnesses</h1>
  <p class="lede">Hand-curated, ranked list of {total} AI agent harnesses — the runtimes that
  close the loop between a stateless model and the outside world.</p>
  <p class="stats">{total} harnesses · {len(g.CATEGORIES)} categories · MCP-ready · weekly-rescored</p>
  <pre class="install"><code>claude mcp add agent-harnesses -- uvx agent-harnesses-mcp</code></pre>
  <p><img class="landscape" src="{u()}assets/landscape.svg" alt="The agent-harness landscape: every project plotted by adoption surface against GitHub stars" loading="lazy"></p>
</section>

<section id="browse">
  <h2>Browse all {total}</h2>
  <div class="filters">
    <input id="q" type="search" placeholder="Search name, description, tag…" aria-label="Search harnesses">
    <select id="fcat" aria-label="Category"><option value="">All categories</option>{cat_opts}</select>
    <select id="ftier" aria-label="Tier"><option value="">Any tier</option>{tier_opts}</select>
    <label><input id="foss" type="checkbox"> Open source only</label>
    <span id="count" class="count"></span>
  </div>
  <table id="grid">
    <thead><tr><th data-sort="name">Project</th><th>Category</th>
    <th data-sort="stars" class="num">Stars</th><th>Tier</th><th>OSS</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</section>

<section id="categories"><h2>Categories</h2><div class="cards">{cat_cards}</div></section>

<section id="usecases"><h2>Pick by use case</h2><ul class="usecases">{use_cases}</ul></section>

<section id="compare"><h2>Decision guides</h2><ul>{comparisons}</ul></section>

<section id="templates"><h2>Templates</h2><p>Files you copy into your project to set a harness up safely.</p><ul>{templates}</ul></section>

<section id="playbooks"><h2>Playbooks</h2><p>Step-by-step guides, one task each.</p><ul>{playbooks}</ul></section>

<section id="faq-teaser"><h2>FAQ</h2><ul>{faq_teaser}</ul><p><a href="{u("faq")}">All questions →</a></p></section>

<section id="agents"><h2>For agents</h2>
  <p>This list is published machine-readable so coding and research agents can recommend harnesses directly:</p>
  <ul>
    <li><a href="{u()}harnesses.json">harnesses.json</a> — every project with tier, tags, axes, license, example, and use-case index.</li>
    <li><a href="{u()}llms.txt">llms.txt</a> — the whole list in one agent-readable file.</li>
    <li><a href="{u()}llms-full.txt">llms-full.txt</a>: llms.txt plus the full text of every decision guide, one file.</li>
    <li><a href="{u()}harnesses.jsonld">harnesses.jsonld</a> — schema.org Dataset + ItemList.</li>
    <li><a href="{u()}feed.json">feed.json</a> — JSON Feed of refreshes.</li>
    <li><strong>MCP server</strong>: <code>uvx agent-harnesses-mcp</code> — pick_harness, search_harnesses, get_harness, comparisons.</li>
  </ul>
</section>
<script src="{u()}filter.js"></script>
"""
    jsonld = json.loads(g.generate_jsonld())
    return page(
        "Best of Agent Harnesses — curated, ranked AI agent harnesses",
        f"Hand-curated, ranked list of {total} AI agent harnesses, orchestration frameworks, "
        "and harness techniques. Browse by category, capability, autonomy, and recovery.",
        "", body, jsonld=jsonld,
    )


def render_project(p) -> str:
    m = project_meta(p)
    cat_title = next(t for cid, t, _ in g.CATEGORIES if cid == m["category_id"])
    chips = "".join(f'<span class="chip">{esc(t)}</span>' for t in m["tags"])
    siblings = [
        q for q in sorted(g.live_projects(m["category_id"]), key=lambda x: g.stars_for(x.github_id), reverse=True)
        if q.github_id != p.github_id
    ][:6]
    related = "".join(
        f'<li><a href="{u("h/"+g.project_slug(q.github_id))}">{esc(q.display_name)}</a></li>'
        for q in siblings
    )
    body = f"""
<nav class="crumbs"><a href="{u()}">Home</a> › <a href="{u("c/"+m["category_id"])}">{esc(cat_title)}</a> › {esc(m["name"])}</nav>
<article class="project">
  <h1>{esc(m["name"])}</h1>
  <p class="lede">{esc(m["description"])}</p>
  <div class="chips">{chips}</div>
  <dl class="facts">
    <div><dt>Stars</dt><dd>{esc(m["stars_h"])}</dd></div>
    <div><dt>Adoption surface</dt><dd>{esc(m["tier"])}</dd></div>
    <div><dt>Autonomy</dt><dd>{esc(m["autonomy"])}</dd></div>
    <div><dt>Recovery</dt><dd>{esc(m["recovery"])}</dd></div>
    <div><dt>License</dt><dd>{esc(m["oss"])} {esc(m["oss_signal"])}</dd></div>
    <div><dt>Category</dt><dd><a href="{u("c/"+m["category_id"])}">{esc(cat_title)}</a></dd></div>
  </dl>
  <p class="actions">
    <a class="btn" href="https://github.com/{esc(m["github_id"])}">Repository ↗</a>
    <a class="btn" href="{esc(m["example_url"])}">Example: {esc(m["example_label"])} ↗</a>
  </p>
  <h2>Related in {esc(cat_title)}</h2>
  <ul>{related}</ul>
</article>
"""
    jsonld = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": m["name"],
        "url": f"https://github.com/{m['github_id']}",
        "description": m["description"],
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "Cross-platform",
        "keywords": ", ".join(m["tags"]),
        "isPartOf": {"@type": "Dataset", "name": "Best of Agent Harnesses", "url": abs_url()},
    }
    crumbs = breadcrumb_ld([("Home", abs_url()), (cat_title, abs_url("c/" + m["category_id"])),
                            (m["name"], abs_url("h/" + m["slug"]))])
    return page(
        f"{m['name']} — agent harness · Best of Agent Harnesses",
        f"{m['name']}: {m['description']}",
        f"h/{m['slug']}", body, jsonld=[jsonld, crumbs],
    )


def render_category(cid: str, title: str, subtitle: str) -> str:
    plist = sorted(g.live_projects(cid), key=lambda x: g.stars_for(x.github_id), reverse=True)
    rows = []
    items = []
    for i, p in enumerate(plist, 1):
        m = project_meta(p)
        chips = "".join(f'<span class="chip">{esc(t)}</span>' for t in m["tags"][:5])
        rows.append(
            f'<tr><td class="num">{i}</td>'
            f'<td><a href="{u("h/"+m["slug"])}"><strong>{esc(m["name"])}</strong></a><div class="chips">{chips}</div></td>'
            f'<td class="num">{esc(m["stars_h"])}</td><td>{esc(m["tier"])}</td><td>{esc(m["oss"])}</td>'
            f'<td>{esc(m["description"])}</td></tr>'
        )
        items.append({"@type": "ListItem", "position": i,
                      "url": abs_url("h/" + m["slug"]), "name": m["name"]})
    body = f"""
<nav class="crumbs"><a href="{u()}">Home</a> › {esc(title)}</nav>
<h1>{esc(title)}</h1>
<p class="lede">{esc(subtitle)}</p>
<table><thead><tr><th>#</th><th>Project</th><th class="num">Stars</th><th>Tier</th><th>OSS</th><th>Description</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table>
"""
    jsonld = {"@context": "https://schema.org", "@type": "ItemList",
              "name": title, "numberOfItems": len(items), "itemListElement": items}
    crumbs = breadcrumb_ld([("Home", abs_url()), (title, abs_url("c/" + cid))])
    return page(f"{title} — Best of Agent Harnesses", subtitle, f"c/{cid}", body, jsonld=[jsonld, crumbs])


def render_radar_page() -> str:
    entries = g.radar_entries()
    rows = "".join(
        f'<tr><td><a href="https://github.com/{esc(e["github_id"])}"><strong>{esc(e["github_id"].split("/")[-1])}</strong></a></td>'
        f'<td class="num">{esc(g.format_stars(e["stars"])) if e["stars"] else "—"}</td>'
        f'<td>{esc(e["desc"])}</td><td>{esc(e["via"])}</td></tr>'
        for e in entries
    )
    body = f"""
<nav class="crumbs"><a href="{u()}">Home</a> › On the radar</nav>
<h1>🔭 On the radar</h1>
<p class="lede">Up-and-coming candidates — surfaced by the weekly discovery scan or submitted by the community —
that haven't cleared the curation bar or a vetting pass yet. Stars refresh weekly from the discovery queue;
descriptions are the projects' own, unvetted. Entries graduate into <a href="{u()}">the ranked list</a> or drop off.</p>
<table><thead><tr><th>Project</th><th class="num">Stars</th><th>What it says it is</th><th>Via</th></tr></thead>
<tbody>{rows}</tbody></table>
"""
    return page("On the radar — Best of Agent Harnesses",
                "Up-and-coming agent-harness candidates being watched before they enter the ranked list.",
                "radar", body)


def render_comparison(c: dict) -> str:
    rel = f"comparisons/{c['slug']}.md"
    src = site_links((ROOT / rel).read_text())
    html_body = markdown.markdown(src, extensions=["tables", "fenced_code", "toc"])
    body = f'<nav class="crumbs"><a href="{u()}">Home</a> › <a href="{u()}#compare">Decision guides</a> › {esc(c["title"])}</nav>\n<article class="prose">{html_body}</article>'
    published, modified = source_dates(rel)
    page_url = abs_url("compare/" + c["slug"])
    article = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": c["title"],
        "description": c["summary"],
        "url": page_url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": page_url},
        "datePublished": published,
        "dateModified": modified,
        "author": AUTHOR,
        "publisher": AUTHOR,
        "image": OG_IMAGE,
        "inLanguage": "en",
        "license": "https://creativecommons.org/licenses/by-sa/4.0/",
        "isPartOf": {"@type": "Dataset", "name": "Best of Agent Harnesses", "url": abs_url()},
    }
    crumbs = breadcrumb_ld([("Home", abs_url()), ("Decision guides", abs_url() + "#compare"), (c["title"], page_url)])
    return page(f"{c['title']} — Best of Agent Harnesses", c["summary"], f"compare/{c['slug']}", body,
                jsonld=[article, crumbs])


def render_playbook(pb: dict) -> str:
    rel = f"playbooks/{pb['slug']}.md"
    src = site_links((ROOT / rel).read_text())
    html_body = markdown.markdown(src, extensions=["tables", "fenced_code", "toc"])
    body = f'<nav class="crumbs"><a href="{u()}">Home</a> › <a href="{u()}#playbooks">Playbooks</a> › {esc(pb["title"])}</nav>\n<article class="prose">{html_body}</article>'
    published, modified = source_dates(rel)
    page_url = abs_url("playbooks/" + pb["slug"])
    steps = [m.group(1).strip() for m in re.finditer(r"^## (.+)$", (ROOT / rel).read_text(), re.M)]
    howto = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": pb["title"],
        "description": pb["summary"],
        "url": page_url,
        "datePublished": published,
        "dateModified": modified,
        "author": AUTHOR,
        "inLanguage": "en",
        "license": "https://creativecommons.org/licenses/by-sa/4.0/",
        "step": [{"@type": "HowToStep", "position": i, "name": name, "url": f"{page_url}#{re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')}"}
                 for i, name in enumerate(steps, 1)],
    }
    crumbs = breadcrumb_ld([("Home", abs_url()), ("Playbooks", abs_url() + "#playbooks"), (pb["title"], page_url)])
    return page(f"{pb['title']} — Best of Agent Harnesses", pb["summary"], f"playbooks/{pb['slug']}", body,
                jsonld=[howto, crumbs])


COPY_JS = """<script>
document.querySelectorAll('button.copy').forEach(function(b){
 b.addEventListener('click',function(){
  navigator.clipboard.writeText(document.getElementById(b.dataset.target).textContent).then(function(){
   b.textContent='Copied';setTimeout(function(){b.textContent='Copy'},1500)});
 });
});
</script>"""


def render_template(t: dict) -> str:
    d = ROOT / "templates" / t["slug"]
    readme = (d / "README.md").read_text()
    # Links to the template's own files become anchors to the file blocks below.
    for f in t["files"]:
        readme = readme.replace(f"]({f['path']})", f"](#file-{f['path']})")
    readme = re.sub(r"\]\(\.\./([\w-]+)/?\)", r"](../../templates/\1/)", readme)  # sibling templates
    src = site_links(readme.replace("](../../", "](../"))
    html_body = markdown.markdown(src, extensions=["tables", "fenced_code", "toc"])
    blocks = "".join(
        f'<section class="tfile" id="file-{esc(f["path"])}"><h2><code>{esc(f["path"])}</code></h2>'
        f'<p><button class="copy btn" data-target="src-{i}">Copy</button>'
        f'<a class="btn" href="{esc(f["raw_url"])}">Raw file</a></p>'
        f'<pre><code id="src-{i}">{esc((d / f["path"]).read_text())}</code></pre></section>'
        for i, f in enumerate(t["files"])
    )
    body = (f'<nav class="crumbs"><a href="{u()}">Home</a> › <a href="{u()}#templates">Templates</a> › {esc(t["title"])}</nav>\n'
            f'<article class="prose">{html_body}</article>\n{blocks}\n{COPY_JS}')
    published, modified = source_dates(f"templates/{t['slug']}")
    page_url = abs_url("templates/" + t["slug"])
    code = {
        "@context": "https://schema.org",
        "@type": "SoftwareSourceCode",
        "name": t["title"],
        "description": t["summary"],
        "url": page_url,
        "codeRepository": f"{GITHUB_REPO}/tree/main/templates/{t['slug']}",
        "datePublished": published,
        "dateModified": modified,
        "author": AUTHOR,
        "license": "https://creativecommons.org/licenses/by-sa/4.0/",
        "isPartOf": {"@type": "Dataset", "name": "Best of Agent Harnesses", "url": abs_url()},
    }
    crumbs = breadcrumb_ld([("Home", abs_url()), ("Templates", abs_url() + "#templates"), (t["title"], page_url)])
    return page(f"{t['title']} — Best of Agent Harnesses", t["summary"], f"templates/{t['slug']}", body,
                jsonld=[code, crumbs])


def render_faq() -> str:
    faq = g.build_faq()
    blocks = "".join(
        f'<section class="qa" id="{item["slug"]}"><h2>{esc(item["q"])}</h2><p>{esc(item["a"])}</p>'
        + (f'<p><a href="{u("compare/" + item["more"])}">Sources and the full argument →</a></p>' if item.get("more") else "")
        + "</section>"
        for item in faq
    )
    body = f'<nav class="crumbs"><a href="{u()}">Home</a> › FAQ</nav>\n<h1>Frequently asked questions</h1>\n{blocks}'
    jsonld = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"],
             "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faq
        ],
    }
    return page("FAQ — Best of Agent Harnesses",
                "Answers to common questions about choosing an AI agent harness.",
                "faq", body, jsonld=jsonld)


STYLES = """
:root{--bg:#0d1117;--fg:#e6edf3;--sub:#9ca3af;--accent:#5ac4bf;--card:#161b22;--line:#21262d}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
.nav{border-bottom:1px solid var(--line);background:#0d1117ee;position:sticky;top:0;backdrop-filter:blur(6px);z-index:5}
.nav .wrap{display:flex;align-items:center;justify-content:space-between;padding:12px 20px}
.nav .brand{font-weight:700;color:var(--fg)}
.nav nav a{margin-left:16px;color:var(--sub);font-size:14px}
h1{font-size:2.1rem;line-height:1.2;margin:.4em 0}h2{margin-top:1.6em;border-bottom:1px solid var(--line);padding-bottom:.3em}
.lede{font-size:1.15rem;color:var(--fg)}
.hero .stats{font-weight:600}.install{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px;overflow:auto}
.landscape{max-width:100%;border:1px solid var(--line);border-radius:8px;margin-top:12px}
table{width:100%;border-collapse:collapse;font-size:14px;margin:12px 0}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th[data-sort]{cursor:pointer}th[data-sort]:hover{color:var(--accent)}
.num{text-align:right;white-space:nowrap}
.chip{display:inline-block;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1px 8px;margin:2px 3px 0 0;font-size:11px;color:var(--sub)}
.chips{margin-top:2px}
.filters{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:10px 0}
.filters input[type=search],.filters select{background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:7px 10px}
.filters input[type=search]{flex:1;min-width:220px}.count{color:var(--sub);font-size:13px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}
.card{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px}
.card span{color:var(--sub);font-size:13px}
.crumbs{color:var(--sub);font-size:13px;margin-top:14px}
.facts{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px;margin:16px 0}
.facts dt{color:var(--sub);font-size:12px;text-transform:uppercase;letter-spacing:.04em}.facts dd{margin:0;font-weight:600}
.btn{display:inline-block;background:var(--card);border:1px solid var(--line);border-radius:6px;padding:8px 14px;margin:4px 6px 0 0;color:var(--fg)}
.usecases li,.qa{margin:.4em 0}.qa h2{font-size:1.15rem;border:0;margin-bottom:.2em}
.prose h1{font-size:1.8rem}.prose table{font-size:14px}
pre{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px;overflow:auto;font-size:13px}
.tfile h2{font-size:1.05rem}button.btn{cursor:pointer;font:inherit}
footer{color:var(--sub);font-size:13px;border-top:1px solid var(--line);margin-top:40px;padding:20px}
"""

FILTER_JS = """
(function(){
 var q=document.getElementById('q'),fc=document.getElementById('fcat'),
     ft=document.getElementById('ftier'),fo=document.getElementById('foss'),
     cnt=document.getElementById('count'),tb=document.querySelector('#grid tbody');
 var rows=[].slice.call(tb.querySelectorAll('tr'));
 function apply(){
   var s=(q.value||'').toLowerCase(),c=fc.value,t=ft.value,o=fo.checked,n=0;
   rows.forEach(function(r){
     var ok=(!s||r.dataset.name.indexOf(s)>-1)&&(!c||r.dataset.category===c)
            &&(!t||r.dataset.tier===t)&&(!o||r.dataset.oss==='1');
     r.style.display=ok?'':'none'; if(ok)n++;
   });
   cnt.textContent=n+' / '+rows.length;
 }
 [q,fc,ft,fo].forEach(function(e){e.addEventListener('input',apply)});
 document.querySelectorAll('#grid th[data-sort]').forEach(function(th){
   var key=th.dataset.sort,asc=false;
   th.addEventListener('click',function(){
     asc=!asc;
     rows.sort(function(a,b){
       var x=key==='stars'?+a.dataset.stars:a.dataset.name,
           y=key==='stars'?+b.dataset.stars:b.dataset.name;
       return (x<y?-1:x>y?1:0)*(asc?1:-1);
     });
     rows.forEach(function(r){tb.appendChild(r)});
   });
 });
 apply();
})();
"""


def build() -> dict:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    written = {"projects": 0, "categories": 0, "comparisons": 0, "playbooks": 0, "templates": 0, "other": 0}
    urls = [(abs_url(), g.STARS_CAPTURED)]

    (OUT / "index.html").write_text(render_index())
    (OUT / "styles.css").write_text(STYLES)
    (OUT / "filter.js").write_text(FILTER_JS)
    (OUT / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
        '<rect width="32" height="32" rx="7" fill="#0d1117"/>'
        '<rect x="7" y="7" width="18" height="18" rx="4" fill="#5ac4bf"/></svg>\n'
    )
    (OUT / ".nojekyll").write_text("")

    (OUT / "faq").mkdir()
    (OUT / "faq" / "index.html").write_text(render_faq())
    urls.append((abs_url("faq"), g.STARS_CAPTURED))

    (OUT / "radar").mkdir()
    (OUT / "radar" / "index.html").write_text(render_radar_page())
    urls.append((abs_url("radar"), g.STARS_CAPTURED))

    for p in g.ordered_projects():
        slug = g.project_slug(p.github_id)
        d = OUT / "h" / slug
        d.mkdir(parents=True)
        (d / "index.html").write_text(render_project(p))
        urls.append((abs_url("h/" + slug), g.STARS_CAPTURED))
        written["projects"] += 1

    for cid, title, subtitle in g.CATEGORIES:
        d = OUT / "c" / cid
        d.mkdir(parents=True)
        (d / "index.html").write_text(render_category(cid, title, subtitle))
        urls.append((abs_url("c/" + cid), g.STARS_CAPTURED))
        written["categories"] += 1

    for c in g.comparisons_index():
        d = OUT / "compare" / c["slug"]
        d.mkdir(parents=True)
        (d / "index.html").write_text(render_comparison(c))
        urls.append((abs_url("compare/" + c["slug"]), source_dates(f"comparisons/{c['slug']}.md")[1]))
        written["comparisons"] += 1

    for pb in g.playbooks_index():
        d = OUT / "playbooks" / pb["slug"]
        d.mkdir(parents=True)
        (d / "index.html").write_text(render_playbook(pb))
        urls.append((abs_url("playbooks/" + pb["slug"]), source_dates(f"playbooks/{pb['slug']}.md")[1]))
        written["playbooks"] += 1

    for t in g.templates_index():
        d = OUT / "templates" / t["slug"]
        d.mkdir(parents=True)
        (d / "index.html").write_text(render_template(t))
        urls.append((abs_url("templates/" + t["slug"]), source_dates(f"templates/{t['slug']}")[1]))
        written["templates"] += 1

    # Copy machine-readable surfaces + assets so the site serves them directly.
    for f in ["harnesses.json", "harnesses.jsonld", "llms.txt", "feed.json"]:
        src = ROOT / f
        if src.exists():
            shutil.copy2(src, OUT / f)
            written["other"] += 1
    shutil.copytree(ROOT / "assets", OUT / "assets")
    guides = "\n\n---\n\n".join((ROOT / "comparisons" / f"{c['slug']}.md").read_text() for c in g.comparisons_index())
    playbooks = "\n\n---\n\n".join((ROOT / "playbooks" / f"{pb['slug']}.md").read_text() for pb in g.playbooks_index())
    templates = "\n\n---\n\n".join((ROOT / "templates" / t["slug"] / "README.md").read_text() for t in g.templates_index())
    (OUT / "llms-full.txt").write_text(
        (ROOT / "llms.txt").read_text() + "\n\n---\n\n# Decision guides, full text\n\n" + guides
        + "\n\n---\n\n# Playbooks, full text\n\n" + playbooks
        + "\n\n---\n\n# Templates\n\n" + templates + "\n")
    written["other"] += 1

    # sitemap.xml + robots.txt
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, lastmod in urls:
        sm.append(f"  <url><loc>{url}</loc><lastmod>{lastmod}</lastmod></url>")
    sm.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(sm) + "\n")
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {abs_url()}sitemap.xml\n"
    )
    written["urls"] = len(urls)
    return written


if __name__ == "__main__":
    stats = build()
    print(f"Site built to {OUT}")
    print(f"  {stats['projects']} project pages, {stats['categories']} category pages, "
          f"{stats['comparisons']} comparison pages, {stats['playbooks']} playbook pages, "
          f"{stats['templates']} template pages")
    print(f"  {stats['urls']} URLs in sitemap.xml")
