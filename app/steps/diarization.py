from __future__ import annotations

from pathlib import Path
from typing import List

from app.schema import PipelineError, Segment


def run_diarization(audio_path: Path, models: dict) -> List[Segment]:
    provider = models.get("diarization", {}).get("provider")
    if provider is None:
        raise PipelineError("Diarization provider not configured.")
    # Placeholder: integrate pyannote or whisperx diarization here.
    return [Segment(speaker="S1", start=0.0, end=1.0, text="")]
