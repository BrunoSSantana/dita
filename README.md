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

Dita reads `~/.config/dita/dita.toml` on startup. The file is **never written by the app** — create it manually to override defaults.

```toml
# ~/.config/dita/dita.toml

model = "medium"                      # Whisper model size
language = "pt"                       # transcription language
hotkey = "<ctrl>+<shift>+<space>"     # pynput key string
auto_copy = true                      # copy result to clipboard
auto_close_after = 3                  # seconds to close after transcription (0 = never)
device = "cpu"                        # cpu | cuda
compute_type = "int8"                 # int8 | float16 | float32

[theme]
name = "dark"                         # dark | light
# Optional color overrides:
# background = "#1a1a1e"
# surface    = "#2a2a2e"
# text       = "#e2e2e2"
# subtext    = "#888888"
# accent     = "#e05252"
# border     = "rgba(255,255,255,0.08)"
```

### Options

| Key | Type | Default | Description |
|---|---|---|---|
| `model` | string | `medium` | Whisper model: `tiny` `base` `small` `medium` `large-v3` |
| `language` | string | `pt` | ISO language code or `auto` for detection |
| `hotkey` | string | `<ctrl>+<shift>+<space>` | Global hotkey in pynput format |
| `auto_copy` | bool | `true` | Copy transcription to clipboard automatically |
| `auto_close_after` | int | `3` | Seconds before window closes (`0` = never) |
| `device` | string | `cpu` | Inference device: `cpu` or `cuda` |
| `compute_type` | string | `int8` | Quantization: `int8` (cpu), `float16` or `float32` (cuda) |

### `[theme]` section

| Key | Type | Default | Description |
|---|---|---|---|
| `name` | string | `dark` | Base theme: `dark` or `light` |
| `background` | string | *(theme default)* | Main window background color |
| `surface` | string | *(theme default)* | Card / panel background |
| `text` | string | *(theme default)* | Primary text color |
| `subtext` | string | *(theme default)* | Secondary / muted text color |
| `accent` | string | *(theme default)* | Accent / highlight color |
| `border` | string | *(theme default)* | Border color (supports `rgba`) |

Color overrides in `[theme]` are optional — omit any key to use the theme default.

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
