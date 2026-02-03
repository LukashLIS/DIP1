from __future__ import annotations

from pathlib import Path
from typing import List

from app.schema import PipelineError, Segment


def run_asr(audio_path: Path, segments: List[Segment], models: dict) -> List[Segment]:
    provider = models.get("asr", {}).get("provider")
    if provider is None:
        raise PipelineError("ASR provider not configured.")
    # Placeholder: integrate whisper/faster-whisper here.
    for segment in segments:
        segment.text = "Recognized text"
    return segments
