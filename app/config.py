from __future__ import annotations

from pathlib import Path

import yaml

from app.schema import PipelineConfig


def load_config(config_path: Path) -> tuple[PipelineConfig, dict]:
    with config_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)

    pipeline_raw = raw.get("pipeline", {})
    io_raw = raw.get("io", {})

    config = PipelineConfig(
        sample_rate=int(pipeline_raw.get("sample_rate", 16000)),
        language=str(pipeline_raw.get("language", "auto")),
        target_language=str(pipeline_raw.get("target_language", "ru")),
        keep_timestamps=bool(pipeline_raw.get("keep_timestamps", True)),
        tmp_dir=Path(io_raw.get("tmp_dir", "./tmp")),
        keep_intermediate=bool(io_raw.get("keep_intermediate", False)),
    )
    models = raw.get("models", {})
    return config, models
