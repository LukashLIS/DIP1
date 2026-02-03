from __future__ import annotations

from typing import Iterable

from app.ffmpeg_utils import generate_silence
from app.schema import PipelineError, Segment


def run_tts(segments: Iterable[Segment], output_audio, models: dict, sample_rate: int) -> None:
    provider = models.get("tts", {}).get("provider")
    if provider is None:
        raise PipelineError("TTS provider not configured.")
    # Placeholder: generate audio and align timings.
    generate_silence(output_audio, duration=1.0, sample_rate=sample_rate)
