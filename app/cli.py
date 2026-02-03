from __future__ import annotations

import argparse
from pathlib import Path

from app.config import load_config
from app.pipeline import VideoDubPipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Local video dubbing pipeline")
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    config, models = load_config(args.config)
    pipeline = VideoDubPipeline(config, models)
    output_video = pipeline.run(args.input, args.output)
    print(f"Saved: {output_video}")


if __name__ == "__main__":
    main()
