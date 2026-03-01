"""
Parakeet-MLX STT — Speech-to-text on Apple Silicon.

Uses mlx-community/parakeet-tdt-0.6b-v2 via parakeet-mlx.
25 languages, auto-detect, built-in chunking, beam decoding.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Optional


# Supported output formats
OUTPUT_FORMATS = ("text", "srt", "vtt", "json")


def transcribe(
    audio_path: str | Path,
    language: Optional[str] = None,
    output_format: str = "text",
    beam_size: int = 1,
    word_timestamps: bool = False,
    verbose: bool = False,
) -> str:
    """
    Transcribe audio using Parakeet-MLX.

    Args:
        audio_path: Path to audio file (WAV, MP3, FLAC, etc.).
        language: Language code or None for auto-detect.
        output_format: Output format — 'text', 'srt', 'vtt', or 'json'.
        beam_size: Beam size for decoding (1=greedy, 3=balanced, 5=best).
        word_timestamps: Include word-level timestamps (SRT/VTT only).
        verbose: Print processing details.

    Returns:
        Transcribed text (or SRT/VTT/JSON string).

    Raises:
        FileNotFoundError: If audio file doesn't exist.
        RuntimeError: If transcription fails.
    """
    audio_path = Path(audio_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    if output_format not in OUTPUT_FORMATS:
        raise ValueError(
            f"Unknown format '{output_format}'. Available: {', '.join(OUTPUT_FORMATS)}"
        )

    if verbose:
        size_mb = audio_path.stat().st_size / (1024 * 1024)
        print(f"🎧 Transcribing: {audio_path.name} ({size_mb:.1f} MB)")
        print(f"   Format: {output_format} | Beam: {beam_size}")

    t0 = time.perf_counter()

    try:
        import subprocess
        import json as json_mod

        cmd = ["parakeet-mlx", str(audio_path)]

        if language:
            cmd.extend(["--language", language])

        if beam_size > 1:
            cmd.extend(["--decoding", "beam", "--beam-size", str(beam_size)])

        if output_format in ("srt", "vtt"):
            cmd.extend(["--format", output_format])
            if word_timestamps:
                cmd.append("--highlight-words")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,  # 10 min max
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"parakeet-mlx failed (exit {result.returncode}): {result.stderr.strip()}"
            )

        text = result.stdout.strip()

    except FileNotFoundError:
        raise RuntimeError(
            "parakeet-mlx is not installed. Run: pip install parakeet-mlx"
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("Transcription timed out (>10 min)")

    elapsed = time.perf_counter() - t0

    if verbose:
        words = len(text.split()) if output_format == "text" else "—"
        print(f"   ✅ Transcribed in {elapsed:.1f}s ({words} words)")

    if output_format == "json":
        import json as json_mod
        return json_mod.dumps({
            "text": text,
            "audio_file": str(audio_path),
            "duration_seconds": elapsed,
            "language": language or "auto",
            "beam_size": beam_size,
        }, indent=2)

    return text


def cli():
    """CLI entry point for STT."""
    parser = argparse.ArgumentParser(
        prog="voice-ai-stt",
        description="Parakeet-MLX STT — Speech-to-text on Apple Silicon",
    )
    parser.add_argument("audio", help="Audio file to transcribe")
    parser.add_argument(
        "-f", "--format",
        default="text",
        choices=list(OUTPUT_FORMATS),
        help="Output format (default: text)",
    )
    parser.add_argument(
        "-l", "--language",
        default=None,
        help="Language code (default: auto-detect)",
    )
    parser.add_argument(
        "-b", "--beam-size",
        type=int,
        default=1,
        help="Beam size for decoding (default: 1 = greedy)",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Write output to file instead of stdout",
    )
    parser.add_argument(
        "--word-timestamps",
        action="store_true",
        help="Include word-level timestamps (SRT/VTT only)",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress output",
    )

    args = parser.parse_args()

    try:
        result = transcribe(
            audio_path=args.audio,
            language=args.language,
            output_format=args.format,
            beam_size=args.beam_size,
            word_timestamps=args.word_timestamps,
            verbose=not args.quiet,
        )

        if args.output:
            Path(args.output).write_text(result)
            if not args.quiet:
                print(f"   📁 Written to {args.output}")
        else:
            print(result)

    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    cli()
