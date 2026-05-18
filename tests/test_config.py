import json

import pytest

import config
from config import DEFAULTS


@pytest.fixture(autouse=True)
def isolate_config(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "CONFIG_PATH", tmp_path / "config.json")


def test_load_defaults_when_file_missing():
    result = config.load_config()
    assert result == DEFAULTS


def test_load_merges_partial_config(tmp_path, monkeypatch):
    cfg_path = tmp_path / "config.json"
    monkeypatch.setattr(config, "CONFIG_PATH", cfg_path)
    cfg_path.write_text(json.dumps({"model": "small"}))

    result = config.load_config()

    assert result["model"] == "small"
    assert result["language"] == DEFAULTS["language"]
    assert result["hotkey"] == DEFAULTS["hotkey"]


def test_load_returns_defaults_on_corrupt_json(tmp_path, monkeypatch):
    cfg_path = tmp_path / "config.json"
    monkeypatch.setattr(config, "CONFIG_PATH", cfg_path)
    cfg_path.write_text("{ not valid json }")

    result = config.load_config()

    assert result == DEFAULTS


def test_save_persists_only_patch_keeps_rest(tmp_path, monkeypatch):
    cfg_path = tmp_path / "config.json"
    monkeypatch.setattr(config, "CONFIG_PATH", cfg_path)

    config.save_config({"model": "large"})
    saved = json.loads(cfg_path.read_text())

    assert saved["model"] == "large"
    assert saved["language"] == DEFAULTS["language"]
    assert saved["auto_copy"] == DEFAULTS["auto_copy"]


def test_save_load_round_trip(tmp_path, monkeypatch):
    cfg_path = tmp_path / "config.json"
    monkeypatch.setattr(config, "CONFIG_PATH", cfg_path)

    patch = {"model": "large", "language": "en", "auto_copy": False}
    config.save_config(patch)
    result = config.load_config()

    assert result["model"] == "large"
    assert result["language"] == "en"
    assert result["auto_copy"] is False
    assert result["hotkey"] == DEFAULTS["hotkey"]
