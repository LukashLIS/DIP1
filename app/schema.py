from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Segment:
    speaker: str
    start: float
    end: float
    text: str


@dataclass
class PipelineConfig:
    sample_rate: int
    language: str
    target_language: str
    keep_timestamps: bool
    tmp_dir: Path
    keep_intermediate: bool


class PipelineError(RuntimeError):
    pass
