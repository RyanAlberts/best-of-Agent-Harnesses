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
            pass

        def tool(self):
            return lambda fn: fn

        def run(self):
            pass

    fastmcp.FastMCP = FastMCP
    server_pkg = types.ModuleType("mcp.server")
    server_pkg.fastmcp = fastmcp
    mcp_pkg = types.ModuleType("mcp")
    mcp_pkg.server = server_pkg
    saved = {k: sys.modules.get(k) for k in ("mcp", "mcp.server", "mcp.server.fastmcp")}
    sys.modules.update({"mcp": mcp_pkg, "mcp.server": server_pkg, "mcp.server.fastmcp": fastmcp})
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
        _proj("AlphaClaw", "alpha/alphaclaw", 50000, 4, 4, 4),
        _proj("BetaPilot", "beta/betapilot", 12000, 2, 3, 2),
        _proj("GammaKit", "gamma/gammakit", 12000, 2, 0, 0),
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


def test_compare_real_data(server):
    server._data = None  # force a reload from the repo's harnesses.json
    out = json.loads(server.compare(["openclaw/openclaw", "NousResearch/hermes-agent"]))
    assert len(out["projects"]) == 2
    assert out["see_also"]["slug"] == "openclaw-vs-hermes"
    assert out["edges"]["most_stars"]
