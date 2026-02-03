from __future__ import annotations

from typing import List

from app.schema import PipelineError, Segment


def run_understanding(segments: List[Segment], models: dict) -> List[Segment]:
    provider = models.get("understanding", {}).get("provider")
    if provider is None:
        raise PipelineError("Understanding provider not configured.")
    # Placeholder: use LLM to normalize/clean text for better translation.
    return segments
