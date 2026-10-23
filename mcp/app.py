"""Vercel entrypoint for the hosted connector: Vercel imports `app` (an ASGI
app) from this file, set by [tool.vercel] in pyproject.toml. The Vercel
project's root directory is mcp/, so server.py fetches the list from GitHub
and refetches it hourly. Deploy steps: "Hosted connector (maintainer
runbook)" in README.md."""
from server import http_app

app = http_app()
