"""End-to-end test of the hosted mode: start `mcp/server.py --http` on a free
local port, then speak the MCP wire protocol to it with plain urllib, the way
a remote connector (Claude.ai, ChatGPT, Cursor) does.

Needs the real MCP SDK in this interpreter (CI installs it); skipped without it.
"""
import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SERVER = ROOT / "mcp" / "server.py"


def _has_sdk() -> bool:
    # Run from mcp/ so the repo's own mcp/ folder can't shadow the SDK.
    return subprocess.run([sys.executable, "-c", "import mcp.server.fastmcp, uvicorn"],
                          cwd=ROOT / "mcp", capture_output=True).returncode == 0


pytestmark = pytest.mark.skipif(not _has_sdk(), reason="needs the MCP SDK: pip install 'mcp>=1.7,<2'")


@pytest.fixture(scope="module")
def url():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    proc = subprocess.Popen([sys.executable, str(SERVER), "--http"],
                            env=dict(os.environ, PORT=str(port)),
                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    deadline = time.monotonic() + 30
    while True:
        if proc.poll() is not None:
            pytest.fail("server exited: " + proc.stderr.read().decode()[-2000:])
        try:
            socket.create_connection(("127.0.0.1", port), timeout=1).close()
            break
        except OSError:
            if time.monotonic() > deadline:
                proc.kill()
                pytest.fail("server did not start listening within 30s")
            time.sleep(0.2)
    yield f"http://127.0.0.1:{port}/mcp"
    proc.terminate()
    proc.wait(timeout=10)


def _rpc(url: str, method: str, params: dict | None = None, host: str = "") -> dict:
    body = {"jsonrpc": "2.0", "id": 1, "method": method}
    if params is not None:
        body["params"] = params
    headers = {"Content-Type": "application/json",
               "Accept": "application/json, text/event-stream",
               "MCP-Protocol-Version": "2025-06-18"}
    if host:
        headers["Host"] = host
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        text = r.read().decode()
        sse = r.headers.get("Content-Type", "").startswith("text/event-stream")
    if sse:  # one JSON-RPC message per `data:` line
        text = next(line[5:] for line in text.splitlines() if line.startswith("data:"))
    msg = json.loads(text)
    assert "error" not in msg, msg
    return msg["result"]


def test_initialize_from_a_public_hostname(url):
    # A hosted server sees its public hostname in Host; the SDK's localhost-only
    # default would reject it before the request reaches the MCP layer.
    result = _rpc(url, "initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                      "clientInfo": {"name": "pytest", "version": "0"}},
                  host="agent-harnesses-mcp.example.com")
    assert result["serverInfo"]["name"] == "agent-harnesses"
    assert "tools" in result["capabilities"]


def test_lists_every_tool_read_only(url):
    tools = _rpc(url, "tools/list")["tools"]
    declared = re.findall(r"@mcp\.tool\([^)]*\)\s*\ndef (\w+)", SERVER.read_text())
    assert sorted(t["name"] for t in tools) == sorted(declared)
    assert len(declared) >= 17
    assert all(t["annotations"]["readOnlyHint"] for t in tools)


def test_calls_a_tool(url):
    # Stateless mode: a tools/call needs no session from an earlier initialize.
    result = _rpc(url, "tools/call", {"name": "list_categories", "arguments": {}})
    assert not result.get("isError"), result
    assert json.loads(result["content"][0]["text"])["categories"]
