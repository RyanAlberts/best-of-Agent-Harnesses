"""Guard the MCP package's SDK pin.

mcp/server.py imports mcp.server.fastmcp, which MCP SDK 2.0 (2026-07-28)
renamed to MCPServer. An unbounded `mcp>=1.2` let 2.x install and crash
`uvx agent-harnesses-mcp` on startup for six weeks (PR #61, issues #95/#96).
Keep the upper bound until server.py is ported to the 2.x API.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = (ROOT / "mcp" / "pyproject.toml").read_text()


def _dependency_specs() -> list:
    m = re.search(r"^dependencies\s*=\s*\[(.*?)\]", PYPROJECT, re.S | re.M)
    assert m, "mcp/pyproject.toml has no dependencies array"
    return re.findall(r'"([^"]+)"', m.group(1))  # quoted specs; a spec may contain commas


def test_mcp_sdk_pinned_below_2():
    specs = [s for s in _dependency_specs() if re.match(r"mcp(?![\w-])", s)]
    assert specs, "mcp is not declared as a dependency"
    assert re.search(r"<\s*2(?:\.0)*(?![\d.])", specs[0]), (
        "mcp must keep an upper bound below 2 until server.py is ported "
        f"off mcp.server.fastmcp: {specs[0]!r}"
    )


def test_server_json_version_matches_pyproject():
    version = re.search(r'^version = "([^"]+)"', PYPROJECT, re.M).group(1)
    manifest = json.loads((ROOT / "server.json").read_text())
    assert manifest["version"] == version
    assert all(p["version"] == version for p in manifest["packages"])
