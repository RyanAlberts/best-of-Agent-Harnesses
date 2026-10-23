"""Tests for mcp/server.py (the agent-harnesses MCP server).

CI installs only pytest+markdown, and the repo's mcp/ directory would shadow
the real `mcp` SDK on sys.path anyway — so the SDK is stubbed and server.py is
loaded straight from its file path.
"""
import importlib.util
import json
import sys
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _load_server():
    fastmcp = types.ModuleType("mcp.server.fastmcp")

    class FastMCP:
        def __init__(self, name):
            self.tools = {}  # tool name -> annotations it was registered with

        def tool(self, name=None, description=None, annotations=None):
            def register(fn):
                self.tools[name or fn.__name__] = annotations
                return fn
            return register

        def run(self):
            pass

    fastmcp.FastMCP = FastMCP
    server_pkg = types.ModuleType("mcp.server")
    server_pkg.fastmcp = fastmcp
    mcp_types = types.ModuleType("mcp.types")
    mcp_types.ToolAnnotations = types.SimpleNamespace
    mcp_pkg = types.ModuleType("mcp")
    mcp_pkg.server = server_pkg
    mcp_pkg.types = mcp_types
    stubs = {"mcp": mcp_pkg, "mcp.server": server_pkg, "mcp.server.fastmcp": fastmcp,
             "mcp.types": mcp_types}
    saved = {k: sys.modules.get(k) for k in stubs}
    sys.modules.update(stubs)
    try:
        spec = importlib.util.spec_from_file_location("ah_mcp_server", ROOT / "mcp" / "server.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v
    return mod


@pytest.fixture(scope="module")
def server():
    return _load_server()


def _proj(name, gid, stars, tier_rank, autonomy_rank, recovery_rank, **over):
    tiers = ["super simple", "mostly simple", "slightly complex", "complex"]
    a_tiers = ["step-gated", "checkpoint-gated", "bounded", "headless"]
    r_tiers = ["none", "retry", "resumable", "durable"]
    p = {
        "name": name, "github_id": gid, "url": f"https://github.com/{gid}",
        "page_url": "", "stars": stars,
        "tier": tiers[tier_rank - 1], "tier_rank": tier_rank,
        "autonomy": a_tiers[autonomy_rank - 1] if autonomy_rank else "n/a",
        "autonomy_rank": autonomy_rank,
        "recovery": r_tiers[recovery_rank - 1] if recovery_rank else "n/a",
        "recovery_rank": recovery_rank,
        "license_signal": "open-source", "category": "personal",
        "category_title": "Personal agents",
        "description": "An always-on personal agent.", "tags": ["python"],
    }
    p.update(over)
    return p


DATA = {
    "meta": {
        "url": "https://example.com/list", "stars_captured": "2026-07-19",
        "tiers": ["super simple", "mostly simple", "slightly complex", "complex"],
        "autonomy_tiers": ["step-gated", "checkpoint-gated", "bounded", "headless"],
        "recovery_tiers": ["none", "retry", "resumable", "durable"],
    },
    "projects": [
        _proj("AlphaClaw", "alpha/alphaclaw", 50000, 4, 4, 4, deep_dive={
            "researched": "2026-07-19",
            "tooling_sandboxing": {"rating": "strong", "rank": 3, "detail": "d", "evidence": "https://e.com"},
            "context_memory": {"rating": "basic", "rank": 2, "detail": "d", "evidence": "https://e.com"},
            "lifecycle_hooks": {"rating": "full", "rank": 3, "detail": "d", "evidence": "https://e.com"},
            "prompt_optimization": {"rating": "unknown", "rank": 0, "detail": "d", "evidence": ""},
            "build_vs_buy": {"tier": 2, "label": "blueprint", "detail": "d", "evidence": "https://e.com"},
        }),
        _proj("BetaPilot", "beta/betapilot", 12000, 2, 3, 2, deep_dive={
            "researched": "2026-07-19",
            "tooling_sandboxing": {"rating": "basic", "rank": 2, "detail": "d", "evidence": "https://e.com"},
            "context_memory": {"rating": "strong", "rank": 3, "detail": "d", "evidence": "https://e.com"},
            "lifecycle_hooks": {"rating": "none", "rank": 1, "detail": "d", "evidence": "https://e.com"},
            "prompt_optimization": {"rating": "unknown", "rank": 0, "detail": "d", "evidence": ""},
            "build_vs_buy": {"tier": 1, "label": "build", "detail": "d", "evidence": "https://e.com"},
        }),
        _proj("GammaKit", "gamma/gammakit", 12000, 2, 0, 0, deep_dive=None),
    ],
    "graveyard": [
        {"github_id": "bad/starfarm", "name": "starfarm", "last_stars": 90000,
         "reason": "suspected star manipulation", "since": "2026-07"},
    ],
    "comparisons": [
        {"slug": "alphaclaw-vs-betapilot", "title": "AlphaClaw vs BetaPilot",
         "summary": "the always-on personal-agent debate",
         "raw_url": "https://example.com/raw"},
    ],
    "use_cases": [],
}


def test_every_tool_is_read_only(server):
    # No tool writes anything, and every tool calls data(), which fetches
    # harnesses.json from GitHub when installed from PyPI.
    assert server.mcp.tools, "no tools registered"
    for name, ann in server.mcp.tools.items():
        assert getattr(ann, "readOnlyHint", None) is True, name
        assert getattr(ann, "openWorldHint", None) is True, name


def test_compare_two(server):
    server._data = DATA
    out = json.loads(server.compare(["alpha/alphaclaw", "beta/betapilot"]))
    assert [p["github_id"] for p in out["projects"]] == ["alpha/alphaclaw", "beta/betapilot"]
    assert out["edges"]["most_stars"] == ["AlphaClaw"]
    assert out["edges"]["simplest_adoption"] == ["BetaPilot"]
    assert out["edges"]["highest_autonomy"] == ["AlphaClaw"]
    assert out["edges"]["strongest_recovery"] == ["AlphaClaw"]
    assert out["warnings"] == []
    assert out["see_also"]["slug"] == "alphaclaw-vs-betapilot"


def test_compare_tie_and_unrated_axes(server):
    server._data = DATA
    out = json.loads(server.compare(["beta/betapilot", "gamma/gammakit"]))
    assert out["edges"]["most_stars"] == ["BetaPilot", "GammaKit"]
    assert out["edges"]["simplest_adoption"] == ["BetaPilot", "GammaKit"]
    # GammaKit is unrated on autonomy/recovery: no edge is declared against n/a.
    assert "highest_autonomy" not in out["edges"]
    assert "strongest_recovery" not in out["edges"]


def test_compare_graveyard_warning(server):
    server._data = DATA
    out = json.loads(server.compare(["alpha/alphaclaw", "bad/starfarm"]))
    assert len(out["projects"]) == 1
    assert len(out["warnings"]) == 1
    assert "star manipulation" in out["warnings"][0]["warning"]
    assert out["warnings"][0]["last_stars"] == 90000


def test_compare_unknown_id(server):
    server._data = DATA
    out = json.loads(server.compare(["alpha/alphaclaw", "nope/missing"]))
    assert "nope/missing" in out["error"]
    assert "search_harnesses" in out["hint"]


def test_compare_arity(server):
    server._data = DATA
    assert "error" in json.loads(server.compare(["alpha/alphaclaw"]))
    assert "error" in json.loads(server.compare(
        ["a/a", "b/b", "c/c", "d/d", "e/e"]))


def test_compare_deep_dive_edges(server):
    server._data = DATA
    out = json.loads(server.compare(["alpha/alphaclaw", "beta/betapilot"]))
    assert out["edges"]["strongest_sandboxing"] == ["AlphaClaw"]
    assert out["edges"]["strongest_memory"] == ["BetaPilot"]
    assert out["edges"]["fullest_lifecycle_hooks"] == ["AlphaClaw"]
    # Both unknown on prompt_optimization: no edge declared.
    assert "most_prompt_optimization" not in out["edges"]
    assert out["projects"][0]["deep_dive"]["build_vs_buy"]["label"] == "blueprint"


def test_compare_unrated_deep_dive_omitted(server):
    server._data = DATA
    # GammaKit has no deep_dive: axes with <2 rated projects declare no edge.
    out = json.loads(server.compare(["alpha/alphaclaw", "gamma/gammakit"]))
    assert "strongest_sandboxing" not in out["edges"]
    assert out["projects"][1]["deep_dive"] is None


def test_compare_for(server):
    server._data = DATA
    out = json.loads(server.compare_for("always-on personal agent", limit=2))
    assert out["use_case"] == "always-on personal agent"
    assert len(out["projects"]) == 2
    assert out["projects"][0]["name"] == "AlphaClaw"  # stars tiebreak on equal overlap
    assert set(out["why_picked"]) == {p["name"] for p in out["projects"]}
    assert "edges" in out


def test_compare_for_no_match(server):
    server._data = DATA
    out = json.loads(server.compare_for("quantum blockchain farming"))
    assert "message" in out and "projects" not in out


def test_compare_real_data(server):
    server._data = None  # force a reload from the repo's harnesses.json
    out = json.loads(server.compare(["openclaw/openclaw", "NousResearch/hermes-agent"]))
    assert len(out["projects"]) == 2
    assert out["see_also"]["slug"] == "openclaw-vs-hermes"
    assert out["edges"]["most_stars"]


def test_pick_infrastructure_curated_and_level(server):
    server._data = DATA
    out = json.loads(server.pick_infrastructure(
        "an always-on personal agent runtime", include_live_search=False))
    assert out["level"]["id"] == "harness"
    assert out["level"]["how"] == "inferred"
    assert out["curated_picks"], "curated picks must come from the list"
    assert out["live_discovery"]["status"] == "skipped"


def test_pick_infrastructure_unknown_level_errors(server):
    server._data = DATA
    out = json.loads(server.pick_infrastructure("anything", level="nonsense"))
    assert "error" in out
    assert "sandboxing" in out["levels"]


def test_pick_infrastructure_live_dedups_and_labels(server, monkeypatch):
    server._data = DATA

    def fake_http(url, timeout=8):
        if "api.github.com" in url:
            return {"items": [
                {"full_name": "alpha/alphaclaw", "html_url": "u", "stargazers_count": 1,
                 "license": None, "pushed_at": "2026-08-01T00:00:00Z",
                 "description": "already listed"},
                {"full_name": "new/shiny", "html_url": "https://github.com/new/shiny",
                 "stargazers_count": 321, "license": {"spdx_id": "MIT"},
                 "pushed_at": "2026-08-01T00:00:00Z", "description": "brand new sandbox"},
            ]}
        return {"hits": [{"title": "Shiny sandbox launches", "points": 99,
                          "created_at": "2026-08-01T12:00:00Z", "objectID": "1"}]}

    monkeypatch.setattr(server, "_http_json", fake_http)
    out = json.loads(server.pick_infrastructure("sandboxed code execution"))
    assert out["level"]["id"] == "sandboxing"
    gids = [r["github_id"] for r in out["live_discovery"]["github_new"]]
    assert "alpha/alphaclaw" not in gids and "new/shiny" in gids
    assert all(r["status"] == "unvetted" for r in out["live_discovery"]["github_new"])
    assert out["live_discovery"]["community_signals"][0]["points"] == 99


def test_pick_infrastructure_degrades_offline(server, monkeypatch):
    server._data = DATA

    def boom(url, timeout=8):
        raise OSError("offline")

    monkeypatch.setattr(server, "_http_json", boom)
    out = json.loads(server.pick_infrastructure("agent memory layer"))
    assert out["live_discovery"]["status"] == "unavailable"
    assert out["live_discovery"]["github_error"].startswith("OSError")
    assert "curated_picks" in out


def test_templates_and_playbooks_tools(server):
    import generate
    server._data = dict(DATA, templates=generate.templates_index(), playbooks=generate.playbooks_index())
    listed = json.loads(server.list_templates())["templates"]
    assert "agents-md" in [t["slug"] for t in listed]
    t = json.loads(server.get_template("agents-md"))
    files = {f["path"]: f["content"] for f in t["files"]}
    assert files["CLAUDE.md"].startswith("@AGENTS.md") and "## Boundaries" in files["AGENTS.md"]
    assert t["readme"].startswith("# One AGENTS.md")
    assert "available" in json.loads(server.get_template("nope"))
    assert json.loads(server.list_playbooks())["playbooks"]
    assert server.get_playbook("build-your-own-agent-harness").startswith("# Build your own agent harness")


def test_ranked_skips_archived_projects(server):
    d = json.loads((ROOT / "harnesses.json").read_text())
    names = [p["name"] for _, p, _ in server._ranked(d, "drag and drop no-code flow builder")]
    assert "Flowise" not in names


def test_whats_new(server, tmp_path, monkeypatch):
    weeks = [{"date": "2026-10-25"}, {"date": "2026-10-18"}, {"date": "2026-10-11"}]
    changes = tmp_path / "changes.json"
    changes.write_text(json.dumps({"weeks": weeks}))
    monkeypatch.setattr(server, "_fetch_text", lambda local, url: changes.read_text())
    assert [w["date"] for w in json.loads(server.whats_new())["weeks"]] == ["2026-10-25", "2026-10-18", "2026-10-11"]
    assert [w["date"] for w in json.loads(server.whats_new(limit=1))["weeks"]] == ["2026-10-25"]
    assert [w["date"] for w in json.loads(server.whats_new(since="2026-10-11"))["weeks"]] == ["2026-10-25", "2026-10-18"]


def test_skills_tools(server):
    import generate
    server._data = DATA  # a harnesses.json from before skills existed
    assert json.loads(server.list_skills())["skills"] == []
    skills = generate.skills_index()
    server._data = dict(DATA, skills=skills)
    listed = json.loads(server.list_skills())["skills"]
    assert listed and [s["name"] for s in listed] == [s["name"] for s in skills]
    name = listed[0]["name"]
    got = json.loads(server.get_skill(name))
    skill_md = next(f["content"] for f in got["files"] if f["path"] == f".claude/skills/{name}/SKILL.md")
    assert skill_md.startswith(f"---\nname: {name}\n")
    agents = json.loads(server.get_skill(name, target="agents"))
    assert all(f["path"].startswith(f".agents/skills/{name}/") for f in agents["files"])
    assert "available" in json.loads(server.get_skill("nope"))
    assert "available" in json.loads(server.get_skill(name, target="nope"))
