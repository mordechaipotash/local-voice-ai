# local-voice-ai

**Local voice AI for Apple Silicon — TTS + STT, no cloud, no API keys.**

https://github.com/mordechaipotash/local-voice-ai/raw/main/assets/demo.mp4

---

## Install

```bash
pip install local-voice-ai
```

## Speak

```bash
voice-ai speak "The future of voice is local"
# → output.wav (3 seconds later)
```

## Transcribe

```bash
voice-ai transcribe meeting.wav
# → Full transcript with timestamps
```

That's it. Two models. Two commands. Zero cloud.

---

## What's Inside

| | TTS (Kokoro-MLX) | STT (Parakeet-MLX) |
|---|---|---|
| Model | 82M parameters | 600M parameters |
| Speed | ~3 seconds | Real-time |
| Quality | 24kHz WAV | Word-level timestamps |
| Cost | $0 | $0 |
| Privacy | 100% local | 100% local |

Both models run on Apple Neural Engine via [MLX](https://github.com/ml-explore/mlx). First run downloads the models (~500MB total). After that, everything is offline.

---

## Voices

| Voice | Gender | ID |
|-------|--------|----|
| Heart | Female | `af_heart` |
| Bella | Female | `af_bella` |
| Alice | British F | `bf_alice` |
| Michael | Male | `am_michael` |
| Fenrir | Male | `am_fenrir` |

```bash
voice-ai speak "Hello world" --voice af_heart --output hello.wav
```

---

## Output Formats (STT)

```bash
voice-ai transcribe audio.wav                    # Plain text
voice-ai transcribe audio.wav --format srt       # Subtitles
voice-ai transcribe audio.wav --format vtt       # Web subtitles
voice-ai transcribe audio.wav --format json      # Structured
```

---

## Requirements

- Apple Silicon Mac (M1/M2/M3/M4)
- Python 3.11+
- ~500MB disk (models)
- ~2GB RAM

---

## Part of the ecosystem

[brain-mcp](https://github.com/mordechaipotash/brain-mcp) · [agent-memory-loop](https://github.com/mordechaipotash/agent-memory-loop) · [mordenews](https://github.com/mordechaipotash/mordenews) · [live-translate](https://github.com/mordechaipotash/live-translate)

## License

MIT
