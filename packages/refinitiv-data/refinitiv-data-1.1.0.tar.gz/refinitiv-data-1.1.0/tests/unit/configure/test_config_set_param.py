import pytest

from refinitiv.data import _configure as configure

config_value = "value"

config = configure.get_config()


@pytest.mark.xdist_group(name="config_group")
def test_set_param_to_config():
    try:
        config["param-name"] = config_value
    except Exception as e:
        assert False, e


@pytest.mark.xdist_group(name="config_group")
def test_get_param_from_config():
    try:
        value = config["param-name"]
        assert value == config_value, value
    except Exception as e:
        assert False, e

    try:
        value = config.get_str("param-name")
        assert value == config_value, value
    except Exception as e:
        assert False, e
