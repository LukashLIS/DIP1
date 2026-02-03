from __future__ import annotations

import shutil
from pathlib import Path

from app.ffmpeg_utils import extract_audio, mux_audio
from app.schema import PipelineConfig
from app.steps.asr import run_asr
from app.steps.diarization import run_diarization
from app.steps.reporting import write_report
from app.steps.translation import run_translation
from app.steps.tts import run_tts
from app.steps.understanding import run_understanding


class VideoDubPipeline:
    def __init__(self, config: PipelineConfig, models: dict):
        self.config = config
        self.models = models

    def run(self, input_video: Path, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        tmp_dir = self.config.tmp_dir
        tmp_dir.mkdir(parents=True, exist_ok=True)

        audio_path = tmp_dir / "audio.wav"
        extract_audio(input_video, audio_path, self.config.sample_rate)

        segments = run_diarization(audio_path, self.models)
        segments = run_asr(audio_path, segments, self.models)
        segments = run_understanding(segments, self.models)
        segments = run_translation(segments, self.models)

        tts_audio = tmp_dir / "tts.wav"
        run_tts(segments, tts_audio, self.models, self.config.sample_rate)

        output_video = output_dir / f"{input_video.stem}_ru.mp4"
        mux_audio(input_video, tts_audio, output_video)

        write_report(output_dir, segments)

        if not self.config.keep_intermediate:
            shutil.rmtree(tmp_dir, ignore_errors=True)

        return output_video
