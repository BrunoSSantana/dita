# Dita

> Voice transcription overlay for Linux. Press a hotkey, speak, get text on clipboard.

![CI](https://github.com/BrunoSSantana/dita/actions/workflows/ci.yml/badge.svg)

Dita opens as a floating, frameless window over your screen. It records from your microphone, transcribes with [faster-whisper](https://github.com/SYSTRAN/faster-whisper), and automatically copies the result to the clipboard. No browser, no cloud, no subscription.

## Features

- Global hotkey (configurable) — one key to open, record, stop, and close
- Local transcription via Whisper (runs fully offline after first setup)
- Auto-copy to clipboard on completion
- Glassmorphism UI, always-on-top, frameless
- Configurable model size, language, and auto-close delay

## Requirements

- Ubuntu / Debian (x86_64)
- Python 3.11+
- System packages: `python3-gi python3-gi-cairo gir1.2-webkit2-4.1 libportaudio2 xclip ffmpeg`

## Install

Download the latest `.deb` from the [Releases](../../releases) page, then:

```bash
sudo dpkg -i dita_*.deb
sudo apt-get install -f   # install any missing system deps
```

The installer creates a Python venv under `/opt/dita/` and downloads the Whisper model (~1.5 GB for `medium`). This takes a few minutes on the first install.

After that, launch Dita from your application menu or run:

```bash
dita
```

## Usage

| Action | Hotkey (default) |
|---|---|
| Open / show window | `Ctrl+Shift+Space` |
| Start recording | `Ctrl+Shift+Space` (window open + idle) |
| Stop & transcribe | `Ctrl+Shift+Space` (while recording) |
| Close window | `Esc` or hotkey when done |

The transcribed text is copied to clipboard automatically. Paste with `Ctrl+V`.

## Configuration

Edit `~/.config/dita/config.json` (created on first run):

```json
{
  "model": "medium",
  "language": "pt",
  "hotkey": "<ctrl>+<shift>+<space>",
  "auto_copy": true,
  "auto_close_after": 3,
  "device": "cpu",
  "compute_type": "int8"
}
```

| Field | Values | Default |
|---|---|---|
| `model` | `tiny` `base` `small` `medium` `large-v3` | `medium` |
| `language` | ISO code or `auto` | `pt` |
| `hotkey` | pynput key string | `<ctrl>+<shift>+<space>` |
| `auto_copy` | `true` / `false` | `true` |
| `auto_close_after` | seconds; `0` = never | `3` |
| `device` | `cpu` / `cuda` | `cpu` |
| `compute_type` | `int8` (cpu) / `float16` (cuda) | `int8` |

## Development

```bash
# Prerequisites
sudo apt install python3-dev python3-gi python3-gi-cairo gir1.2-webkit2-4.1 libportaudio2 xclip

# Install deps (requires uv)
make install

# Run
make run

# Lint & format
make lint
make fmt

# Tests
make test

# Build .deb
bash build-deb.sh
```

> `uv` install: `curl -LsSf https://astral.sh/uv/install.sh | sh`

## License

MIT
