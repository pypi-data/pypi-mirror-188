from importlib import reload
from refinitiv.data import _configure as configure


def test_config_import():
    reload(configure)

    assert configure._config is None
