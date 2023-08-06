from unittest import mock

import pytest

import refinitiv.data as rd
from refinitiv.data._config_functions import _load_config_and_set_default
from refinitiv.data._configure import _RDPConfig


@mock.patch("os.path.exists")
def test_load_config(mock_file_exist):
    path = "path/to/file.json"
    result = rd.load_config(path)
    assert result.__class__.__name__ == _RDPConfig.__name__


@mock.patch("os.path.exists")
def test_load_config_and_set_default(mock_file_exist):
    path = "path/to/file.json"
    result = _load_config_and_set_default(path)
    assert result.__class__.__name__ == _RDPConfig.__name__


def test_load_config_error():
    with pytest.raises(FileNotFoundError) as error:
        rd.load_config("path/to/file.json")
    assert "Can't find file: path/to/file.json." in error.value.args[0]


def test_get_config():
    config = rd.get_config()
    assert config.__class__.__name__ == _RDPConfig.__name__


def test_set_param():
    config = rd.get_config()
    config.set_param("custom.param", "custom-value", auto_create=True)
    assert config.get_param("custom.param") == "custom-value"


def test_set_param_error():
    config = rd.get_config()
    with pytest.raises(
        ValueError,
        match="'invalid.param' is not defined in config. "
        "To create new parameter please use 'auto_create' property.",
    ):
        config.set_param("invalid.param", "custom-value")
