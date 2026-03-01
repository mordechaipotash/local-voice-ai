"""Tests for STT module."""

import pytest
from local_voice_ai.stt import OUTPUT_FORMATS, transcribe


def test_output_formats():
    assert "text" in OUTPUT_FORMATS
    assert "srt" in OUTPUT_FORMATS
    assert "vtt" in OUTPUT_FORMATS
    assert "json" in OUTPUT_FORMATS


def test_transcribe_file_not_found():
    with pytest.raises(FileNotFoundError):
        transcribe("/nonexistent/audio.wav")


def test_transcribe_invalid_format():
    # Create a dummy file first
    import tempfile
    from pathlib import Path

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(b"fake audio")
        tmp = f.name

    try:
        with pytest.raises(ValueError, match="Unknown format"):
            transcribe(tmp, output_format="mp3")
    finally:
        Path(tmp).unlink()
