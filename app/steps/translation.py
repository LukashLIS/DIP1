from __future__ import annotations

from typing import List

from app.schema import PipelineError, Segment


def run_translation(segments: List[Segment], models: dict) -> List[Segment]:
    provider = models.get("translation", {}).get("provider")
    if provider is None:
        raise PipelineError("Translation provider not configured.")
    # Placeholder: integrate translation model.
    for segment in segments:
        segment.text = f"[RU] {segment.text}"
    return segments
