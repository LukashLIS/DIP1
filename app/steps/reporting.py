from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from app.schema import Segment


def write_report(output_dir: Path, segments: Iterable[Segment]) -> None:
    report_path = output_dir / "segments.json"
    with report_path.open("w", encoding="utf-8") as handle:
        json.dump(
            [segment.__dict__ for segment in segments],
            handle,
            ensure_ascii=False,
            indent=2,
        )
