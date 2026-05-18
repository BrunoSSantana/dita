import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).parent / "config.json"

DEFAULTS: dict = {
    "model": "medium",
    "language": "pt",
    "hotkey": "<ctrl>+<shift>+<space>",
    "auto_copy": True,
    "auto_close_after": 3,
    "device": "cpu",
    "compute_type": "int8",
}


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        log.warning("config.json not found, using defaults")
        return DEFAULTS.copy()
    try:
        with open(CONFIG_PATH) as f:
            return {**DEFAULTS, **json.load(f)}
    except (json.JSONDecodeError, OSError) as e:
        log.error("failed to read config.json: %s — using defaults", e)
        return DEFAULTS.copy()


def save_config(patch: dict) -> None:
    cfg = load_config()
    cfg.update(patch)
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
