"""
Kokoro-MLX TTS — Text-to-speech on Apple Silicon.

Uses mlx-community/Kokoro-82M-bf16 via mlx-audio.
~3 second generation, 1.6GB memory, 24kHz WAV output.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Optional

# Default configuration
DEFAULT_MODEL = "mlx-community/Kokoro-82M-bf16"
DEFAULT_VOICE = "am_michael"
DEFAULT_SPEED = 1.6
DEFAULT_LANG = "a"  # American English

# Available voices with metadata
VOICES = {
    "af_heart":   {"gender": "female", "accent": "American", "quality": "A"},
    "af_bella":   {"gender": "female", "accent": "American", "quality": "A-"},
    "bf_alice":   {"gender": "female", "accent": "British",  "quality": "A"},
    "am_fenrir":  {"gender": "male",   "accent": "American", "quality": "C+"},
    "am_michael": {"gender": "male",   "accent": "American", "quality": "C+"},
}


def list_voices() -> dict:
    """Return available voices with metadata."""
    return VOICES.copy()


def speak(
    text: str,
    output: Optional[str | Path] = None,
    voice: str = DEFAULT_VOICE,
    speed: float = DEFAULT_SPEED,
    model: str = DEFAULT_MODEL,
    lang_code: str = DEFAULT_LANG,
    verbose: bool = False,
) -> Path:
    """
    Generate speech from text using Kokoro-MLX.

    Args:
        text: Text to speak.
        output: Output WAV path. Defaults to /tmp/voice_ai_tts.wav.
        voice: Voice ID (see VOICES dict).
        speed: Playback speed multiplier. Default 1.6x.
        model: HuggingFace model ID.
        lang_code: Language code ('a' = American English).
        verbose: Print generation details.

    Returns:
        Path to the generated WAV file.

    Raises:
        ValueError: If voice is not recognized.
        RuntimeError: If generation fails.
    """
    if voice not in VOICES:
        raise ValueError(
            f"Unknown voice '{voice}'. Available: {', '.join(VOICES.keys())}"
        )

    if output is None:
        output = Path("/tmp/voice_ai_tts.wav")
    else:
        output = Path(output)

    output.parent.mkdir(parents=True, exist_ok=True)

    # mlx-audio appends _000.wav to the prefix, so we strip .wav
    file_prefix = str(output.with_suffix(""))

    if verbose:
        print(f"🎙️  Generating speech with {voice} @ {speed}x...")
        print(f"   Model: {model}")
        print(f"   Text: {text[:80]}{'...' if len(text) > 80 else ''}")

    t0 = time.perf_counter()

    try:
        from mlx_audio.tts.generate import generate_audio

        generate_audio(
            text,
            model=model,
            voice=voice,
            speed=speed,
            lang_code=lang_code,
            file_prefix=file_prefix,
            join_audio=True,
            verbose=False,
        )
    except ImportError:
        raise RuntimeError(
            "mlx-audio is not installed. Run: pip install mlx-audio"
        )
    except Exception as e:
        raise RuntimeError(f"TTS generation failed: {e}")

    # Handle mlx-audio's _000 suffix naming
    if not output.exists():
        suffixed = Path(f"{file_prefix}_000.wav")
        if suffixed.exists():
            suffixed.rename(output)

    elapsed = time.perf_counter() - t0

    if not output.exists():
        raise RuntimeError(f"Generation produced no output at {output}")

    if verbose:
        size_kb = output.stat().st_size / 1024
        print(f"   ✅ Generated in {elapsed:.1f}s ({size_kb:.0f} KB)")
        print(f"   📁 {output}")

    return output


def cli():
    """CLI entry point for TTS."""
    parser = argparse.ArgumentParser(
        prog="voice-ai-tts",
        description="Kokoro-MLX TTS — Text-to-speech on Apple Silicon",
    )
    parser.add_argument("text", help="Text to speak")
    parser.add_argument(
        "-o", "--output",
        default="/tmp/voice_ai_tts.wav",
        help="Output WAV file path (default: /tmp/voice_ai_tts.wav)",
    )
    parser.add_argument(
        "-v", "--voice",
        default=DEFAULT_VOICE,
        choices=list(VOICES.keys()),
        help=f"Voice to use (default: {DEFAULT_VOICE})",
    )
    parser.add_argument(
        "-s", "--speed",
        type=float,
        default=DEFAULT_SPEED,
        help=f"Speed multiplier (default: {DEFAULT_SPEED})",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model ID (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="List available voices and exit",
    )
    parser.add_argument(
        "--play",
        action="store_true",
        help="Play audio after generation (macOS only)",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress output except the file path",
    )

    args = parser.parse_args()

    if args.list_voices:
        print("Available voices:")
        print(f"  {'Voice':<14} {'Gender':<8} {'Accent':<10} {'Quality'}")
        print(f"  {'─'*14} {'─'*8} {'─'*10} {'─'*7}")
        for name, info in VOICES.items():
            marker = " ← default" if name == DEFAULT_VOICE else ""
            print(f"  {name:<14} {info['gender']:<8} {info['accent']:<10} {info['quality']}{marker}")
        sys.exit(0)

    try:
        result = speak(
            text=args.text,
            output=args.output,
            voice=args.voice,
            speed=args.speed,
            model=args.model,
            verbose=not args.quiet,
        )

        if args.play:
            import subprocess
            subprocess.run(["afplay", str(result)], check=True)

        if args.quiet:
            print(result)

    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    cli()
