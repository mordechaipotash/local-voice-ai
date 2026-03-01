"""Tests for CLI module."""

import subprocess
import sys


def test_cli_help():
    result = subprocess.run(
        [sys.executable, "-m", "local_voice_ai.cli", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "voice-ai" in result.stdout
    assert "speak" in result.stdout
    assert "transcribe" in result.stdout


def test_cli_version():
    result = subprocess.run(
        [sys.executable, "-m", "local_voice_ai.cli", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "0.1.0" in result.stdout


def test_cli_voices():
    result = subprocess.run(
        [sys.executable, "-m", "local_voice_ai.cli", "voices"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "am_michael" in result.stdout
    assert "af_heart" in result.stdout
