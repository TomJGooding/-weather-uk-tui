from pathlib import Path

import pytest

from weather_uk import config


@pytest.fixture
def fake_config_filepath(tmp_path: Path) -> Path:
    return tmp_path / config.APPNAME / "weather-uk.cfg"


def test_template_config_created_if_none_exists(
    fake_config_filepath: Path,
) -> None:
    user_config = config.load_config(fake_config_filepath)

    assert fake_config_filepath.is_file()
    assert user_config.api_key == ""


def test_update_config(fake_config_filepath: Path) -> None:
    old_config = config.load_config(fake_config_filepath)
    assert old_config.api_key == ""

    api_key = "01234567-89ab-cdef-0123-456789abcdef"
    new_config = config.update_config(api_key, fake_config_filepath)
    assert new_config.api_key == api_key
