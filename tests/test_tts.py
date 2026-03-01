"""Tests for TTS module."""

import pytest
from local_voice_ai.tts import VOICES, list_voices, DEFAULT_VOICE, DEFAULT_SPEED


def test_voices_dict_not_empty():
    assert len(VOICES) > 0


def test_list_voices_returns_copy():
    voices = list_voices()
    assert voices == VOICES
    # Ensure it's a copy, not the original
    voices["fake_voice"] = {}
    assert "fake_voice" not in VOICES


def test_default_voice_exists():
    assert DEFAULT_VOICE in VOICES


def test_default_speed():
    assert DEFAULT_SPEED == 1.6


def test_all_voices_have_metadata():
    for name, info in VOICES.items():
        assert "gender" in info, f"{name} missing gender"
        assert "accent" in info, f"{name} missing accent"
        assert "quality" in info, f"{name} missing quality"


def test_speak_invalid_voice():
    from local_voice_ai.tts import speak
    with pytest.raises(ValueError, match="Unknown voice"):
        speak("test", voice="nonexistent_voice")


def test_voice_ids():
    expected = {"af_heart", "af_bella", "bf_alice", "am_fenrir", "am_michael"}
    assert set(VOICES.keys()) == expected
