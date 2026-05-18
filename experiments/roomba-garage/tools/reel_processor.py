#!/usr/bin/env python3
"""
Instagram reel processor.

Downloads a public reel with yt-dlp, samples frames at scene cuts with ffmpeg,
and (optionally) transcribes the audio with whisper. Emits a single Markdown
report containing the caption / description, an ordered list of frame stills,
and the transcript so an LLM (or a human) can reason about what the reel shows.

Usage:
    python reel_processor.py <reel-url> [--out DIR] [--no-transcribe]

Requirements (install once):
    pip install yt-dlp openai-whisper
    apt-get install ffmpeg

This is a thin wrapper, not an MCP. The functions below are deliberately small
so they can be re-exposed via fastmcp / the Python MCP SDK later:

    process_reel(url, out_dir) -> dict
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}", file=sys.stderr)
    subprocess.run(cmd, check=True)


def download(url: str, out_dir: Path) -> tuple[Path, dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    template = str(out_dir / "reel.%(ext)s")
    _run(["yt-dlp", "--write-info-json", "--write-description",
          "-o", template, url])
    video = next(out_dir.glob("reel.*"), None)
    if video is None or video.suffix == ".json":
        video = next(p for p in out_dir.glob("reel.*") if p.suffix not in {".json", ".description"})
    info_path = out_dir / "reel.info.json"
    info = json.loads(info_path.read_text()) if info_path.exists() else {}
    return video, info


def extract_scene_frames(video: Path, out_dir: Path, threshold: float = 0.25) -> list[Path]:
    frames_dir = out_dir / "frames"
    frames_dir.mkdir(exist_ok=True)
    _run([
        "ffmpeg", "-y", "-i", str(video),
        "-vf", f"select='gt(scene,{threshold})',showinfo",
        "-vsync", "vfr",
        str(frames_dir / "frame_%03d.jpg"),
    ])
    frames = sorted(frames_dir.glob("frame_*.jpg"))
    if not frames:
        # Fallback: sample one frame per second.
        _run([
            "ffmpeg", "-y", "-i", str(video),
            "-vf", "fps=1", str(frames_dir / "frame_%03d.jpg"),
        ])
        frames = sorted(frames_dir.glob("frame_*.jpg"))
    return frames


def transcribe(video: Path, out_dir: Path, model: str = "base") -> str:
    try:
        import whisper  # type: ignore
    except ImportError:
        print("openai-whisper not installed; skipping transcription", file=sys.stderr)
        return ""
    print(f"Loading whisper model: {model}", file=sys.stderr)
    result = whisper.load_model(model).transcribe(str(video))
    transcript = result.get("text", "").strip()
    (out_dir / "transcript.txt").write_text(transcript + "\n")
    return transcript


def write_report(out_dir: Path, info: dict, frames: list[Path], transcript: str) -> Path:
    title = info.get("title") or info.get("description", "").split("\n", 1)[0] or "Reel"
    lines = [f"# {title}", ""]
    if uploader := info.get("uploader"):
        lines.append(f"- Uploader: **{uploader}**")
    if duration := info.get("duration"):
        lines.append(f"- Duration: {duration:.1f}s")
    if webpage := info.get("webpage_url"):
        lines.append(f"- Source: {webpage}")
    lines.append("")
    if description := info.get("description"):
        lines.append("## Caption")
        lines.append("")
        lines.append(description.strip())
        lines.append("")
    if transcript:
        lines.append("## Transcript")
        lines.append("")
        lines.append(transcript)
        lines.append("")
    if frames:
        lines.append("## Frames")
        lines.append("")
        for f in frames:
            lines.append(f"![{f.name}]({f.relative_to(out_dir)})")
        lines.append("")
    report = out_dir / "report.md"
    report.write_text("\n".join(lines))
    return report


def process_reel(url: str, out_dir: Path, do_transcribe: bool = True) -> dict:
    for tool in ("yt-dlp", "ffmpeg"):
        if not shutil.which(tool):
            raise RuntimeError(f"missing required tool: {tool}")
    video, info = download(url, out_dir)
    frames = extract_scene_frames(video, out_dir)
    transcript = transcribe(video, out_dir) if do_transcribe else ""
    report = write_report(out_dir, info, frames, transcript)
    return {"video": str(video), "frames": [str(f) for f in frames],
            "transcript": transcript, "report": str(report)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--out", default="reel_out", type=Path)
    ap.add_argument("--no-transcribe", action="store_true")
    args = ap.parse_args()
    result = process_reel(args.url, args.out, do_transcribe=not args.no_transcribe)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
