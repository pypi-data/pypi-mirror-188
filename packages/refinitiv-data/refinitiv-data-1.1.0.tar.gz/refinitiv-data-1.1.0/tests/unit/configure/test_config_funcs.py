from refinitiv.data import _configure as configure


def test_get_config():
    # when
    result = configure.get_config()

    # then
    assert result is not None
    assert result is configure._config


def test_get_config_file():
    configure.reload()

    path = configure._get_filepath(None, None)

    assert path is None
