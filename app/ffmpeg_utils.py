from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import List

from app.schema import PipelineError


def require_tool(tool: str) -> None:
    if shutil.which(tool) is None:
        raise PipelineError(f"Required tool '{tool}' not found in PATH.")


def run(cmd: List[str], step: str) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise PipelineError(
            f"Failed to {step}. Command: {' '.join(cmd)}\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )


def extract_audio(input_video: Path, audio_path: Path, sample_rate: int) -> None:
    require_tool("ffmpeg")
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_video),
        "-vn",
        "-ac",
        "1",
        "-ar",
        str(sample_rate),
        str(audio_path),
    ]
    run(cmd, "extract audio")


def generate_silence(output_audio: Path, duration: float, sample_rate: int) -> None:
    require_tool("ffmpeg")
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"anullsrc=r={sample_rate}:cl=mono",
        "-t",
        str(duration),
        str(output_audio),
    ]
    run(cmd, "generate placeholder audio")


def mux_audio(input_video: Path, audio_path: Path, output_video: Path) -> None:
    require_tool("ffmpeg")
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_video),
        "-i",
        str(audio_path),
        "-c:v",
        "copy",
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-shortest",
        str(output_video),
    ]
    run(cmd, "mux audio")
