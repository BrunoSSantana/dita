import pytest

import dita.config as config
from dita.config import DEFAULTS


@pytest.fixture(autouse=True)
def isolate_config(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "CONFIG_PATH", tmp_path / "dita.toml")


def test_load_defaults_when_file_missing():
    result = config.load_config()
    assert result["model"] == DEFAULTS["model"]
    assert result["language"] == DEFAULTS["language"]
    assert result["theme"] == DEFAULTS["theme"]


def test_load_merges_partial_config(tmp_path, monkeypatch):
    cfg_path = tmp_path / "dita.toml"
    monkeypatch.setattr(config, "CONFIG_PATH", cfg_path)
    cfg_path.write_text('model = "small"\n')

    result = config.load_config()

    assert result["model"] == "small"
    assert result["language"] == DEFAULTS["language"]
    assert result["hotkey"] == DEFAULTS["hotkey"]


def test_load_returns_defaults_on_corrupt_toml(tmp_path, monkeypatch):
    cfg_path = tmp_path / "dita.toml"
    monkeypatch.setattr(config, "CONFIG_PATH", cfg_path)
    cfg_path.write_text("this is not valid toml ][[\n")

    result = config.load_config()

    assert result["model"] == DEFAULTS["model"]
    assert result["theme"] == DEFAULTS["theme"]


def test_load_deep_merges_theme_section(tmp_path, monkeypatch):
    cfg_path = tmp_path / "dita.toml"
    monkeypatch.setattr(config, "CONFIG_PATH", cfg_path)
    cfg_path.write_text('[theme]\nname = "light"\naccent = "#ff0000"\n')

    result = config.load_config()

    assert result["theme"]["name"] == "light"
    assert result["theme"]["accent"] == "#ff0000"
    # defaults for other top-level keys still present
    assert result["model"] == DEFAULTS["model"]


def test_load_theme_defaults_when_no_theme_section(tmp_path, monkeypatch):
    cfg_path = tmp_path / "dita.toml"
    monkeypatch.setattr(config, "CONFIG_PATH", cfg_path)
    cfg_path.write_text('model = "tiny"\n')

    result = config.load_config()

    assert result["theme"] == DEFAULTS["theme"]
