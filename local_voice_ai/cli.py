"""
Unified CLI for local-voice-ai.

Usage:
    voice-ai speak "Hello world"
    voice-ai speak "Hello" --voice af_heart --play
    voice-ai transcribe recording.mp3
    voice-ai transcribe meeting.wav --format srt --beam-size 3
    voice-ai voices
"""

from __future__ import annotations

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="voice-ai",
        description="Local voice AI for Apple Silicon — TTS + STT, no cloud, no API keys",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- speak ---
    speak_parser = subparsers.add_parser(
        "speak", help="Text-to-speech (Kokoro-MLX)"
    )
    speak_parser.add_argument("text", help="Text to speak")
    speak_parser.add_argument(
        "-o", "--output",
        default="/tmp/voice_ai_tts.wav",
        help="Output WAV path (default: /tmp/voice_ai_tts.wav)",
    )
    speak_parser.add_argument(
        "-v", "--voice",
        default="am_michael",
        help="Voice ID (default: am_michael)",
    )
    speak_parser.add_argument(
        "-s", "--speed",
        type=float,
        default=1.6,
        help="Speed multiplier (default: 1.6)",
    )
    speak_parser.add_argument(
        "--play",
        action="store_true",
        help="Play audio after generation (macOS)",
    )
    speak_parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Only output file path",
    )

    # --- transcribe ---
    transcribe_parser = subparsers.add_parser(
        "transcribe", help="Speech-to-text (Parakeet-MLX)"
    )
    transcribe_parser.add_argument("audio", help="Audio file to transcribe")
    transcribe_parser.add_argument(
        "-f", "--format",
        default="text",
        choices=["text", "srt", "vtt", "json"],
        help="Output format (default: text)",
    )
    transcribe_parser.add_argument(
        "-l", "--language",
        default=None,
        help="Language code (default: auto-detect)",
    )
    transcribe_parser.add_argument(
        "-b", "--beam-size",
        type=int,
        default=1,
        help="Beam size (default: 1 = greedy)",
    )
    transcribe_parser.add_argument(
        "-o", "--output",
        default=None,
        help="Write output to file",
    )
    transcribe_parser.add_argument(
        "--word-timestamps",
        action="store_true",
        help="Word-level timestamps (SRT/VTT)",
    )
    transcribe_parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress output",
    )

    # --- voices ---
    subparsers.add_parser("voices", help="List available TTS voices")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "voices":
        from local_voice_ai.tts import VOICES, DEFAULT_VOICE

        print("🎙️  Available voices:\n")
        print(f"  {'Voice':<14} {'Gender':<8} {'Accent':<10} {'Quality'}")
        print(f"  {'─' * 14} {'─' * 8} {'─' * 10} {'─' * 7}")
        for name, info in VOICES.items():
            marker = " ← default" if name == DEFAULT_VOICE else ""
            print(
                f"  {name:<14} {info['gender']:<8} {info['accent']:<10} {info['quality']}{marker}"
            )
        print(f"\nUsage: voice-ai speak \"text\" --voice af_heart")

    elif args.command == "speak":
        from local_voice_ai.tts import speak

        try:
            result = speak(
                text=args.text,
                output=args.output,
                voice=args.voice,
                speed=args.speed,
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

    elif args.command == "transcribe":
        from local_voice_ai.stt import transcribe
        from pathlib import Path

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
                    print(f"📁 Written to {args.output}")
            else:
                print(result)

        except (FileNotFoundError, ValueError, RuntimeError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
