from __future__ import annotations

from pathlib import Path

import gradio as gr

from app.config import load_config
from app.pipeline import VideoDubPipeline
from app.schema import PipelineConfig, PipelineError


def run_pipeline(
    config_path: str,
    input_video: str,
    output_dir: str,
    output_filename: str,
    sample_rate: int,
    language: str,
    target_language: str,
    keep_timestamps: bool,
    tmp_dir: str,
    keep_intermediate: bool,
    diarization_model: str,
    asr_model: str,
    understanding_model: str,
    translation_model: str,
    tts_model: str,
) -> str:
    if not input_video or not output_dir or not output_filename:
        return "Please provide input video, output directory, and filename."

    try:
        if config_path:
            config, models = load_config(Path(config_path))
        else:
            config = PipelineConfig(
                sample_rate=sample_rate,
                language=language,
                target_language=target_language,
                keep_timestamps=keep_timestamps,
                tmp_dir=Path(tmp_dir),
                keep_intermediate=keep_intermediate,
            )
            models = {}
        provider_defaults = {
            "diarization": "pyannote",
            "asr": "faster-whisper",
            "understanding": "transformers",
            "translation": "transformers",
            "tts": "coqui",
        }
        model_overrides = {
            "diarization": diarization_model,
            "asr": asr_model,
            "understanding": understanding_model,
            "translation": translation_model,
            "tts": tts_model,
        }
        for key, model_name in model_overrides.items():
            if model_name:
                models.setdefault(key, {})
                models[key].setdefault("provider", provider_defaults.get(key))
                models[key]["model"] = model_name
        pipeline = VideoDubPipeline(config, models)
        output_video = pipeline.run(
            Path(input_video),
            Path(output_dir),
            output_name=output_filename,
        )
        return f"Saved: {output_video}"
    except (PipelineError, FileNotFoundError, ValueError) as error:
        return f"Error: {error}"


def build_app() -> gr.Blocks:
    with gr.Blocks(title="Local Video Dubbing") as demo:
        gr.Markdown(
            "# Local Video Dubbing\n"
            "Run the local pipeline to translate and dub video audio into Russian."
        )
        config_path = gr.File(
            label="Config file (optional)",
            file_types=[".yaml", ".yml"],
            type="filepath",
        )
        input_video = gr.File(label="Input video", file_types=["video"], type="filepath")
        output_dir = gr.File(
            label="Output directory",
            file_count="directory",
            type="filepath",
        )
        output_filename = gr.Textbox(label="Output filename", value="output_ru.mp4")
        gr.Markdown("### Pipeline settings (used when no config file is provided)")
        sample_rate = gr.Number(label="Sample rate", value=16000, precision=0)
        language = gr.Textbox(label="Source language", value="auto")
        target_language = gr.Textbox(label="Target language", value="ru")
        keep_timestamps = gr.Checkbox(label="Keep timestamps", value=True)
        tmp_dir = gr.Textbox(label="Temp directory", value="./tmp")
        keep_intermediate = gr.Checkbox(label="Keep intermediate files", value=False)
        gr.Markdown("### Model selection (optional)")
        diarization_model = gr.Dropdown(
            label="Diarization model",
            choices=["pyannote/speaker-diarization"],
            value="pyannote/speaker-diarization",
            allow_custom_value=True,
        )
        asr_model = gr.Dropdown(
            label="ASR model",
            choices=["large-v3", "medium", "small"],
            value="large-v3",
            allow_custom_value=True,
        )
        understanding_model = gr.Dropdown(
            label="Understanding model",
            choices=["facebook/mbart-large-50-many-to-many-mmt"],
            value="facebook/mbart-large-50-many-to-many-mmt",
            allow_custom_value=True,
        )
        translation_model = gr.Dropdown(
            label="Translation model",
            choices=["facebook/nllb-200-distilled-600M"],
            value="facebook/nllb-200-distilled-600M",
            allow_custom_value=True,
        )
        tts_model = gr.Dropdown(
            label="TTS model",
            choices=["tts_models/multilingual/multi-dataset/xtts_v2"],
            value="tts_models/multilingual/multi-dataset/xtts_v2",
            allow_custom_value=True,
        )
        run_button = gr.Button("Run pipeline")
        output = gr.Textbox(label="Status", lines=4)

        run_button.click(
            run_pipeline,
            inputs=[
                config_path,
                input_video,
                output_dir,
                output_filename,
                sample_rate,
                language,
                target_language,
                keep_timestamps,
                tmp_dir,
                keep_intermediate,
                diarization_model,
                asr_model,
                understanding_model,
                translation_model,
                tts_model,
            ],
            outputs=[output],
        )

    return demo


def main() -> None:
    app = build_app()
    app.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
