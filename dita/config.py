import logging
import tomllib
from pathlib import Path

log = logging.getLogger(__name__)

CONFIG_PATH = Path.home() / ".config" / "dita" / "dita.toml"

DEFAULTS: dict = {
    "model": "medium",
    "language": "pt",
    "hotkey": "<ctrl>+<shift>+<space>",
    "auto_copy": True,
    "auto_close_after": 3,
    "device": "cpu",
    "compute_type": "int8",
    "theme": {"name": "dark"},
}


def _deep_merge(base: dict, override: dict) -> dict:
    result = base.copy()
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        log.warning("%s not found, using defaults", CONFIG_PATH)
        return _deep_merge(DEFAULTS, {})
    try:
        with open(CONFIG_PATH, "rb") as f:
            user = tomllib.load(f)
        return _deep_merge(DEFAULTS, user)
    except tomllib.TOMLDecodeError as e:
        log.error("invalid TOML in %s: %s — using defaults", CONFIG_PATH, e)
        return _deep_merge(DEFAULTS, {})
    except OSError as e:
        log.error("failed to read %s: %s — using defaults", CONFIG_PATH, e)
        return _deep_merge(DEFAULTS, {})
