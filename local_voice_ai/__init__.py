"""Local voice AI for Apple Silicon — TTS + STT, no cloud, no API keys."""

__version__ = "0.1.0"

from local_voice_ai.tts import speak, list_voices
from local_voice_ai.stt import transcribe

__all__ = ["speak", "transcribe", "list_voices"]
