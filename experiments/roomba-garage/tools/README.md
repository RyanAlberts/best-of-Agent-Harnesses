# reel_processor

A tiny CLI for turning a public Instagram (or TikTok / YouTube Short) reel into
a Markdown report with scene-change stills and a Whisper transcript. Useful
when you want an LLM to reason about a "show me how to build X" video without
re-watching it yourself.

## Why this exists

The agent harness running on Claude Code on the web sits behind a network
policy that blocks `instagram.com`, so the video could not be fetched from
inside that session. Run this locally (or from a session with a more permissive
network policy) and the tool will pull the reel, extract frames, transcribe,
and emit a single `report.md` you can paste back to Claude.

## Install

```sh
pip install yt-dlp openai-whisper
# macOS:   brew install ffmpeg
# Debian:  sudo apt-get install ffmpeg
```

## Run

```sh
python reel_processor.py "https://www.instagram.com/reel/DMs716wy9Zm/" \
    --out ./roomba_reel
open ./roomba_reel/report.md
```

Pass `--no-transcribe` to skip the Whisper step (saves ~30s + a model download
on first run).

## Wrapping as an MCP

The `process_reel(url, out_dir)` function is the natural seam. The thinnest
working MCP server is ~20 lines with
[fastmcp](https://github.com/jlowin/fastmcp):

```python
from fastmcp import FastMCP
from pathlib import Path
from reel_processor import process_reel

mcp = FastMCP("reel-processor")

@mcp.tool()
def process(url: str, out_dir: str = "./reel_out") -> dict:
    return process_reel(url, Path(out_dir))

if __name__ == "__main__":
    mcp.run()
```

That's intentionally left out of this commit — wire it up once you've confirmed
the CLI works on your network.
